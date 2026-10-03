from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, stdev

from scripts.evaluate_pedicularis_predator_method import (
    _binary,
    _num,
    read_rows,
)
from scripts.scale_free_relative import relative_change


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot summarize empty values")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    weight = pos - lo
    return ordered[lo] * (1.0 - weight) + ordered[hi] * weight


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        raise ValueError("cannot summarize empty values")
    return {
        "n": len(values),
        "mean": mean(values),
        "sd": stdev(values) if len(values) >= 2 else None,
        "min": min(values),
        "q05": _quantile(values, 0.05),
        "median": _quantile(values, 0.50),
        "q95": _quantile(values, 0.95),
        "max": max(values),
    }


def _context(rows: list[dict[str, str]]) -> tuple[str, str]:
    contexts = {(row["population_id"], row["season_id"]) for row in rows}
    if len(contexts) != 1:
        raise ValueError("one G device screen must contain one population and season")
    return next(iter(contexts))


def _initial_seed(row: dict[str, str]) -> float:
    ovules = _num(row, "ovule_count")
    if ovules <= 0:
        raise ValueError("ovule_count must be > 0")
    return (
        _num(row, "undamaged_seed_count")
        + _num(row, "damaged_seed_count")
    ) / ovules


def _final_seed(row: dict[str, str]) -> float:
    ovules = _num(row, "ovule_count")
    if ovules <= 0:
        raise ValueError("ovule_count must be > 0")
    return _num(row, "undamaged_seed_count") / ovules


def _predation(row: dict[str, str]) -> float:
    total = (
        _num(row, "undamaged_seed_count")
        + _num(row, "damaged_seed_count")
    )
    if total <= 0:
        return 0.0
    return _num(row, "damaged_seed_count") / total


def _mean_rows(rows: list[dict[str, str]], field: str) -> float:
    return mean(_num(row, field) for row in rows)


def _mean_binary(rows: list[dict[str, str]], field: str) -> float:
    return mean(_binary(row, field) for row in rows)


def _paired_metrics(
    exposed_rows: list[dict[str, str]],
    excluded_rows: list[dict[str, str]],
) -> dict[str, float]:
    exp_attack = _mean_binary(exposed_rows, "early_predator_attack_present")
    exc_attack = _mean_binary(excluded_rows, "early_predator_attack_present")
    exp_pred = mean(_predation(row) for row in exposed_rows)
    exc_pred = mean(_predation(row) for row in excluded_rows)
    exp_final = mean(_final_seed(row) for row in exposed_rows)
    exc_final = mean(_final_seed(row) for row in excluded_rows)
    exp_initial = mean(_initial_seed(row) for row in exposed_rows)
    exc_initial = mean(_initial_seed(row) for row in excluded_rows)

    def rel(field: str) -> float:
        return relative_change(
            _mean_rows(excluded_rows, field),
            _mean_rows(exposed_rows, field),
        )

    return {
        "attack_reduction": exp_attack - exc_attack,
        "predation_reduction": exp_pred - exc_pred,
        "final_seed_gain": exc_final - exp_final,
        "initial_seed_abs_difference": abs(exc_initial - exp_initial),
        "pollen_relative_change": rel("pollen_grains"),
        "pollinator_visit_relative_change": rel("pollinator_visits"),
        "z_relative_change": rel("realized_exsertion"),
        "water_depth_abs_difference": abs(
            _mean_rows(excluded_rows, "water_depth")
            - _mean_rows(exposed_rows, "water_depth")
        ),
        "damage_rate_abs_difference": abs(
            _mean_binary(excluded_rows, "mechanical_damage")
            - _mean_binary(exposed_rows, "mechanical_damage")
        ),
    }


def _method_rows(
    rows: list[dict[str, str]],
    method: str,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[str]]:
    excluded = [
        row
        for row in rows
        if row["predator_treatment"] == "EXCLUDED"
        and row["exclusion_method"] == method
    ]
    plants = {row["plant_id"] for row in excluded}
    exposed = [
        row
        for row in rows
        if row["predator_treatment"] == "EXPOSED"
        and row["plant_id"] in plants
    ]
    paired = sorted(
        plant
        for plant in plants
        if any(row["plant_id"] == plant for row in exposed)
    )
    return exposed, excluded, paired


def _screen_method(
    rows: list[dict[str, str]],
    method: str,
) -> dict:
    exposed, excluded, paired_plants = _method_rows(rows, method)
    if not excluded:
        raise ValueError(f"method {method!r} has no EXCLUDED rows")

    exposed_by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    excluded_by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in exposed:
        exposed_by_plant[row["plant_id"]].append(row)
    for row in excluded:
        excluded_by_plant[row["plant_id"]].append(row)

    pair_metrics = []
    for plant in paired_plants:
        if not exposed_by_plant[plant] or not excluded_by_plant[plant]:
            continue
        pair_metrics.append(
            _paired_metrics(
                exposed_by_plant[plant],
                excluded_by_plant[plant],
            )
        )

    if not pair_metrics:
        raise ValueError(
            f"method {method!r} has no plant-level EXPOSED/EXCLUDED pairs"
        )

    delays = [
        _num(row, "barrier_application_time_hours")
        - _num(row, "anthesis_time_hours")
        for row in excluded
    ]

    hard_failures = {
        "pollination_window_incomplete": sum(
            1 - _binary(row, "pollination_window_complete_before_barrier")
            for row in excluded
        ),
        "ovary_swollen_at_barrier": sum(
            _binary(row, "ovary_swollen_at_barrier")
            for row in excluded
        ),
        "pollinator_entry_covered": sum(
            _binary(row, "barrier_covers_pollinator_entry")
            for row in excluded
        ),
        "pre_barrier_attack_present": sum(
            _binary(row, "pre_barrier_attack_present")
            for row in excluded
        ),
        "barrier_integrity_failure": sum(
            _binary(row, "barrier_integrity_failure_present")
            for row in excluded
        ),
        "exposed_missing_sham": sum(
            1 - _binary(row, "sham_device_applied")
            for row in exposed
        ),
    }

    hard_validity_pass = all(value == 0 for value in hard_failures.values())

    metric_names = (
        "attack_reduction",
        "predation_reduction",
        "final_seed_gain",
        "initial_seed_abs_difference",
        "pollen_relative_change",
        "pollinator_visit_relative_change",
        "z_relative_change",
        "water_depth_abs_difference",
        "damage_rate_abs_difference",
    )

    return {
        "exclusion_method": method,
        "n_excluded_rows": len(excluded),
        "n_exposed_rows_on_paired_plants": len(exposed),
        "n_paired_plants": len(paired_plants),
        "paired_plant_ids": paired_plants,
        "barrier_delay_hours": _summary(delays),
        "hard_failure_counts": hard_failures,
        "hard_validity_pass": hard_validity_pass,
        "plant_level_distributions": {
            field: _summary(
                [float(record[field]) for record in pair_metrics]
            )
            for field in metric_names
        },
        "status": (
            "G_DEVICE_HARD_VALIDITY_ADMISSIBLE"
            if hard_validity_pass
            else "G_DEVICE_REJECTED_HARD_VALIDITY"
        ),
    }


def build(rows: list[dict[str, str]]) -> dict:
    population_id, season_id = _context(rows)
    methods = sorted(
        {
            row["exclusion_method"]
            for row in rows
            if row["predator_treatment"] == "EXCLUDED"
        }
    )
    if not methods:
        raise ValueError("G device screen requires at least one EXCLUDED method")

    exposed = [
        row for row in rows
        if row["predator_treatment"] == "EXPOSED"
    ]
    if not exposed:
        raise ValueError("G device screen requires EXPOSED sham controls")

    method_results = {
        method: _screen_method(rows, method)
        for method in methods
    }
    admissible = sorted(
        method
        for method, result in method_results.items()
        if result["hard_validity_pass"]
    )
    rejected = sorted(set(methods) - set(admissible))

    return {
        "receipt_schema_version": "SCH_PEDICULARIS_G_DEVICE_SCREEN_V1",
        "analysis": "pedicularis_g_exploratory_device_screen",
        "population_id": population_id,
        "season_id": season_id,
        "n_candidate_methods": len(methods),
        "candidate_methods": methods,
        "n_admissible_methods": len(admissible),
        "admissible_methods": admissible,
        "rejected_methods": rejected,
        "method_results": method_results,
        "status": (
            "G_DEVICE_SCREEN_HAS_ADMISSIBLE_METHOD"
            if admissible
            else "G_DEVICE_SCREEN_NO_ADMISSIBLE_METHOD"
        ),
        "thresholds_applied": False,
        "effectiveness_pass_fail_applied": False,
        "confirmatory_receipt_generated": False,
        "claim_ceiling": [
            "exploratory_method_screen_only",
            "hard_method_validity_can_reject_a_device_before_threshold_freeze",
            "effect_size_distributions_are_descriptive_not_pass_fail",
            "does_not_select_CAL_B_targets",
            "does_not_validate_registered_G",
            "admissible_method_still_requires_manual_selection_and_prospective_freeze",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Screen exploratory Pedicularis G barrier methods for hard physical "
            "validity without applying effect-size or F0 thresholds"
        )
    )
    parser.add_argument("g_exploratory_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(read_rows(args.g_exploratory_csv))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

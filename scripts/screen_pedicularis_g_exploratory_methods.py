from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, stdev

from scripts import evaluate_pedicularis_predator_method as gmethod
from scripts import evaluate_pedicularis_predator_weight as gweight


HARD_VALIDITY_FIELDS = {
    "pollination_window_complete": (
        "pollination_window_complete_before_barrier",
        lambda value: int(value) == 1,
    ),
    "ovary_not_swollen": (
        "ovary_swollen_at_barrier",
        lambda value: int(value) == 0,
    ),
    "pollinator_entry_preserved": (
        "barrier_covers_pollinator_entry",
        lambda value: int(value) == 0,
    ),
    "no_pre_barrier_attack": (
        "pre_barrier_attack_present",
        lambda value: int(value) == 0,
    ),
    "barrier_integrity_preserved": (
        "barrier_integrity_failure_present",
        lambda value: int(value) == 0,
    ),
}


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot summarize empty values")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    w = pos - lo
    return ordered[lo] * (1 - w) + ordered[hi] * w


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
    pops = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(pops) != 1 or len(seasons) != 1:
        raise ValueError(
            "one G method screen must contain exactly one population and season"
        )
    return next(iter(pops)), next(iter(seasons))


def _candidate_methods(rows: list[dict[str, str]]) -> list[str]:
    methods = sorted(
        {
            row["exclusion_method"]
            for row in rows
            if row["predator_treatment"] == "EXCLUDED"
        }
    )
    if not methods:
        raise ValueError("G method screen requires at least one EXCLUDED method")
    return methods


def _paired_subset(
    rows: list[dict[str, str]],
    method: str,
) -> list[dict[str, str]]:
    exposed_by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    excluded_by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        if row["predator_treatment"] == "EXPOSED":
            exposed_by_plant[row["plant_id"]].append(row)
        elif (
            row["predator_treatment"] == "EXCLUDED"
            and row["exclusion_method"] == method
        ):
            excluded_by_plant[row["plant_id"]].append(row)

    plants = sorted(set(exposed_by_plant) & set(excluded_by_plant))
    subset: list[dict[str, str]] = []
    for plant in plants:
        subset.extend(exposed_by_plant[plant])
        subset.extend(excluded_by_plant[plant])
    return subset


def _hard_validity(
    *,
    method_rows: list[dict[str, str]],
    exposed_rows: list[dict[str, str]],
) -> tuple[dict[str, bool], dict[str, int]]:
    flags = {}
    failures = {}

    for flag, (field, predicate) in HARD_VALIDITY_FIELDS.items():
        n_fail = sum(
            not predicate(row[field])
            for row in method_rows
        )
        failures[flag] = n_fail
        flags[flag] = n_fail == 0

    n_bad_sham = sum(
        int(row["sham_device_applied"]) != 1
        for row in exposed_rows
    )
    failures["exposed_sham_handling"] = n_bad_sham
    flags["exposed_sham_handling"] = n_bad_sham == 0

    return flags, failures


def _method_screen(
    rows: list[dict[str, str]],
    method: str,
) -> dict:
    excluded = [
        row
        for row in rows
        if row["predator_treatment"] == "EXCLUDED"
        and row["exclusion_method"] == method
    ]
    if not excluded:
        raise ValueError(f"no EXCLUDED rows for method {method!r}")

    subset = _paired_subset(rows, method)
    plants = sorted({row["plant_id"] for row in subset})
    if len(plants) < 2:
        raise ValueError(
            f"method {method!r} needs >=2 plants with EXPOSED and EXCLUDED rows"
        )

    exposed = [
        row
        for row in subset
        if row["predator_treatment"] == "EXPOSED"
    ]
    paired_excluded = [
        row
        for row in subset
        if row["predator_treatment"] == "EXCLUDED"
    ]

    hard_flags, hard_failures = _hard_validity(
        method_rows=paired_excluded,
        exposed_rows=exposed,
    )

    delays = [
        float(row["barrier_application_time_hours"])
        - float(row["anthesis_time_hours"])
        for row in paired_excluded
    ]
    if any(delay < 0 for delay in delays):
        raise ValueError("barrier delay cannot be negative")

    pairs = gweight._plant_pairs(subset)
    if len(pairs) != len(plants):
        raise ValueError(
            f"method {method!r} paired-plant summary lost plants"
        )

    effect_fields = (
        "attack_reduction",
        "predation_reduction",
        "final_seed_gain",
    )
    contamination_fields = (
        "initial_seed_abs_difference",
        "pollen_relative_change",
        "pollinator_visit_relative_change",
        "z_relative_change",
        "water_depth_abs_difference",
        "damage_rate_abs_difference",
    )

    hard_pass = all(hard_flags.values())

    return {
        "method": method,
        "n_paired_plants": len(plants),
        "n_exposed_rows_in_paired_plants": len(exposed),
        "n_excluded_rows": len(paired_excluded),
        "paired_plant_ids": plants,
        "barrier_delay_hours": _summary(delays),
        "hard_validity_flags": hard_flags,
        "hard_validity_failure_counts": hard_failures,
        "hard_validity_all_pass": hard_pass,
        "effect_distributions": {
            field: _summary([float(pair[field]) for pair in pairs])
            for field in effect_fields
        },
        "contamination_distributions": {
            field: _summary([float(pair[field]) for pair in pairs])
            for field in contamination_fields
        },
        "screen_state": (
            "HARD_VALIDITY_PASS_EFFECT_AND_SELECTIVITY_TARGETS_UNFROZEN"
            if hard_pass
            else "HARD_VALIDITY_FAIL_METHOD_SHOULD_NOT_ADVANCE_AS_IS"
        ),
    }


def build(rows: list[dict[str, str]]) -> dict:
    population_id, season_id = _context(rows)
    methods = _candidate_methods(rows)

    screens = {
        method: _method_screen(rows, method)
        for method in methods
    }
    hard_pass_methods = sorted(
        method
        for method, result in screens.items()
        if result["hard_validity_all_pass"]
    )

    if not hard_pass_methods:
        frontier = "NO_METHOD_PASSES_REGISTERED_HARD_VALIDITY"
    elif len(hard_pass_methods) == 1:
        frontier = (
            "ONE_METHOD_PASSES_HARD_VALIDITY_"
            "EFFECT_AND_SELECTIVITY_TARGETS_STILL_UNFROZEN"
        )
    else:
        frontier = (
            "MULTIPLE_METHODS_PASS_HARD_VALIDITY_"
            "NO_AUTOMATIC_METHOD_SELECTION"
        )

    return {
        "analysis": "pedicularis_g_exploratory_method_screen_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_candidate_methods": len(methods),
        "candidate_methods": methods,
        "n_hard_validity_pass_methods": len(hard_pass_methods),
        "hard_validity_pass_methods": hard_pass_methods,
        "method_screens": screens,
        "current_frontier": frontier,
        "effect_thresholds_applied": False,
        "selectivity_thresholds_applied": False,
        "method_selected": False,
        "confirmatory_receipt_generated": False,
        "status": "G_EXPLORATORY_FAIL_FAST_SCREEN_ONLY",
        "claim_ceiling": [
            "registered_hard_method_validity_only",
            "effect_and_selectivity_distributions_are_descriptive",
            "does_not_choose_minimum_predator_effect",
            "does_not_choose_equivalence_margins",
            "does_not_select_one_method_when_multiple_pass",
            "does_not_validate_registered_G",
            "does_not_generate_confirmatory_receipt",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Screen multiple exploratory P. rex seed-predator barrier methods "
            "using registered hard validity checks but no effect/selectivity thresholds"
        )
    )
    parser.add_argument("g_v4_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(gmethod.read_rows(args.g_v4_csv))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

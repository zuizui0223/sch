from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, stdev

from scripts import evaluate_pedicularis_stage_p0 as p0
from scripts import evaluate_pedicularis_pollination_weight as p1
from scripts import evaluate_pedicularis_predator_method as gmethod
from scripts import evaluate_pedicularis_predator_weight as gweight
from scripts.scale_free_relative import relative_change


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot summarize an empty value set")
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    weight = pos - lo
    return ordered[lo] * (1 - weight) + ordered[hi] * weight


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        raise ValueError("cannot summarize an empty value set")
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


def _context_from_rows(rows: list[dict[str, str]]) -> tuple[str, str]:
    populations = {row["population_id"] for row in rows}
    seasons = {row["season_id"] for row in rows}
    if len(populations) != 1 or len(seasons) != 1:
        raise ValueError("one calibration input must contain one population and season")
    return next(iter(populations)), next(iter(seasons))


def _p0_plant_gap_distributions(rows: list[dict[str, str]]) -> dict[str, dict]:
    by_plant: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    labels: dict[int, str] = {}
    for row in rows:
        rank = int(row["assigned_z_rank"])
        by_plant[row["plant_id"]][rank].append(float(row["realized_exsertion"]))
        labels[rank] = row["assigned_z_level"]

    all_ranks = sorted(labels)
    transitions: dict[str, list[float]] = defaultdict(list)
    for plant, ranks in by_plant.items():
        if not all(rank in ranks for rank in all_ranks):
            continue
        means = {rank: mean(ranks[rank]) for rank in all_ranks}
        for left, right in zip(all_ranks, all_ranks[1:]):
            key = f"{labels[left]}->{labels[right]}"
            transitions[key].append(means[right] - means[left])

    return {
        transition: _summary(values)
        for transition, values in sorted(transitions.items())
        if values
    }


def _summarize_p0(path: Path) -> tuple[dict, tuple[str, str]]:
    rows = p0._read_csv(path)
    context = _context_from_rows(rows)
    rank_metrics = p0._rank_metrics(rows)
    off_target = p0._offtarget_metrics(rows)
    groups = p0._group_by_rank(rows)
    return {
        "n_rows": len(rows),
        "n_plants": len({row["plant_id"] for row in rows}),
        "n_assigned_z_levels": len(groups),
        "realized_exsertion_mean_by_rank": {
            str(rank): value for rank, value in rank_metrics["means"].items()
        },
        "observed_adjacent_gaps": rank_metrics["adjacent_gaps"],
        "observed_minimum_adjacent_gap": rank_metrics["minimum_adjacent_gap"],
        "plant_level_adjacent_gap_distributions": _p0_plant_gap_distributions(rows),
        "off_target_observed": off_target,
        "pollinator_visits_mean_by_rank": {
            str(rank): p0._mean_field(group, "pollinator_visits")
            for rank, group in groups.items()
        },
        "pollen_grains_mean_by_rank": {
            str(rank): p0._mean_field(group, "pollen_grains")
            for rank, group in groups.items()
        },
        "interpretation": (
            "CAL-A evidence only: observed manipulation separation and off-target "
            "variation are summarized without selecting a threshold."
        ),
    }, context


def _p1_plant_metrics(rows: list[dict[str, str]]) -> list[dict[str, float | str]]:
    plants = p1._paired_plants(rows)
    out = []
    for plant in plants:
        natural = [
            row for row in rows
            if row["plant_id"] == plant and row["pollination_treatment"] == "NATURAL"
        ]
        supplemented = [
            row for row in rows
            if row["plant_id"] == plant and row["pollination_treatment"] == "SUPPLEMENTED"
        ]

        def m(group, fn):
            return mean(fn(row) for row in group)

        nat_initial = m(natural, p1._initial_seed_set)
        sup_initial = m(supplemented, p1._initial_seed_set)
        nat_pollen = m(natural, lambda r: p1._num(r, "pollen_grains_post_treatment"))
        sup_pollen = m(supplemented, lambda r: p1._num(r, "pollen_grains_post_treatment"))
        nat_attack = m(natural, lambda r: float(p1._binary(r, "early_predator_attack_present")))
        sup_attack = m(supplemented, lambda r: float(p1._binary(r, "early_predator_attack_present")))
        nat_damage = m(natural, lambda r: float(p1._binary(r, "mechanical_damage")))
        sup_damage = m(supplemented, lambda r: float(p1._binary(r, "mechanical_damage")))

        def rel(field: str) -> float:
            nat = m(natural, lambda r, f=field: p1._num(r, f))
            sup = m(supplemented, lambda r, f=field: p1._num(r, f))
            return relative_change(sup, nat)

        out.append({
            "plant_id": plant,
            "initial_seed_set_delta": sup_initial - nat_initial,
            "pollen_grains_delta": sup_pollen - nat_pollen,
            "early_predator_attack_abs_difference": abs(sup_attack - nat_attack),
            "z_relative_change": rel("realized_exsertion"),
            "bract_height_relative_change": rel("bract_height"),
            "opening_width_relative_change": rel("corolla_opening_width"),
            "water_depth_abs_difference": abs(
                m(supplemented, lambda r: p1._num(r, "water_depth"))
                - m(natural, lambda r: p1._num(r, "water_depth"))
            ),
            "mechanical_damage_abs_difference": abs(sup_damage - nat_damage),
        })
    return out


def _summarize_p1(path: Path) -> tuple[dict, tuple[str, str]]:
    rows = p1._read_csv(path)
    context = _context_from_rows(rows)
    plant_metrics = _p1_plant_metrics(rows)
    if len(plant_metrics) < 2:
        raise ValueError("CAL-B P1 summary requires at least two paired plants")
    fields = [
        "initial_seed_set_delta",
        "pollen_grains_delta",
        "early_predator_attack_abs_difference",
        "z_relative_change",
        "bract_height_relative_change",
        "opening_width_relative_change",
        "water_depth_abs_difference",
        "mechanical_damage_abs_difference",
    ]
    return {
        "n_rows": len(rows),
        "n_paired_plants": len(plant_metrics),
        "plant_level_distributions": {
            field: _summary([float(row[field]) for row in plant_metrics])
            for field in fields
        },
        "interpretation": (
            "CAL-A/CAL-B exploratory evidence only: effect and contamination "
            "distributions are summarized without defining minimum effects or "
            "equivalence margins."
        ),
    }, context


def _summarize_g(path: Path) -> tuple[dict, tuple[str, str]]:
    rows = gmethod.read_rows(path)
    context = _context_from_rows(rows)
    excluded = [row for row in rows if row["predator_treatment"] == "EXCLUDED"]
    if not excluded:
        raise ValueError("CAL-B G summary requires EXCLUDED rows")

    delays = [
        float(row["barrier_application_time_hours"])
        - float(row["anthesis_time_hours"])
        for row in excluded
    ]
    method_counts = Counter(row["exclusion_method"] for row in excluded)
    pairs = gweight._plant_pairs(rows)
    if len(pairs) < 2:
        raise ValueError("CAL-B G summary requires at least two paired plants")

    pair_fields = [
        "attack_reduction",
        "predation_reduction",
        "final_seed_gain",
        "initial_seed_abs_difference",
        "pollen_relative_change",
        "pollinator_visit_relative_change",
        "z_relative_change",
        "water_depth_abs_difference",
        "damage_rate_abs_difference",
    ]

    return {
        "n_rows": len(rows),
        "n_paired_plants": len(pairs),
        "excluded_method_counts": dict(sorted(method_counts.items())),
        "barrier_delay_hours": _summary(delays),
        "excluded_pollination_window_complete_rate": mean(
            int(row["pollination_window_complete_before_barrier"])
            for row in excluded
        ),
        "excluded_ovary_not_swollen_rate": mean(
            1 - int(row["ovary_swollen_at_barrier"])
            for row in excluded
        ),
        "excluded_pollinator_entry_preserved_rate": mean(
            1 - int(row["barrier_covers_pollinator_entry"])
            for row in excluded
        ),
        "plant_level_distributions": {
            field: _summary([float(row[field]) for row in pairs])
            for field in pair_fields
        },
        "interpretation": (
            "CAL-A/CAL-B exploratory evidence only: timing, effectiveness and "
            "selectivity distributions are summarized without qualifying a G "
            "method or setting confirmatory thresholds."
        ),
    }, context


def build(
    *,
    p0_path: Path | None = None,
    p1_path: Path | None = None,
    g_path: Path | None = None,
) -> dict:
    if p0_path is None and p1_path is None and g_path is None:
        raise ValueError("at least one calibration pilot input is required")

    summaries = {}
    contexts = set()

    if p0_path is not None:
        summaries["P0"] , context = _summarize_p0(p0_path)
        contexts.add(context)
    if p1_path is not None:
        summaries["P1"], context = _summarize_p1(p1_path)
        contexts.add(context)
    if g_path is not None:
        summaries["G"], context = _summarize_g(g_path)
        contexts.add(context)

    if len(contexts) != 1:
        raise ValueError(
            "all supplied calibration pilots must target the same population and season"
        )
    population_id, season_id = next(iter(contexts))

    return {
        "analysis": "pedicularis_calibration_pilot_summary_v1",
        "population_id": population_id,
        "season_id": season_id,
        "available_pilot_lanes": sorted(summaries),
        "pilot_summaries": summaries,
        "calibration_modules_supported": {
            "CAL_A": sorted(
                lane for lane in summaries
                if lane in {"P0", "P1", "G"}
            ),
            "CAL_B": sorted(
                lane for lane in summaries
                if lane in {"P1", "G"}
            ),
            "CAL_C": (
                "PILOT_VARIANCE_INPUTS_ONLY_NOT_SAMPLE_SIZE_DECISIONS"
            ),
        },
        "status": "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION",
        "thresholds_selected": False,
        "confirmatory_receipt_generated": False,
        "claim_ceiling": [
            "descriptive_calibration_only",
            "does_not_set_equivalence_margin",
            "does_not_set_minimum_effect",
            "does_not_set_sample_size",
            "does_not_validate_P0_P1_or_G",
            "pilot_rows_must_not_be_reused_as_confirmatory_rows",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize nonconfirmatory Pedicularis calibration pilots without applying thresholds"
    )
    parser.add_argument("--p0", type=Path)
    parser.add_argument("--p1", type=Path)
    parser.add_argument("--g", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(p0_path=args.p0, p1_path=args.p1, g_path=args.g)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

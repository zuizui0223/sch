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


def _p0_plant_gate_metrics(rows: list[dict[str, str]]) -> list[dict[str, float | str]]:
    by_plant: dict[str, dict[int, list[dict[str, str]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    rank_labels: dict[int, str] = {}
    sham_rows = p0._sham_rows(rows)
    sham_rank = int(sham_rows[0]["assigned_z_rank"])

    for row in rows:
        rank = int(row["assigned_z_rank"])
        by_plant[row["plant_id"]][rank].append(row)
        rank_labels[rank] = row["assigned_z_level"]

    all_ranks = sorted(rank_labels)
    out: list[dict[str, float | str]] = []

    def group_mean(group: list[dict[str, str]], field: str) -> float:
        return mean(float(row[field]) for row in group)

    def group_binary_mean(group: list[dict[str, str]], field: str) -> float:
        return mean(float(int(row[field])) for row in group)

    for plant_id, rank_rows in sorted(by_plant.items()):
        if not all(rank in rank_rows for rank in all_ranks):
            continue
        sham = rank_rows[sham_rank]
        sham_means = {
            field: group_mean(sham, field)
            for field in (
                "corolla_opening_width",
                "tube_diameter",
                "bract_height",
                "lower_lip_angle_deg",
                "water_depth",
                "flower_orientation_deg",
            )
        }
        exsertion_means = {
            rank: group_mean(rank_rows[rank], "realized_exsertion")
            for rank in all_ranks
        }
        adjacent = [
            exsertion_means[right] - exsertion_means[left]
            for left, right in zip(all_ranks, all_ranks[1:])
        ]

        def max_relative(field: str) -> float:
            ref = sham_means[field]
            return max(
                relative_change(group_mean(rank_rows[rank], field), ref)
                for rank in all_ranks
            )

        def max_absolute(field: str) -> float:
            ref = sham_means[field]
            return max(
                abs(group_mean(rank_rows[rank], field) - ref)
                for rank in all_ranks
            )

        out.append(
            {
                "plant_id": plant_id,
                "minimum_adjacent_exsertion_gap": min(adjacent),
                "opening_width_relative_change": max_relative(
                    "corolla_opening_width"
                ),
                "tube_diameter_relative_change": max_relative(
                    "tube_diameter"
                ),
                "bract_height_relative_change": max_relative(
                    "bract_height"
                ),
                "lower_lip_angle_abs_change": max_absolute(
                    "lower_lip_angle_deg"
                ),
                "water_depth_abs_change": max_absolute("water_depth"),
                "flower_orientation_abs_change": max_absolute(
                    "flower_orientation_deg"
                ),
                "maximum_mechanical_damage_rate": max(
                    group_binary_mean(rank_rows[rank], "mechanical_damage")
                    for rank in all_ranks
                ),
            }
        )
    return out


def _summarize_p0(path: Path) -> tuple[dict, tuple[str, str]]:
    rows = p0._read_csv(path)
    context = _context_from_rows(rows)
    rank_metrics = p0._rank_metrics(rows)
    off_target = p0._offtarget_metrics(rows)
    groups = p0._group_by_rank(rows)
    plant_gate_metrics = _p0_plant_gate_metrics(rows)
    if len(plant_gate_metrics) < 2:
        raise ValueError(
            "CAL-A P0 summary requires at least two plants with complete z-rank profiles"
        )
    plant_gate_fields = [
        "minimum_adjacent_exsertion_gap",
        "opening_width_relative_change",
        "tube_diameter_relative_change",
        "bract_height_relative_change",
        "lower_lip_angle_abs_change",
        "water_depth_abs_change",
        "flower_orientation_abs_change",
        "maximum_mechanical_damage_rate",
    ]
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
        "n_complete_profile_plants": len(plant_gate_metrics),
        "plant_level_gate_metric_distributions": {
            field: _summary(
                [float(row[field]) for row in plant_gate_metrics]
            )
            for field in plant_gate_fields
        },
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


def _p1_paired_metrics(
    rows: list[dict[str, str]],
) -> list[dict[str, float | str]]:
    plants = p1._paired_plants(rows)
    out = []

    for plant in plants:
        natural = [
            row
            for row in rows
            if row["plant_id"] == plant
            and row["pollination_treatment"] == "NATURAL"
        ]
        supplemented = [
            row
            for row in rows
            if row["plant_id"] == plant
            and row["pollination_treatment"] == "SUPPLEMENTED"
        ]

        def m(group, fn):
            return mean(fn(row) for row in group)

        nat_initial = m(natural, p1._initial_seed_set)
        sup_initial = m(supplemented, p1._initial_seed_set)
        nat_pollen = m(
            natural,
            lambda row: p1._num(
                row,
                "pollen_grains_post_treatment",
            ),
        )
        sup_pollen = m(
            supplemented,
            lambda row: p1._num(
                row,
                "pollen_grains_post_treatment",
            ),
        )
        nat_attack = m(
            natural,
            lambda row: float(
                p1._binary(
                    row,
                    "early_predator_attack_present",
                )
            ),
        )
        sup_attack = m(
            supplemented,
            lambda row: float(
                p1._binary(
                    row,
                    "early_predator_attack_present",
                )
            ),
        )
        nat_damage = m(
            natural,
            lambda row: float(
                p1._binary(row, "mechanical_damage")
            ),
        )
        sup_damage = m(
            supplemented,
            lambda row: float(
                p1._binary(row, "mechanical_damage")
            ),
        )

        def rel(field: str) -> float:
            natural_value = m(
                natural,
                lambda row, f=field: p1._num(row, f),
            )
            supplemented_value = m(
                supplemented,
                lambda row, f=field: p1._num(row, f),
            )
            return relative_change(
                supplemented_value,
                natural_value,
            )

        out.append(
            {
                "plant_id": plant,
                "initial_seed_set_delta": (
                    sup_initial - nat_initial
                ),
                "pollen_grains_delta": (
                    sup_pollen - nat_pollen
                ),
                "early_predator_attack_abs_difference": abs(
                    sup_attack - nat_attack
                ),
                "z_relative_change": rel(
                    "realized_exsertion"
                ),
                "bract_height_relative_change": rel(
                    "bract_height"
                ),
                "opening_width_relative_change": rel(
                    "corolla_opening_width"
                ),
                "water_depth_abs_difference": abs(
                    m(
                        supplemented,
                        lambda row: p1._num(
                            row,
                            "water_depth",
                        ),
                    )
                    - m(
                        natural,
                        lambda row: p1._num(
                            row,
                            "water_depth",
                        ),
                    )
                ),
                "maximum_mechanical_damage_rate": max(
                    sup_damage,
                    nat_damage,
                ),
                "mechanical_damage_abs_difference": abs(
                    sup_damage - nat_damage
                ),
            }
        )

    return out


def _p1_summary_with_planning_sd(
    values: list[float],
    *,
    planning_sd: float | None = None,
    planning_sd_definition: str,
    observed_n: int | None = None,
) -> dict:
    result = _summary(values)
    if observed_n is not None:
        result["descriptive_pair_combinations"] = result["n"]
        result["n"] = observed_n

    if planning_sd is None:
        planning_sd = result["sd"]

    result["planning_sd"] = planning_sd
    result["planning_sd_definition"] = (
        planning_sd_definition
    )
    return result


def _p1_arm_plant_values(
    rows: list[dict[str, str]],
    treatment: str,
    metric,
) -> list[float]:
    plants = p1._whole_plants_by_treatment(rows)[
        treatment
    ]
    return [
        p1._plant_mean(
            rows,
            plant,
            treatment,
            metric,
        )
        for plant in plants
    ]


def _sd(values: list[float]) -> float:
    if len(values) < 2:
        raise ValueError(
            "at least two plant units are required for SD"
        )
    return stdev(values)


def _independent_additive_planning_sd(
    natural: list[float],
    supplemented: list[float],
) -> float:
    return math.sqrt(
        _sd(natural) ** 2
        + _sd(supplemented) ** 2
    )


def _independent_relative_planning_sd(
    natural: list[float],
    supplemented: list[float],
) -> float:
    mu_natural = mean(natural)
    mu_supplemented = mean(supplemented)
    if mu_natural == 0:
        raise ValueError(
            "whole-plant relative-change planning requires "
            "nonzero natural-arm mean"
        )

    sd_natural = _sd(natural)
    sd_supplemented = _sd(supplemented)

    return math.sqrt(
        (sd_supplemented / mu_natural) ** 2
        + (
            mu_supplemented
            * sd_natural
            / (mu_natural ** 2)
        )
        ** 2
    )


def _cross_contrasts(
    natural: list[float],
    supplemented: list[float],
    *,
    mode: str,
) -> list[float]:
    values = []
    for natural_value in natural:
        for supplemented_value in supplemented:
            if mode == "signed":
                values.append(
                    supplemented_value - natural_value
                )
            elif mode == "absolute":
                values.append(
                    abs(
                        supplemented_value
                        - natural_value
                    )
                )
            elif mode == "relative":
                values.append(
                    relative_change(
                        supplemented_value,
                        natural_value,
                    )
                )
            elif mode == "maximum":
                values.append(
                    max(
                        supplemented_value,
                        natural_value,
                    )
                )
            else:
                raise ValueError(
                    f"unregistered contrast mode: {mode}"
                )
    return values


def _whole_metric_summary(
    rows: list[dict[str, str]],
    metric,
    *,
    mode: str,
    relative: bool = False,
) -> dict:
    natural = _p1_arm_plant_values(
        rows,
        "NATURAL",
        metric,
    )
    supplemented = _p1_arm_plant_values(
        rows,
        "SUPPLEMENTED",
        metric,
    )

    contrasts = _cross_contrasts(
        natural,
        supplemented,
        mode=mode,
    )

    if relative:
        planning_sd = (
            _independent_relative_planning_sd(
                natural,
                supplemented,
            )
        )
        planning_definition = (
            "DELTA_METHOD_INDEPENDENT_ARM_RELATIVE_CHANGE_"
            "SQRT_N_SCALING_COEFFICIENT"
        )
    else:
        planning_sd = (
            _independent_additive_planning_sd(
                natural,
                supplemented,
            )
        )
        planning_definition = (
            "INDEPENDENT_ARM_CONTRAST_"
            "SQRT_SD_NATURAL2_PLUS_SD_SUPPLEMENTED2"
        )

    return _p1_summary_with_planning_sd(
        contrasts,
        planning_sd=planning_sd,
        planning_sd_definition=planning_definition,
        observed_n=min(
            len(natural),
            len(supplemented),
        ),
    )


def _summarize_p1(
    path: Path,
) -> tuple[dict, tuple[str, str]]:
    rows = p1._read_csv(path)
    context = _context_from_rows(rows)
    design_unit = p1._infer_design_unit(rows)

    fields = [
        "initial_seed_set_delta",
        "pollen_grains_delta",
        "early_predator_attack_abs_difference",
        "z_relative_change",
        "bract_height_relative_change",
        "opening_width_relative_change",
        "water_depth_abs_difference",
        "maximum_mechanical_damage_rate",
        "mechanical_damage_abs_difference",
    ]

    if design_unit == p1.PAIRED:
        plant_metrics = _p1_paired_metrics(rows)
        if len(plant_metrics) < 2:
            raise ValueError(
                "CAL-B P1 paired summary requires at least "
                "two paired plants"
            )
        distributions = {}
        for field in fields:
            distributions[field] = (
                _p1_summary_with_planning_sd(
                    [
                        float(row[field])
                        for row in plant_metrics
                    ],
                    planning_sd_definition=(
                        "SD_OF_PAIRED_PLANT_LEVEL_CONTRASTS"
                    ),
                )
            )

        plant_units = len(plant_metrics)
        plants_by_treatment = {
            "NATURAL": plant_units,
            "SUPPLEMENTED": plant_units,
        }
        estimand_family = (
            "PAIRED_PLANT_LEVEL_TREATMENT_CONTRAST"
        )
        n_paired_plants = plant_units

    else:
        initial_metric = p1._initial_seed_set
        pollen_metric = lambda row: p1._num(
            row,
            "pollen_grains_post_treatment",
        )
        attack_metric = lambda row: float(
            p1._binary(
                row,
                "early_predator_attack_present",
            )
        )
        damage_metric = lambda row: float(
            p1._binary(
                row,
                "mechanical_damage",
            )
        )

        distributions = {
            "initial_seed_set_delta": (
                _whole_metric_summary(
                    rows,
                    initial_metric,
                    mode="signed",
                )
            ),
            "pollen_grains_delta": (
                _whole_metric_summary(
                    rows,
                    pollen_metric,
                    mode="signed",
                )
            ),
            "early_predator_attack_abs_difference": (
                _whole_metric_summary(
                    rows,
                    attack_metric,
                    mode="absolute",
                )
            ),
            "z_relative_change": (
                _whole_metric_summary(
                    rows,
                    lambda row: p1._num(
                        row,
                        "realized_exsertion",
                    ),
                    mode="relative",
                    relative=True,
                )
            ),
            "bract_height_relative_change": (
                _whole_metric_summary(
                    rows,
                    lambda row: p1._num(
                        row,
                        "bract_height",
                    ),
                    mode="relative",
                    relative=True,
                )
            ),
            "opening_width_relative_change": (
                _whole_metric_summary(
                    rows,
                    lambda row: p1._num(
                        row,
                        "corolla_opening_width",
                    ),
                    mode="relative",
                    relative=True,
                )
            ),
            "water_depth_abs_difference": (
                _whole_metric_summary(
                    rows,
                    lambda row: p1._num(
                        row,
                        "water_depth",
                    ),
                    mode="absolute",
                )
            ),
            "maximum_mechanical_damage_rate": (
                _whole_metric_summary(
                    rows,
                    damage_metric,
                    mode="maximum",
                )
            ),
            "mechanical_damage_abs_difference": (
                _whole_metric_summary(
                    rows,
                    damage_metric,
                    mode="absolute",
                )
            ),
        }

        plant_lists = p1._whole_plants_by_treatment(
            rows
        )
        plants_by_treatment = {
            treatment: len(plant_lists[treatment])
            for treatment in p1.TREATMENTS
        }
        plant_units = min(
            plants_by_treatment.values()
        )
        estimand_family = (
            "INDEPENDENT_ARM_PLANT_LEVEL_TREATMENT_CONTRAST"
        )
        n_paired_plants = None

    return {
        "n_rows": len(rows),
        "design_unit": design_unit,
        "estimand_family": estimand_family,
        "plant_units_by_treatment": (
            plants_by_treatment
        ),
        "n_plant_units_per_treatment_min": plant_units,
        "n_paired_plants": n_paired_plants,
        "plant_level_distributions": distributions,
        "interpretation": (
            "CAL-A/CAL-B exploratory evidence only. "
            "The P1 design unit is inferred from the "
            "calibration rows and retained because paired "
            "and whole-plant contrasts use different "
            "planning-variance definitions. Effect and "
            "contamination distributions are summarized "
            "without defining minimum effects or "
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

from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256
from scripts import analyze_pedicularis_randomized_pollen_sentinels as sentinel
from scripts import validate_pedicularis_cohort_registry as cohort
from scripts.analyze_pedicularis_full_surface import _validate_readiness
from scripts.audit_pedicularis_xia2013_patch_units import seed_output_decomposition
from scripts.build_pedicularis_two_cohort_fruit_allocation import (
    FROZEN_FIELDS as FRUIT_FROZEN_FIELDS,
    RECEIPT_SCHEMA as FRUIT_SCHEMA,
    RECEIPT_STATUS as FRUIT_STATUS,
)

SCHEMA = "PEDICULARIS_TWO_COHORT_ECOLOGICAL_BRIDGE_CONFIG_V1"
STATUS = "FROZEN_BEFORE_BOTH_COHORT_OUTCOMES"
CLAIM_LANE = "TWO_COHORT_NON_GATING_ECOLOGICAL_GEOMETRY_NOT_W1_W2"


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("two-cohort input CSV has no header")
        rows = [
            {str(key): (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("two-cohort input CSV is empty")
    return rows


def _load(path: Path) -> dict:
    obj = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(obj, dict):
        raise ValueError("two-cohort receipt must be a JSON object")
    return obj


def _number(value: object, label: str) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a resolved number") from exc
    if not math.isfinite(x):
        raise ValueError(f"{label} must be finite")
    return x


def _positive_int(value: object, label: str, minimum: int) -> int:
    x = _number(value, label)
    if not x.is_integer() or x < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return int(x)


def _configuration(raw: dict) -> dict:
    if raw.get("schema") != SCHEMA or raw.get("status") != STATUS:
        raise ValueError("two-cohort config is not the frozen registered schema")
    if raw.get("frozen_before_both_cohort_outcomes") is not True:
        raise ValueError("two-cohort analysis must be frozen before both outcomes")
    if raw.get("claim_lane") != CLAIM_LANE:
        raise ValueError("two-cohort bridge cannot promote W1/W2")
    population = raw.get("population_id")
    season = raw.get("season_id")
    if not population or not season or "REQUIRED_BEFORE_USE" in (population, season):
        raise ValueError("two-cohort population and season must be resolved")
    n = _positive_int(raw.get("min_fruit_plants"), "min_fruit_plants", 3)
    reps = _positive_int(raw.get("plant_bootstrap_reps"), "plant_bootstrap_reps", 200)
    seed = _positive_int(raw.get("random_seed"), "random_seed", 0)
    max_water = _number(raw.get("max_water_depth_range"), "max_water_depth_range")
    max_damage = _number(
        raw.get("max_mechanical_damage_fraction"), "max_mechanical_damage_fraction"
    )
    if max_water < 0 or not 0 <= max_damage <= 1:
        raise ValueError("two-cohort handling and water tolerances out of range")
    return {
        "population_id": population,
        "season_id": season,
        "min_fruit_plants": n,
        "bootstrap_reps": reps,
        "random_seed": seed,
        "max_water_depth_range": max_water,
        "max_damage_fraction": max_damage,
    }


def _validated_fruit_blocks(
    rows: list[dict[str, str]],
    allocation: dict,
    p0: dict,
    readiness: dict,
    registry_rows: list[dict[str, str]],
    config: dict,
) -> tuple[dict[str, list[dict[str, str]]], dict]:
    if (allocation.get("receipt_schema"), allocation.get("status")) != (
        FRUIT_SCHEMA, FRUIT_STATUS
    ):
        raise ValueError("fruit-only assignment is not a frozen z x G allocation")
    population, season = config["population_id"], config["season_id"]
    if (allocation.get("population_id"), allocation.get("season_id")) != (
        population, season
    ):
        raise ValueError("fruit allocation population/season differs from bridge")
    _validate_readiness(readiness, population, season)
    if allocation.get("readiness_sha256") != _semantic_sha256(readiness):
        raise ValueError("fruit allocation does not match exact qualified readiness")
    if allocation.get("p0_qualification_sha256") != _semantic_sha256(p0):
        raise ValueError("fruit allocation does not match positive P0 qualification")
    if allocation.get("allocation_algorithm") != "SHA256_RANK_V1":
        raise ValueError("fruit assignment does not use registered randomizer")
    if allocation.get("cohort_role") != "TWO_COHORT_FRUIT":
        raise ValueError("fruit-only cohort role mismatch")
    if allocation.get("pollination_treatment") != "NATURAL":
        raise ValueError("fruit-only cohort must preserve natural pollination")
    required = set(FRUIT_FROZEN_FIELDS) | {
        "ovule_count", "undamaged_seed_count", "damaged_seed_count",
        "water_depth", "mechanical_damage", "early_predator_attack_present",
        "realized_exsertion_before_G",
    }
    if not rows or any(not required.issubset(set(row)) for row in rows):
        raise ValueError("fruit-only rows are missing required reproductive columns")
    frozen = sorted(
        [{field: row[field] for field in FRUIT_FROZEN_FIELDS} for row in rows],
        key=lambda r: (r["plant_id"], r["flower_id"]),
    )
    if frozen != allocation.get("expected_frozen_rows"):
        raise ValueError("fruit-only z/G/randomized flower assignments changed")
    if _semantic_sha256(frozen) != allocation.get("allocation_identity_sha256"):
        raise ValueError("fruit-only allocation fingerprint differs")
    if len(rows) != allocation.get("n_allocated_flowers"):
        raise ValueError("fruit-only expected outcome count changed")

    registry_by_flower = {row["flower_id"]: row for row in registry_rows}
    by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    observed_flower_ids: set[str] = set()
    waters: list[float] = []
    mechanical: list[int] = []
    observed_z: dict[tuple[str, int], list[float]] = defaultdict(list)
    ranks = list(range(int(allocation["n_z_levels"])))
    expected = {(rank, g) for rank in ranks for g in ("EXCLUDED", "EXPOSED")}
    valid_settings = {
        (v["assigned_z_level"], int(v["assigned_z_rank"])): v["manipulation_setting_id"]
        for v in allocation["z_manipulation_settings"]
    }
    if len(valid_settings) != len(ranks):
        raise ValueError("fruit-only physical z grid is incomplete")
    for row in rows:
        flower_id = row["flower_id"]
        if flower_id in observed_flower_ids:
            raise ValueError("fruit-only flower IDs must be unique")
        observed_flower_ids.add(flower_id)
        if (row["population_id"], row["season_id"]) != (population, season):
            raise ValueError("fruit-only row context mismatch")
        registry_entry = registry_by_flower.get(flower_id)
        if (
            registry_entry is None
            or registry_entry["cohort_role"] != "TWO_COHORT_FRUIT"
            or registry_entry["plant_id"] != row["plant_id"]
        ):
            raise ValueError("fruit-only flower lacks the nonconfirmatory registry role")
        if row["pollination_treatment"] != "NATURAL":
            raise ValueError("fruit-only outcomes must come from NATURAL P treatment")
        rank = int(row["assigned_z_rank"])
        if rank not in ranks or valid_settings.get(
            (row["assigned_z_level"], rank)
        ) != row["manipulation_setting_id"]:
            raise ValueError("fruit-only physical z setting differs from P0")
        g = row["predator_treatment"]
        expected_method = readiness["validated_execution"][
            "g_exclusion_method" if g == "EXCLUDED" else "g_exposed_sham_method"
        ] if g in ("EXCLUDED", "EXPOSED") else None
        if row["exclusion_method"] != expected_method:
            raise ValueError("fruit-only predator treatment or method mismatch")
        if row.get("pollen_grains", "").strip():
            raise ValueError("fruit-only rows must never borrow sentinel pollen grains")
        n_ovules = _number(row["ovule_count"], "ovule_count")
        good = _number(row["undamaged_seed_count"], "undamaged_seed_count")
        bad = _number(row["damaged_seed_count"], "damaged_seed_count")
        if (
            n_ovules < 1 or not n_ovules.is_integer()
            or min(good, bad) < 0
            or not good.is_integer() or not bad.is_integer()
            or good + bad > n_ovules
        ):
            raise ValueError("fruit-only counts must be consistent integer seed/ovule counts")
        for bit in ("mechanical_damage", "early_predator_attack_present"):
            if row[bit] not in ("0", "1"):
                raise ValueError(f"{bit} must be 0/1")
        waters.append(_number(row["water_depth"], "water_depth"))
        observed_z[(g, rank)].append(
            _number(row["realized_exsertion_before_G"], "realized_exsertion_before_G")
        )
        mechanical.append(int(row["mechanical_damage"]))
        by_plant[row["plant_id"]].append(row)
    if len(by_plant) < config["min_fruit_plants"]:
        raise ValueError("too few independent fruit-only plants")
    if any(
        {(int(row["assigned_z_rank"]), row["predator_treatment"]) for row in block}
        != expected or len(block) != len(expected)
        for block in by_plant.values()
    ):
        raise ValueError("each fruit plant must cover every z x G combination exactly once")
    if max(waters) - min(waters) > config["max_water_depth_range"]:
        raise ValueError("fruit-only water-y changed beyond registered tolerance")
    if mean(mechanical) > config["max_damage_fraction"]:
        raise ValueError("fruit-only handling damage exceeded registered tolerance")
    z_means = {
        treatment: {
            rank: mean(observed_z[(treatment, rank)]) for rank in ranks
        }
        for treatment in ("EXCLUDED", "EXPOSED")
    }
    first_stage_ordered = all(
        all(values[after] > values[before] for before, after in zip(ranks, ranks[1:]))
        for values in z_means.values()
    )
    return dict(by_plant), {
        "realized_exsertion_before_G_by_state_and_rank": {
            g: {str(rank): val for rank, val in values.items()}
            for g, values in z_means.items()
        },
        "fruit_z_first_stage_ordered_in_both_G_states": first_stage_ordered,
        "n_fruit_plants": len(by_plant),
        "n_fruit_flowers": len(rows),
        "n_physical_z_levels": len(ranks),
        "water_depth_range": max(waters) - min(waters),
        "mechanical_damage_fraction": mean(mechanical),
    }


def _profile(
    blocks: list[list[dict[str, str]]],
    levels: list[int],
    kind: str,
) -> dict:
    if kind == "pollen":
        return {
            rank: mean(
                float(row["pollen_grains"])
                for block in blocks for row in block
                if int(row["assigned_z_rank"]) == rank
            )
            for rank in levels
        }
    return {
        treatment: {
            rank: mean(
                float(row["undamaged_seed_count"])
                for block in blocks for row in block
                if int(row["assigned_z_rank"]) == rank
                and row["predator_treatment"] == treatment
            )
            for rank in levels
        }
        for treatment in ("EXCLUDED", "EXPOSED")
    }


def _seed_fitness_translation(
    fruit_rows: list[dict[str, str]], ranks: list[int]
) -> dict:
    """Descriptive within-FRUIT decomposition; no pollen/seed row imputation.

    The source columns distinguish damaged and intact seed coats but do not
    resolve 0/0 seed fate, so any cell containing 0/0 fails the stage
    decomposition rather than dropping those flowers or setting q=1.
    """
    cells: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(list)
    for row in fruit_rows:
        cells[row["predator_treatment"], int(row["assigned_z_rank"])].append(row)
    result: dict[str, dict[str, dict]] = {}
    for treatment in ("EXCLUDED", "EXPOSED"):
        result[treatment] = {}
        for rank in ranks:
            subset = cells[treatment, rank]
            if not subset:
                raise ValueError("missing fruit z by predator cell for decomposition")
            u = [float(r["undamaged_seed_count"]) for r in subset]
            d = [float(r["damaged_seed_count"]) for r in subset]
            n = [float(r["ovule_count"]) for r in subset]
            final = mean(ui / ni for ui, ni in zip(u, n, strict=True))
            zero_fate = [
                r["flower_id"] for r, ui, di in zip(subset, u, d, strict=True)
                if ui + di == 0
            ]
            if zero_fate:
                result[treatment][str(rank)] = {
                    "status": "NOT_MODELABLE_ZERO_DISTINGUISHABLE_SEED_FATE",
                    "n_flowers": len(subset),
                    "zero_distinguishable_seed_flower_ids": sorted(zero_fate),
                    "mean_final_viable_seed_fraction_all_flowers": final,
                    "mean_initial_seed_fraction": None,
                    "mean_predation_fraction": None,
                    "initial_predation_covariance": None,
                    "complete_stage_identity_checked": False,
                }
                continue
            initial = [(ui + di) / ni for ui, di, ni in zip(u, d, n, strict=True)]
            predation = [di / (ui + di) for ui, di in zip(u, d, strict=True)]
            detail = seed_output_decomposition(initial, predation)
            if not math.isclose(
                detail["mean_final_seed_fraction"], final, rel_tol=1e-10, abs_tol=1e-12
            ):
                raise ValueError("within-fruit seed initiation–predation identity failed")
            result[treatment][str(rank)] = {
                "status": "DISTINGUISHABLE_SEED_DECOMPOSITION",
                "n_flowers": len(subset),
                "zero_distinguishable_seed_flower_ids": [],
                "mean_final_viable_seed_fraction_all_flowers": final,
                "mean_initial_seed_fraction": detail["mean_initial_seed_fraction"],
                "mean_predation_fraction": detail["mean_seed_predation_fraction"],
                "initial_predation_covariance": detail["initial_predation_covariance"],
                "complete_stage_identity_checked": True,
            }

    endpoints: dict[str, dict] = {}
    for treatment, profile in result.items():
        low, high = profile[str(ranks[0])], profile[str(ranks[-1])]
        if any(
            entry["status"] != "DISTINGUISHABLE_SEED_DECOMPOSITION"
            for entry in (low, high)
        ):
            endpoints[treatment] = {
                "status": "NOT_MODELABLE_ZERO_SEED_FATE_AT_ENDPOINT",
                "rank_low": ranks[0],
                "rank_high": ranks[-1],
            }
            continue
        delta_initial = (
            high["mean_initial_seed_fraction"] - low["mean_initial_seed_fraction"]
        )
        delta_predation = (
            high["mean_predation_fraction"] - low["mean_predation_fraction"]
        )
        middle_initial = (
            high["mean_initial_seed_fraction"] + low["mean_initial_seed_fraction"]
        ) / 2
        middle_predation = (
            high["mean_predation_fraction"] + low["mean_predation_fraction"]
        ) / 2
        delta_cov = (
            high["initial_predation_covariance"] - low["initial_predation_covariance"]
        )
        initiation = (1 - middle_predation) * delta_initial
        predation = -middle_initial * delta_predation
        covariance = -delta_cov
        observed_change = (
            high["mean_final_viable_seed_fraction_all_flowers"]
            - low["mean_final_viable_seed_fraction_all_flowers"]
        )
        if not math.isclose(
            initiation + predation + covariance, observed_change,
            rel_tol=1e-10, abs_tol=1e-12,
        ):
            raise ValueError("fruit endpoint decomposition does not sum to fitness change")
        endpoints[treatment] = {
            "status": "MATCHED_FRUIT_IDENTITY_VALIDATED_DESCRIPTIVE",
            "rank_low": ranks[0],
            "rank_high": ranks[-1],
            "viable_seed_change": observed_change,
            "seed_initiation_contribution": initiation,
            "seed_predation_contribution": predation,
            "within_fruit_covariance_contribution": covariance,
        }
    unresolved = sum(
        v["status"] != "DISTINGUISHABLE_SEED_DECOMPOSITION"
        for cells_for_g in result.values() for v in cells_for_g.values()
    )
    return {
        "by_predator_state_and_rank": result,
        "fixed_extreme_rank_decomposition": endpoints,
        "n_unresolved_z_by_G_cells": unresolved,
        "status": (
            "ALL_MATCHED_DISTINGUISHABLE_SEED_CELLS_DECOMPOSABLE"
            if unresolved == 0 else "PARTIAL_DECOMPOSITION_ZERO_SEED_FATE_UNRESOLVED"
        ),
        "claim_ceiling": [
            "matched_distinguishable_seed_counts_only_not_causal_mediation",
            "fully_consumed_seeds_without_coats_may_be_misclassified",
            "0_over_0_seed_fate_cannot_be_assigned_100_percent_predation",
            "true_initial_seed_set_requires_qualified_seed_fate_and_stage_protocol",
            "no_causal_exsertion_by_G_selection_gradient_identified_from_this_identity",
        ],
    }


def _unique_peak(profile: dict[int, float]) -> int | None:
    top = max(profile.values())
    best = [rank for rank, value in profile.items() if value == top]
    return best[0] if len(best) == 1 else None


def _comparison(
    pollen: dict[int, float],
    seed: dict[str, dict[int, float]],
) -> dict:
    free = _unique_peak(seed["EXCLUDED"])
    exposed = _unique_peak(seed["EXPOSED"])
    if free is None or exposed is None:
        return {
            "predator_excluded_optimum_rank": free,
            "predator_exposed_optimum_rank": exposed,
            "rank_shift_predator_removal": None,
            "pollen_gain_at_shifted_ranks": None,
            "positive_alignment": False,
            "status": "DISCRETE_PEAK_TIE_UNRESOLVED",
        }
    shift = free - exposed
    gain = pollen[free] - pollen[exposed]
    return {
        "predator_excluded_optimum_rank": free,
        "predator_exposed_optimum_rank": exposed,
        "rank_shift_predator_removal": shift,
        "pollen_gain_at_shifted_ranks": gain,
        "positive_alignment": shift > 0 and gain > 0,
        "status": "DESCRIPTIVE_DISCRETE_OPTIMUM_CONTRAST",
    }


def _quantile(values: list[float], q: float) -> float:
    xs = sorted(values)
    pos = (len(xs) - 1) * q
    low = math.floor(pos)
    high = math.ceil(pos)
    return xs[low] if low == high else (
        xs[low] * (high - pos) + xs[high] * (pos - low)
    )


def build(
    pollen_rows: list[dict[str, str]],
    pollen_allocation: dict,
    p0_receipt: dict,
    registry_rows: list[dict[str, str]],
    pollen_config: dict,
    fruit_rows: list[dict[str, str]],
    fruit_allocation: dict,
    readiness: dict,
    bridge_config: dict,
) -> dict:
    cfg = _configuration(bridge_config)
    # This recomputes the independently allocated sentinel result rather than
    # trusting a copied pollen receipt or assuming same-flower covariance.
    pollen_receipt = sentinel.build(
        pollen_rows, pollen_allocation, p0_receipt, registry_rows, pollen_config
    )
    if (pollen_receipt["population_id"], pollen_receipt["season_id"]) != (
        cfg["population_id"], cfg["season_id"]
    ):
        raise ValueError("pollen and fruit cohorts are from different contexts")
    cohort.validate(registry_rows)
    fruit_blocks, fruit_checks = _validated_fruit_blocks(
        fruit_rows, fruit_allocation, p0_receipt, readiness, registry_rows, cfg
    )
    fruit_ids = {row["flower_id"] for row in fruit_rows}
    pollen_ids = {row["flower_id"] for row in pollen_rows}
    if fruit_ids & pollen_ids:
        raise ValueError("same flower cannot be both pollen and mature seed cohort")
    if (
        pollen_allocation.get("z_manipulation_settings")
        != fruit_allocation.get("z_manipulation_settings")
    ):
        raise ValueError("pollen and fruit treatment physical z grids differ")

    pollen_blocks: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in pollen_rows:
        pollen_blocks[row["plant_id"]].append(row)
    pollen_keys, fruit_keys = set(pollen_blocks), set(fruit_blocks)
    if pollen_keys == fruit_keys:
        relationship = "SAME_PLANTS_DISJOINT_FLOWERS_PAIRED_BOOTSTRAP"
    elif pollen_keys.isdisjoint(fruit_keys):
        relationship = "DISJOINT_PLANTS_INDEPENDENT_BOOTSTRAP"
    else:
        raise ValueError(
            "partially overlapping plant sets require a separately registered "
            "joint cluster-resampling design"
        )
    ranks = list(range(int(fruit_allocation["n_z_levels"])))
    pollen_profile = _profile(list(pollen_blocks.values()), ranks, "pollen")
    seed_profile = _profile(list(fruit_blocks.values()), ranks, "seed")
    observed = _comparison(pollen_profile, seed_profile)
    fitness_translation = _seed_fitness_translation(fruit_rows, ranks)

    rng = random.Random(cfg["random_seed"])
    pids, fids = sorted(pollen_keys), sorted(fruit_keys)
    shift_draws: list[float] = []
    gain_draws: list[float] = []
    tie_draws = 0
    aligned_draws = 0
    for _ in range(cfg["bootstrap_reps"]):
        if relationship.startswith("SAME_PLANTS"):
            common = rng.choices(pids, k=len(pids))
            pollen_sample = [pollen_blocks[p] for p in common]
            seed_sample = [fruit_blocks[p] for p in common]
        else:
            pollen_sample = [
                pollen_blocks[p] for p in rng.choices(pids, k=len(pids))
            ]
            seed_sample = [
                fruit_blocks[p] for p in rng.choices(fids, k=len(fids))
            ]
        profile_p = _profile(pollen_sample, ranks, "pollen")
        profile_f = _profile(seed_sample, ranks, "seed")
        comparison = _comparison(profile_p, profile_f)
        if comparison["status"] == "DISCRETE_PEAK_TIE_UNRESOLVED":
            tie_draws += 1
            # Ambiguous bootstrap peaks are not silently discarded to
            # overstate the fraction of stable positive alignment.
            shift_draws.append(0.0)
            gain_draws.append(0.0)
        else:
            shift_draws.append(comparison["rank_shift_predator_removal"])
            gain_draws.append(comparison["pollen_gain_at_shifted_ranks"])
        aligned_draws += int(comparison["positive_alignment"])
    return {
        "analysis": "pedicularis_split_cohort_discrete_optimum_pollen_alignment_v1",
        "receipt_schema": "PEDICULARIS_TWO_COHORT_NON_GATING_ECOLOGICAL_CONTRAST_V1",
        "status": (
            "TWO_COHORT_DESCRIPTIVE_CONTRAST_NO_W1_W2_PROMOTION"
            if fruit_checks["fruit_z_first_stage_ordered_in_both_G_states"]
            else "TWO_COHORT_Z_FIRST_STAGE_NOT_ORDERED_NO_EXSERTION_INTERPRETATION"
        ),
        "population_id": cfg["population_id"],
        "season_id": cfg["season_id"],
        "estimand": (
            "mean_stigmatic_pollen_by_randomized_z_rank_on_sentinels_vs_"
            "mean_intact_viable_seeds_by_z_rank_and_randomized_G_on_distinct_flowers"
        ),
        "pollen_sentinel_status": pollen_receipt["status"],
        "pollen_mean_by_rank": {str(r): pollen_profile[r] for r in ranks},
        "viable_seeds_per_flower_by_G_and_rank": {
            g: {str(r): values[r] for r in ranks}
            for g, values in seed_profile.items()
        },
        "observed_discrete_contrast": observed,
        "fruit_stage_fitness_translation_non_gating": fitness_translation,
        "plant_overlap_resampling": relationship,
        "plant_bootstrap": {
            "reps": cfg["bootstrap_reps"],
            "unresolved_tie_fraction": tie_draws / cfg["bootstrap_reps"],
            "positive_shift_and_positive_pollen_gain_fraction": (
                aligned_draws / cfg["bootstrap_reps"]
            ),
            "rank_shift_percentile_range_descriptive_not_regular_CI": [
                _quantile(shift_draws, 0.025),
                _quantile(shift_draws, 0.975),
            ],
            "pollen_gain_percentile_range_descriptive_not_regular_CI": [
                _quantile(gain_draws, 0.025),
                _quantile(gain_draws, 0.975),
            ],
        },
        "fruit_nuisance_checks": fruit_checks,
        "sentinel_allocation_sha256": _semantic_sha256(pollen_allocation),
        "sentinel_data_sha256": pollen_receipt["sentinel_data_sha256"],
        "fruit_allocation_sha256": _semantic_sha256(fruit_allocation),
        "fruit_data_sha256": _semantic_sha256(sorted(
            fruit_rows, key=lambda r: (r["plant_id"], r["flower_id"])
        )),
        "registry_sha256": _semantic_sha256(registry_rows),
        "bridge_config_sha256": _semantic_sha256(bridge_config),
        "claim_ceiling": [
            "experimental_descriptive_profiles_not_preregistered_confirmatory_W1_W2",
            "separate_cohorts_identify_population_means_under_exchangeability",
            "same_flower_pollen_seed_covariance_not_identified",
            "within_fruit_seed_coupling_does_not_identify_pollen_seed_mediation",
            "no_pure_pollinator_optimum_or_genetic_architecture_identified",
            "argmax_bootstrap_percentiles_are_nonregular_not_formal_95pct_inference",
            "predator_barrier_spillover_and_maternal_resource_competition_need_pilot",
            "natural_pollination_pollen_receipt_not_specific_pollinator_mediation",
            "cohort_exchangeability_and_G_selectivity_across_z_not_proved_by_receipts",
            "assigned_setting_rank_not_actual_mm_exsertion_without_first_stage",
            "does_not_unlock_original_same_flower_P2_or_SCH_primary_compromise",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Non-gating two-cohort exsertion / pollen / seed-geometry diagnostic"
    )
    for field in (
        "completed_sentinel_csv", "sentinel_allocation_json",
        "positive_p0_receipt_json", "cohort_registry_csv",
        "frozen_sentinel_config_json", "completed_fruit_csv",
        "fruit_allocation_json", "qualified_readiness_json",
        "frozen_two_cohort_config_json",
    ):
        parser.add_argument(field, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(
        _read_csv(args.completed_sentinel_csv),
        _load(args.sentinel_allocation_json),
        _load(args.positive_p0_receipt_json),
        cohort._read(args.cohort_registry_csv),
        _load(args.frozen_sentinel_config_json),
        _read_csv(args.completed_fruit_csv),
        _load(args.fruit_allocation_json),
        _load(args.qualified_readiness_json),
        _load(args.frozen_two_cohort_config_json),
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

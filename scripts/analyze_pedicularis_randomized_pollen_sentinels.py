from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts.build_pedicularis_p0_randomized_assignment import (
    FROZEN_FIELDS,
    _semantic_sha256,
)
from scripts import validate_pedicularis_cohort_registry as cohort
from scripts.build_pedicularis_randomized_pollen_sentinels import (
    SCHEMA as ASSIGNMENT_SCHEMA,
    STATUS as ASSIGNMENT_STATUS,
)


CONFIG_SCHEMA = "PEDICULARIS_RANDOMIZED_POLLEN_SENTINEL_CONFIG_V1"
CONFIG_STATUS = "PEDICULARIS_POLLEN_SENTINEL_INFERENCE_FROZEN_BEFORE_OUTCOMES"

REQUIRED = (
    *FROZEN_FIELDS,
    "realized_exsertion",
    "pollen_grains",
    "flower_age_at_sampling_hours",
    "pollen_sampling_stage",
    "pollen_assay_method_id",
    "stigma_removed",
    "mechanical_damage",
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("pollen sentinel CSV has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("pollen sentinel CSV is empty")
    return rows


def _load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("pollen sentinel JSON must be an object")
    return data


def _finite(value: object, label: str) -> float:
    if value in (None, "", "REQUIRED_BEFORE_USE"):
        raise ValueError(f"{label} must be prospectively resolved")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(result):
        raise ValueError(f"{label} must be finite")
    return result


def _integer(value: object, label: str, minimum: int) -> int:
    number = _finite(value, label)
    if not number.is_integer() or number < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return int(number)


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    pos = (len(ordered) - 1) * q
    low = math.floor(pos)
    high = math.ceil(pos)
    return (
        ordered[low] if low == high
        else ordered[low] * (high - pos) + ordered[high] * (pos - low)
    )


def _slope_within_plant(blocks: list[list[dict[str, str]]]) -> float:
    numerator = 0.0
    denominator = 0.0
    for block in blocks:
        ranks = [float(row["assigned_z_rank"]) for row in block]
        pollen = [float(row["pollen_grains"]) for row in block]
        rank_center = mean(ranks)
        pollen_center = mean(pollen)
        numerator += sum(
            (rank - rank_center) * (grain - pollen_center)
            for rank, grain in zip(ranks, pollen, strict=True)
        )
        denominator += sum(
            (rank - rank_center) ** 2 for rank in ranks
        )
    if denominator <= 0:
        raise ValueError("randomized sentinel analysis needs within-plant z variation")
    return numerator / denominator


def _mean_pollen_by_rank(
    blocks: list[list[dict[str, str]]], ranks: list[int]
) -> dict[int, float]:
    """Balanced-block dose-response; one randomized flower per rank and plant."""
    values: dict[int, list[float]] = {rank: [] for rank in ranks}
    for block in blocks:
        per_plant = {int(row["assigned_z_rank"]): float(row["pollen_grains"]) for row in block}
        if set(per_plant) != set(ranks):
            raise ValueError("dose-response requires every rank within each plant")
        for rank in ranks:
            values[rank].append(per_plant[rank])
    return {rank: mean(values[rank]) for rank in ranks}


def _central_vs_endpoints(profile: dict[int, float], ranks: list[int]) -> float:
    """Predefined descriptive shape contrast, never a confirmatory gate."""
    n = len(ranks)
    center = [ranks[n // 2]] if n % 2 else [ranks[n // 2 - 1], ranks[n // 2]]
    return mean(profile[rank] for rank in center) - (
        profile[ranks[0]] + profile[ranks[-1]]
    ) / 2


def _configuration(config: dict) -> dict:
    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError("pollen sentinel analysis config schema mismatch")
    if config.get("status") != CONFIG_STATUS:
        raise ValueError("pollen sentinel inference was not frozen before outcomes")
    if config.get("frozen_before_sentinel_outcomes") is not True:
        raise ValueError("pollen sentinel effect thresholds must be frozen before outcomes")
    if config.get("claim_lane") != "RANDOMIZED_POLLINATION_FUNCTION_ONLY_NOT_W1_W2":
        raise ValueError("pollen sentinel inference must not claim W1/W2")

    for field in (
        "population_id",
        "season_id",
        "pollen_assay_method_id",
        "prespecified_pollen_sampling_stage",
    ):
        if config.get(field) in (None, "", "REQUIRED_BEFORE_USE"):
            raise ValueError(f"{field} must be prospectively resolved")

    min_plants = _integer(config.get("min_independent_plants"), "min_independent_plants", 3)
    bootstrap = _integer(config.get("bootstrap_reps"), "bootstrap_reps", 200)
    permutations = _integer(
        config.get("randomization_permutation_reps"),
        "randomization_permutation_reps",
        199,
    )
    age = _finite(
        config.get("max_pollen_sampling_age_spread_hours"),
        "max_pollen_sampling_age_spread_hours",
    )
    damage = _finite(
        config.get("max_mechanical_damage_fraction"),
        "max_mechanical_damage_fraction",
    )
    min_slope = _finite(
        config.get("min_biologically_meaningful_pollen_grains_per_rank"),
        "min_biologically_meaningful_pollen_grains_per_rank",
    )
    valid = _finite(
        config.get("min_valid_plant_bootstrap_fraction"),
        "min_valid_plant_bootstrap_fraction",
    )
    alpha = _finite(
        config.get("one_sided_randomization_alpha"),
        "one_sided_randomization_alpha",
    )
    if age < 0 or min_slope < 0:
        raise ValueError("age tolerance and minimum positive effect must be >=0")
    if not 0 <= damage <= 1:
        raise ValueError("max_mechanical_damage_fraction must lie in [0,1]")
    if not 0 < valid <= 1 or not 0 < alpha < 1:
        raise ValueError("bootstrap fraction and randomization alpha must lie in (0,1)")
    return {
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "pollen_assay_method_id": config["pollen_assay_method_id"],
        "sampling_stage": config["prespecified_pollen_sampling_stage"],
        "min_plants": min_plants,
        "bootstrap_reps": bootstrap,
        "permutation_reps": permutations,
        "random_seed": _integer(config.get("random_seed"), "random_seed", 0),
        "max_age_spread": age,
        "max_damage_fraction": damage,
        "min_slope": min_slope,
        "min_valid_bootstrap_fraction": valid,
        "alpha": alpha,
    }


def _validate(
    rows: list[dict[str, str]],
    allocation: dict,
    p0_receipt: dict,
    registry_rows: list[dict[str, str]],
    config: dict,
) -> tuple[dict[str, list[dict[str, str]]], dict]:
    if allocation.get("receipt_schema") != ASSIGNMENT_SCHEMA:
        raise ValueError("sentinel allocation receipt schema mismatch")
    if allocation.get("status") != ASSIGNMENT_STATUS:
        raise ValueError("sentinel randomized allocation is not frozen")
    if p0_receipt.get("receipt_schema_version") != (
        "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1"
    ) or p0_receipt.get("status") != "PEDICULARIS_Z_MANIPULATION_VALIDATED":
        raise ValueError("sentinel inference requires qualified P0 manipulation")
    if allocation.get("p0_qualification_sha256") != _semantic_sha256(p0_receipt):
        raise ValueError("sentinel allocation is not bound to this positive P0 receipt")

    pop = config["population_id"]
    season = config["season_id"]
    for obj, name in ((allocation, "allocation"), (p0_receipt, "P0 qualification")):
        if obj.get("population_id") != pop or obj.get("season_id") != season:
            raise ValueError(f"pollen sentinel {name} population/season mismatch")
    if not rows or any(field not in rows[0] for field in REQUIRED):
        raise ValueError("sentinel rows lack required pollen-only fields")

    fields = [
        {field: row[field] for field in FROZEN_FIELDS}
        for row in rows
    ]
    fields.sort(key=lambda row: (row["plant_id"], row["flower_id"]))
    if fields != allocation.get("expected_frozen_rows"):
        raise ValueError("sentinel flowers or randomized z settings drifted from allocation")
    if _semantic_sha256(fields) != allocation.get("allocation_identity_sha256"):
        raise ValueError("sentinel assignment digest drifted from allocation")
    if len(fields) != int(allocation.get("n_allocated_flowers", -1)):
        raise ValueError("sentinel row count does not match allocation")

    registry_result = cohort.validate(registry_rows)
    registry_by_flower = {row["flower_id"]: row for row in registry_rows}
    blocks: dict[str, list[dict[str, str]]] = defaultdict(list)
    ages = []
    damage = []
    ranks = set()
    for row in rows:
        if (row["population_id"], row["season_id"]) != (pop, season):
            raise ValueError("sentinel rows must share one population and season")
        flower_id = row["flower_id"]
        registry_entry = registry_by_flower.get(flower_id)
        if registry_entry is None or registry_entry["cohort_role"] != "POLLEN_SENTINEL":
            raise ValueError("every sentinel flower must have a POLLEN_SENTINEL cohort role")
        if row["pollen_assay_method_id"] != config["pollen_assay_method_id"]:
            raise ValueError("sentinel pollen assay differs from prospectively frozen method")
        if row["pollen_sampling_stage"] != config["sampling_stage"]:
            raise ValueError(
                "sentinel pollen sampling stage differs from prospectively frozen stage"
            )
        for field in ("stigma_removed", "mechanical_damage", "sham_control"):
            if row[field] not in ("0", "1"):
                raise ValueError(f"{field} must be coded 0/1")
        for field in (
            "realized_exsertion", "pollen_grains", "flower_age_at_sampling_hours"
        ):
            value = _finite(row[field], field)
            if field in ("pollen_grains", "flower_age_at_sampling_hours") and value < 0:
                raise ValueError(f"{field} must be nonnegative")
        for forbidden in ("undamaged_seed_count", "damaged_seed_count"):
            if row.get(forbidden, "").strip():
                raise ValueError(
                    "destructive pollen sentinel rows must not be treated as mature-seed flowers"
                )
        ages.append(float(row["flower_age_at_sampling_hours"]))
        damage.append(int(row["mechanical_damage"]))
        rank = int(row["assigned_z_rank"])
        ranks.add(rank)
        blocks[row["plant_id"]].append(row)

    if len(blocks) < config["min_plants"]:
        raise ValueError("too few independent sentinel plants")
    expected_ranks = set(range(int(allocation["n_z_levels"])))
    if ranks != expected_ranks:
        raise ValueError("not all preregistered sentinel z levels were observed")
    if any(
        {int(row["assigned_z_rank"]) for row in block} != expected_ranks
        for block in blocks.values()
    ):
        raise ValueError("every sentinel plant must cover every randomized z level")
    if max(ages) - min(ages) > config["max_age_spread"]:
        raise ValueError("sentinel pollen sampling flower age varies beyond frozen tolerance")
    if mean(damage) > config["max_damage_fraction"]:
        raise ValueError("sentinel z manipulation handling damage exceeds frozen tolerance")

    z_means = {
        rank: mean(
            float(row["realized_exsertion"])
            for row in rows
            if int(row["assigned_z_rank"]) == rank
        )
        for rank in sorted(expected_ranks)
    }
    if any(
        z_means[next_rank] <= z_means[prior_rank]
        for prior_rank, next_rank in zip(
            sorted(expected_ranks),
            sorted(expected_ranks)[1:],
        )
    ):
        raise ValueError(
            "sentinel realized exsertion is not ordered by randomized z rank"
        )
    return dict(blocks), {
        "n_registered_sentinel_plants": len(blocks),
        "n_sentinel_flowers": len(rows),
        "n_randomized_z_levels": len(expected_ranks),
        "realized_z_means_by_rank": {str(k): v for k, v in z_means.items()},
        "max_observed_flower_age_spread_hours": max(ages) - min(ages),
        "mechanical_damage_fraction": mean(damage),
        "cohort_registry_sha256": _semantic_sha256(registry_rows),
        "cohort_registry_status": registry_result["status"],
    }


def build(
    rows: list[dict[str, str]],
    allocation: dict,
    p0_receipt: dict,
    registry_rows: list[dict[str, str]],
    config_payload: dict,
) -> dict:
    config = _configuration(config_payload)
    blocks, checks = _validate(
        rows, allocation, p0_receipt, registry_rows, config
    )
    block_list = [blocks[key] for key in sorted(blocks)]
    observed = _slope_within_plant(block_list)
    ranks = sorted(int(row["assigned_z_rank"]) for row in block_list[0])
    observed_profile = _mean_pollen_by_rank(block_list, ranks)

    rng = random.Random(config["random_seed"])
    plant_keys = sorted(blocks)
    boot_slopes = []
    boot_profiles = []
    for _ in range(config["bootstrap_reps"]):
        sample = [
            blocks[plant_id]
            for plant_id in rng.choices(plant_keys, k=len(plant_keys))
        ]
        try:
            boot_slopes.append(_slope_within_plant(sample))
            boot_profiles.append(_mean_pollen_by_rank(sample, ranks))
        except ValueError:
            pass
    valid_fraction = len(boot_slopes) / config["bootstrap_reps"]
    if (
        valid_fraction < config["min_valid_bootstrap_fraction"]
        or len(boot_slopes) < 50
    ):
        raise ValueError("too few valid plant-block bootstrap replicates")
    lo = _quantile(boot_slopes, 0.025)
    hi = _quantile(boot_slopes, 0.975)

    # Secondary, outcome-agnostic diagnostics preserve the full randomized
    # response curve. A peaked response can coexist with a zero linear ITT
    # slope; the diagnostic must never change the registered benefit status.
    by_rank_ci = {
        str(rank): [
            _quantile([profile[rank] for profile in boot_profiles], 0.025),
            _quantile([profile[rank] for profile in boot_profiles], 0.975),
        ]
        for rank in ranks
    }
    adjacent = {
        f"{left}_to_{right}": observed_profile[right] - observed_profile[left]
        for left, right in zip(ranks, ranks[1:])
    }
    central_contrast = _central_vs_endpoints(observed_profile, ranks)
    central_ci = [
        _quantile(
            [_central_vs_endpoints(profile, ranks) for profile in boot_profiles], q
        ) for q in (0.025, 0.975)
    ]
    best_rank = max(ranks, key=lambda rank: observed_profile[rank])
    descriptive_profile = {
        "mean_pollen_grains_by_assigned_rank": {
            str(rank): observed_profile[rank] for rank in ranks
        },
        "plant_cluster_bootstrap_mean_ci95_by_rank": by_rank_ci,
        "adjacent_rank_mean_differences": adjacent,
        "predefined_central_vs_endpoints_contrast": central_contrast,
        "predefined_central_vs_endpoints_bootstrap_ci95": central_ci,
        "highest_observed_mean_rank": best_rank,
        "interior_peak_in_observed_means": best_rank not in (ranks[0], ranks[-1]),
        "status": "DESCRIPTIVE_NON_GATING_NOT_A_PURE_FUNCTION_OPTIMUM",
    }

    null_at_least_as_positive = 0
    for _ in range(config["permutation_reps"]):
        permuted = []
        for block in block_list:
            shuffled = [row["pollen_grains"] for row in block]
            rng.shuffle(shuffled)
            permuted.append([
                {**row, "pollen_grains": new}
                for row, new in zip(block, shuffled, strict=True)
            ])
        if _slope_within_plant(permuted) >= observed - 1e-12:
            null_at_least_as_positive += 1
    p_one_sided = (
        null_at_least_as_positive + 1
    ) / (config["permutation_reps"] + 1)

    supported = (
        lo > config["min_slope"]
        and p_one_sided <= config["alpha"]
    )
    return {
        "analysis": "pedicularis_randomized_z_pollen_function_v1",
        "receipt_schema": "PEDICULARIS_RANDOMIZED_POLLEN_FUNCTION_V1",
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "experimental_unit": "NATURALLY_POLLINATED_SEPARATE_POLLEN_SENTINEL_FLOWER",
        "randomized_coordinate": "ASSIGNED_PHYSICAL_Z_SETTING_RANK",
        "effect_units": "STIGMATIC_POLLEN_GRAINS_PER_ASSIGNED_RANK",
        "assigned_z_rank_itt_slope": observed,
        "plant_cluster_bootstrap_slope_ci95": [lo, hi],
        "one_sided_within_plant_randomization_p": p_one_sided,
        "preregistered_min_effect_per_rank": config["min_slope"],
        "preregistered_one_sided_alpha": config["alpha"],
        "pollen_benefit_supported_in_tested_population_season": supported,
        "non_gating_randomized_dose_response": descriptive_profile,
        "nuisance_checks": checks,
        "p0_qualification_sha256": _semantic_sha256(p0_receipt),
        "sentinel_assignment_sha256": _semantic_sha256(allocation),
        "sentinel_data_sha256": _semantic_sha256(sorted(
            rows, key=lambda row: (row["plant_id"], row["flower_id"])
        )),
        "frozen_inference_config_sha256": _semantic_sha256(config_payload),
        "status": (
            "RANDOMIZED_EXSERTION_TREATMENT_INCREASES_POLLEN_RECEIPT"
            if supported else "RANDOMIZED_EXSERTION_POLLEN_BENEFIT_NOT_ESTABLISHED"
        ),
        "claim_ceiling": [
            "causal_intention_to_treat_effect_of_randomized_physical_z_settings",
            "does_not_identify_pure_pollinator_function_optimum",
            "descriptive_dose_response_does_not_change_primary_ITT_status",
            "pollen_receipt_under_open_access_does_not_by_itself_prove_pollinator_mediation",
            "no_predator_G_causal_effect_in_sentinel_flowers",
            "no_same_flower_pollen_seed_covariance",
            "not_a_W1_W2_or_causal_compromise_receipt",
            "cannot_be_inserted_into_original_single_flower_P2_raw_rows",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Estimate causal stigmatic-pollen response to randomized exsertion "
            "using independent destructive pollen sentinel flowers"
        )
    )
    parser.add_argument("completed_sentinel_csv", type=Path)
    parser.add_argument("sentinel_allocation_receipt_json", type=Path)
    parser.add_argument("qualified_p0_receipt_json", type=Path)
    parser.add_argument("cohort_registry_csv", type=Path)
    parser.add_argument("frozen_sentinel_inference_config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    receipt = build(
        _read(args.completed_sentinel_csv),
        _load(args.sentinel_allocation_receipt_json),
        _load(args.qualified_p0_receipt_json),
        cohort._read(args.cohort_registry_csv),
        _load(args.frozen_sentinel_inference_config_json),
    )
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

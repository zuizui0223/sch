from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from scripts import analyze_pedicularis_full_surface as surface


PLACEHOLDER = "REQUIRED_BEFORE_USE"
CONFIG_SCHEMA = "PEDICULARIS_FULL_SURFACE_ALLOCATION_CONFIG_V1"
CONFIG_STATUS = "PEDICULARIS_FULL_SURFACE_ALLOCATION_PROSPECTIVELY_FROZEN"
POWER_ANALYSIS = "pedicularis_W1_W2_full_surface_power_v1"
POWER_STATUS = "PEDICULARIS_W1_W2_POWER_SIMULATION_COMPLETE"
ALLOCATION_METHOD = "SHA256_BALANCED_CYCLIC_Z_BY_P_BY_G_V1"
CELL_STRATEGY = "BALANCED_CYCLIC_RANDOMIZED_Z_BY_P_BY_G_V1"
STATE_PLAN = (
    ("P0G0", "SUPPLEMENTED", "EXCLUDED"),
    ("P1G0", "NATURAL", "EXCLUDED"),
    ("P0G1", "SUPPLEMENTED", "EXPOSED"),
    ("P1G1", "NATURAL", "EXPOSED"),
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError(f"{path} has no data rows")
    return rows


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _resolved_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"{label} must be prospectively resolved")
    return value.strip()


def _positive_int(value: object, label: str) -> int:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be prospectively resolved")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(numeric) or numeric < 1 or not numeric.is_integer():
        raise ValueError(f"{label} must be a positive integer")
    return int(numeric)


def _nonnegative_int(value: object, label: str) -> int:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be prospectively resolved")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(numeric) or numeric < 0 or not numeric.is_integer():
        raise ValueError(f"{label} must be a nonnegative integer")
    return int(numeric)


def _finite_number(value: object, label: str) -> float:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be prospectively resolved")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(numeric):
        raise ValueError(f"{label} must be finite")
    return numeric


def _semantic_sha256(payload: object) -> str:
    text = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _validate_config(config: dict) -> dict:
    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError(f"allocation config schema must be {CONFIG_SCHEMA}")
    if config.get("status") != CONFIG_STATUS:
        raise ValueError("P2 allocation config is not prospectively frozen")
    if config.get("frozen_before_full_surface_outcomes") is not True:
        raise ValueError(
            "P2 allocation config must be frozen before full-surface outcomes"
        )

    population_id = _resolved_text(
        config.get("population_id"), "population_id"
    )
    season_id = _resolved_text(config.get("season_id"), "season_id")
    n_plants = _positive_int(
        config.get("planned_n_plants"), "planned_n_plants"
    )
    flowers_per_plant = _positive_int(
        config.get("flowers_per_plant"), "flowers_per_plant"
    )
    total = n_plants * flowers_per_plant
    p0_level_plan_sha256 = _resolved_text(
        config.get("p0_level_plan_sha256"),
        "p0_level_plan_sha256",
    )
    if (
        len(p0_level_plan_sha256) != 64
        or any(ch not in "0123456789abcdef" for ch in p0_level_plan_sha256.lower())
    ):
        raise ValueError("p0_level_plan_sha256 must be a 64-character hexadecimal digest")

    z_rows = config.get("z_levels")
    if not isinstance(z_rows, list) or len(z_rows) < 5:
        raise ValueError("z_levels must contain at least five levels")

    normalized_z = []
    labels: set[str] = set()
    ranks: set[int] = set()
    targets: set[float] = set()
    setting_ids: set[str] = set()
    for row in z_rows:
        if not isinstance(row, dict):
            raise ValueError("each z_levels row must be an object")
        label = _resolved_text(
            row.get("assigned_z_level"), "z_levels.assigned_z_level"
        )
        rank = _nonnegative_int(
            row.get("assigned_z_rank"),
            "z_levels.assigned_z_rank",
        )
        target = _finite_number(
            row.get("target_exsertion"), "z_levels.target_exsertion"
        )
        setting_id = _resolved_text(
            row.get("manipulation_setting_id"),
            "z_levels.manipulation_setting_id",
        )
        if label in labels:
            raise ValueError("assigned_z_level must be unique")
        if rank in ranks:
            raise ValueError("assigned_z_rank must be unique")
        if target in targets:
            raise ValueError("target_exsertion must be unique")
        if setting_id in setting_ids:
            raise ValueError("manipulation_setting_id must be unique")
        labels.add(label)
        ranks.add(rank)
        targets.add(target)
        setting_ids.add(setting_id)
        normalized_z.append(
            {
                "assigned_z_level": label,
                "assigned_z_rank": rank,
                "target_exsertion": target,
                "manipulation_setting_id": setting_id,
            }
        )

    normalized_z.sort(key=lambda row: row["assigned_z_rank"])
    if [row["assigned_z_rank"] for row in normalized_z] != list(
        range(len(normalized_z))
    ):
        raise ValueError("assigned_z_rank must form contiguous 0..k-1 ranks")

    n_surface_cells = len(normalized_z) * len(STATE_PLAN)
    if flowers_per_plant > n_surface_cells:
        raise ValueError(
            "flowers_per_plant cannot exceed the number of z x P x G cells"
        )
    if total % n_surface_cells != 0:
        raise ValueError(
            "planned_n_plants x flowers_per_plant must be divisible by the "
            "number of z x P x G cells"
        )

    excluded_method = _resolved_text(
        config.get("excluded_method_code"), "excluded_method_code"
    )
    exposed_method = _resolved_text(
        config.get("exposed_method_code"), "exposed_method_code"
    )
    if excluded_method == exposed_method:
        raise ValueError(
            "excluded_method_code and exposed_method_code must differ"
        )

    return {
        "population_id": population_id,
        "season_id": season_id,
        "planned_n_plants": n_plants,
        "flowers_per_plant": flowers_per_plant,
        "n_surface_cells": n_surface_cells,
        "replicates_per_cell": total // n_surface_cells,
        "z_levels": normalized_z,
        "p0_level_plan_sha256": p0_level_plan_sha256,
        "excluded_method_code": excluded_method,
        "exposed_method_code": exposed_method,
    }


def _validate_power(power: dict, config: dict) -> dict:
    if power.get("analysis") != POWER_ANALYSIS:
        raise ValueError("power receipt is not the W1/W2 production planner")
    if power.get("status") != POWER_STATUS:
        raise ValueError("W1/W2 power receipt is not complete")
    if power.get("registered_field_allocation_recommendation_allowed") is not True:
        raise ValueError(
            "W1/W2 power receipt is not authorized for registered P2 field allocation"
        )
    if power.get("p0_f0_config_binding_status") != (
        "PEDICULARIS_W1_W2_P0_F0_CONFIG_EXACTLY_BOUND"
    ):
        raise ValueError(
            "W1/W2 power receipt lacks exact final-three P0/F0 config binding"
        )
    production_config_sha = power.get("production_surface_config_sha256")
    threshold_freeze_sha = power.get("surface_threshold_freeze_sha256")
    power_config_sha = power.get("power_config_sha256")
    for value, label in (
        (production_config_sha, "production_surface_config_sha256"),
        (threshold_freeze_sha, "surface_threshold_freeze_sha256"),
        (power_config_sha, "power_config_sha256"),
    ):
        if not isinstance(value, str) or len(value) != 64:
            raise ValueError(f"W1/W2 power receipt lacks {label}")

    provenance = power.get("planning_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("power receipt lacks planning_provenance")
    if provenance.get("population_id") != config["population_id"]:
        raise ValueError("power and allocation population_id do not match")
    if provenance.get("season_id") != config["season_id"]:
        raise ValueError("power and allocation season_id do not match")

    powered_design = power.get("powered_design")
    if not isinstance(powered_design, dict):
        raise ValueError(
            "power receipt lacks powered_design; rerun the current W1/W2 planner"
        )
    field_design = powered_design.get("field_design")
    if not isinstance(field_design, dict):
        raise ValueError("power receipt lacks powered field_design")
    if field_design.get("allocation_strategy") != CELL_STRATEGY:
        raise ValueError("power receipt uses a different allocation strategy")
    if int(field_design.get("flowers_per_plant", -1)) != config[
        "flowers_per_plant"
    ]:
        raise ValueError(
            "allocation flowers_per_plant does not match powered design"
        )

    powered_z = powered_design.get("nominal_z_levels")
    if not isinstance(powered_z, list):
        raise ValueError("power receipt lacks nominal_z_levels")
    configured_targets = [
        row["target_exsertion"] for row in config["z_levels"]
    ]
    if [float(value) for value in powered_z] != configured_targets:
        raise ValueError(
            "allocation target_exsertion grid does not match powered z levels"
        )

    candidates = power.get("candidate_results")
    if not isinstance(candidates, list):
        raise ValueError("power receipt lacks candidate_results")
    matches = [
        row
        for row in candidates
        if int(row.get("plants", -1)) == config["planned_n_plants"]
    ]
    if len(matches) != 1:
        raise ValueError(
            "planned_n_plants must match exactly one evaluated power candidate"
        )
    candidate = matches[0]

    primary_target = float(power["target_primary_surface_power"])
    headline_target = float(power["target_headline_w1_or_w2_power"])
    primary_power = float(candidate["primary_surface_power"])
    headline_power = float(candidate["headline_W1_or_W2_power"])
    if primary_power < primary_target:
        raise ValueError(
            "planned_n_plants does not meet primary-surface power target"
        )
    if headline_power < headline_target:
        raise ValueError(
            "planned_n_plants does not meet W1/W2 headline power target"
        )

    expected_total = (
        config["planned_n_plants"] * config["flowers_per_plant"]
    )
    if int(candidate.get("total_full_surface_flowers", -1)) != expected_total:
        raise ValueError(
            "power candidate total flowers do not match allocation design"
        )

    return {
        "target_truth_world": power.get("target_truth_world"),
        "target_primary_surface_power": primary_target,
        "target_headline_w1_or_w2_power": headline_target,
        "candidate_primary_surface_power": primary_power,
        "candidate_headline_w1_or_w2_power": headline_power,
        "powered_design": powered_design,
        "production_surface_config_sha256": production_config_sha,
        "surface_threshold_freeze_sha256": threshold_freeze_sha,
        "power_config_sha256": power_config_sha,
        "power_receipt_sha256": _semantic_sha256(power),
    }


def _validate_readiness(
    readiness: dict,
    config: dict,
) -> dict:
    surface._validate_readiness(
        readiness,
        config["population_id"],
        config["season_id"],
    )
    validated = readiness.get("validated_execution")
    if not isinstance(validated, dict):
        raise ValueError("P2 allocation readiness lacks validated execution")

    if validated.get("p0_level_plan_sha256") != config[
        "p0_level_plan_sha256"
    ]:
        raise ValueError(
            "P2 allocation P0 level-plan SHA-256 does not match readiness"
        )

    expected_z_levels = [
        row["assigned_z_level"] for row in config["z_levels"]
    ]
    if validated.get("z_levels") != expected_z_levels:
        raise ValueError(
            "P2 allocation z-level labels do not match validated P0 readiness"
        )

    expected_settings = [
        {
            "assigned_z_level": row["assigned_z_level"],
            "assigned_z_rank": row["assigned_z_rank"],
            "manipulation_setting_id": row["manipulation_setting_id"],
        }
        for row in config["z_levels"]
    ]
    if validated.get("z_manipulation_settings") != expected_settings:
        raise ValueError(
            "P2 allocation physical z-manipulation settings do not match readiness"
        )

    if validated.get("g_exclusion_method") != config["excluded_method_code"]:
        raise ValueError(
            "P2 allocation EXCLUDED method does not match validated G readiness"
        )
    if validated.get("g_exposed_sham_method") != config[
        "exposed_method_code"
    ]:
        raise ValueError(
            "P2 allocation EXPOSED sham method does not match validated G readiness"
        )

    return {
        "readiness_receipt_sha256": _semantic_sha256(readiness),
        "p0_level_plan_sha256": validated["p0_level_plan_sha256"],
        "z_levels": list(validated["z_levels"]),
        "z_manipulation_settings": list(
            validated["z_manipulation_settings"]
        ),
        "p1_experimental_unit": validated["p_experimental_unit"],
        "g_exclusion_method": validated["g_exclusion_method"],
        "g_exposed_sham_method": validated["g_exposed_sham_method"],
    }


def _validate_manifest(
    rows: list[dict[str, str]],
    config: dict,
) -> dict[str, list[str]]:
    required = {"population_id", "season_id", "plant_id", "flower_id"}
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError(
            "full-surface flower manifest lacks columns: "
            + ", ".join(missing)
        )

    by_plant: dict[str, list[str]] = {}
    all_flowers: set[str] = set()

    for row in rows:
        if row["population_id"] != config["population_id"]:
            raise ValueError("manifest population_id does not match config")
        if row["season_id"] != config["season_id"]:
            raise ValueError("manifest season_id does not match config")
        plant_id = _resolved_text(row["plant_id"], "manifest plant_id")
        flower_id = _resolved_text(row["flower_id"], "manifest flower_id")
        if flower_id in all_flowers:
            raise ValueError("flower_id must be unique across the P2 manifest")
        all_flowers.add(flower_id)
        by_plant.setdefault(plant_id, []).append(flower_id)

    if len(by_plant) != config["planned_n_plants"]:
        raise ValueError(
            "manifest plant count does not match planned_n_plants"
        )

    wrong = {
        plant_id: len(flower_ids)
        for plant_id, flower_ids in by_plant.items()
        if len(flower_ids) != config["flowers_per_plant"]
    }
    if wrong:
        detail = ", ".join(
            f"{plant}={count}" for plant, count in sorted(wrong.items())
        )
        raise ValueError(
            "every P2 plant must supply exactly flowers_per_plant flowers; "
            + detail
        )

    return by_plant


def _hash_rank(
    values: list[str],
    *,
    prefix: list[str],
) -> list[str]:
    decorated = []
    for value in values:
        token = "\x1f".join([*prefix, value])
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        decorated.append((digest, value))
    return [value for _, value in sorted(decorated)]


def _cell_plan(config: dict, allocation_seed: str) -> list[dict]:
    cells = []
    for z in config["z_levels"]:
        for state_id, pollination, predator in STATE_PLAN:
            method = (
                config["excluded_method_code"]
                if predator == "EXCLUDED"
                else config["exposed_method_code"]
            )
            cells.append(
                {
                    "cell_id": f"{z['assigned_z_level']}__{state_id}",
                    "assigned_z_level": z["assigned_z_level"],
                    "assigned_z_rank": z["assigned_z_rank"],
                    "target_exsertion": z["target_exsertion"],
                    "manipulation_setting_id": z["manipulation_setting_id"],
                    "state_id": state_id,
                    "pollination_treatment": pollination,
                    "predator_treatment": predator,
                    "exclusion_method": method,
                }
            )

    by_id = {cell["cell_id"]: cell for cell in cells}
    ranked = _hash_rank(
        list(by_id),
        prefix=[
            allocation_seed,
            config["population_id"],
            config["season_id"],
            "CELL_ORDER",
        ],
    )
    return [by_id[cell_id] for cell_id in ranked]


def build(
    manifest_rows: list[dict[str, str]],
    config_payload: dict,
    power_receipt: dict,
    readiness_receipt: dict,
    allocation_seed: str,
) -> tuple[list[dict[str, str]], dict]:
    allocation_seed = allocation_seed.strip()
    if not allocation_seed or allocation_seed == PLACEHOLDER:
        raise ValueError("allocation_seed must be precommitted and resolved")

    config = _validate_config(config_payload)
    power = _validate_power(power_receipt, config)
    readiness = _validate_readiness(readiness_receipt, config)
    by_plant = _validate_manifest(manifest_rows, config)

    plant_order = _hash_rank(
        sorted(by_plant),
        prefix=[
            allocation_seed,
            config["population_id"],
            config["season_id"],
            "PLANT_ORDER",
        ],
    )
    cells = _cell_plan(config, allocation_seed)
    k = config["flowers_per_plant"]

    allocations = []
    cell_counts: Counter[str] = Counter()

    for plant_rank, plant_id in enumerate(plant_order):
        start = (plant_rank * k) % len(cells)
        selected_cells = [
            cells[(start + offset) % len(cells)]
            for offset in range(k)
        ]
        if len({cell["cell_id"] for cell in selected_cells}) != k:
            raise ValueError("allocator produced a duplicate cell within plant")

        flower_order = _hash_rank(
            by_plant[plant_id],
            prefix=[
                allocation_seed,
                config["population_id"],
                config["season_id"],
                plant_id,
                "FLOWER_ORDER",
            ],
        )

        for flower_id, cell in zip(
            flower_order,
            selected_cells,
            strict=True,
        ):
            cell_counts[cell["cell_id"]] += 1
            allocations.append(
                {
                    "population_id": config["population_id"],
                    "season_id": config["season_id"],
                    "plant_id": plant_id,
                    "flower_id": flower_id,
                    "assigned_z_level": cell["assigned_z_level"],
                    "assigned_z_rank": str(cell["assigned_z_rank"]),
                    "target_exsertion": repr(cell["target_exsertion"]),
                    "manipulation_setting_id": cell["manipulation_setting_id"],
                    "pollination_treatment": cell["pollination_treatment"],
                    "predator_treatment": cell["predator_treatment"],
                    "exclusion_method": cell["exclusion_method"],
                    "allocation_cell_id": cell["cell_id"],
                    "assignment_method": ALLOCATION_METHOD,
                    "field_status": "ALLOCATED_NOT_YET_MEASURED",
                }
            )

    expected_per_cell = config["replicates_per_cell"]
    if set(cell_counts) != {cell["cell_id"] for cell in cells}:
        raise ValueError("not all full-surface z x P x G cells were allocated")
    if set(cell_counts.values()) != {expected_per_cell}:
        raise ValueError("full-surface allocation is not exactly cell-balanced")

    canonical_allocations = sorted(
        allocations,
        key=lambda row: (
            row["plant_id"],
            row["flower_id"],
        ),
    )
    allocation_digest = _semantic_sha256(canonical_allocations)

    receipt = {
        "analysis": "pedicularis_full_surface_balanced_allocation_v1",
        "receipt_schema": "PEDICULARIS_FULL_SURFACE_ALLOCATION_V1",
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "n_plants": config["planned_n_plants"],
        "flowers_per_plant": config["flowers_per_plant"],
        "n_allocated_flowers": len(allocations),
        "n_surface_cells": config["n_surface_cells"],
        "replicates_per_cell": expected_per_cell,
        "exact_cell_balance": True,
        "cell_counts": dict(sorted(cell_counts.items())),
        "z_levels": config["z_levels"],
        "p0_level_plan_sha256": config["p0_level_plan_sha256"],
        "excluded_method_code": config["excluded_method_code"],
        "exposed_method_code": config["exposed_method_code"],
        "allocation_strategy": CELL_STRATEGY,
        "allocation_algorithm": ALLOCATION_METHOD,
        "allocation_seed": allocation_seed,
        "allocation_seed_sha256": hashlib.sha256(
            allocation_seed.encode("utf-8")
        ).hexdigest(),
        "allocation_identity_sha256": allocation_digest,
        "allocation_config_sha256": _semantic_sha256(config_payload),
        "power_binding": power,
        "production_surface_config_sha256": power[
            "production_surface_config_sha256"
        ],
        "surface_threshold_freeze_sha256": power[
            "surface_threshold_freeze_sha256"
        ],
        "power_config_sha256": power["power_config_sha256"],
        "readiness_binding": readiness,
        "readiness_receipt_sha256": readiness[
            "readiness_receipt_sha256"
        ],
        "sample_size_chosen_by_script": False,
        "flowers_per_plant_chosen_by_script": False,
        "z_levels_chosen_by_script": False,
        "status": "P2_FULL_SURFACE_ALLOCATED_NOT_YET_MEASURED",
        "next_step": (
            "apply the frozen z/P/G treatments by flower_id, record the full "
            "surface outcomes, and verify allocation identity before analysis"
        ),
        "claim_ceiling": [
            "field_allocation_only",
            "power_design_to_field_execution_binding",
            "production_surface_threshold_config_bound_from_power_to_field",
            "positive_readiness_bound_before_field_allocation",
            "validated_P0_z_settings_and_G0_G1_methods_match_allocation",
            "treatment_blind_flower_registration_before_assignment",
            "exact_global_z_by_P_by_G_cell_balance",
            "no_duplicate_cell_within_plant",
            "does_not_choose_sample_size",
            "does_not_choose_z_levels",
            "does_not_generate_outcomes",
            "does_not_validate_causal_compromise",
        ],
    }
    return allocations, receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Bind a prospectively powered P. rex P2 design to treatment-blind "
            "flower IDs with exact balanced z x P x G allocation"
        )
    )
    parser.add_argument("flower_manifest_csv", type=Path)
    parser.add_argument("allocation_config_json", type=Path)
    parser.add_argument("power_receipt_json", type=Path)
    parser.add_argument("readiness_v3_json", type=Path)
    parser.add_argument("--allocation-seed", required=True)
    parser.add_argument("--allocations-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    allocations, receipt = build(
        _read_csv(args.flower_manifest_csv),
        _load_json(args.allocation_config_json),
        _load_json(args.power_receipt_json),
        _load_json(args.readiness_v3_json),
        args.allocation_seed,
    )
    _write_csv(args.allocations_out, allocations)
    args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_out.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

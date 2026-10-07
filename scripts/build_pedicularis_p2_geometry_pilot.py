from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from scripts import analyze_pedicularis_full_surface as surface
from scripts.build_pedicularis_full_surface_allocation import (
    CELL_STRATEGY,
    STATE_PLAN,
    _semantic_sha256,
)
from scripts.bind_pedicularis_geometry_intervention_plan import (
    SCHEMA as INTERVENTION_BINDING_SCHEMA,
    STATUS as INTERVENTION_BINDING_STATUS,
)


PLACEHOLDER = "REQUIRED_BEFORE_USE"
CONFIG_SCHEMA = "PEDICULARIS_P2_GEOMETRY_PILOT_CONFIG_V1"
CONFIG_STATUS = "PEDICULARIS_P2_GEOMETRY_PILOT_PROSPECTIVELY_FROZEN"
RECEIPT_SCHEMA = "PEDICULARIS_P2_GEOMETRY_PILOT_ALLOCATION_V1"
ALLOCATION_METHOD = "SHA256_BALANCED_CYCLIC_GEOMETRY_PILOT_V1"
PROVENANCE_FIELDS = (
    "assigned_z_rank",
    "target_exsertion",
    "allocation_cell_id",
    "assignment_method",
    "pilot_role",
    "plant_accrual_rank",
    "first_precision_look_n",
)
OUTPUT_FIELDS = (*surface.RAW_FIELDS, *PROVENANCE_FIELDS)


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


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"{label} must be prospectively resolved")
    return value.strip()


def _number(value: object, label: str) -> float:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be prospectively resolved")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{label} must be finite")
    return out


def _positive_int(value: object, label: str) -> int:
    out = _number(value, label)
    if out < 1 or not out.is_integer():
        raise ValueError(f"{label} must be a positive integer")
    return int(out)


def _nonnegative_int(value: object, label: str) -> int:
    out = _number(value, label)
    if out < 0 or not out.is_integer():
        raise ValueError(f"{label} must be a nonnegative integer")
    return int(out)


def _validate_config(config: dict) -> dict:
    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError(f"geometry-pilot config schema must be {CONFIG_SCHEMA}")
    if config.get("status") != CONFIG_STATUS:
        raise ValueError("geometry-pilot config is not prospectively frozen")
    if config.get("frozen_before_geometry_outcomes") is not True:
        raise ValueError("geometry-pilot config must be frozen before pilot outcomes")
    if config.get("pilot_role") != "POWER_BASIS_ONLY_NEVER_CONFIRMATORY":
        raise ValueError("geometry pilot must be POWER_BASIS_ONLY_NEVER_CONFIRMATORY")
    if config.get("allocation_strategy") != CELL_STRATEGY:
        raise ValueError(f"allocation_strategy must be {CELL_STRATEGY}")

    precision_gate = config.get("precision_gate")
    if not isinstance(precision_gate, dict):
        raise ValueError("precision_gate must be frozen before geometry allocation")
    bootstrap_reps = _positive_int(
        precision_gate.get("bootstrap_reps"),
        "precision_gate.bootstrap_reps",
    )
    if bootstrap_reps < 200:
        raise ValueError("precision_gate.bootstrap_reps must be >=200")
    for field in (
        "min_valid_bootstrap_fraction",
        "min_interior_concave_fraction_per_state",
    ):
        value = _number(
            precision_gate.get(field),
            f"precision_gate.{field}",
        )
        if not 0 < value <= 1:
            raise ValueError(f"precision_gate.{field} must lie in (0,1]")
    max_width = _number(
        precision_gate.get("max_normalized_95ci_width_per_power_basis_path"),
        "precision_gate.max_normalized_95ci_width_per_power_basis_path",
    )
    if max_width <= 0:
        raise ValueError(
            "precision_gate.max_normalized_95ci_width_per_power_basis_path must be >0"
        )

    population_id = _text(config.get("population_id"), "population_id")
    season_id = _text(config.get("season_id"), "season_id")
    n_plants = _positive_int(config.get("planned_n_plants"), "planned_n_plants")
    flowers_per_plant = _positive_int(
        config.get("flowers_per_plant"), "flowers_per_plant"
    )
    raw_looks = config.get("candidate_cumulative_plants")
    if not isinstance(raw_looks, list) or not raw_looks:
        raise ValueError(
            "candidate_cumulative_plants must be a non-empty prospectively frozen list"
        )
    cumulative_looks = [
        _positive_int(value, "candidate_cumulative_plants")
        for value in raw_looks
    ]
    if cumulative_looks != sorted(set(cumulative_looks)):
        raise ValueError(
            "candidate_cumulative_plants must be strictly increasing and unique"
        )
    if cumulative_looks[-1] != n_plants:
        raise ValueError(
            "planned_n_plants must equal the final candidate_cumulative_plants value"
        )

    z_rows = config.get("z_levels")
    if not isinstance(z_rows, list) or len(z_rows) < 5:
        raise ValueError("geometry pilot requires at least five z levels")

    normalized_z = []
    labels: set[str] = set()
    ranks: set[int] = set()
    targets: set[float] = set()
    setting_ids: set[str] = set()
    for row in z_rows:
        if not isinstance(row, dict):
            raise ValueError("each z_levels entry must be an object")
        label = _text(row.get("assigned_z_level"), "assigned_z_level")
        rank = _nonnegative_int(row.get("assigned_z_rank"), "assigned_z_rank")
        target = _number(row.get("target_exsertion"), "target_exsertion")
        setting_id = _text(
            row.get("manipulation_setting_id"),
            "manipulation_setting_id",
        )
        if label in labels or rank in ranks or target in targets:
            raise ValueError("z labels, ranks and target exsertion values must be unique")
        if setting_id in setting_ids:
            raise ValueError("manipulation_setting_id must be unique across z levels")
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

    n_cells = len(normalized_z) * len(STATE_PLAN)
    if flowers_per_plant > n_cells:
        raise ValueError("flowers_per_plant cannot exceed the number of surface cells")
    total = n_plants * flowers_per_plant
    if total % n_cells != 0:
        raise ValueError(
            "planned_n_plants x flowers_per_plant must be divisible by "
            "n_z_levels x 2 P x 2 G for exact balance"
        )
    for stage_n in cumulative_looks:
        if (stage_n * flowers_per_plant) % n_cells != 0:
            raise ValueError(
                "every candidate_cumulative_plants value x flowers_per_plant "
                "must be divisible by n_z_levels x 2 P x 2 G so every planned "
                "precision look is exactly balanced"
            )

    excluded_method = _text(
        config.get("excluded_method_code"), "excluded_method_code"
    )
    exposed_method = _text(
        config.get("exposed_method_code"), "exposed_method_code"
    )
    if excluded_method == exposed_method:
        raise ValueError("excluded and exposed method codes must differ")

    return {
        "population_id": population_id,
        "season_id": season_id,
        "planned_n_plants": n_plants,
        "candidate_cumulative_plants": cumulative_looks,
        "flowers_per_plant": flowers_per_plant,
        "z_levels": normalized_z,
        "n_surface_cells": n_cells,
        "replicates_per_cell": total // n_cells,
        "excluded_method_code": excluded_method,
        "exposed_method_code": exposed_method,
        "pilot_role": "POWER_BASIS_ONLY_NEVER_CONFIRMATORY",
        "precision_gate": {
            "bootstrap_reps": bootstrap_reps,
            "random_seed": int(precision_gate.get("random_seed", 20261006)),
            "min_valid_bootstrap_fraction": float(
                precision_gate["min_valid_bootstrap_fraction"]
            ),
            "min_interior_concave_fraction_per_state": float(
                precision_gate["min_interior_concave_fraction_per_state"]
            ),
            "max_normalized_95ci_width_per_power_basis_path": max_width,
        },
    }


def _validate_manifest(
    rows: list[dict[str, str]],
    config: dict,
) -> dict[str, list[str]]:
    required = {"population_id", "season_id", "plant_id", "flower_id"}
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError("geometry-pilot manifest lacks columns: " + ", ".join(missing))

    by_plant: dict[str, list[str]] = {}
    all_flowers: set[str] = set()
    for row in rows:
        if row["population_id"] != config["population_id"]:
            raise ValueError("manifest population_id does not match pilot config")
        if row["season_id"] != config["season_id"]:
            raise ValueError("manifest season_id does not match pilot config")
        plant_id = _text(row["plant_id"], "plant_id")
        flower_id = _text(row["flower_id"], "flower_id")
        if flower_id in all_flowers:
            raise ValueError("flower_id must be globally unique in geometry pilot")
        all_flowers.add(flower_id)
        by_plant.setdefault(plant_id, []).append(flower_id)

    if len(by_plant) != config["planned_n_plants"]:
        raise ValueError("manifest plant count does not match planned_n_plants")
    wrong = {
        plant: len(flowers)
        for plant, flowers in by_plant.items()
        if len(flowers) != config["flowers_per_plant"]
    }
    if wrong:
        details = ", ".join(
            f"{plant}={count}" for plant, count in sorted(wrong.items())
        )
        raise ValueError(
            "every geometry-pilot plant must supply exactly flowers_per_plant; "
            + details
        )
    return by_plant


def _rank(values: list[str], prefix: list[str]) -> list[str]:
    decorated = []
    for value in values:
        token = "\x1f".join([*prefix, value])
        decorated.append(
            (hashlib.sha256(token.encode("utf-8")).hexdigest(), value)
        )
    return [value for _, value in sorted(decorated)]


def _cells(config: dict, allocation_seed: str) -> list[dict[str, str]]:
    cells = []
    for z in config["z_levels"]:
        for state_id, pollination, predator in STATE_PLAN:
            cells.append(
                {
                    "cell_id": f"{z['assigned_z_level']}__{state_id}",
                    "assigned_z_level": z["assigned_z_level"],
                    "assigned_z_rank": str(z["assigned_z_rank"]),
                    "target_exsertion": repr(z["target_exsertion"]),
                    "manipulation_setting_id": z["manipulation_setting_id"],
                    "pollination_treatment": pollination,
                    "predator_treatment": predator,
                    "exclusion_method": (
                        config["excluded_method_code"]
                        if predator == "EXCLUDED"
                        else config["exposed_method_code"]
                    ),
                }
            )
    by_id = {row["cell_id"]: row for row in cells}
    order = _rank(
        list(by_id),
        [
            allocation_seed,
            config["population_id"],
            config["season_id"],
            "GEOMETRY_CELL_ORDER",
        ],
    )
    return [by_id[cell_id] for cell_id in order]


def build(
    manifest_rows: list[dict[str, str]],
    config_payload: dict,
    intervention_binding: dict,
    allocation_seed: str,
) -> tuple[list[dict[str, str]], dict]:
    allocation_seed = allocation_seed.strip()
    if not allocation_seed or allocation_seed == PLACEHOLDER:
        raise ValueError("allocation_seed must be precommitted and resolved")

    config = _validate_config(config_payload)

    if intervention_binding.get("receipt_schema") != INTERVENTION_BINDING_SCHEMA:
        raise ValueError("geometry intervention-plan binding schema mismatch")
    if intervention_binding.get("status") != INTERVENTION_BINDING_STATUS:
        raise ValueError("geometry intervention plan is not prospectively frozen")
    if intervention_binding.get("population_id") != config["population_id"]:
        raise ValueError(
            "geometry intervention binding population does not match pilot config"
        )
    if intervention_binding.get("season_id") != config["season_id"]:
        raise ValueError(
            "geometry intervention binding season does not match pilot config"
        )
    if intervention_binding.get("geometry_config_sha256") != _semantic_sha256(
        config_payload
    ):
        raise ValueError(
            "geometry intervention binding is not tied to the exact pilot config"
        )

    expected_z = [
        {
            "assigned_z_level": row["assigned_z_level"],
            "assigned_z_rank": str(row["assigned_z_rank"]),
            "manipulation_setting_id": row["manipulation_setting_id"],
        }
        for row in config["z_levels"]
    ]
    bound_z = [
        {
            "assigned_z_level": row["assigned_z_level"],
            "assigned_z_rank": str(row["assigned_z_rank"]),
            "manipulation_setting_id": row["manipulation_setting_id"],
        }
        for row in intervention_binding.get("z_level_plan", [])
    ]
    if expected_z != bound_z:
        raise ValueError(
            "geometry intervention binding z/manipulation plan does not match pilot config"
        )
    if intervention_binding.get("p1_experimental_unit") != (
        "WITHIN_PLANT_PAIRED_FLOWERS"
    ):
        raise ValueError(
            "geometry intervention binding lacks current paired-flower P1 plan"
        )
    if intervention_binding.get("g_exclusion_method") != config[
        "excluded_method_code"
    ]:
        raise ValueError(
            "geometry excluded method does not match bound confirmatory G method"
        )
    if intervention_binding.get("g_exposed_sham_method") != config[
        "exposed_method_code"
    ]:
        raise ValueError(
            "geometry exposed method does not match bound confirmatory G sham"
        )
    if intervention_binding.get(
        "geometry_analysis_requires_later_positive_readiness_v3"
    ) is not True:
        raise ValueError(
            "geometry intervention binding must defer analysis until readiness V3"
        )

    by_plant = _validate_manifest(manifest_rows, config)

    plant_order = _rank(
        sorted(by_plant),
        [
            allocation_seed,
            config["population_id"],
            config["season_id"],
            "GEOMETRY_PLANT_ORDER",
        ],
    )
    cells = _cells(config, allocation_seed)
    k = config["flowers_per_plant"]

    rows = []
    counts: Counter[str] = Counter()
    for plant_rank, plant_id in enumerate(plant_order):
        one_based_rank = plant_rank + 1
        first_precision_look_n = next(
            stage_n
            for stage_n in config["candidate_cumulative_plants"]
            if stage_n >= one_based_rank
        )
        start = (plant_rank * k) % len(cells)
        selected = [cells[(start + offset) % len(cells)] for offset in range(k)]
        if len({row["cell_id"] for row in selected}) != k:
            raise ValueError("geometry allocator produced duplicate cell within plant")

        flower_order = _rank(
            by_plant[plant_id],
            [
                allocation_seed,
                config["population_id"],
                config["season_id"],
                plant_id,
                "GEOMETRY_FLOWER_ORDER",
            ],
        )
        for flower_id, cell in zip(flower_order, selected, strict=True):
            counts[cell["cell_id"]] += 1
            row = {field: "" for field in OUTPUT_FIELDS}
            row.update(
                {
                    "population_id": config["population_id"],
                    "season_id": config["season_id"],
                    "plant_id": plant_id,
                    "flower_id": flower_id,
                    "assigned_z_level": cell["assigned_z_level"],
                    "manipulation_setting_id": cell["manipulation_setting_id"],
                    "pollination_treatment": cell["pollination_treatment"],
                    "predator_treatment": cell["predator_treatment"],
                    "exclusion_method": cell["exclusion_method"],
                    "assigned_z_rank": cell["assigned_z_rank"],
                    "target_exsertion": cell["target_exsertion"],
                    "allocation_cell_id": cell["cell_id"],
                    "assignment_method": ALLOCATION_METHOD,
                    "pilot_role": config["pilot_role"],
                    "plant_accrual_rank": str(one_based_rank),
                    "first_precision_look_n": str(first_precision_look_n),
                }
            )
            rows.append(row)

    if set(counts) != {row["cell_id"] for row in cells}:
        raise ValueError("not all geometry-pilot cells were allocated")
    if set(counts.values()) != {config["replicates_per_cell"]}:
        raise ValueError("geometry-pilot allocation is not exactly balanced")

    frozen_fields = (
        "population_id",
        "season_id",
        "plant_id",
        "flower_id",
        "assigned_z_level",
        "manipulation_setting_id",
        "pollination_treatment",
        "predator_treatment",
        "exclusion_method",
        *PROVENANCE_FIELDS,
    )
    frozen_rows = sorted(
        [
            {field: row[field] for field in frozen_fields}
            for row in rows
        ],
        key=lambda row: (row["plant_id"], row["flower_id"]),
    )

    receipt = {
        "analysis": "pedicularis_p2_geometry_pilot_allocation_v1",
        "receipt_schema": RECEIPT_SCHEMA,
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "n_plants": config["planned_n_plants"],
        "candidate_cumulative_plants": config["candidate_cumulative_plants"],
        "plant_accrual_order": plant_order,
        "flowers_per_plant": config["flowers_per_plant"],
        "n_surface_cells": config["n_surface_cells"],
        "replicates_per_cell": config["replicates_per_cell"],
        "n_allocated_flowers": len(rows),
        "exact_cell_balance": True,
        "cell_counts": dict(sorted(counts.items())),
        "precision_look_designs": [
            {
                "cumulative_plants": stage_n,
                "cumulative_flowers": stage_n * config["flowers_per_plant"],
                "replicates_per_cell": (
                    stage_n
                    * config["flowers_per_plant"]
                    // config["n_surface_cells"]
                ),
            }
            for stage_n in config["candidate_cumulative_plants"]
        ],
        "z_levels": config["z_levels"],
        "allocation_strategy": CELL_STRATEGY,
        "allocation_algorithm": ALLOCATION_METHOD,
        "allocation_seed": allocation_seed,
        "allocation_seed_sha256": hashlib.sha256(
            allocation_seed.encode("utf-8")
        ).hexdigest(),
        "config_sha256": _semantic_sha256(config_payload),
        "intervention_plan_binding_sha256": _semantic_sha256(
            intervention_binding
        ),
        "intervention_plan_binding_status": intervention_binding["status"],
        "bound_intervention_plan": {
            "p0_level_plan_sha256": intervention_binding[
                "p0_level_plan_sha256"
            ],
            "p0_field_config_sha256": intervention_binding[
                "p0_field_config_sha256"
            ],
            "p1_field_config_sha256": intervention_binding[
                "p1_field_config_sha256"
            ],
            "g_field_config_sha256": intervention_binding[
                "g_field_config_sha256"
            ],
            "g_method_selection_sha256": intervention_binding[
                "g_method_selection_sha256"
            ],
            "z_levels": [
                row["assigned_z_level"]
                for row in intervention_binding["z_level_plan"]
            ],
            "z_manipulation_settings": intervention_binding[
                "z_manipulation_settings"
            ],
            "p1_experimental_unit": intervention_binding[
                "p1_experimental_unit"
            ],
            "g_exclusion_method": intervention_binding[
                "g_exclusion_method"
            ],
        },
        "precision_gate": config["precision_gate"],
        "precision_gate_frozen_before_outcomes": True,
        "frozen_identity_sha256": _semantic_sha256(frozen_rows),
        "expected_frozen_rows": frozen_rows,
        "pilot_role": config["pilot_role"],
        "confirmatory_eligible": False,
        "threshold_basis_eligible": False,
        "status": "P2_GEOMETRY_PILOT_ALLOCATED_NOT_YET_MEASURED",
        "claim_ceiling": [
            "nonconfirmatory_power_basis_only",
            "collection_allowed_after_preoutcome_intervention_plan_binding",
            "analysis_and_basis_use_still_require_later_positive_readiness_V3",
            "precision_gate_frozen_before_any_geometry_outcomes",
            "cumulative_precision_looks_frozen_before_any_geometry_outcomes",
            "exact_balanced_randomized_z_P_G_allocation",
            "never_enters_confirmatory_P2_inference",
            "does_not_choose_pilot_sample_size",
            "does_not_generate_biological_outcomes",
        ],
    }
    return rows, receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(OUTPUT_FIELDS))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Allocate a separate nonconfirmatory P. rex z x P x G mini-surface "
            "for W1/W2 power-basis geometry and variance estimation"
        )
    )
    parser.add_argument("flower_manifest_csv", type=Path)
    parser.add_argument("pilot_config_json", type=Path)
    parser.add_argument("intervention_plan_binding_json", type=Path)
    parser.add_argument("--allocation-seed", required=True)
    parser.add_argument("--field-sheet-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    rows, receipt = build(
        _read_csv(args.flower_manifest_csv),
        _load_json(args.pilot_config_json),
        _load_json(args.intervention_plan_binding_json),
        args.allocation_seed,
    )
    _write_csv(args.field_sheet_out, rows)
    args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_out.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

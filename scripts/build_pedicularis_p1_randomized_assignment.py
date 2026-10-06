from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from scripts.pedicularis_config_freeze import (
    FREEZE_STATUS,
    validate_prospective_freeze,
)


PLACEHOLDER = "REQUIRED_BEFORE_USE"
ALLOCATION_SCHEMA = "PEDICULARIS_P1_RANDOMIZED_ALLOCATION_V1"
ALLOCATION_STATUS = "P1_FLOWERS_RANDOMIZED_NOT_YET_MEASURED"
CONFIG_SCHEMA = "PEDICULARIS_P1_ALLOCATION_CONFIG_V1"
CONFIG_STATUS = "PEDICULARIS_P1_ALLOCATION_PROSPECTIVELY_FROZEN"
P1_FIELD_CONFIG_STATUS = "PEDICULARIS_P1_FIELD_CONFIG_FROZEN"
EXPERIMENTAL_UNIT = "WITHIN_PLANT_PAIRED_FLOWERS"
ASSIGNMENT_METHOD = "SHA256_WITHIN_PLANT_BALANCED_P1_V1"
ARM_PLAN = (
    ("NATURAL", "SHAM_STIGMA_CONTACT"),
    ("SUPPLEMENTED", "DONOR_MIXED_CROSS_POLLEN"),
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


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"{label} must be resolved prospectively")
    return value.strip()


def _positive_int(value: object, label: str) -> int:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be resolved prospectively")
    try:
        numeric = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if (
        not math.isfinite(numeric)
        or numeric < 1
        or not numeric.is_integer()
    ):
        raise ValueError(f"{label} must be a positive integer")
    return int(numeric)


def _semantic_sha256(payload: object) -> str:
    text = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _validate_allocation_config(config: dict) -> dict:
    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError(f"P1 allocation config schema must be {CONFIG_SCHEMA}")
    if config.get("status") != CONFIG_STATUS:
        raise ValueError("P1 allocation config is not prospectively frozen")
    if config.get("frozen_before_confirmatory_outcomes") is not True:
        raise ValueError(
            "P1 allocation config must be frozen before confirmatory outcomes"
        )
    population_id = _text(config.get("population_id"), "population_id")
    season_id = _text(config.get("season_id"), "season_id")
    planned = _positive_int(
        config.get("planned_paired_plants"),
        "planned_paired_plants",
    )
    flowers_per_arm = _positive_int(
        config.get("flowers_per_treatment_per_plant"),
        "flowers_per_treatment_per_plant",
    )
    return {
        "population_id": population_id,
        "season_id": season_id,
        "planned_paired_plants": planned,
        "flowers_per_treatment_per_plant": flowers_per_arm,
        "flowers_per_plant": flowers_per_arm * len(ARM_PLAN),
    }


def _validate_p1_field_config(
    p1_config: dict,
    allocation: dict,
) -> dict:
    if p1_config.get("status") != P1_FIELD_CONFIG_STATUS:
        raise ValueError(
            "P1 randomized confirmatory allocation requires the F0-assembled "
            "PEDICULARIS_P1_FIELD_CONFIG_FROZEN config"
        )
    freeze = validate_prospective_freeze(p1_config, "P1")
    if freeze["status"] != FREEZE_STATUS:
        raise ValueError("P1 threshold freeze is not positive")
    if freeze.get("population_id") != allocation["population_id"]:
        raise ValueError("P1 field config and allocation population_id differ")
    if freeze.get("season_id") != allocation["season_id"]:
        raise ValueError("P1 field config and allocation season_id differ")

    block = p1_config.get("pollination_weight")
    if not isinstance(block, dict):
        raise ValueError("P1 field config lacks pollination_weight block")
    if block.get("experimental_unit") != EXPERIMENTAL_UNIT:
        raise ValueError(
            "current P1 allocation supports only WITHIN_PLANT_PAIRED_FLOWERS"
        )

    min_plants = _positive_int(
        block.get("min_paired_plants"),
        "pollination_weight.min_paired_plants",
    )
    min_flowers = _positive_int(
        block.get("min_flowers_per_treatment"),
        "pollination_weight.min_flowers_per_treatment",
    )
    planned_plants = allocation["planned_paired_plants"]
    flowers_per_arm = allocation["flowers_per_treatment_per_plant"]
    planned_flowers_per_treatment = planned_plants * flowers_per_arm

    if planned_plants < min_plants:
        raise ValueError(
            "planned_paired_plants is below frozen P1 min_paired_plants"
        )
    if planned_flowers_per_treatment < min_flowers:
        raise ValueError(
            "planned flowers per treatment are below frozen "
            "min_flowers_per_treatment"
        )

    return {
        "freeze": freeze,
        "min_paired_plants": min_plants,
        "min_flowers_per_treatment": min_flowers,
        "planned_flowers_per_treatment": planned_flowers_per_treatment,
        "p1_field_config_sha256": _semantic_sha256(p1_config),
    }


def _validate_manifest(
    rows: list[dict[str, str]],
    allocation: dict,
) -> dict[str, list[str]]:
    required = {"population_id", "season_id", "plant_id", "flower_id"}
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError(
            "P1 treatment-blind flower manifest lacks columns: "
            + ", ".join(missing)
        )

    by_plant: dict[str, list[str]] = {}
    all_flowers: set[str] = set()
    for row in rows:
        if row["population_id"] != allocation["population_id"]:
            raise ValueError("P1 manifest population_id does not match config")
        if row["season_id"] != allocation["season_id"]:
            raise ValueError("P1 manifest season_id does not match config")
        plant_id = _text(row["plant_id"], "manifest plant_id")
        flower_id = _text(row["flower_id"], "manifest flower_id")
        if flower_id in all_flowers:
            raise ValueError("flower_id must be globally unique in P1 manifest")
        all_flowers.add(flower_id)
        by_plant.setdefault(plant_id, []).append(flower_id)

    if len(by_plant) != allocation["planned_paired_plants"]:
        raise ValueError(
            "P1 manifest plant count does not match planned_paired_plants"
        )

    required_per_plant = allocation["flowers_per_plant"]
    wrong = {
        plant_id: len(ids)
        for plant_id, ids in by_plant.items()
        if len(ids) != required_per_plant
    }
    if wrong:
        detail = ", ".join(
            f"{plant}={count}" for plant, count in sorted(wrong.items())
        )
        raise ValueError(
            "each P1 plant must supply exactly "
            f"{required_per_plant} treatment-blind flowers; {detail}"
        )
    return by_plant


def _hash_order(
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


def build(
    manifest_rows: list[dict[str, str]],
    allocation_config: dict,
    p1_field_config: dict,
    allocation_seed: str,
) -> tuple[list[dict[str, str]], dict]:
    allocation_seed = allocation_seed.strip()
    if not allocation_seed or allocation_seed == PLACEHOLDER:
        raise ValueError("allocation_seed must be precommitted and resolved")

    allocation = _validate_allocation_config(allocation_config)
    field_basis = _validate_p1_field_config(p1_field_config, allocation)
    by_plant = _validate_manifest(manifest_rows, allocation)

    allocations = []
    k = allocation["flowers_per_treatment_per_plant"]
    for plant_id in sorted(by_plant):
        randomized = _hash_order(
            by_plant[plant_id],
            prefix=[
                allocation_seed,
                allocation["population_id"],
                allocation["season_id"],
                plant_id,
            ],
        )
        arms = [
            arm
            for arm in ARM_PLAN
            for _ in range(k)
        ]
        for flower_id, (treatment, handling) in zip(
            randomized,
            arms,
            strict=True,
        ):
            allocations.append(
                {
                    "population_id": allocation["population_id"],
                    "season_id": allocation["season_id"],
                    "plant_id": plant_id,
                    "flower_id": flower_id,
                    "pollination_treatment": treatment,
                    "pollination_handling_role": handling,
                    "assignment_method": ASSIGNMENT_METHOD,
                    "field_status": "ALLOCATED_NOT_YET_MEASURED",
                }
            )

    expected_assignments = sorted(
        [
            {
                "population_id": row["population_id"],
                "season_id": row["season_id"],
                "plant_id": row["plant_id"],
                "flower_id": row["flower_id"],
                "pollination_treatment": row["pollination_treatment"],
                "pollination_handling_role": row[
                    "pollination_handling_role"
                ],
            }
            for row in allocations
        ],
        key=lambda row: (
            row["population_id"],
            row["season_id"],
            row["plant_id"],
            row["flower_id"],
        ),
    )
    identity_digest = _semantic_sha256(expected_assignments)

    treatment_counts = {
        treatment: sum(
            row["pollination_treatment"] == treatment
            for row in allocations
        )
        for treatment, _ in ARM_PLAN
    }
    expected_arm_n = field_basis["planned_flowers_per_treatment"]
    if set(treatment_counts.values()) != {expected_arm_n}:
        raise ValueError("P1 allocation failed exact treatment balance")

    receipt = {
        "analysis": "pedicularis_p1_randomized_allocation_v1",
        "receipt_schema": ALLOCATION_SCHEMA,
        "population_id": allocation["population_id"],
        "season_id": allocation["season_id"],
        "experimental_unit": EXPERIMENTAL_UNIT,
        "n_paired_plants": allocation["planned_paired_plants"],
        "flowers_per_treatment_per_plant": k,
        "n_allocated_flowers": len(allocations),
        "n_by_treatment": treatment_counts,
        "minimum_paired_plants_gate": field_basis["min_paired_plants"],
        "minimum_flowers_per_treatment_gate": field_basis[
            "min_flowers_per_treatment"
        ],
        "p1_field_config_sha256": field_basis["p1_field_config_sha256"],
        "threshold_freeze_status": field_basis["freeze"]["status"],
        "assignment_randomized_within_plant": True,
        "assignment_method": ASSIGNMENT_METHOD,
        "allocation_seed": allocation_seed,
        "allocation_seed_sha256": hashlib.sha256(
            allocation_seed.encode("utf-8")
        ).hexdigest(),
        "allocation_identity_sha256": identity_digest,
        "allocation_config_sha256": _semantic_sha256(allocation_config),
        "expected_assignments": expected_assignments,
        "sample_size_chosen_by_script": False,
        "experimental_unit_chosen_by_script": False,
        "status": ALLOCATION_STATUS,
        "next_step": (
            "apply sham stigma-contact or donor-mixed cross-pollen exactly by "
            "flower_id, record P1 outcomes, then run the locked P1 evaluator"
        ),
        "claim_ceiling": [
            "confirmatory_field_allocation_only",
            "paired_within_plant_randomization",
            "does_not_choose_sample_size",
            "does_not_choose_experimental_unit",
            "does_not_choose_effect_thresholds",
            "does_not_validate_pollination_weight",
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
            "Randomize treatment-blind P. rex confirmatory P1 flowers within "
            "plants to NATURAL sham handling or SUPPLEMENTED donor-mixed pollen"
        )
    )
    parser.add_argument("flower_manifest_csv", type=Path)
    parser.add_argument("allocation_config_json", type=Path)
    parser.add_argument("p1_field_config_json", type=Path)
    parser.add_argument("--allocation-seed", required=True)
    parser.add_argument("--allocations-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    allocations, receipt = build(
        _read_csv(args.flower_manifest_csv),
        _load_json(args.allocation_config_json),
        _load_json(args.p1_field_config_json),
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

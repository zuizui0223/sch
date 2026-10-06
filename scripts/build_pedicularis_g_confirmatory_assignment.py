from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256


PLACEHOLDER = "REQUIRED_BEFORE_USE"
SELECTION_SCHEMA = "PEDICULARIS_G_CONFIRMATORY_METHOD_SELECTION_V1"
SELECTION_STATUS = "PEDICULARIS_G_CONFIRMATORY_METHOD_SELECTED_BEFORE_OUTCOMES"
RECEIPT_SCHEMA = "PEDICULARIS_G_CONFIRMATORY_RANDOMIZED_ALLOCATION_V1"
ASSIGNMENT_METHOD = "SHA256_PAIRED_G_WITHIN_PLANT_V1"
FROZEN_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "predator_treatment",
    "exclusion_method",
    "sham_device_applied",
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("confirmatory G flower manifest has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("confirmatory G flower manifest is empty")
    return rows


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _rank(
    values: list[str],
    *,
    seed: str,
    population_id: str,
    season_id: str,
    plant_id: str,
) -> list[str]:
    decorated = []
    for value in values:
        token = "\x1f".join(
            [seed, population_id, season_id, plant_id, value]
        )
        decorated.append(
            (hashlib.sha256(token.encode("utf-8")).hexdigest(), value)
        )
    return [value for _, value in sorted(decorated)]


def build(
    rows: list[dict[str, str]],
    selection_receipt: dict,
    allocation_seed: str,
) -> tuple[list[dict[str, str]], dict]:
    allocation_seed = allocation_seed.strip()
    if not allocation_seed or allocation_seed == PLACEHOLDER:
        raise ValueError("allocation_seed must be precommitted and resolved")

    if selection_receipt.get("receipt_schema") != SELECTION_SCHEMA:
        raise ValueError("confirmatory G selection receipt schema mismatch")
    if selection_receipt.get("status") != SELECTION_STATUS:
        raise ValueError("confirmatory G method is not prospectively selected")

    required = {"population_id", "season_id", "plant_id", "flower_id"}
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError(
            "confirmatory G manifest lacks columns: " + ", ".join(missing)
        )

    population_id = selection_receipt["population_id"]
    season_id = selection_receipt["season_id"]
    n_plants = int(selection_receipt["planned_n_plants"])
    flowers_per_arm = int(
        selection_receipt["flowers_per_treatment_per_plant"]
    )
    expected_per_plant = 2 * flowers_per_arm

    by_plant: dict[str, list[str]] = {}
    all_flowers: set[str] = set()
    for row in rows:
        if row["population_id"] != population_id:
            raise ValueError("confirmatory G manifest population does not match selection")
        if row["season_id"] != season_id:
            raise ValueError("confirmatory G manifest season does not match selection")
        plant_id = row["plant_id"]
        flower_id = row["flower_id"]
        if not plant_id or plant_id == PLACEHOLDER:
            raise ValueError("every confirmatory G row needs a resolved plant_id")
        if not flower_id or flower_id == PLACEHOLDER:
            raise ValueError("every confirmatory G row needs a resolved flower_id")
        if flower_id in all_flowers:
            raise ValueError("flower_id must be globally unique in confirmatory G")
        all_flowers.add(flower_id)
        by_plant.setdefault(plant_id, []).append(flower_id)

    if len(by_plant) != n_plants:
        raise ValueError(
            "confirmatory G manifest plant count does not match frozen design"
        )
    wrong = {
        plant: len(flowers)
        for plant, flowers in by_plant.items()
        if len(flowers) != expected_per_plant
    }
    if wrong:
        detail = ", ".join(
            f"{plant}={count}" for plant, count in sorted(wrong.items())
        )
        raise ValueError(
            "every confirmatory G plant must supply exactly "
            f"{expected_per_plant} treatment-blind flowers; {detail}"
        )

    excluded_method = selection_receipt["selected_exclusion_method"]
    sham_method = selection_receipt["exposed_sham_method_code"]

    allocations = []
    for plant_id in sorted(by_plant):
        order = _rank(
            by_plant[plant_id],
            seed=allocation_seed,
            population_id=population_id,
            season_id=season_id,
            plant_id=plant_id,
        )
        arms = (
            [("EXPOSED", sham_method, "1")] * flowers_per_arm
            + [("EXCLUDED", excluded_method, "0")] * flowers_per_arm
        )
        for flower_id, (
            treatment,
            method,
            sham,
        ) in zip(order, arms, strict=True):
            allocations.append(
                {
                    "population_id": population_id,
                    "season_id": season_id,
                    "plant_id": plant_id,
                    "flower_id": flower_id,
                    "predator_treatment": treatment,
                    "exclusion_method": method,
                    "sham_device_applied": sham,
                    "assignment_method": ASSIGNMENT_METHOD,
                    "field_status": "ALLOCATED_NOT_YET_MEASURED",
                }
            )

    frozen_rows = sorted(
        [
            {field: row[field] for field in FROZEN_FIELDS}
            for row in allocations
        ],
        key=lambda row: (row["plant_id"], row["flower_id"]),
    )

    receipt = {
        "analysis": "pedicularis_g_confirmatory_randomized_allocation_v1",
        "receipt_schema": RECEIPT_SCHEMA,
        "population_id": population_id,
        "season_id": season_id,
        "selected_candidate_id": selection_receipt["selected_candidate_id"],
        "selected_exclusion_method": excluded_method,
        "exposed_sham_method_code": sham_method,
        "n_plants": n_plants,
        "flowers_per_treatment_per_plant": flowers_per_arm,
        "n_allocated_flowers": len(allocations),
        "n_flowers_per_treatment": n_plants * flowers_per_arm,
        "assignment_randomized_within_plant": True,
        "assignment_method": ASSIGNMENT_METHOD,
        "allocation_seed": allocation_seed,
        "allocation_seed_sha256": hashlib.sha256(
            allocation_seed.encode("utf-8")
        ).hexdigest(),
        "selection_receipt_sha256": _semantic_sha256(selection_receipt),
        "g_field_config_sha256": selection_receipt["g_field_config_sha256"],
        "allocation_identity_sha256": _semantic_sha256(frozen_rows),
        "expected_frozen_rows": frozen_rows,
        "status": "G_CONFIRMATORY_FLOWERS_RANDOMIZED_NOT_YET_MEASURED",
        "claim_ceiling": [
            "field_allocation_only",
            "paired_within_plant_randomization",
            "selected_method_frozen_before_confirmatory_outcomes",
            "does_not_choose_candidate",
            "does_not_choose_sample_size",
            "does_not_validate_G",
        ],
    }
    return allocations, receipt


def _write(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Randomize treatment-blind P. rex flowers within plants to the "
            "prospectively selected confirmatory G EXPOSED/EXCLUDED arms"
        )
    )
    parser.add_argument("flower_manifest_csv", type=Path)
    parser.add_argument("method_selection_receipt_json", type=Path)
    parser.add_argument("--allocation-seed", required=True)
    parser.add_argument("--allocations-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    allocations, receipt = build(
        _read(args.flower_manifest_csv),
        _load(args.method_selection_receipt_json),
        args.allocation_seed,
    )
    _write(args.allocations_out, allocations)
    args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_out.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


PLACEHOLDER = "REQUIRED_BEFORE_USE"
FLOWER_FIELDS = ("flower_id_1", "flower_id_2", "flower_id_3")
ARMS = (
    ("EXPOSED_SHAM", "EXPOSED", "SHAM_SLEEVE"),
    ("G_A1_FINE_MESH", "EXCLUDED", "FINE_MESH_LOWER_FRUIT_SLEEVE"),
    ("G_A2_POROUS_TUBING", "EXCLUDED", "POROUS_TUBING_LOWER_FRUIT_SLEEVE"),
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("G first-tier plant manifest has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("G first-tier plant manifest is empty")
    return rows


def _arm_order(
    randomization_key: str,
    population_id: str,
    season_id: str,
    plant_id: str,
) -> list[tuple[str, str, str]]:
    if not randomization_key or randomization_key == PLACEHOLDER:
        raise ValueError("randomization_key must be resolved before allocation")

    scored = []
    for arm in ARMS:
        token = "|".join(
            [randomization_key, population_id, season_id, plant_id, arm[0]]
        )
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        scored.append((digest, arm))
    return [arm for _, arm in sorted(scored)]


def build(
    rows: list[dict[str, str]],
    randomization_key: str,
) -> tuple[list[dict[str, str]], dict]:
    required = {
        "population_id",
        "season_id",
        "plant_id",
        *FLOWER_FIELDS,
    }
    missing_columns = sorted(required - set(rows[0]))
    if missing_columns:
        raise ValueError(
            "G first-tier manifest lacks columns: "
            + ", ".join(missing_columns)
        )

    contexts = {
        (row["population_id"], row["season_id"])
        for row in rows
    }
    if len(contexts) != 1:
        raise ValueError(
            "G first-tier pilot must use exactly one population and season"
        )
    population_id, season_id = next(iter(contexts))
    if (
        not population_id
        or not season_id
        or population_id == PLACEHOLDER
        or season_id == PLACEHOLDER
    ):
        raise ValueError("population_id and season_id must be resolved")

    plant_ids = [row["plant_id"] for row in rows]
    if any(not value or value == PLACEHOLDER for value in plant_ids):
        raise ValueError("every pilot row needs a resolved plant_id")
    if len(plant_ids) != len(set(plant_ids)):
        raise ValueError("plant_id must be unique in the first-tier manifest")

    if not randomization_key or randomization_key == PLACEHOLDER:
        raise ValueError("randomization_key must be resolved before allocation")

    all_flower_ids: list[str] = []
    allocations: list[dict[str, str]] = []

    for row in rows:
        flower_ids = [row[field] for field in FLOWER_FIELDS]
        if any(
            not value or value == PLACEHOLDER
            for value in flower_ids
        ):
            raise ValueError(
                f"plant {row['plant_id']} needs three resolved flower IDs"
            )
        if len(flower_ids) != len(set(flower_ids)):
            raise ValueError(
                f"plant {row['plant_id']} reuses a flower across G arms"
            )
        all_flower_ids.extend(flower_ids)

        randomized_arms = _arm_order(
            randomization_key,
            population_id,
            season_id,
            row["plant_id"],
        )
        for flower_id, (arm_id, treatment, method) in zip(
            flower_ids, randomized_arms
        ):
            allocations.append(
                {
                    "population_id": population_id,
                    "season_id": season_id,
                    "plant_id": row["plant_id"],
                    "flower_id": flower_id,
                    "pilot_arm_id": arm_id,
                    "predator_treatment": treatment,
                    "exclusion_method": method,
                    "sham_device_applied": (
                        "1" if treatment == "EXPOSED" else "0"
                    ),
                    "candidate_selected": "NO",
                    "randomization_algorithm": "SHA256_SORT_V1",
                    "field_status": "ALLOCATED_NOT_YET_MEASURED",
                }
            )

    if len(all_flower_ids) != len(set(all_flower_ids)):
        raise ValueError(
            "flower_id must be unique across the entire first-tier pilot"
        )

    receipt = {
        "analysis": "pedicularis_g_first_tier_pilot_manifest_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_plants": len(plant_ids),
        "n_allocated_flowers": len(allocations),
        "arms_per_plant": 3,
        "pilot_arm_ids": [arm[0] for arm in ARMS],
        "candidate_ids_tested": [
            "G_A1_FINE_MESH",
            "G_A2_POROUS_TUBING",
        ],
        "candidate_selected": False,
        "sample_size_chosen_by_script": False,
        "within_plant_randomized": True,
        "randomization_algorithm": "SHA256_SORT_V1",
        "randomization_key": randomization_key,
        "status": "G_FIRST_TIER_PILOT_ALLOCATED_NOT_YET_MEASURED",
        "next_step": (
            "freeze this allocation receipt before field outcomes; collect V4 "
            "timing/outcome fields using the canonical method codes, then run "
            "screen_pedicularis_g_candidates.py"
        ),
        "claim_ceiling": [
            "field_allocation_only",
            "within_plant_randomized_three_arm_comparison",
            "does_not_choose_number_of_plants",
            "does_not_choose_effect_or_selectivity_thresholds",
            "does_not_validate_any_candidate",
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
            "Build a randomized three-arm within-plant field allocation manifest "
            "for the two first-tier P. rex G barrier candidates"
        )
    )
    parser.add_argument("plant_manifest_csv", type=Path)
    parser.add_argument(
        "--randomization-key",
        required=True,
        help=(
            "Prospectively fixed key used for deterministic SHA256 within-plant "
            "arm allocation. Freeze it with the allocation receipt before outcomes."
        ),
    )
    parser.add_argument("--allocations-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    allocations, receipt = build(
        _read(args.plant_manifest_csv),
        args.randomization_key,
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

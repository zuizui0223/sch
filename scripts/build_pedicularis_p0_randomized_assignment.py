from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


PLACEHOLDER = "REQUIRED_BEFORE_USE"
ASSIGNMENT_METHOD = "SHA256_RANK_V1"


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


def _read_level_plan(path: Path) -> list[dict[str, str]]:
    rows = _read_csv(path)
    required = {"assigned_z_level", "assigned_z_rank", "sham_control"}
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError("P0 level plan lacks columns: " + ", ".join(missing))

    levels: list[dict[str, str]] = []
    seen_labels: set[str] = set()
    seen_ranks: set[int] = set()
    sham_count = 0

    for row in rows:
        label = row["assigned_z_level"]
        if not label or label == PLACEHOLDER:
            raise ValueError("every P0 level needs a resolved assigned_z_level")
        try:
            rank = int(row["assigned_z_rank"])
        except ValueError as exc:
            raise ValueError("assigned_z_rank must be an integer") from exc
        if row["sham_control"] not in {"0", "1"}:
            raise ValueError("sham_control must be coded 0/1")
        sham = int(row["sham_control"])
        sham_count += sham

        if label in seen_labels:
            raise ValueError("assigned_z_level must be unique")
        if rank in seen_ranks:
            raise ValueError("assigned_z_rank must be unique")
        seen_labels.add(label)
        seen_ranks.add(rank)

        levels.append(
            {
                "assigned_z_level": label,
                "assigned_z_rank": str(rank),
                "sham_control": str(sham),
            }
        )

    if len(levels) < 5:
        raise ValueError(
            "P0 randomized allocation requires at least five planned z levels"
        )
    if sham_count != 1:
        raise ValueError("P0 level plan must contain exactly one sham_control=1")

    return sorted(levels, key=lambda row: int(row["assigned_z_rank"]))


def _read_flowers(path: Path) -> tuple[list[dict[str, str]], str, str]:
    rows = _read_csv(path)
    required = {"population_id", "season_id", "plant_id", "flower_id"}
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError("P0 flower manifest lacks columns: " + ", ".join(missing))

    contexts = {
        (row["population_id"], row["season_id"])
        for row in rows
    }
    if len(contexts) != 1:
        raise ValueError(
            "P0 flower manifest must use exactly one population and season"
        )
    population_id, season_id = next(iter(contexts))
    if (
        not population_id
        or not season_id
        or population_id == PLACEHOLDER
        or season_id == PLACEHOLDER
    ):
        raise ValueError("population_id and season_id must be resolved")

    flower_ids: set[str] = set()
    for row in rows:
        if (
            not row["plant_id"]
            or row["plant_id"] == PLACEHOLDER
            or not row["flower_id"]
            or row["flower_id"] == PLACEHOLDER
        ):
            raise ValueError("plant_id and flower_id must be resolved")
        if row["flower_id"] in flower_ids:
            raise ValueError("flower_id must be unique across the P0 manifest")
        flower_ids.add(row["flower_id"])

    return rows, population_id, season_id


def _randomized_order(
    flower_ids: list[str],
    *,
    population_id: str,
    season_id: str,
    plant_id: str,
    allocation_seed: str,
) -> list[str]:
    decorated: list[tuple[str, str]] = []
    for flower_id in flower_ids:
        token = "\x1f".join(
            [
                allocation_seed,
                population_id,
                season_id,
                plant_id,
                flower_id,
            ]
        )
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        decorated.append((digest, flower_id))
    return [flower_id for _, flower_id in sorted(decorated)]


def build(
    flowers: list[dict[str, str]],
    levels: list[dict[str, str]],
    allocation_seed: str,
) -> tuple[list[dict[str, str]], dict]:
    allocation_seed = allocation_seed.strip()
    if not allocation_seed or allocation_seed == PLACEHOLDER:
        raise ValueError("allocation_seed must be resolved before allocation")

    contexts = {
        (row["population_id"], row["season_id"])
        for row in flowers
    }
    if len(contexts) != 1:
        raise ValueError("P0 allocation requires one population and season")
    population_id, season_id = next(iter(contexts))

    by_plant: dict[str, list[str]] = {}
    all_flower_ids: set[str] = set()
    for row in flowers:
        plant_id = row["plant_id"]
        flower_id = row["flower_id"]
        if not plant_id or plant_id == PLACEHOLDER:
            raise ValueError("plant_id must be resolved")
        if not flower_id or flower_id == PLACEHOLDER:
            raise ValueError("flower_id must be resolved")
        if flower_id in all_flower_ids:
            raise ValueError("flower_id must be unique across the P0 manifest")
        all_flower_ids.add(flower_id)
        by_plant.setdefault(plant_id, []).append(flower_id)

    n_levels = len(levels)
    if n_levels < 5:
        raise ValueError("P0 allocation requires at least five z levels")
    if sum(int(row["sham_control"]) for row in levels) != 1:
        raise ValueError("P0 level plan must contain exactly one sham_control=1")

    wrong_counts = {
        plant_id: len(ids)
        for plant_id, ids in by_plant.items()
        if len(ids) != n_levels
    }
    if wrong_counts:
        details = ", ".join(
            f"{plant_id}={count}"
            for plant_id, count in sorted(wrong_counts.items())
        )
        raise ValueError(
            "each P0 plant must supply exactly one flower per planned z level; "
            + details
        )

    sorted_levels = sorted(levels, key=lambda row: int(row["assigned_z_rank"]))
    allocations: list[dict[str, str]] = []
    for plant_id in sorted(by_plant):
        randomized_flowers = _randomized_order(
            by_plant[plant_id],
            population_id=population_id,
            season_id=season_id,
            plant_id=plant_id,
            allocation_seed=allocation_seed,
        )
        for flower_id, level in zip(
            randomized_flowers,
            sorted_levels,
            strict=True,
        ):
            allocations.append(
                {
                    "population_id": population_id,
                    "season_id": season_id,
                    "plant_id": plant_id,
                    "flower_id": flower_id,
                    "assigned_z_level": level["assigned_z_level"],
                    "assigned_z_rank": level["assigned_z_rank"],
                    "sham_control": level["sham_control"],
                    "assignment_method": ASSIGNMENT_METHOD,
                    "field_status": "ALLOCATED_NOT_YET_MEASURED",
                }
            )

    receipt = {
        "analysis": "pedicularis_p0_randomized_allocation_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_plants": len(by_plant),
        "n_z_levels": n_levels,
        "n_allocated_flowers": len(allocations),
        "z_levels": [row["assigned_z_level"] for row in sorted_levels],
        "z_ranks": [int(row["assigned_z_rank"]) for row in sorted_levels],
        "sham_z_rank": next(
            int(row["assigned_z_rank"])
            for row in sorted_levels
            if row["sham_control"] == "1"
        ),
        "assignment_randomized_within_plant": True,
        "allocation_algorithm": ASSIGNMENT_METHOD,
        "allocation_seed": allocation_seed,
        "allocation_seed_sha256": hashlib.sha256(
            allocation_seed.encode("utf-8")
        ).hexdigest(),
        "sample_size_chosen_by_script": False,
        "z_level_values_chosen_by_script": False,
        "status": "P0_FLOWERS_RANDOMIZED_NOT_YET_MEASURED",
        "next_step": (
            "apply the prospectively specified graded manipulation, collect "
            "Stage-P0 outcome fields, and merge them with this allocation "
            "before evaluate_pedicularis_stage_p0.py"
        ),
        "claim_ceiling": [
            "field_allocation_only",
            "complete_block_within_plant_randomization",
            "does_not_choose_number_of_plants",
            "does_not_choose_z_level_values",
            "does_not_choose_thresholds",
            "does_not_validate_p0",
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
            "Randomize treatment-blind P. rex flowers within plants across a "
            "prospectively specified Stage-P0 z-level plan"
        )
    )
    parser.add_argument("flower_manifest_csv", type=Path)
    parser.add_argument("level_plan_csv", type=Path)
    parser.add_argument("--allocation-seed", required=True)
    parser.add_argument("--allocations-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    flowers, _, _ = _read_flowers(args.flower_manifest_csv)
    levels = _read_level_plan(args.level_plan_csv)
    allocations, receipt = build(
        flowers,
        levels,
        allocation_seed=args.allocation_seed,
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

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from scripts.build_pedicularis_p0_randomized_assignment import (
    ASSIGNMENT_METHOD,
    _read_csv,
    _read_flowers,
    _read_level_plan,
    _randomized_order,
    _semantic_sha256,
)
from scripts.analyze_pedicularis_full_surface import (
    _validate_readiness,
)

RECEIPT_SCHEMA = "PEDICULARIS_P1_FRUIT_ONLY_RANDOMIZED_ALLOCATION_V1"
RECEIPT_STATUS = "FRUIT_ONLY_RANDOMIZED_NOT_YET_MEASURED"
FROZEN_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "assigned_z_level",
    "assigned_z_rank",
    "manipulation_setting_id",
    "sham_control",
    "pollination_treatment",
    "predator_treatment",
    "exclusion_method",
)


def build(
    flowers: list[dict[str, str]],
    levels: list[dict[str, str]],
    p0_receipt: dict,
    readiness: dict,
    allocation_seed: str,
) -> tuple[list[dict[str, str]], dict]:
    """Create a genuinely new NATURAL x predator G fruit allocation.

    Pollen is measured on another flower cohort. This allocator does not
    grant production P2 or confirmatory W1/W2 permission.
    """
    if p0_receipt.get("receipt_schema_version") != (
        "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1"
    ) or p0_receipt.get("status") != "PEDICULARIS_Z_MANIPULATION_VALIDATED":
        raise ValueError("fruit-only cohort needs positive focal P0 qualification")
    verified = p0_receipt.get("field_allocation_verification")
    if (
        not isinstance(verified, dict)
        or verified.get("receipt_schema") != "PEDICULARIS_P0_RANDOMIZED_ALLOCATION_V1"
        or verified.get("identity_z_assignment_match") is not True
        or verified.get("physical_manipulation_setting_match") is not True
    ):
        raise ValueError("P0 lacks exact randomized physical setting provenance")

    if not flowers:
        raise ValueError("fruit-only manifest is empty")
    contexts = {(f["population_id"], f["season_id"]) for f in flowers}
    if len(contexts) != 1:
        raise ValueError("fruit-only manifest must use one population/season")
    population, season = next(iter(contexts))
    if (population, season) != (
        p0_receipt.get("population_id"), p0_receipt.get("season_id")
    ):
        raise ValueError("fruit-only P0 and manifest population/season differ")
    _validate_readiness(readiness, population, season)
    if (
        readiness.get("source_receipts", {}).get("z", {}).get("receipt_sha256")
        != _semantic_sha256(p0_receipt)
    ):
        raise ValueError("fruit-only readiness not bound to supplied P0 qualification")

    setting_plan = [
        {
            "assigned_z_level": level["assigned_z_level"],
            "assigned_z_rank": int(level["assigned_z_rank"]),
            "manipulation_setting_id": level["manipulation_setting_id"],
        }
        for level in sorted(levels, key=lambda l: int(l["assigned_z_rank"]))
    ]
    if setting_plan != p0_receipt.get("z_manipulation_settings"):
        raise ValueError("fruit-only physical z levels differ from positive P0")
    if setting_plan != readiness["validated_execution"]["z_manipulation_settings"]:
        raise ValueError("fruit-only physical z levels differ from readiness")
    ranks = [item["assigned_z_rank"] for item in setting_plan]
    if ranks != list(range(len(ranks))):
        raise ValueError("fruit-only rank levels must be contiguous and start at zero")
    if len(ranks) < 5:
        raise ValueError("fruit-only G response needs >=5 physical z levels")

    if not isinstance(allocation_seed, str) or not allocation_seed.strip() or (
        allocation_seed == "REQUIRED_BEFORE_USE"
    ):
        raise ValueError("fruit-only allocation seed must be precommitted")
    by_plant: dict[str, list[str]] = defaultdict(list)
    seen: set[str] = set()
    for row in flowers:
        plant_id = row["plant_id"]
        flower_id = row["flower_id"]
        if not plant_id or not flower_id or flower_id in seen:
            raise ValueError("fruit-only manifest has missing or duplicate flower ID")
        seen.add(flower_id)
        by_plant[plant_id].append(flower_id)
    if any(len(ids) != 2 * len(levels) for ids in by_plant.values()):
        raise ValueError("fruit-only complete blocks require two flowers per z rank and plant")

    exposed_method = readiness["validated_execution"]["g_exposed_sham_method"]
    excluded_method = readiness["validated_execution"]["g_exclusion_method"]
    assignments: list[dict[str, str]] = []
    for plant_id in sorted(by_plant):
        ordered = _randomized_order(
            by_plant[plant_id],
            population_id=population,
            season_id=season,
            plant_id=plant_id,
            allocation_seed=allocation_seed,
        )
        combos = [
            (level, predator)
            for level in sorted(levels, key=lambda r: int(r["assigned_z_rank"]))
            for predator in ("EXCLUDED", "EXPOSED")
        ]
        for flower_id, (level, predator) in zip(ordered, combos, strict=True):
            assignments.append({
                "population_id": population,
                "season_id": season,
                "plant_id": plant_id,
                "flower_id": flower_id,
                "assigned_z_level": level["assigned_z_level"],
                "assigned_z_rank": level["assigned_z_rank"],
                "manipulation_setting_id": level["manipulation_setting_id"],
                "sham_control": level["sham_control"],
                "pollination_treatment": "NATURAL",
                "predator_treatment": predator,
                "exclusion_method": (
                    excluded_method if predator == "EXCLUDED" else exposed_method
                ),
                "assignment_method": ASSIGNMENT_METHOD,
                "field_status": "ALLOCATED_NOT_YET_MEASURED",
            })
    frozen_rows = sorted(
        [{field: row[field] for field in FROZEN_FIELDS} for row in assignments],
        key=lambda row: (row["plant_id"], row["flower_id"]),
    )
    receipt = {
        "analysis": "pedicularis_separate_natural_pollination_fruit_allocation_v1",
        "receipt_schema": RECEIPT_SCHEMA,
        "status": RECEIPT_STATUS,
        "population_id": population,
        "season_id": season,
        "n_plants": len(by_plant),
        "n_z_levels": len(ranks),
        "n_allocated_flowers": len(assignments),
        "z_manipulation_settings": setting_plan,
        "p0_qualification_sha256": _semantic_sha256(p0_receipt),
        "readiness_sha256": _semantic_sha256(readiness),
        "allocation_seed_sha256": _semantic_sha256(allocation_seed),
        "allocation_algorithm": ASSIGNMENT_METHOD,
        "frozen_fields": list(FROZEN_FIELDS),
        "expected_frozen_rows": frozen_rows,
        "allocation_identity_sha256": _semantic_sha256(frozen_rows),
        "experimental_unit": "FLOWERS_WITHIN_RANDOMIZED_PLANT_BLOCK",
        "cohort_role": "TWO_COHORT_FRUIT",
        "pollination_treatment": "NATURAL",
        "claim_ceiling": [
            "does_not_authorize_original_same_flower_P2_route",
            "G_exposure_independent_of_BITA_water_defence",
            "pollen_and_viable_seed_endpoints_remain_on_distinct_flower_IDs",
            "does_not_choose_sample_size_or_certify_no_within_plant_interference",
            "not_a_confirmatory_two_cohort_W1_W2_power_receipt",
        ],
    }
    return assignments, receipt


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Randomize separate fruit-bearing P. rex flowers over z x G"
    )
    parser.add_argument("treatment_blind_fruit_manifest_csv", type=Path)
    parser.add_argument("p0_level_plan_csv", type=Path)
    parser.add_argument("qualified_p0_receipt_json", type=Path)
    parser.add_argument("qualified_readiness_v3_json", type=Path)
    parser.add_argument("--allocation-seed", required=True)
    parser.add_argument("--allocations-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()
    flowers, _, _ = _read_flowers(args.treatment_blind_fruit_manifest_csv)
    levels = _read_level_plan(args.p0_level_plan_csv)
    p0 = json.loads(args.qualified_p0_receipt_json.read_text(encoding="utf-8"))
    readiness = json.loads(args.qualified_readiness_v3_json.read_text(encoding="utf-8"))
    allocations, receipt = build(flowers, levels, p0, readiness, args.allocation_seed)
    args.allocations_out.parent.mkdir(parents=True, exist_ok=True)
    with args.allocations_out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(allocations[0]))
        writer.writeheader()
        writer.writerows(allocations)
    args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_out.write_text(
        json.dumps(receipt, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()

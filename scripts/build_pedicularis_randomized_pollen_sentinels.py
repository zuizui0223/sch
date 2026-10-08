from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts.build_pedicularis_p0_randomized_assignment import (
    FROZEN_FIELDS,
    _read_csv,
    _read_level_plan,
    _semantic_sha256,
    build as randomized_z_build,
)


SCHEMA = "PEDICULARIS_RANDOMIZED_POLLEN_SENTINEL_ALLOCATION_V1"
STATUS = "POLLEN_SENTINEL_FLOWERS_RANDOMIZED_NOT_YET_MEASURED"


def build(
    flowers: list[dict[str, str]],
    levels: list[dict[str, str]],
    p0_qualification: dict,
    seed: str,
) -> tuple[list[dict[str, str]], dict]:
    if p0_qualification.get("receipt_schema_version") != (
        "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1"
    ):
        raise ValueError("pollen sentinels require the focal Stage P0 receipt")
    if p0_qualification.get("status") != "PEDICULARIS_Z_MANIPULATION_VALIDATED":
        raise ValueError("pollen sentinels require positive validated P0 manipulation")
    verification = p0_qualification.get("field_allocation_verification")
    if (
        not isinstance(verification, dict)
        or verification.get("receipt_schema")
        != "PEDICULARIS_P0_RANDOMIZED_ALLOCATION_V1"
        or verification.get("identity_z_assignment_match") is not True
    ):
        raise ValueError("P0 qualification lacks randomized physical-z provenance")

    expected = p0_qualification.get("z_manipulation_settings")
    actual = [
        {
            "assigned_z_level": row["assigned_z_level"],
            "assigned_z_rank": int(row["assigned_z_rank"]),
            "manipulation_setting_id": row["manipulation_setting_id"],
        }
        for row in sorted(levels, key=lambda x: int(x["assigned_z_rank"]))
    ]
    if expected != actual:
        raise ValueError(
            "sentinel z-level settings must match the validated P0 physical manipulation"
        )

    allocations, base = randomized_z_build(flowers, levels, seed)
    if base["population_id"] != p0_qualification.get("population_id"):
        raise ValueError("sentinel population does not match qualified P0")
    if base["season_id"] != p0_qualification.get("season_id"):
        raise ValueError("sentinel season does not match qualified P0")

    return allocations, {
        "analysis": "pedicularis_randomized_pollen_sentinel_allocation_v1",
        "receipt_schema": SCHEMA,
        "population_id": base["population_id"],
        "season_id": base["season_id"],
        "cohort_role": "POLLEN_SENTINEL",
        "n_plants": base["n_plants"],
        "n_z_levels": base["n_z_levels"],
        "n_allocated_flowers": base["n_allocated_flowers"],
        "z_manipulation_settings": expected,
        "p0_qualification_sha256": _semantic_sha256(p0_qualification),
        "p0_level_plan_sha256": base["level_plan_sha256"],
        "allocation_seed_sha256": base["allocation_seed_sha256"],
        "allocation_identity_sha256": base["allocation_identity_sha256"],
        "expected_frozen_rows": base["expected_frozen_rows"],
        "frozen_fields": list(FROZEN_FIELDS),
        "status": STATUS,
        "claim_ceiling": [
            "separate_sacrificial_pollen_sentinel_flowers",
            "randomized_z_under_natural_pollination_only",
            "not_a_G_treatment_or_seed_fitness_surface",
            "does_not_validate_W1_W2",
            "never_copy_pollen_counts_to_seed_flower_IDs",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Randomize disjoint P. rex pollen sentinel flowers across "
            "already validated physical exsertion settings"
        )
    )
    parser.add_argument("sentinel_manifest_csv", type=Path)
    parser.add_argument("frozen_p0_level_plan_csv", type=Path)
    parser.add_argument("positive_p0_qualification_json", type=Path)
    parser.add_argument("--allocation-seed", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path, required=True)
    args = parser.parse_args()

    flowers = _read_csv(args.sentinel_manifest_csv)
    levels = _read_level_plan(args.frozen_p0_level_plan_csv)
    qualification = json.loads(
        args.positive_p0_qualification_json.read_text(encoding="utf-8")
    )
    rows, receipt = build(flowers, levels, qualification, args.allocation_seed)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
    args.receipt_out.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROLE_RULES = {
    "CAL_A": {
        "lane": "MULTI",
        "threshold_basis_eligible": "YES",
        "confirmatory_eligible": "NO",
        "phase": "CALIBRATION",
    },
    "CAL_B_P1": {
        "lane": "P1",
        "threshold_basis_eligible": "YES",
        "confirmatory_eligible": "NO",
        "phase": "CALIBRATION",
    },
    "CAL_B_G": {
        "lane": "G",
        "threshold_basis_eligible": "YES",
        "confirmatory_eligible": "NO",
        "phase": "CALIBRATION",
    },
    "CAL_B_G_TIMING": {
        "lane": "G",
        "threshold_basis_eligible": "YES",
        "confirmatory_eligible": "NO",
        "phase": "CALIBRATION",
    },
    "CONFIRMATORY_P0": {
        "lane": "P0",
        "threshold_basis_eligible": "NO",
        "confirmatory_eligible": "YES",
        "phase": "CONFIRMATORY",
    },
    "CONFIRMATORY_P1": {
        "lane": "P1",
        "threshold_basis_eligible": "NO",
        "confirmatory_eligible": "YES",
        "phase": "CONFIRMATORY",
    },
    "CONFIRMATORY_G": {
        "lane": "G",
        "threshold_basis_eligible": "NO",
        "confirmatory_eligible": "YES",
        "phase": "CONFIRMATORY",
    },
    "FULL_SURFACE": {
        "lane": "P0_P1_G",
        "threshold_basis_eligible": "NO",
        "confirmatory_eligible": "YES",
        "phase": "FULL_SURFACE",
    },
    "POLLEN_SENTINEL": {
        "lane": "POLLEN",
        "threshold_basis_eligible": "NO",
        "confirmatory_eligible": "YES",
        "phase": "FULL_SURFACE",
    },
    "POWER_GEOMETRY_PILOT": {
        "lane": "P0_P1_G",
        "threshold_basis_eligible": "NO",
        "confirmatory_eligible": "NO",
        "phase": "POWER_BASIS",
    },
}

REQUIRED_FIELDS = (
    "record_id",
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "cohort_role",
    "lane",
    "threshold_basis_eligible",
    "confirmatory_eligible",
    "notes",
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("cohort registry has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError("missing required columns: " + ", ".join(missing))
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("cohort registry has no data rows")
    return rows


def validate(rows: list[dict[str, str]]) -> dict:
    record_ids = [row["record_id"] for row in rows]
    if len(record_ids) != len(set(record_ids)):
        raise ValueError("record_id must be unique")

    flower_ids = [row["flower_id"] for row in rows]
    if len(flower_ids) != len(set(flower_ids)):
        raise ValueError(
            "flower_id must be globally unique across calibration, confirmatory, "
            "and full-surface cohorts"
        )

    contexts = {(row["population_id"], row["season_id"]) for row in rows}
    if len(contexts) != 1:
        raise ValueError(
            "one active Pedicularis execution registry must target exactly one "
            "population and season"
        )

    phases: dict[str, set[str]] = {
        "CALIBRATION": set(),
        "POWER_BASIS": set(),
        "CONFIRMATORY": set(),
        "FULL_SURFACE": set(),
    }
    role_counts: dict[str, int] = {}

    for row in rows:
        role = row["cohort_role"]
        if role not in ROLE_RULES:
            raise ValueError(f"unregistered cohort_role: {role}")
        rule = ROLE_RULES[role]
        for field in ("lane", "threshold_basis_eligible", "confirmatory_eligible"):
            if row[field] != rule[field]:
                raise ValueError(
                    f"{field} mismatch for {role}: expected {rule[field]}, "
                    f"got {row[field]}"
                )
        if (
            row["threshold_basis_eligible"] == "YES"
            and row["confirmatory_eligible"] == "YES"
        ):
            raise ValueError(
                "one record cannot contribute to both threshold basis and "
                "confirmatory inference"
            )
        phases[rule["phase"]].add(row["plant_id"])
        role_counts[role] = role_counts.get(role, 0) + 1

    calibration_plants = phases["CALIBRATION"]
    power_basis_plants = phases["POWER_BASIS"]
    confirmatory_plants = phases["CONFIRMATORY"] | phases["FULL_SURFACE"]
    shared_plants = sorted(calibration_plants & confirmatory_plants)
    power_basis_overlap = sorted(
        power_basis_plants & (calibration_plants | confirmatory_plants)
    )
    if power_basis_overlap:
        raise ValueError(
            "POWER_GEOMETRY_PILOT plants must be disjoint from calibration and "
            "confirmatory/full-surface plants: " + ", ".join(power_basis_overlap)
        )

    if not shared_plants:
        independence = "PLANT_AND_FLOWER_LEVEL_DISJOINT"
    else:
        independence = "FLOWER_LEVEL_DISJOINT_PLANT_OVERLAP_PRESENT"

    population_id, season_id = next(iter(contexts))
    return {
        "analysis": "pedicularis_calibration_confirmatory_cohort_registry",
        "population_id": population_id,
        "season_id": season_id,
        "n_records": len(rows),
        "role_counts": dict(sorted(role_counts.items())),
        "n_calibration_plants": len(calibration_plants),
        "n_power_geometry_pilot_plants": len(power_basis_plants),
        "n_confirmatory_or_surface_plants": len(confirmatory_plants),
        "n_shared_plants_across_calibration_and_confirmatory": len(shared_plants),
        "power_geometry_pilot_plant_overlap_detected": False,
        "shared_plant_ids": shared_plants,
        "flower_level_reuse_detected": False,
        "independence_status": independence,
        "status": "PEDICULARIS_COHORT_REGISTRY_VALID",
        "claim_ceiling": [
            "flower_level_data_reuse_is_prohibited",
            "plant_level_overlap_is_reported_not_silently_ignored",
            "plant_level_overlap_does_not_make_calibration_data_confirmatory",
            "power_geometry_pilot_plants_are_disjoint_from_all_other_phases",
            "power_geometry_pilot_rows_are_neither_threshold_basis_nor_confirmatory",
            "threshold_basis_rows_cannot_be_confirmatory_rows",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Pedicularis calibration/confirmatory cohort separation"
    )
    parser.add_argument("registry", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = validate(_read(args.registry))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

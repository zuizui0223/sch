from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER = "REQUIRED_BEFORE_USE"
DEFAULT_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_PREDATOR_METHOD_TEMPLATE_V4.csv"
)

ARM_EXPECTATIONS = {
    "EXPOSED_SHAM": {
        "predator_treatment": "EXPOSED",
        "exclusion_method": "SHAM_SLEEVE",
        "sham_device_applied": "1",
    },
    "G_A1_FINE_MESH": {
        "predator_treatment": "EXCLUDED",
        "exclusion_method": "FINE_MESH_LOWER_FRUIT_SLEEVE",
        "sham_device_applied": "0",
    },
    "G_A2_POROUS_TUBING": {
        "predator_treatment": "EXCLUDED",
        "exclusion_method": "POROUS_TUBING_LOWER_FRUIT_SLEEVE",
        "sham_device_applied": "0",
    },
}
IDENTITY_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "pilot_arm_id",
    "predator_treatment",
    "exclusion_method",
    "sham_device_applied",
)
V4_IDENTITY_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "predator_treatment",
    "exclusion_method",
    "sham_device_applied",
)


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    return list(reader.fieldnames), rows


def _write_csv(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _canonical_identity_rows(
    rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    normalized = [
        {field: row[field] for field in IDENTITY_FIELDS}
        for row in rows
    ]
    return sorted(
        normalized,
        key=lambda row: (
            row["population_id"],
            row["season_id"],
            row["plant_id"],
            row["pilot_arm_id"],
            row["flower_id"],
        ),
    )


def _identity_digest(rows: list[dict[str, str]]) -> str:
    canonical = json.dumps(
        _canonical_identity_rows(rows),
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return _sha256_bytes(canonical)


def _validate_allocation_rows(rows: list[dict[str, str]]) -> tuple[str, str, int]:
    if not rows:
        raise ValueError("allocation manifest is empty")

    required = set(IDENTITY_FIELDS) | {
        "candidate_selected",
        "assignment_method",
        "field_status",
    }
    missing = sorted(required - set(rows[0]))
    if missing:
        raise ValueError(
            "allocation manifest lacks columns: " + ", ".join(missing)
        )

    contexts = {
        (row["population_id"], row["season_id"])
        for row in rows
    }
    if len(contexts) != 1:
        raise ValueError(
            "allocation manifest must contain exactly one population and season"
        )
    population_id, season_id = next(iter(contexts))
    if any(
        not value or value == PLACEHOLDER
        for value in (population_id, season_id)
    ):
        raise ValueError("allocation population_id and season_id must be resolved")

    plant_ids = [row["plant_id"] for row in rows]
    if any(
        not value or value == PLACEHOLDER
        for value in plant_ids
    ):
        raise ValueError("every allocation row needs a resolved plant_id")

    flower_ids = [row["flower_id"] for row in rows]
    if any(not value for value in flower_ids):
        raise ValueError("allocation manifest contains a blank flower_id")
    if len(flower_ids) != len(set(flower_ids)):
        raise ValueError("flower_id must be unique in the allocation manifest")

    by_plant: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_plant.setdefault(row["plant_id"], []).append(row)

        arm_id = row["pilot_arm_id"]
        if arm_id not in ARM_EXPECTATIONS:
            raise ValueError(f"unregistered first-tier pilot arm: {arm_id!r}")
        expected = ARM_EXPECTATIONS[arm_id]
        for field, value in expected.items():
            if row[field] != value:
                raise ValueError(
                    f"{arm_id} has {field}={row[field]!r}; expected {value!r}"
                )
        if row["candidate_selected"] != "NO":
            raise ValueError("candidate_selected must remain NO in the pilot")
        if row["assignment_method"] != "SHA256_RANK_V1":
            raise ValueError(
                "allocation manifest must use SHA256_RANK_V1 assignments"
            )
        if row["field_status"] != "ALLOCATED_NOT_YET_MEASURED":
            raise ValueError(
                "allocation manifest must be frozen before field outcomes"
            )

    expected_arms = set(ARM_EXPECTATIONS)
    for plant_id, plant_rows in by_plant.items():
        observed_arms = {row["pilot_arm_id"] for row in plant_rows}
        if len(plant_rows) != 3 or observed_arms != expected_arms:
            raise ValueError(
                f"plant {plant_id!r} must contain exactly the three first-tier arms"
            )

    return population_id, season_id, len(by_plant)


def _validate_allocation_receipt(
    receipt: dict,
    *,
    population_id: str,
    season_id: str,
    n_plants: int,
    n_rows: int,
) -> None:
    expected = {
        "population_id": population_id,
        "season_id": season_id,
        "n_plants": n_plants,
        "n_allocated_flowers": n_rows,
        "allocation_algorithm": "SHA256_RANK_V1",
        "assignment_randomized_within_plant": True,
        "status": "G_FIRST_TIER_PILOT_ALLOCATED_NOT_YET_MEASURED",
    }
    for field, value in expected.items():
        if receipt.get(field) != value:
            raise ValueError(
                f"allocation receipt mismatch for {field}: "
                f"{receipt.get(field)!r} != {value!r}"
            )

    seed = receipt.get("allocation_seed")
    seed_digest = receipt.get("allocation_seed_sha256")
    if not isinstance(seed, str) or not seed:
        raise ValueError("allocation receipt lacks allocation_seed")
    if seed_digest != _sha256_bytes(seed.encode("utf-8")):
        raise ValueError("allocation receipt seed digest does not match seed")


def prepare(
    allocation_rows: list[dict[str, str]],
    allocation_receipt: dict,
    v4_fieldnames: list[str],
    *,
    allocation_receipt_sha256: str | None = None,
) -> tuple[list[dict[str, str]], dict]:
    population_id, season_id, n_plants = _validate_allocation_rows(
        allocation_rows
    )
    _validate_allocation_receipt(
        allocation_receipt,
        population_id=population_id,
        season_id=season_id,
        n_plants=n_plants,
        n_rows=len(allocation_rows),
    )

    missing_v4 = sorted(set(V4_IDENTITY_FIELDS) - set(v4_fieldnames))
    if missing_v4:
        raise ValueError(
            "V4 template lacks identity columns: " + ", ".join(missing_v4)
        )

    field_rows = []
    for allocation in _canonical_identity_rows(allocation_rows):
        row = {field: "" for field in v4_fieldnames}
        for field in V4_IDENTITY_FIELDS:
            row[field] = allocation[field]
        field_rows.append(row)

    frozen_rows = _canonical_identity_rows(allocation_rows)
    lock = {
        "analysis": "pedicularis_g_v4_field_handoff_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_plants": n_plants,
        "n_rows": len(field_rows),
        "allocation_algorithm": allocation_receipt["allocation_algorithm"],
        "allocation_seed_sha256": allocation_receipt[
            "allocation_seed_sha256"
        ],
        "allocation_receipt_sha256": allocation_receipt_sha256,
        "allocation_identity_sha256": _identity_digest(allocation_rows),
        "v4_fieldnames": v4_fieldnames,
        "frozen_identity_rows": frozen_rows,
        "status": "G_V4_FIELD_SHEET_PREPARED_NOT_YET_MEASURED",
        "next_step": (
            "collect V4 timing/outcome fields without changing frozen identity "
            "columns; verify against this lock before candidate screening"
        ),
        "claim_ceiling": [
            "field_sheet_and_identity_lock_only",
            "no_field_outcomes_generated",
            "no_candidate_selected",
            "no_effect_or_selectivity_thresholds_applied",
        ],
    }
    return field_rows, lock


def _arm_from_v4_row(row: dict[str, str]) -> str:
    matches = [
        arm_id
        for arm_id, expected in ARM_EXPECTATIONS.items()
        if all(row[field] == value for field, value in expected.items())
    ]
    if len(matches) != 1:
        raise ValueError(
            "completed V4 row does not map to exactly one frozen first-tier arm"
        )
    return matches[0]


def verify(
    completed_rows: list[dict[str, str]],
    lock: dict,
    *,
    require_complete: bool = False,
) -> dict:
    if not completed_rows:
        raise ValueError("completed V4 field sheet is empty")

    expected_fieldnames = lock.get("v4_fieldnames")
    if not isinstance(expected_fieldnames, list):
        raise ValueError("lock lacks v4_fieldnames")
    missing = sorted(set(expected_fieldnames) - set(completed_rows[0]))
    if missing:
        raise ValueError(
            "completed V4 sheet lacks locked columns: " + ", ".join(missing)
        )

    reconstructed = []
    for row in completed_rows:
        arm_id = _arm_from_v4_row(row)
        reconstructed.append(
            {
                **{field: row[field] for field in V4_IDENTITY_FIELDS},
                "pilot_arm_id": arm_id,
            }
        )

    if len({row["flower_id"] for row in reconstructed}) != len(reconstructed):
        raise ValueError("completed V4 sheet contains duplicate flower_id rows")

    observed = sorted(
        reconstructed,
        key=lambda row: (
            row["population_id"],
            row["season_id"],
            row["plant_id"],
            row["pilot_arm_id"],
            row["flower_id"],
        ),
    )
    frozen = lock.get("frozen_identity_rows")
    if observed != frozen:
        raise ValueError(
            "completed V4 identity rows do not match the frozen allocation lock"
        )

    blank_cells: list[str] = []
    if require_complete:
        outcome_fields = [
            field
            for field in expected_fieldnames
            if field not in V4_IDENTITY_FIELDS
        ]
        for row in completed_rows:
            for field in outcome_fields:
                if not row.get(field, "").strip():
                    blank_cells.append(f"{row['flower_id']}:{field}")
        if blank_cells:
            preview = ", ".join(blank_cells[:10])
            suffix = " ..." if len(blank_cells) > 10 else ""
            raise ValueError(
                "completed V4 sheet still has blank outcome/timing cells: "
                + preview
                + suffix
            )

    return {
        "analysis": "pedicularis_g_v4_field_handoff_verify_v1",
        "population_id": lock["population_id"],
        "season_id": lock["season_id"],
        "n_rows": len(completed_rows),
        "identity_lock_match": True,
        "require_complete": require_complete,
        "all_locked_v4_cells_complete": require_complete,
        "ready_for_candidate_screen": require_complete,
        "allocation_identity_sha256": lock["allocation_identity_sha256"],
        "status": (
            "G_V4_IDENTITY_VERIFIED_COMPLETE_READY_FOR_CANDIDATE_SCREEN"
            if require_complete
            else "G_V4_IDENTITY_VERIFIED_PARTIAL_COLLECTION_ALLOWED"
        ),
        "claim_ceiling": [
            "identity_and_completion_check_only",
            "does_not_evaluate_method_validity",
            "does_not_select_candidate",
            "does_not_generate_confirmatory_G_receipt",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare and verify a locked V4 P. rex G field sheet from the "
            "randomized first-tier allocation manifest"
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prep = subparsers.add_parser("prepare")
    prep.add_argument("allocation_csv", type=Path)
    prep.add_argument("allocation_receipt_json", type=Path)
    prep.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    prep.add_argument("--field-sheet-out", type=Path, required=True)
    prep.add_argument("--lock-out", type=Path, required=True)

    check = subparsers.add_parser("verify")
    check.add_argument("completed_v4_csv", type=Path)
    check.add_argument("lock_json", type=Path)
    check.add_argument("--require-complete", action="store_true")
    check.add_argument("--output", type=Path)

    args = parser.parse_args()

    if args.command == "prepare":
        _, allocation_rows = _read_csv(args.allocation_csv)
        allocation_receipt_bytes = args.allocation_receipt_json.read_bytes()
        allocation_receipt = json.loads(
            allocation_receipt_bytes.decode("utf-8")
        )
        v4_fieldnames, _ = _read_csv(args.template)
        field_rows, lock = prepare(
            allocation_rows,
            allocation_receipt,
            v4_fieldnames,
            allocation_receipt_sha256=_sha256_bytes(
                allocation_receipt_bytes
            ),
        )
        _write_csv(args.field_sheet_out, v4_fieldnames, field_rows)
        args.lock_out.parent.mkdir(parents=True, exist_ok=True)
        args.lock_out.write_text(
            json.dumps(lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(lock, indent=2, sort_keys=True))
        return

    _, completed_rows = _read_csv(args.completed_v4_csv)
    lock = json.loads(args.lock_json.read_text(encoding="utf-8"))
    result = verify(
        completed_rows,
        lock,
        require_complete=args.require_complete,
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

from scripts import analyze_pedicularis_full_surface as surface
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256


ALLOCATION_SCHEMA = "PEDICULARIS_FULL_SURFACE_ALLOCATION_V1"
ALLOCATION_STATUS = "P2_FULL_SURFACE_ALLOCATED_NOT_YET_MEASURED"
LOCK_SCHEMA = "PEDICULARIS_FULL_SURFACE_FIELD_IDENTITY_LOCK_V1"

PROVENANCE_FIELDS = (
    "assigned_z_rank",
    "target_exsertion",
    "allocation_cell_id",
    "assignment_method",
)
FROZEN_FIELDS = (
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


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(OUTPUT_FIELDS))
        writer.writeheader()
        writer.writerows(rows)


def _receipt_sha256(receipt: dict) -> str:
    return _semantic_sha256(receipt)


def _normalize_frozen_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    missing = sorted(set(FROZEN_FIELDS) - set(rows[0]))
    if missing:
        raise ValueError(
            "P2 allocation/field rows lack frozen columns: "
            + ", ".join(missing)
        )

    seen_flowers: set[str] = set()
    normalized = []
    for row in rows:
        frozen = {field: row[field].strip() for field in FROZEN_FIELDS}
        if any(not value for value in frozen.values()):
            raise ValueError("frozen P2 identity/treatment fields cannot be blank")
        if frozen["flower_id"] in seen_flowers:
            raise ValueError("flower_id must be unique in the P2 field packet")
        seen_flowers.add(frozen["flower_id"])
        normalized.append(frozen)

    return sorted(
        normalized,
        key=lambda row: (
            row["population_id"],
            row["season_id"],
            row["plant_id"],
            row["flower_id"],
        ),
    )


def _validate_allocation(
    allocation_rows: list[dict[str, str]],
    allocation_receipt: dict,
) -> list[dict[str, str]]:
    if allocation_receipt.get("receipt_schema") != ALLOCATION_SCHEMA:
        raise ValueError("allocation receipt schema mismatch")
    if allocation_receipt.get("status") != ALLOCATION_STATUS:
        raise ValueError("allocation receipt is not in pre-field allocated state")

    normalized = _normalize_frozen_rows(allocation_rows)
    if len(normalized) != int(allocation_receipt.get("n_allocated_flowers", -1)):
        raise ValueError("allocation row count does not match receipt")

    canonical_allocation_rows = sorted(
        [
            {key: value.strip() for key, value in row.items()}
            for row in allocation_rows
        ],
        key=lambda row: (row["plant_id"], row["flower_id"]),
    )
    if _semantic_sha256(canonical_allocation_rows) != allocation_receipt.get(
        "allocation_identity_sha256"
    ):
        raise ValueError(
            "allocation CSV identity does not match allocation receipt digest"
        )

    populations = {row["population_id"] for row in normalized}
    seasons = {row["season_id"] for row in normalized}
    if populations != {allocation_receipt.get("population_id")}:
        raise ValueError("allocation population does not match receipt")
    if seasons != {allocation_receipt.get("season_id")}:
        raise ValueError("allocation season does not match receipt")

    cell_counts: dict[str, int] = {}
    for row in normalized:
        cell = row["allocation_cell_id"]
        cell_counts[cell] = cell_counts.get(cell, 0) + 1
    expected_counts = allocation_receipt.get("cell_counts")
    if cell_counts != expected_counts:
        raise ValueError("allocation cell counts do not match receipt")

    return normalized


def prepare(
    allocation_rows: list[dict[str, str]],
    allocation_receipt: dict,
) -> tuple[list[dict[str, str]], dict]:
    normalized = _validate_allocation(
        allocation_rows,
        allocation_receipt,
    )

    by_flower = {
        row["flower_id"]: row
        for row in allocation_rows
    }
    field_rows = []
    for frozen in normalized:
        source = by_flower[frozen["flower_id"]]
        row = {field: "" for field in OUTPUT_FIELDS}
        for field in (
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
        ):
            row[field] = source[field].strip()
        field_rows.append(row)

    lock = {
        "analysis": "pedicularis_full_surface_field_identity_lock_v1",
        "receipt_schema": LOCK_SCHEMA,
        "population_id": allocation_receipt["population_id"],
        "season_id": allocation_receipt["season_id"],
        "n_rows": len(normalized),
        "allocation_identity_sha256": allocation_receipt[
            "allocation_identity_sha256"
        ],
        "allocation_receipt_sha256": _receipt_sha256(allocation_receipt),
        "p0_level_plan_sha256": allocation_receipt.get(
            "p0_level_plan_sha256"
        ),
        "readiness_receipt_sha256": allocation_receipt.get(
            "readiness_receipt_sha256"
        ),
        "field_identity_sha256": _semantic_sha256(normalized),
        "frozen_fields": list(FROZEN_FIELDS),
        "expected_frozen_rows": normalized,
        "outcome_fields_prefilled": False,
        "status": "P2_FIELD_SHEET_PREPARED_IDENTITY_LOCKED",
        "claim_ceiling": [
            "field_identity_and_treatment_handoff_only",
            "no_outcome_values_generated",
            "no_flower_substitution_allowed",
            "no_treatment_drift_allowed",
            "does_not_validate_full_surface",
        ],
    }
    return field_rows, lock


def verify(
    field_rows: list[dict[str, str]],
    lock: dict,
    *,
    require_complete: bool,
) -> dict:
    if lock.get("receipt_schema") != LOCK_SCHEMA:
        raise ValueError("P2 field identity lock schema mismatch")
    if lock.get("status") != "P2_FIELD_SHEET_PREPARED_IDENTITY_LOCKED":
        raise ValueError("P2 field identity lock is not in prepared state")

    normalized = _normalize_frozen_rows(field_rows)
    expected = lock.get("expected_frozen_rows")
    if not isinstance(expected, list):
        raise ValueError("P2 field identity lock lacks expected frozen rows")
    if len(normalized) != int(lock.get("n_rows", -1)):
        raise ValueError("P2 field sheet row count drifted from identity lock")
    if normalized != expected:
        raise ValueError(
            "P2 field identity/treatment rows drifted from the locked allocation"
        )
    if _semantic_sha256(normalized) != lock.get("field_identity_sha256"):
        raise ValueError("P2 field identity digest does not match lock")

    missing_raw = sorted(set(surface.RAW_FIELDS) - set(field_rows[0]))
    if missing_raw:
        raise ValueError(
            "P2 field sheet lacks canonical raw columns: "
            + ", ".join(missing_raw)
        )

    blank_cells = []
    if require_complete:
        for row_index, row in enumerate(field_rows, start=2):
            for field in surface.RAW_FIELDS:
                if row.get(field, "").strip() == "":
                    blank_cells.append(
                        {"csv_line": row_index, "field": field}
                    )
        if blank_cells:
            first = blank_cells[0]
            raise ValueError(
                "P2 field sheet is incomplete; first blank canonical cell is "
                f"line {first['csv_line']} field {first['field']}"
            )

    surface_digest = None
    if require_complete:
        surface_digest = surface.surface_data_sha256(field_rows)

    return {
        "analysis": "pedicularis_full_surface_field_verification_v1",
        "receipt_schema": "PEDICULARIS_FULL_SURFACE_FIELD_VERIFICATION_V1",
        "population_id": lock["population_id"],
        "season_id": lock["season_id"],
        "n_rows": len(normalized),
        "allocation_identity_sha256": lock["allocation_identity_sha256"],
        "allocation_receipt_sha256": lock["allocation_receipt_sha256"],
        "p0_level_plan_sha256": lock.get("p0_level_plan_sha256"),
        "readiness_receipt_sha256": lock.get(
            "readiness_receipt_sha256"
        ),
        "field_identity_sha256": lock["field_identity_sha256"],
        "identity_and_treatment_match": True,
        "canonical_outcomes_complete": require_complete,
        "surface_data_sha256": surface_digest,
        "status": (
            "P2_FULL_SURFACE_FIELD_PACKET_VERIFIED_COMPLETE"
            if require_complete
            else "P2_FULL_SURFACE_FIELD_IDENTITY_VERIFIED"
        ),
        "claim_ceiling": [
            "execution_integrity_only",
            "does_not_establish_causal_compromise",
            "does_not_assign_W0_W5",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Prepare or verify a powered P. rex full-surface field sheet while "
            "locking flower identity, z/P/G treatment and method assignment"
        )
    )
    sub = parser.add_subparsers(dest="command", required=True)

    prep = sub.add_parser("prepare")
    prep.add_argument("allocation_csv", type=Path)
    prep.add_argument("allocation_receipt_json", type=Path)
    prep.add_argument("--field-sheet-out", type=Path, required=True)
    prep.add_argument("--identity-lock-out", type=Path, required=True)

    check = sub.add_parser("verify")
    check.add_argument("field_sheet_csv", type=Path)
    check.add_argument("identity_lock_json", type=Path)
    check.add_argument("--require-complete", action="store_true")
    check.add_argument("--receipt-out", type=Path)

    args = parser.parse_args()

    if args.command == "prepare":
        rows, lock = prepare(
            _read_csv(args.allocation_csv),
            _load_json(args.allocation_receipt_json),
        )
        _write_csv(args.field_sheet_out, rows)
        args.identity_lock_out.parent.mkdir(parents=True, exist_ok=True)
        args.identity_lock_out.write_text(
            json.dumps(lock, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(lock, indent=2, sort_keys=True))
        return

    receipt = verify(
        _read_csv(args.field_sheet_csv),
        _load_json(args.identity_lock_json),
        require_complete=args.require_complete,
    )
    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        args.receipt_out.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

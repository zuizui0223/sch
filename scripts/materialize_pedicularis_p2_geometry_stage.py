from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.build_pedicularis_p2_geometry_pilot import (
    OUTPUT_FIELDS,
    PROVENANCE_FIELDS,
    RECEIPT_SCHEMA,
)


ALLOCATION_STATUS = "P2_GEOMETRY_PILOT_ALLOCATED_NOT_YET_MEASURED"
STAGE_SCOPE = "CUMULATIVE_PRECISION_LOOK"
FROZEN_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "assigned_z_level",
    "pollination_treatment",
    "predator_treatment",
    "exclusion_method",
    *PROVENANCE_FIELDS,
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


def _frozen(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    missing = sorted(set(FROZEN_FIELDS) - set(rows[0]))
    if missing:
        raise ValueError(
            "geometry field sheet lacks frozen fields: " + ", ".join(missing)
        )
    normalized = [
        {field: row[field].strip() for field in FROZEN_FIELDS}
        for row in rows
    ]
    return sorted(
        normalized,
        key=lambda row: (row["plant_id"], row["flower_id"]),
    )


def build(
    full_rows: list[dict[str, str]],
    allocation_receipt: dict,
    stage_n: int,
) -> tuple[list[dict[str, str]], dict]:
    if allocation_receipt.get("receipt_schema") != RECEIPT_SCHEMA:
        raise ValueError("geometry allocation receipt schema mismatch")
    if allocation_receipt.get("status") != ALLOCATION_STATUS:
        raise ValueError("geometry allocation receipt is not in allocated state")

    candidates = allocation_receipt.get("candidate_cumulative_plants")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError(
            "geometry allocation receipt lacks candidate_cumulative_plants"
        )
    candidates = [int(value) for value in candidates]
    if stage_n not in candidates:
        raise ValueError(
            "stage_n must be one of the prospectively frozen cumulative looks"
        )

    expected_full = allocation_receipt.get("expected_frozen_rows")
    if not isinstance(expected_full, list):
        raise ValueError("geometry allocation receipt lacks expected_frozen_rows")
    if _frozen(full_rows) != expected_full:
        raise ValueError(
            "maximum geometry field sheet identity drifted from frozen allocation"
        )

    stage_rows = [
        dict(row)
        for row in full_rows
        if int(row["plant_accrual_rank"]) <= stage_n
    ]
    if not stage_rows:
        raise ValueError("cumulative geometry stage has no rows")

    plant_ids = {row["plant_id"] for row in stage_rows}
    if len(plant_ids) != stage_n:
        raise ValueError(
            "cumulative geometry stage does not contain exactly stage_n plants"
        )

    expected_stage = [
        row
        for row in expected_full
        if int(row["plant_accrual_rank"]) <= stage_n
    ]
    observed_stage = _frozen(stage_rows)
    if observed_stage != expected_stage:
        raise ValueError(
            "cumulative geometry stage identity does not match allocation prefix"
        )

    cell_counts = Counter(
        row["allocation_cell_id"]
        for row in stage_rows
    )
    n_cells = int(allocation_receipt["n_surface_cells"])
    if len(cell_counts) != n_cells:
        raise ValueError(
            "cumulative geometry stage does not cover every surface cell"
        )
    expected_rep = (
        stage_n * int(allocation_receipt["flowers_per_plant"]) // n_cells
    )
    if set(cell_counts.values()) != {expected_rep}:
        raise ValueError(
            "cumulative geometry stage is not exactly balanced across cells"
        )

    config_sha = allocation_receipt.get("config_sha256")
    parent_sha = _semantic_sha256(allocation_receipt)
    stage_receipt = {
        "analysis": "pedicularis_p2_geometry_pilot_stage_allocation_v1",
        "receipt_schema": RECEIPT_SCHEMA,
        "allocation_scope": STAGE_SCOPE,
        "parent_allocation_sha256": parent_sha,
        "population_id": allocation_receipt["population_id"],
        "season_id": allocation_receipt["season_id"],
        "candidate_cumulative_plants": candidates,
        "current_precision_look_n": stage_n,
        "n_plants": stage_n,
        "flowers_per_plant": int(allocation_receipt["flowers_per_plant"]),
        "n_surface_cells": n_cells,
        "replicates_per_cell": expected_rep,
        "n_allocated_flowers": len(stage_rows),
        "exact_cell_balance": True,
        "cell_counts": dict(sorted(cell_counts.items())),
        "z_levels": allocation_receipt["z_levels"],
        "allocation_strategy": allocation_receipt["allocation_strategy"],
        "allocation_algorithm": allocation_receipt["allocation_algorithm"],
        "allocation_seed_sha256": allocation_receipt["allocation_seed_sha256"],
        "config_sha256": config_sha,
        "readiness_receipt_sha256": allocation_receipt.get(
            "readiness_receipt_sha256"
        ),
        "readiness_status": allocation_receipt.get("readiness_status"),
        "validated_execution": allocation_receipt.get("validated_execution"),
        "precision_gate": allocation_receipt["precision_gate"],
        "precision_gate_frozen_before_outcomes": True,
        "frozen_identity_sha256": _semantic_sha256(observed_stage),
        "expected_frozen_rows": observed_stage,
        "pilot_role": allocation_receipt["pilot_role"],
        "confirmatory_eligible": False,
        "threshold_basis_eligible": False,
        "status": ALLOCATION_STATUS,
        "claim_ceiling": [
            "cumulative_precision_look_only",
            "stage_n_predeclared_before_geometry_outcomes",
            "exact_prefix_of_maximum_randomized_geometry_allocation",
            "inherits_positive_randomized_P0_P1_G_readiness_from_maximum_allocation",
            "does_not_change_any_prior_treatment_assignment",
            "does_not_authorize_collection_beyond_next_registered_stage",
        ],
    }
    return stage_rows, stage_receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Materialize one prospectively frozen cumulative precision look "
            "from the maximum randomized P. rex geometry-pilot allocation"
        )
    )
    parser.add_argument("maximum_field_sheet_csv", type=Path)
    parser.add_argument("maximum_allocation_receipt_json", type=Path)
    parser.add_argument("--stage-n", type=int, required=True)
    parser.add_argument("--stage-sheet-out", type=Path, required=True)
    parser.add_argument("--stage-receipt-out", type=Path, required=True)
    args = parser.parse_args()

    rows, receipt = build(
        _read_csv(args.maximum_field_sheet_csv),
        _load_json(args.maximum_allocation_receipt_json),
        args.stage_n,
    )
    _write_csv(args.stage_sheet_out, rows)
    args.stage_receipt_out.parent.mkdir(parents=True, exist_ok=True)
    args.stage_receipt_out.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts import audit_pedicularis_w1_w2_power_basis as basis
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256


GEOMETRY_SUMMARY_SCHEMA = "PEDICULARIS_P2_GEOMETRY_PILOT_SUMMARY_V1"
GEOMETRY_READY_STATUS = "PEDICULARIS_P2_GEOMETRY_PILOT_POWER_BASIS_READY"
PROMOTED_STATUS = "DIRECT_SAME_CONTEXT_READY"
PROMOTED_GROUPS = {
    "FITNESS_VARIANCE",
    "FITNESS_GEOMETRY",
    "POLLEN_VARIANCE",
    "POLLEN_GEOMETRY",
    "INITIAL_SEED_VARIANCE",
    "INITIAL_SEED_GEOMETRY",
}


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def materialize(
    rows: list[dict[str, str]],
    geometry_summary: dict,
) -> tuple[list[dict[str, str]], dict]:
    if geometry_summary.get("receipt_schema") != GEOMETRY_SUMMARY_SCHEMA:
        raise ValueError("geometry-pilot summary schema mismatch")
    if geometry_summary.get("status") != GEOMETRY_READY_STATUS:
        raise ValueError("geometry-pilot summary is not ready for power basis")
    if geometry_summary.get("geometry_and_variance_basis_complete") is not True:
        raise ValueError("geometry-pilot basis is incomplete")
    if geometry_summary.get("n_power_basis_paths_resolved") != 18:
        raise ValueError("geometry pilot must resolve exactly 18 power-basis paths")

    values = geometry_summary.get("resolved_power_basis_values")
    if not isinstance(values, dict):
        raise ValueError("geometry-pilot summary lacks resolved power-basis values")

    expected_paths = {
        row["config_path"]
        for row in rows
        if row["field_group"] in PROMOTED_GROUPS
    }
    if len(expected_paths) != 18:
        raise ValueError(
            "canonical basis ledger must contain exactly 18 geometry/variance paths"
        )
    if set(values) != expected_paths:
        missing = sorted(expected_paths - set(values))
        extra = sorted(set(values) - expected_paths)
        raise ValueError(
            "geometry-pilot resolved paths do not match canonical basis ledger: "
            f"missing={missing}, extra={extra}"
        )

    summary_digest = _semantic_sha256(geometry_summary)
    updated = []
    promoted = []
    for row in rows:
        out = dict(row)
        if row["config_path"] in expected_paths:
            out["current_source"] = (
                "same-context separate nonconfirmatory P2 geometry pilot "
                + summary_digest
            )
            out["current_status"] = PROMOTED_STATUS
            out["direct_registered_n_eligible"] = "YES"
            out["notes"] = (
                "Resolved from independent POWER_GEOMETRY_PILOT rows excluded "
                "from confirmatory P2 inference; value stored in geometry summary."
            )
            promoted.append(row["config_path"])
        updated.append(out)

    audit = basis.build(updated)
    return updated, {
        "analysis": "pedicularis_w1_w2_basis_materialization_from_geometry_pilot_v1",
        "population_id": geometry_summary["population_id"],
        "season_id": geometry_summary["season_id"],
        "geometry_summary_sha256": summary_digest,
        "n_paths_promoted": len(promoted),
        "promoted_config_paths": sorted(promoted),
        "basis_audit_after_materialization": audit,
        "remaining_blockers": audit["blocking_config_paths"],
        "status": (
            "PEDICULARIS_W1_W2_GEOMETRY_BASIS_MATERIALIZED"
            if len(promoted) == 18
            else "PEDICULARIS_W1_W2_GEOMETRY_BASIS_INCOMPLETE"
        ),
        "claim_ceiling": [
            "power_basis_materialization_only",
            "does_not_freeze_remaining_P0_or_primary_threshold_inputs",
            "does_not_register_final_n_until_all_blockers_are_zero",
            "does_not_use_geometry_pilot_rows_in_confirmatory_inference",
        ],
    }


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Promote only the 18 same-estimand geometry/variance W1/W2 power "
            "basis rows from a separate nonconfirmatory P2 geometry pilot"
        )
    )
    parser.add_argument("geometry_summary_json", type=Path)
    parser.add_argument("--ledger", type=Path, default=basis.DEFAULT_LEDGER)
    parser.add_argument("--ledger-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    updated, receipt = materialize(
        basis._read(args.ledger),
        _load(args.geometry_summary_json),
    )
    _write_csv(args.ledger_out, updated)
    if args.receipt_out:
        args.receipt_out.parent.mkdir(parents=True, exist_ok=True)
        args.receipt_out.write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

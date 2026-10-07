from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from scripts import audit_pedicularis_w1_w2_power_basis as basis
from scripts import evaluate_pedicularis_stage_p0 as p0
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.freeze_pedicularis_full_surface_thresholds import (
    FREEZE_SCHEMA as SURFACE_FREEZE_SCHEMA,
    RECEIPT_STATUS as SURFACE_FREEZE_STATUS,
)


P0_SCHEMA = "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1"
P0_STATUS = "PEDICULARIS_Z_MANIPULATION_VALIDATED"
PROMOTED = {
    "generating_model.z_levels": "DIRECT_SAME_CONTEXT_READY",
    "generating_model.realized_z_sd": "DIRECT_SAME_CONTEXT_READY",
    "production_surface_config.sch_surface.*": "REGISTERED_THRESHOLD_READY",
}


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _read_p0(path: Path) -> list[dict[str, str]]:
    return p0._read_csv(path)


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _p0_power_values(
    rows: list[dict[str, str]],
    receipt: dict,
) -> tuple[list[float], float, list[dict[str, object]]]:
    if receipt.get("receipt_schema_version") != P0_SCHEMA:
        raise ValueError("P0 receipt schema mismatch")
    if receipt.get("status") != P0_STATUS:
        raise ValueError("P0 manipulation receipt is not positive")
    freeze = receipt.get("config_freeze")
    if (
        not isinstance(freeze, dict)
        or freeze.get("schema") != "SCH_PEDICULARIS_THRESHOLD_FREEZE_V1"
        or freeze.get("status") != "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN"
        or freeze.get("lane") != "P0"
        or freeze.get("population_id") != receipt.get("population_id")
        or freeze.get("season_id") != receipt.get("season_id")
    ):
        raise ValueError("P0 receipt lacks positive same-context threshold-freeze provenance")
    if receipt.get("p0_data_sha256") != p0.p0_data_sha256(rows):
        raise ValueError("P0 raw rows do not match the validated P0 data fingerprint")

    allocation = receipt.get("field_allocation_verification")
    if not isinstance(allocation, dict):
        raise ValueError("P0 receipt lacks randomized allocation verification")
    if allocation.get("receipt_schema") != "PEDICULARIS_P0_RANDOMIZED_ALLOCATION_V1":
        raise ValueError("P0 receipt is not grounded in the randomized allocation")
    if allocation.get("identity_z_assignment_match") is not True:
        raise ValueError("P0 randomized z assignment is not verified")
    if allocation.get("physical_manipulation_setting_match") is not True:
        raise ValueError("P0 physical manipulation setting identity is not verified")

    groups = p0._group_by_rank(rows)
    receipt_means = receipt.get("realized_exsertion", {}).get("mean_by_rank")
    settings = receipt.get("z_manipulation_settings")
    if not isinstance(receipt_means, dict):
        raise ValueError("P0 receipt lacks realized-exsertion means by rank")
    if not isinstance(settings, list) or len(settings) != len(groups):
        raise ValueError("P0 receipt lacks validated manipulation settings")
    expected_settings = [
        {
            "assigned_z_level": groups[rank][0]["assigned_z_level"],
            "assigned_z_rank": rank,
            "manipulation_setting_id": groups[rank][0][
                "manipulation_setting_id"
            ],
        }
        for rank in groups
    ]
    if settings != expected_settings:
        raise ValueError(
            "P0 receipt manipulation-setting mapping does not match raw rows"
        )

    nominal = []
    setting_rows = []
    residual_ss = 0.0
    n = 0

    for rank, group in groups.items():
        key = str(rank)
        if key not in receipt_means:
            raise ValueError(f"P0 receipt lacks realized mean for rank {rank}")
        observed_mean = sum(
            float(row["realized_exsertion"]) for row in group
        ) / len(group)
        receipt_mean = float(receipt_means[key])
        if not math.isclose(observed_mean, receipt_mean, rel_tol=0, abs_tol=1e-12):
            raise ValueError("P0 receipt mean-by-rank does not match raw rows")

        labels = {row["assigned_z_level"] for row in group}
        setting_ids = {row["manipulation_setting_id"] for row in group}
        if len(labels) != 1 or len(setting_ids) != 1:
            raise ValueError("P0 rank identity is not unique")

        nominal.append(receipt_mean)
        setting_rows.append(
            {
                "assigned_z_rank": rank,
                "assigned_z_level": next(iter(labels)),
                "manipulation_setting_id": next(iter(setting_ids)),
                "nominal_realized_z": receipt_mean,
            }
        )
        for row in group:
            residual = float(row["realized_exsertion"]) - receipt_mean
            residual_ss += residual * residual
            n += 1

    if len(nominal) < 5:
        raise ValueError("registered z grid requires at least five validated levels")
    if any(right <= left for left, right in zip(nominal, nominal[1:])):
        raise ValueError("validated P0 nominal realized-z grid must be strictly ordered")

    df = n - len(groups)
    if df <= 0:
        raise ValueError("P0 within-level realized-z SD requires residual degrees of freedom")
    realized_z_sd = math.sqrt(residual_ss / df)
    if not math.isfinite(realized_z_sd) or realized_z_sd < 0:
        raise ValueError("invalid P0 within-level realized-z SD")

    return nominal, realized_z_sd, setting_rows


def materialize(
    ledger_rows: list[dict[str, str]],
    p0_rows: list[dict[str, str]],
    p0_receipt: dict,
    full_surface_config: dict,
    surface_freeze_receipt: dict,
) -> tuple[list[dict[str, str]], dict]:
    population = p0_receipt.get("population_id")
    season = p0_receipt.get("season_id")
    if not isinstance(population, str) or not population:
        raise ValueError("P0 receipt lacks population_id")
    if not isinstance(season, str) or not season:
        raise ValueError("P0 receipt lacks season_id")

    row_contexts = {
        (row["population_id"], row["season_id"])
        for row in p0_rows
    }
    if row_contexts != {(population, season)}:
        raise ValueError("P0 raw rows do not match P0 receipt context")

    if surface_freeze_receipt.get("receipt_schema") != SURFACE_FREEZE_SCHEMA:
        raise ValueError("full-surface threshold-freeze receipt schema mismatch")
    if surface_freeze_receipt.get("status") != SURFACE_FREEZE_STATUS:
        raise ValueError("full-surface threshold freeze is not validated")
    if surface_freeze_receipt.get("population_id") != population:
        raise ValueError("full-surface threshold freeze population does not match P0")
    if surface_freeze_receipt.get("season_id") != season:
        raise ValueError("full-surface threshold freeze season does not match P0")
    if surface_freeze_receipt.get("frozen_before_geometry_outcomes") is not True:
        raise ValueError("full-surface thresholds were not frozen before geometry outcomes")
    if surface_freeze_receipt.get("frozen_before_full_surface_outcomes") is not True:
        raise ValueError("full-surface thresholds were not frozen before P2 outcomes")
    if surface_freeze_receipt.get("full_surface_config_sha256") != _semantic_sha256(
        full_surface_config
    ):
        raise ValueError(
            "full-surface threshold freeze is not bound to the supplied config"
        )

    sch_surface = full_surface_config.get("sch_surface")
    if not isinstance(sch_surface, dict):
        raise ValueError("full-surface config lacks sch_surface")
    if surface_freeze_receipt.get("sch_surface_sha256") != _semantic_sha256(
        surface_freeze_receipt.get("sch_surface")
    ):
        raise ValueError("full-surface threshold receipt sch_surface digest mismatch")
    if surface_freeze_receipt.get("sch_surface") != sch_surface:
        raise ValueError(
            "full-surface config sch_surface differs from the frozen threshold receipt"
        )

    z_levels, realized_z_sd, setting_rows = _p0_power_values(
        p0_rows,
        p0_receipt,
    )

    by_path = {row["config_path"]: row for row in ledger_rows}
    if not set(PROMOTED).issubset(by_path):
        missing = sorted(set(PROMOTED) - set(by_path))
        raise ValueError("power basis ledger lacks final P0/F0 paths: " + ", ".join(missing))

    p0_digest = _semantic_sha256(p0_receipt)
    freeze_digest = _semantic_sha256(surface_freeze_receipt)

    updated = []
    for row in ledger_rows:
        out = dict(row)
        path = row["config_path"]
        if path == "generating_model.z_levels":
            out["current_source"] = (
                "same-context positive randomized P0 receipt "
                + p0_digest
                + " validated rank means"
            )
            out["current_status"] = PROMOTED[path]
            out["direct_registered_n_eligible"] = "YES"
            out["notes"] = (
                "Nominal power z grid is the ordered realized-exsertion mean of each "
                "validated physical P0 manipulation setting."
            )
        elif path == "generating_model.realized_z_sd":
            out["current_source"] = (
                "same-context positive randomized P0 raw data "
                + p0_receipt["p0_data_sha256"]
            )
            out["current_status"] = PROMOTED[path]
            out["direct_registered_n_eligible"] = "YES"
            out["notes"] = (
                "Pooled within-validated-z-level residual SD of realized exsertion; "
                "computed before P2 outcomes."
            )
        elif path == "production_surface_config.sch_surface.*":
            out["current_source"] = (
                "prospective full-surface threshold freeze " + freeze_digest
            )
            out["current_status"] = PROMOTED[path]
            out["direct_registered_n_eligible"] = "YES"
            out["notes"] = (
                "Exact sch_surface decision thresholds/config were frozen before "
                "geometry and confirmatory P2 outcomes."
            )
        updated.append(out)

    audit = basis.build(updated)

    return updated, {
        "analysis": "pedicularis_w1_w2_final_p0_f0_basis_materialization_v1",
        "population_id": population,
        "season_id": season,
        "p0_receipt_sha256": p0_digest,
        "p0_data_sha256": p0_receipt["p0_data_sha256"],
        "surface_threshold_freeze_sha256": freeze_digest,
        "full_surface_config_sha256": _semantic_sha256(full_surface_config),
        "resolved_power_inputs": {
            "generating_model.z_levels": z_levels,
            "generating_model.realized_z_sd": realized_z_sd,
            "production_surface_config.sch_surface": sch_surface,
        },
        "validated_z_setting_mapping": setting_rows,
        "n_paths_promoted": 3,
        "promoted_config_paths": sorted(PROMOTED),
        "basis_audit_after_materialization": audit,
        "remaining_blockers": audit["blocking_config_paths"],
        "registered_single_scenario_n_basis_ready": audit[
            "registered_single_scenario_n_basis_ready"
        ],
        "status": (
            "PEDICULARIS_W1_W2_FINAL_P0_F0_BASIS_MATERIALIZED"
            if audit["registered_single_scenario_n_basis_ready"]
            else "PEDICULARIS_W1_W2_FINAL_P0_F0_BASIS_PARTIAL"
        ),
        "claim_ceiling": [
            "power_basis_materialization_only",
            "z_grid_and_z_error_come_from_positive_same_context_randomized_P0",
            "surface_thresholds_frozen_before_geometry_and_P2_outcomes",
            "does_not_create_geometry_or_variance_basis",
            "registered_n_requires_all_other_basis_rows_already_ready",
            "does_not_generate_biological_evidence",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Materialize the final three P. rex W1/W2 power-basis blockers "
            "from validated P0 realized z plus a prospective full-surface threshold freeze"
        )
    )
    parser.add_argument("completed_p0_csv", type=Path)
    parser.add_argument("p0_receipt_json", type=Path)
    parser.add_argument("full_surface_config_json", type=Path)
    parser.add_argument("surface_threshold_freeze_receipt_json", type=Path)
    parser.add_argument("--ledger", type=Path, default=basis.DEFAULT_LEDGER)
    parser.add_argument("--ledger-out", type=Path, required=True)
    parser.add_argument("--receipt-out", type=Path)
    args = parser.parse_args()

    updated, receipt = materialize(
        basis._read(args.ledger),
        _read_p0(args.completed_p0_csv),
        _load(args.p0_receipt_json),
        _load(args.full_surface_config_json),
        _load(args.surface_threshold_freeze_receipt_json),
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

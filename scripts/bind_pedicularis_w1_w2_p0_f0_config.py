from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256


POWER_SCHEMA = "PEDICULARIS_W1_W2_POWER_CONFIG_V1"
POWER_STATUS = "PEDICULARIS_W1_W2_POWER_INPUTS_PROSPECTIVELY_FROZEN"
BASIS_ANALYSIS = "pedicularis_w1_w2_power_basis_audit_v1"
BASIS_READY_STATUS = "PEDICULARIS_W1_W2_POWER_BASIS_READY_FOR_REGISTERED_N"
MATERIALIZATION_ANALYSIS = "pedicularis_w1_w2_final_p0_f0_basis_materialization_v1"
MATERIALIZATION_STATUS = "PEDICULARIS_W1_W2_FINAL_P0_F0_BASIS_MATERIALIZED"
FREEZE_SCHEMA = "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_V1"
FREEZE_STATUS = "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_VALIDATED"
BINDING_SCHEMA = "PEDICULARIS_W1_W2_P0_F0_CONFIG_BINDING_V1"
BINDING_STATUS = "PEDICULARIS_W1_W2_P0_F0_CONFIG_EXACTLY_BOUND"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _normalize_numeric(value: object, label: str) -> object:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        out = float(value)
        if not math.isfinite(out):
            raise ValueError(f"{label} must be finite")
        return out
    if isinstance(value, list):
        return [
            _normalize_numeric(item, f"{label}[]")
            for item in value
        ]
    if isinstance(value, dict):
        return {
            key: _normalize_numeric(val, f"{label}.{key}")
            for key, val in sorted(value.items())
        }
    raise ValueError(f"{label} must contain only numeric/list/dict values")


def build(
    power_config: dict,
    materialization_receipt: dict,
    basis_receipt: dict,
    surface_threshold_freeze: dict,
) -> dict:
    if power_config.get("schema") != POWER_SCHEMA:
        raise ValueError("power config schema mismatch")
    if power_config.get("status") != POWER_STATUS:
        raise ValueError("P0/F0 binding requires prospectively frozen power config")

    provenance = power_config.get("planning_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("power config lacks planning_provenance")
    population = provenance.get("population_id")
    season = provenance.get("season_id")

    if materialization_receipt.get("analysis") != MATERIALIZATION_ANALYSIS:
        raise ValueError("P0/F0 materialization receipt analysis mismatch")
    if materialization_receipt.get("status") != MATERIALIZATION_STATUS:
        raise ValueError("P0/F0 materialization receipt is not ready")
    if materialization_receipt.get("remaining_blockers") != []:
        raise ValueError("P0/F0 materialization still reports blockers")
    if materialization_receipt.get(
        "registered_single_scenario_n_basis_ready"
    ) is not True:
        raise ValueError("P0/F0 materialization does not authorize registered basis")
    if materialization_receipt.get("population_id") != population:
        raise ValueError("P0/F0 materialization population does not match power config")
    if materialization_receipt.get("season_id") != season:
        raise ValueError("P0/F0 materialization season does not match power config")

    if basis_receipt.get("analysis") != BASIS_ANALYSIS:
        raise ValueError("basis receipt analysis mismatch")
    if basis_receipt.get("registered_power_status") != BASIS_READY_STATUS:
        raise ValueError("basis receipt is not ready for registered n")
    if basis_receipt.get("registered_single_scenario_n_basis_ready") is not True:
        raise ValueError("basis receipt does not authorize registered n")
    if int(basis_receipt.get("n_blocking_rows", -1)) != 0:
        raise ValueError("basis receipt still contains blockers")

    embedded_basis = materialization_receipt.get("basis_audit_after_materialization")
    if embedded_basis != basis_receipt:
        raise ValueError(
            "basis receipt is not the exact post-materialization audit"
        )

    if surface_threshold_freeze.get("receipt_schema") != FREEZE_SCHEMA:
        raise ValueError("surface threshold freeze schema mismatch")
    if surface_threshold_freeze.get("status") != FREEZE_STATUS:
        raise ValueError("surface threshold freeze is not validated")
    if surface_threshold_freeze.get("population_id") != population:
        raise ValueError("surface threshold freeze population mismatch")
    if surface_threshold_freeze.get("season_id") != season:
        raise ValueError("surface threshold freeze season mismatch")
    if materialization_receipt.get(
        "surface_threshold_freeze_sha256"
    ) != _semantic_sha256(surface_threshold_freeze):
        raise ValueError(
            "P0/F0 materialization is not bound to this threshold freeze receipt"
        )

    resolved = materialization_receipt.get("resolved_power_inputs")
    if not isinstance(resolved, dict):
        raise ValueError("P0/F0 materialization lacks resolved power inputs")

    generating = power_config.get("generating_model")
    production = power_config.get("production_surface_config")
    if not isinstance(generating, dict) or not isinstance(production, dict):
        raise ValueError("power config lacks generating/production config")

    checks = {
        "generating_model.z_levels": (
            _normalize_numeric(
                generating.get("z_levels"),
                "power_config.generating_model.z_levels",
            )
            == _normalize_numeric(
                resolved.get("generating_model.z_levels"),
                "materialized.generating_model.z_levels",
            )
        ),
        "generating_model.realized_z_sd": (
            _normalize_numeric(
                generating.get("realized_z_sd"),
                "power_config.generating_model.realized_z_sd",
            )
            == _normalize_numeric(
                resolved.get("generating_model.realized_z_sd"),
                "materialized.generating_model.realized_z_sd",
            )
        ),
        "production_surface_config.sch_surface": (
            _normalize_numeric(
                production.get("sch_surface"),
                "power_config.production_surface_config.sch_surface",
            )
            == _normalize_numeric(
                resolved.get("production_surface_config.sch_surface"),
                "materialized.production_surface_config.sch_surface",
            )
        ),
        "production_surface_config.system_checks": (
            _normalize_numeric(
                production.get("system_checks"),
                "power_config.production_surface_config.system_checks",
            )
            == _normalize_numeric(
                surface_threshold_freeze.get("system_checks"),
                "surface_threshold_freeze.system_checks",
            )
        ),
    }
    failed = [path for path, passed in checks.items() if not passed]
    if failed:
        raise ValueError(
            "power config drifts from the resolved P0/F0 basis: "
            + ", ".join(failed)
        )

    analysis_config = {
        "sch_surface": production["sch_surface"],
        "system_checks": production["system_checks"],
    }
    analysis_config_sha = _semantic_sha256(analysis_config)
    if surface_threshold_freeze.get("analysis_config_sha256") != analysis_config_sha:
        raise ValueError(
            "power production surface config does not match the threshold-freeze analysis config"
        )

    return {
        "analysis": "pedicularis_w1_w2_p0_f0_config_binding_v1",
        "receipt_schema": BINDING_SCHEMA,
        "population_id": population,
        "season_id": season,
        "path_checks": checks,
        "all_final_three_paths_match": True,
        "analysis_config_sha256": analysis_config_sha,
        "surface_threshold_freeze_sha256": _semantic_sha256(
            surface_threshold_freeze
        ),
        "p0_f0_materialization_sha256": _semantic_sha256(
            materialization_receipt
        ),
        "power_basis_receipt_sha256": _semantic_sha256(basis_receipt),
        "power_config_sha256": _semantic_sha256(power_config),
        "status": BINDING_STATUS,
        "claim_ceiling": [
            "input_provenance_binding_only",
            "binds_final_three_power_basis_inputs_to_exact_power_config",
            "binds_analysis_thresholds_to_pregeometry_freeze",
            "does_not_register_n_by_itself",
            "does_not_generate_biological_evidence",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Bind the final P. rex W1/W2 power config to the exact validated "
            "P0 z grid/error and prospectively frozen full-surface thresholds"
        )
    )
    parser.add_argument("power_config_json", type=Path)
    parser.add_argument("p0_f0_materialization_receipt_json", type=Path)
    parser.add_argument("zero_blocker_basis_receipt_json", type=Path)
    parser.add_argument("surface_threshold_freeze_receipt_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        _load(args.power_config_json),
        _load(args.p0_f0_materialization_receipt_json),
        _load(args.zero_blocker_basis_receipt_json),
        _load(args.surface_threshold_freeze_receipt_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

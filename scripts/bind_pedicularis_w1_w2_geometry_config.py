from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


GEOMETRY_SUMMARY_SCHEMA = "PEDICULARIS_P2_GEOMETRY_PILOT_SUMMARY_V1"
GEOMETRY_POINT_READY_STATUS = (
    "PEDICULARIS_P2_GEOMETRY_PILOT_POINT_ESTIMATES_READY_NOT_YET_PRECISION_QUALIFIED"
)
PRECISION_SCHEMA = "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_V1"
PRECISION_READY_STATUS = "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_READY_FOR_BASIS"
BASIS_ANALYSIS = "pedicularis_w1_w2_power_basis_audit_v1"
BASIS_READY_STATUS = "PEDICULARIS_W1_W2_POWER_BASIS_READY_FOR_REGISTERED_N"
POWER_SCHEMA = "PEDICULARIS_W1_W2_POWER_CONFIG_V1"
POWER_FROZEN_STATUS = "PEDICULARIS_W1_W2_POWER_INPUTS_PROSPECTIVELY_FROZEN"
BINDING_SCHEMA = "PEDICULARIS_W1_W2_GEOMETRY_CONFIG_BINDING_V2"
BINDING_STATUS = "PEDICULARIS_W1_W2_GEOMETRY_CONFIG_BINDING_READY"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _semantic_sha256(payload: object) -> str:
    text = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _resolve_path(payload: dict, path: str) -> object:
    current: object = payload
    for token in path.split("."):
        if not isinstance(current, dict) or token not in current:
            raise ValueError(f"power config lacks geometry basis path: {path}")
        current = current[token]
    return current


def _normalize_numeric(value: object, label: str) -> object:
    if isinstance(value, bool):
        raise ValueError(f"{label} must not use booleans as numeric values")
    if isinstance(value, (int, float)):
        out = float(value)
        if not math.isfinite(out):
            raise ValueError(f"{label} contains non-finite numeric value")
        return out
    if isinstance(value, dict):
        return {
            str(key): _normalize_numeric(item, f"{label}.{key}")
            for key, item in sorted(value.items())
        }
    raise ValueError(
        f"{label} must be a numeric scalar or numeric object, "
        f"got {type(value).__name__}"
    )


def _validate_geometry_and_precision(
    geometry_summary: dict,
    precision_receipt: dict,
) -> tuple[str, str]:
    if geometry_summary.get("receipt_schema") != GEOMETRY_SUMMARY_SCHEMA:
        raise ValueError("geometry summary schema mismatch")
    if geometry_summary.get("status") != GEOMETRY_POINT_READY_STATUS:
        raise ValueError("geometry point summary is not structurally ready")
    if geometry_summary.get(
        "geometry_and_variance_point_estimates_complete"
    ) is not True:
        raise ValueError("geometry point summary lacks complete 18-path estimates")
    if geometry_summary.get("n_power_basis_paths_resolved") != 18:
        raise ValueError("geometry point summary must expose exactly 18 paths")
    readiness_sha = geometry_summary.get("readiness_receipt_sha256")
    binding_sha = geometry_summary.get("intervention_plan_binding_sha256")
    matches = geometry_summary.get("readiness_intervention_plan_match")
    required_match_keys = {
        "z_levels",
        "z_manipulation_settings",
        "p1_experimental_unit",
        "g_exclusion_method",
        "p0_level_plan_sha256",
        "p0_field_config_sha256",
        "p1_field_config_sha256",
        "g_field_config_sha256",
        "g_method_selection_sha256",
    }
    if not isinstance(readiness_sha, str) or len(readiness_sha) != 64:
        raise ValueError("geometry point summary lacks later readiness SHA-256")
    if not isinstance(binding_sha, str) or len(binding_sha) != 64:
        raise ValueError(
            "geometry point summary lacks preoutcome intervention binding"
        )
    if (
        not isinstance(matches, dict)
        or set(matches) != required_match_keys
        or not all(matches.values())
    ):
        raise ValueError(
            "geometry point summary is not admissible under later readiness"
        )

    if precision_receipt.get("receipt_schema") != PRECISION_SCHEMA:
        raise ValueError("geometry precision receipt schema mismatch")
    if precision_receipt.get("status") != PRECISION_READY_STATUS:
        raise ValueError("geometry precision receipt is not ready")
    if precision_receipt.get("basis_materialization_authorized") is not True:
        raise ValueError("geometry precision does not authorize basis use")
    if precision_receipt.get("all_18_path_precision_gate_passed") is not True:
        raise ValueError("geometry precision does not pass all 18 path gates")
    if precision_receipt.get("n_power_basis_paths_precision_evaluated") != 18:
        raise ValueError("geometry precision must evaluate exactly 18 paths")

    geometry_digest = _semantic_sha256(geometry_summary)
    if precision_receipt.get("geometry_summary_sha256") != geometry_digest:
        raise ValueError("geometry precision receipt is not bound to this summary")
    if precision_receipt.get("pilot_data_sha256") != geometry_summary.get(
        "pilot_data_sha256"
    ):
        raise ValueError(
            "geometry precision and summary pilot-data fingerprints differ"
        )
    if precision_receipt.get("pilot_config_sha256") != geometry_summary.get(
        "pilot_config_sha256"
    ):
        raise ValueError(
            "geometry precision and summary frozen-config fingerprints differ"
        )

    return geometry_digest, _semantic_sha256(precision_receipt)


def build(
    power_config: dict,
    geometry_summary: dict,
    precision_receipt: dict,
    basis_receipt: dict,
) -> dict:
    geometry_digest, precision_digest = _validate_geometry_and_precision(
        geometry_summary,
        precision_receipt,
    )
    readiness_sha = geometry_summary["readiness_receipt_sha256"]
    binding_sha = geometry_summary["intervention_plan_binding_sha256"]

    if basis_receipt.get("analysis") != BASIS_ANALYSIS:
        raise ValueError("power-basis receipt analysis schema mismatch")
    if basis_receipt.get("registered_power_status") != BASIS_READY_STATUS:
        raise ValueError("power-basis receipt is not ready for registered n")
    if basis_receipt.get("registered_single_scenario_n_basis_ready") is not True:
        raise ValueError("power-basis receipt does not authorize single-scenario n")
    if int(basis_receipt.get("n_blocking_rows", -1)) != 0:
        raise ValueError("power-basis receipt still has unresolved blockers")

    if power_config.get("schema") != POWER_SCHEMA:
        raise ValueError("power config schema mismatch")
    if power_config.get("status") != POWER_FROZEN_STATUS:
        raise ValueError(
            "geometry binding requires a prospectively frozen power config"
        )

    provenance = power_config.get("planning_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("power config lacks planning_provenance")
    for field in ("population_id", "season_id"):
        if geometry_summary.get(field) != provenance.get(field):
            raise ValueError(
                f"geometry summary and power config do not match for {field}"
            )
        if precision_receipt.get(field) != provenance.get(field):
            raise ValueError(
                f"geometry precision and power config do not match for {field}"
            )
        if basis_receipt.get(field) not in (None, provenance.get(field)):
            raise ValueError(
                f"power-basis receipt and power config do not match for {field}"
            )

    values = geometry_summary.get("resolved_power_basis_values")
    if not isinstance(values, dict) or len(values) != 18:
        raise ValueError(
            "geometry summary must expose exactly 18 resolved basis paths"
        )

    checks = []
    mismatches = []
    for path in sorted(values):
        expected = _normalize_numeric(
            values[path],
            f"geometry_summary.{path}",
        )
        observed = _normalize_numeric(
            _resolve_path(power_config, path),
            f"power_config.{path}",
        )
        match = observed == expected
        checks.append(
            {
                "config_path": path,
                "matches_geometry_summary": match,
                "geometry_value": expected,
                "power_config_value": observed,
                "normalized_precision_width": precision_receipt[
                    "normalized_95ci_width_by_power_basis_path"
                ][path],
            }
        )
        if not match:
            mismatches.append(path)

    if mismatches:
        raise ValueError(
            "power config geometry/variance values drift from geometry summary: "
            + ", ".join(mismatches)
        )

    basis_digest = _semantic_sha256(basis_receipt)
    config_digest = _semantic_sha256(power_config)

    return {
        "analysis": "pedicularis_w1_w2_geometry_config_binding_v2",
        "receipt_schema": BINDING_SCHEMA,
        "population_id": provenance["population_id"],
        "season_id": provenance["season_id"],
        "n_geometry_variance_paths_bound": len(checks),
        "all_geometry_variance_paths_match": True,
        "geometry_precision_qualified": True,
        "later_readiness_exact_plan_match": True,
        "readiness_receipt_sha256": readiness_sha,
        "intervention_plan_binding_sha256": binding_sha,
        "geometry_summary_sha256": geometry_digest,
        "geometry_precision_sha256": precision_digest,
        "pilot_data_sha256": geometry_summary["pilot_data_sha256"],
        "pilot_config_sha256": geometry_summary["pilot_config_sha256"],
        "power_basis_receipt_sha256": basis_digest,
        "power_config_sha256": config_digest,
        "path_checks": checks,
        "status": BINDING_STATUS,
        "claim_ceiling": [
            "input_provenance_binding_only",
            "requires_precision_qualified_independent_geometry_pilot",
            "binds_18_geometry_variance_values_to_exact_pilot_point_estimates",
            "binds_exact_precision_receipt_summary_basis_and_power_config",
            "does_not_register_n_by_itself",
            "does_not_generate_biological_evidence",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Bind the 18 geometry/variance values in a frozen P. rex W1/W2 "
            "power config to the exact precision-qualified independent geometry "
            "pilot and zero-blocker power-basis receipt"
        )
    )
    parser.add_argument("power_config_json", type=Path)
    parser.add_argument("geometry_summary_json", type=Path)
    parser.add_argument("geometry_precision_json", type=Path)
    parser.add_argument("power_basis_receipt_json", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = build(
        _load(args.power_config_json),
        _load(args.geometry_summary_json),
        _load(args.geometry_precision_json),
        _load(args.power_basis_receipt_json),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import math
from datetime import datetime
from pathlib import Path

from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256


FREEZE_SCHEMA = "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_V1"
FREEZE_INPUT_STATUS = "PEDICULARIS_FULL_SURFACE_THRESHOLDS_PROSPECTIVELY_FROZEN"
CONFIG_STATUS = "PEDICULARIS_FULL_SURFACE_CONFIG_PROSPECTIVELY_FROZEN"
RECEIPT_STATUS = "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_VALIDATED"
PLACEHOLDER = "REQUIRED_BEFORE_USE"

THRESHOLD_PATHS = (
    "sch_surface.min_z_levels",
    "sch_surface.min_valid_bootstrap_fraction",
    "sch_surface.min_interior_bootstrap_fraction",
    "sch_surface.min_optimum_separation",
    "sch_surface.min_optimum_shift",
    "sch_surface.min_abs_component_gradient",
)


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"{label} must be prospectively resolved")
    return value.strip()


def _number(value: object, label: str) -> float:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be prospectively resolved")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{label} must be finite")
    return out


def _positive(value: object, label: str) -> float:
    out = _number(value, label)
    if out <= 0:
        raise ValueError(f"{label} must be >0")
    return out


def _probability(value: object, label: str) -> float:
    out = _number(value, label)
    if not 0 < out <= 1:
        raise ValueError(f"{label} must lie in (0,1]")
    return out


def _positive_int(value: object, label: str) -> int:
    out = _positive(value, label)
    if not out.is_integer():
        raise ValueError(f"{label} must be an integer")
    return int(out)


def _timestamp(value: object, label: str) -> str:
    text = _text(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be ISO-8601 with timezone") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include timezone")
    return text


def _validate_config(config: dict) -> dict:
    if config.get("status") != CONFIG_STATUS:
        raise ValueError(
            "full-surface config must be explicitly prospectively frozen"
        )
    sch = config.get("sch_surface")
    checks = config.get("system_checks")
    if not isinstance(sch, dict) or not isinstance(checks, dict):
        raise ValueError(
            "full-surface config requires sch_surface and system_checks"
        )

    normalized_sch = {
        "bootstrap_reps": _positive_int(
            sch.get("bootstrap_reps"), "sch_surface.bootstrap_reps"
        ),
        "random_seed": int(
            _number(sch.get("random_seed"), "sch_surface.random_seed")
        ),
        "min_z_levels": _positive_int(
            sch.get("min_z_levels"), "sch_surface.min_z_levels"
        ),
        "min_valid_bootstrap_fraction": _probability(
            sch.get("min_valid_bootstrap_fraction"),
            "sch_surface.min_valid_bootstrap_fraction",
        ),
        "min_interior_bootstrap_fraction": _probability(
            sch.get("min_interior_bootstrap_fraction"),
            "sch_surface.min_interior_bootstrap_fraction",
        ),
        "min_optimum_separation": _positive(
            sch.get("min_optimum_separation"),
            "sch_surface.min_optimum_separation",
        ),
        "min_optimum_shift": _positive(
            sch.get("min_optimum_shift"),
            "sch_surface.min_optimum_shift",
        ),
        "min_abs_component_gradient": _positive(
            sch.get("min_abs_component_gradient"),
            "sch_surface.min_abs_component_gradient",
        ),
    }
    if normalized_sch["bootstrap_reps"] < 200:
        raise ValueError("sch_surface.bootstrap_reps must be >=200")
    if normalized_sch["min_z_levels"] < 5:
        raise ValueError("sch_surface.min_z_levels must be >=5")

    normalized_checks = {
        "max_water_depth_range": _number(
            checks.get("max_water_depth_range"),
            "system_checks.max_water_depth_range",
        ),
        "max_mechanical_damage_rate": _number(
            checks.get("max_mechanical_damage_rate"),
            "system_checks.max_mechanical_damage_rate",
        ),
    }
    if any(value < 0 for value in normalized_checks.values()):
        raise ValueError("system-check tolerances must be >=0")

    return {
        "sch_surface": normalized_sch,
        "system_checks": normalized_checks,
        "status": CONFIG_STATUS,
    }


def build(config: dict, freeze: dict) -> dict:
    normalized_config = _validate_config(config)

    if freeze.get("schema") != FREEZE_SCHEMA:
        raise ValueError(f"freeze schema must be {FREEZE_SCHEMA}")
    if freeze.get("status") != FREEZE_INPUT_STATUS:
        raise ValueError("full-surface threshold freeze is not prospective")

    population_id = _text(freeze.get("population_id"), "population_id")
    season_id = _text(freeze.get("season_id"), "season_id")
    frozen_at = _timestamp(freeze.get("frozen_at_utc"), "frozen_at_utc")
    basis_document = _text(freeze.get("basis_document"), "basis_document")

    if freeze.get("frozen_before_geometry_outcomes") is not True:
        raise ValueError(
            "full-surface decision thresholds must be frozen before geometry outcomes"
        )
    if freeze.get("frozen_before_full_surface_outcomes") is not True:
        raise ValueError(
            "full-surface decision thresholds must be frozen before P2 outcomes"
        )

    threshold_basis = freeze.get("threshold_basis")
    if not isinstance(threshold_basis, dict):
        raise ValueError("threshold_basis is required")
    if set(threshold_basis) != set(THRESHOLD_PATHS):
        raise ValueError(
            "threshold_basis must cover exactly the registered sch_surface decision paths"
        )
    normalized_basis = {
        path: _text(threshold_basis[path], f"threshold_basis.{path}")
        for path in THRESHOLD_PATHS
    }

    sch_values = normalized_config["sch_surface"]
    return {
        "analysis": "pedicularis_full_surface_threshold_freeze_v1",
        "receipt_schema": FREEZE_SCHEMA,
        "population_id": population_id,
        "season_id": season_id,
        "frozen_at_utc": frozen_at,
        "basis_document": basis_document,
        "threshold_basis": normalized_basis,
        "sch_surface": sch_values,
        "system_checks": normalized_config["system_checks"],
        "full_surface_config_sha256": _semantic_sha256(config),
        "analysis_config_sha256": _semantic_sha256(
            {
                "sch_surface": sch_values,
                "system_checks": normalized_config["system_checks"],
            }
        ),
        "sch_surface_sha256": _semantic_sha256(sch_values),
        "system_checks_sha256": _semantic_sha256(
            normalized_config["system_checks"]
        ),
        "frozen_before_geometry_outcomes": True,
        "frozen_before_full_surface_outcomes": True,
        "status": RECEIPT_STATUS,
        "claim_ceiling": [
            "prospective_decision_threshold_freeze_only",
            "threshold_values_not_inferred_from_geometry_or_P2_outcomes",
            "does_not_validate_causal_compromise",
            "does_not_register_sample_size_by_itself",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Freeze the exact P. rex full-surface decision thresholds before "
            "geometry or confirmatory P2 outcomes"
        )
    )
    parser.add_argument("full_surface_config_json", type=Path)
    parser.add_argument("threshold_freeze_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        _load(args.full_surface_config_json),
        _load(args.threshold_freeze_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

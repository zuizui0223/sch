from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256


CONFIG_SCHEMA = "PEDICULARIS_P2_CONTEXT_FREEZE_CONFIG_V1"
CONFIG_STATUS = "PEDICULARIS_P2_CONTEXT_SELECTION_PROSPECTIVELY_DECLARED"
RECEIPT_SCHEMA = "PEDICULARIS_P2_CONTEXT_FREEZE_V1"
READY_SCHEMA = "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3"
READY_STATUS = "PEDICULARIS_FULL_SURFACE_READY"

ALLOWED_SELECTION_MODES = {
    "CURRENT_CONTEXT_ONLY",
    "HISTORICAL_CONTEXT_PRIOR",
}
ALLOWED_MAPPING_STATUS = {
    "NONE",
    "SOURCE_VERIFIED",
}
PLACEHOLDER = "REQUIRED_BEFORE_USE"
PLACEHOLDER_OR_NONE = "REQUIRED_BEFORE_USE_OR_NONE"


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _read_priors(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("historical context prior ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("historical context prior ledger is empty")
    return rows


def _text(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or value in {PLACEHOLDER, PLACEHOLDER_OR_NONE}
    ):
        raise ValueError(f"{label} must be prospectively resolved")
    return value.strip()


def _validate_config(config: dict) -> dict:
    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError(f"context config schema must be {CONFIG_SCHEMA}")
    if config.get("status") != CONFIG_STATUS:
        raise ValueError("P2 context selection config is not prospectively declared")
    if config.get("declared_before_full_surface_outcomes") is not True:
        raise ValueError(
            "P2 context selection must be declared before full-surface outcomes"
        )

    population_id = _text(config.get("population_id"), "population_id")
    season_id = _text(config.get("season_id"), "season_id")
    selection_mode = _text(
        config.get("selection_mode"),
        "selection_mode",
    )
    if selection_mode not in ALLOWED_SELECTION_MODES:
        raise ValueError(
            "selection_mode must be CURRENT_CONTEXT_ONLY or HISTORICAL_CONTEXT_PRIOR"
        )

    inference_scope = _text(
        config.get("inference_scope"),
        "inference_scope",
    )
    basis_note = _text(
        config.get("selection_basis_note"),
        "selection_basis_note",
    )

    historical_code = _text(
        config.get("historical_population_code"),
        "historical_population_code",
    )
    mapping_status = _text(
        config.get("historical_mapping_status"),
        "historical_mapping_status",
    )
    if mapping_status not in ALLOWED_MAPPING_STATUS:
        raise ValueError(
            "historical_mapping_status must be NONE or SOURCE_VERIFIED"
        )

    mapping_source_raw = config.get("historical_mapping_source")
    mapping_source = (
        mapping_source_raw.strip()
        if isinstance(mapping_source_raw, str)
        else ""
    )

    if selection_mode == "CURRENT_CONTEXT_ONLY":
        if historical_code != "NONE":
            raise ValueError(
                "CURRENT_CONTEXT_ONLY requires historical_population_code=NONE"
            )
        if mapping_status != "NONE":
            raise ValueError(
                "CURRENT_CONTEXT_ONLY requires historical_mapping_status=NONE"
            )
        if mapping_source not in {"", "NONE", PLACEHOLDER_OR_NONE}:
            raise ValueError(
                "CURRENT_CONTEXT_ONLY must not claim a historical mapping source"
            )
        mapping_source = None
    else:
        if historical_code == "NONE":
            raise ValueError(
                "HISTORICAL_CONTEXT_PRIOR requires a historical population code"
            )
        if mapping_status != "SOURCE_VERIFIED":
            raise ValueError(
                "historical population codes require SOURCE_VERIFIED locality mapping"
            )
        if (
            not mapping_source
            or mapping_source in {"NONE", PLACEHOLDER, PLACEHOLDER_OR_NONE}
        ):
            raise ValueError(
                "historical population codes require a verified mapping source"
            )

    return {
        "population_id": population_id,
        "season_id": season_id,
        "selection_mode": selection_mode,
        "inference_scope": inference_scope,
        "selection_basis_note": basis_note,
        "historical_population_code": historical_code,
        "historical_mapping_status": mapping_status,
        "historical_mapping_source": mapping_source,
    }


def _validate_readiness(readiness: dict, config: dict) -> dict:
    if readiness.get("receipt_schema_version") != READY_SCHEMA:
        raise ValueError("context freeze requires full-surface readiness V3")
    if readiness.get("status") != READY_STATUS:
        raise ValueError("same-season P2 context is not full-surface ready")
    if readiness.get("population_id") != config["population_id"]:
        raise ValueError("readiness population_id does not match context config")
    if readiness.get("season_id") != config["season_id"]:
        raise ValueError("readiness season_id does not match context config")

    checks = readiness.get("checks")
    if not isinstance(checks, dict) or not checks or not all(
        bool(value) for value in checks.values()
    ):
        raise ValueError("readiness receipt does not have all positive checks")

    source = readiness.get("source_receipts")
    if not isinstance(source, dict):
        raise ValueError("readiness receipt lacks source receipt summary")

    p = source.get("p")
    g = source.get("g")
    z = source.get("z")
    if not isinstance(p, dict) or not isinstance(g, dict) or not isinstance(z, dict):
        raise ValueError("readiness receipt lacks z/P/G source summaries")
    if p.get("status") != "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED":
        raise ValueError("current-season pollination lane is not validated")
    if g.get("status") != "PEDICULARIS_PREDATOR_METHOD_VALIDATED":
        raise ValueError("current-season antagonist lane is not validated")
    if z.get("status") != "PEDICULARIS_Z_MANIPULATION_VALIDATED":
        raise ValueError("current-season z manipulation is not validated")

    return {
        "pollination_lane_validated": True,
        "antagonist_lane_validated": True,
        "z_manipulation_validated": True,
        "same_population_and_season": True,
        "readiness_receipt_sha256": _semantic_sha256(readiness),
    }


def _historical_prior(
    prior_rows: list[dict[str, str]],
    config: dict,
) -> dict | None:
    if config["selection_mode"] == "CURRENT_CONTEXT_ONLY":
        return None

    code = config["historical_population_code"]
    matches = [
        row
        for row in prior_rows
        if row.get("historical_population_code") == code
    ]
    if len(matches) != 1:
        raise ValueError(
            "historical_population_code must match exactly one prior row"
        )
    row = matches[0]

    pressure = row.get("exact_main_text_seed_predation_percent", "")
    rank = row.get("exact_pressure_rank_among_four", "")
    return {
        "historical_population_code": code,
        "individual_linkage_retained": (
            row.get("individual_linkage_retained") == "YES"
        ),
        "exact_main_text_seed_predation_percent": (
            float(pressure) if pressure else None
        ),
        "exact_pressure_rank_among_four": int(rank) if rank else None,
        "history_class": row.get("history_class"),
        "allowed_use": row.get("allowed_use"),
        "source": row.get("source"),
        "mapping_status": config["historical_mapping_status"],
        "mapping_source": config["historical_mapping_source"],
        "historical_value_is_current_season_measurement": False,
    }


def build(
    config_payload: dict,
    readiness: dict,
    prior_rows: list[dict[str, str]],
) -> dict:
    config = _validate_config(config_payload)
    current = _validate_readiness(readiness, config)
    historical = _historical_prior(prior_rows, config)

    return {
        "analysis": "pedicularis_p2_context_freeze_v1",
        "receipt_schema": RECEIPT_SCHEMA,
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "selection_mode": config["selection_mode"],
        "inference_scope": config["inference_scope"],
        "selection_basis_note": config["selection_basis_note"],
        "historical_context_prior": historical,
        "current_season_context": current,
        "same_season_pollination_and_antagonist_lanes_validated": True,
        "context_selected_before_full_surface_outcomes": True,
        "readiness_receipt_sha256": current["readiness_receipt_sha256"],
        "context_config_sha256": _semantic_sha256(config_payload),
        "status": (
            "P2_CONTEXT_FROZEN_CURRENT_SEASON_BOTH_FUNCTIONAL_LANES_VALIDATED"
        ),
        "next_step": (
            "freeze W1/W2 headline-power scenario for this exact population/season, "
            "then bind the passing powered design to P2 flower allocation"
        ),
        "claim_ceiling": [
            "same_season_context_qualification_only",
            "historical_pressure_is_recruitment_prior_not_current_season_measurement",
            "current_P1_and_G_validation_supports_both_functional_lanes_active",
            "does_not_establish_W1_or_W2",
            "does_not_estimate_population_prevalence",
            "does_not_generalize_from_enriched_context_to_species_wide_effect",
            "historical_population_code_requires_source_verified_locality_mapping",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Freeze the P. rex P2 population/season after same-context P1/G/z "
            "validation, optionally attaching a source-verified historical context prior"
        )
    )
    parser.add_argument("context_config_json", type=Path)
    parser.add_argument("readiness_json", type=Path)
    parser.add_argument("historical_priors_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        _load_json(args.context_config_json),
        _load_json(args.readiness_json),
        _read_priors(args.historical_priors_csv),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

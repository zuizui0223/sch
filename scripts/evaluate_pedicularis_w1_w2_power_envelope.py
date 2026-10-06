from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from scripts.simulate_pedicularis_w1_w2_power import (
    SENSITIVITY_STATUS,
    simulate_power,
)


SCHEMA = "PEDICULARIS_W1_W2_POWER_ENVELOPE_V1"
STATUS = "PEDICULARIS_W1_W2_POWER_ENVELOPE_PROSPECTIVELY_DECLARED"
PLACEHOLDER = "REQUIRED_BEFORE_USE"
OUTPUT_STATUS = (
    "PEDICULARIS_W1_W2_POWER_ENVELOPE_DIAGNOSTIC_READY_NOT_REGISTERED_N"
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


def _semantic_sha256(payload: object) -> str:
    text = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _validate_manifest(manifest: dict) -> list[dict[str, str]]:
    if manifest.get("schema") != SCHEMA:
        raise ValueError(f"envelope schema must be {SCHEMA}")
    if manifest.get("status") != STATUS:
        raise ValueError("power envelope is not prospectively declared")
    if manifest.get("frozen_before_full_surface_outcomes") is not True:
        raise ValueError(
            "power envelope must be frozen before full-surface outcomes"
        )

    _text(manifest.get("population_id"), "population_id")
    _text(manifest.get("season_id"), "season_id")
    _text(manifest.get("envelope_basis_note"), "envelope_basis_note")

    scenarios = manifest.get("scenarios")
    if not isinstance(scenarios, list) or len(scenarios) < 2:
        raise ValueError("power envelope requires at least two scenarios")

    normalized = []
    seen: set[str] = set()
    for row in scenarios:
        if not isinstance(row, dict):
            raise ValueError("every envelope scenario entry must be an object")
        scenario_id = _text(row.get("scenario_id"), "scenario_id")
        if scenario_id in seen:
            raise ValueError("scenario_id must be unique")
        seen.add(scenario_id)
        normalized.append(
            {
                "scenario_id": scenario_id,
                "config_path": _text(row.get("config_path"), "config_path"),
                "scenario_role": _text(
                    row.get("scenario_role"),
                    "scenario_role",
                ),
                "basis_note": _text(row.get("basis_note"), "basis_note"),
            }
        )
    return normalized


def _signature(config: dict) -> dict:
    if config.get("status") != SENSITIVITY_STATUS:
        raise ValueError(
            "every envelope scenario config must use "
            "PEDICULARIS_W1_W2_POWER_SENSITIVITY_SCENARIO_ONLY"
        )

    provenance = config.get("planning_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("scenario config lacks planning_provenance")

    model = config.get("generating_model")
    if not isinstance(model, dict):
        raise ValueError("scenario config lacks generating_model")
    z_levels = model.get("z_levels")
    if not isinstance(z_levels, list):
        raise ValueError("scenario config lacks generating_model.z_levels")

    return {
        "population_id": provenance.get("population_id"),
        "season_id": provenance.get("season_id"),
        "candidate_plants": config.get("candidate_plants"),
        "field_design": config.get("field_design"),
        "simulation_reps": config.get("simulation_reps"),
        "target_primary_surface_power": config.get(
            "target_primary_surface_power"
        ),
        "target_headline_w1_or_w2_power": config.get(
            "target_headline_w1_or_w2_power"
        ),
        "z_levels": z_levels,
        "production_surface_config": config.get("production_surface_config"),
        "secondary_diagnostic_config": config.get(
            "secondary_diagnostic_config"
        ),
    }


def _validate_scenario_set(
    manifest: dict,
    scenario_entries: list[dict[str, str]],
    configs: dict[str, dict],
) -> dict:
    if set(configs) != {row["scenario_id"] for row in scenario_entries}:
        raise ValueError(
            "scenario config IDs do not match envelope manifest IDs"
        )

    signatures = {
        scenario_id: _signature(config)
        for scenario_id, config in configs.items()
    }
    reference_id = scenario_entries[0]["scenario_id"]
    reference = signatures[reference_id]

    if reference["population_id"] != manifest["population_id"]:
        raise ValueError("manifest and scenario population_id do not match")
    if reference["season_id"] != manifest["season_id"]:
        raise ValueError("manifest and scenario season_id do not match")

    drift = {}
    for scenario_id, signature in signatures.items():
        if signature != reference:
            changed = sorted(
                key
                for key in reference
                if signature.get(key) != reference.get(key)
            )
            drift[scenario_id] = changed
    if drift:
        detail = "; ".join(
            f"{scenario}={','.join(fields)}"
            for scenario, fields in sorted(drift.items())
        )
        raise ValueError(
            "envelope scenarios must share one design/analysis signature; "
            + detail
        )

    truth_worlds = {
        scenario_id: config.get("target_truth_world")
        for scenario_id, config in configs.items()
    }
    if any(value not in {"W1", "W2"} for value in truth_worlds.values()):
        raise ValueError("envelope target_truth_world values must be W1 or W2")

    return {
        "signature": reference,
        "truth_worlds": truth_worlds,
        "scenario_config_sha256": {
            scenario_id: _semantic_sha256(config)
            for scenario_id, config in configs.items()
        },
    }


def _scenario_minimum(result: dict) -> int | None:
    target_primary = float(result["target_primary_surface_power"])
    target_headline = float(result["target_headline_w1_or_w2_power"])
    eligible = [
        int(row["plants"])
        for row in result["candidate_results"]
        if (
            float(row["primary_surface_power"]) >= target_primary
            and float(row["headline_W1_or_W2_power"]) >= target_headline
        )
    ]
    return min(eligible) if eligible else None


def aggregate(
    *,
    manifest: dict,
    scenario_entries: list[dict[str, str]],
    scenario_results: dict[str, dict],
    validation: dict,
    basis_receipt: dict,
) -> dict:
    scenario_ids = [row["scenario_id"] for row in scenario_entries]
    if set(scenario_results) != set(scenario_ids):
        raise ValueError("scenario results do not match manifest")

    first = scenario_results[scenario_ids[0]]
    target_primary = float(first["target_primary_surface_power"])
    target_headline = float(first["target_headline_w1_or_w2_power"])

    candidate_sets = {
        scenario_id: tuple(
            int(row["plants"])
            for row in scenario_results[scenario_id]["candidate_results"]
        )
        for scenario_id in scenario_ids
    }
    if len(set(candidate_sets.values())) != 1:
        raise ValueError("scenario results do not share the same candidate n grid")
    candidate_grid = list(candidate_sets[scenario_ids[0]])

    indexed = {
        scenario_id: {
            int(row["plants"]): row
            for row in scenario_results[scenario_id]["candidate_results"]
        }
        for scenario_id in scenario_ids
    }

    candidate_envelope = []
    for n in candidate_grid:
        primary = {
            scenario_id: float(indexed[scenario_id][n]["primary_surface_power"])
            for scenario_id in scenario_ids
        }
        headline = {
            scenario_id: float(
                indexed[scenario_id][n]["headline_W1_or_W2_power"]
            )
            for scenario_id in scenario_ids
        }
        truth = {
            scenario_id: float(
                indexed[scenario_id][n]["target_truth_world_power"]
            )
            for scenario_id in scenario_ids
        }

        min_primary = min(primary.values())
        min_headline = min(headline.values())
        min_truth = min(truth.values())

        candidate_envelope.append(
            {
                "plants": n,
                "worst_case_primary_surface_power": min_primary,
                "worst_case_headline_W1_or_W2_power": min_headline,
                "worst_case_target_truth_world_power": min_truth,
                "worst_primary_scenario_ids": sorted(
                    scenario_id
                    for scenario_id, value in primary.items()
                    if value == min_primary
                ),
                "worst_headline_scenario_ids": sorted(
                    scenario_id
                    for scenario_id, value in headline.items()
                    if value == min_headline
                ),
                "meets_targets_in_every_scenario": (
                    min_primary >= target_primary
                    and min_headline >= target_headline
                ),
            }
        )

    all_scenario_candidate = [
        row["plants"]
        for row in candidate_envelope
        if row["meets_targets_in_every_scenario"]
    ]
    envelope_min = (
        min(all_scenario_candidate) if all_scenario_candidate else None
    )

    scenario_minima = {
        scenario_id: _scenario_minimum(scenario_results[scenario_id])
        for scenario_id in scenario_ids
    }
    resolved_minima = [
        value for value in scenario_minima.values() if value is not None
    ]
    all_have_candidate = len(resolved_minima) == len(scenario_ids)
    min_range = (
        [min(resolved_minima), max(resolved_minima)]
        if resolved_minima
        else None
    )
    all_same = (
        all_have_candidate
        and len(set(resolved_minima)) == 1
    )

    metadata = {
        row["scenario_id"]: {
            "scenario_role": row["scenario_role"],
            "basis_note": row["basis_note"],
            "target_truth_world": validation["truth_worlds"][row["scenario_id"]],
            "config_sha256": validation["scenario_config_sha256"][
                row["scenario_id"]
            ],
        }
        for row in scenario_entries
    }

    return {
        "analysis": "pedicularis_w1_w2_power_envelope_v1",
        "status": OUTPUT_STATUS,
        "population_id": manifest["population_id"],
        "season_id": manifest["season_id"],
        "envelope_basis_note": manifest["envelope_basis_note"],
        "manifest_sha256": _semantic_sha256(manifest),
        "basis_receipt_status": basis_receipt.get("registered_power_status"),
        "basis_blocker_count": int(basis_receipt.get("n_blocking_rows", -1)),
        "n_scenarios": len(scenario_ids),
        "scenario_metadata": metadata,
        "shared_design_signature": validation["signature"],
        "target_primary_surface_power": target_primary,
        "target_headline_w1_or_w2_power": target_headline,
        "scenario_minimum_candidate_plants": scenario_minima,
        "all_scenarios_have_candidate_meeting_targets": all_have_candidate,
        "all_scenarios_same_minimum_candidate": all_same,
        "scenario_minimum_candidate_range": min_range,
        "geometry_uncertainty_changes_minimum_candidate": (
            all_have_candidate and not all_same
        ),
        "some_scenario_exceeds_candidate_grid": not all_have_candidate,
        "candidate_envelope": candidate_envelope,
        "minimum_candidate_meeting_targets_in_every_scenario": envelope_min,
        "registered_n_promoted": False,
        "registered_field_allocation_authorized": False,
        "interpretation": (
            "This envelope quantifies how much prospective causal-geometry "
            "uncertainty changes the sample-size requirement. It is a "
            "value-of-information diagnostic, not a registered n."
        ),
        "claim_ceiling": [
            "sensitivity_envelope_only",
            "scenario_powers_are_not_averaged",
            "worst_case_power_across_declared_scenarios_is_reported",
            "does_not_resolve_missing_causal_geometry_basis",
            "does_not_authorize_P2_field_allocation",
            "scenario_bounds_require_independent_scientific_justification",
        ],
    }


def build(
    manifest: dict,
    configs: dict[str, dict],
    basis_receipt: dict,
) -> dict:
    scenario_entries = _validate_manifest(manifest)
    validation = _validate_scenario_set(
        manifest,
        scenario_entries,
        configs,
    )
    scenario_results = {
        scenario_id: simulate_power(
            configs[scenario_id],
            basis_receipt=basis_receipt,
        )
        for scenario_id in [row["scenario_id"] for row in scenario_entries]
    }
    return aggregate(
        manifest=manifest,
        scenario_entries=scenario_entries,
        scenario_results=scenario_results,
        validation=validation,
        basis_receipt=basis_receipt,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Run a prospectively declared multi-scenario sensitivity envelope "
            "for the P. rex W1/W2 production power pipeline"
        )
    )
    parser.add_argument("manifest_json", type=Path)
    parser.add_argument("basis_receipt_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = _load(args.manifest_json)
    entries = _validate_manifest(manifest)
    configs = {}
    for row in entries:
        path = Path(row["config_path"])
        if not path.is_absolute():
            path = args.manifest_json.parent / path
        configs[row["scenario_id"]] = _load(path)

    result = build(
        manifest,
        configs,
        _load(args.basis_receipt_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

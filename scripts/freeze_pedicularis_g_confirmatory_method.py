from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.pedicularis_config_freeze import (
    validate_freeze_context,
    validate_prospective_freeze,
)


SCHEMA = "PEDICULARIS_G_CONFIRMATORY_METHOD_FREEZE_V1"
STATUS = "PEDICULARIS_G_CONFIRMATORY_METHOD_PROSPECTIVELY_FROZEN"
OUTPUT_SCHEMA = "PEDICULARIS_G_CONFIRMATORY_METHOD_SELECTION_V1"
OUTPUT_STATUS = "PEDICULARIS_G_CONFIRMATORY_METHOD_SELECTED_BEFORE_OUTCOMES"
PLACEHOLDER = "REQUIRED_BEFORE_USE"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"{label} must be prospectively resolved")
    return value.strip()


def _positive_int(value: object, label: str) -> int:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be prospectively resolved")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(number) or number < 1 or not number.is_integer():
        raise ValueError(f"{label} must be a positive integer")
    return int(number)


def build(
    freeze_config: dict,
    exploratory_screen: dict,
    g_field_config: dict,
) -> dict:
    if freeze_config.get("schema") != SCHEMA:
        raise ValueError(f"confirmatory G method-freeze schema must be {SCHEMA}")
    if freeze_config.get("status") != STATUS:
        raise ValueError("confirmatory G method is not prospectively frozen")
    if freeze_config.get("frozen_before_confirmatory_G_data") is not True:
        raise ValueError(
            "confirmatory G method choice must be frozen before confirmatory outcomes"
        )

    population_id = _text(freeze_config.get("population_id"), "population_id")
    season_id = _text(freeze_config.get("season_id"), "season_id")
    candidate_id = _text(
        freeze_config.get("selected_candidate_id"), "selected_candidate_id"
    )
    method = _text(
        freeze_config.get("selected_exclusion_method"),
        "selected_exclusion_method",
    )
    sham_method = _text(
        freeze_config.get("exposed_sham_method_code"),
        "exposed_sham_method_code",
    )
    if sham_method == method:
        raise ValueError("exposed sham and excluded method codes must differ")
    basis_note = _text(
        freeze_config.get("selection_basis_note"), "selection_basis_note"
    )
    n_plants = _positive_int(
        freeze_config.get("planned_n_plants"), "planned_n_plants"
    )
    flowers_per_treatment = _positive_int(
        freeze_config.get("flowers_per_treatment_per_plant"),
        "flowers_per_treatment_per_plant",
    )

    if exploratory_screen.get("analysis") != "pedicularis_g_candidate_linked_screen_v1":
        raise ValueError("G exploratory screen schema mismatch")
    if exploratory_screen.get("status") != "G_CANDIDATE_LINKED_EXPLORATORY_SCREEN_ONLY":
        raise ValueError("G exploratory screen is not in the registered exploratory state")
    if exploratory_screen.get("population_id") != population_id:
        raise ValueError("exploratory G screen population does not match method freeze")
    if exploratory_screen.get("season_id") != season_id:
        raise ValueError("exploratory G screen season does not match method freeze")
    if exploratory_screen.get("candidate_selected") is not False:
        raise ValueError("exploratory screen must not have selected a candidate")

    hard_pass = exploratory_screen.get("hard_validity_pass_candidate_ids")
    if not isinstance(hard_pass, list) or candidate_id not in hard_pass:
        raise ValueError(
            "selected confirmatory G candidate must be a hard-validity pass candidate"
        )
    candidate_screens = exploratory_screen.get("candidate_screens")
    if not isinstance(candidate_screens, dict) or candidate_id not in candidate_screens:
        raise ValueError("selected candidate is missing from exploratory screen")
    candidate = candidate_screens[candidate_id]
    if candidate.get("hard_validity_all_pass") is not True:
        raise ValueError("selected candidate did not pass all hard-validity gates")
    if candidate.get("field_exclusion_method") != method:
        raise ValueError(
            "selected_exclusion_method does not match the registered candidate method"
        )

    freeze = validate_prospective_freeze(g_field_config, "G")
    validate_freeze_context(freeze, population_id, season_id)
    method_gate = g_field_config.get("method_gate")
    predator_weight = g_field_config.get("predator_weight")
    if not isinstance(method_gate, dict) or not isinstance(predator_weight, dict):
        raise ValueError("G field config lacks method/predator-weight gates")

    min_plants = max(
        _positive_int(method_gate.get("min_paired_plants"), "method_gate.min_paired_plants"),
        _positive_int(
            predator_weight.get("min_paired_plants"),
            "predator_weight.min_paired_plants",
        ),
    )
    min_flowers = max(
        _positive_int(
            method_gate.get("min_flowers_per_treatment"),
            "method_gate.min_flowers_per_treatment",
        ),
        _positive_int(
            predator_weight.get("min_flowers_per_treatment"),
            "predator_weight.min_flowers_per_treatment",
        ),
    )
    if n_plants < min_plants:
        raise ValueError("planned_n_plants is below the frozen G minimum paired plants")
    n_per_treatment = n_plants * flowers_per_treatment
    if n_per_treatment < min_flowers:
        raise ValueError(
            "planned G flowers per treatment are below the frozen G minimum"
        )

    return {
        "analysis": "pedicularis_g_confirmatory_method_freeze_v1",
        "receipt_schema": OUTPUT_SCHEMA,
        "population_id": population_id,
        "season_id": season_id,
        "selected_candidate_id": candidate_id,
        "selected_exclusion_method": method,
        "exposed_sham_method_code": sham_method,
        "planned_n_plants": n_plants,
        "flowers_per_treatment_per_plant": flowers_per_treatment,
        "n_flowers_per_treatment": n_per_treatment,
        "selection_basis_note": basis_note,
        "hard_validity_pass_candidate_ids": list(hard_pass),
        "multiple_hard_pass_candidates_present": len(hard_pass) > 1,
        "exploratory_screen_sha256": _semantic_sha256(exploratory_screen),
        "g_field_config_sha256": _semantic_sha256(g_field_config),
        "g_threshold_freeze": freeze,
        "candidate_effect_size_used_for_selection": False,
        "confirmatory_G_outcomes_used_for_selection": False,
        "status": OUTPUT_STATUS,
        "claim_ceiling": [
            "method_selection_and_sample_size_binding_only",
            "selected_candidate_must_have_passed_hard_validity",
            "multiple_hard_pass_candidates_require_explicit_preoutcome_basis_note",
            "no_posthoc_effect_size_ranking",
            "does_not_validate_confirmatory_G",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Freeze one hard-validity-passing P. rex G method and paired "
            "confirmatory design before confirmatory outcomes"
        )
    )
    parser.add_argument("method_freeze_json", type=Path)
    parser.add_argument("exploratory_screen_json", type=Path)
    parser.add_argument("g_field_config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        _load(args.method_freeze_json),
        _load(args.exploratory_screen_json),
        _load(args.g_field_config_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

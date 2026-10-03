from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


SCREEN_SCHEMA = "SCH_PEDICULARIS_G_DEVICE_SCREEN_V1"
SCREEN_STATUS = "G_DEVICE_SCREEN_HAS_ADMISSIBLE_METHOD"
SELECTION_SCHEMA = "SCH_PEDICULARIS_G_DEVICE_SELECTION_V1"
SELECTION_INPUT_STATUS = "PEDICULARIS_G_DEVICE_SELECTION_INPUT_FROZEN"
SELECTION_STATUS = "PEDICULARIS_G_DEVICE_SELECTED_FOR_CONFIRMATORY_QUALIFICATION"
PLACEHOLDER = "REQUIRED_BEFORE_USE"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _text(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or value == PLACEHOLDER
    ):
        raise ValueError(f"{label} is not prospectively specified")
    return value.strip()


def _timestamp(value: object, label: str) -> str:
    text = _text(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} is not a valid ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must be timezone-aware")
    return text


def freeze_selection(
    screen_receipt: dict,
    selection_input: dict,
) -> dict:
    if screen_receipt.get("receipt_schema_version") != SCREEN_SCHEMA:
        raise ValueError("G device screen receipt schema mismatch")
    if screen_receipt.get("status") != SCREEN_STATUS:
        raise ValueError(
            "G device selection requires a screen with at least one admissible method"
        )
    if screen_receipt.get("thresholds_applied") is not False:
        raise ValueError("G device screen must remain threshold-free")
    if screen_receipt.get("confirmatory_receipt_generated") is not False:
        raise ValueError("G device screen must not be confirmatory")

    if selection_input.get("receipt_schema_version") != SELECTION_SCHEMA:
        raise ValueError("G device selection input schema mismatch")
    if selection_input.get("status") != SELECTION_INPUT_STATUS:
        raise ValueError("G device selection input status is not frozen")
    if selection_input.get("selected_before_confirmatory_data") is not True:
        raise ValueError(
            "G device identity must be selected before confirmatory data"
        )

    screen_context = (
        screen_receipt.get("population_id"),
        screen_receipt.get("season_id"),
    )
    selection_context = (
        selection_input.get("population_id"),
        selection_input.get("season_id"),
    )
    if screen_context != selection_context:
        raise ValueError(
            "G device screen and selection must share population and season"
        )

    population_id = _text(selection_input.get("population_id"), "population_id")
    season_id = _text(selection_input.get("season_id"), "season_id")
    selected = _text(
        selection_input.get("selected_exclusion_method"),
        "selected_exclusion_method",
    )
    basis_document = _text(
        selection_input.get("basis_document"),
        "basis_document",
    )
    selection_basis_note = _text(
        selection_input.get("selection_basis_note"),
        "selection_basis_note",
    )
    selected_at_utc = _timestamp(
        selection_input.get("selected_at_utc"),
        "selected_at_utc",
    )

    admissible = set(screen_receipt.get("admissible_methods") or [])
    if selected not in admissible:
        raise ValueError(
            "selected_exclusion_method is not hard-validity admissible in the "
            "exploratory G device screen"
        )

    method_results = screen_receipt.get("method_results")
    if not isinstance(method_results, dict):
        raise ValueError("G device screen lacks method_results")
    selected_result = method_results.get(selected)
    if not isinstance(selected_result, dict):
        raise ValueError("selected G device lacks screen result")
    if selected_result.get("hard_validity_pass") is not True:
        raise ValueError("selected G device failed hard method validity")

    return {
        "receipt_schema_version": SELECTION_SCHEMA,
        "analysis": "pedicularis_g_device_selection_freeze",
        "population_id": population_id,
        "season_id": season_id,
        "selected_exclusion_method": selected,
        "selected_at_utc": selected_at_utc,
        "basis_document": basis_document,
        "selection_basis_note": selection_basis_note,
        "screen_receipt_schema": screen_receipt["receipt_schema_version"],
        "screen_status": screen_receipt["status"],
        "screen_candidate_methods": screen_receipt["candidate_methods"],
        "screen_admissible_methods": screen_receipt["admissible_methods"],
        "selected_method_screen_summary": selected_result,
        "status": SELECTION_STATUS,
        "claim_ceiling": [
            "prospective_method_identity_selection_only",
            "selected_method_has_passed_hard_exploratory_validity_only",
            "does_not_validate_G_effectiveness",
            "does_not_freeze_CAL_B_effect_or_timing_targets",
            "does_not_generate_confirmatory_G_receipt",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Freeze one hard-validity-admissible Pedicularis G barrier identity "
            "before confirmatory method qualification"
        )
    )
    parser.add_argument("screen_receipt_json", type=Path)
    parser.add_argument("selection_input_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = freeze_selection(
        _load(args.screen_receipt_json),
        _load(args.selection_input_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

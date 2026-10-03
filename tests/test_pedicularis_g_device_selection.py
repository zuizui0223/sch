from __future__ import annotations

import pytest

from scripts.freeze_pedicularis_g_device_selection import (
    SELECTION_INPUT_STATUS,
    SELECTION_SCHEMA,
    SELECTION_STATUS,
    freeze_selection,
)


def _screen() -> dict:
    method_results = {
        "SLEEVE_A": {
            "hard_validity_pass": True,
            "status": "G_DEVICE_HARD_VALIDITY_ADMISSIBLE",
            "n_paired_plants": 8,
        },
        "SLEEVE_B": {
            "hard_validity_pass": False,
            "status": "G_DEVICE_REJECTED_HARD_VALIDITY",
            "n_paired_plants": 8,
        },
    }
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_G_DEVICE_SCREEN_V1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "candidate_methods": ["SLEEVE_A", "SLEEVE_B"],
        "admissible_methods": ["SLEEVE_A"],
        "rejected_methods": ["SLEEVE_B"],
        "method_results": method_results,
        "status": "G_DEVICE_SCREEN_HAS_ADMISSIBLE_METHOD",
        "thresholds_applied": False,
        "confirmatory_receipt_generated": False,
    }


def _selection(method: str = "SLEEVE_A") -> dict:
    return {
        "receipt_schema_version": SELECTION_SCHEMA,
        "status": SELECTION_INPUT_STATUS,
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "selected_exclusion_method": method,
        "selected_before_confirmatory_data": True,
        "selected_at_utc": "2026-10-03T12:00:00Z",
        "basis_document": "UNIT_TEST_G_DEVICE_SELECTION_BASIS",
        "selection_basis_note": "UNIT_TEST_MANUAL_SELECTION_AFTER_HARD_SCREEN",
    }


def test_admissible_device_can_be_frozen_prospectively() -> None:
    result = freeze_selection(_screen(), _selection())
    assert result["receipt_schema_version"] == SELECTION_SCHEMA
    assert result["status"] == SELECTION_STATUS
    assert result["selected_exclusion_method"] == "SLEEVE_A"
    assert result["selected_method_screen_summary"]["hard_validity_pass"] is True


def test_hard_invalid_device_cannot_be_selected() -> None:
    with pytest.raises(ValueError, match="not hard-validity admissible"):
        freeze_selection(_screen(), _selection("SLEEVE_B"))


def test_device_selection_context_must_match_screen() -> None:
    selection = _selection()
    selection["season_id"] = "S2"
    with pytest.raises(ValueError, match="share population and season"):
        freeze_selection(_screen(), selection)


def test_device_identity_must_be_frozen_before_confirmatory_data() -> None:
    selection = _selection()
    selection["selected_before_confirmatory_data"] = False
    with pytest.raises(ValueError, match="before confirmatory data"):
        freeze_selection(_screen(), selection)


def test_device_selection_timestamp_must_be_timezone_aware() -> None:
    selection = _selection()
    selection["selected_at_utc"] = "2026-10-03T12:00:00"
    with pytest.raises(ValueError, match="timezone-aware"):
        freeze_selection(_screen(), selection)


def test_screen_with_no_admissible_method_cannot_generate_selection() -> None:
    screen = _screen()
    screen["status"] = "G_DEVICE_SCREEN_NO_ADMISSIBLE_METHOD"
    screen["admissible_methods"] = []
    with pytest.raises(ValueError, match="at least one admissible"):
        freeze_selection(screen, _selection())

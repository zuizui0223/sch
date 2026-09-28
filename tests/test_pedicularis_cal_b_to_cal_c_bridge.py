from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from scripts.apply_pedicularis_cal_b_to_cal_c import (
    PLACEHOLDER,
    _read_csv,
    build,
)


ROOT = Path(__file__).resolve().parents[1]
CAL_C_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_C_CRITERIA_TEMPLATE_V1.csv"
)


EFFECT_TARGETS = {
    "pollination_weight.min_pollen_grain_delta": 5.0,
    "pollination_weight.min_initial_seed_set_delta": 0.10,
    "predator_weight.min_early_attack_reduction": 0.20,
    "predator_weight.min_predation_fraction_reduction": 0.10,
    "predator_weight.min_final_seed_set_gain": 0.08,
}


def _receipt() -> dict:
    decisions = [
        {
            "gate_path": gate,
            "target_value": value,
            "target_basis_note": f"UNIT_TEST_BASIS_{gate}",
        }
        for gate, value in EFFECT_TARGETS.items()
    ]
    decisions += [
        {
            "gate_path": "method_gate.min_hours_after_anthesis_before_barrier",
            "target_value": 8.0,
            "target_basis_note": "UNIT_TEST_TIMING_LOWER",
        },
        {
            "gate_path": "method_gate.max_hours_after_anthesis_before_barrier",
            "target_value": 24.0,
            "target_basis_note": "UNIT_TEST_TIMING_UPPER",
        },
    ]
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "targets": {
            **EFFECT_TARGETS,
            "method_gate.min_hours_after_anthesis_before_barrier": 8.0,
            "method_gate.max_hours_after_anthesis_before_barrier": 24.0,
        },
        "decision_rows": decisions,
        "status": "PEDICULARIS_CAL_B_TARGETS_FROZEN",
    }


def _criteria() -> list[dict[str, str]]:
    rows = _read_csv(CAL_C_TEMPLATE)
    for row in rows:
        row["population_id"] = "P_REX_TEST"
        row["season_id"] = "S1"
        row["pilot_sd"] = "0.5"
        row["pilot_sd_source"] = "UNIT_TEST_CALIBRATION_SUMMARY.sd"
    return rows


def test_bridge_transfers_exactly_five_effect_boundaries() -> None:
    rows, receipt = build(_receipt(), _criteria())

    assert receipt["status"] == "CAL_B_EFFECT_BOUNDARIES_TRANSFERRED_TO_CAL_C"
    assert receipt["n_boundaries_transferred"] == 5
    assert set(receipt["transferred_gate_paths"]) == set(EFFECT_TARGETS)
    assert receipt["assumed_true_values_selected"] == 0

    by_gate = {row["gate_path"]: row for row in rows}
    for gate, value in EFFECT_TARGETS.items():
        assert float(by_gate[gate]["boundary"]) == pytest.approx(value)
        assert by_gate[gate]["basis_note"].startswith("CAL_B_TARGET_FREEZE:")
        assert by_gate[gate]["assumed_true_value"] == PLACEHOLDER

    untouched = [
        row for row in rows
        if row["gate_path"] not in EFFECT_TARGETS
    ]
    assert all(row["boundary"] == PLACEHOLDER for row in untouched)
    assert all(row["basis_note"] == PLACEHOLDER for row in untouched)
    assert all(row["assumed_true_value"] == PLACEHOLDER for row in untouched)


def test_timing_targets_are_not_inserted_into_cal_c_criteria() -> None:
    rows, _ = build(_receipt(), _criteria())
    gate_paths = {row["gate_path"] for row in rows}
    assert "method_gate.min_hours_after_anthesis_before_barrier" not in gate_paths
    assert "method_gate.max_hours_after_anthesis_before_barrier" not in gate_paths


def test_bridge_refuses_context_mismatch() -> None:
    rows = _criteria()
    rows[0]["season_id"] = "S2"
    with pytest.raises(ValueError, match="season does not match"):
        build(_receipt(), rows)


def test_bridge_refuses_to_overwrite_existing_boundary() -> None:
    rows = _criteria()
    target = next(
        row for row in rows
        if row["gate_path"] == "pollination_weight.min_pollen_grain_delta"
    )
    target["boundary"] = "99"
    with pytest.raises(ValueError, match="already populated"):
        build(_receipt(), rows)


def test_bridge_refuses_to_touch_prefilled_assumed_true_value() -> None:
    rows = _criteria()
    altered = deepcopy(rows)
    altered[-1]["assumed_true_value"] = "1.0"
    with pytest.raises(ValueError, match="must remain unresolved"):
        build(_receipt(), altered)

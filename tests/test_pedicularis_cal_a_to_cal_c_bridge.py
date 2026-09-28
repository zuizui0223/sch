from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from scripts.apply_pedicularis_cal_a_to_cal_c import (
    CAL_A_GATE_PATHS,
    PLACEHOLDER,
    _read_csv,
    build as apply_cal_a,
)
from scripts.apply_pedicularis_cal_b_to_cal_c import (
    EFFECT_GATE_PATHS,
    build as apply_cal_b,
)


ROOT = Path(__file__).resolve().parents[1]
CAL_C_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_C_CRITERIA_TEMPLATE_V1.csv"
)


def _criteria() -> list[dict[str, str]]:
    rows = _read_csv(CAL_C_TEMPLATE)
    for row in rows:
        row["population_id"] = "P_REX_TEST"
        row["season_id"] = "S1"
        row["pilot_sd"] = "0.5"
        row["pilot_sd_source"] = "UNIT_TEST_CALIBRATION_SUMMARY.sd"
    return rows


def _cal_a_receipt() -> dict:
    targets = {gate: 0.10 for gate in CAL_A_GATE_PATHS}
    decisions = [
        {
            "gate_path": gate,
            "target_value": value,
            "target_basis_note": f"UNIT_TEST_CAL_A_{gate}",
        }
        for gate, value in sorted(targets.items())
    ]
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_CAL_A_TARGET_FREEZE_V1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "targets": targets,
        "decision_rows": decisions,
        "status": "PEDICULARIS_CAL_A_TARGETS_FROZEN",
    }


def _cal_b_receipt() -> dict:
    targets = {
        "pollination_weight.min_pollen_grain_delta": 5.0,
        "pollination_weight.min_initial_seed_set_delta": 0.10,
        "predator_weight.min_early_attack_reduction": 0.20,
        "predator_weight.min_predation_fraction_reduction": 0.10,
        "predator_weight.min_final_seed_set_gain": 0.08,
        "method_gate.min_hours_after_anthesis_before_barrier": 8.0,
        "method_gate.max_hours_after_anthesis_before_barrier": 24.0,
    }
    decisions = [
        {
            "gate_path": gate,
            "target_value": value,
            "target_basis_note": f"UNIT_TEST_CAL_B_{gate}",
        }
        for gate, value in sorted(targets.items())
    ]
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "targets": targets,
        "decision_rows": decisions,
        "status": "PEDICULARIS_CAL_B_TARGETS_FROZEN",
    }


def test_cal_a_bridge_transfers_exactly_20_boundaries() -> None:
    rows, receipt = apply_cal_a(_cal_a_receipt(), _criteria())

    assert receipt["status"] == "CAL_A_BOUNDARIES_TRANSFERRED_TO_CAL_C"
    assert receipt["n_boundaries_transferred"] == 20
    assert set(receipt["transferred_gate_paths"]) == CAL_A_GATE_PATHS
    assert receipt["assumed_true_values_selected"] == 0

    by_gate = {row["gate_path"]: row for row in rows}
    for gate in CAL_A_GATE_PATHS:
        assert float(by_gate[gate]["boundary"]) == pytest.approx(0.10)
        assert by_gate[gate]["basis_note"].startswith("CAL_A_TARGET_FREEZE:")
        assert by_gate[gate]["assumed_true_value"] == PLACEHOLDER

    cal_b_rows = [row for row in rows if row["gate_path"] in EFFECT_GATE_PATHS]
    assert len(cal_b_rows) == 5
    assert all(row["boundary"] == PLACEHOLDER for row in cal_b_rows)
    assert all(row["basis_note"] == PLACEHOLDER for row in cal_b_rows)


def test_cal_a_plus_cal_b_fill_all_25_cal_c_boundaries_only() -> None:
    after_a, _ = apply_cal_a(_cal_a_receipt(), _criteria())
    after_b, receipt_b = apply_cal_b(_cal_b_receipt(), after_a)

    assert receipt_b["n_boundaries_transferred"] == 5
    assert len(after_b) == 25
    assert all(row["boundary"] != PLACEHOLDER for row in after_b)
    assert all(row["basis_note"] != PLACEHOLDER for row in after_b)
    assert all(row["assumed_true_value"] == PLACEHOLDER for row in after_b)

    prefixes = {row["basis_note"].split(":", 1)[0] for row in after_b}
    assert prefixes == {"CAL_A_TARGET_FREEZE", "CAL_B_TARGET_FREEZE"}


def test_cal_a_bridge_refuses_context_mismatch() -> None:
    rows = _criteria()
    rows[0]["season_id"] = "S2"
    with pytest.raises(ValueError, match="season does not match"):
        apply_cal_a(_cal_a_receipt(), rows)


def test_cal_a_bridge_refuses_existing_boundary() -> None:
    rows = _criteria()
    target = next(row for row in rows if row["gate_path"] in CAL_A_GATE_PATHS)
    target["boundary"] = "1.0"
    with pytest.raises(ValueError, match="already populated"):
        apply_cal_a(_cal_a_receipt(), rows)


def test_cal_a_bridge_refuses_prefilled_assumed_true_value() -> None:
    rows = deepcopy(_criteria())
    rows[-1]["assumed_true_value"] = "1.0"
    with pytest.raises(ValueError, match="must remain unresolved"):
        apply_cal_a(_cal_a_receipt(), rows)

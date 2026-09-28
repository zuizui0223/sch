from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "empirical" / "architecture" / "PEDICULARIS_CALIBRATION_MODULE_LEDGER_V1.csv"

EXPECTED_MODULE_COUNTS = {
    "REGISTERED_CONTRACT": 5,
    "CAL_A": 20,
    "CAL_B": 7,
    "CAL_C": 8,
}


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_calibration_module_ledger_maps_all_40_gate_fields() -> None:
    rows = _rows()
    assert len(rows) == 40
    assert len({(row["lane"], row["gate_path"]) for row in rows}) == 40
    assert Counter(row["calibration_module"] for row in rows) == EXPECTED_MODULE_COUNTS


def test_all_unresolved_gate_fields_map_to_exactly_one_calibration_module() -> None:
    rows = _rows()
    unresolved = [
        row for row in rows
        if row["basis_status"] != "RESOLVED_FROM_REGISTERED_CONTRACT"
    ]
    assert len(unresolved) == 35
    assert {row["calibration_module"] for row in unresolved} == {
        "CAL_A", "CAL_B", "CAL_C"
    }
    assert all(row["calibration_module"] != "REGISTERED_CONTRACT" for row in unresolved)


def test_cal_c_is_downstream_of_cal_a_and_cal_b_threshold_inputs() -> None:
    rows = [
        row for row in _rows()
        if row["calibration_module"] == "CAL_C"
    ]
    assert len(rows) == 8
    assert {
        row["prerequisite"] for row in rows
    } == {"CAL_A_AND_CAL_B_RELEVANT_THRESHOLD_INPUTS_FROZEN"}
    assert all(
        row["required_output"] == "PROSPECTIVE_SAMPLE_SIZE_OR_PRECISION_REQUIREMENT"
        for row in rows
    )


def test_cal_a_and_cal_b_are_nonconfirmatory_evidence_modules() -> None:
    rows = _rows()
    cal_a = [row for row in rows if row["calibration_module"] == "CAL_A"]
    cal_b = [row for row in rows if row["calibration_module"] == "CAL_B"]
    assert len(cal_a) == 20
    assert len(cal_b) == 7
    assert all("confirmatory" not in row["required_output"].lower() for row in cal_a + cal_b)

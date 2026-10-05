from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

from scripts.pedicularis_config_freeze import required_gate_paths


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "empirical" / "architecture" / "PEDICULARIS_THRESHOLD_BASIS_LEDGER_V1.csv"

EXPECTED_STATUS_COUNTS = {
    "RESOLVED_FROM_REGISTERED_CONTRACT": 5,
    "NEEDS_POWER_OR_PRECISION": 8,
    "NEEDS_MEASUREMENT_CALIBRATION": 1,
    "NEEDS_EQUIVALENCE_CALIBRATION": 17,
    "NEEDS_METHOD_FEASIBILITY_CALIBRATION": 2,
    "NEEDS_EFFECT_SIZE_JUSTIFICATION": 5,
    "NEEDS_METHOD_PILOT": 2,
}


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_threshold_basis_ledger_covers_every_freeze_gate_exactly_once() -> None:
    rows = _rows()
    assert len(rows) == 40

    actual = [(row["lane"], row["gate_path"]) for row in rows]
    assert len(actual) == len(set(actual))

    expected = {
        (lane, path)
        for lane in ("P0", "P1", "G")
        for path in required_gate_paths(lane)
    }
    assert set(actual) == expected
    assert {row["confirmatory_use"] for row in rows} == {"BLOCKING"}


def test_only_five_gate_values_are_resolved_from_existing_contracts() -> None:
    rows = _rows()
    counts = Counter(row["basis_status"] for row in rows)
    assert dict(counts) == EXPECTED_STATUS_COUNTS

    resolved = {
        (row["lane"], row["gate_path"]): row["registered_value"]
        for row in rows
        if row["basis_status"] == "RESOLVED_FROM_REGISTERED_CONTRACT"
    }
    assert resolved == {
        ("P0", "stage_p0.min_z_levels"): "5",
        ("G", "method_gate.require_pollination_window_complete"): "true",
        ("G", "method_gate.require_ovary_not_swollen"): "true",
        ("G", "method_gate.require_barrier_not_cover_pollinator_entry"): "true",
        ("G", "method_gate.require_sham_on_exposed"): "true",
    }


def test_unresolved_gates_do_not_smuggle_in_numeric_test_fixture_values() -> None:
    rows = _rows()
    unresolved = [
        row
        for row in rows
        if row["basis_status"] != "RESOLVED_FROM_REGISTERED_CONTRACT"
    ]
    assert len(unresolved) == 35
    assert all(row["registered_value"] == "" for row in unresolved)
    assert all(row["basis_source"] for row in unresolved)
    assert all(row["resolution_action"] for row in unresolved)
    assert all("tests/" not in row["basis_source"] for row in rows)


def test_g_timing_bounds_remain_explicitly_pilot_dependent() -> None:
    rows = {
        (row["lane"], row["gate_path"]): row
        for row in _rows()
    }
    for path in (
        "method_gate.min_hours_after_anthesis_before_barrier",
        "method_gate.max_hours_after_anthesis_before_barrier",
    ):
        row = rows[("G", path)]
        assert row["basis_status"] == "NEEDS_METHOD_PILOT"
        assert row["registered_value"] == ""
        assert row["basis_route"] == (
            "ORDINAL_PRIMARY_EVIDENCE_PLUS_FOCAL_EVENT_TIME_PILOT"
        )
        assert "SCH_PEDICULARIS_G_TIMING_PRIMARY_EVIDENCE_V1.md" in (
            row["basis_source"]
        )
        assert "METHOD_PRECEDENTS" in row["basis_source"]
        assert "focal P. rex method-development pilot" in row[
            "resolution_action"
        ]

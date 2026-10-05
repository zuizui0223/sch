from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.audit_pedicularis_g_timing_primary_evidence import (
    DEFAULT_EVIDENCE,
    build,
)


def _rows(path: Path = DEFAULT_EVIDENCE) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_primary_timing_audit_recovers_order_but_not_hour_bounds() -> None:
    result = build(_rows())

    assert result["focal_ordinal_oviposition_window_recovered"] is True
    assert result["focal_bumblebee_dependence_recovered"] is True
    assert result["focal_pollination_mechanism_recovered"] is True
    assert result["focal_hour_scale_lower_bound_recovered"] is False
    assert result["focal_hour_scale_upper_bound_recovered"] is False
    assert result["current_timing_gate_state"] == (
        "FOCAL_HOUR_SCALE_TIMING_REQUIRES_METHOD_PILOT"
    )


def test_natural_predation_pressure_is_not_method_failure_tolerance() -> None:
    result = build(_rows())

    assert result["natural_predation_range_percent"] == [1.36, 27.42]
    assert (
        result["natural_predation_can_set_device_hard_failure_tolerance"]
        is False
    )
    assert "no_device_failure_tolerance_from_natural_predation" in (
        result["claim_ceiling"]
    )


def test_congeneric_flower_longevity_is_not_portable_to_p_rex_timing() -> None:
    result = build(_rows())
    assert result["congeneric_flower_longevity_can_set_focal_timing_bound"] is False

    rows = {row["evidence_id"]: row for row in _rows()}
    congeneric = rows["PEDICULARIS2013_FLOWER_LONGEVITY"]
    assert congeneric["taxon_scope"] == "Pedicularis_congeneric_set"
    assert congeneric["reported_value"] == "4 to 7"
    assert congeneric["direct_hour_bound_eligible"] == "NO"


def test_required_focal_event_time_estimands_remain_explicit() -> None:
    result = build(_rows())
    assert set(result["field_estimands_required"]) == {
        "time_from_anthesis_to_pollination_window_complete",
        "time_from_anthesis_to_first_pre_barrier_attack_or_oviposition",
        "time_from_anthesis_to_ovary_swelling",
    }


def test_primary_evidence_cannot_be_silently_promoted_to_hour_bound() -> None:
    rows = _rows()
    rows[0] = dict(rows[0])
    rows[0]["direct_hour_bound_eligible"] = "YES"

    with pytest.raises(ValueError, match="hour-scale G timing bound"):
        build(rows)


def test_primary_evidence_cannot_be_silently_promoted_to_failure_tolerance() -> None:
    rows = _rows()
    pred = next(
        i
        for i, row in enumerate(rows)
        if row["evidence_axis"] == "NATURAL_SEED_PREDATION"
    )
    rows[pred] = dict(rows[pred])
    rows[pred]["hard_failure_tolerance_eligible"] = "YES"

    with pytest.raises(ValueError, match="hard-failure tolerance"):
        build(rows)


def test_threshold_basis_keeps_both_hour_bounds_in_focal_method_pilot() -> None:
    ledger_path = (
        Path(__file__).resolve().parents[1]
        / "empirical"
        / "architecture"
        / "PEDICULARIS_THRESHOLD_BASIS_LEDGER_V1.csv"
    )
    rows = _rows(ledger_path)
    timing = {
        row["gate_path"]: row
        for row in rows
        if row["lane"] == "G"
        and row["gate_kind"] == "METHOD_TIMING_BOUND"
    }

    assert set(timing) == {
        "method_gate.min_hours_after_anthesis_before_barrier",
        "method_gate.max_hours_after_anthesis_before_barrier",
    }
    assert {
        row["basis_status"] for row in timing.values()
    } == {"NEEDS_METHOD_PILOT"}
    assert {
        row["basis_route"] for row in timing.values()
    } == {"ORDINAL_PRIMARY_EVIDENCE_PLUS_FOCAL_EVENT_TIME_PILOT"}
    assert all(
        "SCH_PEDICULARIS_G_TIMING_PRIMARY_EVIDENCE_V1.md"
        in row["basis_source"]
        for row in timing.values()
    )

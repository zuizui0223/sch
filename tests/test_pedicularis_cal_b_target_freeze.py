from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from scripts.freeze_pedicularis_cal_b_targets import (
    FREEZE_STATUS,
    _read as read_target_table,
    validate,
)
from scripts.materialize_pedicularis_cal_b_observed import (
    PLACEHOLDER,
    _read_csv,
    build,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_B_TARGET_TEMPLATE_V1.csv"
)


def _dist(mean: float) -> dict:
    return {
        "n": 12,
        "mean": mean,
        "sd": 0.1,
        "min": mean - 0.2,
        "q05": mean - 0.1,
        "median": mean,
        "q95": mean + 0.1,
        "max": mean + 0.2,
    }


def _summary() -> dict:
    return {
        "analysis": "pedicularis_calibration_pilot_summary_v1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "available_pilot_lanes": ["G", "G_TIMING", "P0", "P1"],
        "pilot_summaries": {
            "P1": {
                "plant_level_distributions": {
                    "pollen_grains_delta": _dist(12.0),
                    "initial_seed_set_delta": _dist(0.18),
                }
            },
            "G": {
                "plant_level_distributions": {
                    "attack_reduction": _dist(0.50),
                    "predation_reduction": _dist(0.20),
                    "final_seed_gain": _dist(0.15),
                },
                "barrier_delay_hours": _dist(14.0),
            },
            "G_TIMING": {
                "pollination_complete_observation_hours": _dist(8.0),
                "first_constraint_positive_observation_hours": _dist(20.0),
            },
        },
        "status": "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION",
        "thresholds_selected": False,
        "confirmatory_receipt_generated": False,
    }


def _materialized() -> list[dict[str, str]]:
    rows, receipt = build(_summary(), _read_csv(TEMPLATE))
    assert receipt["status"] == (
        "CAL_B_OBSERVED_SUMMARIES_MATERIALIZED_TARGETS_UNFROZEN"
    )
    return rows


def _frozen_rows() -> list[dict[str, str]]:
    rows = _materialized()
    targets = {
        "pollination_weight.min_pollen_grain_delta": 5.0,
        "pollination_weight.min_initial_seed_set_delta": 0.10,
        "predator_weight.min_early_attack_reduction": 0.20,
        "predator_weight.min_predation_fraction_reduction": 0.10,
        "predator_weight.min_final_seed_set_gain": 0.08,
        "method_gate.min_hours_after_anthesis_before_barrier": 8.0,
        "method_gate.max_hours_after_anthesis_before_barrier": 24.0,
    }
    for row in rows:
        row["target_value"] = str(targets[row["gate_path"]])
        row["target_basis_note"] = "UNIT_TEST_SYNTHETIC_BIOLOGICAL_TARGET"
        row["frozen_before_confirmatory_data"] = "YES"
        row["frozen_at_utc"] = "2026-09-28T00:00:00Z"
        row["status"] = FREEZE_STATUS
    return rows


def test_template_has_exact_seven_cal_b_decisions() -> None:
    rows = _read_csv(TEMPLATE)
    assert len(rows) == 7
    assert {row["decision_kind"] for row in rows} == {
        "MINIMUM_EFFECT",
        "TIMING_LOWER_BOUND",
        "TIMING_UPPER_BOUND",
    }
    assert all(row["target_value"] == PLACEHOLDER for row in rows)


def test_materializer_copies_observed_context_but_never_targets() -> None:
    rows, receipt = build(_summary(), _read_csv(TEMPLATE))

    assert receipt["n_target_decisions"] == 7
    assert receipt["targets_selected"] == 0
    assert {row["population_id"] for row in rows} == {"P_REX_TEST"}
    assert {row["season_id"] for row in rows} == {"S1"}
    assert all(row["observed_n"] == "12" for row in rows)
    assert all(row["observed_mean"] != PLACEHOLDER for row in rows)
    assert all(row["target_value"] == PLACEHOLDER for row in rows)
    assert all(row["target_basis_note"] == PLACEHOLDER for row in rows)
    assert all(
        row["frozen_before_confirmatory_data"] == PLACEHOLDER
        for row in rows
    )


def test_positive_cal_b_freeze_receipt_requires_all_seven_manual_targets() -> None:
    result = validate(_frozen_rows())

    assert result["receipt_schema_version"] == (
        "SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1"
    )
    assert result["status"] == "PEDICULARIS_CAL_B_TARGETS_FROZEN"
    assert result["n_decisions"] == 7
    assert result["targets"][
        "method_gate.min_hours_after_anthesis_before_barrier"
    ] == pytest.approx(8.0)
    assert result["targets"][
        "method_gate.max_hours_after_anthesis_before_barrier"
    ] == pytest.approx(24.0)


def test_materialized_but_unfrozen_targets_fail_closed() -> None:
    with pytest.raises(ValueError, match="target_value"):
        validate(_materialized())


def test_minimum_effect_targets_must_be_positive() -> None:
    rows = _frozen_rows()
    row = next(
        item
        for item in rows
        if item["gate_path"] == "pollination_weight.min_initial_seed_set_delta"
    )
    row["target_value"] = "0"
    with pytest.raises(ValueError, match="must be > 0"):
        validate(rows)


def test_g_timing_lower_bound_must_precede_upper_bound() -> None:
    rows = _frozen_rows()
    for row in rows:
        if row["decision_kind"] == "TIMING_LOWER_BOUND":
            row["target_value"] = "30"
        if row["decision_kind"] == "TIMING_UPPER_BOUND":
            row["target_value"] = "24"
    with pytest.raises(ValueError, match="strictly below"):
        validate(rows)


def test_freeze_timestamp_must_be_timezone_aware() -> None:
    rows = _frozen_rows()
    rows[0]["frozen_at_utc"] = "2026-09-28T00:00:00"
    with pytest.raises(ValueError, match="timezone-aware"):
        validate(rows)


def test_cal_b_target_is_not_required_to_equal_pilot_mean() -> None:
    rows = _frozen_rows()
    pollen = next(
        item
        for item in rows
        if item["gate_path"] == "pollination_weight.min_pollen_grain_delta"
    )
    assert float(pollen["observed_mean"]) == pytest.approx(12.0)
    assert float(pollen["target_value"]) == pytest.approx(5.0)
    result = validate(rows)
    assert result["targets"][pollen["gate_path"]] == pytest.approx(5.0)


def test_materializer_refuses_prefilled_target_leakage() -> None:
    template = _read_csv(TEMPLATE)
    altered = deepcopy(template)
    altered[0]["target_value"] = "1.0"
    with pytest.raises(ValueError, match="must remain unresolved"):
        build(_summary(), altered)


def test_g_timing_targets_use_natural_event_time_sources_not_barrier_delay() -> None:
    rows = _read_csv(TEMPLATE)
    timing = {
        row["decision_kind"]: row["calibration_source_path"]
        for row in rows
        if row["lane"] == "G" and row["decision_kind"].startswith("TIMING_")
    }
    assert timing == {
        "TIMING_LOWER_BOUND": (
            "pilot_summaries.G_TIMING.pollination_complete_observation_hours"
        ),
        "TIMING_UPPER_BOUND": (
            "pilot_summaries.G_TIMING.first_constraint_positive_observation_hours"
        ),
    }
    assert all("barrier_delay_hours" not in value for value in timing.values())


def test_cal_b_materializer_requires_separate_g_timing_summary() -> None:
    summary = _summary()
    summary["available_pilot_lanes"] = ["G", "P0", "P1"]
    summary["pilot_summaries"].pop("G_TIMING")
    with pytest.raises(ValueError, match="G event-time"):
        build(summary, _read_csv(TEMPLATE))

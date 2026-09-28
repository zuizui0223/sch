from __future__ import annotations

from pathlib import Path

import pytest

from scripts.freeze_pedicularis_cal_a_targets import (
    FREEZE_STATUS,
    validate,
)
from scripts.materialize_pedicularis_cal_a_observed import (
    NOT_APPLICABLE,
    PLACEHOLDER,
    _read_csv,
    build,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_A_TARGET_TEMPLATE_V1.csv"
)


def _dist(mean: float = 0.05) -> dict:
    return {
        "n": 12,
        "mean": mean,
        "sd": 0.02,
        "min": 0.0,
        "q05": max(0.0, mean - 0.02),
        "median": mean,
        "q95": mean + 0.02,
        "max": mean + 0.03,
    }


def _calibration_summary() -> dict:
    return {
        "analysis": "pedicularis_calibration_pilot_summary_v1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "available_pilot_lanes": ["G", "P0", "P1"],
        "pilot_summaries": {
            "P0": {
                "plant_level_gate_metric_distributions": {
                    "minimum_adjacent_exsertion_gap": _dist(0.15),
                    "opening_width_relative_change": _dist(),
                    "tube_diameter_relative_change": _dist(),
                    "bract_height_relative_change": _dist(),
                    "lower_lip_angle_abs_change": _dist(),
                    "water_depth_abs_change": _dist(),
                    "flower_orientation_abs_change": _dist(),
                    "maximum_mechanical_damage_rate": _dist(0.02),
                }
            },
            "P1": {
                "plant_level_distributions": {
                    "early_predator_attack_abs_difference": _dist(),
                    "z_relative_change": _dist(),
                    "bract_height_relative_change": _dist(),
                    "opening_width_relative_change": _dist(),
                    "water_depth_abs_difference": _dist(),
                    "maximum_mechanical_damage_rate": _dist(0.02),
                }
            },
            "G": {
                "plant_level_distributions": {
                    "initial_seed_abs_difference": _dist(),
                    "pollen_relative_change": _dist(),
                    "pollinator_visit_relative_change": _dist(),
                    "z_relative_change": _dist(),
                    "water_depth_abs_difference": _dist(),
                    "damage_rate_abs_difference": _dist(),
                }
            },
        },
        "status": "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION",
        "thresholds_selected": False,
        "confirmatory_receipt_generated": False,
    }


def _repeatability_summary() -> dict:
    def metric(relative: bool) -> dict:
        out = {
            "max_absolute_deviation_from_flower_mean": {"q95": 0.01},
        }
        if relative:
            out["max_relative_deviation_from_flower_mean"] = {"q95": 0.01}
        return out

    return {
        "analysis": "pedicularis_cal_a_repeatability_summary_v1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "metric_repeatability": {
            "realized_exsertion": metric(True),
            "corolla_opening_width": metric(True),
            "tube_diameter": metric(True),
            "bract_height": metric(True),
            "lower_lip_angle_deg": metric(False),
            "water_depth": metric(False),
            "flower_orientation_deg": metric(False),
        },
        "status": "CAL_A_REPEATABILITY_SUMMARY_ONLY_NO_MARGIN_DECISION",
        "thresholds_selected": False,
        "confirmatory_receipt_generated": False,
    }


def _materialized() -> list[dict[str, str]]:
    rows, receipt = build(
        _calibration_summary(),
        _repeatability_summary(),
        _read_csv(TEMPLATE),
    )
    assert receipt["status"] == (
        "CAL_A_OBSERVED_AND_REPEATABILITY_MATERIALIZED_TARGETS_UNFROZEN"
    )
    return rows


def _frozen_rows() -> list[dict[str, str]]:
    rows = _materialized()
    for row in rows:
        if row["decision_kind"] == "MINIMUM_SEPARATION":
            row["target_value"] = "0.10"
        else:
            row["target_value"] = "0.10"
        row["target_basis_note"] = "UNIT_TEST_SYNTHETIC_MARGIN_BASIS"
        row["frozen_before_confirmatory_data"] = "YES"
        row["frozen_at_utc"] = "2026-09-28T00:00:00Z"
        row["status"] = FREEZE_STATUS
    return rows


def test_template_covers_exactly_20_cal_a_decisions() -> None:
    rows = _read_csv(TEMPLATE)
    assert len(rows) == 20
    assert sum(row["lane"] == "P0" for row in rows) == 8
    assert sum(row["lane"] == "P1" for row in rows) == 6
    assert sum(row["lane"] == "G" for row in rows) == 6
    assert {row["decision_kind"] for row in rows} == {
        "MINIMUM_SEPARATION",
        "EQUIVALENCE_UPPER",
    }


def test_materializer_combines_pilot_and_repeatability_without_targets() -> None:
    rows, receipt = build(
        _calibration_summary(),
        _repeatability_summary(),
        _read_csv(TEMPLATE),
    )
    assert receipt["n_target_decisions"] == 20
    assert receipt["n_with_measurement_noise_q95"] == 13
    assert receipt["n_without_direct_repeatability_metric"] == 7
    assert receipt["targets_selected"] == 0
    assert all(row["target_value"] == PLACEHOLDER for row in rows)

    with_noise = [
        row for row in rows
        if row["repeatability_source_path"] != NOT_APPLICABLE
    ]
    without_noise = [
        row for row in rows
        if row["repeatability_source_path"] == NOT_APPLICABLE
    ]
    assert len(with_noise) == 13
    assert len(without_noise) == 7
    assert all(float(row["measurement_noise_q95"]) == pytest.approx(0.01) for row in with_noise)
    assert all(row["measurement_noise_q95"] == NOT_APPLICABLE for row in without_noise)


def test_positive_cal_a_freeze_receipt_has_20_targets() -> None:
    result = validate(_frozen_rows())
    assert result["receipt_schema_version"] == "SCH_PEDICULARIS_CAL_A_TARGET_FREEZE_V1"
    assert result["status"] == "PEDICULARIS_CAL_A_TARGETS_FROZEN"
    assert result["n_decisions"] == 20
    assert result["n_targets_with_measurement_noise_floor"] == 13
    assert len(result["targets"]) == 20


def test_materialized_but_unfrozen_cal_a_targets_fail_closed() -> None:
    with pytest.raises(ValueError, match="target_value"):
        validate(_materialized())


def test_target_must_exceed_measurement_noise_q95_when_available() -> None:
    rows = _frozen_rows()
    target = next(
        row for row in rows
        if row["repeatability_source_path"] != NOT_APPLICABLE
    )
    target["target_value"] = target["measurement_noise_q95"]
    with pytest.raises(ValueError, match="must exceed measurement_noise_q95"):
        validate(rows)


def test_target_without_repeatability_metric_still_requires_positive_basis() -> None:
    rows = _frozen_rows()
    target = next(
        row for row in rows
        if row["repeatability_source_path"] == NOT_APPLICABLE
    )
    target["target_value"] = "0"
    with pytest.raises(ValueError, match="target must be > 0"):
        validate(rows)


def test_repeatability_context_must_match_calibration_context() -> None:
    repeatability = _repeatability_summary()
    repeatability["season_id"] = "S2"
    with pytest.raises(ValueError, match="share population and season"):
        build(_calibration_summary(), repeatability, _read_csv(TEMPLATE))


def test_freeze_timestamp_must_be_timezone_aware() -> None:
    rows = _frozen_rows()
    rows[0]["frozen_at_utc"] = "2026-09-28T00:00:00"
    with pytest.raises(ValueError, match="timezone-aware"):
        validate(rows)

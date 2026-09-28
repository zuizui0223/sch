from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from scripts.materialize_pedicularis_cal_c_pilot_sd import (
    PLACEHOLDER,
    _read_csv,
    build,
)


ROOT = Path(__file__).resolve().parents[1]
CRITERIA_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_C_CRITERIA_TEMPLATE_V1.csv"
)


def _summary(criteria_rows: list[dict[str, str]]) -> dict:
    p0 = {}
    p1 = {}
    g = {}
    for row in criteria_rows:
        if row["criterion_type"] != "NORMAL_BOUND":
            continue
        target = {"sd": 0.5}
        if row["lane"] == "P0":
            p0[row["metric_source"]] = target
        elif row["lane"] == "P1":
            p1[row["metric_source"]] = target
        else:
            g[row["metric_source"]] = target

    return {
        "analysis": "pedicularis_calibration_pilot_summary_v1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "available_pilot_lanes": ["G", "P0", "P1"],
        "pilot_summaries": {
            "P0": {
                "plant_level_gate_metric_distributions": p0,
            },
            "P1": {
                "plant_level_distributions": p1,
            },
            "G": {
                "plant_level_distributions": g,
            },
        },
        "status": "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION",
        "thresholds_selected": False,
        "confirmatory_receipt_generated": False,
    }


def test_materializer_fills_only_pilot_sd_and_provenance() -> None:
    template = _read_csv(CRITERIA_TEMPLATE)
    rows, receipt = build(_summary(template), template)

    assert receipt["n_criteria"] == 25
    assert receipt["n_continuous_criteria_with_pilot_sd"] == 23
    assert receipt["n_binomial_criteria_without_sd"] == 2
    assert receipt["boundaries_selected"] == 0
    assert receipt["assumed_true_values_selected"] == 0
    assert receipt["status"] == (
        "CAL_C_PILOT_SD_MATERIALIZED_TARGETS_STILL_UNFROZEN"
    )

    normal = [row for row in rows if row["criterion_type"] == "NORMAL_BOUND"]
    assert len(normal) == 23
    assert all(float(row["pilot_sd"]) == pytest.approx(0.5) for row in normal)
    assert all(row["pilot_sd_source"].endswith(".sd") for row in normal)

    binomial = [
        row for row in rows
        if row["criterion_type"] == "BINOMIAL_UPPER"
    ]
    assert len(binomial) == 2
    assert {
        row["pilot_sd"] for row in binomial
    } == {"NOT_APPLICABLE"}
    assert {
        row["pilot_sd_source"] for row in binomial
    } == {"NOT_APPLICABLE"}

    assert all(row["boundary"] == PLACEHOLDER for row in rows)
    assert all(row["assumed_true_value"] == PLACEHOLDER for row in rows)
    assert all(row["basis_note"] == PLACEHOLDER for row in rows)
    assert {row["population_id"] for row in rows} == {"P_REX_TEST"}
    assert {row["season_id"] for row in rows} == {"S1"}


def test_materializer_fails_if_required_pilot_metric_is_missing() -> None:
    template = _read_csv(CRITERIA_TEMPLATE)
    summary = _summary(template)
    summary["pilot_summaries"]["P1"]["plant_level_distributions"].pop(
        "pollen_grains_delta"
    )
    with pytest.raises(ValueError, match="lacks metric"):
        build(summary, template)


def test_materializer_requires_all_three_pilot_lanes() -> None:
    template = _read_csv(CRITERIA_TEMPLATE)
    summary = _summary(template)
    summary["available_pilot_lanes"] = ["P0", "P1"]
    with pytest.raises(ValueError, match="requires P0, P1 and G"):
        build(summary, template)


def test_materializer_refuses_to_overwrite_a_prefilled_boundary() -> None:
    template = _read_csv(CRITERIA_TEMPLATE)
    altered = deepcopy(template)
    altered[0]["boundary"] = "0.1"
    with pytest.raises(ValueError, match="must remain unresolved"):
        build(_summary(template), altered)


def test_materializer_requires_threshold_free_calibration_summary() -> None:
    template = _read_csv(CRITERIA_TEMPLATE)
    summary = _summary(template)
    summary["thresholds_selected"] = True
    with pytest.raises(ValueError, match="must not have selected thresholds"):
        build(summary, template)

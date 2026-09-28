from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.plan_pedicularis_cal_c import (
    PLANNING_STATUS,
    _read_criteria,
    build_plan,
    minimum_binomial_n,
    normal_boundary_required_n,
)


ROOT = Path(__file__).resolve().parents[1]
CRITERIA_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_C_CRITERIA_TEMPLATE_V1.csv"
)
CONFIG_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_C_PLANNING_CONFIG_TEMPLATE_V1.json"
)


def _criteria() -> list[dict[str, str]]:
    rows = _read_criteria(CRITERIA_TEMPLATE)
    for row in rows:
        row["population_id"] = "P_REX_TEST"
        row["season_id"] = "S1"
        row["basis_note"] = "UNIT_TEST_SYNTHETIC_PLANNING_INPUT"
        if row["criterion_type"] == "BINOMIAL_UPPER":
            row["boundary"] = "0.10"
            row["assumed_true_value"] = "0.0"
        elif row["direction"] == "LOWER":
            row["boundary"] = "0.0"
            row["assumed_true_value"] = "1.0"
        else:
            row["boundary"] = "1.0"
            row["assumed_true_value"] = "0.0"
        row["pilot_sd"] = (
            "NOT_APPLICABLE"
            if row["criterion_type"] == "BINOMIAL_UPPER"
            else "1.0"
        )
        row["pilot_sd_source"] = (
            "NOT_APPLICABLE"
            if row["criterion_type"] == "BINOMIAL_UPPER"
            else "UNIT_TEST_SYNTHETIC_CALIBRATION_SUMMARY"
        )
    return rows


def _config(
    *,
    familywise_power: float = 0.80,
    design_effect: float = 1.0,
    p1_design_unit: str = "WITHIN_PLANT_PAIRED_FLOWERS",
) -> dict:
    config = {
        "confidence_level": 0.95,
        "familywise_target_power": familywise_power,
        "familywise_target_power_basis": "UNIT_TEST_SYNTHETIC_PLANNING_INPUT",
        "planning_provenance": {
            "status": PLANNING_STATUS,
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "frozen_before_confirmatory_data": True,
            "basis_document": "UNIT_TEST_SYNTHETIC_PLANNING_INPUT",
        },
        "lane_design": {
            lane: {
                "design_effect": design_effect,
                "design_effect_basis": "UNIT_TEST_SYNTHETIC_PLANNING_INPUT",
                "flowers_per_plant_per_cell": 1,
                "flowers_per_plant_per_cell_basis": "UNIT_TEST_SYNTHETIC_PLANNING_INPUT",
            }
            for lane in ("P0", "P1", "G")
        },
    }
    config["lane_design"]["P1"]["design_unit"] = p1_design_unit
    config["lane_design"]["P1"]["design_unit_basis"] = (
        "UNIT_TEST_SYNTHETIC_P1_DESIGN_BASIS"
    )
    return config


def test_cal_c_templates_are_fail_closed_and_cover_25_criteria() -> None:
    rows = _read_criteria(CRITERIA_TEMPLATE)
    assert len(rows) == 25
    assert {row["lane"] for row in rows} == {"P0", "P1", "G"}
    assert sum(row["lane"] == "P0" for row in rows) == 8
    assert sum(row["lane"] == "P1" for row in rows) == 8
    assert sum(row["lane"] == "G" for row in rows) == 9
    assert {row["criterion_type"] for row in rows} == {"NORMAL_BOUND"}
    assert {row["unit_type"] for row in rows} == {"PLANT"}
    assert all(row["boundary"] == "REQUIRED_BEFORE_USE" for row in rows)

    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["confidence_level"] == 0.95
    assert config["familywise_target_power"] == "REQUIRED_BEFORE_USE"
    assert (
        config["lane_design"]["P1"]["design_unit"]
        == "REQUIRED_BEFORE_USE"
    )
    assert "DO_NOT_RUN" in config["status"]

    with pytest.raises(ValueError, match="familywise_target_power"):
        build_plan(rows, config)


def test_normal_bound_known_case_requires_eight_units() -> None:
    assert normal_boundary_required_n(
        pilot_sd=1.0,
        distance_to_boundary=1.0,
        confidence=0.95,
        target_power=0.80,
    ) == 8


def test_zero_event_binomial_upper_bound_needs_35_observations_for_margin_point_one() -> None:
    n, achieved = minimum_binomial_n(
        true_p=0.0,
        boundary=0.10,
        confidence=0.95,
        target_power=0.80,
    )
    assert n == 35
    assert achieved == 1.0


def test_complete_cal_c_plan_populates_all_eight_sample_size_fields() -> None:
    result = build_plan(_criteria(), _config())
    assert result["status"] == "PEDICULARIS_CAL_C_SAMPLE_SIZE_PLAN_READY"
    assert result["familywise_method"] == (
        "union_bound_failure_allocation_no_independence_assumption"
    )
    assert result["familywise_target_power_basis"] == (
        "UNIT_TEST_SYNTHETIC_PLANNING_INPUT"
    )
    assert result["lane_plans"]["P0"]["design_effect_basis"] == (
        "UNIT_TEST_SYNTHETIC_PLANNING_INPUT"
    )
    assert result["p1_design_unit"] == "WITHIN_PLANT_PAIRED_FLOWERS"
    assert result["lane_plans"]["P1"]["design_unit"] == (
        "WITHIN_PLANT_PAIRED_FLOWERS"
    )
    assert result["lane_plans"]["P1"]["design_unit_basis"] == (
        "UNIT_TEST_SYNTHETIC_P1_DESIGN_BASIS"
    )

    gates = result["sample_size_gate_values"]
    assert set(gates) == {
        "stage_p0.min_plants",
        "stage_p0.min_flowers_per_level",
        "pollination_weight.min_plant_units_per_treatment",
        "pollination_weight.min_flowers_per_treatment",
        "method_gate.min_paired_plants",
        "method_gate.min_flowers_per_treatment",
        "predator_weight.min_paired_plants",
        "predator_weight.min_flowers_per_treatment",
    }
    assert all(value >= 2 for value in gates.values())
    assert gates["method_gate.min_paired_plants"] == gates[
        "predator_weight.min_paired_plants"
    ]
    assert gates["method_gate.min_flowers_per_treatment"] == gates[
        "predator_weight.min_flowers_per_treatment"
    ]

    assert result["lane_plans"]["P0"]["n_criteria"] == 8
    assert result["lane_plans"]["P1"]["n_criteria"] == 8
    assert result["lane_plans"]["G"]["n_criteria"] == 9
    assert result["lane_plans"]["P0"][
        "union_bound_per_criterion_target_power"
    ] == pytest.approx(0.975)


def test_higher_familywise_power_cannot_reduce_required_plants() -> None:
    low = build_plan(_criteria(), _config(familywise_power=0.80))
    high = build_plan(_criteria(), _config(familywise_power=0.90))
    for lane in ("P0", "P1", "G"):
        assert high["lane_plans"][lane]["required_plants"] >= low[
            "lane_plans"
        ][lane]["required_plants"]


def test_design_effect_inflates_required_plants() -> None:
    base = build_plan(_criteria(), _config(design_effect=1.0))
    inflated = build_plan(_criteria(), _config(design_effect=1.5))
    for lane in ("P0", "P1", "G"):
        assert inflated["lane_plans"][lane]["required_plants"] >= base[
            "lane_plans"
        ][lane]["required_plants"]


def test_assumed_true_value_must_be_on_success_side_of_boundary() -> None:
    rows = _criteria()
    target = next(row for row in rows if row["criterion_id"] == "P1_POLLEN")
    target["assumed_true_value"] = "-0.1"
    with pytest.raises(ValueError, match="success side"):
        build_plan(rows, _config())


def test_planning_context_must_match_every_criterion() -> None:
    rows = _criteria()
    rows[0]["season_id"] = "S2"
    with pytest.raises(ValueError, match="season_id does not match"):
        build_plan(rows, _config())


def test_cal_c_output_does_not_claim_empirical_validation() -> None:
    result = build_plan(_criteria(), _config())
    payload = str(result)
    assert "PEDICULARIS_Z_MANIPULATION_VALIDATED" not in payload
    assert "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED" not in payload
    assert "PEDICULARIS_PREDATOR_METHOD_VALIDATED" not in payload
    assert "prospective_planning_only" in result["claim_ceiling"]


def test_cal_c_retains_whole_plant_p1_design_unit() -> None:
    result = build_plan(
        _criteria(),
        _config(p1_design_unit="WHOLE_PLANT_RANDOMIZED"),
    )
    assert result["p1_design_unit"] == "WHOLE_PLANT_RANDOMIZED"
    assert result["lane_plans"]["P1"]["design_unit"] == (
        "WHOLE_PLANT_RANDOMIZED"
    )


def test_cal_c_rejects_unregistered_p1_design_unit() -> None:
    with pytest.raises(ValueError, match="design_unit must be"):
        build_plan(
            _criteria(),
            _config(p1_design_unit="MIXED_UNREGISTERED_DESIGN"),
        )

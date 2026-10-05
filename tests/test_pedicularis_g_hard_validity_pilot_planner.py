from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.plan_pedicularis_g_hard_validity_pilot import (
    DEFAULT_CANDIDATES,
    FREEZE_STATUS,
    PLAN_STATUS,
    SCHEMA,
    _read_candidates,
    build,
    minimum_zero_failure_n,
    zero_failure_upper_bound,
)


def _config(max_failure: float = 0.10) -> dict:
    return {
        "schema": SCHEMA,
        "status": FREEZE_STATUS,
        "confidence_level": 0.95,
        "max_acceptable_per_plant_hard_failure_probability": max_failure,
        "planning_basis_note": "UNIT_TEST_PROSPECTIVE_HARD_VALIDITY_TOLERANCE",
        "frozen_before_exploratory_G_data": True,
        "frozen_at_utc": "2026-10-05T00:00:00Z",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
    }


def test_zero_failure_exact_upper_bound_known_values() -> None:
    assert minimum_zero_failure_n(
        max_failure_probability=0.10,
        confidence_level=0.95,
    ) == 29
    assert minimum_zero_failure_n(
        max_failure_probability=0.05,
        confidence_level=0.95,
    ) == 59

    assert zero_failure_upper_bound(29, 0.95) <= 0.10
    assert zero_failure_upper_bound(28, 0.95) > 0.10
    assert zero_failure_upper_bound(59, 0.95) <= 0.05
    assert zero_failure_upper_bound(58, 0.95) > 0.05


def test_planner_applies_same_prospective_hard_validity_n_to_candidates() -> None:
    result = build(_config(0.10), _read_candidates(DEFAULT_CANDIDATES))

    assert result["status"] == PLAN_STATUS
    assert result["minimum_paired_plants_per_tested_candidate"] == 29
    assert result["first_tier_candidate_ids"] == [
        "G_A1_FINE_MESH",
        "G_A2_POROUS_TUBING",
    ]
    assert result["initial_first_tier_total_paired_plant_assignments"] == 58
    assert result["current_three_arm_manifest_compatible"] is True
    assert result["minimum_distinct_plants_for_current_three_arm_manifest"] == 29
    assert result["minimum_total_flowers_for_current_three_arm_manifest"] == 87
    assert result["first_tier_candidate_trials_independent_for_pooling"] is False
    assert (
        "do_not_pool_first_tier_candidate_assignments_as_independent_trials_because_candidates_share_plants_and_sham"
        in result["claim_ceiling"]
    )
    assert result["hard_failure_unit"].startswith(
        "paired-plant candidate application fails if any"
    )
    assert {
        row["minimum_paired_plants_for_zero_failure_screen"]
        for row in result["candidate_plans"]
    } == {29}


def test_stricter_five_percent_failure_tolerance_requires_59_per_candidate() -> None:
    result = build(_config(0.05), _read_candidates(DEFAULT_CANDIDATES))
    assert result["minimum_paired_plants_per_tested_candidate"] == 59
    assert result["initial_first_tier_total_paired_plant_assignments"] == 118
    assert result["minimum_distinct_plants_for_current_three_arm_manifest"] == 59
    assert result["minimum_total_flowers_for_current_three_arm_manifest"] == 177


def test_planner_does_not_select_candidate_or_effect_thresholds() -> None:
    result = build(_config(), _read_candidates(DEFAULT_CANDIDATES))
    assert result["candidate_selected"] is False
    assert result["effect_thresholds_selected"] is False
    assert result["selectivity_thresholds_selected"] is False
    assert "does_not_establish_predator_exclusion_effectiveness" in (
        result["claim_ceiling"]
    )


def test_unfrozen_or_unjustified_plan_fails_closed() -> None:
    config = _config()
    config["status"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="not prospectively frozen"):
        build(config, _read_candidates(DEFAULT_CANDIDATES))

    config = _config()
    config["planning_basis_note"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="planning_basis_note"):
        build(config, _read_candidates(DEFAULT_CANDIDATES))


def test_invalid_failure_probability_fails_closed() -> None:
    with pytest.raises(ValueError, match="max_failure_probability"):
        minimum_zero_failure_n(
            max_failure_probability=0.0,
            confidence_level=0.95,
        )
    with pytest.raises(ValueError, match="max_failure_probability"):
        minimum_zero_failure_n(
            max_failure_probability=1.0,
            confidence_level=0.95,
        )


def test_template_remains_unfrozen() -> None:
    template = json.loads(
        (
            Path(__file__).resolve().parents[1]
            / "empirical"
            / "architecture"
            / "PEDICULARIS_G_HARD_VALIDITY_PLANNING_CONFIG_TEMPLATE_V1.json"
        ).read_text(encoding="utf-8")
    )
    assert template["status"] == "REQUIRED_BEFORE_USE"
    assert template["confidence_level"] == "REQUIRED_BEFORE_USE"
    assert template[
        "max_acceptable_per_plant_hard_failure_probability"
    ] == "REQUIRED_BEFORE_USE"

from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.evaluate_pedicularis_w1_w2_power_envelope import (
    OUTPUT_STATUS,
    _validate_manifest,
    _validate_scenario_set,
    aggregate,
)
from scripts.simulate_pedicularis_w1_w2_power import SENSITIVITY_STATUS


def _manifest() -> dict:
    return {
        "schema": "PEDICULARIS_W1_W2_POWER_ENVELOPE_V1",
        "status": "PEDICULARIS_W1_W2_POWER_ENVELOPE_PROSPECTIVELY_DECLARED",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "envelope_basis_note": "prospective scenario spread test",
        "frozen_before_full_surface_outcomes": True,
        "scenarios": [
            {
                "scenario_id": "A",
                "config_path": "a.json",
                "scenario_role": "lower-effect sensitivity",
                "basis_note": "prospective synthetic test",
            },
            {
                "scenario_id": "B",
                "config_path": "b.json",
                "scenario_role": "higher-variance sensitivity",
                "basis_note": "prospective synthetic test",
            },
        ],
    }


def _config(world: str = "W1") -> dict:
    return {
        "status": SENSITIVITY_STATUS,
        "planning_provenance": {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
        },
        "candidate_plants": [10, 20, 30],
        "field_design": {
            "flowers_per_plant": 4,
            "n_surface_cells": 20,
            "allocation_strategy": (
                "BALANCED_CYCLIC_RANDOMIZED_Z_BY_P_BY_G_V1"
            ),
        },
        "simulation_reps": 200,
        "target_primary_surface_power": 0.8,
        "target_headline_w1_or_w2_power": 0.8,
        "target_truth_world": world,
        "generating_model": {
            "z_levels": [-2, -1, 0, 1, 2],
            "dummy_geometry": world,
        },
        "production_surface_config": {
            "sch_surface": {
                "bootstrap_reps": 200,
                "random_seed": 1,
                "min_z_levels": 5,
                "min_valid_bootstrap_fraction": 0.8,
                "min_interior_bootstrap_fraction": 0.8,
                "min_optimum_separation": 0.5,
                "min_optimum_shift": 0.2,
                "min_abs_component_gradient": 0.2,
            },
            "system_checks": {
                "max_water_depth_range": 0.0,
                "max_mechanical_damage_rate": 0.0,
            },
        },
        "secondary_diagnostic_config": {
            "bootstrap_reps": 200,
            "random_seed": 2,
        },
    }


def _result(primary: list[float], headline: list[float]) -> dict:
    return {
        "target_primary_surface_power": 0.8,
        "target_headline_w1_or_w2_power": 0.8,
        "candidate_results": [
            {
                "plants": n,
                "primary_surface_power": p,
                "headline_W1_or_W2_power": h,
                "target_truth_world_power": min(p, h),
            }
            for n, p, h in zip(
                [10, 20, 30],
                primary,
                headline,
                strict=True,
            )
        ],
    }


def _basis() -> dict:
    return {
        "registered_power_status": "PEDICULARIS_W1_W2_POWER_BASIS_BLOCKED",
        "n_blocking_rows": 21,
    }


def _validation(configs: dict[str, dict]) -> dict:
    return _validate_scenario_set(
        _manifest(),
        _validate_manifest(_manifest()),
        configs,
    )


def test_envelope_uses_worst_case_not_average_power() -> None:
    configs = {"A": _config("W1"), "B": _config("W2")}
    validation = _validation(configs)

    result = aggregate(
        manifest=_manifest(),
        scenario_entries=_validate_manifest(_manifest()),
        scenario_results={
            "A": _result(
                [0.70, 0.85, 0.92],
                [0.60, 0.82, 0.91],
            ),
            "B": _result(
                [0.65, 0.79, 0.86],
                [0.55, 0.75, 0.83],
            ),
        },
        validation=validation,
        basis_receipt=_basis(),
    )

    assert result["status"] == OUTPUT_STATUS
    assert result["scenario_minimum_candidate_plants"] == {
        "A": 20,
        "B": 30,
    }
    assert result["scenario_minimum_candidate_range"] == [20, 30]
    assert result["geometry_uncertainty_changes_minimum_candidate"] is True
    assert result["minimum_candidate_meeting_targets_in_every_scenario"] == 30
    assert result["registered_n_promoted"] is False
    assert result["registered_field_allocation_authorized"] is False

    n20 = next(
        row for row in result["candidate_envelope"]
        if row["plants"] == 20
    )
    assert n20["worst_case_primary_surface_power"] == 0.79
    assert n20["worst_case_headline_W1_or_W2_power"] == 0.75
    assert n20["meets_targets_in_every_scenario"] is False


def test_envelope_reports_candidate_grid_too_small_without_promoting_n() -> None:
    configs = {"A": _config(), "B": _config()}
    result = aggregate(
        manifest=_manifest(),
        scenario_entries=_validate_manifest(_manifest()),
        scenario_results={
            "A": _result(
                [0.70, 0.85, 0.92],
                [0.60, 0.82, 0.91],
            ),
            "B": _result(
                [0.40, 0.55, 0.70],
                [0.30, 0.50, 0.75],
            ),
        },
        validation=_validation(configs),
        basis_receipt=_basis(),
    )

    assert result["some_scenario_exceeds_candidate_grid"] is True
    assert result["all_scenarios_have_candidate_meeting_targets"] is False
    assert result["minimum_candidate_meeting_targets_in_every_scenario"] is None
    assert result["registered_n_promoted"] is False


def test_same_minimum_across_scenarios_is_reported_without_overclaim() -> None:
    configs = {"A": _config(), "B": _config()}
    result = aggregate(
        manifest=_manifest(),
        scenario_entries=_validate_manifest(_manifest()),
        scenario_results={
            "A": _result(
                [0.70, 0.85, 0.92],
                [0.60, 0.82, 0.91],
            ),
            "B": _result(
                [0.65, 0.84, 0.90],
                [0.50, 0.81, 0.88],
            ),
        },
        validation=_validation(configs),
        basis_receipt=_basis(),
    )

    assert result["scenario_minimum_candidate_plants"] == {
        "A": 20,
        "B": 20,
    }
    assert result["all_scenarios_same_minimum_candidate"] is True
    assert result["geometry_uncertainty_changes_minimum_candidate"] is False
    assert result["minimum_candidate_meeting_targets_in_every_scenario"] == 20
    assert result["registered_n_promoted"] is False


def test_envelope_requires_two_unique_scenarios() -> None:
    manifest = _manifest()
    manifest["scenarios"] = manifest["scenarios"][:1]
    with pytest.raises(ValueError, match="at least two"):
        _validate_manifest(manifest)

    manifest = _manifest()
    manifest["scenarios"][1]["scenario_id"] = "A"
    with pytest.raises(ValueError, match="scenario_id must be unique"):
        _validate_manifest(manifest)


def test_scenarios_must_share_field_design_and_analysis_signature() -> None:
    configs = {"A": _config(), "B": _config()}
    configs["B"] = deepcopy(configs["B"])
    configs["B"]["field_design"]["flowers_per_plant"] = 5

    with pytest.raises(ValueError, match="share one design/analysis signature"):
        _validation(configs)


def test_truth_world_may_vary_between_w1_and_w2() -> None:
    configs = {"A": _config("W1"), "B": _config("W2")}
    validation = _validation(configs)

    assert validation["truth_worlds"] == {"A": "W1", "B": "W2"}


def test_scenario_configs_must_be_sensitivity_only() -> None:
    configs = {"A": _config(), "B": _config()}
    configs["B"]["status"] = "PEDICULARIS_W1_W2_POWER_INPUTS_PROSPECTIVELY_FROZEN"

    with pytest.raises(ValueError, match="SENSITIVITY_SCENARIO_ONLY"):
        _validation(configs)

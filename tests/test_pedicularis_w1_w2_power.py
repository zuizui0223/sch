from __future__ import annotations

import json
import random
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.simulate_pedicularis_w1_w2_power import (
    FROZEN_STATUS,
    TEST_STATUS,
    _validate_config,
    generate_rows,
    simulate_power,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_W1_W2_POWER_CONFIG_TEMPLATE_V1.json"
)


def _config() -> dict:
    return {
        "schema": "PEDICULARIS_W1_W2_POWER_CONFIG_V1",
        "status": TEST_STATUS,
        "planning_provenance": {
            "population_id": "P_REX_POWER_TEST",
            "season_id": "S1",
            "basis_document": "SYNTHETIC_TEST_ONLY",
            "frozen_before_full_surface_data": True,
        },
        "candidate_complete_block_plants": [6],
        "simulation_reps": 1,
        "simulation_seed": 17,
        "target_primary_surface_power": 0.8,
        "target_headline_w1_or_w2_power": 0.8,
        "target_truth_world": "W1",
        "generating_model": {
            "z_levels": [-2, -1, 0, 1, 2],
            "ovule_count": 100,
            "fitness_between_plant_sd": 0.0,
            "fitness_residual_sd": 0.0,
            "realized_z_sd": 0.0,
            "state_fitness_surfaces": {
                "P0G0": {"peak": 50.0, "optimum": 0.0, "curvature": 0.1},
                "P1G0": {"peak": 70.0, "optimum": 1.5, "curvature": 2.0},
                "P0G1": {"peak": 65.0, "optimum": -1.5, "curvature": 2.0},
                "P1G1": {"peak": 60.0, "optimum": 0.0, "curvature": 2.0},
            },
            "pollen_between_plant_sd": 0.0,
            "pollen_residual_sd": 0.0,
            "pollen_state_models": {
                "P0G0": {"intercept": 40.0, "z_slope": 0.0},
                "P1G0": {"intercept": 50.0, "z_slope": 5.0},
                "P0G1": {"intercept": 40.0, "z_slope": 0.0},
                "P1G1": {"intercept": 50.0, "z_slope": 5.0},
            },
            "initial_seed_between_plant_sd_fraction": 0.0,
            "initial_seed_residual_sd_fraction": 0.0,
            "initial_seed_state_models": {
                "P0G0": {
                    "intercept_fraction": 0.85,
                    "z_slope_fraction": 0.0,
                },
                "P1G0": {
                    "intercept_fraction": 0.85,
                    "z_slope_fraction": 0.03,
                },
                "P0G1": {
                    "intercept_fraction": 0.85,
                    "z_slope_fraction": 0.0,
                },
                "P1G1": {
                    "intercept_fraction": 0.85,
                    "z_slope_fraction": 0.03,
                },
            },
            "early_attack_rate_excluded": 0.0,
            "early_attack_rate_exposed": 0.5,
            "water_depth": 1.0,
        },
        "production_surface_config": {
            "sch_surface": {
                "bootstrap_reps": 200,
                "random_seed": 19,
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
            "random_seed": 23,
        },
    }


def test_template_is_fail_closed() -> None:
    config = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="not prospectively frozen"):
        _validate_config(config)


def test_strong_w1_truth_runs_current_production_pipeline() -> None:
    result = simulate_power(_config())
    candidate = result["candidate_results"][0]

    assert result["target_truth_world"] == "W1"
    assert result["generating_truth_descriptor"]["target_truth_world"] == "W1"
    assert all(
        result["generating_truth_descriptor"]["primary_truth_checks"].values()
    )
    assert candidate["primary_surface_power"] == 1.0
    assert candidate["headline_W1_or_W2_power"] == 1.0
    assert candidate["strongest_W1_power"] == 1.0
    assert candidate["target_truth_world_power"] == 1.0
    assert candidate["world_probabilities"]["W1"] == 1.0
    assert result["minimum_complete_block_plants_meeting_both_targets"] == 6
    assert result["minimum_total_full_surface_flowers_meeting_both_targets"] == 120


def test_w2_truth_rejects_hidden_w1_initial_seed_model() -> None:
    config = _config()
    config["target_truth_world"] = "W2"

    with pytest.raises(ValueError, match="W2 truth requires"):
        _validate_config(config)


def test_primary_truth_below_shift_gate_is_rejected_before_simulation() -> None:
    config = _config()
    config["generating_model"]["state_fitness_surfaces"]["P1G1"]["optimum"] = 1.4

    with pytest.raises(ValueError, match="primary-success side"):
        _validate_config(config)


def test_realized_z_uncertainty_is_used_by_generator() -> None:
    config = _config()
    config["generating_model"]["realized_z_sd"] = 0.25
    frozen = _validate_config(config)

    rows, diagnostics = generate_rows(
        frozen["generating_model"],
        3,
        random.Random(7),
        population_id="P_REX_POWER_TEST",
        season_id="S1",
    )

    assert diagnostics["n_plants"] == 3
    assert diagnostics["flowers_per_plant"] == 20
    nominal = {-2.0, -1.0, 0.0, 1.0, 2.0}
    realized = {float(row["realized_exsertion"]) for row in rows}
    assert not realized.issubset(nominal)


def test_frozen_prospective_plan_requires_many_monte_carlo_reps() -> None:
    config = _config()
    config["status"] = FROZEN_STATUS
    config["simulation_reps"] = 199

    with pytest.raises(ValueError, match="requires >=200 reps"):
        _validate_config(config)


def test_w1_truth_requires_positive_pollen_slope_in_both_g_states() -> None:
    config = deepcopy(_config())
    config["generating_model"]["pollen_state_models"]["P1G1"]["z_slope"] = 0.0

    with pytest.raises(ValueError, match="positive z->pollen slopes"):
        _validate_config(config)

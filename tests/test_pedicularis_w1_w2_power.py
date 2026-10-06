from __future__ import annotations

import json
import random
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.simulate_pedicularis_w1_w2_power import (
    FROZEN_STATUS,
    SENSITIVITY_STATUS,
    TEST_STATUS,
    _validate_basis_receipt,
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
        "candidate_plants": [6],
        "field_design": {
            "flowers_per_plant": 20,
            "allocation_strategy": "BALANCED_CYCLIC_RANDOMIZED_Z_BY_P_BY_G_V1",
        },
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
    assert result["minimum_plants_meeting_both_targets"] == 6
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
        flowers_per_plant=20,
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


def test_balanced_incomplete_block_generator_equalizes_all_twenty_cells() -> None:
    config = _config()
    config["candidate_plants"] = [10]
    config["field_design"]["flowers_per_plant"] = 4
    frozen = _validate_config(config)

    rows, diagnostics = generate_rows(
        frozen["generating_model"],
        10,
        random.Random(13),
        flowers_per_plant=4,
        population_id="P_REX_POWER_TEST",
        season_id="S1",
    )

    assert len(rows) == 40
    assert diagnostics["flowers_per_plant"] == 4
    assert diagnostics["replicates_per_cell"] == 2
    assert diagnostics["exact_cell_balance"] is True
    assert set(diagnostics["cell_counts"].values()) == {2}
    assert all(
        len([row for row in rows if row["plant_id"] == f"P{i:04d}"]) == 4
        for i in range(10)
    )


def test_unbalanced_candidate_design_is_rejected_before_power() -> None:
    config = _config()
    config["candidate_plants"] = [7]
    config["field_design"]["flowers_per_plant"] = 4

    with pytest.raises(ValueError, match="divisible.*number of z x P x G cells"):
        _validate_config(config)


def test_six_z_levels_use_twenty_four_cells_not_hardcoded_twenty() -> None:
    config = _config()
    config["generating_model"]["z_levels"] = [-2, -1, 0, 1, 2, 3]
    config["candidate_plants"] = [8]
    config["field_design"]["flowers_per_plant"] = 6
    frozen = _validate_config(config)

    rows, diagnostics = generate_rows(
        frozen["generating_model"],
        8,
        random.Random(29),
        flowers_per_plant=6,
        population_id="P_REX_POWER_TEST",
        season_id="S1",
    )

    assert len(rows) == 48
    assert diagnostics["n_surface_cells"] == 24
    assert diagnostics["replicates_per_cell"] == 2
    assert diagnostics["exact_cell_balance"] is True
    assert set(diagnostics["cell_counts"].values()) == {2}


def _blocked_basis() -> dict:
    return {
        "analysis": "pedicularis_w1_w2_power_basis_audit_v1",
        "registered_power_status": "PEDICULARIS_W1_W2_POWER_BASIS_BLOCKED",
        "registered_single_scenario_n_basis_ready": False,
        "n_blocking_rows": 21,
    }


def _ready_basis() -> dict:
    return {
        "analysis": "pedicularis_w1_w2_power_basis_audit_v1",
        "registered_power_status": (
            "PEDICULARIS_W1_W2_POWER_BASIS_READY_FOR_REGISTERED_N"
        ),
        "registered_single_scenario_n_basis_ready": True,
        "n_blocking_rows": 0,
    }


def test_registered_power_rejects_blocked_basis_receipt() -> None:
    with pytest.raises(ValueError, match="blocked until"):
        _validate_basis_receipt(
            _blocked_basis(),
            status=FROZEN_STATUS,
        )


def test_registered_power_accepts_only_zero_blocker_ready_basis() -> None:
    result = _validate_basis_receipt(
        _ready_basis(),
        status=FROZEN_STATUS,
    )
    assert result is not None
    assert result["n_blocking_rows"] == 0


def test_sensitivity_run_with_blocked_basis_cannot_emit_registered_n() -> None:
    config = _config()
    config["status"] = SENSITIVITY_STATUS

    result = simulate_power(
        config,
        basis_receipt=_blocked_basis(),
    )

    assert result["status"] == "PEDICULARIS_W1_W2_POWER_SENSITIVITY_ONLY"
    assert result["basis_blocker_count"] == 21
    assert result["minimum_plants_meeting_both_targets"] is None
    assert result[
        "minimum_total_full_surface_flowers_meeting_both_targets"
    ] is None
    assert result["registered_field_allocation_recommendation_allowed"] is False


def test_non_test_power_run_requires_basis_receipt() -> None:
    config = _config()
    config["status"] = SENSITIVITY_STATUS

    with pytest.raises(ValueError, match="requires a power-basis audit receipt"):
        simulate_power(config)

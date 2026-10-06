from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.bind_pedicularis_w1_w2_geometry_config import (
    BINDING_STATUS,
    _semantic_sha256,
    build as bind_geometry,
)
from scripts.simulate_pedicularis_w1_w2_power import (
    FROZEN_STATUS,
    SENSITIVITY_STATUS,
    _validate_geometry_binding,
    simulate_power,
)


def _base_config() -> dict:
    return {
        "schema": "PEDICULARIS_W1_W2_POWER_CONFIG_V1",
        "status": "SYNTHETIC_TEST_ONLY",
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
            "fitness_between_plant_sd": 2.0,
            "fitness_residual_sd": 3.0,
            "realized_z_sd": 0.1,
            "state_fitness_surfaces": {
                "P0G0": {"peak": 50.0, "optimum": 0.0, "curvature": 0.1},
                "P1G0": {"peak": 70.0, "optimum": 1.5, "curvature": 2.0},
                "P0G1": {"peak": 65.0, "optimum": -1.5, "curvature": 2.0},
                "P1G1": {"peak": 60.0, "optimum": 0.0, "curvature": 2.0},
            },
            "pollen_between_plant_sd": 2.0,
            "pollen_residual_sd": 3.0,
            "pollen_state_models": {
                "P0G0": {"intercept": 40.0, "z_slope": 0.0},
                "P1G0": {"intercept": 50.0, "z_slope": 5.0},
                "P0G1": {"intercept": 40.0, "z_slope": 0.0},
                "P1G1": {"intercept": 50.0, "z_slope": 5.0},
            },
            "initial_seed_between_plant_sd_fraction": 0.02,
            "initial_seed_residual_sd_fraction": 0.03,
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


def _frozen_config() -> dict:
    config = _base_config()
    config["status"] = FROZEN_STATUS
    config["simulation_reps"] = 200
    config["planning_provenance"]["basis_document"] = (
        "PRECISION_QUALIFIED_GEOMETRY_BINDING_TEST"
    )
    return config


def _ready_basis() -> dict:
    return {
        "analysis": "pedicularis_w1_w2_power_basis_audit_v1",
        "population_id": "P_REX_POWER_TEST",
        "season_id": "S1",
        "registered_power_status": (
            "PEDICULARIS_W1_W2_POWER_BASIS_READY_FOR_REGISTERED_N"
        ),
        "registered_single_scenario_n_basis_ready": True,
        "n_blocking_rows": 0,
    }


def _geometry_summary(config: dict) -> dict:
    model = config["generating_model"]
    values = {
        "generating_model.fitness_between_plant_sd": model[
            "fitness_between_plant_sd"
        ],
        "generating_model.fitness_residual_sd": model["fitness_residual_sd"],
        "generating_model.pollen_between_plant_sd": model[
            "pollen_between_plant_sd"
        ],
        "generating_model.pollen_residual_sd": model["pollen_residual_sd"],
        "generating_model.initial_seed_between_plant_sd_fraction": model[
            "initial_seed_between_plant_sd_fraction"
        ],
        "generating_model.initial_seed_residual_sd_fraction": model[
            "initial_seed_residual_sd_fraction"
        ],
    }
    for state in ("P0G0", "P1G0", "P0G1", "P1G1"):
        values[f"generating_model.state_fitness_surfaces.{state}"] = deepcopy(
            model["state_fitness_surfaces"][state]
        )
        values[f"generating_model.pollen_state_models.{state}"] = deepcopy(
            model["pollen_state_models"][state]
        )
        values[
            f"generating_model.initial_seed_state_models.{state}"
        ] = deepcopy(model["initial_seed_state_models"][state])

    assert len(values) == 18
    return {
        "receipt_schema": "PEDICULARIS_P2_GEOMETRY_PILOT_SUMMARY_V1",
        "status": (
            "PEDICULARIS_P2_GEOMETRY_PILOT_POINT_ESTIMATES_READY_"
            "NOT_YET_PRECISION_QUALIFIED"
        ),
        "geometry_and_variance_point_estimates_complete": True,
        "n_power_basis_paths_resolved": 18,
        "population_id": config["planning_provenance"]["population_id"],
        "season_id": config["planning_provenance"]["season_id"],
        "pilot_data_sha256": "d" * 64,
        "pilot_config_sha256": "c" * 64,
        "resolved_power_basis_values": values,
    }


def _precision(summary: dict, *, ready: bool = True) -> dict:
    paths = summary["resolved_power_basis_values"]
    return {
        "receipt_schema": "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_V1",
        "status": (
            "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_READY_FOR_BASIS"
            if ready
            else "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_INSUFFICIENT_FOR_BASIS"
        ),
        "population_id": summary["population_id"],
        "season_id": summary["season_id"],
        "geometry_summary_sha256": _semantic_sha256(summary),
        "pilot_data_sha256": summary["pilot_data_sha256"],
        "pilot_config_sha256": summary["pilot_config_sha256"],
        "basis_materialization_authorized": ready,
        "all_18_path_precision_gate_passed": ready,
        "n_power_basis_paths_precision_evaluated": 18,
        "normalized_95ci_width_by_power_basis_path": {
            path: 0.10 for path in paths
        },
    }


def test_binding_certifies_precision_qualified_eighteen_paths() -> None:
    config = _frozen_config()
    basis = _ready_basis()
    summary = _geometry_summary(config)
    precision = _precision(summary)

    binding = bind_geometry(config, summary, precision, basis)

    assert binding["status"] == BINDING_STATUS
    assert binding["geometry_precision_qualified"] is True
    assert binding["n_geometry_variance_paths_bound"] == 18
    assert binding["all_geometry_variance_paths_match"] is True
    assert all(
        row["matches_geometry_summary"] for row in binding["path_checks"]
    )
    assert all(
        row["normalized_precision_width"] == pytest.approx(0.10)
        for row in binding["path_checks"]
    )


def test_binding_rejects_geometry_value_drift() -> None:
    config = _frozen_config()
    summary = _geometry_summary(config)
    precision = _precision(summary)
    config["generating_model"]["state_fitness_surfaces"]["P1G1"][
        "curvature"
    ] += 0.1

    with pytest.raises(ValueError, match="drift from geometry summary"):
        bind_geometry(config, summary, precision, _ready_basis())


def test_binding_rejects_nonready_precision() -> None:
    config = _frozen_config()
    summary = _geometry_summary(config)

    with pytest.raises(ValueError, match="precision receipt is not ready"):
        bind_geometry(
            config,
            summary,
            _precision(summary, ready=False),
            _ready_basis(),
        )


def test_binding_rejects_precision_from_different_summary() -> None:
    config = _frozen_config()
    summary = _geometry_summary(config)
    precision = _precision(summary)
    changed = deepcopy(summary)
    changed["pilot_data_sha256"] = "e" * 64

    with pytest.raises(ValueError, match="not bound to this summary"):
        bind_geometry(config, changed, precision, _ready_basis())


def test_registered_power_rejects_missing_geometry_binding_before_simulation() -> None:
    config = _frozen_config()

    with pytest.raises(
        ValueError,
        match="requires an exact precision-qualified geometry-config binding",
    ):
        simulate_power(
            config,
            basis_receipt=_ready_basis(),
        )


def test_registered_binding_detects_config_edit_after_binding() -> None:
    config = _frozen_config()
    basis = _ready_basis()
    summary = _geometry_summary(config)
    binding = bind_geometry(config, summary, _precision(summary), basis)

    changed = deepcopy(config)
    changed["candidate_plants"] = [10]

    with pytest.raises(ValueError, match="power config has changed"):
        _validate_geometry_binding(changed, basis, binding)


def test_registered_binding_detects_basis_edit_after_binding() -> None:
    config = _frozen_config()
    basis = _ready_basis()
    summary = _geometry_summary(config)
    binding = bind_geometry(config, summary, _precision(summary), basis)

    changed_basis = deepcopy(basis)
    changed_basis["extra_note"] = "post-binding edit"

    with pytest.raises(ValueError, match="power-basis receipt has changed"):
        _validate_geometry_binding(config, changed_basis, binding)


def test_sensitivity_run_does_not_require_geometry_binding() -> None:
    config = _frozen_config()
    config["status"] = SENSITIVITY_STATUS
    config["simulation_reps"] = 1

    result = _validate_geometry_binding(
        config,
        {"anything": "allowed because sensitivity only"},
        None,
    )
    assert result is None

import json
from pathlib import Path

import pytest

from scripts.simulate_pedicularis_experiment_a_power import generate_rows, simulate_power


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_EXPERIMENT_A_POWER_CONFIG_TEMPLATE_V1.json"


def _config() -> dict:
    return {
        "status": "FROZEN_SYNTHETIC_TEST_ONLY",
        "candidate_plants_per_cell": [6],
        "simulation_reps": 1,
        "simulation_seed": 17,
        "target_joint_power": 0.8,
        "generating_model": {
            "z_levels": [-2, -1, 0, 1, 2],
            "baseline_fitness": 80.0,
            "pollination_peak": 20.0,
            "pollination_optimum": 1.5,
            "pollination_curvature": 2.0,
            "antagonist_peak": 20.0,
            "antagonist_optimum": -1.5,
            "antagonist_curvature": 2.0,
            "between_plant_sd": 0.0,
            "residual_sd": 0.0,
            "ovule_count": 200.0,
            "water_depth_mean": 10.0,
            "water_depth_sd": 0.0,
            "mechanical_damage_rate": 0.0,
            "predator_attack_rate_exposed": 0.5,
            "predator_attack_rate_excluded": 0.0
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
                "min_abs_component_gradient": 0.2
            },
            "system_checks": {
                "max_water_depth_range": 0.01,
                "max_mechanical_damage_rate": 0.01
            }
        },
        "production_conflict_budget_config": {
            "fitness_scale_id": "SIM_INTACT_SEEDS",
            "min_z_levels": 5,
            "bootstrap_reps": 200,
            "random_seed": 23,
            "min_valid_bootstrap_fraction": 0.8
        }
    }


def test_template_is_fail_closed() -> None:
    config = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    assert "DO_NOT_RUN" in config["status"]
    assert config["candidate_plants_per_cell"] == "REQUIRED_BEFORE_USE"


def test_generator_preserves_twenty_cell_complete_block() -> None:
    import random

    config = _config()
    rows = generate_rows(config["generating_model"], 3, random.Random(1))
    assert len(rows) == 3 * 5 * 2 * 2
    assert len({row["plant_id"] for row in rows}) == 3
    assert {row["pollination_treatment"] for row in rows} == {"NATURAL", "SUPPLEMENTED"}
    assert {row["predator_treatment"] for row in rows} == {"EXPOSED", "EXCLUDED"}


def test_strong_synthetic_conflict_passes_joint_production_pipeline() -> None:
    result = simulate_power(_config())
    row = result["candidate_results"][0]
    assert row["surface_gate_power"] == 1.0
    assert row["positive_conflict_budget_power"] == 1.0
    assert row["joint_primary_gate_power"] == 1.0
    assert result["minimum_candidate_meeting_target"] == 6


def test_unfrozen_template_is_rejected() -> None:
    config = json.loads(TEMPLATE.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="fully frozen"):
        simulate_power(config)

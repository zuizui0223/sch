import random

from scripts.extract_pedicularis_experiment_a_pilot_parameters import extract
from scripts.simulate_pedicularis_experiment_a_power import generate_rows


def _model() -> dict:
    return {
        "z_levels": [-2, -1, 0, 1, 2],
        "baseline_fitness": 80.0,
        "pollination_peak": 20.0,
        "pollination_optimum": 1.5,
        "pollination_curvature": 2.0,
        "antagonist_peak": 20.0,
        "antagonist_optimum": -1.5,
        "antagonist_curvature": 2.0,
        "between_plant_sd": 2.0,
        "residual_sd": 3.0,
        "ovule_count": 200.0,
        "water_depth_mean": 10.0,
        "water_depth_sd": 0.2,
        "mechanical_damage_rate": 0.0,
        "predator_attack_rate_exposed": 0.6,
        "predator_attack_rate_excluded": 0.1,
    }


def test_pilot_receipt_is_descriptive_and_power_only() -> None:
    rows = generate_rows(_model(), 8, random.Random(7))
    result = extract(rows)
    assert result["receipt_schema_version"] == "PEDICULARIS_EXPERIMENT_A_PILOT_PARAMETERS_V1"
    assert result["status"] == "DESCRIPTIVE_PILOT_ONLY_NOT_BIOLOGICAL_TEST"
    assert result["n_plants"] == 8
    assert len(result["realized_z_by_assigned_level"]) == 5
    assert result["pooled_within_cell_fitness_variance"] > 0
    assert result["power_config_draft"]["residual_sd"] > 0
    assert result["power_config_draft"]["effect_geometry_status"].startswith("REQUIRES_")
    assert "do not test SCH biology" in result["claim_ceiling"]


def test_residualized_cluster_component_is_available_for_complete_block() -> None:
    rows = generate_rows(_model(), 8, random.Random(11))
    result = extract(rows)
    components = result["residualized_cluster_components"]
    assert components["balanced_cluster_estimate_available"] is True
    assert components["rows_per_plant"] == 20
    assert components["between_plant_variance_component"] is not None
    assert components["within_plant_residual_variance"] is not None

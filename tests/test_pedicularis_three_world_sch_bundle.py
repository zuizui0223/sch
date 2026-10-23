from __future__ import annotations

import pytest

from scripts.validate_pedicularis_three_world_sch_bundle import bundle


def _surface(population: str = "POP_A", season: str = "2027") -> dict:
    return {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "system_wrapper_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2",
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
        "system": "Pedicularis rex",
        "population_id": population,
        "season_id": season,
        "pedicularis_state_mapping": {
            "G0": "SEED_PREDATOR_INDEPENDENTLY_EXCLUDED",
            "G1": "SEED_PREDATOR_EXPOSED",
            "water_y": "HELD_FIXED_ACROSS_ALL_SCH_CELLS",
        },
        "readiness_reference": {
            "predator_method_requirement": "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED",
        },
        "optimum_semantics": {
            "z_pollinator_context": "STATE_SPECIFIC_P1G0_REPRODUCTIVE_OPTIMUM_NOT_AUTOMATICALLY_PURE_F1",
            "z_antagonist_context": "STATE_SPECIFIC_P0G1_REPRODUCTIVE_OPTIMUM_NOT_AUTOMATICALLY_PURE_F2",
            "z_combined": "STATE_SPECIFIC_P1G1_COMBINED_REPRODUCTIVE_OPTIMUM",
        },
        "observed_estimands": {
            "z_pollinator_context": 2.0,
            "z_antagonist_context": -2.0,
            "z_combined": 0.0,
        },
    }


def _conflict(population: str = "POP_A", season: str = "2027") -> dict:
    return {
        "receipt_schema_version": "THREE_WORLD_CONFLICT_HANDOFF_V1",
        "status": "THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED",
        "context_id": "PEDICULARIS_POP_A_2027",
        "system": "Pedicularis rex",
        "population_id": population,
        "season_id": season,
        "fitness_scale_id": "UNDAMAGED_SEEDS_PER_FOCAL_FLOWER",
        "conflict_load": {"point": 0.4, "lower_95": 0.3, "upper_95": 0.5},
    }


def test_bundle_freezes_state_reference_and_conflict_in_one_context() -> None:
    out = bundle(_surface(), _conflict())
    assert out["receipt_schema_version"] == "PEDICULARIS_THREE_WORLD_SCH_BUNDLE_V1"
    assert out["status"] == "PEDICULARIS_SCH_EXPERIMENT_A_BUNDLED"
    assert out["context_id"] == "PEDICULARIS_POP_A_2027"
    assert out["state_optima"]["z_P_star"] == 2.0
    assert out["state_optima"]["z_G_star"] == -2.0
    assert out["state_optima"]["z_C_star"] == 0.0
    assert out["conflict_load"]["lower_95"] > 0
    assert all(out["experiment_A_guards"].values())


def test_population_or_season_mismatch_fails_closed() -> None:
    with pytest.raises(ValueError, match="population and season"):
        bundle(_surface(season="2028"), _conflict())


def test_legacy_water_as_G_surface_is_rejected() -> None:
    surface = _surface()
    surface["pedicularis_state_mapping"]["G0"] = "WATER_PROTECTED"
    with pytest.raises(ValueError, match="independent seed-predator"):
        bundle(surface, _conflict())


def test_water_y_must_be_fixed_during_experiment_A() -> None:
    surface = _surface()
    surface["pedicularis_state_mapping"]["water_y"] = "VARIED"
    with pytest.raises(ValueError, match="water-y"):
        bundle(surface, _conflict())

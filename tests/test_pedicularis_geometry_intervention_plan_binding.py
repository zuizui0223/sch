from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.bind_pedicularis_geometry_intervention_plan import build
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.pedicularis_config_freeze import (
    FREEZE_SCHEMA,
    FREEZE_STATUS,
    required_gate_paths,
)


POP = "P_REX_TEST"
SEASON = "S1"


def _freeze(lane: str) -> dict:
    return {
        "schema": FREEZE_SCHEMA,
        "status": FREEZE_STATUS,
        "lane": lane,
        "population_id": POP,
        "season_id": SEASON,
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-10-07T00:00:00+00:00",
        "basis_document": "UNIT_TEST_SYNTHETIC_ONLY",
        "threshold_basis": {
            path: "UNIT_TEST_SYNTHETIC_ONLY"
            for path in required_gate_paths(lane)
        },
    }


def _p0() -> dict:
    return {
        "status": "PEDICULARIS_P0_FIELD_CONFIG_FROZEN",
        "prospective_freeze": _freeze("P0"),
        "bootstrap_reps": 300,
        "random_seed": 1,
        "stage_p0": {
            "min_z_levels": 5,
            "min_flowers_per_level": 5,
            "min_plants": 5,
            "min_adjacent_exsertion_gap": 0.1,
            "max_opening_width_relative_change": 0.1,
            "max_tube_diameter_relative_change": 0.1,
            "max_bract_height_relative_change": 0.1,
            "max_lower_lip_angle_change_deg": 5.0,
            "max_water_depth_change": 1.0,
            "max_flower_orientation_change_deg": 5.0,
            "max_mechanical_damage_rate": 0.1,
        },
    }


def _p1() -> dict:
    return {
        "status": "PEDICULARIS_P1_FIELD_CONFIG_FROZEN",
        "prospective_freeze": _freeze("P1"),
        "bootstrap_reps": 300,
        "random_seed": 2,
        "pollination_weight": {
            "experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
            "min_paired_plants": 5,
            "min_flowers_per_treatment": 5,
            "min_pollen_grain_delta": 1.0,
            "min_initial_seed_set_delta": 0.01,
            "max_early_predator_attack_difference": 0.1,
            "max_z_relative_change": 0.1,
            "max_bract_height_relative_change": 0.1,
            "max_opening_width_relative_change": 0.1,
            "max_water_depth_change": 1.0,
            "max_mechanical_damage_rate": 0.1,
        },
    }


def _g() -> dict:
    return {
        "status": "PEDICULARIS_G_FIELD_CONFIG_FROZEN",
        "prospective_freeze": _freeze("G"),
        "bootstrap_reps": 300,
        "random_seed": 3,
        "method_gate": {
            "min_paired_plants": 5,
            "min_flowers_per_treatment": 5,
            "min_hours_after_anthesis_before_barrier": 6.0,
            "max_hours_after_anthesis_before_barrier": 30.0,
            "require_pollination_window_complete": True,
            "require_ovary_not_swollen": True,
            "require_barrier_not_cover_pollinator_entry": True,
            "require_sham_on_exposed": True,
        },
        "predator_weight": {
            "min_paired_plants": 5,
            "min_flowers_per_treatment": 5,
            "min_early_attack_reduction": 0.1,
            "min_predation_fraction_reduction": 0.1,
            "min_final_seed_set_gain": 0.1,
            "max_initial_seed_set_difference": 0.1,
            "max_pollen_grain_relative_change": 0.1,
            "max_pollinator_visit_relative_change": 0.1,
            "max_z_relative_change": 0.1,
            "max_water_depth_change": 1.0,
            "max_damage_rate_difference": 0.1,
        },
    }


def _levels() -> list[dict[str, str]]:
    return [
        {
            "assigned_z_level": f"Z{i}",
            "assigned_z_rank": str(i),
            "sham_control": "1" if i == 4 else "0",
        }
        for i in range(5)
    ]


def _geometry() -> dict:
    return {
        "schema": "PEDICULARIS_P2_GEOMETRY_PILOT_CONFIG_V1",
        "status": "PEDICULARIS_P2_GEOMETRY_PILOT_PROSPECTIVELY_FROZEN",
        "population_id": POP,
        "season_id": SEASON,
        "planned_n_plants": 10,
        "candidate_cumulative_plants": [5, 10],
        "flowers_per_plant": 4,
        "z_levels": [
            {
                "assigned_z_level": f"Z{i}",
                "assigned_z_rank": i,
                "target_exsertion": float(i),
            }
            for i in range(5)
        ],
        "excluded_method_code": "FINE_MESH_LOWER_FRUIT_SLEEVE",
        "exposed_method_code": "SHAM_SLEEVE",
        "allocation_strategy": "BALANCED_CYCLIC_RANDOMIZED_Z_BY_P_BY_G_V1",
        "frozen_before_geometry_outcomes": True,
        "pilot_role": "POWER_BASIS_ONLY_NEVER_CONFIRMATORY",
        "precision_gate": {
            "bootstrap_reps": 200,
            "random_seed": 31,
            "min_valid_bootstrap_fraction": 0.8,
            "min_interior_concave_fraction_per_state": 0.8,
            "max_normalized_95ci_width_per_power_basis_path": 0.5,
        },
    }


def _g_selection(g_config: dict) -> dict:
    return {
        "receipt_schema": "PEDICULARIS_G_CONFIRMATORY_METHOD_SELECTION_V1",
        "status": "PEDICULARIS_G_CONFIRMATORY_METHOD_SELECTED_BEFORE_OUTCOMES",
        "population_id": POP,
        "season_id": SEASON,
        "selected_candidate_id": "G_A1_FINE_MESH",
        "selected_exclusion_method": "FINE_MESH_LOWER_FRUIT_SLEEVE",
        "exposed_sham_method_code": "SHAM_SLEEVE",
        "g_field_config_sha256": _semantic_sha256(g_config),
    }


def _f0_receipt(
    *,
    p0_config: dict | None = None,
    p1_config: dict | None = None,
    g_config: dict | None = None,
) -> dict:
    p0_config = _p0() if p0_config is None else p0_config
    p1_config = _p1() if p1_config is None else p1_config
    g_config = _g() if g_config is None else g_config
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_F0_CONFIG_ASSEMBLY_V1",
        "population_id": POP,
        "season_id": SEASON,
        "assembled_config_status": {
            "P0": p0_config["status"],
            "P1": p1_config["status"],
            "G": g_config["status"],
        },
        "assembled_config_sha256": {
            "P0": _semantic_sha256(p0_config),
            "P1": _semantic_sha256(p1_config),
            "G": _semantic_sha256(g_config),
        },
        "status": "PEDICULARIS_F0_CONFIGS_ASSEMBLED_AND_FROZEN",
    }


def _build() -> dict:
    p0 = _p0()
    p1 = _p1()
    g = _g()
    return build(
        geometry_config=_geometry(),
        p0_level_plan=_levels(),
        p0_field_config=p0,
        p1_field_config=p1,
        g_field_config=g,
        g_method_selection=_g_selection(g),
        f0_assembly_receipt=_f0_receipt(
            p0_config=p0,
            p1_config=p1,
            g_config=g,
        ),
    )


def test_binding_allows_parallel_collection_but_not_basis_use() -> None:
    result = _build()

    assert result["status"] == (
        "PEDICULARIS_GEOMETRY_INTERVENTION_PLAN_"
        "FROZEN_BEFORE_CONFIRMATORY_OUTCOMES"
    )
    assert result["geometry_collection_may_run_before_lane_validation"] is True
    assert result["geometry_analysis_requires_later_positive_readiness_v3"] is True
    assert result["p1_experimental_unit"] == "WITHIN_PLANT_PAIRED_FLOWERS"
    assert result["g_exclusion_method"] == "FINE_MESH_LOWER_FRUIT_SLEEVE"
    assert all(
        len(result[key]) == 64
        for key in (
            "geometry_config_sha256",
            "p0_level_plan_sha256",
            "p0_field_config_sha256",
            "p1_field_config_sha256",
            "g_field_config_sha256",
            "g_method_selection_sha256",
            "f0_assembly_receipt_sha256",
        )
    )


def test_geometry_z_plan_must_match_frozen_p0_plan() -> None:
    geometry = _geometry()
    geometry["z_levels"][4]["assigned_z_level"] = "DIFFERENT"
    g = _g()

    with pytest.raises(ValueError, match="z labels/ranks"):
        build(
            geometry_config=geometry,
            p0_level_plan=_levels(),
            p0_field_config=_p0(),
            p1_field_config=_p1(),
            g_field_config=g,
            g_method_selection=_g_selection(g),
            f0_assembly_receipt=_f0_receipt(),
        )


def test_geometry_g_method_must_match_preoutcome_selected_method() -> None:
    geometry = _geometry()
    geometry["excluded_method_code"] = "POROUS_TUBING_LOWER_FRUIT_SLEEVE"
    g = _g()

    with pytest.raises(ValueError, match="selected G method"):
        build(
            geometry_config=geometry,
            p0_level_plan=_levels(),
            p0_field_config=_p0(),
            p1_field_config=_p1(),
            g_field_config=g,
            g_method_selection=_g_selection(g),
            f0_assembly_receipt=_f0_receipt(),
        )


def test_g_selection_must_be_bound_to_exact_g_field_config() -> None:
    g = _g()
    selection = _g_selection(g)
    changed_g = deepcopy(g)
    changed_g["method_gate"]["max_hours_after_anthesis_before_barrier"] = 29.0

    with pytest.raises(ValueError, match="exact frozen G field config"):
        build(
            geometry_config=_geometry(),
            p0_level_plan=_levels(),
            p0_field_config=_p0(),
            p1_field_config=_p1(),
            g_field_config=changed_g,
            g_method_selection=selection,
            f0_assembly_receipt=_f0_receipt(g_config=changed_g),
        )


def test_all_intervention_plans_must_share_same_context() -> None:
    p1 = _p1()
    p1["prospective_freeze"]["season_id"] = "S2"
    g = _g()

    with pytest.raises(ValueError, match="share one population/season"):
        build(
            geometry_config=_geometry(),
            p0_level_plan=_levels(),
            p0_field_config=_p0(),
            p1_field_config=p1,
            g_field_config=g,
            g_method_selection=_g_selection(g),
            f0_assembly_receipt=_f0_receipt(),
        )


def test_parallel_binding_requires_current_paired_p1_plan() -> None:
    p1 = _p1()
    p1["pollination_weight"]["experimental_unit"] = "WHOLE_PLANT"
    g = _g()

    with pytest.raises(ValueError, match="paired-flower"):
        build(
            geometry_config=_geometry(),
            p0_level_plan=_levels(),
            p0_field_config=_p0(),
            p1_field_config=p1,
            g_field_config=g,
            g_method_selection=_g_selection(g),
            f0_assembly_receipt=_f0_receipt(),
        )


def test_preoutcome_binding_contains_no_readiness_or_lane_outcomes() -> None:
    result = _build()

    assert "readiness_receipt_sha256" not in result
    assert "readiness_status" not in result
    assert "P0_status" not in result
    assert "P1_status" not in result
    assert "G_status" not in result
    assert result["geometry_collection_may_run_before_lane_validation"] is True
    assert result["geometry_analysis_requires_later_positive_readiness_v3"] is True


def test_hand_edited_lane_config_with_same_status_is_rejected_by_f0_digest() -> None:
    p0 = _p0()
    p1 = _p1()
    g = _g()
    receipt = _f0_receipt(
        p0_config=p0,
        p1_config=p1,
        g_config=g,
    )
    changed_p0 = deepcopy(p0)
    changed_p0["stage_p0"]["min_adjacent_exsertion_gap"] = 0.12345

    with pytest.raises(ValueError, match="exact configs produced by F0 assembly"):
        build(
            geometry_config=_geometry(),
            p0_level_plan=_levels(),
            p0_field_config=changed_p0,
            p1_field_config=p1,
            g_field_config=g,
            g_method_selection=_g_selection(g),
            f0_assembly_receipt=receipt,
        )

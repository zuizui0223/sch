from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.build_pedicularis_full_surface_allocation import build as allocate
from scripts.prepare_pedicularis_full_surface_field_sheet import (
    prepare,
    verify,
)


def _allocation_config() -> dict:
    return {
        "schema": "PEDICULARIS_FULL_SURFACE_ALLOCATION_CONFIG_V1",
        "status": "PEDICULARIS_FULL_SURFACE_ALLOCATION_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "planned_n_plants": 10,
        "flowers_per_plant": 4,
        "p0_level_plan_sha256": "1" * 64,
        "z_levels": [
            {
                "assigned_z_level": f"Z{i}",
                "assigned_z_rank": i,
                "target_exsertion": value,
                "manipulation_setting_id": f"SETTING_Z{i}",
            }
            for i, value in enumerate((-2.0, -1.0, 0.0, 1.0, 2.0))
        ],
        "excluded_method_code": "FINE_MESH_LOWER_FRUIT_SLEEVE",
        "exposed_method_code": "SHAM_SLEEVE",
        "frozen_before_full_surface_outcomes": True,
    }


def _readiness(config: dict | None = None) -> dict:
    config = _allocation_config() if config is None else config
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3",
        "status": "PEDICULARIS_FULL_SURFACE_READY",
        "population_id": config["population_id"],
        "season_id": config["season_id"],
        "checks": {
            "same_population_and_season": True,
            "z_randomized_allocation_verified": True,
            "z_levels_validated": True,
            "z_manipulation_settings_validated": True,
            "p_randomized_allocation_verified": True,
            "g_randomized_allocation_verified": True,
            "g_method_timing_validated": True,
        },
        "validated_execution": {
            "z_levels": [
                row["assigned_z_level"] for row in config["z_levels"]
            ],
            "z_manipulation_settings": [
                {
                    "assigned_z_level": row["assigned_z_level"],
                    "assigned_z_rank": row["assigned_z_rank"],
                    "manipulation_setting_id": row["manipulation_setting_id"],
                }
                for row in config["z_levels"]
            ],
            "p0_level_plan_sha256": config["p0_level_plan_sha256"],
            "p_experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
            "g_exclusion_method": config["excluded_method_code"],
            "g_exposed_sham_method": config["exposed_method_code"],
            "z_allocation_identity_sha256": "a" * 64,
            "p_allocation_identity_sha256": "b" * 64,
            "g_allocation_identity_sha256": "c" * 64,
        },
        "source_receipts": {
            "z": {
                "schema": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1",
                "threshold_freeze_status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
                "receipt_sha256": "d" * 64,
            },
            "p": {
                "schema": "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1",
                "threshold_freeze_status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
                "receipt_sha256": "e" * 64,
            },
            "g": {
                "schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V4",
                "threshold_freeze_status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
                "receipt_sha256": "f" * 64,
            },
        },
        "water_y_requirement": "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "predator_method_requirement": (
            "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_"
            "WITH_POLLINATOR_ACCESS_PRESERVED"
        ),
    }


def _power() -> dict:
    return {
        "analysis": "pedicularis_W1_W2_full_surface_power_v1",
        "status": "PEDICULARIS_W1_W2_POWER_SIMULATION_COMPLETE",
        "planning_provenance": {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "basis_document": "SYNTHETIC_TEST",
        },
        "target_truth_world": "W1",
        "target_primary_surface_power": 0.80,
        "target_headline_w1_or_w2_power": 0.80,
        "registered_field_allocation_recommendation_allowed": True,
        "p0_f0_config_binding_status": (
            "PEDICULARIS_W1_W2_P0_F0_CONFIG_EXACTLY_BOUND"
        ),
        "production_surface_config_sha256": "7" * 64,
        "surface_threshold_freeze_sha256": "8" * 64,
        "power_config_sha256": "9" * 64,
        "powered_design": {
            "nominal_z_levels": [-2.0, -1.0, 0.0, 1.0, 2.0],
            "realized_z_sd": 0.1,
            "field_design": {
                "flowers_per_plant": 4,
                "n_surface_cells": 20,
                "allocation_strategy": (
                    "BALANCED_CYCLIC_RANDOMIZED_Z_BY_P_BY_G_V1"
                ),
            },
        },
        "candidate_results": [
            {
                "plants": 10,
                "flowers_per_plant": 4,
                "flowers_per_treatment_cell": 2,
                "total_full_surface_flowers": 40,
                "primary_surface_power": 0.90,
                "headline_W1_or_W2_power": 0.85,
            }
        ],
    }


def _manifest() -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower:02d}",
        }
        for plant in range(10)
        for flower in range(4)
    ]


def _allocation_packet() -> tuple[list[dict[str, str]], dict]:
    config = _allocation_config()
    return allocate(
        _manifest(),
        config,
        _power(),
        _readiness(config),
        "LOCKED-P2-SEED",
    )


def _complete(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    completed = deepcopy(rows)
    for row in completed:
        row["realized_exsertion"] = row["target_exsertion"]
        row["water_depth"] = "1.0"
        row["ovule_count"] = "100"
        row["undamaged_seed_count"] = "50"
        row["damaged_seed_count"] = "5"
        row["pollen_grains"] = "20"
        row["early_predator_attack_present"] = (
            "1" if row["predator_treatment"] == "EXPOSED" else "0"
        )
        row["mechanical_damage"] = "0"
    return completed


def test_prepare_prefills_only_frozen_identity_and_treatment_fields() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)

    assert len(field_rows) == 40
    assert lock["n_rows"] == 40
    assert lock["allocation_identity_sha256"] == allocation_receipt[
        "allocation_identity_sha256"
    ]
    assert lock["outcome_fields_prefilled"] is False
    assert lock["p0_level_plan_sha256"] == "1" * 64
    assert len(lock["readiness_receipt_sha256"]) == 64
    assert lock["production_surface_config_sha256"] == "7" * 64
    assert lock["surface_threshold_freeze_sha256"] == "8" * 64
    assert lock["power_config_sha256"] == "9" * 64
    assert all(row["assigned_z_level"] for row in field_rows)
    assert all(row["manipulation_setting_id"] for row in field_rows)
    assert all(row["pollination_treatment"] for row in field_rows)
    assert all(row["predator_treatment"] for row in field_rows)
    assert all(row["exclusion_method"] for row in field_rows)
    assert all(row["target_exsertion"] for row in field_rows)
    assert all(row["realized_exsertion"] == "" for row in field_rows)
    assert all(row["undamaged_seed_count"] == "" for row in field_rows)
    assert all(row["pollen_grains"] == "" for row in field_rows)


def test_row_order_can_change_without_breaking_identity_lock() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)

    receipt = verify(
        list(reversed(field_rows)),
        lock,
        require_complete=False,
    )

    assert receipt["identity_and_treatment_match"] is True
    assert receipt["canonical_outcomes_complete"] is False
    assert receipt["status"] == "P2_FULL_SURFACE_FIELD_IDENTITY_VERIFIED"


def test_flower_substitution_fails_closed() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)
    field_rows[0]["flower_id"] = "SUBSTITUTED_FLOWER"

    with pytest.raises(ValueError, match="drifted from the locked allocation"):
        verify(field_rows, lock, require_complete=False)


def test_treatment_drift_fails_closed() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)
    field_rows[0]["pollination_treatment"] = (
        "SUPPLEMENTED"
        if field_rows[0]["pollination_treatment"] == "NATURAL"
        else "NATURAL"
    )

    with pytest.raises(ValueError, match="drifted from the locked allocation"):
        verify(field_rows, lock, require_complete=False)


def test_method_drift_fails_closed() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)
    field_rows[0]["exclusion_method"] = "AD_HOC_METHOD"

    with pytest.raises(ValueError, match="drifted from the locked allocation"):
        verify(field_rows, lock, require_complete=False)


def test_missing_row_fails_closed() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)

    with pytest.raises(ValueError, match="row count drifted"):
        verify(field_rows[:-1], lock, require_complete=False)


def test_duplicate_flower_fails_closed() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)
    field_rows[1]["flower_id"] = field_rows[0]["flower_id"]

    with pytest.raises(ValueError, match="flower_id must be unique"):
        verify(field_rows, lock, require_complete=False)


def test_require_complete_rejects_blank_outcome_cells() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)

    with pytest.raises(ValueError, match="first blank canonical cell"):
        verify(field_rows, lock, require_complete=True)


def test_complete_packet_produces_surface_data_fingerprint() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)
    completed = _complete(field_rows)

    receipt = verify(completed, lock, require_complete=True)

    assert receipt["identity_and_treatment_match"] is True
    assert receipt["canonical_outcomes_complete"] is True
    assert receipt["surface_data_sha256"] is not None
    assert receipt["readiness_receipt_sha256"] == lock["readiness_receipt_sha256"]
    assert receipt["production_surface_config_sha256"] == "7" * 64
    assert receipt["surface_threshold_freeze_sha256"] == "8" * 64
    assert receipt["power_config_sha256"] == "9" * 64
    assert len(receipt["surface_data_sha256"]) == 64
    assert receipt["status"] == (
        "P2_FULL_SURFACE_FIELD_PACKET_VERIFIED_COMPLETE"
    )


def test_allocation_receipt_drift_is_rejected_at_prepare() -> None:
    allocations, allocation_receipt = _allocation_packet()
    allocation_receipt = deepcopy(allocation_receipt)
    allocation_receipt["allocation_identity_sha256"] = "0" * 64

    with pytest.raises(ValueError, match="allocation receipt digest"):
        prepare(allocations, allocation_receipt)


def test_physical_z_setting_drift_fails_closed() -> None:
    allocations, allocation_receipt = _allocation_packet()
    field_rows, lock = prepare(allocations, allocation_receipt)
    field_rows[0]["manipulation_setting_id"] = "AD_HOC_SETTING"

    with pytest.raises(ValueError, match="drifted from the locked allocation"):
        verify(field_rows, lock, require_complete=False)


def test_production_field_sheet_rejects_unvalidated_dual_endpoint_allocation() -> None:
    allocations, allocation_receipt = _allocation_packet()
    with pytest.raises(ValueError, match="validated same-flower"):
        prepare(
            allocations,
            allocation_receipt,
            require_endpoint_binding=True,
        )


def test_production_field_sheet_propagates_joint_endpoint_assay_identity() -> None:
    allocations, allocation_receipt = _allocation_packet()
    allocation_receipt["endpoint_feasibility_binding"] = {
        "receipt_schema": "PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBILITY_V1",
        "status": "PEDICULARIS_P2_DUAL_ENDPOINT_FEASIBLE_FOR_SINGLE_FLOWER_PIPELINE",
        "collection_route": "SAME_FLOWER_NONDESTRUCTIVE_POLLEN_QUANTIFICATION",
        "pollen_assay_method_id": "SYNTHETIC_TEST_METHOD",
        "feasibility_receipt_sha256": "d" * 64,
        "independent_pilot_data_sha256": "e" * 64,
    }
    allocation_receipt[
        "single_flower_endpoint_compatibility_validated_before_allocation"
    ] = True

    field_rows, lock = prepare(
        allocations,
        allocation_receipt,
        require_endpoint_binding=True,
    )
    assert lock["endpoint_feasibility_binding"]["pollen_assay_method_id"] == (
        "SYNTHETIC_TEST_METHOD"
    )
    receipt = verify(_complete(field_rows), lock, require_complete=True)
    assert receipt["endpoint_feasibility_binding"]["feasibility_receipt_sha256"] == (
        "d" * 64
    )

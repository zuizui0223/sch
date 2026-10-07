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
    return allocate(
        _manifest(),
        _allocation_config(),
        _power(),
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

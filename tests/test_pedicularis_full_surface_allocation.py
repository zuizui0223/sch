from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.build_pedicularis_full_surface_allocation import build


def _config() -> dict:
    return {
        "schema": "PEDICULARIS_FULL_SURFACE_ALLOCATION_CONFIG_V1",
        "status": "PEDICULARIS_FULL_SURFACE_ALLOCATION_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "planned_n_plants": 10,
        "flowers_per_plant": 4,
        "z_levels": [
            {
                "assigned_z_level": f"Z{i}",
                "assigned_z_rank": i,
                "target_exsertion": value,
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
        "powered_design": {
            "nominal_z_levels": [-2.0, -1.0, 0.0, 1.0, 2.0],
            "realized_z_sd": 0.1,
            "field_design": {
                "flowers_per_plant": 4,
                "allocation_strategy": "BALANCED_CYCLIC_RANDOMIZED_20_CELL",
            },
        },
        "candidate_results": [
            {
                "plants": 5,
                "flowers_per_plant": 4,
                "flowers_per_treatment_cell": 1,
                "total_full_surface_flowers": 20,
                "primary_surface_power": 0.70,
                "headline_W1_or_W2_power": 0.60,
            },
            {
                "plants": 10,
                "flowers_per_plant": 4,
                "flowers_per_treatment_cell": 2,
                "total_full_surface_flowers": 40,
                "primary_surface_power": 0.90,
                "headline_W1_or_W2_power": 0.85,
            },
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


def test_balanced_incomplete_block_allocation_matches_powered_design() -> None:
    allocations, receipt = build(
        _manifest(),
        _config(),
        _power(),
        "PRECOMMITTED-SEED-1",
    )

    assert len(allocations) == 40
    assert receipt["n_plants"] == 10
    assert receipt["flowers_per_plant"] == 4
    assert receipt["n_surface_cells"] == 20
    assert receipt["replicates_per_cell"] == 2
    assert receipt["exact_cell_balance"] is True
    assert set(receipt["cell_counts"].values()) == {2}
    assert receipt["power_binding"]["candidate_primary_surface_power"] == 0.90
    assert receipt["power_binding"]["candidate_headline_w1_or_w2_power"] == 0.85

    by_plant: dict[str, set[str]] = {}
    for row in allocations:
        by_plant.setdefault(row["plant_id"], set()).add(
            row["allocation_cell_id"]
        )
    assert len(by_plant) == 10
    assert all(len(cells) == 4 for cells in by_plant.values())


def test_same_seed_is_reproducible_and_new_seed_changes_assignment() -> None:
    a1, r1 = build(_manifest(), _config(), _power(), "SEED-A")
    a2, r2 = build(_manifest(), _config(), _power(), "SEED-A")
    a3, r3 = build(_manifest(), _config(), _power(), "SEED-B")

    assert a1 == a2
    assert r1["allocation_identity_sha256"] == r2[
        "allocation_identity_sha256"
    ]
    assert r1["allocation_identity_sha256"] != r3[
        "allocation_identity_sha256"
    ]
    assert a1 != a3
    assert set(r3["cell_counts"].values()) == {2}


def test_duplicate_flower_id_fails_closed() -> None:
    manifest = _manifest()
    manifest[1]["flower_id"] = manifest[0]["flower_id"]

    with pytest.raises(ValueError, match="flower_id must be unique"):
        build(manifest, _config(), _power(), "SEED")


def test_wrong_flower_count_per_plant_fails_closed() -> None:
    manifest = _manifest()[:-1]

    with pytest.raises(ValueError, match="exactly flowers_per_plant"):
        build(manifest, _config(), _power(), "SEED")


def test_manifest_context_mismatch_fails_closed() -> None:
    manifest = _manifest()
    manifest[0]["season_id"] = "S2"

    with pytest.raises(ValueError, match="season_id does not match config"):
        build(manifest, _config(), _power(), "SEED")


def test_z_grid_must_match_powered_design() -> None:
    config = _config()
    config["z_levels"][4]["target_exsertion"] = 2.5

    with pytest.raises(ValueError, match="does not match powered z levels"):
        build(_manifest(), config, _power(), "SEED")


def test_flowers_per_plant_must_match_powered_design() -> None:
    config = _config()
    config["flowers_per_plant"] = 5
    config["planned_n_plants"] = 8

    manifest = [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower:02d}",
        }
        for plant in range(8)
        for flower in range(5)
    ]

    with pytest.raises(ValueError, match="flowers_per_plant does not match"):
        build(manifest, config, _power(), "SEED")


def test_planned_n_must_be_an_evaluated_power_candidate() -> None:
    config = _config()
    config["planned_n_plants"] = 15
    manifest = [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower:02d}",
        }
        for plant in range(15)
        for flower in range(4)
    ]

    with pytest.raises(ValueError, match="exactly one evaluated power candidate"):
        build(manifest, config, _power(), "SEED")


def test_candidate_below_headline_target_cannot_be_allocated() -> None:
    power = _power()
    power["candidate_results"][1]["headline_W1_or_W2_power"] = 0.79

    with pytest.raises(ValueError, match="headline power target"):
        build(_manifest(), _config(), power, "SEED")


def test_candidate_below_primary_target_cannot_be_allocated() -> None:
    power = _power()
    power["candidate_results"][1]["primary_surface_power"] = 0.79

    with pytest.raises(ValueError, match="primary-surface power target"):
        build(_manifest(), _config(), power, "SEED")


def test_unresolved_allocation_seed_fails_closed() -> None:
    with pytest.raises(ValueError, match="allocation_seed"):
        build(_manifest(), _config(), _power(), "REQUIRED_BEFORE_USE")


def test_zero_based_z_ranks_must_be_contiguous() -> None:
    config = _config()
    config["z_levels"][4]["assigned_z_rank"] = 6

    with pytest.raises(ValueError, match="contiguous 0..k-1"):
        build(_manifest(), config, _power(), "SEED")


def test_power_context_must_match_allocation_context() -> None:
    power = deepcopy(_power())
    power["planning_provenance"]["season_id"] = "S2"

    with pytest.raises(ValueError, match="power and allocation season_id"):
        build(_manifest(), _config(), power, "SEED")

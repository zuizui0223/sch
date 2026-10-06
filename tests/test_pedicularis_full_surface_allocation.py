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
                "allocation_strategy": "BALANCED_CYCLIC_RANDOMIZED_Z_BY_P_BY_G_V1",
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


def _context() -> dict:
    return {
        "analysis": "pedicularis_p2_context_freeze_v1",
        "receipt_schema": "PEDICULARIS_P2_CONTEXT_FREEZE_V1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "selection_mode": "CURRENT_CONTEXT_ONLY",
        "inference_scope": "PRIMARY_TESTED_CONTEXT_ONLY",
        "selection_basis_note": "SYNTHETIC_TEST",
        "historical_context_prior": None,
        "current_season_context": {
            "pollination_lane_validated": True,
            "antagonist_lane_validated": True,
            "z_manipulation_validated": True,
            "same_population_and_season": True,
            "readiness_receipt_sha256": "a" * 64,
        },
        "same_season_pollination_and_antagonist_lanes_validated": True,
        "context_selected_before_full_surface_outcomes": True,
        "readiness_receipt_sha256": "a" * 64,
        "context_config_sha256": "b" * 64,
        "status": (
            "P2_CONTEXT_FROZEN_CURRENT_SEASON_BOTH_FUNCTIONAL_LANES_VALIDATED"
        ),
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
        _context(),
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
    a1, r1 = build(_manifest(), _config(), _power(), _context(), "SEED-A")
    a2, r2 = build(_manifest(), _config(), _power(), _context(), "SEED-A")
    a3, r3 = build(_manifest(), _config(), _power(), _context(), "SEED-B")

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
        build(manifest, _config(), _power(), _context(), "SEED")


def test_wrong_flower_count_per_plant_fails_closed() -> None:
    manifest = _manifest()[:-1]

    with pytest.raises(ValueError, match="exactly flowers_per_plant"):
        build(manifest, _config(), _power(), _context(), "SEED")


def test_manifest_context_mismatch_fails_closed() -> None:
    manifest = _manifest()
    manifest[0]["season_id"] = "S2"

    with pytest.raises(ValueError, match="season_id does not match config"):
        build(manifest, _config(), _power(), _context(), "SEED")


def test_z_grid_must_match_powered_design() -> None:
    config = _config()
    config["z_levels"][4]["target_exsertion"] = 2.5

    with pytest.raises(ValueError, match="does not match powered z levels"):
        build(_manifest(), config, _power(), _context(), "SEED")


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
        build(manifest, config, _power(), _context(), "SEED")


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
        build(manifest, config, _power(), _context(), "SEED")


def test_candidate_below_headline_target_cannot_be_allocated() -> None:
    power = _power()
    power["candidate_results"][1]["headline_W1_or_W2_power"] = 0.79

    with pytest.raises(ValueError, match="headline power target"):
        build(_manifest(), _config(), power, _context(), "SEED")


def test_candidate_below_primary_target_cannot_be_allocated() -> None:
    power = _power()
    power["candidate_results"][1]["primary_surface_power"] = 0.79

    with pytest.raises(ValueError, match="primary-surface power target"):
        build(_manifest(), _config(), power, _context(), "SEED")


def test_unresolved_allocation_seed_fails_closed() -> None:
    with pytest.raises(ValueError, match="allocation_seed"):
        build(_manifest(), _config(), _power(), _context(), "REQUIRED_BEFORE_USE")


def test_zero_based_z_ranks_must_be_contiguous() -> None:
    config = _config()
    config["z_levels"][4]["assigned_z_rank"] = 6

    with pytest.raises(ValueError, match="contiguous 0..k-1"):
        build(_manifest(), config, _power(), _context(), "SEED")


def test_power_context_must_match_allocation_context() -> None:
    power = deepcopy(_power())
    power["planning_provenance"]["season_id"] = "S2"

    with pytest.raises(ValueError, match="power and allocation season_id"):
        build(_manifest(), _config(), power, _context(), "SEED")


def test_six_z_level_allocation_uses_all_twenty_four_cells() -> None:
    config = _config()
    config["planned_n_plants"] = 8
    config["flowers_per_plant"] = 6
    config["z_levels"] = [
        {
            "assigned_z_level": f"Z{i}",
            "assigned_z_rank": i,
            "target_exsertion": value,
        }
        for i, value in enumerate((-2.0, -1.0, 0.0, 1.0, 2.0, 3.0))
    ]
    power = _power()
    power["powered_design"]["nominal_z_levels"] = [
        -2.0, -1.0, 0.0, 1.0, 2.0, 3.0
    ]
    power["powered_design"]["field_design"]["flowers_per_plant"] = 6
    power["powered_design"]["field_design"]["n_surface_cells"] = 24
    power["candidate_results"] = [
        {
            "plants": 8,
            "flowers_per_plant": 6,
            "flowers_per_treatment_cell": 2,
            "total_full_surface_flowers": 48,
            "primary_surface_power": 0.90,
            "headline_W1_or_W2_power": 0.85,
        }
    ]
    manifest = [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower:02d}",
        }
        for plant in range(8)
        for flower in range(6)
    ]

    allocations, receipt = build(manifest, config, power, _context(), "SEED-24")

    assert len(allocations) == 48
    assert receipt["n_surface_cells"] == 24
    assert receipt["replicates_per_cell"] == 2
    assert len(receipt["cell_counts"]) == 24
    assert set(receipt["cell_counts"].values()) == {2}


def test_allocation_requires_positive_same_season_context_freeze() -> None:
    context = _context()
    context["same_season_pollination_and_antagonist_lanes_validated"] = False

    with pytest.raises(ValueError, match="same-season validated pollination"):
        build(
            _manifest(),
            _config(),
            _power(),
            context,
            "SEED",
        )


def test_context_population_must_match_allocation_context() -> None:
    context = _context()
    context["population_id"] = "OTHER_POP"

    with pytest.raises(ValueError, match="context and allocation population_id"):
        build(
            _manifest(),
            _config(),
            _power(),
            context,
            "SEED",
        )


def test_context_historical_prior_remains_prior_in_allocation_receipt() -> None:
    context = _context()
    context["selection_mode"] = "HISTORICAL_CONTEXT_PRIOR"
    context["inference_scope"] = "PRIMARY_HIGH_ANTAGONISM_ENRICHED_CONTEXT"
    context["historical_context_prior"] = {
        "historical_population_code": "POP5",
        "individual_linkage_retained": True,
        "exact_main_text_seed_predation_percent": 27.42,
        "exact_pressure_rank_among_four": 1,
        "history_class": "HIGHEST_EXACT_PRESSURE_LINKED",
        "allowed_use": "HISTORICAL_ENRICHMENT_PRIOR_ONLY",
        "source": "Sun_Armbruster_Huang_2016_mcw097",
        "mapping_status": "SOURCE_VERIFIED",
        "mapping_source": "SYNTHETIC_VERIFIED_TABLE_S1_MAPPING",
        "historical_value_is_current_season_measurement": False,
    }

    _, receipt = build(
        _manifest(),
        _config(),
        _power(),
        context,
        "SEED",
    )

    historical = receipt["context_binding"]["historical_context_prior"]
    assert historical["historical_population_code"] == "POP5"
    assert historical["exact_main_text_seed_predation_percent"] == 27.42
    assert historical["history_class"] == "HIGHEST_EXACT_PRESSURE_LINKED"

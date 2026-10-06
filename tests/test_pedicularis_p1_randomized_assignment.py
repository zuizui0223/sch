from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.build_pedicularis_p1_randomized_assignment import build
from scripts.pedicularis_config_freeze import required_gate_paths


def _freeze() -> dict:
    return {
        "schema": "SCH_PEDICULARIS_THRESHOLD_FREEZE_V1",
        "status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
        "lane": "P1",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-10-06T00:00:00Z",
        "basis_document": "SYNTHETIC_TEST_ONLY",
        "threshold_basis": {
            path: "SYNTHETIC_TEST_ONLY"
            for path in required_gate_paths("P1")
        },
    }


def _p1_field_config() -> dict:
    return {
        "status": "PEDICULARIS_P1_FIELD_CONFIG_FROZEN",
        "bootstrap_reps": 300,
        "random_seed": 31,
        "pollination_weight": {
            "experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
            "min_paired_plants": 10,
            "min_flowers_per_treatment": 20,
            "min_pollen_grain_delta": 5.0,
            "min_initial_seed_set_delta": 0.10,
            "max_early_predator_attack_difference": 0.05,
            "max_z_relative_change": 0.03,
            "max_bract_height_relative_change": 0.03,
            "max_opening_width_relative_change": 0.03,
            "max_water_depth_change": 0.15,
            "max_mechanical_damage_rate": 0.05,
        },
        "prospective_freeze": _freeze(),
    }


def _allocation_config(
    *,
    plants: int = 10,
    flowers_per_treatment_per_plant: int = 2,
) -> dict:
    return {
        "schema": "PEDICULARIS_P1_ALLOCATION_CONFIG_V1",
        "status": "PEDICULARIS_P1_ALLOCATION_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "planned_paired_plants": plants,
        "flowers_per_treatment_per_plant": flowers_per_treatment_per_plant,
        "frozen_before_confirmatory_outcomes": True,
    }


def _manifest(
    *,
    plants: int = 10,
    flowers_per_plant: int = 4,
) -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower:02d}",
        }
        for plant in range(plants)
        for flower in range(flowers_per_plant)
    ]


def test_randomized_paired_allocation_is_exactly_balanced() -> None:
    allocations, receipt = build(
        _manifest(),
        _allocation_config(),
        _p1_field_config(),
        "P1-SEED-A",
    )

    assert len(allocations) == 40
    assert receipt["n_paired_plants"] == 10
    assert receipt["flowers_per_treatment_per_plant"] == 2
    assert receipt["n_by_treatment"] == {
        "NATURAL": 20,
        "SUPPLEMENTED": 20,
    }
    assert receipt["experimental_unit"] == "WITHIN_PLANT_PAIRED_FLOWERS"
    assert receipt["assignment_randomized_within_plant"] is True
    assert receipt["sample_size_chosen_by_script"] is False

    for plant in range(10):
        rows = [
            row
            for row in allocations
            if row["plant_id"] == f"P{plant:02d}"
        ]
        assert sum(
            row["pollination_treatment"] == "NATURAL" for row in rows
        ) == 2
        assert sum(
            row["pollination_treatment"] == "SUPPLEMENTED" for row in rows
        ) == 2
        assert all(
            row["pollination_handling_role"] == (
                "SHAM_STIGMA_CONTACT"
                if row["pollination_treatment"] == "NATURAL"
                else "DONOR_MIXED_CROSS_POLLEN"
            )
            for row in rows
        )


def test_same_seed_reproduces_assignment_and_new_seed_changes_it() -> None:
    a1, r1 = build(
        _manifest(),
        _allocation_config(),
        _p1_field_config(),
        "P1-SEED-A",
    )
    a2, r2 = build(
        _manifest(),
        _allocation_config(),
        _p1_field_config(),
        "P1-SEED-A",
    )
    a3, r3 = build(
        _manifest(),
        _allocation_config(),
        _p1_field_config(),
        "P1-SEED-B",
    )

    assert a1 == a2
    assert r1["allocation_identity_sha256"] == r2[
        "allocation_identity_sha256"
    ]
    assert a1 != a3
    assert r1["allocation_identity_sha256"] != r3[
        "allocation_identity_sha256"
    ]


def test_planned_paired_plants_cannot_drop_below_frozen_minimum() -> None:
    with pytest.raises(ValueError, match="below frozen P1 min_paired_plants"):
        build(
            _manifest(plants=9, flowers_per_plant=4),
            _allocation_config(plants=9),
            _p1_field_config(),
            "SEED",
        )


def test_planned_flowers_per_treatment_cannot_drop_below_frozen_minimum() -> None:
    config = _p1_field_config()
    config["pollination_weight"]["min_flowers_per_treatment"] = 30

    with pytest.raises(ValueError, match="below frozen min_flowers_per_treatment"):
        build(
            _manifest(),
            _allocation_config(),
            config,
            "SEED",
        )


def test_manifest_requires_exact_treatment_blind_flower_count_per_plant() -> None:
    manifest = _manifest()
    manifest.pop()

    with pytest.raises(ValueError, match="exactly 4 treatment-blind flowers"):
        build(
            manifest,
            _allocation_config(),
            _p1_field_config(),
            "SEED",
        )


def test_duplicate_flower_id_fails_closed() -> None:
    manifest = _manifest()
    manifest[1]["flower_id"] = manifest[0]["flower_id"]

    with pytest.raises(ValueError, match="globally unique"):
        build(
            manifest,
            _allocation_config(),
            _p1_field_config(),
            "SEED",
        )


def test_whole_plant_route_cannot_enter_current_paired_allocator() -> None:
    config = _p1_field_config()
    config["pollination_weight"]["experimental_unit"] = (
        "WHOLE_PLANT_SUPPLEMENTATION"
    )

    with pytest.raises(ValueError, match="only WITHIN_PLANT_PAIRED_FLOWERS"):
        build(
            _manifest(),
            _allocation_config(),
            config,
            "SEED",
        )


def test_allocation_context_must_match_frozen_p1_context() -> None:
    allocation = _allocation_config()
    allocation["season_id"] = "S2"

    with pytest.raises(ValueError, match="season_id differ"):
        build(
            _manifest(),
            allocation,
            _p1_field_config(),
            "SEED",
        )


def test_allocation_requires_f0_assembled_p1_config() -> None:
    config = _p1_field_config()
    config["status"] = "TEMPLATE_ONLY_DO_NOT_RUN"

    with pytest.raises(ValueError, match="F0-assembled"):
        build(
            _manifest(),
            _allocation_config(),
            config,
            "SEED",
        )


def test_unresolved_seed_fails_closed() -> None:
    with pytest.raises(ValueError, match="allocation_seed"):
        build(
            _manifest(),
            _allocation_config(),
            _p1_field_config(),
            "REQUIRED_BEFORE_USE",
        )


def test_config_digest_changes_if_thresholds_are_changed() -> None:
    _, r1 = build(
        _manifest(),
        _allocation_config(),
        _p1_field_config(),
        "SEED",
    )
    changed = deepcopy(_p1_field_config())
    changed["pollination_weight"]["min_pollen_grain_delta"] = 6.0
    _, r2 = build(
        _manifest(),
        _allocation_config(),
        changed,
        "SEED",
    )

    assert r1["p1_field_config_sha256"] != r2[
        "p1_field_config_sha256"
    ]

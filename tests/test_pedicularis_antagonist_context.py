from __future__ import annotations

import pytest

from scripts import analyze_pedicularis_full_surface as surface
from scripts.analyze_pedicularis_antagonist_context import (build, _plant_natural_exposed)


def _config() -> dict:
    return {
        "schema": "PEDICULARIS_P2_ANTAGONIST_CONTEXT_CONFIG_V1",
        "status": "PEDICULARIS_P2_ANTAGONIST_CONTEXT_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_before_p2_outcomes": True,
        "historical_comparison": {
            "source": (
                "Xia Sun Liu 2013 Biology Letters "
                "doi:10.1098/rsbl.2013.0387"
            ),
            "sparse_density_max_exclusive_plants_m2": 2.0,
            "dense_density_min_exclusive_plants_m2": 5.0,
            "small_patch_max_exclusive_flowering_plants": 20,
            "large_patch_min_exclusive_flowering_plants": 20,
            "exact_boundary_is_unclassified": True,
        },
        "analysis_gate": {
            "min_patches_per_historical_context_cell": 2,
        },
    }


CELL_PLAN = {
    "SPARSE_SMALL": {
        "patch_area_m2": 10.0,
        "patch_size": 10,
        "predation": 0.40,
    },
    "SPARSE_LARGE": {
        "patch_area_m2": 30.0,
        "patch_size": 30,
        "predation": 0.20,
    },
    "DENSE_SMALL": {
        "patch_area_m2": 1.5,
        "patch_size": 10,
        "predation": 0.05,
    },
    "DENSE_LARGE": {
        "patch_area_m2": 5.0,
        "patch_size": 30,
        "predation": 0.10,
    },
}


def _row(plant: str, predation: float) -> dict[str, str]:
    damaged = int(round(100 * predation))
    undamaged = 100 - damaged
    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "plant_id": plant,
        "flower_id": f"{plant}_F1",
        "assigned_z_level": "Z2",
        "manipulation_setting_id": "SETTING_Z2",
        "realized_exsertion": "0.5",
        "pollination_treatment": "NATURAL",
        "predator_treatment": "EXPOSED",
        "exclusion_method": "SHAM_SLEEVE",
        "water_depth": "10",
        "ovule_count": "100",
        "undamaged_seed_count": str(undamaged),
        "damaged_seed_count": str(damaged),
        "pollen_grains": "12",
        "early_predator_attack_present": "1" if damaged > 0 else "0",
        "mechanical_damage": "0",
    }


def _packet() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows = []
    context = []
    plant_index = 0

    for cell, spec in CELL_PLAN.items():
        for patch_rep in range(2):
            patch_id = f"{cell}_PATCH{patch_rep + 1}"
            for _plant_rep in range(2):
                plant_index += 1
                plant = f"P{plant_index:02d}"
                rows.append(_row(plant, spec["predation"]))
                context.append(
                    {
                        "population_id": "P_REX_TEST",
                        "season_id": "S1",
                        "plant_id": plant,
                        "patch_id": patch_id,
                        "context_measurement_date": "2026-07-01",
                        "patch_area_m2": str(spec["patch_area_m2"]),
                        "patch_size_flowering_plants": str(
                            spec["patch_size"]
                        ),
                        "notes": "",
                    }
                )
    return rows, context


def _surface_receipt(rows: list[dict[str, str]]) -> dict:
    return {
        "system_wrapper_schema_version": (
            "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
        ),
        "system": "Pedicularis rex",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "surface_data_sha256": surface.surface_data_sha256(rows),
        "status": "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE",
    }


def test_historical_density_patch_pattern_is_recovered_without_touching_w0_w5() -> None:
    rows, context = _packet()
    result = build(rows, _surface_receipt(rows), context, _config())

    assert result["status"] == (
        "P2_ANTAGONIST_CONTEXT_PATTERN_CONSISTENT_WITH_XIA2013"
    )
    assert result["historical_comparison_modelable"] is True
    assert result["historical_context_cell_n_patches"] == {
        "DENSE_LARGE": 2,
        "DENSE_SMALL": 2,
        "SPARSE_LARGE": 2,
        "SPARSE_SMALL": 2,
    }
    assert len(result["patch_level_secondary_data"]) == 8
    assert {
        patch["n_plants"] for patch in result["patch_level_secondary_data"]
    } == {2}

    checks = result["historical_pattern_sign_checks"]
    assert checks is not None
    assert all(checks.values())

    contrasts = result["historical_pattern_contrasts"]
    assert contrasts is not None
    assert contrasts["dense_minus_sparse_seed_predation"] < 0
    assert contrasts["sparse_large_minus_small_patch_effect"] < 0
    assert contrasts["dense_large_minus_small_patch_effect"] > 0
    assert contrasts["patch_by_density_difference_in_differences"] > 0
    assert "does_not_change_or_rescue_primary_W0_W5" in result["claim_ceiling"]
    assert (
        "patch_is_the_replication_unit_for_historical_context_comparison"
        in result["claim_ceiling"]
    )


def test_reversed_dense_patch_effect_is_reported_as_not_recovered() -> None:
    rows, context = _packet()
    dense_large = {
        row["plant_id"]
        for row in context
        if row["patch_id"].startswith("DENSE_LARGE_PATCH")
    }
    for row in rows:
        if row["plant_id"] in dense_large:
            row["damaged_seed_count"] = "2"
            row["undamaged_seed_count"] = "98"

    result = build(rows, _surface_receipt(rows), context, _config())

    assert result["historical_comparison_modelable"] is True
    assert result["status"] == "P2_ANTAGONIST_CONTEXT_PATTERN_NOT_RECOVERED"
    assert result["historical_pattern_sign_checks"][
        "large_patch_more_predated_within_dense"
    ] is False


def test_too_few_patches_in_one_historical_cell_is_fail_closed_not_modelable() -> None:
    rows, context = _packet()
    remove_patch = "SPARSE_SMALL_PATCH1"
    remove_plants = {
        row["plant_id"] for row in context if row["patch_id"] == remove_patch
    }
    rows = [row for row in rows if row["plant_id"] not in remove_plants]
    context = [
        row for row in context if row["plant_id"] not in remove_plants
    ]

    result = build(rows, _surface_receipt(rows), context, _config())

    assert result["historical_comparison_modelable"] is False
    assert result["status"] == (
        "P2_ANTAGONIST_CONTEXT_HISTORICAL_COMPARISON_NOT_MODELABLE"
    )
    assert result["historical_context_cell_n_patches"]["SPARSE_SMALL"] == 1
    assert result["historical_pattern_contrasts"] is None
    assert result["historical_pattern_sign_checks"] is None


def test_many_plants_in_one_patch_do_not_count_as_independent_patch_replicates() -> None:
    rows, context = _packet()

    # Remove the second sparse-small patch, then add extra plants to the first
    # one. Plant count rises, but independent patch count remains one.
    remove_patch = "SPARSE_SMALL_PATCH2"
    remove_plants = {
        row["plant_id"] for row in context if row["patch_id"] == remove_patch
    }
    rows = [row for row in rows if row["plant_id"] not in remove_plants]
    context = [
        row for row in context if row["plant_id"] not in remove_plants
    ]

    base = next(
        row for row in context if row["patch_id"] == "SPARSE_SMALL_PATCH1"
    )
    for index in range(20, 24):
        plant = f"P{index}"
        rows.append(_row(plant, 0.40))
        context.append(
            {
                **base,
                "plant_id": plant,
            }
        )

    result = build(rows, _surface_receipt(rows), context, _config())

    assert result["historical_context_cell_n_patches"]["SPARSE_SMALL"] == 1
    assert result["historical_comparison_modelable"] is False


def test_exact_2013_patch_boundary_is_unclassified() -> None:
    rows, context = _packet()

    for row in context:
        if row["patch_id"] == "SPARSE_SMALL_PATCH1":
            row["patch_size_flowering_plants"] = "20"
            row["patch_area_m2"] = "20"

    result = build(rows, _surface_receipt(rows), context, _config())

    assert result["historical_comparison_modelable"] is False
    assert result["historical_context_cell_n_patches"]["SPARSE_SMALL"] == 1


def test_context_registry_must_cover_exactly_all_p2_plants() -> None:
    rows, context = _packet()
    context = context[:-1]

    with pytest.raises(ValueError, match="cover exactly the P2 plants"):
        build(rows, _surface_receipt(rows), context, _config())


def test_context_registry_patch_size_must_be_constant_within_patch() -> None:
    rows, context = _packet()
    same_patch = [
        row for row in context if row["patch_id"] == "SPARSE_SMALL_PATCH1"
    ]
    same_patch[0]["patch_size_flowering_plants"] = "9"

    with pytest.raises(ValueError, match="constant within patch_id"):
        build(rows, _surface_receipt(rows), context, _config())


def test_context_registry_patch_area_must_be_constant_within_patch() -> None:
    rows, context = _packet()
    same_patch = [
        row for row in context if row["patch_id"] == "SPARSE_SMALL_PATCH1"
    ]
    same_patch[0]["patch_area_m2"] = "9"

    with pytest.raises(ValueError, match="patch_area_m2 must be constant"):
        build(rows, _surface_receipt(rows), context, _config())


def test_context_registry_census_date_must_be_constant_within_patch() -> None:
    rows, context = _packet()
    same_patch = [
        row for row in context if row["patch_id"] == "SPARSE_SMALL_PATCH1"
    ]
    same_patch[0]["context_measurement_date"] = "2026-07-02"

    with pytest.raises(
        ValueError,
        match="context_measurement_date must be constant",
    ):
        build(rows, _surface_receipt(rows), context, _config())


def test_patch_density_is_derived_from_patch_size_over_patch_area() -> None:
    rows, context = _packet()
    result = build(rows, _surface_receipt(rows), context, _config())

    by_patch = {
        row["patch_id"]: row for row in result["patch_level_secondary_data"]
    }
    assert by_patch["SPARSE_SMALL_PATCH1"][
        "patch_flowering_density_plants_m2"
    ] == pytest.approx(1.0)
    assert by_patch["DENSE_LARGE_PATCH1"][
        "patch_flowering_density_plants_m2"
    ] == pytest.approx(6.0)


def test_surface_fingerprint_mismatch_is_rejected() -> None:
    rows, context = _packet()
    receipt = _surface_receipt(rows)
    receipt["surface_data_sha256"] = "0" * 64

    with pytest.raises(ValueError, match="exact data used for the P2 surface"):
        build(rows, receipt, context, _config())


def test_context_cutpoints_cannot_be_changed_after_p2_outcomes() -> None:
    rows, context = _packet()
    config = _config()
    config["frozen_before_p2_outcomes"] = False

    with pytest.raises(ValueError, match="frozen before P2 outcomes"):
        build(rows, _surface_receipt(rows), context, config)


def test_context_thresholds_are_historical_not_posthoc() -> None:
    config = _config()
    config["historical_comparison"][
        "large_patch_min_exclusive_flowering_plants"
    ] = 21

    rows, context = _packet()
    with pytest.raises(ValueError, match="one shared excluded value"):
        build(rows, _surface_receipt(rows), context, config)


def test_seed_predation_uses_mean_per_capsule_not_pooled_seeds() -> None:
    # Two capsules with very different developed-seed counts:
    # historical 2013 definition averages 50% and 90%, not 91/102.
    first = _row("P99", 0.5)
    first["flower_id"] = "P99_F1"
    first["damaged_seed_count"] = "1"
    first["undamaged_seed_count"] = "1"
    second = _row("P99", 0.9)
    second["flower_id"] = "P99_F2"
    second["damaged_seed_count"] = "90"
    second["undamaged_seed_count"] = "10"

    result, unresolved = _plant_natural_exposed([first, second])

    assert unresolved == []
    assert result["P99"]["seed_predation_fraction"] == pytest.approx(0.7)
    assert result["P99"]["seed_predation_fraction"] != pytest.approx(91 / 102)
    assert result["P99"]["n_evaluable_natural_exposed_flowers"] == 2


def test_zero_developed_seed_case_is_not_silently_excluded_or_assumed_100_percent() -> None:
    rows, context = _packet()
    flower_id = rows[0]["flower_id"]
    rows[0]["damaged_seed_count"] = "0"
    rows[0]["undamaged_seed_count"] = "0"
    rows[0]["early_predator_attack_present"] = "1"

    result = build(rows, _surface_receipt(rows), context, _config())

    assert result["historical_comparison_modelable"] is False
    assert result["status"] == (
        "P2_ANTAGONIST_CONTEXT_HISTORICAL_COMPARISON_NOT_MODELABLE"
    )
    assert result["unresolved_zero_developed_seed_flower_ids"] == [flower_id]
    assert result["n_unresolved_zero_developed_seed_flowers"] == 1
    assert result["historical_zero_seed_coding_admissible"] is False
    assert result["patch_replication_gate_passed"] is True
    assert result["historical_comparison_not_modelable_reason"] == (
        "UNRESOLVED_ZERO_DEVELOPED_SEED_FATE"
    )
    assert result["historical_pattern_contrasts"] is None
    assert result["historical_pattern_sign_checks"] is None


def test_early_attack_absence_does_not_resolve_zero_seed_fate_either() -> None:
    rows, context = _packet()
    rows[0]["damaged_seed_count"] = "0"
    rows[0]["undamaged_seed_count"] = "0"
    rows[0]["early_predator_attack_present"] = "0"

    result = build(rows, _surface_receipt(rows), context, _config())
    assert result["historical_comparison_modelable"] is False
    assert result["historical_comparison_not_modelable_reason"] == (
        "UNRESOLVED_ZERO_DEVELOPED_SEED_FATE"
    )

from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.build_pedicularis_randomized_pollen_sentinels import (
    build as allocate,
)
from scripts.analyze_pedicularis_randomized_pollen_sentinels import (
    build as analyze,
)
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256


def _levels() -> list[dict[str, str]]:
    return [
        {
            "assigned_z_level": f"Z{i}",
            "assigned_z_rank": str(i),
            "manipulation_setting_id": f"BEND_FIX_Z{i}",
            "manipulation_setting_spec": f"SYNTHETIC_SETTING_Z{i}",
            "sham_control": "1" if i == 4 else "0",
        }
        for i in range(5)
    ]


def _p0() -> dict:
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1",
        "status": "PEDICULARIS_Z_MANIPULATION_VALIDATED",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "z_manipulation_settings": [
            {
                "assigned_z_level": row["assigned_z_level"],
                "assigned_z_rank": int(row["assigned_z_rank"]),
                "manipulation_setting_id": row["manipulation_setting_id"],
            }
            for row in _levels()
        ],
        "field_allocation_verification": {
            "receipt_schema": "PEDICULARIS_P0_RANDOMIZED_ALLOCATION_V1",
            "identity_z_assignment_match": True,
            "allocation_identity_sha256": "f" * 64,
        },
    }


def _flowers() -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_S{flower:02d}",
        }
        for plant in range(12)
        for flower in range(5)
    ]


def _config() -> dict:
    return {
        "schema": "PEDICULARIS_RANDOMIZED_POLLEN_SENTINEL_CONFIG_V1",
        "status": "PEDICULARIS_POLLEN_SENTINEL_INFERENCE_FROZEN_BEFORE_OUTCOMES",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "pollen_assay_method_id": "SYNTHETIC_DESTRUCTIVE_STIGMA_COUNT",
        "prespecified_pollen_sampling_stage": "LATE_ANTHESIS",
        "max_pollen_sampling_age_spread_hours": 2.0,
        "max_mechanical_damage_fraction": 0.0,
        "min_independent_plants": 10,
        "bootstrap_reps": 200,
        "randomization_permutation_reps": 499,
        "random_seed": 27,
        "min_biologically_meaningful_pollen_grains_per_rank": 0.5,
        "min_valid_plant_bootstrap_fraction": 0.80,
        "one_sided_randomization_alpha": 0.05,
        "frozen_before_sentinel_outcomes": True,
        "claim_lane": "RANDOMIZED_POLLINATION_FUNCTION_ONLY_NOT_W1_W2",
    }


def _packet(
    slope: float = 4.0,
) -> tuple[list[dict[str, str]], dict, list[dict[str, str]]]:
    assignments, receipt = allocate(
        _flowers(),
        _levels(),
        _p0(),
        "SENTINEL-PREOUTCOME-SEED",
    )
    filled = []
    for row in assignments:
        rank = int(row["assigned_z_rank"])
        plant = int(row["plant_id"][1:])
        filled.append({
            **row,
            "realized_exsertion": repr(0.1 + 0.17 * rank + 0.001 * plant),
            "pollen_grains": repr(25 + rank * slope + (plant % 3) * 0.2),
            "flower_age_at_sampling_hours": "48",
            "pollen_sampling_stage": "LATE_ANTHESIS",
            "pollen_assay_method_id": "SYNTHETIC_DESTRUCTIVE_STIGMA_COUNT",
            "stigma_removed": "1",
            "mechanical_damage": "0",
        })
    registry = [
        {
            "record_id": f"RS{i:04d}",
            "population_id": row["population_id"],
            "season_id": row["season_id"],
            "plant_id": row["plant_id"],
            "flower_id": row["flower_id"],
            "cohort_role": "POLLEN_SENTINEL",
            "lane": "POLLEN",
            "threshold_basis_eligible": "NO",
            "confirmatory_eligible": "YES",
            "notes": "SYNTHETIC_TEST_ONLY",
        }
        for i, row in enumerate(filled)
    ]
    return filled, receipt, registry


def test_randomized_sentinel_records_real_biological_endpoint_lane_only() -> None:
    rows, receipt, registry = _packet()
    assert receipt["cohort_role"] == "POLLEN_SENTINEL"
    assert receipt["n_allocated_flowers"] == 60
    assert set(receipt["z_manipulation_settings"][i]["assigned_z_level"] for i in range(5)) == {
        f"Z{i}" for i in range(5)
    }
    assert all("undamaged_seed_count" not in row for row in rows)
    assert all("damaged_seed_count" not in row for row in rows)
    assert {row["cohort_role"] for row in registry} == {"POLLEN_SENTINEL"}


def test_randomized_exsertion_increases_pollen_receipt_in_synthetic_positive_world() -> None:
    rows, receipt, registry = _packet(slope=4.0)
    result = analyze(rows, receipt, _p0(), registry, _config())

    assert result["status"] == (
        "RANDOMIZED_EXSERTION_TREATMENT_INCREASES_POLLEN_RECEIPT"
    )
    assert result["assigned_z_rank_itt_slope"] == pytest.approx(4.0)
    assert result["plant_cluster_bootstrap_slope_ci95"][0] > 0.5
    assert result["one_sided_within_plant_randomization_p"] <= 0.05
    assert result["nuisance_checks"]["n_registered_sentinel_plants"] == 12
    assert "not_a_W1_W2_or_causal_compromise_receipt" in result["claim_ceiling"]


def test_negative_pollen_effect_does_not_pass_biological_benefit_gate() -> None:
    rows, receipt, registry = _packet(slope=-2.0)
    result = analyze(rows, receipt, _p0(), registry, _config())
    assert result["status"] == "RANDOMIZED_EXSERTION_POLLEN_BENEFIT_NOT_ESTABLISHED"
    assert result["pollen_benefit_supported_in_tested_population_season"] is False


def test_sentinel_pollen_from_other_flower_must_not_be_copied_to_mature_seed_row() -> None:
    rows, receipt, registry = _packet()
    rows[0]["undamaged_seed_count"] = "52"
    with pytest.raises(ValueError, match="must not be treated as mature-seed"):
        analyze(rows, receipt, _p0(), registry, _config())


def test_flower_substitution_or_changed_z_settings_rejected() -> None:
    rows, receipt, registry = _packet()
    rows[0]["flower_id"] = "SUBSTITUTED"
    with pytest.raises(ValueError, match="drifted from allocation"):
        analyze(rows, receipt, _p0(), registry, _config())

    rows, receipt, registry = _packet()
    rows[0]["manipulation_setting_id"] = "AFTER_OUTCOME"
    with pytest.raises(ValueError, match="drifted from allocation"):
        analyze(rows, receipt, _p0(), registry, _config())


def test_invalid_p0_and_unregistered_sentinel_cohort_are_rejected() -> None:
    rows, receipt, registry = _packet()
    p0 = _p0()
    p0["status"] = "PEDICULARIS_Z_MANIPULATION_NOT_VALIDATED"
    with pytest.raises(ValueError, match="qualified P0"):
        analyze(rows, receipt, p0, registry, _config())

    rows, receipt, registry = _packet()
    registry[0]["cohort_role"] = "FULL_SURFACE"
    registry[0]["lane"] = "P0_P1_G"
    with pytest.raises(ValueError, match="POLLEN_SENTINEL cohort role"):
        analyze(rows, receipt, _p0(), registry, _config())


def test_unfrozen_effect_or_different_assay_fails_closed() -> None:
    rows, receipt, registry = _packet()
    config = _config()
    config["min_biologically_meaningful_pollen_grains_per_rank"] = (
        "REQUIRED_BEFORE_USE"
    )
    with pytest.raises(ValueError, match="prospectively resolved"):
        analyze(rows, receipt, _p0(), registry, config)

    rows, receipt, registry = _packet()
    rows[0]["pollen_assay_method_id"] = "UNREGISTERED"
    with pytest.raises(ValueError, match="differs from prospectively frozen"):
        analyze(rows, receipt, _p0(), registry, _config())


def test_age_spread_must_stay_within_frozen_window() -> None:
    rows, receipt, registry = _packet()
    rows[0]["flower_age_at_sampling_hours"] = "70"
    with pytest.raises(ValueError, match="age varies beyond"):
        analyze(rows, receipt, _p0(), registry, _config())


def test_p0_physical_setting_mismatch_is_rejected_at_allocation() -> None:
    p0 = _p0()
    p0["z_manipulation_settings"][0]["manipulation_setting_id"] = (
        "DIFFERENT_BEND"
    )
    with pytest.raises(ValueError, match="must match the validated P0"):
        allocate(_flowers(), _levels(), p0, "SEED")


def test_registry_prevents_same_flower_reuse_in_pollen_and_seed_cohorts() -> None:
    rows, receipt, registry = _packet()
    seed_row = deepcopy(registry[0])
    seed_row["record_id"] = "SEED_FLOWER_DUPLICATE"
    seed_row["cohort_role"] = "FULL_SURFACE"
    seed_row["lane"] = "P0_P1_G"
    registry.append(seed_row)
    with pytest.raises(ValueError, match="globally unique"):
        analyze(rows, receipt, _p0(), registry, _config())


def test_sentinel_sampling_stage_must_match_prospective_protocol() -> None:
    rows, receipt, registry = _packet()
    rows[0]["pollen_sampling_stage"] = "EARLY_ANTHESIS"

    with pytest.raises(ValueError, match="sampling stage differs"):
        analyze(rows, receipt, _p0(), registry, _config())

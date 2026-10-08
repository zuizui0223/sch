from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256
from scripts.build_pedicularis_randomized_pollen_sentinels import build as pollen_allocate
from scripts.build_pedicularis_two_cohort_fruit_allocation import build as fruit_allocate
from scripts.analyze_pedicularis_two_cohort_ecological_bridge import build as analyze
from scripts import validate_pedicularis_cohort_registry as cohort
from scripts.pedicularis_config_freeze import FREEZE_STATUS


def _levels() -> list[dict[str, str]]:
    return [
        {
            "assigned_z_level": f"Z{z}",
            "assigned_z_rank": str(z),
            "manipulation_setting_id": f"DEVICE_Z{z}",
            "manipulation_setting_spec": f"TEST_PHYSICAL_MANIP_Z{z}",
            "sham_control": "1" if z == 4 else "0",
        }
        for z in range(5)
    ]


def _p0() -> dict:
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1",
        "status": "PEDICULARIS_Z_MANIPULATION_VALIDATED",
        "population_id": "P_REX_SYNTHETIC",
        "season_id": "S1",
        "z_manipulation_settings": [
            {
                "assigned_z_level": level["assigned_z_level"],
                "assigned_z_rank": int(level["assigned_z_rank"]),
                "manipulation_setting_id": level["manipulation_setting_id"],
            }
            for level in _levels()
        ],
        "field_allocation_verification": {
            "receipt_schema": "PEDICULARIS_P0_RANDOMIZED_ALLOCATION_V1",
            "identity_z_assignment_match": True,
            "physical_manipulation_setting_match": True,
        },
    }


def _readiness(p0: dict) -> dict:
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3",
        "status": "PEDICULARIS_FULL_SURFACE_READY",
        "population_id": p0["population_id"],
        "season_id": p0["season_id"],
        "water_y_requirement": "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "predator_method_requirement": (
            "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED"
        ),
        "checks": {
            key: True for key in (
                "same_population_and_season",
                "z_randomized_allocation_verified",
                "z_levels_validated",
                "z_manipulation_settings_validated",
                "p_randomized_allocation_verified",
                "g_randomized_allocation_verified",
                "g_method_timing_validated",
            )
        },
        "validated_execution": {
            "z_levels": [v["assigned_z_level"] for v in _levels()],
            "z_manipulation_settings": p0["z_manipulation_settings"],
            "p_experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
            "g_exclusion_method": "TEST_VALIDATED_G_BARRIER",
            "g_exposed_sham_method": "TEST_G_SHAM",
        },
        "source_receipts": {
            "z": {
                "schema": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1",
                "receipt_sha256": _semantic_sha256(p0),
                "threshold_freeze_status": FREEZE_STATUS,
            },
            "p": {
                "schema": "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1",
                "receipt_sha256": "b" * 64,
                "threshold_freeze_status": FREEZE_STATUS,
            },
            "g": {
                "schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V4",
                "receipt_sha256": "c" * 64,
                "threshold_freeze_status": FREEZE_STATUS,
            },
        },
    }


def _pollen_cfg() -> dict:
    return {
        "schema": "PEDICULARIS_RANDOMIZED_POLLEN_SENTINEL_CONFIG_V1",
        "status": "PEDICULARIS_POLLEN_SENTINEL_INFERENCE_FROZEN_BEFORE_OUTCOMES",
        "population_id": "P_REX_SYNTHETIC",
        "season_id": "S1",
        "pollen_assay_method_id": "SYNTHETIC_STIGMA_SLIDE",
        "prespecified_pollen_sampling_stage": "LATE_ANTHESIS",
        "max_pollen_sampling_age_spread_hours": 3.0,
        "max_mechanical_damage_fraction": 0.0,
        "min_independent_plants": 10,
        "bootstrap_reps": 200,
        "randomization_permutation_reps": 199,
        "random_seed": 123,
        "min_biologically_meaningful_pollen_grains_per_rank": 0.5,
        "min_valid_plant_bootstrap_fraction": 0.8,
        "one_sided_randomization_alpha": 0.05,
        "frozen_before_sentinel_outcomes": True,
        "claim_lane": "RANDOMIZED_POLLINATION_FUNCTION_ONLY_NOT_W1_W2",
    }


def _bridge_cfg() -> dict:
    return {
        "schema": "PEDICULARIS_TWO_COHORT_ECOLOGICAL_BRIDGE_CONFIG_V1",
        "status": "FROZEN_BEFORE_BOTH_COHORT_OUTCOMES",
        "population_id": "P_REX_SYNTHETIC",
        "season_id": "S1",
        "frozen_before_both_cohort_outcomes": True,
        "claim_lane": "TWO_COHORT_NON_GATING_ECOLOGICAL_GEOMETRY_NOT_W1_W2",
        "min_fruit_plants": 10,
        "plant_bootstrap_reps": 200,
        "random_seed": 47,
        "max_water_depth_range": 0.1,
        "max_mechanical_damage_fraction": 0.0,
    }


def _packet(
    *,
    peaked_pollen: bool = False,
    no_optimum_shift: bool = False,
    disjoint_plants: bool = False,
) -> tuple:
    p0 = _p0()
    readiness = _readiness(p0)
    pollen_manifest = [
        {
            "population_id": p0["population_id"],
            "season_id": p0["season_id"],
            "plant_id": f"P{i:02d}",
            "flower_id": f"P{i:02d}_P{j}",
        }
        for i in range(12)
        for j in range(5)
    ]
    pollen_assignment, pollen_allocation = pollen_allocate(
        pollen_manifest, _levels(), p0, "SENTINEL_SEED_BEFORE_OUTCOMES"
    )
    pollen_rows = []
    for row in pollen_assignment:
        rank = int(row["assigned_z_rank"])
        n = int(row["plant_id"][1:])
        grains = (10 + [0, 8, 25, 16, 8][rank]) if peaked_pollen else (10 + 3 * rank)
        pollen_rows.append({
            **row,
            "realized_exsertion": repr(0.2 + rank * 0.1 + n * 0.0001),
            "pollen_grains": str(grains + (n % 3)),
            "flower_age_at_sampling_hours": "48",
            "pollen_sampling_stage": "LATE_ANTHESIS",
            "pollen_assay_method_id": "SYNTHETIC_STIGMA_SLIDE",
            "stigma_removed": "1",
            "mechanical_damage": "0",
        })
    fruit_manifest = [
        {
            "population_id": p0["population_id"],
            "season_id": p0["season_id"],
            "plant_id": f"{'F' if disjoint_plants else 'P'}{i:02d}",
            "flower_id": f"{'F' if disjoint_plants else 'P'}{i:02d}_F{j}",
        }
        for i in range(12)
        for j in range(10)
    ]
    fruit_assignment, fruit_allocation = fruit_allocate(
        fruit_manifest, _levels(), p0, readiness, "FRUIT_SEED_BEFORE_OUTCOMES"
    )
    fruit_rows = []
    for row in fruit_assignment:
        z = int(row["assigned_z_rank"])
        n = int(row["plant_id"][1:])
        if row["predator_treatment"] == "EXCLUDED":
            seeds = 12 + 3 * z
        elif no_optimum_shift:
            seeds = 12 + 3 * z - 2
        else:
            seeds = 22 - 3 * abs(z - 2)
        fruit_rows.append({
            **row,
            "ovule_count": "40",
            "undamaged_seed_count": str(seeds + n % 3),
            "damaged_seed_count": (
                "0" if row["predator_treatment"] == "EXCLUDED" else "3"
            ),
            "water_depth": "1.0",
            "mechanical_damage": "0",
            "early_predator_attack_present": (
                "0" if row["predator_treatment"] == "EXCLUDED" else "1"
            ),
        })
    registry = [
        {
            "record_id": f"PS{index:04d}",
            "population_id": row["population_id"],
            "season_id": row["season_id"],
            "plant_id": row["plant_id"],
            "flower_id": row["flower_id"],
            "cohort_role": "POLLEN_SENTINEL",
            "lane": "POLLEN",
            "threshold_basis_eligible": "NO",
            "confirmatory_eligible": "YES",
            "notes": "SYNTHETIC",
        }
        for index, row in enumerate(pollen_rows)
    ]
    registry.extend([
        {
            "record_id": f"FR{index:04d}",
            "population_id": row["population_id"],
            "season_id": row["season_id"],
            "plant_id": row["plant_id"],
            "flower_id": row["flower_id"],
            "cohort_role": "TWO_COHORT_FRUIT",
            "lane": "FRUIT_P1_G",
            "threshold_basis_eligible": "NO",
            "confirmatory_eligible": "NO",
            "notes": "SYNTHETIC_NOT_CONFIRMATORY",
        }
        for index, row in enumerate(fruit_rows)
    ])
    return (
        pollen_rows, pollen_allocation, p0, registry, _pollen_cfg(),
        fruit_rows, fruit_allocation, readiness, _bridge_cfg()
    )


def test_positive_two_cohort_alignment_does_not_require_same_flower_covariance() -> None:
    packet = _packet()
    result = analyze(*packet)
    assert result["status"] == "TWO_COHORT_DESCRIPTIVE_CONTRAST_NO_W1_W2_PROMOTION"
    assert result["pollen_sentinel_status"] == (
        "RANDOMIZED_EXSERTION_TREATMENT_INCREASES_POLLEN_RECEIPT"
    )
    assert result["plant_overlap_resampling"] == (
        "SAME_PLANTS_DISJOINT_FLOWERS_PAIRED_BOOTSTRAP"
    )
    obs = result["observed_discrete_contrast"]
    assert obs["predator_excluded_optimum_rank"] == 4
    assert obs["predator_exposed_optimum_rank"] == 2
    assert obs["rank_shift_predator_removal"] == 2
    assert obs["pollen_gain_at_shifted_ranks"] == pytest.approx(6.0)
    assert obs["positive_alignment"] is True
    assert result["plant_bootstrap"]["positive_shift_and_positive_pollen_gain_fraction"] > 0.95
    assert result["fruit_nuisance_checks"]["n_fruit_flowers"] == 120
    assert "same_flower_pollen_seed_covariance_not_identified" in result["claim_ceiling"]


def test_interior_pollen_peak_defeats_linear_shift_narrative() -> None:
    packet = _packet(peaked_pollen=True)
    result = analyze(*packet)
    obs = result["observed_discrete_contrast"]
    assert obs["rank_shift_predator_removal"] == 2
    assert result["pollen_sentinel_status"] == (
        "RANDOMIZED_EXSERTION_TREATMENT_INCREASES_POLLEN_RECEIPT"
    )
    assert obs["pollen_gain_at_shifted_ranks"] == pytest.approx(-17)
    assert obs["positive_alignment"] is False
    assert result["plant_bootstrap"]["positive_shift_and_positive_pollen_gain_fraction"] == 0


def test_no_predator_optimum_shift_does_not_become_tradeoff() -> None:
    result = analyze(*_packet(no_optimum_shift=True))
    obs = result["observed_discrete_contrast"]
    assert obs["rank_shift_predator_removal"] == 0
    assert obs["pollen_gain_at_shifted_ranks"] == 0
    assert obs["positive_alignment"] is False


def test_nonoverlapping_plant_sets_bootstrap_separately() -> None:
    result = analyze(*_packet(disjoint_plants=True))
    assert result["plant_overlap_resampling"] == (
        "DISJOINT_PLANTS_INDEPENDENT_BOOTSTRAP"
    )
    assert result["observed_discrete_contrast"]["positive_alignment"] is True


def test_partial_plant_overlap_does_not_use_wrong_covariance_bootstrap() -> None:
    packet = list(_packet())
    fruit_rows = deepcopy(packet[5])
    fruit_alloc = deepcopy(packet[6])
    # One new plant is inadmissible without a revised randomized packet.
    # In this synthetic unit test, preserve the frozen z/G identity by
    # changing every plant ID in both the rows and allocation/registry.
    old = "P00"
    replacement = "X00"
    for row in fruit_rows:
        if row["plant_id"] == old:
            row["plant_id"] = replacement
            row["flower_id"] = row["flower_id"].replace(old, replacement)
    frozen = [
        {field: row[field] for field in (
            "population_id", "season_id", "plant_id", "flower_id",
            "assigned_z_level", "assigned_z_rank", "manipulation_setting_id",
            "sham_control", "pollination_treatment", "predator_treatment",
            "exclusion_method",
        )}
        for row in fruit_rows
    ]
    frozen.sort(key=lambda r: (r["plant_id"], r["flower_id"]))
    fruit_alloc["expected_frozen_rows"] = frozen
    fruit_alloc["allocation_identity_sha256"] = _semantic_sha256(frozen)
    registry = deepcopy(packet[3])
    for row in registry:
        if row["cohort_role"] == "TWO_COHORT_FRUIT" and row["plant_id"] == old:
            row["plant_id"] = replacement
            row["flower_id"] = row["flower_id"].replace(old, replacement)
    packet[3], packet[5], packet[6] = registry, fruit_rows, fruit_alloc
    with pytest.raises(ValueError, match="partially overlapping plant sets"):
        analyze(*packet)


@pytest.mark.parametrize(("index", "change", "error"), [
    (5, ("undamaged_seed_count", "-1"), "consistent integer"),
    (5, ("pollen_grains", "5"), "never borrow sentinel"),
    (5, ("water_depth", "999"), "water-y changed"),
    (5, ("predator_treatment", "EXPOSED" ), "assignments changed"),
])
def test_fruit_source_fails_closed(index: int, change: tuple[str, str], error: str) -> None:
    packet = list(_packet())
    altered = deepcopy(packet[index])
    altered[0][change[0]] = change[1]
    packet[index] = altered
    with pytest.raises(ValueError, match=error):
        analyze(*packet)


def test_sentinel_and_fruit_cannot_share_flower_id_or_silent_pollen_copy() -> None:
    packet = list(_packet())
    rows = deepcopy(packet[5])
    rows[0]["flower_id"] = packet[0][0]["flower_id"]
    packet[5] = rows
    with pytest.raises(ValueError, match="assignments changed"):
        analyze(*packet)


def test_fruit_only_allocation_rejects_unqualified_G_and_wrong_physical_z() -> None:
    packet = _packet()
    p0, readiness = packet[2], packet[7]
    manifest = [
        {key: row[key] for key in (
            "population_id", "season_id", "plant_id", "flower_id"
        )}
        for row in packet[5]
    ]
    bad_ready = deepcopy(readiness)
    bad_ready["checks"]["g_method_timing_validated"] = False
    with pytest.raises(ValueError, match="readiness"):
        fruit_allocate(manifest, _levels(), p0, bad_ready, "SEED")
    bad_levels = deepcopy(_levels())
    bad_levels[0]["manipulation_setting_id"] = "CHANGED_AFTER_P0"
    with pytest.raises(ValueError, match="physical z levels differ"):
        fruit_allocate(manifest, bad_levels, p0, readiness, "SEED")


def test_fruit_registry_role_is_nonconfirmatory_and_stays_independent() -> None:
    packet = _packet()
    result = cohort.validate(packet[3])
    assert result["role_counts"]["TWO_COHORT_FRUIT"] == 120
    assert result["n_exploratory_fruit_plants"] == 12
    assert result["n_calibration_plants"] == 0


def test_bridge_config_cannot_authorize_W1_W2_after_outcomes() -> None:
    packet = list(_packet())
    bad = deepcopy(packet[-1])
    bad["claim_lane"] = "PROMOTE_W1_W2"
    packet[-1] = bad
    with pytest.raises(ValueError, match="cannot promote W1/W2"):
        analyze(*packet)

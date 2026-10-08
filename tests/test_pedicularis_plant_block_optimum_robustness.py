from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_plant_block_optimum_robustness import build
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256
from scripts.build_pedicularis_two_cohort_fruit_allocation import (
    FROZEN_FIELDS, RECEIPT_SCHEMA, RECEIPT_STATUS,
)


def _packet(*, plant_ids=("A","B"), reversed_direction=False):
    rows=[]
    for plant in plant_ids:
        for rank in range(5):
            for g in ("EXCLUDED","EXPOSED"):
                normal=(
                    (1 if g=="EXCLUDED" else 7)
                    if reversed_direction else
                    (7 if g=="EXCLUDED" else 1)
                ) if rank==4 else 3
                if rank==0:
                    normal=1
                row={
                    "population_id":"SYNTHETIC_P_REX",
                    "season_id":"SYNTHETIC_S1",
                    "plant_id":plant,
                    "flower_id":f"{plant}_Z{rank}_{g}",
                    "assigned_z_level":f"Z{rank}",
                    "assigned_z_rank":str(rank),
                    "manipulation_setting_id":f"SETTING_Z{rank}",
                    "sham_control":"0",
                    "pollination_treatment":"NATURAL",
                    "predator_treatment":g,
                    "exclusion_method":(
                        "BARRIER" if g=="EXCLUDED" else "G_SHAM"
                    ),
                    "fate_status":"MATURE_COUNTED",
                    "intact_seeds":str(normal),
                    "damaged_seeds":"0",
                    "seed_stage_proof":"COMPLETE_COUNTED_SEED_FATES",
                    "viable_lower":"",
                    "viable_upper":"",
                    "seed_potential_upper":"10",
                    "seed_potential_upper_basis":"PROSPECTIVELY_FROZEN_UPPER_BOUND",
                    "zero_fate_proof":"",
                    "partial_interval_proof":"",
                }
                if plant=="B" and rank==4 and not reversed_direction:
                    row.update(
                        fate_status="FATE_UNOBSERVED",
                        intact_seeds="",
                        damaged_seeds="",
                        seed_stage_proof="",
                        seed_potential_upper=(
                            "4" if g=="EXCLUDED" else "3"
                        ),
                    )
                rows.append(row)
    frozen=sorted(
        [{f:r[f] for f in FROZEN_FIELDS} for r in rows],
        key=lambda x:(x["plant_id"],x["flower_id"])
    )
    receipt={
        "receipt_schema":RECEIPT_SCHEMA,
        "status":RECEIPT_STATUS,
        "cohort_role":"TWO_COHORT_FRUIT",
        "pollination_treatment":"NATURAL",
        "population_id":"SYNTHETIC_P_REX",
        "season_id":"SYNTHETIC_S1",
        "n_z_levels":5,
        "n_allocated_flowers":len(rows),
        "expected_frozen_rows":frozen,
        "allocation_identity_sha256":_semantic_sha256(frozen),
    }
    return rows,receipt


def test_pooled_guaranteed_shift_can_depend_on_one_plant():
    rows,allocation=_packet()
    r=build(rows,allocation)
    assert r["n_source_plant_blocks"]==2
    assert r["baseline_original_all_plant_shift"]["classification"]==(
        "GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
    )
    assert r["baseline_original_all_plant_shift"][
        "excluded_minus_exposed_rank_shift_outer_interval"
    ]==[1,3]
    loo={x["omitted_plant_id"]:x for x in r["per_omitted_plant_sensitivity"]}
    assert loo["B"]["conditional_optimum_shift"]["classification"]==(
        "GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
    )
    assert loo["A"]["conditional_optimum_shift"]["classification"]==(
        "BOTH_POSITIVE_AND_NEGATIVE_SHIFT_POSSIBLE"
    )
    assert loo["A"]["conditional_optimum_shift"][
        "excluded_minus_exposed_rank_shift_outer_interval"
    ]==[-3,3]
    assert r["omitted_plants_that_change_baseline_classification"]==["A"]
    assert r["n_jackknife_subsets_with_guaranteed_positive_shift"]==1
    assert r[
        "full_sample_guaranteed_positive_shift_robust_to_every_single_plant_deletion"
    ] is False
    assert r["field_data_independently_verified"] is False


def test_three_complete_plants_preserve_shift_after_every_one_plant_removal():
    rows,allocation=_packet(plant_ids=("A","B","C"))
    r=build(rows,allocation)
    assert r["n_full_original_allocated_flowers"]==30
    assert r["n_source_plant_blocks"]==3
    assert r["baseline_original_all_plant_shift"]["classification"]==(
        "GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
    )
    assert r["n_jackknife_subsets_with_guaranteed_positive_shift"]==3
    assert r["omitted_plants_that_change_baseline_classification"]==[]
    assert r[
        "full_sample_guaranteed_positive_shift_robust_to_every_single_plant_deletion"
    ] is True
    for sample in r["per_omitted_plant_sensitivity"]:
        assert sample["n_retained_plant_blocks"]==2
        assert sample["n_retained_allocated_flowers"]==20
        assert sample["is_original_precommitted_allocation_receipt"] is False
        for state in ("EXCLUDED","EXPOSED"):
            for rank in range(5):
                item=sample["bounded_mean_seed_fitness_by_z_and_G"][state][str(rank)]
                assert item["n_retained_fruit_observations"]==2


def test_negative_optimum_shift_could_also_be_jackknife_robust():
    rows,allocation=_packet(
        plant_ids=("A","C","D"), reversed_direction=True
    )
    r=build(rows,allocation)
    assert r["baseline_original_all_plant_shift"]["classification"]==(
        "GUARANTEED_NEGATIVE_EXCLUSION_SHIFT"
    )
    assert r["n_jackknife_subsets_with_guaranteed_negative_shift"]==3
    assert r[
        "full_sample_guaranteed_negative_shift_robust_to_every_single_plant_deletion"
    ] is True


def test_original_allocation_must_validate_before_plant_jackknife():
    rows,allocation=_packet()
    with pytest.raises(ValueError,match="exact allocated"):
        build(rows[:-1],allocation)
    bad=deepcopy(rows)
    bad[0]["predator_treatment"]="EXPOSED"
    with pytest.raises(ValueError,match="exact allocated"):
        build(bad,allocation)
    bad=deepcopy(rows)
    target=next(row for row in bad if row["fate_status"]=="FATE_UNOBSERVED")
    target["intact_seeds"]="0"
    with pytest.raises(ValueError,match="cannot be recoded as zero"):
        build(bad,allocation)


def test_single_plant_does_not_pretend_to_provide_leave_one_out_stability():
    rows,allocation=_packet(plant_ids=("A",))
    with pytest.raises(ValueError,match="at least two complete plant blocks"):
        build(rows,allocation)

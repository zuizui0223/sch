from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import math

import pytest

from scripts.prioritize_pedicularis_fruit_fate_remeasurement import (
    build, one_fruit_sign_tipping,
)
from scripts.build_pedicularis_two_cohort_fruit_allocation import (
    FROZEN_FIELDS, RECEIPT_SCHEMA, RECEIPT_STATUS,
)
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256


def _rows_and_receipt():
    rows=[]
    for plant in ("P1","P2"):
        for z in range(5):
            for g in ("EXCLUDED","EXPOSED"):
                row={
                    "population_id":"SYNTHETIC_P_REX",
                    "season_id":"S1",
                    "plant_id":plant,
                    "flower_id":f"{plant}_Z{z}_{g}",
                    "assigned_z_level":f"Z{z}",
                    "assigned_z_rank":str(z),
                    "manipulation_setting_id":f"M{z}",
                    "sham_control":"0",
                    "pollination_treatment":"NATURAL",
                    "predator_treatment":g,
                    "exclusion_method":"G_BARRIER" if g=="EXCLUDED" else "G_SHAM",
                    "fate_status":"MATURE_COUNTED",
                    "intact_seeds":"3",
                    "damaged_seeds":"0",
                    "seed_stage_proof":"COMPLETE_COUNTED_SEED_FATES",
                    "viable_lower":"","viable_upper":"",
                    "seed_potential_upper":"10",
                    "seed_potential_upper_basis":"PROSPECTIVELY_FROZEN_UPPER_BOUND",
                    "zero_fate_proof":"","partial_interval_proof":"",
                }
                if z==0 and plant=="P1":
                    row["intact_seeds"]="2" if g=="EXCLUDED" else "3"
                if z==0 and plant=="P2":
                    row.update(
                        fate_status="ZERO_VIABLE_VERIFIED",
                        intact_seeds="0",
                        damaged_seeds="",
                        seed_stage_proof="",
                        zero_fate_proof="RECOVERED_EMPTY_PRE_DISPERSAL",
                    )
                if z==4 and plant=="P1":
                    row["intact_seeds"]="7" if g=="EXCLUDED" else "1"
                if z==4 and plant=="P2":
                    row.update(
                        fate_status="FATE_UNOBSERVED",
                        intact_seeds="",damaged_seeds="",seed_stage_proof="",
                        seed_potential_upper="4" if g=="EXCLUDED" else "3",
                    )
                rows.append(row)
    frozen=sorted(
        [{col:r[col] for col in FROZEN_FIELDS} for r in rows],
        key=lambda x:(x["plant_id"],x["flower_id"])
    )
    receipt={
        "receipt_schema":RECEIPT_SCHEMA,
        "status":RECEIPT_STATUS,
        "cohort_role":"TWO_COHORT_FRUIT",
        "pollination_treatment":"NATURAL",
        "population_id":"SYNTHETIC_P_REX",
        "season_id":"S1",
        "n_z_levels":5,
        "n_allocated_flowers":len(rows),
        "expected_frozen_rows":frozen,
        "allocation_identity_sha256":_semantic_sha256(frozen),
    }
    return rows,receipt


def test_exposed_high_z_missing_fruit_has_exact_discriminating_tipping_values():
    rows,allocation=_rows_and_receipt()
    result=build(rows,allocation)
    assert result["status"]=="NON_GATING_ONE_FLOWER_OUTCOME_TIPPING_POINTS"
    assert result["n_original_allocated_flowers"]==20
    assert result["n_currently_uncertain_viable_fruit_outcomes"]==2
    assert result["optimum_shift_after_one_remeasurement_not_claimed"] is True
    assert result["current_finite_sample_optimum_shift_outer_bound"]==[1,3]
    first,second=result["prioritized_conditional_remeasurements"]
    assert first["flower_id"]=="P2_Z4_EXPOSED"
    assert first["n_affected_currently_unresolved_contrasts"]==1
    assert first["n_unresolved_contrasts_with_attainable_single_fruit_sign_certification"]==1
    target=next(x for x in first["affected_prespecified_contrasts"]
                if x["contrast"]=="HIGH_MINUS_LOW_Z")
    assert target["current_sign"]=="CURRENTLY_UNRESOLVED"
    c=target["conditional_ascertainment"]
    assert c["would_certify_positive_if_observed_count_in"]=={
        "minimum_viable_seeds_if_measured":3,
        "maximum_viable_seeds_if_measured":3,
        "n_integer_values":1,
    }
    assert c["would_certify_negative_if_observed_count_in"]=={
        "minimum_viable_seeds_if_measured":0,
        "maximum_viable_seeds_if_measured":1,
        "n_integer_values":2,
    }
    assert c["n_measured_values_that_would_leave_sign_unresolved"]==1
    assert c["maximum_contrast_interval_width_reduction"]["exact"]=="3/2"
    assert c["outcome_value_enumeration_is_not_a_predictive_probability"] is True
    second_target=next(x for x in second["affected_prespecified_contrasts"]
                       if x["contrast"]=="HIGH_MINUS_LOW_Z")
    assert second["flower_id"]=="P2_Z4_EXCLUDED"
    assert second_target["current_sign"]=="ALREADY_POSITIVE"
    assert second["n_unresolved_contrasts_with_attainable_single_fruit_sign_certification"]==0


@pytest.mark.parametrize("sign",[-1,1])
def test_one_flower_tipping_thresholds_match_exhaustive_integer_outcomes(sign):
    # Different n and a,b; other fruits are deliberately still intervals.
    # Compare the threshold solver with direct formula for every admissible x.
    for n in (1,2,5):
        for a,b in ((0,3),(2,8),(4,4)):
            other_low=Fraction(-7,3)
            other_high=Fraction(5,4)
            if sign==1:
                current_low=other_low+Fraction(a,n)
                current_high=other_high+Fraction(b,n)
            else:
                current_low=other_low-Fraction(b,n)
                current_high=other_high-Fraction(a,n)
            t=one_fruit_sign_tipping(
                contrast_lower=current_low,
                contrast_upper=current_high,
                n_fruits_in_target_cell=n,
                current_viable_lower=a,
                current_viable_upper=b,
                cell_direction=sign
            )
            for x in range(a,b+1):
                if sign==1:
                    low=other_low+Fraction(x,n)
                    high=other_high+Fraction(x,n)
                else:
                    low=other_low-Fraction(x,n)
                    high=other_high-Fraction(x,n)
                positive=t["would_certify_positive_if_observed_count_in"]
                negative=t["would_certify_negative_if_observed_count_in"]
                in_pos=(positive is not None
                    and positive["minimum_viable_seeds_if_measured"]<=x<=
                    positive["maximum_viable_seeds_if_measured"])
                in_neg=(negative is not None
                    and negative["minimum_viable_seeds_if_measured"]<=x<=
                    negative["maximum_viable_seeds_if_measured"])
                assert in_pos==(low>0)
                assert in_neg==(high<0)
                assert not(in_pos and in_neg)


def test_nonmissing_source_has_no_reobservation_candidates():
    rows,allocation=_rows_and_receipt()
    for row in rows:
        if row["fate_status"]=="FATE_UNOBSERVED":
            row.update(fate_status="MATURE_COUNTED",
                       intact_seeds="2",damaged_seeds="0",
                       seed_stage_proof="COMPLETE_COUNTED_SEED_FATES")
    result=build(rows,allocation)
    assert result["n_currently_uncertain_viable_fruit_outcomes"]==0
    assert result["prioritized_conditional_remeasurements"]==[]


def test_partially_censored_source_has_narrower_information_gain():
    rows,allocation=_rows_and_receipt()
    target=next(row for row in rows
                if row["flower_id"]=="P2_Z4_EXPOSED")
    target.update(
        fate_status="PARTIALLY_CENSORED",
        viable_lower="1",viable_upper="2",
        partial_interval_proof="DOCUMENTED_INTACT_LOWER_AND_POTENTIAL_SEED_UPPER",
    )
    result=build(rows,allocation)
    candidate=next(x for x in result["prioritized_conditional_remeasurements"]
                   if x["flower_id"]==target["flower_id"])
    assert candidate["maximum_cell_mean_bound_width_reduction"]["exact"]=="1/2"
    assert candidate["observed_viable_seed_lower"]==1
    assert candidate["observed_viable_seed_upper"]==2


@pytest.mark.parametrize("bad",[
    {"contrast_lower":Fraction(2),"contrast_upper":Fraction(1)},
    {"n_fruits_in_target_cell":0},
    {"cell_direction":0},
    {"current_viable_lower":-1},
    {"current_viable_lower":4,"current_viable_upper":3},
])
def test_threshold_rejects_invalid_parameters(bad):
    kwargs={
        "contrast_lower":Fraction(-1),
        "contrast_upper":Fraction(1),
        "n_fruits_in_target_cell":2,
        "current_viable_lower":0,
        "current_viable_upper":4,
        "cell_direction":1,
    }
    kwargs.update(bad)
    with pytest.raises(ValueError,match="invalid interval"):
        one_fruit_sign_tipping(**kwargs)


def test_missing_or_misallocated_source_rows_are_not_accepted_for_triage():
    rows,allocation=_rows_and_receipt()
    with pytest.raises(ValueError,match="exact allocated"):
        build(rows[:-1],allocation)
    corrupted=deepcopy(rows)
    corrupted[0]["assigned_z_rank"]="4"
    with pytest.raises(ValueError,match="exact allocated"):
        build(corrupted,allocation)
    corrupted=deepcopy(rows)
    corrupted[0]["fate_status"]="ZERO_VIABLE_VERIFIED"
    with pytest.raises(ValueError,match="pre-dispersal outcome proof|no inferred"):
        build(corrupted,allocation)

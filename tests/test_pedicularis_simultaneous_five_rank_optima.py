from __future__ import annotations

from copy import deepcopy
import math
import random

import pytest

from scripts.bound_pedicularis_simultaneous_five_rank_optima import (
    CONFIG_SCHEMA, CAP_PROVENANCE, SCHEMA, build,
    hoeffding_radius, possible_optimum_rank_set,
    simultaneous_cell_intervals, sufficient_batches_for_symmetric_gap,
)
from scripts.plan_pedicularis_two_flower_cyclic_blocks import (
    build as allocate, ALLOC_FIELDS,
)
from scripts.simulate_pedicularis_two_flower_detectability import (
    _manifest, _settings,
)


EXCLUDED=(4,6,8,10,14)
EXPOSED=(5,9,11,9,6)
K=25


def _perfect_batch(*, unknown_exposed_high=False):
    b={
        (g,z):(float(curve[z]),float(curve[z]))
        for g,curve in (("EXCLUDED",EXCLUDED),("EXPOSED",EXPOSED))
        for z in range(5)
    }
    if unknown_exposed_high:
        b["EXPOSED",4]=(0.,float(K))
    return b


def _config(cap=K):
    return {
        "schema":CONFIG_SCHEMA,
        "simultaneous_alpha":.05,
        "global_max_intact_seeds_per_flower":cap,
        "global_cap_source_status":CAP_PROVENANCE,
        "independent_batch_randomization_assumed":True,
    }


def _packet(*,n_batches=2,unknown_fates=False):
    manifest=_manifest(n_batches)
    assignments,receipt=allocate(
        manifest,_settings(),
        allocation_seed="PRE_OUTCOME_SIMULTANEOUS_BOUND_TWO_FLOWER_SEED_20261014",
        g_exclusion_candidate_method="CANDIDATE_G_BARRIER_NOT_PILOT_VALIDATED",
        g_exposed_sham_candidate_method="CANDIDATE_G_EXPOSED_SHAM",
    )
    rows=[]
    for row in assignments:
        g=row["predator_treatment"]
        z=int(row["assigned_z_rank"])
        y=EXCLUDED[z] if g=="EXCLUDED" else EXPOSED[z]
        new={
            **{key:row[key] for key in ALLOC_FIELDS},
            "fate_status":"MATURE_COUNTED",
            "intact_seeds":str(y),
            "damaged_seeds":"0",
            "seed_stage_proof":"COMPLETE_COUNTED_SEED_FATES",
            "viable_lower":"","viable_upper":"",
            "seed_potential_upper":str(K),
            "seed_potential_upper_basis":"PROSPECTIVELY_FROZEN_UPPER_BOUND",
            "zero_fate_proof":"","partial_interval_proof":"",
        }
        if (
            unknown_fates and g=="EXPOSED" and z==4
            and row["patch_id"]=="INDEPENDENT_PATCH_000"
        ):
            new.update(
                fate_status="FATE_UNOBSERVED",
                intact_seeds="",damaged_seeds="",seed_stage_proof="",
            )
        rows.append(new)
    return rows,receipt


def test_correct_10_cell_union_radius_counts_randomized_batches_not_flowers():
    r=hoeffding_radius(batches=32,seed_cap=25,alpha=.05)
    expected=25*math.sqrt(math.log(400)/(64))
    assert r==pytest.approx(expected)
    assert 7.64<r<7.66
    # The two flowers per z×G cell in every batch must NOT be
    # counted as 64 independent randomization groups.
    incorrect=hoeffding_radius(batches=64,seed_cap=25,alpha=.05)
    assert r>incorrect
    assert sufficient_batches_for_symmetric_gap(
        hypothetical_gap=2,seed_cap=25,alpha=.05
    )==1873
    assert sufficient_batches_for_symmetric_gap(
        hypothetical_gap=4,seed_cap=25,alpha=.05
    )==469


def test_32_batches_source_like_perfect_profiles_still_cannot_prove_peak_move():
    out=simultaneous_cell_intervals(
        [_perfect_batch() for _ in range(32)],
        seed_cap=25,alpha=.05,
    )
    assert out["n_independently_randomized_batches_assumed"]==32
    assert out["n_simultaneous_cell_means"]==10
    assert out["simultaneous_nominal_coverage"]==pytest.approx(.95)
    a=possible_optimum_rank_set(out["cells"])
    assert a["states"]["EXCLUDED"]["possible_optimum_ranks"]==[0,1,2,3,4]
    assert a["states"]["EXPOSED"]["possible_optimum_ranks"]==[0,1,2,3,4]
    assert a["excluded_minus_exposed_optimum_rank_shift_outer_interval"]==[-4,4]
    assert a["zero_optimum_displacement_ruled_out"] is False


def test_enough_independent_batches_can_certify_discrete_peak_shift_under_ideal_conditions():
    no_missing=[_perfect_batch() for _ in range(1873)]
    out=simultaneous_cell_intervals(no_missing,seed_cap=25,alpha=.05)
    r=out["hoeffding_radius_seeds_per_flower"]
    assert 2*r<2
    a=possible_optimum_rank_set(out["cells"])
    assert a["states"]["EXCLUDED"]=={
        "possible_optimum_ranks":[4],
        "guaranteed_unique_optimum_rank":4
    }
    assert a["states"]["EXPOSED"]=={
        "possible_optimum_ranks":[2],
        "guaranteed_unique_optimum_rank":2
    }
    assert a["excluded_minus_exposed_optimum_rank_shift_outer_interval"]==[2,2]
    assert a["optimum_shift_classification"]=="POSITIVE_SHIFT_SIMULTANEOUSLY_CERTIFIED"
    assert a["zero_optimum_displacement_ruled_out"] is True


def test_structural_maturity_missingness_can_block_shift_at_arbitrarily_large_batch_n():
    b=[_perfect_batch(unknown_exposed_high=True) for _ in range(1873)]
    out=simultaneous_cell_intervals(b,seed_cap=25,alpha=.05)
    result=possible_optimum_rank_set(out["cells"])
    assert 4 in result["states"]["EXPOSED"]["possible_optimum_ranks"]
    assert result["zero_optimum_displacement_ruled_out"] is False
    assert result["optimum_shift_classification"]==(
        "OPTIMUM_DISPLACEMENT_NOT_SIMULTANEOUSLY_IDENTIFIED"
    )


def test_source_receipt_and_missing_mature_outcome_are_retained():
    rows,receipt=_packet(unknown_fates=True)
    r=build(rows,receipt,_config())
    assert r["receipt_schema"]==SCHEMA
    assert r["n_patch_stage_batches"] if "n_patch_stage_batches" in r else (
        r["simultaneous_result"]["n_independently_randomized_batches_assumed"]==2
    )
    assert r["source_field_data_independently_verified"] if (
        "source_field_data_independently_verified" in r
    ) else r["actual_pre_treatment_cap_authentication_completed"] is False
    assert r["actual_pre_treatment_cap_authentication_completed"] is False
    assert r["batch_assignments_independently_randomized_verified"] is False
    assert r["global_seed_cap_K"]==25
    assert r["legacy_descriptive_optimum_outer_interval"]!=[2,2]
    unknown=r["simultaneous_result"]["cells"]["EXPOSED"]["4"]
    assert unknown["mean_observed_fate_lower"]<=6
    assert unknown["mean_observed_fate_upper"]>=6
    assert r["optimum_result"]["zero_optimum_displacement_ruled_out"] is False


def test_source_rerandomization_and_cap_validity_cannot_be_claimed_by_user_values():
    rows,receipt=_packet()
    with pytest.raises(ValueError,match="global biological cap"):
        bad=_config()
        bad["global_cap_source_status"]="MEASURED_AFTER_OUTCOME_EXPOSURE"
        build(rows,receipt,bad)
    with pytest.raises(ValueError,match="source potential seed cap exceeds"):
        build(rows,receipt,_config(cap=14))
    with pytest.raises(ValueError,match="independent source batch"):
        bad=_config()
        bad["independent_batch_randomization_assumed"]=False
        build(rows,receipt,bad)
    with pytest.raises(ValueError,match="source manifest"):
        build(rows[:-1],receipt,_config())
    corrupted=deepcopy(rows)
    corrupted[0]["predator_treatment"]=(
        "EXCLUDED" if corrupted[0]["predator_treatment"]=="EXPOSED"
        else "EXPOSED"
    )
    with pytest.raises(ValueError,match="source manifest"):
        build(corrupted,receipt,_config())


@pytest.mark.parametrize("b,cap,alpha",[(0,25,.05),(2,0,.05),(2,25,0),(2,25,1)])
def test_invalid_distribution_free_radius_inputs_fail_closed(b,cap,alpha):
    with pytest.raises(ValueError,match="Hoeffding requires"):
        hoeffding_radius(batches=b,seed_cap=cap,alpha=alpha)


def test_simultaneous_fitness_rejects_out_of_range_or_incomplete_source_batches():
    b=_perfect_batch()
    b["EXCLUDED",2]=(-1,10)
    with pytest.raises(ValueError,match="outside global potential cap"):
        simultaneous_cell_intervals([b],seed_cap=25,alpha=.05)
    b=_perfect_batch()
    del b["EXPOSED",4]
    with pytest.raises(ValueError,match="missing a registered"):
        simultaneous_cell_intervals([b],seed_cap=25,alpha=.05)


def test_nonidentical_independent_bounded_batch_means_are_covered_simultaneously_in_simulation():
    # This is an extra synthetic concentration sanity check, NOT source
    # randomization qualification. Ten independently simulated cell means
    # (with arbitrary dependence allowed INSIDE a batch) in [0,K].
    rng=random.Random(20261014)
    B=150
    successes=0
    n_sim=300
    for _ in range(n_sim):
        batches=[]
        for b in range(B):
            # Arbitrary batch-specific mean depending on its fixed index.
            # Shared uniforms create strong across-cell correlation.
            u=rng.random()
            v=rng.random()
            row={}
            for j,(g,z) in enumerate(
                (("EXCLUDED",i) for i in range(5))
            ):
                value=25 if (u if j%2 else v)<(.4+.1*(b%3)) else 0
                row[g,z]=(value,value)
            for j in range(5):
                value=25 if (v if j%2 else u)<(.4+.1*(b%3)) else 0
                row["EXPOSED",j]=(value,value)
            batches.append(row)
        result=simultaneous_cell_intervals(
            batches,seed_cap=25,alpha=.05
        )["cells"]
        # Probabilities .4, .5, .6 cycle => across 150 means exactly .5.
        if all(
            result[g][str(z)]["simultaneous_lower"]<=12.5<=
            result[g][str(z)]["simultaneous_upper"]
            for g in ("EXCLUDED","EXPOSED") for z in range(5)
        ):
            successes+=1
    assert successes/n_sim>=.95

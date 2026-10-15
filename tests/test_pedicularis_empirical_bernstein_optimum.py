"""Focus on empirical Bernstein familywise logic, not fake field success."""
from __future__ import annotations

import math
import random
from copy import deepcopy
from fractions import Fraction

import pytest

from scripts.certify_pedicularis_empirical_bernstein_optimum import (
    METHOD,
    SCHEMA,
    empirical_bernstein_one_sided_radius,
    empirical_bernstein_from_patch_cell_bounds,
)

E=(5,7,10,14,19)
X=(5,8,13,8,5)


def blocks(n, *,e=E,x=X,offsets=None):
    return [
        {
            "patch_id":f"INDEPENDENT_PATCH_{i:06d}",
            "stage_block_id":"SYNTHETIC_STAGED_FLOWERING",
            "cells":{
                (arm,z):(v+(offsets[i] if offsets else 0),)*2
                for arm,curve in (("EXCLUDED",e),("EXPOSED",x))
                for z,v in enumerate(curve)
            },
        }
        for i in range(n)
    ]


def cert(b,cap=40):
    return empirical_bernstein_from_patch_cell_bounds(
        b, registered_global_viable_seed_cap=cap,alpha=.05
    )


def test_40_endpoints_and_unbiased_patch_variance():
    example = [Fraction(-3),Fraction(3),Fraction(6)]
    stat = empirical_bernstein_one_sided_radius(
        example,global_seed_cap=40,endpoint_delta=.05/40
    )
    assert stat["empirical_mean"]==2
    assert stat["sample_variance_ddof1"]==21
    assert stat["variance_term"]==pytest.approx(
        math.sqrt(2*21*math.log(2*40/.05)/3)
    )
    report=cert(blocks(3))
    assert report["receipt_schema"]==SCHEMA
    assert report["method"]==METHOD
    assert report["n_simultaneous_pairs"]==20
    assert report["n_one_sided_endpoints"]==40
    assert report["bonferroni_failure_probability_per_endpoint"]==.05/40
    assert report["n_original_distinct_mother_plants_per_batch"]==10
    assert len(report["all_contrast_intervals"])==20
    assert all(row["lower_endpoint_sample_variance_ddof1"]==0 for row in report["all_contrast_intervals"])
    assert report["positive_optimum_shift_certified_conditional_on_assumptions"] is False


def test_noiseless_277_vs_276_is_only_a_synthetic_method_feasibility_result():
    # At K=40 and alpha=.05, nearest-winner gap = 5 seeds/flower.
    # Exact unbiased-variance term is zero, residual range term remains.
    below=cert(blocks(276))
    above=cert(blocks(277))
    assert below["positive_optimum_shift_certified_conditional_on_assumptions"] is False
    assert above["positive_optimum_shift_certified_conditional_on_assumptions"] is True
    assert above["hoeffding_companion_positive_certificate_at_same_nominal_alpha"] is False
    assert above["patch_level_simultaneous_enrolled_batch_mean_rank_sets"][
        "possible_optimum_ranks"]=={"EXCLUDED":[4],"EXPOSED":[2]}
    assert above["patch_level_simultaneous_enrolled_batch_mean_rank_sets"][
        "excluded_minus_exposed_rank_shift_outer_interval"]==[2,2]
    assert above["all_contrast_intervals"][0]["lower_endpoint_radius_before_clipping"]==pytest.approx(
        14*40*math.log(80/.05)/(3*(277-1))
    )


def test_patch_shared_fitness_baseline_cancels_from_paired_z_contrast():
    # Different ecological site productivity can coexist with zero
    # variance in WITHIN-PATCH trait contrasts. Preserve patch pairing.
    arr=blocks(277,offsets=[i%4 for i in range(277)])
    report=cert(arr)
    assert report["positive_optimum_shift_certified_conditional_on_assumptions"] is True
    assert all(item["lower_endpoint_sample_variance_ddof1"]==0 for item in report["all_contrast_intervals"])


def test_trait_specific_patch_heterogeneity_increases_radius():
    base=blocks(100)
    with_noise=deepcopy(base)
    for i,b in enumerate(with_noise):
        # One rank has ±3 source-valid plant-environment interaction.
        key=("EXCLUDED",4)
        v=b["cells"][key][0]+(3 if i%2 else -3)
        b["cells"][key]=(v,v)
    stable=cert(base)
    varying=cert(with_noise)
    target=lambda x: next(i for i in x["all_contrast_intervals"] if
        i["predator_treatment"]=="EXCLUDED" and i["rank_a"]==3 and i["rank_b"]==4)
    assert target(varying)["lower_endpoint_sample_variance_ddof1"]>0
    assert target(varying)["lower_endpoint_radius_before_clipping"]>target(stable)["lower_endpoint_radius_before_clipping"]


def test_missing_maturity_loosens_both_envelope_and_patch_variance():
    full=blocks(277)
    partial=deepcopy(full)
    partial[0]["cells"][("EXCLUDED",4)]=(0,40)
    rf=cert(full)
    rm=cert(partial)
    q=lambda r: next(v for v in r["all_contrast_intervals"] if v["predator_treatment"]=="EXCLUDED" and v["rank_a"]==3 and v["rank_b"]==4)
    assert q(rm)["finite_allocated_batch_mean_fate_interval"][0]<q(rf)["finite_allocated_batch_mean_fate_interval"][0]
    assert q(rm)["finite_allocated_batch_mean_fate_interval"][1]>q(rf)["finite_allocated_batch_mean_fate_interval"][1]
    assert q(rm)["lower_endpoint_sample_variance_ddof1"]>0
    # Losing one optimal-z fate prevents identification of exact best rank,
    # but may still preserve strictly positive direction (z3 or z4).
    assert rm["patch_level_simultaneous_enrolled_batch_mean_rank_sets"]["possible_optimum_ranks"]["EXCLUDED"] == [3,4]
    assert rm["positive_optimum_shift_certified_conditional_on_assumptions"] is True
    for b in partial[:40]:
        b["cells"][("EXCLUDED",4)] = (0,40)
    assert cert(partial)["positive_optimum_shift_certified_conditional_on_assumptions"] is False


def test_same_G_curves_cannot_certify_displacement_even_large_B():
    result=cert(blocks(1000,e=X,x=X))
    assert result["positive_optimum_shift_certified_conditional_on_assumptions"] is False
    assert result["patch_level_simultaneous_enrolled_batch_mean_rank_sets"]["possible_optimum_ranks"]=={
        "EXCLUDED":[2],"EXPOSED":[2]
    }
    assert result["patch_level_simultaneous_enrolled_batch_mean_rank_sets"][
        "excluded_minus_exposed_rank_shift_outer_interval"]==[0,0]


def test_invalid_independence_and_range_fail_closed():
    bad=blocks(3)
    bad[1]["patch_id"]=bad[0]["patch_id"]
    bad[1]["stage_block_id"]="LATER_STAGE"
    with pytest.raises(ValueError,match="same patch cannot serve"):
        cert(bad)
    with pytest.raises(ValueError,match="at least two independent"):
        cert(blocks(1))
    with pytest.raises(ValueError,match="seed fate means"):
        cert(blocks(3),cap=18)
    with pytest.raises(ValueError,match="simultaneous alpha"):
        empirical_bernstein_from_patch_cell_bounds(blocks(3),registered_global_viable_seed_cap=40,alpha=1.0)
    with pytest.raises(ValueError,match="contrast exceeds registered"):
        empirical_bernstein_one_sided_radius([Fraction(0),Fraction(41)],global_seed_cap=40,endpoint_delta=.001)


def test_simulated_sharp_no_G_shift_keeps_all_true_optima_under_CI():
    rng=random.Random(250519)
    for rep in range(15):
        bb=[]
        for i in range(60):
            # Two G states have exactly the same known distribution;
            # true expected contrast is zero for ALL z pairs.
            bb.append({
                "patch_id":f"TRIAL_{rep}_{i}","stage_block_id":"SYNTHETIC",
                "cells":{(g,z):(v,v) for g in ("EXCLUDED","EXPOSED")
                         for z in range(5)
                         for v in [rng.randint(0,40)]}
            })
        r=cert(bb)
        assert not r["positive_optimum_shift_certified_conditional_on_assumptions"]
        assert not r["patch_level_simultaneous_enrolled_batch_mean_rank_sets"][
            "simultaneous_rank_shift_direction"].startswith("GUARANTEED_NEGATIVE")


def test_real_source_contract_from_existing_frozen_two_flower_allocation():
    """Integration: authenticates assigned IDs/fates, not a field treatment."""
    from scripts.certify_pedicularis_empirical_bernstein_optimum import build
    from scripts.plan_pedicularis_two_flower_cyclic_blocks import (
        build as allocate, ALLOC_FIELDS,
    )
    from scripts.simulate_pedicularis_two_flower_detectability import (
        _manifest, _settings,
    )

    allocation, receipt = allocate(
        _manifest(2),_settings(),
        allocation_seed="PRECOMMITTED_EMPIRICAL_BERNSTEIN_SYNTHETIC_20261015",
        g_exclusion_candidate_method="G_BARRIER_UNQUALIFIED",
        g_exposed_sham_candidate_method="G_SHAM_UNQUALIFIED",
    )
    rows=[]
    for r in allocation:
        z=int(r["assigned_z_rank"])
        y=E[z] if r["predator_treatment"]=="EXCLUDED" else X[z]
        rows.append({
            **{f:r[f] for f in ALLOC_FIELDS},
            "fate_status":"MATURE_COUNTED",
            "intact_seeds":str(y),
            "damaged_seeds":"0",
            "seed_stage_proof":"COMPLETE_COUNTED_SEED_FATES",
            "viable_lower":"",
            "viable_upper":"",
            "seed_potential_upper":"40",
            "seed_potential_upper_basis":"PROSPECTIVELY_FROZEN_UPPER_BOUND",
            "zero_fate_proof":"",
            "partial_interval_proof":"",
        })
    report=build(rows,receipt,registered_global_viable_seed_cap=40)
    assert report["original_registered_flower_count"]==40
    assert report["n_source_fruit_outcomes_unresolved"]==0
    assert report["source_allocation_identity_sha256"]
    assert report["source_fate_analysis_sha256"]
    assert report["n_independent_patch_stage_batches"]==2
    assert not report["positive_optimum_shift_certified_conditional_on_assumptions"]
    tampered=deepcopy(rows)
    tampered[0]["assigned_z_rank"]="4" if tampered[0]["assigned_z_rank"]!="4" else "0"
    with pytest.raises(ValueError,match="frozen source manifest"):
        build(tampered,receipt,registered_global_viable_seed_cap=40)
    with pytest.raises(ValueError,match="registered global K"):
        build(rows,receipt,registered_global_viable_seed_cap=35)

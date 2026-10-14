from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
import math
import random

import pytest

from scripts.certify_pedicularis_simultaneous_optimum_rank import (
    SCHEMA, _rank_sets_from_pair_bands, build,
    simultaneous_from_batch_cell_bounds,
)
from scripts.plan_pedicularis_two_flower_cyclic_blocks import (
    build as allocate, ALLOC_FIELDS,
)
from scripts.simulate_pedicularis_two_flower_detectability import (
    _manifest, _settings,
)

E=[5,7,10,14,19]
X=[5,8,13,8,5]


def _cells(*,excluded=None,exposed=None,cap=40):
    e=E if excluded is None else excluded
    x=X if exposed is None else exposed
    return {
        (g,z):(val,val)
        for g,curve in (("EXCLUDED",e),("EXPOSED",x))
        for z,val in enumerate(curve)
    }


def _blocks(n:int, *,cap=40):
    return [
        {
            "patch_id":f"INDEPENDENT_PATCH_{i:05d}",
            "stage_block_id":"MATCHED_FLOWERING_STAGE",
            "cells":_cells(cap=cap),
        } for i in range(n)
    ]


def _source_packet(n_batches=2):
    manifest=_manifest(n_batches)
    alloc,receipt=allocate(
        manifest,_settings(),
        allocation_seed="PRECOMMITTED_SIMULTANEOUS_RANK_METHOD_20261014",
        g_exclusion_candidate_method="G_BARRIER_UNQUALIFIED",
        g_exposed_sham_candidate_method="G_SHAM_UNQUALIFIED",
    )
    rows=[]
    for r in alloc:
        z=int(r["assigned_z_rank"])
        y=E[z] if r["predator_treatment"]=="EXCLUDED" else X[z]
        rows.append({
            **{field:r[field] for field in ALLOC_FIELDS},
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
    return rows,receipt


def test_simultaneous_family_is_exactly_twenty_with_only_patch_sample_size():
    report=simultaneous_from_batch_cell_bounds(
        _blocks(4),registered_global_viable_seed_cap=40,alpha=.05
    )
    assert report["receipt_schema"]==SCHEMA
    assert report["n_independent_patch_stage_batches"]==4
    assert report["n_original_distinct_mother_plants_per_batch"]==10
    assert report["n_original_fruit_flowers_per_batch"]==20
    assert report["n_simultaneous_two_sided_pairwise_difference_bands"]==20
    assert report["n_one_sided_endpoints_protected_by_union_bound"]==40
    eps=40*math.sqrt(2*math.log(40/.05)/4)
    assert report["per_contrast_Hoeffding_half_width_before_physical_clipping"] == pytest.approx(eps)
    assert report["per_contrast_Hoeffding_half_width_before_physical_clipping"]>40
    assert len(report["all_contrast_intervals"])==20
    assert report["descriptive_finite_allocated_sample_rank_sets"][
        "possible_optimum_ranks"
    ] == {"EXCLUDED":[4], "EXPOSED":[2]}
    assert report["descriptive_finite_allocated_sample_rank_sets"][
        "excluded_minus_exposed_rank_shift_outer_interval"
    ]==[2,2]
    assert report["patch_level_simultaneous_population_rank_sets"][
        "possible_optimum_ranks"
    ]=={"EXCLUDED":[0,1,2,3,4],"EXPOSED":[0,1,2,3,4]}
    assert report["patch_level_simultaneous_population_rank_sets"][
        "excluded_minus_exposed_rank_shift_outer_interval"
    ]==[-4,4]
    assert report["positive_optimum_shift_certified_conditional_on_assumptions"] is False


def test_distribution_free_bounds_need_hundreds_of_independent_patches_even_noiseless():
    # Independent patch vectors are hypothetical here. We are testing
    # the sample-size cost of a *rigorous worst-case* Hoeffding radius,
    # NOT recommending that many P. rex field populations be recruited.
    lower=simultaneous_from_batch_cell_bounds(
        _blocks(855),registered_global_viable_seed_cap=40
    )
    higher=simultaneous_from_batch_cell_bounds(
        _blocks(856),registered_global_viable_seed_cap=40
    )
    assert lower["per_contrast_Hoeffding_half_width_before_physical_clipping"] > 5
    assert higher["per_contrast_Hoeffding_half_width_before_physical_clipping"] < 5
    assert lower["positive_optimum_shift_certified_conditional_on_assumptions"] is False
    assert higher["positive_optimum_shift_certified_conditional_on_assumptions"] is True
    assert higher["patch_level_simultaneous_population_rank_sets"][
        "possible_optimum_ranks"
    ]=={"EXCLUDED":[4],"EXPOSED":[2]}
    assert higher["patch_level_simultaneous_population_rank_sets"][
        "excluded_minus_exposed_rank_shift_outer_interval"
    ]==[2,2]


def test_source_locked_five_rank_fruit_fate_intervals_are_retained_without_imputation():
    rows,receipt=_source_packet()
    result=build(rows,receipt,registered_global_viable_seed_cap=40)
    assert result["original_registered_flower_count"]==40
    assert result["n_independent_patch_stage_batches"]==2
    assert result["n_source_fruit_outcomes_unresolved"]==0
    assert result["descriptive_finite_allocated_sample_rank_sets"][
        "excluded_minus_exposed_rank_shift_outer_interval"
    ]==[2,2]
    assert result["positive_optimum_shift_certified_conditional_on_assumptions"] is False
    # A missing high-exsertion outcome has [0,40], not a fabricated 0.
    partially=deepcopy(rows)
    missing=next(r for r in partially if
                 r["predator_treatment"]=="EXCLUDED" and
                 r["assigned_z_rank"]=="4")
    missing.update(
        fate_status="FATE_UNOBSERVED",intact_seeds="",
        damaged_seeds="",seed_stage_proof="",
    )
    after=build(partially,receipt,registered_global_viable_seed_cap=40)
    assert after["n_source_fruit_outcomes_unresolved"]==1
    target=next(x for x in after["all_contrast_intervals"] if
                x["predator_treatment"]=="EXCLUDED" and
                x["rank_a"]==3 and x["rank_b"]==4)
    assert target["finite_allocated_batch_mean_fate_interval"][0]<0
    assert target["finite_allocated_batch_mean_fate_interval"][1]>0
    assert after["positive_optimum_shift_certified_conditional_on_assumptions"] is False


def test_source_randomized_plants_and_registered_cap_cannot_be_tampered():
    rows,receipt=_source_packet()
    broken=deepcopy(rows)
    broken[0]["assigned_z_rank"]="4"
    with pytest.raises(ValueError,match="frozen source manifest"):
        build(broken,receipt,registered_global_viable_seed_cap=40)
    with pytest.raises(ValueError,match="registered global K"):
        build(rows,receipt,registered_global_viable_seed_cap=35)
    with pytest.raises(ValueError,match="at least two independent"):
        one,receipt1=_source_packet(n_batches=1)
        build(one,receipt1,registered_global_viable_seed_cap=40)
    with pytest.raises(ValueError,match="simultaneous alpha"):
        build(rows,receipt,registered_global_viable_seed_cap=40,alpha=1.0)


def test_repeated_patch_with_different_stages_must_not_be_two_independent_clusters():
    block=_blocks(3)
    block[1]["patch_id"]=block[0]["patch_id"]
    block[1]["stage_block_id"]="LATER_FLOWERING"
    with pytest.raises(ValueError,match="same patch cannot serve"):
        simultaneous_from_batch_cell_bounds(
            block,registered_global_viable_seed_cap=40
        )


def test_every_rank_optimum_is_retained_when_all_differences_have_zero_true_mean():
    rng=random.Random(1111)
    # Each patch has ten equally exchangeable random counts, so true
    # expected means are equal: the entire five-rank set should be retained
    # on simultaneous coverage. These generated source blocks are iid.
    for trial in range(30):
        blocks=[]
        for patch in range(12):
            values={
                (g,z):(v,v)
                for g in ("EXCLUDED","EXPOSED")
                for z in range(5)
                for v in [rng.randrange(41)]
            }
            blocks.append({
                "patch_id":f"TRIAL_{trial}_PATCH_{patch}",
                "stage_block_id":"STAGE",
                "cells":values,
            })
        cert=simultaneous_from_batch_cell_bounds(
            blocks,registered_global_viable_seed_cap=40
        )
        assert cert["patch_level_simultaneous_population_rank_sets"][
            "possible_optimum_ranks"
        ]=={"EXCLUDED":[0,1,2,3,4],"EXPOSED":[0,1,2,3,4]}


def test_monotone_certified_pairwise_bounds_eliminate_only_inferior_ranks():
    bands={}
    for g in ("EXCLUDED","EXPOSED"):
        values=E if g=="EXCLUDED" else X
        for a in range(5):
            for b in range(a+1,5):
                d=values[a]-values[b]
                bands[(g,a,b)]=(d-.1,d+.1)
    result=_rank_sets_from_pair_bands(bands)
    assert result["possible_optimum_ranks"]=={
        "EXCLUDED":[4],"EXPOSED":[2]
    }
    assert result["excluded_minus_exposed_rank_shift_outer_interval"]==[2,2]


@pytest.mark.parametrize(
    ("invalid","message"),
    [
        ({"patch_id":"","stage_block_id":"s","cells":_cells()},
         "patch and developmental"),
        ({"patch_id":"P","stage_block_id":"s","cells":{}},
         "all five ranks"),
    ],
)
def test_unsupported_batch_schema_fails_closed(invalid,message):
    source=[invalid, _blocks(1)[0]]
    with pytest.raises(ValueError,match=message):
        simultaneous_from_batch_cell_bounds(
            source,registered_global_viable_seed_cap=40
        )

from __future__ import annotations

from collections import Counter
from copy import deepcopy
from fractions import Fraction

import pytest

from scripts.plan_pedicularis_two_flower_cyclic_blocks import (
    ALLOC_FIELDS, build as design, STATUS as DESIGN_STATUS,
)
from scripts.analyze_pedicularis_two_flower_cyclic_fruit_bounds import (
    build as analyze,
)


def _levels():
    return [
        {
            "assigned_z_level":f"Z{z}",
            "assigned_z_rank":str(z),
            "manipulation_setting_id":f"MECHANICAL_SETTING_Z{z}",
            "sham_control":"1" if z==4 else "0",
        }
        for z in range(5)
    ]


def _manifest(*, n_batches=2):
    return [
        {
            "population_id":"SYNTHETIC_P_REX",
            "season_id":"PRE_FIELD_PILOT",
            "patch_id":f"PATCH_{b}",
            "stage_block_id":"MATCHED_ANTHESIS",
            "plant_id":f"B{b}_P{i:02d}",
            "flower_id":f"B{b}_P{i:02d}_F{f}",
            "flower_position_code":f"FLOWER_POSITION_{f}",
        }
        for b in range(n_batches)
        for i in range(10)
        for f in range(2)
    ]


def _candidate(rows):
    return design(
        rows,_levels(),allocation_seed="SEED_FROZEN_BEFORE_FIELD_20261009",
        g_exclusion_candidate_method="CANDIDATE_NO_WATER_CHANGE_G_BARRIER",
        g_exposed_sham_candidate_method="CANDIDATE_G_EXPOSED_SHAM",
    )


def _fates(alloc):
    rows=[]
    for row in alloc:
        z=int(row["assigned_z_rank"])
        g=row["predator_treatment"]
        viable=9 if g=="EXCLUDED" and z==4 else (
            1 if g=="EXPOSED" and z==4 else
            1 if z==0 else 3
        )
        rows.append({
            **{field:row[field] for field in ALLOC_FIELDS},
            "fate_status":"MATURE_COUNTED",
            "intact_seeds":str(viable),
            "damaged_seeds":"0",
            "seed_stage_proof":"COMPLETE_COUNTED_SEED_FATES",
            "viable_lower":"",
            "viable_upper":"",
            "seed_potential_upper":"10",
            "seed_potential_upper_basis":"PROSPECTIVELY_FROZEN_UPPER_BOUND",
            "zero_fate_proof":"",
            "partial_interval_proof":"",
        })
    return rows


def test_two_flower_cyclic_design_exact_incidence_and_plant_G_randomization():
    alloc,receipt=_candidate(_manifest())
    assert receipt["status"]==DESIGN_STATUS
    assert receipt["n_patch_stage_batches"]==2
    assert receipt["n_plants"]==20
    assert receipt["n_allocated_fruit_flowers"]==40
    assert receipt["max_required_fruit_flowers_per_plant"]==2
    assert receipt["n_per_z_by_G_per_patch_stage_batch"]==2
    assert receipt["G_randomization_unit"]=="PLANT"
    assert receipt["plant_incidence_graph"]=="CONNECTED_FIVE_CYCLE_NOT_PAIRWISE_BALANCED"
    assert receipt["status_not_field_qualification"] is True
    assert len(alloc)==40
    byplant={}
    for row in alloc:
        byplant.setdefault(row["plant_id"],[]).append(row)
    assert all(len(rows)==2 for rows in byplant.values())
    for rows in byplant.values():
        assert len({x["predator_treatment"] for x in rows})==1
        assert len({x["assigned_z_rank"] for x in rows})==2
        assert sorted(int(x["assigned_z_rank"]) for x in rows) in (
            [0,1],[1,2],[2,3],[3,4],[0,4]
        )
    freq=Counter((
        r["patch_id"],r["predator_treatment"],r["assigned_z_rank"]
    ) for r in alloc)
    assert len(freq)==20
    assert set(freq.values())=={2}
    for patch in ("PATCH_0","PATCH_1"):
        assert len({r["plant_id"] for r in alloc
                    if r["patch_id"]==patch and
                    r["predator_treatment"]=="EXCLUDED"})==5
        assert len({r["plant_id"] for r in alloc
                    if r["patch_id"]==patch and
                    r["predator_treatment"]=="EXPOSED"})==5


def test_randomization_slots_give_equal_marginal_z_and_G_probability_per_flower():
    # Uniform permutation of plants over ten slots + independent flower
    # randomization over the two z levels in each slot. Each labeled
    # flower has chance 2/(10*2) = 1/10 of each z x G treatment.
    for g in ("EXCLUDED","EXPOSED"):
        for z in range(5):
            count=0
            for slot in range(10):
                arm="EXCLUDED" if slot<5 else "EXPOSED"
                ranks=(slot%5,(slot%5+1)%5)
                if arm==g:
                    count+=sum(1 for level in ranks if level==z)
            assert Fraction(count,10*2)==Fraction(1,10)


def test_salted_randomization_is_reproducible_under_manifest_reordering():
    original=_manifest()
    first,receipt=_candidate(original)
    rearranged,_=_candidate(list(reversed(original)))
    freeze=lambda rows: sorted(
        [{k:r[k] for k in ALLOC_FIELDS} for r in rows],
        key=lambda x:x["flower_id"],
    )
    assert freeze(first)==freeze(rearranged)
    assert receipt["allocation_identity_sha256"]==_candidate(
        list(reversed(original))
    )[1]["allocation_identity_sha256"]
    other,_=design(
        original,_levels(),allocation_seed="DIFFERENT_BUT_FROZEN_SEED_20261009",
        g_exclusion_candidate_method="CANDIDATE_NO_WATER_CHANGE_G_BARRIER",
        g_exposed_sham_candidate_method="CANDIDATE_G_EXPOSED_SHAM",
    )
    assert freeze(first)!=freeze(other)


def test_candidate_fitness_curve_optimum_shifts_with_distinct_plant_units():
    allocation,receipt=_candidate(_manifest())
    report=analyze(_fates(allocation),receipt)
    assert report["status"]==(
        "NON_GATING_TWO_FLOWER_PLANT_RANDOMIZED_CANDIDATE_DESCRIPTIVE"
    )
    assert report["n_plants"]==20
    assert report["n_fruit_flowers"]==40
    assert report["n_patch_stage_batches"]==2
    assert report["G_randomization_unit"]=="PLANT"
    for g in ("EXCLUDED","EXPOSED"):
        for z in range(5):
            cell=report["mean_fitness_by_predator_state_and_z"][g][str(z)]
            assert cell["n_distinct_plant_units"]==4
            assert cell["n_fruits"]==4
    assert report["possible_state_specific_optima"]["EXCLUDED"][
        "possible_discrete_optimum_ranks"
    ]==[4]
    assert report["possible_state_specific_optima"]["EXPOSED"][
        "possible_discrete_optimum_ranks"
    ]==[1,2,3]
    assert report["excluded_minus_exposed_possible_optimum_shift_outer_interval"]==[
        1,3
    ]
    assert report["guaranteed_positive_rank_shift_conditional_on_fate_caps"] is True
    assert report["full_randomization_inference_and_plant_cluster_CI_implemented"] is False
    assert report["observed_field_data_independently_verified"] is False


def test_zero_yield_is_distinct_from_unobserved_yield():
    alloc,receipt=_candidate(_manifest(n_batches=1))
    rows=_fates(alloc)
    target=next(r for r in rows
                if r["predator_treatment"]=="EXCLUDED" and r["assigned_z_rank"]=="4")
    target.update(
        fate_status="ZERO_VIABLE_VERIFIED",
        intact_seeds="0",damaged_seeds="",seed_stage_proof="",
        zero_fate_proof="RECOVERED_EMPTY_PRE_DISPERSAL",
    )
    missing=next(r for r in rows
                 if r["predator_treatment"]=="EXPOSED" and r["assigned_z_rank"]=="4")
    missing.update(
        fate_status="FATE_UNOBSERVED",
        intact_seeds="",damaged_seeds="",seed_stage_proof="",
    )
    out=analyze(rows,receipt)
    assert out["mean_fitness_by_predator_state_and_z"]["EXCLUDED"]["4"][
        "mean_viable_seed_count_per_flower_bounds"
    ]==[{"exact":"9/2","value":4.5},{"exact":"9/2","value":4.5}]
    assert out["mean_fitness_by_predator_state_and_z"]["EXPOSED"]["4"][
        "n_unresolved_fruit_fates"
    ]==1
    assert out["guaranteed_positive_rank_shift_conditional_on_fate_caps"] is False


@pytest.mark.parametrize(("break_it","message"),[
    (lambda rows:rows[:-1],"ten plants|exactly two|stratum"),
    (lambda rows:[dict(r,plant_id="B0_P00") if r["plant_id"]=="B0_P09" else r
                  for r in rows],"ten plants|exactly two"),
    (lambda rows:[dict(r,flower_id=rows[0]["flower_id"]) if i==1 else r
                  for i,r in enumerate(rows)],"globally unique"),
    (lambda rows:[dict(r,flower_position_code="FLOWER_POSITION_0")
                  if r["plant_id"]=="B0_P00" else r for r in rows],
     "distinguishable"),
])
def test_source_design_rejects_bad_plant_and_flower_sourcing(break_it,message):
    with pytest.raises(ValueError,match=message):
        _candidate(break_it(_manifest(n_batches=1)))


def test_source_design_requires_five_distinct_physical_levels_and_seed():
    m=_manifest(n_batches=1)
    with pytest.raises(ValueError,match="five z settings"):
        design(
            m,_levels()[:4],allocation_seed="VALID_LARGE_SEED_20261009",
            g_exclusion_candidate_method="G1",g_exposed_sham_candidate_method="G0",
        )
    with pytest.raises(ValueError,match="seed >=12"):
        design(
            m,_levels(),allocation_seed="weak",
            g_exclusion_candidate_method="G1",g_exposed_sham_candidate_method="G0",
        )


def test_any_changed_z_G_or_missing_fruit_after_freeze_fails_closed():
    alloc,receipt=_candidate(_manifest(n_batches=1))
    rows=_fates(alloc)
    with pytest.raises(ValueError,match="frozen source manifest"):
        analyze(rows[:-1],receipt)
    bad=deepcopy(rows)
    bad[0]["predator_treatment"]=(
        "EXPOSED" if bad[0]["predator_treatment"]=="EXCLUDED" else "EXCLUDED"
    )
    with pytest.raises(ValueError,match="frozen source manifest"):
        analyze(bad,receipt)
    bad=deepcopy(rows)
    bad[0]["intact_seeds"]="11"
    with pytest.raises(ValueError,match="integer intact"):
        analyze(bad,receipt)
    bad=deepcopy(rows)
    bad[0]["fate_status"]="FATE_UNOBSERVED"
    with pytest.raises(ValueError,match="cannot be recoded"):
        analyze(bad,receipt)


def test_frozen_complete_block_receipt_cannot_be_passed_as_two_flower_design():
    alloc,receipt=_candidate(_manifest(n_batches=1))
    receipt["status"]="FICTITIOUS_QUALIFIED_G"
    with pytest.raises(ValueError,match="frozen prospective"):
        analyze(_fates(alloc),receipt)

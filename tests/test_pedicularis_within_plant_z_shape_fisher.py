from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.fisher_pedicularis_within_plant_z_shape import (
    SCHEMA, _per_pair_raw_terms, _validate_edge_pairs, build,
    fisher_within_plant_shape_pairs,
)
from scripts.fisher_pedicularis_plant_pair_G_randomization import (
    _p_from_stats, fisher_from_pairs,
)
from scripts.simulate_pedicularis_plant_pair_fisher_calibration import (
    simulate_pairs,
)
from scripts.plan_pedicularis_two_flower_cyclic_blocks import (
    build as allocate, ALLOC_FIELDS,
)
from scripts.simulate_pedicularis_two_flower_detectability import (
    _manifest, _settings,
)


def _pairs(mode="PREDATOR_EXCLUSION_SHIFTS_PEAK",batches=1, *,
           seed=13579,patch_sd=0,plant_sd=0,flower_sd=0,
           heterogeneous_G_sd=0):
    return simulate_pairs(
        scenario_mode=mode,n_batches=batches,seed=seed,cap=40,
        patch_sd=patch_sd,plant_sd=plant_sd,flower_sd=flower_sd,
        heterogeneous_G_sd=heterogeneous_G_sd,
    )


def _source_rows(*,missing=False):
    assignments,receipt=allocate(
        _manifest(1),_settings(),
        allocation_seed="FROZEN_SHARP_WITHIN_PLANT_FISHER_EXPERIMENT_20261013",
        g_exclusion_candidate_method="G_CANDIDATE_UNQUALIFIED",
        g_exposed_sham_candidate_method="G_SHAM_CANDIDATE_UNQUALIFIED",
    )
    E=(5,7,10,14,19)
    X=(5,8,13,8,5)
    rows=[]
    for a in assignments:
        z=int(a["assigned_z_rank"])
        y=E[z] if a["predator_treatment"]=="EXCLUDED" else X[z]
        rows.append({
            **{key:a[key] for key in ALLOC_FIELDS},
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
    if missing:
        rows[0].update(
            fate_status="FATE_UNOBSERVED",
            intact_seeds="",damaged_seeds="",seed_stage_proof="",
        )
    return rows,receipt


def test_symmetric_five_edge_graph_is_exact_z4_vs_z2_difference_of_differences():
    pairs=_pairs()
    batches,terms=_per_pair_raw_terms(pairs)
    assert batches==1
    assert terms==[1,2,9,8,14]
    result=fisher_within_plant_shape_pairs(pairs)
    assert result["cycle_twice_weights"]==[-1,-1,1,1,-1]
    assert result["observed_exact_twice_weighted_numerator"]==34
    assert result["observed_relative_exsertion_advantage_count_per_flower"]==17
    assert result["target_sign"]=="POSITIVE"
    assert result["n_randomization_statistics"]==32
    assert result["p_calculation"]=="EXACT_CONDITIONAL_ENUMERATION"
    assert result["one_sided_Fisher_sharp_null_p"]==pytest.approx(1/32)
    assert result["plant_specific_common_additive_G_seed_gain_allowed_under_null"] is True
    # Old peak midrank is a distinct, generally less sensitive statistic.
    old=fisher_from_pairs(pairs)
    assert old["observed_predeclared_peak_statistic"][
        "exclusion_minus_exposure_peak_midrank"
    ]==2
    assert old["one_sided_Fisher_sharp_null_p"]>=result["one_sided_Fisher_sharp_null_p"]


def test_fixed_additive_gain_and_changed_shape_with_same_peak_do_not_move_target():
    for mode in ("COMMON_ADDITIVE_G_GAIN","CHANGED_G_BY_Z_SAME_PEAK"):
        r=fisher_within_plant_shape_pairs(_pairs(mode))
        assert r["observed_relative_exsertion_advantage_count_per_flower"]==0
        assert r["target_sign"]=="ZERO"
        assert r["one_sided_Fisher_sharp_null_p"]>=.5


def test_plant_specific_additive_gain_cancels_in_both_flower_seed_differences():
    baseline=_pairs("SHARP_NO_G_EFFECT",patch_sd=0,plant_sd=2,
                    flower_sd=1,seed=23)
    variant=deepcopy(baseline)
    for p in variant:
        # Arbitrary gain within each plant, different across matched pairs,
        # but constant over the parent's two assigned z levels.
        gain=2+(p["edge"]%4)
        for z in p["excluded"]["by_z"]:
            p["excluded"]["by_z"][z]+=gain
    before=_per_pair_raw_terms(baseline)[1]
    after=_per_pair_raw_terms(variant)[1]
    assert before==after
    assert fisher_within_plant_shape_pairs(
        baseline
    )["one_sided_Fisher_sharp_null_p"]==fisher_within_plant_shape_pairs(
        variant
    )["one_sided_Fisher_sharp_null_p"]


def test_within_plant_difference_sharp_null_is_exactly_superuniform_for_32_swaps():
    pairs=_pairs("SHARP_NO_G_EFFECT",seed=113,patch_sd=1,
                 plant_sd=3,flower_sd=2)
    n,contributions=_per_pair_raw_terms(pairs)
    assert n==1
    all_statistics=[
        sum(-term if mask&(1<<j) else term
            for j,term in enumerate(contributions))
        for mask in range(32)
    ]
    pvalues=[
        _p_from_stats(t,all_statistics,exact=True)["one_sided_Fisher_sharp_null_p"]
        for t in all_statistics
    ]
    for alpha in (.01,.05,.10,.20,.5,1.0):
        assert sum(v<=alpha+1e-12 for v in pvalues)/32<=alpha+1e-12


def test_four_batch_monte_carlo_is_reproducible_for_source_edge_pairs():
    pairs=_pairs(batches=4,seed=91,patch_sd=1,plant_sd=2,flower_sd=1)
    r=fisher_within_plant_shape_pairs(pairs,
          monte_carlo_permutations=999,random_seed=765432)
    changed=fisher_within_plant_shape_pairs(
        list(reversed(pairs)),monte_carlo_permutations=999,
        random_seed=765432
    )
    # With deterministic keyed random masks, row order is a source identity
    # dimension. We require deterministic repeated calls on same order;
    # reversal need not have same MC p because it remaps the flips.
    again=fisher_within_plant_shape_pairs(
        pairs,monte_carlo_permutations=999,random_seed=765432
    )
    assert r==again
    assert changed["n_matched_plant_pairs"]==r["n_matched_plant_pairs"]
    assert r["n_matched_plant_pairs"]==20
    assert r["p_calculation"]=="MONTE_CARLO_PLUS_ONE_INCLUDE_OBSERVED_REFERENCE"
    assert r["one_sided_Fisher_sharp_null_p"]>=1/1000
    assert 0<=r["one_sided_Fisher_sharp_null_p"]<=1


def test_source_locked_full_fate_build_and_allocation_protection():
    rows,receipt=_source_rows()
    result=build(rows,receipt)
    assert result["receipt_schema"]==SCHEMA
    assert result["n_distinct_mother_plants"]==10
    assert result["n_assigned_fruit_flowers"]==20
    assert result["observed_relative_exsertion_advantage_count_per_flower"]==17
    assert result["one_sided_Fisher_sharp_null_p"]==pytest.approx(1/32)
    assert result["source_field_data_independently_verified"] is False
    assert result["weak_null_of_equal_population_optimum_ranks_tested"] is False
    assert result["status"]=="NON_GATING_SHARP_WITHIN_PLANT_RESPONSE_NULL_ONLY"
    bad=deepcopy(rows)
    bad[0]["predator_treatment"]=(
        "EXPOSED" if bad[0]["predator_treatment"]=="EXCLUDED"
        else "EXCLUDED"
    )
    with pytest.raises(ValueError,match="frozen source manifest"):
        build(bad,receipt)
    with pytest.raises(ValueError,match="frozen source manifest"):
        build(rows[:-1],receipt)


def test_unknown_maturity_is_not_fabricated_as_intact_seeds():
    rows,receipt=_source_rows(missing=True)
    with pytest.raises(ValueError,match="exact mature seed"):
        build(rows,receipt)


def test_broken_edge_geometry_or_bad_method_inputs_fail_closed():
    pairs=_pairs()
    with pytest.raises(ValueError,match="complete 5-edge"):
        _validate_edge_pairs(pairs[:4])
    corrupted=deepcopy(pairs)
    corrupted[0]["excluded"]["by_z"]={0:4,4:3}
    with pytest.raises(ValueError,match="same cyclic"):
        fisher_within_plant_shape_pairs(corrupted)
    with pytest.raises(ValueError,match="random seed invalid"):
        fisher_within_plant_shape_pairs(pairs,random_seed=-1)
    with pytest.raises(ValueError,match="permutations or random seed invalid"):
        fisher_within_plant_shape_pairs(pairs,monte_carlo_permutations=10)

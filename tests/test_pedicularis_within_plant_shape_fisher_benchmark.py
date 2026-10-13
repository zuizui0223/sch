from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.benchmark_pedicularis_within_plant_shape_fisher import (
    MATERNAL_NULL, build, integer_maternal_additive_control,
)
from scripts.fisher_pedicularis_within_plant_z_shape import (
    _per_pair_raw_terms, fisher_within_plant_shape_pairs,
)
from scripts.fisher_pedicularis_plant_pair_G_randomization import (
    fisher_from_pairs, _p_from_stats,
)
from scripts.simulate_pedicularis_plant_pair_fisher_calibration import (
    SCHEMA, simulate_pairs,
)


def _config():
    return {
        "schema":SCHEMA,
        "patch_stage_batch_grid":[1],
        "replicates_per_condition":10,
        "random_seed":20261013,
        "intact_seeds_upper_cap":40,
        "one_sided_alpha":.05,
        "monte_carlo_permutations":999,
        "plant_sd":1,
        "flower_sd":1,
        "patch_sd":1,
        "G_gain_plant_heterogeneity_sd":2,
        "scenario_modes":[
            "SHARP_NO_G_EFFECT",
            "COMMON_ADDITIVE_G_GAIN",
            "CHANGED_G_BY_Z_SAME_PEAK",
            "PREDATOR_EXCLUSION_SHIFTS_PEAK",
        ],
    }


def test_comparative_benchmark_uses_distinct_valid_sharp_null_claims():
    r=build(_config())
    assert r["status"]=="SYNTHETIC_CONTRAST_STATISTIC_COMPARISON_NOT_FIELD_INFERENCE"
    assert r["n_generated_simulated_studies"]==50
    assert len(r["scenario_grid"])==5
    assert r["tested_population_optimum_shift_weak_null"] is False
    assert r["maternal_integer_null_sharp_for_pair_differences"] is True
    assert r["two_nulls_are_distinct_and_must_not_be_CONFLATED"] is True
    names={x["mode"] for x in r["scenario_grid"]}
    assert MATERNAL_NULL in names
    for item in r["scenario_grid"]:
        assert item["n_eligible_plants"]==10
        assert item["n_simulated_assignments"]==10
        assert 0<=item["fraction_peak_midrank_Fisher_rejections"]<=1
        assert 0<=item["fraction_within_plant_shape_Fisher_rejections"]<=1
        lo,hi=item["shape_rejection_Wilson95_simulation_interval"]
        assert lo<=item["fraction_within_plant_shape_Fisher_rejections"]<=hi
        assert item["null_of_peak_midrank"]!=item["null_of_shape"]


def test_integer_heterogeneous_maternal_gain_is_exact_sharp_difference_null():
    original=simulate_pairs(
        scenario_mode="SHARP_NO_G_EFFECT",
        n_batches=1,seed=441122,cap=40,
        patch_sd=1,plant_sd=3,flower_sd=2,
        heterogeneous_G_sd=0,
    )
    shifted=integer_maternal_additive_control(original,seed=551122)
    assert _per_pair_raw_terms(original)==_per_pair_raw_terms(shifted)
    p0=fisher_within_plant_shape_pairs(original)
    p1=fisher_within_plant_shape_pairs(shifted)
    assert p0["observed_relative_exsertion_advantage_count_per_flower"]==p1[
        "observed_relative_exsertion_advantage_count_per_flower"
    ]
    assert p0["one_sided_Fisher_sharp_null_p"]==p1[
        "one_sided_Fisher_sharp_null_p"
    ]
    assert any(
        shifted[j]["excluded"]["by_z"]!=original[j]["excluded"]["by_z"]
        for j in range(len(original))
    )
    for a in shifted:
        assert all(0<=y<=40 for y in a["excluded"]["by_z"].values())


def test_exact_sharp_difference_null_size_under_all_32_assignments_even_with_additive_gain():
    original=simulate_pairs(
        scenario_mode="SHARP_NO_G_EFFECT",
        n_batches=1,seed=121212,cap=40,
        patch_sd=1,plant_sd=3,flower_sd=2,
        heterogeneous_G_sd=0,
    )
    shifted=integer_maternal_additive_control(original,seed=676767)
    n,terms=_per_pair_raw_terms(shifted)
    assert n==1
    stat=[
        sum(-t if (mask & (1<<i)) else t
            for i,t in enumerate(terms))
        for mask in range(32)
    ]
    pvals=[
        _p_from_stats(t,stat,exact=True)["one_sided_Fisher_sharp_null_p"]
        for t in stat
    ]
    for alpha in (.01,.05,.10,.20,.50,1.):
        assert sum(p<=alpha+1e-12 for p in pvals)/32<=alpha+1e-12


def test_peak_shift_statistic_is_not_adequate_substitute_for_shape_contrast():
    pairs=simulate_pairs(
        scenario_mode="PREDATOR_EXCLUSION_SHIFTS_PEAK",
        n_batches=1,seed=314159,cap=40,
        patch_sd=0,plant_sd=0,flower_sd=0,
        heterogeneous_G_sd=0,
    )
    peak=fisher_from_pairs(pairs)
    shape=fisher_within_plant_shape_pairs(pairs)
    assert peak["observed_peak_shift_direction"]=="POSITIVE"
    assert shape["observed_relative_exsertion_advantage_count_per_flower"]==17
    assert shape["one_sided_Fisher_sharp_null_p"]==pytest.approx(1/32)
    assert peak["one_sided_Fisher_sharp_null_p"]>=shape[
        "one_sided_Fisher_sharp_null_p"
    ]


def test_benchmark_is_reproducible_for_frozen_potential_outcome_generator():
    c=_config()
    assert build(c)==build(deepcopy(c))


def test_weak_null_not_claimed_even_when_shape_null_rejected():
    result=build(_config())
    assert result["tested_population_optimum_shift_weak_null"] is False
    assert "shape_contrast_rejection_not_proof_of_any_fitness_argmax_change" in result[
        "claim_ceiling"
    ]

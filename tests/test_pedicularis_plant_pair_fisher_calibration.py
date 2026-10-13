from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.fisher_pedicularis_plant_pair_G_randomization import (
    _p_from_stats, fisher_from_pairs, statistic, uniform_additive_G_sensitivity,
)
from scripts.simulate_pedicularis_plant_pair_fisher_calibration import (
    SCHEMA, RESULT, _validate, _wilson, _subseed, build, simulate_pairs,
)


def _config():
    return {
        "schema": SCHEMA,
        "patch_stage_batch_grid": [1, 2],
        "replicates_per_condition": 10,
        "random_seed": 20261011,
        "intact_seeds_upper_cap": 40,
        "one_sided_alpha": .05,
        "monte_carlo_permutations": 999,
        "plant_sd": 0.,
        "flower_sd": 0.,
        "patch_sd": 0.,
        "G_gain_plant_heterogeneity_sd": 0.,
        "scenario_modes": [
            "SHARP_NO_G_EFFECT",
            "COMMON_ADDITIVE_G_GAIN",
            "CHANGED_G_BY_Z_SAME_PEAK",
            "PREDATOR_EXCLUSION_SHIFTS_PEAK",
        ],
    }


def _pairs(mode, batches=1, *, noise=False, seed=314159):
    return simulate_pairs(
        scenario_mode=mode,n_batches=batches,seed=seed,cap=40,
        patch_sd=1 if noise else 0,
        plant_sd=2 if noise else 0,
        flower_sd=1 if noise else 0,
        heterogeneous_G_sd=2,
    )


def test_hash_substreams_satisfy_exact_Fisher_63_bit_seed_contract():
    for source_seed in (0,1,17,20261011,2**63-1):
        for serial in range(100):
            generated=_subseed(source_seed,"FISHER_SWAPS",str(serial))
            assert type(generated) is int
            assert 0<=generated<=2**63-1
    assert _subseed(20261011,"PLANT_G_RANDOMIZATION") != _subseed(
        20261011,"POTENTIAL_OUTCOMES"
    )


def test_sharp_null_exhaustive_whole_plant_assignment_fisher_type_I_control():
    pairs=_pairs("SHARP_NO_G_EFFECT",noise=True)
    assert len(pairs)==5
    stats=[
        statistic(pairs,mask)["exclusion_minus_exposure_peak_midrank"]
        for mask in range(32)
    ]
    pvalues=[
        _p_from_stats(t,stats,exact=True)["one_sided_Fisher_sharp_null_p"]
        for t in stats
    ]
    for alpha in (0.01,.05,.10,.20,.50,1.0):
        assert sum(p<=alpha+1e-12 for p in pvalues)/32 <= alpha+1e-12
    assert all(0<p<=1 for p in pvalues)


def test_positive_peak_shift_is_separate_from_fisher_null_rejection():
    additive=_pairs("COMMON_ADDITIVE_G_GAIN")
    same_peak=_pairs("CHANGED_G_BY_Z_SAME_PEAK")
    changed=_pairs("PREDATOR_EXCLUSION_SHIFTS_PEAK")
    assert statistic(additive)["exclusion_minus_exposure_peak_midrank"]==0
    assert statistic(same_peak)["exclusion_minus_exposure_peak_midrank"]==0
    assert statistic(changed)["exclusion_minus_exposure_peak_midrank"]==2
    add_test=fisher_from_pairs(additive)
    assert 0<=add_test["one_sided_Fisher_sharp_null_p"]<=1
    additive_union=uniform_additive_G_sensitivity(additive)
    assert 3 in [
        row["hypothesized_constant_seed_gain_per_flower"]
        for row in additive_union["individual_sharp_tau_sensitivity"]
    ]
    assert additive_union["not_test_of_weak_same_population_peak_null"] is True


def test_potential_outcome_generator_preserves_whole_plant_pair_design():
    pairs=_pairs("HETEROGENEOUS_PLANT_G_GAIN",batches=4,noise=True)
    assert len(pairs)==20
    assert len({
        (p["patch_id"],p["stage_block_id"],p["edge"]) for p in pairs
    })==20
    for pair in pairs:
        assert pair["excluded"]["plant_id"]!=pair["exposed"]["plant_id"]
        ranks={pair["edge"],(pair["edge"]+1)%5}
        for g in ("excluded","exposed"):
            assert set(pair[g]["by_z"])==ranks
            assert all(0<=y<=40 for y in pair[g]["by_z"].values())
    out=fisher_from_pairs(pairs,monte_carlo_permutations=999,random_seed=7)
    assert out["n_matched_plant_pairs"]==20
    assert out["p_calculation"]=="MONTE_CARLO_PLUS_ONE_INCLUDE_OBSERVED_REFERENCE"


def test_synthetic_calibration_run_has_explicit_null_and_power_claim_limits():
    out=build(_config())
    assert out["receipt_schema"]==RESULT
    assert out["n_total_generated_synthetic_datasets"]==80
    assert len(out["scenario_grid"])==8
    for cell in out["scenario_grid"]:
        assert cell["n_simulated_allocations"]==10
        assert cell["n_matched_plant_pairs"] in (5,10)
        assert cell["one_sided_alpha"]==.05
        assert cell["weak_null_same_optimum_tested"] is False
        assert 0<=cell["fraction_Fisher_sharp_null_rejections"]<=1
        assert 0<=cell["fraction_positive_descriptive_peak_shifts"]<=1
        assert cell["n_both_rejected_and_descriptively_positive"]<=(
            cell["n_Fisher_sharp_null_rejections"]
        )
        lo,hi=cell["simulation_rejection_fraction_Wilson95"]
        assert lo<=cell["fraction_Fisher_sharp_null_rejections"]<=hi
    assert "no_weak_null_test_for_equal_population_optimum_ranks" in out["claim_ceiling"]


def test_same_frozen_config_repeats_all_result_statistics_exactly():
    cfg=_config()
    one=build(cfg)
    two=build(deepcopy(cfg))
    assert one==two


@pytest.mark.parametrize(
    ("field","value","error"),
    [
        ("replicates_per_condition",1,"replicates"),
        ("patch_stage_batch_grid",[1,1],"batch grid"),
        ("one_sided_alpha",.5,"one-sided alpha"),
        ("intact_seeds_upper_cap",0,"cap"),
        ("scenario_modes",["INVALID"],"scenario modes"),
        ("scenario_modes",["SHARP_NO_G_EFFECT"]*2,"scenario modes"),
        ("random_seed",-1,"seed"),
        ("G_gain_plant_heterogeneity_sd",-1,"heterogeneity_sd"),
    ]
)
def test_invalid_synthetic_scenario_config_fails_closed(field,value,error):
    cfg=_config()
    cfg[field]=value
    with pytest.raises(ValueError,match=error):
        _validate(cfg)


def test_binomial_wilson_is_not_a_field_effect_confidence_interval():
    assert _wilson(0,40)[0]==0
    assert 0<_wilson(0,40)[1]<0.10
    assert _wilson(40,40)[1]==1
    assert _wilson(20,40)[0]<.5<_wilson(20,40)[1]

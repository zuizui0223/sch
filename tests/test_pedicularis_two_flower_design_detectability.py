from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.simulate_pedicularis_two_flower_detectability import (
    SCHEMA, _config, _limiting_identification, _one_replicate,
    _possible_optima, _screening_requirement, build,
)


def _fixture(*, missing=0.0, plant_sd=0.0, null=False):
    original={
        "EXCLUDED":[4,6,8,10,14],
        "EXPOSED":[5,9,11,9,6],
    }
    if null:
        original["EXCLUDED"]=list(original["EXPOSED"])
    scene={
        "scenario_id":"SYNTHETIC_TEST",
        "fitness_curve_seed_counts":original,
        "patch_sd":0.0, "plant_sd":plant_sd, "flower_sd":0.0,
        "missingness_mechanism":"MCAR",
        "maturity_fate_missing_rate":missing,
        "include_plant_deletion_diagnostic":True,
    }
    config={
        "schema":SCHEMA,
        "patch_stage_batch_grid":[1,2],
        "replicates_per_grid_point":10,
        "random_seed":17,
        "maximum_intact_seeds_per_flower":25,
        "scenarios":[scene],
    }
    return config,scene


def test_hypothetical_eligible_plant_screening_is_exact_binomial_not_observed_field_supply():
    r=_screening_requirement(1,0.5,0.95)
    assert r["minimal_plants_screened_per_batch"]==28
    assert r["required_eligible_plants_per_batch"]==10
    assert r["assumed_probability_every_batch_can_fill"]>=0.95
    assert r["binomial_eligibility_screening_is_not_field_observation"] is True
    assert _screening_requirement(1,0.3,0.95)[
        "minimal_plants_screened_per_batch"
    ]==49
    assert _screening_requirement(1,0.8,0.95)[
        "minimal_plants_screened_per_batch"
    ]==16
    assert _screening_requirement(4,0.5,0.95)[
        "minimal_plants_screened_per_batch"
    ]==32
    assert _screening_requirement(4,0.5,0.95)[
        "total_plants_screened_across_batches"
    ]==128
    assert _screening_requirement(1,1.0,0.95)[
        "minimal_plants_screened_per_batch"
    ]==10


def test_all_original_synthetic_cyclic_design_slots_yield_correct_shift():
    c,scene=_fixture()
    for n_batch in (1,2,4):
        for seed in (11,22,33):
            result=_one_replicate(
                scene=scene,n_batches=n_batch,cap=25,seed=seed,
                check_plant_deletion=True,
            )
            assert result["full_latent_positive"]
            assert result["source_bounded_positive"]
            assert result["plant_deletion_stable_positive"]
            assert result["n_lost_fruit_outcomes"]==0


def test_no_shift_null_is_not_falsely_called_positive_without_noise():
    c,scene=_fixture(null=True)
    for seed in (1,5,9):
        result=_one_replicate(
            scene=scene,n_batches=2,cap=25,seed=seed,
            check_plant_deletion=True,
        )
        assert result["full_latent_positive"] is False
        assert result["source_bounded_positive"] is False


def test_missingness_bounds_cannot_claim_positive_when_latent_completion_contradicts():
    c,scene=_fixture(missing=0.3,plant_sd=3.0)
    for seed in range(12):
        result=_one_replicate(
            scene=scene,n_batches=1,cap=25,seed=seed,
            check_plant_deletion=True,
        )
        if result["source_bounded_positive"]:
            assert result["full_latent_positive"] is True
        if result["plant_deletion_stable_positive"]:
            assert result["source_bounded_positive"] is True


def test_ideal_uniform_missing_fraction_gives_structural_nonidentification_at_high_missing():
    c,scene=_fixture(missing=0.10)
    low=_limiting_identification(scene,25)
    assert low["guaranteed_positive"] is True
    assert low["excluded_possible"]==[4]
    assert low["exposed_possible"]==[1,2,3]
    scene=deepcopy(scene)
    scene["maturity_fate_missing_rate"]=0.15
    high=_limiting_identification(scene,25)
    assert high["guaranteed_positive"] is False
    assert 3 in high["excluded_possible"]
    assert 3 in high["exposed_possible"]
    # The gap is not driven by sampling noise: even the idealized
    # infinite-data deterministic interval remains ambiguous.


def test_configuration_grid_runs_and_does_not_report_calibrated_power():
    config,scene=_fixture()
    result=build(config)
    assert result["receipt_schema"]=="SCH_TWO_FLOWER_SCENARIO_DETECTABILITY_V1"
    assert result["status"]=="SYNTHETIC_HIERARCHICAL_DESIGN_DETECTABILITY_NOT_POWER"
    assert result["n_random_synthetic_datasets"]==20
    assert result["sample_size_requirement_calibrated_from_focal_empirical_variance"] is False
    assert result["no_nominal_alpha_or_valid_p_values_computed"] is True
    assert [(x["n_plants"],x["n_per_z_by_G"]) for x in result["scenario_grid"]]==[
        (10,2),(20,4)
    ]
    for item in result["scenario_grid"]:
        assert item["fraction_complete_latent_guaranteed_positive_shift"]==1
        assert item["fraction_fate_bounded_guaranteed_positive_shift"]==1
        assert item["fraction_fate_bounded_positive_and_stable_to_plant_deletion"]==1
        assert item["mean_fraction_missing_mature_fruit_outcomes"]==0


def test_distinct_patch_effect_plant_effect_and_missingness_are_preserved():
    config,scene=_fixture(missing=0.1,plant_sd=4)
    scene["patch_sd"]=3
    scene["flower_sd"]=1.0
    result=build(config)
    assert result["n_random_synthetic_datasets"]==20
    for row in result["scenario_grid"]:
        assert 0<=row["fraction_fate_bounded_guaranteed_positive_shift"]<=1
        assert 0<=row["fraction_complete_latent_guaranteed_positive_shift"]<=1
        assert (
            row["fraction_fate_bounded_guaranteed_positive_shift"]
            <=row["fraction_complete_latent_guaranteed_positive_shift"]
        )
        assert (
            row["fraction_fate_bounded_positive_and_stable_to_plant_deletion"]
            <=row["fraction_fate_bounded_guaranteed_positive_shift"]
        )


@pytest.mark.parametrize(
    ("field","value","error"),
    [
        ("replicates_per_grid_point",2,"replicates"),
        ("patch_stage_batch_grid",[0],"batch_grid"),
        ("patch_stage_batch_grid",[1,1],"unique"),
        ("maximum_intact_seeds_per_flower",0,"maximum_intact"),
        ("random_seed",-1,"random_seed"),
    ],
)
def test_unrun_plant_deletion_diagnostic_is_null_not_false_zero_rate():
    config, scene=_fixture()
    scene["include_plant_deletion_diagnostic"]=False
    result=build(config)
    for item in result["scenario_grid"]:
        assert item["plant_deletion_diagnostic_evaluated"] is False
        assert item["fraction_fate_bounded_positive_and_stable_to_plant_deletion"] is None
        assert item["fraction_fate_bounded_guaranteed_positive_shift"]==1


def test_invalid_scenario_configuration_fails_closed(field,value,error):
    c,scene=_fixture()
    c[field]=value
    with pytest.raises(ValueError,match=error):
        _config(c)


def test_false_input_source_and_invalid_mechanism_rejected():
    c,scene=_fixture()
    c["schema"]="REPORTED_FIELD_POWER"
    with pytest.raises(ValueError,match="schema"):
        build(c)
    c,scene=_fixture()
    scene["missingness_mechanism"]="PREDATOR_EXCLUSION_CAUSALLY_QUALIFIED"
    with pytest.raises(ValueError,match="missingness"):
        build(c)
    c,scene=_fixture()
    scene["fitness_curve_seed_counts"]["EXPOSED"]=[100]*5
    with pytest.raises(ValueError,match="exceeds source cap"):
        build(c)


def test_possible_optima_checks_extreme_trait_rank_identification_not_only_gradient():
    cells={
        "EXCLUDED":{i:(1.0,1.0) for i in range(5)},
        "EXPOSED":{i:(1.0,1.0) for i in range(5)},
    }
    cells["EXCLUDED"][4]=(5,5)
    cells["EXPOSED"][2]=(5,5)
    result=_possible_optima(cells)
    assert result["guaranteed_positive"] is True
    assert result["outer_rank_shift"]==[2,2]
    cells["EXPOSED"][4]=(4,6)
    updated=_possible_optima(cells)
    assert updated["guaranteed_positive"] is False
    assert updated["outer_rank_shift"]==[0,2]

"""Regression and source-grain tests for eight original experimental programmes."""
from __future__ import annotations

from copy import deepcopy
import math

import pytest

from scripts.analyze_sch_experimental_pollen_meta_8_programmes import (
    ACON,BROWN,LOB,TRIF,MAIN_STUDY_N,STUDIES,
    build,load,new_aconitum,new_lobelia_siphilitica,
    new_lobelia_cardinalis,new_trifolium,
    flower_number_partial_meta,preexisting_frozen_edges,
    sign_test,
)


def test_complete_main_family_is_eight_studies_not_forty_one_replicates():
    data=build()
    assert data["independent_study_units"]==8
    assert data["n_matched_trait_context_edges"]==41
    assert data["n_matched_edges_with_original_SEs"]==40
    assert len(data["programme_summaries"])==8
    assert set(data["programme_summaries"])==set(STUDIES)
    assert data["n_point_sign_crossings"]==16
    assert data["n_both_arm_signs_nominally_supported"]==1
    assert data["forty_edge_covariance_worst_case_change_certificates"]==[]
    assert data["Trifolium_original_primary_DOI_not_present_in_frozen_numeric_csv"]


def test_study_level_original_direction_does_not_pretend_n41_independence():
    d=build()
    expect={
        "Aconitum":(4,4,.03225,1),
        "Dactylorhiza":(5,5,.1694,3),
        "Gymnadenia":(10,5,.03482,3),
        "Lobelia_cardinalis":(6,6,.077,3),
        "Lobelia_siphilitica":(6,6,-.0295,0),
        "Primula":(4,4,.030,2),
        "Trifolium":(1,1,-.16,1),
        "Trillium":(5,3,1.4,3),
    }
    for k,(n,axes,strength,flips) in expect.items():
        r=d["programme_summaries"][k]
        assert r["n_matched_axis_context_pairs"]==n
        assert r["n_distinct_trait_axes"]==axes
        assert r["study_mean_absolute_gradient_attenuation"]==pytest.approx(strength)
        assert r["point_sign_crossings"]==flips
    signs=d["study_strength_directions"]
    assert signs["n_programmes"]==8
    assert signs["n_positive_strength_change"]==6
    assert signs["exploratory_one_sided_p_at_or_above_majority"]==.14453125
    assert signs["exploratory_two_sided_exact_sign_p"]==.2890625
    sensitivity=d["study_strength_sensitivity_excluding_SE_missing_Trifolium"]
    assert sensitivity["n_programmes"]==7
    assert sensitivity["n_positive_strength_change"]==6
    assert sensitivity["exploratory_two_sided_exact_sign_p"]==.125


def test_source_2016_aconitum_and_2023_lobelia_add_two_new_programmes():
    acon=load(ACON)
    brown=load(BROWN)
    assert len(acon)==8
    assert len(brown)==36
    ex=new_aconitum(acon)
    assert len(ex)==4
    diff={r["trait"]:r["delta_open_minus_hand"] for r in ex}
    assert diff["flower_number"]==pytest.approx(-.023)
    assert diff["nectar_position_difference"]==pytest.approx(-.146)
    bs=new_lobelia_siphilitica(brown,"relative_seeds_per_plant")
    bf=new_lobelia_siphilitica(brown,"relative_fruits_per_plant")
    br=new_lobelia_siphilitica(brown,"relative_seeds_per_plant","REDUCED_OPEN")
    assert len(bs)==len(bf)==len(br)==6
    assert sum(x["magnitude_delta"] for x in bs)/6==pytest.approx(-.0295)
    assert sum(x["magnitude_delta"] for x in bf)/6==pytest.approx(-.0275)
    assert sum(x["magnitude_delta"] for x in br)/6==pytest.approx(-.03466666666666667)
    assert {x["source_doi"] for x in bs}=={"10.1002/ece3.10706"}
    assert all("relative_seeds" in x["fixed_background"] for x in bs)


def test_same_biological_system_source_arms_do_not_become_independent_studies():
    g=[r for r in build()["matched_source_edges"] if r["programme"]=="Gymnadenia"]
    assert len(g)==10
    assert len({r["trait"] for r in g})==5
    assert len({r["fixed_background"] for r in g})==2
    assert all(r["independent_experiment_unit"]=="Gymnadenia" for r in g)
    trill=[r for r in build()["matched_source_edges"] if r["programme"]=="Trillium"]
    assert len(trill)==5
    assert {r["source_link_metric"] for r in trill}=={
        "POISSON_LOG_LINK_FEMALE_SEEDS"
    }
    assert sum(r["point_sign_change"] for r in trill)==3


def test_conditional_floral_number_only_partial_meta_does_not_open_random_effects():
    meta=build()["common_flower_number_conditional_fixed_effect"]
    assert meta["n_independent_programmes"]==5
    assert set(meta["study_estimates"])=={
        "Dactylorhiza","Primula","Gymnadenia","Lobelia_cardinalis",
        "Aconitum",
    }
    assert meta["study_estimates"]["Gymnadenia"][
        "n_backgrounds_in_source"]==2
    assert meta["study_estimates"]["Gymnadenia"][
        "within_study_uncertainty_upper"]==pytest.approx(.097)
    assert meta["weighted_mean_source_beta_delta"]==pytest.approx(
        .06192293546648923,abs=1e-12)
    assert meta["covariance_worst_case_SE_upper"]==pytest.approx(
        .04284510019614249,abs=1e-12)
    assert meta["conditional_normal_p_upper"]==pytest.approx(
        .14838076670524472,abs=1e-12)
    lo,hi=meta["conditional_normal_95pct_interval"]
    assert lo<0<hi
    assert meta["random_effects_population_mean_identified"] is False
    assert meta["source_cell_covariance_not_assumed_zero"] is True
    assert "Aconitum" in meta["study_estimates"]
    assert "Lobelia_siphilitica" not in meta["study_estimates"]
    assert "Trillium" not in meta["study_estimates"]


def test_no_doi_se_fabrication_and_all_40_test_bound():
    x=build()
    assert len(preexisting_frozen_edges())==24
    trif=new_trifolium(load(TRIF))
    assert len(trif)==1
    assert trif[0]["source_SE_open"] is None
    assert trif[0]["source_signs_both_nominally_supported"] is None
    assert trif[0]["delta_standard_error_upper"] is None
    z=x["forty_edge_conditional_bonferroni_critical_z"]
    assert 3.22<z<3.24
    assert len([i for i in x["matched_source_edges"] if
                i["source_SE_open"] is not None])==40
    for r in x["matched_source_edges"]:
        if r["source_SE_open"] is not None:
            assert r["delta_standard_error_upper"]>=r["source_SE_open"]
    with pytest.raises(ValueError,match="invalid experiment count"):
        sign_test(8,7)


def test_source_tampering_fails_closed_without_cherry_picking():
    a=load(ACON)
    b=load(BROWN)
    ac=deepcopy(a)
    ac[1]["context"]=ac[0]["context"]
    with pytest.raises(ValueError,match="duplicate"):
        new_aconitum(ac)
    corrupt=deepcopy(b)
    corrupt[1]["fitness_endpoint"]=corrupt[0]["fitness_endpoint"]
    corrupt[1]["trait"]=corrupt[0]["trait"]
    corrupt[1]["context"]=corrupt[0]["context"]
    with pytest.raises(ValueError,match="duplicated"):
        new_lobelia_siphilitica(corrupt,"relative_seeds_per_plant")
    with pytest.raises(ValueError,match="6x3x2 table incomplete"):
        new_lobelia_siphilitica(b[:-1],"relative_seeds_per_plant")
    with pytest.raises(ValueError,match="unregistered"):
        new_lobelia_siphilitica(b,"not_registered")
    with pytest.raises(ValueError,match="full original Lobelia"):
        new_lobelia_cardinalis(load(LOB)[:-1])


def test_scientific_literature_synthesis_not_misreported_as_new_macro_fieldwork():
    source=build()
    assert source["status"].endswith("GENERAL_POPULATION_META_NOT_READY")
    ceiling=source["generalization_blockers"]
    assert "no_meta_analytic_natural_prevalence_or_random_effects_generalization" in ceiling
    assert "earlier_caruso_meta_2018_original_workbook_Dryad_401_403_not_recovered" in ceiling
    assert "source_programmes_are_independent_biological_units_not_41_edge_replicates" in ceiling
    assert "no_new_field_trait_randomization_or_pure_function_optima_or_SCH_L" in ceiling

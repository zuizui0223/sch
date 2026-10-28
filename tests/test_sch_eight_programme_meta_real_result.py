"""Validate actual source-based meta receipts, no 41-edge pseudoreplication."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
RECEIPT=ROOT/"data/SCH_META_EIGHT_PROGRAMME_EXPERIMENTAL_POLLEN_READOUT_V1.json"
NOTE=ROOT/"docs/SCH_EIGHT_PROGRAMME_EXPERIMENTAL_POLLEN_META_PILOT_V1.md"
SOURCE_ACON=ROOT/"data/SCH_META_ACONITUM_2016_SOURCE_TABLE3_SELECTION_V1.csv"
SOURCE_BROWN=ROOT/"data/SCH_META_LOBELIA_SIPHILITICA_2023_SOURCE_TABLE2_SELECTION_V1.csv"


def _result():
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_eight_original_studies_and_verbatim_source_receipt_denominators():
    r=_result()
    assert r["independent_study_units"]==8
    assert r["n_matched_trait_context_edges"]==41
    assert r["n_matched_edges_with_original_SEs"]==40
    assert len(r["matched_source_edges"])==41
    assert len({x["programme"] for x in r["matched_source_edges"]})==8
    assert r["provenance"]["github_run_id"]==40620004537
    assert r["provenance"]["github_job_id"]==122591468125
    assert r["provenance"]["github_artifact_id"]==12787125160
    assert r["provenance"]["original_Dryad_2018_full_meta_dataset_recovered"] is False
    assert r["n_distinct_original_DOIs_with_verified_primary_metadata"]==8
    assert r["study_strength_directions"]["n_positive_strength_change"]==6


def test_effect_is_conditionally_unsupported_and_sign_crossings_are_unconfirmed():
    r=_result()
    assert r["n_point_sign_crossings"]==16
    assert r["n_both_arm_signs_nominally_supported"]==1
    assert len(r["forty_edge_covariance_worst_case_change_certificates"])==0
    a=r["study_strength_directions"]
    assert a["n_programmes"]==8
    assert a["exploratory_two_sided_exact_sign_p"]==.2890625
    sub=r["study_strength_sensitivity_excluding_SE_missing_Trifolium"]
    assert sub["n_programmes"]==7
    assert sub["exploratory_two_sided_exact_sign_p"]==.125
    m=r["common_flower_number_conditional_fixed_effect"]
    assert m["n_independent_programmes"]==5
    assert m["weighted_mean_source_beta_delta"]==pytest.approx(.06192293546648923)
    assert m["covariance_worst_case_SE_upper"]==pytest.approx(.04284510019614249)
    assert m["conditional_normal_95pct_interval"][0]<0<m["conditional_normal_95pct_interval"][1]
    assert m["conditional_normal_p_upper"]==pytest.approx(.14838076670524472)
    assert m["random_effects_population_mean_identified"] is False


def test_two_new_original_study_tables_are_complete_and_not_two_experiments_each():
    from scripts.analyze_sch_experimental_pollen_meta_8_programmes import (
        load,new_aconitum,new_lobelia_siphilitica,
    )
    a=new_aconitum(load(SOURCE_ACON))
    b=new_lobelia_siphilitica(load(SOURCE_BROWN),"relative_seeds_per_plant")
    assert len(a)==4
    assert len(b)==6
    assert {r["source_doi"] for r in a}=={"10.1038/srep34499"}
    assert {r["source_doi"] for r in b}=={"10.1002/ece3.10706"}
    br=_result()["Brown_2023_seed_vs_fruit_study_sensitivity"]
    assert br["all_same_independent_biological_programme"] is True
    assert br["n_new_source_table2_records"]==36
    assert br["fruit_absolute_gradient_attenuation"]==pytest.approx(-.0275)
    assert br["seed_absolute_gradient_attenuation"]==pytest.approx(-.0295)


def test_ecological_doi_provenance_is_not_fabricated():
    r=_result()
    assert {s["source_doi"] for s in r["matched_source_edges"] if
            s["programme"]=="Trifolium"}=={"10.1111/jeb.13392"}
    assert r["provenance"]["original_Trifolium_Doi_external_verified"] is True
    ceiling=r["generalization_blockers"]
    assert "Trifolium_HCN_positive_only_genotype_and_no_source_beta_SE" in ceiling
    assert "Trillium_conditional_Poisson_coefficients_not_poolable_with_linear_slopes" in ceiling
    assert "Lobelia_siphilitica_2023_two_fitness_components_and_three_regimes_same_study" in ceiling
    assert "source_programmes_are_independent_biological_units_not_41_edge_replicates" in ceiling
    assert "earlier_caruso_meta_2018_original_workbook_Dryad_401_403_not_recovered" in ceiling


def test_document_is_an_honest_quantitative_pilot_not_a_claimed_general_law():
    doc=NOTE.read_text(encoding="utf-8")
    for token in (
        "6/8", "0.2890625", "16 of 41", "one of the 40", "zero",
        "0.06192294", "0.148381", "10.5061/dryad.2v8c5g0",
        "401", "403", "not yet a major positive macroecology paper",
    ):
        assert token.lower() in doc.lower()
    assert "not a new field" in doc.lower() or "not an analysis of independent original field plant rows" in doc.lower()

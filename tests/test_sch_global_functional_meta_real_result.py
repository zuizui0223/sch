"""Validate the actual public 2020 Dryad meta reanalysis and each source pair.

The numeric results are from the checksum-verified original 572-row Excel
master on GitHub Actions run 43580775215, NOT from examples constructed
in this test. Experiment-level independence and true response scales matter.
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[1]
READOUT=ROOT/"data/SCH_2020_FUNCTIONAL_META_EXPERIMENTAL_READOUT_V1.json"
PAIRS=ROOT/"data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv"
NOTE=ROOT/"docs/SCH_GLOBAL_FUNCTIONAL_TRAIT_META_EMPIRICAL_V1.md"


def _source():
    report=json.loads(READOUT.read_text(encoding="utf-8"))
    with PAIRS.open(encoding="utf-8",newline="") as fh:
        pairs=list(csv.DictReader(fh))
    return report,pairs


def test_public_unduplicated_original_denominators_and_source_identity():
    d,rows=_source()
    assert d["source_original_reference"]["experimental_master_md5"]=="7f680c344c0a418a3d8742649de24d52"
    assert d["source_original_reference"]["github_original_verified_source_run"]==43581102211
    assert d["source_original_reference"]["github_workflow_job"]==132405799918
    assert d["source_data_doi"]=="10.5061/dryad.sn02v6x0q"
    assert d["source_unduplicated_experimental_rows"]==572
    assert d["source_duplicate_1014_rows_not_used"]
    assert d["source_observational_815_rows_not_pooled"]
    assert d["source_pair_screening"][
        "n_candidate_two_row_two_treatment_keys"]==172
    assert d["source_pair_screening"][
        "rejected_pair_counts"]["missing_original_linear_gradient_or_se"]==35
    assert d["eligible_matched_pair_total"]==137
    assert len(rows)==137
    assert d["eligible_paper_units"]==26
    assert d["eligible_species_units"]==34
    assert len({x["paper_id"] for x in rows})==26
    assert len({x["species"] for x in rows})==34
    used_ids=[i for r in rows for i in (r["source_row_id_1"],r["source_row_id_2"])]
    assert len(used_ids)==len(set(used_ids))==274


def test_original_biotic_abiotic_and_ambiguous_agent_counts_are_not_mixed():
    d,rows=_source()
    groups=d["eligible_agent_category_counts"]
    expect={
        "BIOTIC":(75,17,21,3),
        "ABIOTIC":(58,8,20,0),
        "UNRESOLVED_OR_MIXED":(4,1,0,0),
    }
    for category,(n,papers,flips,certified) in expect.items():
        x=[r for r in rows if r["agent_category"]==category]
        assert len(x)==n
        assert len({r["paper_id"] for r in x})==papers
        assert sum(r["point_sign_flip"].lower()=="true" for r in x)==flips
        assert sum(r["full_family_source_covariance_worst_case_normal_05"].lower()=="true"
                   for r in x)==certified
        assert groups[category]["n_matched_trait_context_pairs"]==n
    assert d["all_source_point_sign_flips"]==41
    assert d["all_source_both_arm_nominal_opp_signs"]==0
    assert d["all_source_familywise_contrast_certificates"]==3
    assert d["n_papers_with_familywise_source_contrast_certificates"]==2
    assert d["n_source_certificates_robust_to_stored_decimal_rounding"]==2


def test_biotic_abiotic_meta_contrast_not_mistaken_for_a_causal_difference():
    d,rows=_source()
    k=d["paper_level_independence_protected_comparison"]
    assert k["independent_biotic_papers"]==17
    assert k["independent_abiotic_papers"]==8
    assert k["n_included_pure_category_independent_papers"]==25
    assert k["n_permutations_run"]==9999
    assert k["observed_difference"]==pytest.approx(-.10100081699346405)
    assert k["two_sided_p_given_paper_label_exchangeability"]==pytest.approx(.3996)
    a,b=k["paper_bootstrap_percentile_interval_descriptive"]
    assert a<0<b
    assert d["eligible_agent_category_counts"]["ABIOTIC"][
        "n_original_study_in_situ_context_pairs"]==0
    common=d["paper_cluster_design_sensitivity"]["source_context_A_or_B_only"]
    assert common["n_source_pairs"]==96
    assert common["n_biotic_pairs"]==38
    assert common["n_abiotic_pairs"]==58
    assert common["n_original_papers"]==17
    assert common["independence_protected_paper_label_comparison"][
        "two_sided_p_given_paper_label_exchangeability"]==pytest.approx(.2044)
    F=d["paper_cluster_design_sensitivity"][
        "original_fecundity_component_F_only"]
    assert F["n_source_pairs"]==94
    assert F["independence_protected_paper_label_comparison"][
        "two_sided_p_given_paper_label_exchangeability"]==pytest.approx(.3842)
    indoor=d["paper_cluster_design_sensitivity"]["source_context_A_only"]
    assert indoor["independence_protected_paper_label_comparison"][
        "status"].startswith("NOT_MODELABLE")
    assert indoor["independence_protected_paper_label_comparison"][
        "independent_biotic_papers"]==1


def test_all_three_original_source_contrast_certificates_have_provenance():
    d,rows=_source()
    c=d["source_reconstructed_familywise_contrast_certificate_details"]
    assert len(c)==3
    expected={
        ("13","Early growth rate"):(
            "Impatiens capensis","Number of fruits",.09,.003,.02,.002,
            -.087,False,
        ),
        ("13","Number of internodes"):(
            "Impatiens capensis","Number of fruits",.14,.36,.01,.02,
            .22,True,
        ),
        ("37","Total leaf area"):(
            "Ipomoea hederacea","Number of seeds",.79,.044,.03,.05,
            -.746,True,
        ),
    }
    assert {(r["paper_id"],r["trait"]) for r in c}==set(expected)
    z=d["source_95pct_normal_bonferroni_critical_z"]
    assert 3.56<z<3.57
    for r in c:
        animal,fitness,b1,b2,se1,se2,delta,robust=expected[
            (r["paper_id"],r["trait"])]
        assert (r["species"],r["fitness_measure"])==(animal,fitness)
        for key,val in (("beta1",b1),("beta2",b2),
                        ("se1",se1),("se2",se2),
                        ("contrast_difference",delta)):
            assert r[key]==pytest.approx(val)
        assert r["point_sign_flip"] is False
        assert r["stored_source_decimal_rounding_robust"] is robust
        assert abs(delta)>z*r["worst_covariance_se"]
        pair=next(x for x in rows if x["paper_id"]==r["paper_id"]
                  and x["trait"]==r["trait"])
        assert pair["full_family_source_covariance_worst_case_normal_05"].lower()=="true"
        assert (pair["certificate_robust_to_stored_source_decimal_rounding"].lower()=="true")==robust
        assert r["adjusted_137_family_normal_p_upper"]<.05
        assert pair["source_row_id_1"]==r["original_row_ids"][0]
        assert pair["source_row_id_2"]==r["original_row_ids"][1]


def test_exact_137_family_cannot_be_used_as_ecological_reversal_prevalence():
    d,rows=_source()
    assert all(r["beta1"]!="" and r["se1"]!="" for r in rows)
    assert all(r["source_both_arm_opposite_signs_nominal95"].lower()=="false" for r in rows)
    assert all(r["treatment_code1"]!=r["treatment_code2"] for r in rows)
    assert "point_estimate_sign_flip_not_inferential_sign_reversal" in d["inferential_limits"]
    assert "source_decimal_printing_rounding_not_independently_audited" in d["inferential_limits"]
    assert d["stored_decimal_rounding_is_not_original_printing_precision_proof"]
    assert "source_pub_bias_and_site_selection_not_adjusted" in d["inferential_limits"]


def test_manuscript_status_does_not_claim_cross_species_causal_conflict():
    note=NOTE.read_text(encoding="utf-8")
    for k in ("572","172","137","26","34","41","0","3","2",
              "0.3996","0.2044","0.3842","0.746","Beans",
              "Stinchcombe","not prevalence","not a causal"):
        assert k.lower() in note.lower()
    status=(ROOT/"docs/PUBLICATION_STATUS.md").read_text(encoding="utf-8")
    assert "GLOBAL_FUNCTIONAL_META_V1" in status
    assert "not a population prevalence" in status.lower()

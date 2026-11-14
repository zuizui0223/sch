"""Original primary-study fitted interaction verification for 137-pair meta."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from copy import deepcopy

import pytest

from scripts.audit_sch_2020_meta_direct_source_interactions import (
    META,QA,read,run,
)

ROOT=Path(__file__).resolve().parents[1]


def _result():
    d=json.loads(META.read_text(encoding="utf-8"))
    return run(d,read(QA))


def test_source_2015_primary_fitted_interaction_overrides_reconstructed_p():
    d=_result()
    assert d["n_conditional_reconstructed_137_fwer_candidates"]==3
    assert d["n_robust_to_stored_workbook_decimal_format"]==2
    assert d["n_direct_original_fitted_interactions_with_verified_test"]==2
    assert d["n_direct_original_fitted_interactions_p_137_fwer_supported"]==1
    assert d["n_source_direct_original_interaction_unverified"]==1
    assert d["n_primary_p_conflicts_with_reconstructed_se_inference"]==1
    assert d["individual_source_direct_Bonferroni_threshold"]==pytest.approx(.05/137)
    assert d["status"].startswith("ONE_PRIMARY_FITTED_DIRECT_INTERACTION")


def test_original_2015_study_direct_tests_and_2002_bias_risk_are_independent():
    d=_result()
    q={(r["paper_id"],r["original_trait"]):r for r in d["original_primary_test_checks"]}
    early=q[("13","Early growth rate")]
    assert early["original_paper_doi"]=="10.3732/ajb.1400355"
    assert early["original_fitted_interaction_p"]=="0.04"
    assert early["source_reconstructed_vs_original_direct_test_inconsistent"]
    assert early["original_source_p_survives_137_Bonferroni"] is False
    internodes=q[("13","Number of internodes")]
    assert internodes["original_fitted_interaction_p"]=="<0.0001"
    assert internodes["original_source_p_survives_137_Bonferroni"] is True
    leaf=q[("37","Total leaf area")]
    assert leaf["original_paper_doi"]=="10.1086/342069"
    assert leaf["original_fitted_interaction_p"]=="NOT_VERIFIED"
    assert leaf["original_source_p_survives_137_Bonferroni"] is None
    assert "PHENOTYPIC_BIAS_RISK" in leaf["assessment"]


@pytest.mark.parametrize(("key","value"),[
    ("author_fitted_treatment_trait_p","0.000001"),
    ("primary_article_doi","10.0000/nonexistent"),
    ("independent_primary_source_assessment","ALL_CAUSAL_OPTIMA_IDENTIFIED"),
])
def test_original_external_paper_evidence_tampering_fails_closed(key,value):
    old=json.loads(META.read_text(encoding="utf-8"))
    q=deepcopy(read(QA))
    q[0][key]=value
    with pytest.raises(ValueError,match="primary test p-value metadata drift"):
        run(old,q)


def test_narrative_preserves_sign_flip_and_fitted_interaction_separation():
    s=(ROOT/"docs/SCH_GLOBAL_FUNCTIONAL_TRAIT_META_EMPIRICAL_V1.md").read_text(
        encoding="utf-8").replace("**","")
    for q in ("p=0.3996","P=0.2044","P=0.3842","41/137","0.04",
              "F=82.74","Stinchcombe","environmental covariance",
              "only ONE","not a causal"):
        assert q.lower() in s.lower()
    assert "source-reconstructed vs original direct test" not in s.lower() or (
        "original direct" in s.lower())

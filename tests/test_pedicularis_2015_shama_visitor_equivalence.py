"""Source to inference tests for 2015 Shama visitor non-equivalence claims."""
from __future__ import annotations

from copy import deepcopy
from statistics import NormalDist

import pytest

from scripts.audit_pedicularis_2015_shama_visitor_equivalence import (
    SOURCE,build,read_source,normal_wald_interval,
    minimum_symmetric_tost_margin,
)


def test_model_source_table_six_rows_one_visitor_site_only():
    data=build(read_source(SOURCE))
    assert data["source_doi"]=="10.1093/aobpla/plv019"
    assert data["source_study_count"]==1
    assert data["source_visitor_sites"]==["Shama"]
    assert data["n_source_coefficients"]==6
    assert data["source_model"]=="BINOMIAL_LOGIT_WITH_YEAR_BY_TREATMENT_INTERACTION"


def test_pollinator_treatment_wald_interval_does_not_support_small_equivalence():
    r=build(read_source(SOURCE))
    effect=r["observed_source_table"]["pollinator_visits"]["TREATMENT"]
    assert effect["published_beta"]==.012
    assert effect["published_se"]==.224
    assert effect["source_p"]=="0.958"
    assert effect["normal_approximation_model_based_90pct_interval"]==pytest.approx(
        [-.3564472124,.3804472124],abs=1e-8)
    assert effect["normal_approximation_model_based_95pct_interval"]==pytest.approx(
        [-.4270319325,.4510319325],abs=1e-8)
    assert effect["minimal_symmetric_equivalence_margin_infimum_on_model_scale"]==pytest.approx(
        .3804472124,abs=1e-8)
    assert effect["equivalence_claim_supported"] is False
    assert effect["is_plot_cluster_robust_reanalysis"] is False


def test_robber_treatment_also_lacks_a_registered_equivalence_margin():
    r=build(read_source(SOURCE))
    x=r["observed_source_table"]["nectar_robber_visits"]["TREATMENT"]
    assert x["published_beta"]==-.014
    assert x["source_p"]=="0.951"
    assert x["normal_approximation_model_based_90pct_interval"]==pytest.approx(
        [-.3840920661,.3560920661],abs=1e-8)
    assert x["minimal_symmetric_equivalence_margin_infimum_on_model_scale"]==pytest.approx(
        .3840920661,abs=1e-8)
    assert x["equivalence_claim_supported"] is False


def test_large_year_interaction_uncertainty_rules_out_all_years_neutrality_claim():
    r=build(read_source(SOURCE))
    x=r["observed_source_table"]
    py=x["pollinator_visits"]["YEAR_X_TREATMENT"]
    ny=x["nectar_robber_visits"]["YEAR_X_TREATMENT"]
    assert py["published_se"]==.451
    assert ny["published_se"]==.444
    assert py["minimal_symmetric_equivalence_margin_infimum_on_model_scale"]==pytest.approx(
        .8408289858,abs=1e-8)
    assert ny["minimal_symmetric_equivalence_margin_infimum_on_model_scale"]==pytest.approx(
        .8473150104,abs=1e-8)
    assert r["interpretation"]["main_effect_is_not_all_years_marginal_effect"] is True
    assert r["interpretation"]["model_year_treatment_covariance_recovered"] is False


@pytest.mark.parametrize(("field","newvalue"),[
    ("source_doi","10.5555/non-source"),
    ("site","Baishuitai"),
    ("source_table","Table_2"),
    ("intervention","WATER_ONLY"),
    ("original_model","GAUSSIAN"),
    ("reported_beta","99"),
    ("reported_se","0.01"),
    ("reported_chi2","23"),
    ("reported_p","0.00001"),
    ("reported_df","5"),
])
def test_all_primary_source_values_fail_closed_on_tampering(field,newvalue):
    rows=deepcopy(read_source(SOURCE))
    rows[1][field]=newvalue
    with pytest.raises(ValueError,match="drift|invalid|duplicate|incompatible"):
        build(rows)


def test_completeness_and_duplicate_rows_cannot_promote_fake_selectivity():
    rows=read_source(SOURCE)
    with pytest.raises(ValueError,match="six unique"):
        build(rows[:-1])
    duplicated=deepcopy(rows)
    duplicated[0]=deepcopy(duplicated[1])
    with pytest.raises(ValueError,match="duplicate"):
        build(duplicated)
    r=build(rows)
    assert r["interpretation"]["preferential_functional_loading_established"] is False
    assert r["interpretation"]["visitor_selectivity_across_all_six_sites_identified"] is False


def test_interval_and_tost_math_require_valid_scale_and_frozen_margin():
    x=NormalDist().inv_cdf(.95)
    assert minimum_symmetric_tost_margin(.012,.224)==pytest.approx(
        abs(.012)+x*.224)
    for args in ((0,0,.90),(0,-1,.90),(0,1,0),(0,1,1)):
        with pytest.raises(ValueError,match="invalid"):
            normal_wald_interval(*args)


def test_manuscript_defence_claims_remain_source_bounded():
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    manuscript=(root/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md").read_text(encoding="utf-8")
    bridge=(root/"docs/PEDICULARIS_SHARED_CONFLICT_AND_DEFENCE_AXIS_BRIDGE_V1.md").read_text(encoding="utf-8")
    note=(root/"docs/SCH_PEDICULARIS_SHAMA_VISITOR_EQUIVALENCE_LIMITS_V1.md").read_text(encoding="utf-8")
    for token in ("−0.427","0.451","Shama","not an equivalence test"):
        assert token in manuscript
    assert "strong preferential loading" not in bridge
    assert "approximately null in the experiment" not in bridge
    assert "POLLINATOR_EQUIVALENCE_NOT_ESTABLISHED" in bridge
    assert "0.38045" in note
    assert "0.38409" in note
    assert "not a field-validated equivalence test" in note

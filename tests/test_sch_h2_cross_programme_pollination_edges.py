from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from scripts.audit_sch_h2_cross_programme_pollination_edges import (
    READOUT, SOURCE, build, read_csv,
)

ROOT=Path(__file__).resolve().parents[1]


def _built():
    return build(read_csv(SOURCE),json.loads(READOUT.read_text(encoding="utf-8")))


def test_frozen_all_14_same_year_source_pairs_are_recovered():
    r=_built()
    assert r["n_original_independent_programmes"]==3
    assert r["n_registered_same_year_matched_trait_edges"]==14
    assert r["n_source_rows"]==31
    assert len(r["all_pairs"])==14
    assert len({p["programme"] for p in r["all_pairs"]})==3
    assert all(p["within_programme_same_year_pair"] for p in r["all_pairs"])
    assert {p["metric_family"] for p in r["all_pairs"]}=={
        "LINEAR_TOTAL_SELECTION","POISSON_LINEAR_TOTAL_SELECTION"
    }
    assert r["original_holdout_H2M1_predictor_classes_and_q_unchanged"] is True


def test_source_printed_familywise_95pct_contrast_evidence_in_three_programmes():
    r=_built()
    passed=[p for p in r["all_pairs"] if p[
        "certified_change_at_alpha_05_using_printed_values"]]
    assert len(passed)==3
    assert r["n_printed_value_familywise_supported_changes"]==3
    assert r["n_programmes_with_printed_value_supported_change"]==3
    lookup={(p["programme"].split("_")[0],p["trait"],p["year"]):p
            for p in passed}
    d=lookup[("Dactylorhiza","spur length","2010_SOURCE_STUDY")]
    assert d["delta_open_minus_supplemented"]==pytest.approx(.324)
    assert d["covariance_worst_case_se_upper"]==pytest.approx(.105)
    assert d["bonferroni_14_adjusted_p_upper"]==pytest.approx(.028429,abs=1e-5)
    assert d["familywise_95pct_normal_wald_outer_interval"][0]>0
    prim=lookup[("Primula","flowering start","2016")]
    assert prim["delta_open_minus_supplemented"]==pytest.approx(.206)
    assert prim["covariance_worst_case_se_upper"]==pytest.approx(.066)
    assert prim["bonferroni_14_adjusted_p_upper"]==pytest.approx(.025215,abs=1e-5)
    assert prim["familywise_95pct_normal_wald_outer_interval"][0]>0
    t=lookup[("Trillium","petal size","2020")]
    assert t["delta_open_minus_supplemented"]==pytest.approx(-4.41)
    assert t["covariance_worst_case_se_upper"]==pytest.approx(1.49)
    assert t["bonferroni_14_adjusted_p_upper"]==pytest.approx(.043107,abs=1e-5)
    assert t["familywise_95pct_normal_wald_outer_interval"][1]<0


def test_rounding_precision_downgrades_borderline_trillium_but_not_other_two():
    r=_built()
    robust=[p for p in r["all_pairs"] if p[
        "certified_with_source_decimal_rounding_sensitivity"]]
    assert len(robust)==2
    assert {p["programme"].split("_")[0] for p in robust}=={
        "Dactylorhiza","Primula"
    }
    trillium=next(p for p in r["all_pairs"]
                 if p["canonical_axis"]=="Trillium_000661_petal_size"
                 and p["year"]=="2020")
    assert trillium["certified_change_at_alpha_05_using_printed_values"]
    assert not trillium["certified_with_source_decimal_rounding_sensitivity"]
    assert trillium["rounding_min_absolute_delta"]==pytest.approx(4.40)
    assert trillium["rounding_max_se_upper"]==pytest.approx(1.545)
    assert "SE_1_2_rounded" in " ".join(r["claim_ceiling"])


def test_trillium_display_source_delta_inconsistency_is_explicit_not_promoted():
    r=_built()
    assert "3.09" in r[
        "trillium_2020_display_height_printed_source_delta_warning"]
    assert "2.83" in r[
        "trillium_2020_display_height_printed_source_delta_warning"]
    display=next(p for p in r["all_pairs"] if p[
        "canonical_axis"]=="Trillium_000661_display_height"
        and p["year"]=="2020")
    assert display["delta_open_minus_supplemented"]==pytest.approx(3.09)
    assert not display["certified_change_at_alpha_05_using_printed_values"]


def test_multiplicity_and_posthoc_limits_remain_explicit():
    r=_built()
    assert r["alpha"]==.05
    assert r["confidence_family"]=="ALL_14_FROZEN_V27_WITHIN_YEAR_POLLINATION_EDGES"
    assert 2.91<r["normal_bonferroni_critical_value"]<2.92
    assert "secondary_exploratory_analysis_not_original_H2M1_primary_test" in r["claim_ceiling"]
    assert "gradient_magnitude_difference_is_not_supported_sign_reversal" in r["claim_ceiling"]
    assert "primula_original_open_treatment_includes_two_style_morphs_hand_only_long_style" in r["claim_ceiling"]
    original=json.loads(READOUT.read_text(encoding="utf-8"))
    assert original["n_supported_reversal_axes"]==2
    assert original["n_programmes_adjudicated"]==3
    assert original["status"].startswith("THREE_HELDOUT_PROGRAMMES")


@pytest.mark.parametrize(("field","value"),[
    ("doi","10.0000/wrong"),("metric_family","NEW_INCOMPATIBLE"),
    ("context","UNREGISTERED"),("beta","nan"),("se","-1.0"),
    ("axis_eligible","NO"),
])
def test_drift_or_noncomparable_effects_do_not_enter_family(field,value):
    rows=deepcopy(read_csv(SOURCE))
    rows[0][field]=value
    h=json.loads(READOUT.read_text(encoding="utf-8"))
    with pytest.raises((ValueError,KeyError)):
        build(rows,h)


def test_missing_or_duplicate_matched_edges_fail_closed():
    rows=read_csv(SOURCE)
    h=json.loads(READOUT.read_text(encoding="utf-8"))
    with pytest.raises(ValueError,match="31-row"):
        build(rows[:-1],h)
    bad=deepcopy(rows)
    bad[1]=deepcopy(bad[0])
    with pytest.raises(ValueError,match="duplicate"):
        build(bad,h)


def test_manuscript_and_source_note_state_experimental_but_nonoptimum_conclusion():
    manuscript=(ROOT/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md").read_text(encoding="utf-8")
    note=(ROOT/"docs/SCH_H2_THREE_PROGRAMME_POLLINATION_SELECTION_V1.md").read_text(encoding="utf-8")
    fig=(ROOT/"manuscript/SHARED_TRAIT_COMPROMISE_FIGURE_MAP_V1.md").read_text(encoding="utf-8")
    assert "### 7.8 Independent pollination-treatment programmes" in manuscript
    for x in ("0.324","0.206","4.41","14","magnitude","not a direct z"):
        assert x in manuscript.lower()
    assert "2019 Primula correction" in note
    assert "1.545" in note
    assert "Primula" in note
    assert "all 14" in note
    assert "three-programme" in fig

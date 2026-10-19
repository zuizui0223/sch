"""Regression tests for the original four-study / 24-pair source spectrum."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
import json
from pathlib import Path

import pytest

from scripts.audit_sch_four_programme_selection_spectrum import (
    GYM_DOI, GYM_PROGRAMME, GYM_SOURCE, V27_SOURCE, V27_READOUT,
    build, read_gym, read_v27,
)

ROOT=Path(__file__).resolve().parents[1]


def _get():
    return build(
        read_v27(V27_SOURCE),
        json.loads(V27_READOUT.read_text(encoding="utf-8")),
        read_gym(GYM_SOURCE),
    )


def test_four_programme_twenty_four_edge_complete_unselected_family():
    receipt=_get()
    r=receipt["totals"]
    assert r["n_independent_programmes"]==4
    assert r["n_source_frozen_v27_pairs"]==14
    assert r["n_source_gymnadenia_pollen_by_herbivory_pairs"]==10
    assert r["n_within_axis_fixed_context_pollination_edges"]==24
    assert r["n_point_sign_switches"]==11
    assert r["n_opposite_individually_supported_directions"]==1
    assert r["n_familywise_printed_difference_certificates"]==2
    assert r["n_familywise_rounding_robust_certificates"]==0
    assert len(receipt["contrasts"])==24
    assert len(receipt["programme_summaries"])==4
    assert receipt["legacy_14_edge_results_retained_as_separate_family"]
    assert receipt["original_V27_readout_and_frozen_H2M1_class_comparison_unchanged"]


def test_source_biology_dactylorhiza_primula_trillium_and_gymnadenia():
    result=_get()
    s=result["programme_summaries"]
    expect={
        "Dactylorhiza":(5,3,0,1,0),
        "Primula":(4,2,0,1,0),
        "Trillium":(5,3,0,0,0),
        "Gymnadenia":(10,3,1,0,0),
    }
    for prefix, (n,flip,both,difference,robust) in expect.items():
        key=next(k for k in s if k.startswith(prefix))
        row=s[key]
        assert row["n_contrasts"]==n
        assert row["point_sign_switches"]==flip
        assert row["nominal_both_cell_signs_supported"]==both
        assert row["familywise_printed_changes"]==difference
        assert row["familywise_rounding_robust_changes"]==robust


def test_gymnadenia_herbivory_fixed_and_original_source_dependent_sign():
    result=_get()
    gym=[x for x in result["contrasts"] if x["programme_id"]==GYM_PROGRAMME]
    assert len(gym)==10
    assert len({x["canonical_axis"] for x in gym})==5
    assert {x["fixed_context"] for x in gym}=={
        "NATURAL_HERBIVORY","HERBIVORES_EXCLUDED"
    }
    assert all(x["source_doi"]==GYM_DOI for x in gym)
    phen=[x for x in gym if x["canonical_axis"]=="Gymnadenia_000030_flowering_start"]
    assert len(phen)==2
    excluded=next(x for x in phen if x["fixed_context"]=="HERBIVORES_EXCLUDED")
    natural=next(x for x in phen if x["fixed_context"]=="NATURAL_HERBIVORY")
    assert excluded["beta_open"]==pytest.approx(.094)
    assert excluded["beta_supplemented"]==pytest.approx(-.066)
    assert excluded["delta_open_minus_supplemented"]==pytest.approx(.16)
    assert excluded["covariance_worst_se_upper"]==pytest.approx(.059)
    assert excluded["opposite_individually_supported_source_cell_directions"]
    assert not excluded["contrast_supported_at_24_edge_nominal_familywise_05"]
    assert natural["beta_open"]==pytest.approx(-.0042)
    assert natural["delta_open_minus_supplemented"]==pytest.approx(.1558)
    assert not natural["point_selection_sign_switch"]


def test_difference_certificates_are_not_global_supported_sign_reversals():
    result=_get()
    certs=[x for x in result["contrasts"] if x[
        "contrast_supported_at_24_edge_nominal_familywise_05"]]
    assert {x["programme_id"].split("_")[0] for x in certs}=={
        "Dactylorhiza","Primula"
    }
    d=next(x for x in certs if x["programme_id"].startswith("Dactylorhiza"))
    p=next(x for x in certs if x["programme_id"].startswith("Primula"))
    assert d["delta_open_minus_supplemented"]==pytest.approx(.324)
    assert d["covariance_worst_se_upper"]==pytest.approx(.105)
    assert p["delta_open_minus_supplemented"]==pytest.approx(.206)
    assert p["covariance_worst_se_upper"]==pytest.approx(.066)
    assert 3.078 < result["normal_two_sided_bonferroni_critical_z"] < 3.079
    assert all(not x["contrast_supported_after_decimal_rounding"] for x in certs)
    assert all(not x["opposite_individually_supported_source_cell_directions"]
               for x in certs)
    trillium=next(x for x in result["contrasts"] if
                  x["canonical_axis"]=="Trillium_000661_petal_size"
                  and x["fixed_context"]=="2020")
    assert trillium["delta_open_minus_supplemented"]==pytest.approx(-4.41)
    assert not trillium["contrast_supported_at_24_edge_nominal_familywise_05"]


def test_gym_source_cannot_relabel_plant_treatment_as_flower_randomization():
    v=read_v27(V27_SOURCE)
    holdout=json.loads(V27_READOUT.read_text(encoding="utf-8"))
    original=read_gym(GYM_SOURCE)
    assert len(original)==20
    bad=deepcopy(original)
    bad[0]["treatment_n"]="999"
    with pytest.raises(ValueError,match="source identity"):
        build(v,holdout,bad)
    bad=deepcopy(original)
    bad[0]["treatment"]=bad[1]["treatment"]
    with pytest.raises(ValueError,match="duplicate"):
        build(v,holdout,bad)
    bad=deepcopy(original)
    bad[0]["se"]="nan"
    with pytest.raises(ValueError,match="invalid source"):
        build(v,holdout,bad)
    with pytest.raises(ValueError,match="complete original"):
        build(v,holdout,original[:-1])


def test_original_V27_study_family_and_both_alpha_gates_protected():
    v=read_v27(V27_SOURCE)
    holdout=json.loads(V27_READOUT.read_text(encoding="utf-8"))
    gym=read_gym(GYM_SOURCE)
    with pytest.raises(ValueError):
        build(v[:-1],holdout,gym)
    with pytest.raises(ValueError,match="invalid alpha"):
        build(v,holdout,gym,alpha=1)
    original=deepcopy(holdout)
    original["n_supported_reversal_axes"]=100
    with pytest.raises(ValueError,match="primary holdout readout"):
        build(v,original,gym)


def test_manuscript_source_bounded_spectrum_not_pooled_prevalence():
    manuscript=(ROOT/"manuscript/MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md").read_text(encoding="utf-8")
    note=(ROOT/"docs/SCH_FOUR_PROGRAMME_POLLINATION_SELECTION_SPECTRUM_V1.md").read_text(encoding="utf-8")
    figure=(ROOT/"manuscript/SHARED_TRAIT_COMPROMISE_FIGURE_MAP_V1.md").read_text(encoding="utf-8")
    for word in (
        "24", "11", "only one", "two", "rounding",
        "four published", "not a natural prevalence",
    ):
        assert word in manuscript.lower()
    for word in ("24","11","two","0 rounding","1 nominal","source decimal"):
        assert word.lower() in note.lower()
    assert "four-programme" in figure.lower()
    assert "not a direct" in note.lower()

"""Source-certified signs and hypothetical precision on the original 137 paired slopes."""
from __future__ import annotations

from copy import deepcopy
import json

import pytest

from scripts.audit_sch_2020_meta_sign_resolution import (
    PARENT,SOURCE,Z95,inspect,read,quantile,
)


def _original():
    return inspect(read(SOURCE),json.loads(PARENT.read_text(encoding="utf-8")))


def test_original_source_meta_paper_denominator_and_exact_source_ids():
    r=_original()
    assert r["original_source_DOI"]=="10.5061/dryad.sn02v6x0q"
    assert r["original_experimental_master_MD5"]=="7f680c344c0a418a3d8742649de24d52"
    assert r["n_complete_paired_source_gradients"]==137
    assert r["n_original_independent_papers"]==26
    assert r["n_original_independent_papers_with_one_or_more_point_flips"]==15
    assert len(r["source_paper_diagnostics"])==26
    assert sum(x["n_original_trait_context_pairs"] for x in
               r["source_paper_diagnostics"])==137
    assert sum(x["n_point_crossings"] for x in
               r["source_paper_diagnostics"])==41


def test_41_apparent_direction_reversals_have_no_double_supported_slopes():
    r=_original()
    assert r["n_source_point_crossings"]==41
    assert r["n_crossings_with_two_nominally_supported_opposite_slopes"]==0
    assert r["n_crossings_with_one_nominally_supported_slope"]==13
    assert r["n_crossings_with_neither_slope_nominally_supported"]==28
    assert r["source_95pct_two_sided_abs_z_threshold"]==Z95
    assert len(r["point_crossing_source_record_diagnostics"])==41
    assert all(x["precision_class"]!="BOTH_OPPOSITE_SOURCE_SUPPORTED"
               for x in r["point_crossing_source_record_diagnostics"])
    assert all(x["min_source_arm_abs_z"]<Z95
               for x in r["point_crossing_source_record_diagnostics"])


def test_precision_is_an_algebraic_counterfactual_not_a_power_claim():
    r=_original()
    p=r["hypothetical_sample_information_multiplier_IF_source_betas_remain_fixed"]
    assert p["NOT_AN_EMPIRICAL_POWER_CALCULATION"] is True
    assert p["ASSUMES_SOURCE_POINT_BETAS_FIXED_AND_GAUSSIAN_SE_SQRT_N"] is True
    assert p["q25"]==pytest.approx(8.6436)
    assert p["median"]==pytest.approx(15.3664)
    assert p["q75"]==pytest.approx(158.76)
    assert p["n_below_or_equal_threshold"]["2"]==3
    assert p["n_below_or_equal_threshold"]["4"]==6
    assert p["n_below_or_equal_threshold"]["8"]==8
    assert p["n_below_or_equal_threshold"]["16"]==21
    assert p["n_exceed_100_fold_sample_information"]==12
    assert p["min"]>1
    assert p["max"]>1000
    assert all(x["hypothetical_sample_information_multiplier_to_two_source_signs"]>1
               for x in r["point_crossing_source_record_diagnostics"])


def test_trait_class_and_agent_category_counts_remain_source_separated():
    r=_original()
    t=r["trait_class_source_diagnostics"]
    assert t["PHYSIOLOGY"]["n_source_pairs"]==22
    assert t["PHYSIOLOGY"]["n_point_crossings"]==11
    assert t["PLANT_SIZE"]["n_source_pairs"]==39
    assert t["PLANT_SIZE"]["n_point_crossings"]==7
    assert t["PHENOLOGY"]["n_source_pairs"]==53
    assert t["PHENOLOGY"]["n_point_crossings"]==16
    a=r["environmental_agent_source_diagnostics"]
    assert a["BIOTIC"]["n_source_pairs"]==75
    assert a["BIOTIC"]["n_point_crossings"]==21
    assert a["ABIOTIC"]["n_source_pairs"]==58
    assert a["ABIOTIC"]["n_point_crossings"]==20
    assert a["UNRESOLVED_OR_MIXED"]["n_source_pairs"]==4


def test_missing_reused_rows_inconsistent_sign_or_impossible_se_fails_closed():
    rows=read(SOURCE)
    parent=json.loads(PARENT.read_text(encoding="utf-8"))
    bad=deepcopy(rows)
    bad[0]["se1"]="0"
    with pytest.raises(ValueError,match="invalid"):
        inspect(bad,parent)
    bad=deepcopy(rows)
    bad[0]["point_sign_flip"]="true"
    with pytest.raises(ValueError,match="classification drift"):
        inspect(bad,parent)
    bad=deepcopy(rows)
    bad[1]["source_row_id_1"]=bad[0]["source_row_id_1"]
    with pytest.raises(ValueError,match="same source gradient row"):
        inspect(bad,parent)
    with pytest.raises(ValueError,match="137-row"):
        inspect(rows[:-1],parent)


def test_note_cannot_claim_true_reversal_eco_prevalence_or_real_power():
    from pathlib import Path
    note=Path("docs/SCH_2020_META_SIGN_RESOLUTION_V1.md").read_text(
        encoding="utf-8")
    for term in ("41","28","13","15","26","15.37","12",
                 "not a power analysis","not a prevalence","one source"):
        assert term.lower() in note.lower()
    assert _original()["status"]=="ORIGINAL_SOURCE_META_NO_INFERENTIALLY_SUPPORTED_SIGN_REVERSALS"


def test_numerical_quantile_edges():
    assert quantile([1,2,3,4],.5)==2.5
    assert quantile([1,2,3,4],.25)==1.75
    with pytest.raises(ValueError):
        quantile([],.5)

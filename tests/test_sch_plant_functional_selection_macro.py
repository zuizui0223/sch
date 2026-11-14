"""Fail-closed original meta source matching and study-replication software QA.

These are only software test fixtures. Original published beta values enter
the actual ecological result exclusively through MD5-verified source Excel.
"""
from __future__ import annotations

import math

import pytest

from scripts.analyze_sch_plant_functional_selection_macro import (
    ABIOTIC,BIOTIC,MIXED_OR_UNKNOWN,
    _average,_quantile,original_agent_group,
    per_paper_summary,study_label_exploration,source_pairs,
)


def _paper_entry(paper:str,cat:str,rates:tuple[bool,...])->list[dict]:
    return [{
        "paper_id":paper,"authors":paper,"published_year":"2018",
        "agent_category":cat,"point_sign_flip":v,
        "source_both_arm_opposite_signs_nominal95":False,"species":"species_a",
    } for v in rates]


def test_categories_partition_the_original_source_taxonomy_without_guessing():
    assert not (BIOTIC&ABIOTIC or BIOTIC&MIXED_OR_UNKNOWN or ABIOTIC&MIXED_OR_UNKNOWN)
    assert original_agent_group("Pollinators")=="BIOTIC"
    assert original_agent_group("Herb")=="BIOTIC"
    assert original_agent_group("Soil moisture")=="ABIOTIC"
    assert original_agent_group("Temperature")=="ABIOTIC"
    assert original_agent_group("Dens")=="UNRESOLVED_OR_MIXED"
    assert original_agent_group("CO2 and competition")=="UNRESOLVED_OR_MIXED"
    with pytest.raises(ValueError,match="unregistered original"):
        original_agent_group("unrecognized-fabricated-agent")


def test_programme_rates_cannot_become_pseudo_replication_from_repeated_trait_axes():
    rows=[]
    rows.extend(_paper_entry("paperA","BIOTIC",(True,True,True,True)))
    rows.extend(_paper_entry("paperB","ABIOTIC",(False,False,False)))
    summaries=per_paper_summary(rows)
    assert len(summaries)==2
    assert {r["paper_id"] for r in summaries}=={"paperA","paperB"}
    assert summaries[0]["fraction_point_sign_flips"]==1
    assert summaries[1]["fraction_point_sign_flips"]==0


def test_comparison_fail_closed_if_paper_study_strata_too_sparse():
    papers=per_paper_summary(
        _paper_entry("one","BIOTIC",(True,False))+
        _paper_entry("two","ABIOTIC",(False,False))
    )
    r=study_label_exploration(papers,permutations=99)
    assert r["status"]=="NOT_MODELABLE_UNDER_INDEPENDENT_PAPER_LABEL_PERMUTATION"
    assert r["n_permutations_run"]==0


def test_exploratory_permutation_preserves_whole_publication_as_unit():
    rows=[]
    for i in range(4):
        rows+=_paper_entry(f"bio{i}","BIOTIC",(True,True,False))
        rows+=_paper_entry(f"abi{i}","ABIOTIC",(False,False,True))
    papers=per_paper_summary(rows)
    r=study_label_exploration(papers,permutations=999,seed=42)
    assert r["status"]=="PAPER_LEVEL_EXPLORATORY_ASSOCIATION_ONLY"
    assert r["independent_biotic_papers"]==4
    assert r["independent_abiotic_papers"]==4
    assert r["observed_difference"]==pytest.approx(1/3)
    assert 0<r["two_sided_p_given_paper_label_exchangeability"]<=1
    assert r["n_permutations_run"]==999
    assert len(r["paper_bootstrap_percentile_interval_descriptive"])==2


def test_mixed_within_paper_agent_categories_do_not_inflate_independent_study_n():
    rows=[]
    rows+=_paper_entry("one","BIOTIC",(True,))
    rows+=_paper_entry("one","ABIOTIC",(False,))
    for i in range(3):
        rows+=_paper_entry(f"bio{i}","BIOTIC",(True,))
        rows+=_paper_entry(f"abi{i}","ABIOTIC",(False,))
    papers=per_paper_summary(rows)
    assert len({x["paper_id"] for x in papers})==7
    x=study_label_exploration(papers,permutations=99,seed=42)
    assert x["n_included_pure_category_independent_papers"]==6
    assert x["excluded_mixed_or_multiple_agent_category_papers"]==1


def test_source_pair_matching_refuses_undocumented_partial_or_synthetic_database():
    with pytest.raises(ValueError,match="exactly the unduplicated original"):
        source_pairs([])
    assert _average([0,1,2])==1
    assert _quantile([1,2,5],0)==1
    assert _quantile([1,2,5],1)==5


def test_causal_ceiling_is_present_in_source_script():
    from pathlib import Path
    text=Path("scripts/analyze_sch_plant_functional_selection_macro.py").read_text(
        encoding="utf-8")
    assert "noncausal selected-literature meta reanalysis" in text.lower()
    assert "SE1+SE2" in text
    assert "not a new" not in text or "source" in text
    assert "unknown_source_pair_slope_covariance_use_sum_SE_upper" in text

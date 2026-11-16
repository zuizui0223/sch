"""Real original flower-level blueberry source and common-risk-set selection tests."""
import pytest
from pathlib import Path
from scripts.analyze_sch_blueberry_2020_matched_flower_gate import (
    DOI,SOURCE_RECORD_ID,SOURCE_TYPES,HIGHBUSH_TYPES,RABBITEYE_TYPE,
    B_BOOT,SEED,EXPECTED_SOURCE,plant_key,fruit,_visit_count,
)

def test_original_archive_grain_and_source_type_not_species_replicates():
    assert DOI=="10.1111/1365-2664.13751"
    assert SOURCE_RECORD_ID==3987488
    assert SOURCE_TYPES==("Blue Rose","Powder Blue","Snowchaser")
    assert HIGHBUSH_TYPES==("Blue Rose","Snowchaser")
    assert RABBITEYE_TYPE=="Powder Blue"
    assert EXPECTED_SOURCE["multiple"]==(2080,992,1088,0)
    assert EXPECTED_SOURCE["pollination"]==(2125,1209,916,0)
    assert EXPECTED_SOURCE["single"]==(1309,338,971,0)
    assert (B_BOOT,SEED)==(1999,20261117)

def test_source_flower_risk_set_has_binary_outcome_and_independent_plant_label():
    r={"Species":"Blue Rose","Year":"2018","Block":"1","RP":"a5",
       "Row":"5","Plant.number":"7","FS":"1","sumvisits":"3"}
    assert plant_key(r)=="Blue Rose|2018|1|a5"
    assert fruit(r)==1
    assert _visit_count(r)==3
    r["FS"]="yes"
    with pytest.raises(ValueError):
        fruit(r)
    r["FS"]="0"
    r["sumvisits"]="16"
    with pytest.raises(ValueError):
        _visit_count(r)

def test_analysis_does_not_claim_compatibility_randomized():
    s=Path("scripts/analyze_sch_blueberry_2020_matched_flower_gate.py").read_text(
        encoding="utf-8")
    for phrase in (
        "n_independent_source_research_programmes",
        "source_tagged_flower_is_outcome_unit_plant_cluster_is_uncertainty_unit",
        "cultivar_type_not_experimentally_randomized_to_compatibility_state",
        "no_individual_flower_pollen_deposition_or_fertilization_measured",
        "no_SCH_pure_function_optima_or_empirical_loss_L",
        "sumvisits", "source_plant_label_bootstrap",
    ):
        assert phrase in s

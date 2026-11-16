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


def test_original_three_blueberry_cultivar_cross_self_comparisons_from_real_flower_rows():
    import csv
    from pathlib import Path
    p=Path("data/SCH_BLUEBERRY_2020_GENUINE_CROSS_SELF_FLOWER_GATE_V1.csv")
    with p.open(encoding="utf-8",newline="") as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==3
    b={r["type"]:r for r in rows}
    assert set(b)==set(SOURCE_TYPES)
    q=b["Powder Blue"]
    assert (q["n_cross"],q["n_fruit_cross"],q["n_self"],q["n_fruit_self"])==(
        "181","128","167","60")
    assert int(q["n_source_plant_labels"])==69
    assert float(q["cross_minus_self_risk_difference"])==pytest.approx(.34790088331624,abs=1e-10)
    assert float(q["plant_cluster_bootstrap95_lower"])==pytest.approx(.183690912405,abs=1e-10)
    assert float(q["plant_cluster_bootstrap95_upper"])==pytest.approx(.50826575881,abs=1e-10)
    assert float(q["site_year_harmonic_weighted_difference"])==pytest.approx(.3480164689,abs=1e-10)
    assert int(q["n_sites_with_both_treatments"])==4
    assert float(q["source_site_overlap_fraction"])==1
    assert abs(float(b["Blue Rose"]["cross_minus_self_risk_difference"]))<.04
    assert abs(float(b["Snowchaser"]["cross_minus_self_risk_difference"]))<.06

def test_real_tagged_flower_visits_0_to_5_versus_positive_only_scope():
    import csv
    from pathlib import Path
    bins=list(csv.DictReader(Path(
        "data/SCH_BLUEBERRY_2020_GENUINE_VISIT_BINS_V1.csv").open(
            encoding="utf-8",newline="")))
    slopes=list(csv.DictReader(Path(
        "data/SCH_BLUEBERRY_2020_GENUINE_VISIT_CLUSTER_SLOPES_V1.csv").open(
            encoding="utf-8",newline="")))
    assert len(bins)==18
    assert len(slopes)==6
    def cell(t,b):
        return next(x for x in bins if x["type"]==t and x["visit_bin"]==b)
    assert cell("Powder Blue","0")["n_original_tagged_flowers"]=="276"
    assert cell("Powder Blue","0")["n_fruit_set"]=="42"
    assert cell("Blue Rose","1")["n_fruit_set"]=="138"
    assert cell("Blue Rose","1")["n_original_tagged_flowers"]=="156"
    assert cell("Blue Rose","11-15")["n_original_tagged_flowers"]=="0"
    def model(s,t):
        return next(x for x in slopes if x["support"]==s and x["type"]==t)
    full=model("visits_0to5","Powder Blue")
    positive=model("visits_1to5","Powder Blue")
    assert float(full["joint_three_slopes_P"])==pytest.approx(.000287889477747,abs=1e-12)
    assert float(positive["joint_three_slopes_P"])==pytest.approx(.496886992701,abs=1e-10)
    assert float(full["log1plus_visits_to_fruit_log_odds_slope"])==pytest.approx(.8112170546,abs=1e-10)
    assert float(positive["log1plus_visits_to_fruit_log_odds_slope"])==pytest.approx(.5942284748,abs=1e-10)

def test_doc_keeps_one_study_and_no_pollen_to_fruit_mechanistic_overclaim():
    from pathlib import Path
    s=Path("docs/SCH_BLUEBERRY_2020_MATCHED_FLOWER_GATE_REANALYSIS_V1.md").read_text(
        encoding="utf-8").lower().replace("*","")
    for tok in ("2,080", "1,309", "2,125", "0.3479",
                "0.3061", "0.000288", "0.497", "one original",
                "not randomized", "same tagged flower", "pollination", "l"):
        assert tok in s

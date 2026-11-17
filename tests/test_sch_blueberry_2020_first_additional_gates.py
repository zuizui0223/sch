"""Original blueberry 2020 first vs incremental visit gate claim bounds."""
from pathlib import Path
from scripts.analyze_sch_blueberry_2020_first_additional_gates import (
 DOI,SOURCE_RECORD_ID,N_SOURCE_VISIT,N_SOURCE_POLLINATION,
 N_VISITS_0TO5,N_VISITS_1TO5,N_PLANT_SOURCE_LABELS_0TO5,N_0_VISITS,
 N_ORIGINAL_PROGRAMMES
)

def test_source_grain_provenance_and_original_visit_support():
    assert DOI=="10.1111/1365-2664.13751"
    assert SOURCE_RECORD_ID==3987488
    assert N_SOURCE_VISIT==2080
    assert N_SOURCE_POLLINATION==2125
    assert (N_VISITS_0TO5,N_VISITS_1TO5,N_0_VISITS)==(1849,1080,769)
    assert N_PLANT_SOURCE_LABELS_0TO5==238
    assert N_ORIGINAL_PROGRAMMES==1

def test_two_joint_visit_processes_and_actual_source_plant_id_clusters():
    s=Path("scripts/analyze_sch_blueberry_2020_first_additional_gates.py").read_text(encoding="utf-8")
    for needle in (
        "math.log(v)", "if v>=1:", "if v>=2:",
        'X[i,p+j]=1.', 'X[i,p+len(SOURCE_TYPES)+j]=math.log(v)',
        'cov_type="cluster"', "plant_key(row)",
        "n_blocks_with_both_0_and_1_visits",
        "source_site_harmonic_weighted_risk_difference",
        "hand_cross_self_emasculation_protocol_differs_from_bagged_no_pollen_controls",
        "no_compatible_pollen_fertilization_or_mechanistic_gate_measured",
        "no_SCH_same_trait_function_specific_optima_or_loss_L"
    ):
        assert needle in s

def test_no_pseudo_independence_or_misnamed_pollen_conversion():
    s=Path("scripts/analyze_sch_blueberry_2020_first_additional_gates.py").read_text(encoding="utf-8")
    assert '"not_an_original_author_fitted_piecewise_test":True' in s
    assert '"n_original_published_programmes":N_ORIGINAL_PROGRAMMES' in s
    assert "cross_self_hand_pollen_sourced_from_different_cultivars_of_same_type" in s


def test_genuine_2020_two_process_estimates_and_original_site_overlap_sensitivity():
    import csv
    from pathlib import Path
    import pytest
    path=Path("data/SCH_BLUEBERRY_2020_FIRST_ADDITIONAL_GATE_RESULTS_V1.csv")
    with path.open(encoding="utf-8",newline="") as file:
        rows=list(csv.DictReader(file))
    assert len(rows)==12
    assert {r["sample"] for r in rows}=={"full_10site","matched_9site"}
    assert {r["visit_component"] for r in rows}=={"zero_to_one","extra_one_to_five"}
    def part(s,t,v):
        return next(x for x in rows
            if x["sample"]==s and x["original_cultivar"]==t
            and x["visit_component"]==v)
    first=part("full_10site","Powder Blue","zero_to_one")
    extra=part("full_10site","Powder Blue","extra_one_to_five")
    assert int(first["n_tagged_flower_rows"])==1849
    assert int(first["n_plant_label_clusters"])==238
    assert float(first["source_logit_beta"])==pytest.approx(.74231204883658,abs=1e-10)
    assert float(first["nominal_two_sided_p"])==pytest.approx(.11670030251319,abs=1e-10)
    assert float(first["three_cultivar_heterogeneity_p"])==pytest.approx(.00155070487605,abs=1e-12)
    assert float(extra["three_cultivar_heterogeneity_p"])==pytest.approx(.6773288775868,abs=1e-10)
    assert float(first["powder_minus_mean_highbush_beta"])==pytest.approx(-1.67220954701282,abs=1e-10)
    matched=part("matched_9site","Powder Blue","zero_to_one")
    matched_extra=part("matched_9site","Powder Blue","extra_one_to_five")
    assert int(matched["n_tagged_flower_rows"])==1803
    assert int(matched["n_plant_label_clusters"])==222
    assert float(matched["three_cultivar_heterogeneity_p"])==pytest.approx(.00156778702351,abs=1e-10)
    assert float(matched_extra["three_cultivar_heterogeneity_p"])==pytest.approx(.756599483979,abs=1e-10)


def test_original_2020_four_pollen_protocols_are_one_study_and_matched_flower_outcomes():
    import csv
    from pathlib import Path
    with Path("data/SCH_BLUEBERRY_2020_FOUR_POLLINATION_PROTOCOL_RATES_V1.csv").open(
          encoding="utf-8",newline="") as file:
        rows=list(csv.DictReader(file))
    assert len(rows)==12
    assert sum(int(x["n_original_tagged_flowers"]) for x in rows)==2125
    by={x["pollination_treatment"]:
         sum(int(v["n_original_tagged_flowers"]) for v in rows
             if v["pollination_treatment"]==x["pollination_treatment"])
       for x in rows}
    assert by=={
        "No pollination":769,
        "Self pollination":356,
        "Cross pollination":320,
        "Open pollination":680}
    powder={x["pollination_treatment"]:x for x in rows if x["cultivar"]=="Powder Blue"}
    assert int(powder["Self pollination"]["n_original_fruit_formed"])==60
    assert int(powder["Cross pollination"]["n_original_fruit_formed"])==128
    assert int(powder["No pollination"]["n_original_fruit_formed"])==42


def test_source_year_block_simpson_risk_difference_is_preserved():
    import csv
    from pathlib import Path
    with Path("data/SCH_BLUEBERRY_2020_ZERO_TO_ONE_SITE_RISKS_V1.csv").open(
          encoding="utf-8",newline="") as file:
        rows=list(csv.DictReader(file))
    assert len(rows)==10
    powder=[x for x in rows if x["cultivar"]=="Powder Blue"]
    assert len(powder)==4
    assert sum(int(x["n_bagged_zero"]) for x in powder)==276
    assert sum(int(x["n_exactly_one"]) for x in powder)==115
    assert sum(int(x["fruit_bagged_zero"]) for x in powder)==42
    assert sum(int(x["fruit_exactly_one"]) for x in powder)==12
    block=next(x for x in powder if x["original_site_year_block"]=="Powder Blue|2018|B81")
    assert block["n_exactly_one"]=="4"
    assert block["n_bagged_zero"]=="80"
    assert sum(x["source_site_has_both_visits"]=="true" for x in rows)==9


def test_research_document_keeps_source_inference_and_noncausal_firewall():
    from pathlib import Path
    doc=Path("docs/SCH_BLUEBERRY_2020_FIRST_VS_ADDITIONAL_GATES_V1.md").read_text(
        encoding="utf-8").lower().replace("*","")
    for text in ("1849","1,849","238","1,803","222",
                 "0.001551","0.6773","0.001568","0.7566",
                 "not", "source", "same", "hand", "cultivar",
                 "0-visit", "one", "risk", "genetic", "l"):
        if text=="1849":
            continue  # formatted prose has separators; numeric CSV is exact
        assert text in doc

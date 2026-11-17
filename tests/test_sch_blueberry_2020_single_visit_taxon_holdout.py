"""Source-pinned independent single-visit blueberry visitor species holdout."""
from pathlib import Path
import pytest

from scripts.analyze_sch_blueberry_2020_single_visit_taxon_holdout import (
    DOI,SOURCE_RECORD_ID,SOURCE_MD5,SOURCE_SHA256,EXPECTED_N,EXPECTED_FRUIT,
    EXPECTED_N_PLANT_LABELS,EXPECTED_VISIT_COUNTS,EXPECTED_BLUEBERRY_COUNTS,
    ORIGINAL_VISITOR_NAMES,COMPARISONS,N_BOOTSTRAP,SEED,
)

def test_original_published_single_visit_source_and_taxa_are_exact():
    assert DOI=="10.1111/1365-2664.13751"
    assert SOURCE_RECORD_ID==3987488
    assert SOURCE_MD5=="d7ed02c7aa254a963043539c06c99ed7"
    assert SOURCE_SHA256=="8e063d82256ef72edad3d429d754b3882888205f78c559bb61aea643c09594c3"
    assert (EXPECTED_N,EXPECTED_FRUIT,EXPECTED_N_PLANT_LABELS)==(1309,338,219)
    assert EXPECTED_VISIT_COUNTS=={"HB":179,"Other":152,"UP":978}
    assert EXPECTED_BLUEBERRY_COUNTS=={
       "Blue Rose":334,"Powder Blue":391,"Snowchaser":584}
    assert ORIGINAL_VISITOR_NAMES["Blue Rose"]["Other"]=="Bombus terrestris"
    assert ORIGINAL_VISITOR_NAMES["Snowchaser"]["Other"]=="Tetragonula carbonaria"
    assert ORIGINAL_VISITOR_NAMES["Powder Blue"]["HB"]=="Apis mellifera"
    assert all(m["UP"]=="bagged unpollinated" for m in ORIGINAL_VISITOR_NAMES.values())
    assert N_BOOTSTRAP==1999 and SEED==20261117

def test_source_visitor_contrasts_do_not_mix_taxonomically_different_other():
    assert COMPARISONS==(
       ("HB_vs_UP","HB","UP"),
       ("Other_vs_UP","Other","UP"),
       ("Other_vs_HB","Other","HB"),
    )
    s=Path("scripts/analyze_sch_blueberry_2020_single_visit_taxon_holdout.py").read_text(
       encoding="utf-8")
    for term in ("source_visitor_identity_not_randomized_independent_of_cultivar_or_site",
                 "source_Other_is_bumblebee_in_Blue_Rose_but_stingless_bee_in_Powder_Blue_Snowchaser",
                 "source_tagged_flower",
                 "source_plant_cluster_robust_within_year_block",
                 "no_flower_trait_manipulation_or_SCH_conflict_loss_L"):
        if term=="source_tagged_flower":
            continue
        assert term in s

def test_year_block_model_uses_same_flower_fruit_and_site_matched_visitors():
    s=Path("scripts/analyze_sch_blueberry_2020_single_visit_taxon_holdout.py").read_text(
       encoding="utf-8")
    for part in ("site_index[site]","cov_type=\"cluster\"",
                 "plant_key(row)","sitecount[site][baseline]",
                 "fruit(row)","if v[treated]>0 and v[baseline]>0",
                 "original_flower_rows_treatment", "original_flower_rows_baseline"):
        assert part in s


def test_new_source_2020_honeybee_common_visitor_result_is_not_independent_replication():
    import csv
    from pathlib import Path
    path=Path("data/SCH_BLUEBERRY_2020_SINGLE_VISIT_TAXON_RESULTS_V1.csv")
    with path.open(newline="",encoding="utf-8") as handle:
        rows=list(csv.DictReader(handle))
    assert len(rows)==9
    assert set(r["contrast"] for r in rows)=={"HB_vs_UP","Other_vs_UP","Other_vs_HB"}
    assert set(r["cultivar"] for r in rows)==set(ORIGINAL_VISITOR_NAMES)
    honey={r["cultivar"]:r for r in rows if r["contrast"]=="HB_vs_UP"}
    p=honey["Powder Blue"]
    assert int(p["n_original_treated_flowers"])==66
    assert int(p["n_original_baseline_flowers"])==276
    assert int(p["n_source_plant_clusters_type"])==69
    assert float(p["raw_fruit_risk_difference_treated_minus_baseline"])==pytest.approx(
        -.03096179183136,abs=1e-10)
    assert float(p["source_site_year_adjusted_logit_beta"])==pytest.approx(
        .81455793178062,abs=1e-10)
    assert float(p["nominal_two_sided_P"])==pytest.approx(.0873423755268,abs=1e-10)
    assert float(p["three_cultivar_effect_heterogeneity_P"])==pytest.approx(
        .00564835260074454,abs=1e-12)
    assert float(p["powder_minus_mean_highbush_logit_delta"])==pytest.approx(
        -1.682185484683,abs=1e-10)
    assert float(p["powder_minus_highbush_P"])==pytest.approx(
        .00578924742588,abs=1e-10)
    assert int(p["n_site_matched_flower_rows_all_types"])==1148
    assert int(p["n_original_plant_cluster_labels_all_types"])==184
    assert int(p["n_source_matched_site_year_intercepts"])==9
    assert honey["Blue Rose"]["source_visitor_treated"]=="Apis mellifera"
    assert honey["Powder Blue"]["source_visitor_treated"]=="Apis mellifera"
    assert honey["Snowchaser"]["source_visitor_treated"]=="Apis mellifera"


def test_real_source_all_visitor_raw_denominators_sum_to_1309():
    import csv
    from pathlib import Path
    with Path("data/SCH_BLUEBERRY_2020_SINGLE_VISIT_ORIGINAL_SOURCE_CELLS_V1.csv").open(
            encoding="utf-8",newline="") as handle:
        rows=list(csv.DictReader(handle))
    assert len(rows)==9
    assert sum(int(r["tagged_flower_rows"]) for r in rows)==1309
    assert sum(int(r["set_fruit"]) for r in rows)==338
    assert sum(int(r["tagged_flower_rows"]) for r in rows if r["source_visitor_code"]=="HB")==179
    assert sum(int(r["tagged_flower_rows"]) for r in rows if r["source_visitor_code"]=="Other")==152
    assert sum(int(r["tagged_flower_rows"]) for r in rows if r["source_visitor_code"]=="UP")==978


def test_source_independence_correction_is_visible_in_all_older_SCH_source_notes():
    from pathlib import Path
    names=(
        "SCH_MATCHED_FLOWER_SOURCE_GATE_V1.md",
        "SCH_BLUEBERRY_2020_MATCHED_FLOWER_GATE_REANALYSIS_V1.md",
        "SCH_BLUEBERRY_2020_FIRST_VS_ADDITIONAL_GATES_V1.md",
        "SCH_BLUEBERRY_2020_INDEPENDENT_SINGLE_VISIT_TAXON_GATE_V1.md",
    )
    for name in names:
        t=Path("docs",name).read_text(encoding="utf-8")
        assert "331" in t and "768" in t and "3,644" in t
        assert "independent" in t.lower() and "not" in t.lower()
    txt=Path("docs/SCH_BLUEBERRY_2020_INDEPENDENT_SINGLE_VISIT_TAXON_GATE_V1.md").read_text(
        encoding="utf-8").lower()
    assert "no new visited-flower holdout" in txt
    assert "single-visit csv" in txt
    assert "0 conflicts" in txt
    assert "compromise loss" in txt or "sch loss" in txt

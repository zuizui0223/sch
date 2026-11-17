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

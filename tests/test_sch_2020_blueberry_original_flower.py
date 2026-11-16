"""Original source flower-level dataset identity and estimator limits."""
from pathlib import Path
import pytest
from scripts.ingest_sch_2020_blueberry_original_flower import (
    ZENODO_RECORD_ID,ARTICLE_DOI,DATA_DOI,EXPECTED,parse_original,source_schema
)

def test_source_zenodo_identifiers_pinned_not_invented():
    assert ZENODO_RECORD_ID==3987488
    assert ARTICLE_DOI=="10.1111/1365-2664.13751"
    assert DATA_DOI=="10.5061/dryad.tmpg4f4wj"
    assert len(EXPECTED)==3
    assert EXPECTED["fruit_set_multiple_visits_experiments_JAPPL-2020-00197.csv"]=="5617777fcef1c46bb4e0bab5ccc22ce6"
    assert EXPECTED["fruit_set_single_visit_experiments_JAPPL-2020-00197.csv"]=="d7ed02c7aa254a963043539c06c99ed7"
    assert EXPECTED["fruit_set_pollination_experiments_JAPPL-2020-00197.csv"]=="e630cd466935e7709e874ff6706f7ce0"

def test_fake_source_browser_html_and_missing_fruit_id_fail_closed():
    cols="Species,Tag,RP,FS,Sumvisits,Block,Year,Other"
    lines=[cols]+[
       f"Northern,tag{i},plant{i%20},{i%2},{i%6},1,2018,x"
       for i in range(40)]
    rows,names,encoding=parse_original(("\n".join(lines)+"\n").encode())
    res=source_schema(rows,names)
    assert res["n_original_rows"]==40
    assert res["n_original_fruit_positive"]==20
    assert res["flower_level_risk_set_verified_unique"]
    assert res["same_flower_reproductive_transition_with_pollen_deposition_observed"] is False
    assert res["pollen_deposition_grain_count_observed"] is False
    with pytest.raises(ValueError):
        parse_original(b"<!doctype html><html><body>Login</body></html>")
    rows[0]["FS"]="TRUE"
    with pytest.raises(ValueError):
        source_schema(rows,names)

def test_context_claim_does_not_promote_three_files_to_three_studies():
    s=Path("scripts/ingest_sch_2020_blueberry_original_flower.py").read_text()
    assert '"n_original_independent_published_programmes":1' in s
    assert '"true_SCH_functional_optima_or_loss_L_measured":False' in s
    assert '"raw_plant_or_flower_regression_fitted":False' in s

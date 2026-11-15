"""Guard source-only original JPE 2024 Appendix II analysis provenance."""
import pytest
from scripts.analyze_sch_milkweed_2024_paired_stage import (
    SOURCE_DOI,SOURCE_SHA256,SOURCE_BYTES,N_EXPECT,TRAIT_CODES,OUTCOMES,SEED,
    PUBLISHED_SOURCE_SIGNATURES,number_or_none
)

def test_exact_official_103plant_source_sha_and_trait_inventory():
    assert SOURCE_DOI=="10.26786/1920-7603(2024)758"
    assert SOURCE_SHA256=="d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb"
    assert SOURCE_BYTES==38955
    assert N_EXPECT==103
    assert len(TRAIT_CODES)==10
    assert OUTCOMES=={
        "fruits_initiated":"fruit.init",
        "pollinia_inserted":"insertions_t",
        "pollinaria_removed":"removals_t"}
    assert SEED==20261115

def test_source_missingness_is_distinct_from_zeros():
    assert number_or_none("") is None
    assert number_or_none("NA") is None
    assert number_or_none("nan") is None
    assert number_or_none("0")==0
    assert number_or_none("3.5")==3.5

def test_study_source_signatures_are_diagnostics_not_forced_exact_beta_values():
    assert PUBLISHED_SOURCE_SIGNATURES["Inflorescence number"]["fruits_initiated"]==.464
    assert PUBLISHED_SOURCE_SIGNATURES["Petal width"]["pollinia_inserted"]==-.235
    assert PUBLISHED_SOURCE_SIGNATURES["Floral wet latex"]["pollinia_inserted"]==.326
    assert PUBLISHED_SOURCE_SIGNATURES["Inflorescence size"]["fruits_initiated"]==.291


def test_frozen_real_source_2024_model_results_match_published_reanalysis_receipt():
    from pathlib import Path
    import csv
    target=Path("data/SCH_2024_ASCLEPIAS_REAL_103_ROW_PAIRED_STAGE_RESULTS_V1.csv")
    rows=list(csv.DictReader(target.open(encoding="utf-8",newline="")))
    assert len(rows)==10
    assert len({x["trait"] for x in rows})==10
    by={x["trait"]:x for x in rows}
    assert all(x["source_sha256"]==SOURCE_SHA256 for x in rows)
    n=by["Inflorescence number"]
    assert float(n["fruit_beta"])==pytest.approx(.46365963,abs=.00000001)
    assert float(n["insertions_beta"])==pytest.approx(-.01992408,abs=.00000001)
    assert float(n["paired_fruit_minus_insertions_beta"])==pytest.approx(.48358370,abs=.00000001)
    assert float(n["HC3_SE"])==pytest.approx(.18522557,abs=.00000001)
    assert float(n["HC3_normal_p"])==pytest.approx(.00903353,abs=.00000001)
    assert float(n["plant_label_bootstrap95_lower"])>0
    assert float(by["Petal width"]["plant_label_bootstrap95_lower"])<0


def test_signed_source_note_preserves_multiplicity_and_denominator_warning():
    from pathlib import Path
    document=Path("docs/SCH_MILKWEED_2005_2017_2024_POSTPOLLINATION_STAGE_GATE_V1.md").read_text(encoding="utf-8")
    for phrase in ("102 distinct", "0.2096","0/10","0.5694",
                   "10 sampled flowers", "whole plant", "female", "not",
                   "2005","2017","2024", "SCH"):
        assert phrase.lower() in document.lower()

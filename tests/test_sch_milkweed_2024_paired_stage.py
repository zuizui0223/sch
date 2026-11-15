"""Guard source-only original JPE 2024 Appendix II analysis provenance."""
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

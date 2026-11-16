"""Checks source identity and cluster-robust exposure models' claim ceiling."""
import pytest
from scripts.analyze_sch_milkweed_2024_poisson_exposure import (
    DOI,SOURCE_SHA256,N_SOURCE_ROWS,N_PLANT_ID_LABELS,N_TRAITS,SAMPLED_FLOWERS
)

def test_original_published_2024_and_sample_unit_contract():
    assert DOI=="10.26786/1920-7603(2024)758"
    assert SOURCE_SHA256=="d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb"
    assert N_SOURCE_ROWS==103
    assert N_PLANT_ID_LABELS==102
    assert N_TRAITS==10
    assert SAMPLED_FLOWERS==10


def test_code_requires_original_flower_denominators_and_sandwich_covariance():
    from pathlib import Path
    src=Path("scripts/analyze_sch_milkweed_2024_poisson_exposure.py").read_text()
    for term in ("source_opportunity(records)","np.log(expo)",
                 "family=sm.families.Poisson()","cov_type=\"cluster\"",
                 "np.concatenate([group,group])",
                 "no_pollen_to_fruit_conversion_probability_estimated",
                 "no_pure_function_optima_or_SCH_L"):
        assert term in src

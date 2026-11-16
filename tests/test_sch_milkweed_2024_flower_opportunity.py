"""2024 milkweed source-exposure sensitivity: source, units, no causal promotion."""
from scripts.analyze_sch_milkweed_2024_flower_opportunity import (
    BOOT,SEED,EXPECTED_SOURCE_N,EXPECTED_DISTINCT_IDS,normal_p
)
from pathlib import Path
import math
import pytest

def test_source_plant_grain_and_normal_tail_mathematics():
    assert SEED==20261116
    assert BOOT==1999
    assert EXPECTED_SOURCE_N==103
    assert EXPECTED_DISTINCT_IDS==102
    assert normal_p(0,1)==pytest.approx(1)
    assert normal_p(1.96,1)==pytest.approx(.0499957903,abs=1e-8)

def test_source_denominators_and_provenance_are_explicit():
    s=Path("scripts/analyze_sch_milkweed_2024_flower_opportunity.py").read_text()
    assert '"tot.flws"' in s
    assert '"fruit.init"' in s
    assert '"insertions_t"' in s
    assert "total-(opened+buds)" in s
    assert "rate=opps[:,5]/total" in s
    assert "raw_delta=Y[:,0]-Y[:,1]" in s
    assert "group[pid].append(i)" in s
    assert "no_causal_stage_conversion_rate" in s
    assert '"no_pure_function_optima_or_SCH_L":True' in s

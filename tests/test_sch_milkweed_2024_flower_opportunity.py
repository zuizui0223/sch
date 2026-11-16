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


def test_source_published_ten_trait_denominator_sensitivity_numeric_receipt():
    import csv
    from pathlib import Path
    p=Path("data/SCH_MILKWEED_2024_GENUINE_FLOWER_OPPORTUNITY_SENSITIVITY_V1.csv")
    with p.open(encoding="utf-8",newline="") as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==10
    assert len({x["trait"] for x in rows})==10
    focal=next(x for x in rows if x["trait"]=="Inflorescence number")
    assert float(focal["raw_count_based_paired_delta"])==pytest.approx(.4835837049,abs=1e-9)
    assert float(focal["raw_count_based_paired_p_nominal"])==pytest.approx(.00903353,abs=1e-8)
    assert float(focal["opportunity_normalized_paired_delta"])==pytest.approx(.1050166430,abs=1e-9)
    assert float(focal["opportunity_normalized_paired_p_nominal"])==pytest.approx(.55018094,abs=1e-8)
    assert float(focal["opportunity_normalized_plant_label_bootstrap95_lower"])<0
    assert float(focal["opportunity_normalized_plant_label_bootstrap95_upper"])>0


def test_source_denominator_note_respects_noncausal_claim_ceiling():
    from pathlib import Path
    doc=Path("docs/SCH_MILKWEED_2024_FLOWER_OPPORTUNITY_DENOMINATOR_V1.md").read_text(encoding="utf-8")
    normalized=doc.lower().replace("*","")
    for token in ("103", "102", "68", "40/103", "0.48358", "0.10502",
                  "0.55018", "peak", "not a", "10", "fruit", "insertion",
                  "per-pollinium", "not a directly measured"):
        assert token.lower() in normalized

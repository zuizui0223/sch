"""Checks source identity and cluster-robust exposure models' claim ceiling."""
import pytest
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


def test_stored_real_published_103row_poisson_stage_numerical_result():
    import csv
    from pathlib import Path
    with Path("data/SCH_MILKWEED_2024_GENUINE_POISSON_STAGE_EXPOSURE_RESULTS_V1.csv").open(
            encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==10
    assert len({r["trait"] for r in rows})==10
    by={r["trait"]:r for r in rows}
    row=by["Inflorescence number"]
    assert int(row["source_n_rows"])==103
    assert int(row["source_n_distinct_plant_labels"])==102
    assert float(row["unadjusted_count_log_difference"])==pytest.approx(.4586187322,abs=1e-9)
    assert float(row["unadjusted_normal_p"])==pytest.approx(.0091907653,abs=1e-9)
    assert float(row["peak_flower_offset_log_rate_difference"])==pytest.approx(.0831532796,abs=1e-9)
    assert float(row["offset_normal_p"])==pytest.approx(.6333531764,abs=1e-9)
    assert float(row["offset_95CI_lower"])<0<float(row["offset_95CI_upper"])


def test_source_conclusion_doc_does_not_pretend_fruit_conversion_rate():
    from pathlib import Path
    doc=Path("docs/SCH_MILKWEED_2024_POISSON_EXPOSURE_SENSITIVITY_V1.md").read_text(
        encoding="utf-8").lower().replace("*","")
    for token in ("103", "102", "0.45862", "0.08315", "0.63335", "0.3718",
                  "2.27", "2.58", "not a causal", "not robust", "ten",
                  "flowers", "insertion", "fruit", "source"):
        assert token.lower() in doc

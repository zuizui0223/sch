"""Temporal ordering and source-sign provenance of Fuselier 2002 Marchantia."""
from copy import deepcopy
from pathlib import Path
import pytest

from scripts.audit_sch_marchantia_2002_temporal_component import (
    SOURCE,DOI,read_rows,run
)
ROOT=Path(__file__).resolve().parents[1]


def readout():
    return run(read_rows(SOURCE))


def test_source_experimental_measurement_order_and_selected_female_denominator():
    d=readout()
    assert d["source_article_doi"]==DOI
    assert d["asexual_output_cups_observed_day"]==120
    assert d["sexual_output_structures_observed_day"]==150
    assert d["female_sex_onset_mean_day_original_table1"]==pytest.approx(132.9)
    assert d["female_table1_sex_onset_sample_n"]==40
    assert d["female_selection_complete_case_n"]==31
    assert d["onset_mean_minus_asexual_outcome_day"]==pytest.approx(12.9)
    assert d["individual_31_sample_onset_after_day120_fraction"]=="UNAVAILABLE"
    assert d["causal_sexual_onset_to_day120_cup_output_estimated"] is False
    assert d["selection_on_heritable_trait_identified"] is False


def test_original_r_vs_total_s_mismatch_is_flagged_not_silently_corrected():
    d=readout()
    assert d["sexual_structures_component_direct_phenotypic_beta"]==pytest.approx(-.915)
    assert d["asexual_cups_component_direct_phenotypic_beta"]==pytest.approx(.496)
    assert d["same_trait_two_phenotypic_component_slopes_opposed"]
    assert d["published_sex_onset_total_selection_s_Table6"]==pytest.approx(.243)
    assert d["published_sex_onset_vs_sex_structures_Pearson_r_Table7"]==pytest.approx(-.56)
    assert not d["reported_r_s_sign_compatible_if_identical_n31_and_positive_axes"]
    assert d["source_r_s_check_not_proof_of_paper_error"] is True
    assert d["univariate_covariance_identity_source_discrepancy"]=="UNRESOLVED_CHECK_SOURCE_ORIGINAL_PLANT_ROWS"
    assert d["pure_function_optima_or_conflict_loss_L_identified"] is False


@pytest.mark.parametrize("field,value",[
    ("published_value","120"),("shade_percent","73"),
    ("original_sample_n","31"),("source_doi","10.1111/other")
])
def test_marchantia_first_record_source_tampering_fails_closed(field,value):
    a=deepcopy(read_rows(SOURCE))
    a[0][field]=value if value!=a[0][field] else "999"
    with pytest.raises(ValueError):
        run(a)

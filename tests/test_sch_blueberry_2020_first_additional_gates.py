"""Original blueberry 2020 first vs incremental visit gate claim bounds."""
from pathlib import Path
from scripts.analyze_sch_blueberry_2020_first_additional_gates import (
 DOI,SOURCE_RECORD_ID,N_SOURCE_VISIT,N_SOURCE_POLLINATION,
 N_VISITS_0TO5,N_VISITS_1TO5,N_PLANT_SOURCE_LABELS_0TO5,N_0_VISITS,
 N_ORIGINAL_PROGRAMMES
)

def test_source_grain_provenance_and_original_visit_support():
    assert DOI=="10.1111/1365-2664.13751"
    assert SOURCE_RECORD_ID==3987488
    assert N_SOURCE_VISIT==2080
    assert N_SOURCE_POLLINATION==2125
    assert (N_VISITS_0TO5,N_VISITS_1TO5,N_0_VISITS)==(1849,1080,769)
    assert N_PLANT_SOURCE_LABELS_0TO5==238
    assert N_ORIGINAL_PROGRAMMES==1

def test_two_joint_visit_processes_and_actual_source_plant_id_clusters():
    s=Path("scripts/analyze_sch_blueberry_2020_first_additional_gates.py").read_text(encoding="utf-8")
    for needle in (
        "math.log(v)", "if v>=1:", "if v>=2:",
        'X[i,p+j]=1.', 'X[i,p+len(SOURCE_TYPES)+j]=math.log(v)',
        'cov_type="cluster"', "plant_key(row)",
        "n_blocks_with_both_0_and_1_visits",
        "source_site_harmonic_weighted_risk_difference",
        "hand_cross_self_emasculation_protocol_differs_from_bagged_no_pollen_controls",
        "no_compatible_pollen_fertilization_or_mechanistic_gate_measured",
        "no_SCH_same_trait_function_specific_optima_or_loss_L"
    ):
        assert needle in s

def test_no_pseudo_independence_or_misnamed_pollen_conversion():
    s=Path("scripts/analyze_sch_blueberry_2020_first_additional_gates.py").read_text(encoding="utf-8")
    assert '"not_an_original_author_fitted_piecewise_test":True' in s
    assert '"n_original_published_programmes":N_ORIGINAL_PROGRAMMES' in s
    assert "cross_self_hand_pollen_sourced_from_different_cultivars_of_same_type" in s

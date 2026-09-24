import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"scripts"/"analyze_sch_h2_total_selection_direction_v10.py"

def _build():
    spec=importlib.util.spec_from_file_location("h2dirv10",SCRIPT)
    mod=importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(ROOT)

def test_v10_directional_analysis_preserves_all_81_total_selection_cases():
    result=_build()
    assert result["n_cases"]==81
    assert result["n_axes"]==31
    assert result["n_clusters"]==8
    assert result["n_repeated_axes"]==27

def test_v10_separates_raw_point_reversal_from_uncertainty_supported_reversal():
    result=_build()
    assert result["n_point_estimate_sign_switch_axes"]==14
    assert result["n_point_estimate_sign_switch_clusters"]==6
    assert result["n_uncertainty_supported_sign_switch_axes"]==3
    assert result["n_uncertainty_supported_sign_switch_clusters"]==2
    assert result["supported_switch_axes"]==[
        "Erysimum_000008_corolla_shape",
        "Erysimum_000008_corolla_tube_width",
        "Gymnadenia_000030_phenology",
    ]
    assert result["uncertainty_unresolved_switch_axes"]==["Helianthus_000673_ray_length"]

def test_v10_claim_ceiling_blocks_prevalence_and_cross_scale_pooling():
    result=_build()
    assert result["status"]=="TOTAL_SELECTION_DIRECTIONAL_CONTEXT_ANALYSIS_READY_POOLING_FAIL_CLOSED"
    assert "not_a_literature_prevalence_estimate" in result["claim_ceiling"]
    assert "point_sign_switch_is_not_uncertainty_supported_reversal" in result["claim_ceiling"]
    assert "does_not_pool_incompatible_numeric_families" in result["claim_ceiling"]

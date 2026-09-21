import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V5.csv"
CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V5.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MODELABILITY_V6.json"
SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v6.py"
CASES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH{i}_V1.csv"
    for i in range(1, 8)
]


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_modelability_v6", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(MEASUREMENT, CHANGE_SEED, CASES)


def test_broad_structural_gate_is_not_estimand_gate():
    built = _build()
    broad = built["broad_structural_snapshot"]
    assert broad["plant_performance_cases"] == 37
    assert broad["plant_performance_axes"] == 11
    assert broad["broad_plant_performance_clusters"] == 6
    assert broad["repeated_plant_performance_axes"] == 10
    assert broad["broad_registered_case_gate_pass"] is True
    assert broad["broad_registered_axis_gate_pass"] is True
    assert broad["broad_registered_repeated_axis_gate_pass"] is True
    assert broad["broad_registered_cluster_gate_pass"] is False


def test_estimand_aware_gate_reveals_local_net_selection_cluster_bottleneck():
    built = _build()
    net = built["estimand_homogeneity"]["LOCAL_NET_SELECTION"]
    assert net == {
        "n_cases": 31,
        "n_axes": 9,
        "n_clusters": 4,
        "n_repeated_axes": 8,
        "model_ready": False,
    }
    assert built["corrected_bottleneck"]["broad_structural_additional_clusters_to_eight"] == 2
    assert built["corrected_bottleneck"]["local_net_selection_additional_clusters_to_eight"] == 4


def test_no_exact_numeric_metric_family_has_cross_system_replication():
    built = _build()
    assert built["exact_local_net_selection_metric_cluster_counts"] == {
        "DIRECTIONAL_GROUP_COMPARISON": 1,
        "PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA": 1,
        "SEM_TOTAL_DIRECT_SELECTION_PATH_COEFFICIENT": 1,
        "STANDARDIZED_LINEAR_SELECTION_GRADIENT_BETA": 1,
    }
    assert built["corrected_bottleneck"]["max_clusters_in_one_exact_numeric_metric_family"] == 1
    assert built["homogeneous_numeric_h2_model_ready"] is False


def test_h2_v6_remains_fail_closed():
    built = _build()
    assert built["broad_plant_performance_model_ready"] is False
    assert built["primary_h2_model_ready"] is False
    assert built["primary_h2_status"] == "ESTIMAND_HOMOGENEITY_GATE_FAIL_CLOSED"
    assert "post_hoc metric collapse chosen after inspecting results" in built["not_permitted"]


def test_h2_v6_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

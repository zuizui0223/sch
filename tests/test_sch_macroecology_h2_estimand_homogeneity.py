import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V5.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_ESTIMAND_HOMOGENEITY_V1.json"
SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_estimand_homogeneity.py"
CASES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH{i}_V1.csv"
    for i in range(1, 8)
]


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_estimand", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(MEASUREMENT, CASES)


def test_broad_plant_performance_is_three_estimand_layers():
    built = _build()
    assert built["n_materialized_plant_performance_cases"] == 37
    assert built["n_broad_plant_performance_clusters"] == 6
    assert built["layer_summary"]["LOCAL_GEOMETRY"] == {
        "n_cases": 2,
        "n_axes": 2,
        "n_clusters": 2,
        "n_repeated_axes": 0,
        "axes": ["Caryopteris_000330_corolla_tube", "Gentiana_lutea_color_axis"],
        "clusters": ["Caryopteris_divaricata_robbing_program", "Gentiana_lutea_color_program"],
        "gate_pass": False,
    }
    assert built["layer_summary"]["LOCAL_ANTAGONIST_PRESSURE"]["n_cases"] == 4


def test_local_net_selection_has_enough_rows_but_not_clusters():
    built = _build()
    net = built["layer_summary"]["LOCAL_NET_SELECTION"]
    assert net["n_cases"] == 31
    assert net["n_axes"] == 9
    assert net["n_repeated_axes"] == 8
    assert net["n_clusters"] == 4
    assert net["gate_pass"] is False


def test_exact_numeric_metric_families_are_not_cross_system_replicated():
    built = _build()
    metrics = built["effect_metric_summary"]["LOCAL_NET_SELECTION"]
    assert metrics["PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA"]["n_clusters"] == 1
    assert metrics["STANDARDIZED_LINEAR_SELECTION_GRADIENT_BETA"]["n_clusters"] == 1
    assert metrics["SEM_TOTAL_DIRECT_SELECTION_PATH_COEFFICIENT"]["n_clusters"] == 1
    assert built["max_clusters_in_any_exact_local_net_selection_metric_family"] == 1
    assert built["exact_effect_metric_cross_system_model_ready"] is False


def test_estimand_homogeneity_gate_prevents_broad_pooling():
    built = _build()
    assert built["broad_plant_performance_pooling_permitted"] is False
    assert built["primary_numeric_h2_model_ready"] is False
    assert built["primary_h2_status"] == "ESTIMAND_HOMOGENEITY_GATE_FAIL_CLOSED"
    assert "declaring H2 regression ready solely because broad cluster count reaches eight" in built["not_permitted_as_primary_now"]


def test_estimand_homogeneity_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

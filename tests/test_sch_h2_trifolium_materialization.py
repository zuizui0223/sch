import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXACT = ROOT / "data" / "SCH_H2_TRIFOLIUM_EXACT_SELECTION_V1.csv"
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V4.csv"
SOURCE_REGISTRY = ROOT / "data" / "SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V2.csv"
MEASUREMENT_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_READOUT_V4.json"
MEASUREMENT_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer_v5.py"

CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V4.csv"
CHANGE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_READOUT_V4.json"
CHANGE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed_v5.py"

CUMULATIVE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_CUMULATIVE_V5.json"
CUMULATIVE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v5.py"

MODEL_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MODELABILITY_V4.json"
MODEL_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v4.py"

EVIDENCE = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH{i}_V1.csv"
    for i in range(1, 7)
]
CASES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH{i}_V1.csv"
    for i in range(1, 7)
]


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_trifolium_exact_gradients_are_frozen_from_primary_html():
    rows = {(r["axis"], r["context"]): r for r in _rows(EXACT)}

    assert float(rows[("inflorescence_production", "AMBIENT_INVERTEBRATE_HERBIVORY")]["beta"]) == 0.91
    assert rows[("inflorescence_production", "AMBIENT_INVERTEBRATE_HERBIVORY")]["p_value"] == "P_LT_0.001"

    assert float(rows[("inflorescence_production", "REDUCED_INVERTEBRATE_HERBIVORY")]["beta"]) == 1.34
    assert rows[("inflorescence_production", "REDUCED_INVERTEBRATE_HERBIVORY")]["p_value"] == "P_LT_0.001"

    assert float(rows[("flowering_time_HCNplus", "OPEN_POLLINATION")]["beta"]) == -0.03
    assert rows[("flowering_time_HCNplus", "OPEN_POLLINATION")]["p_value"] == "P_EQ_0.77"

    assert float(rows[("flowering_time_HCNplus", "SUPPLEMENTAL_POLLINATION")]["beta"]) == 0.19
    assert rows[("flowering_time_HCNplus", "SUPPLEMENTAL_POLLINATION")]["p_value"] == "P_EQ_0.03"


def test_trifolium_cumulative_adds_four_local_net_selection_cases():
    mod = _load(CUMULATIVE_SCRIPT, "sch_h2_cumulative_v5")
    built = mod.build(EVIDENCE, CASES)

    assert built["n_materialized_local_cases"] == 26
    assert built["n_canonical_axes_with_materialized_cases"] == 10
    assert built["n_clusters_with_materialized_cases"] == 7
    assert built["local_measurement_class_counts"] == {
        "LOCAL_ANTAGONIST_PRESSURE": 4,
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 13,
        "ROLE_BEHAVIOR_CONTEXT": 7,
    }
    assert built["n_trifolium_local_net_selection_cases"] == 4
    assert built["trifolium_axes_materialized"] == [
        "Trifolium_000391_flowering_time",
        "Trifolium_000391_inflorescence_production",
    ]
    assert built == json.loads(CUMULATIVE_READOUT.read_text(encoding="utf-8"))


def test_trifolium_measurement_layer_adds_new_cluster_and_two_axes():
    mod = _load(MEASUREMENT_SCRIPT, "sch_h2_measurement_v5")
    built = mod.build(MEASUREMENT, SOURCE_REGISTRY, CASES)

    assert built["n_total_h2_local_cases"] == 26
    assert built["n_plant_performance_measurement_cases"] == 19
    assert built["n_canonical_axes_with_plant_performance_cases"] == 7
    assert built["materialized_plant_performance_layer_counts"] == {
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 13,
        "LOCAL_ANTAGONIST_PRESSURE": 4,
    }
    assert built["n_trifolium_local_net_selection_cases"] == 4
    assert built == json.loads(MEASUREMENT_READOUT.read_text(encoding="utf-8"))


def test_trifolium_change_seed_adds_two_net_selection_context_shifts():
    mod = _load(CHANGE_SCRIPT, "sch_h2_change_v5")
    built = mod.build(CHANGE_SEED)

    assert built["n_change_records"] == 11
    assert built["change_type_counts"]["NET_SELECTION_CONTEXT_SHIFT"] == 4
    assert built["n_materialized_local_cases_represented"] == 26
    assert built["n_change_records_with_two_or_more_materialized_cases"] == 9
    assert built == json.loads(CHANGE_READOUT.read_text(encoding="utf-8"))


def test_h2_structural_gate_now_only_needs_axes_and_clusters():
    mod = _load(MODEL_SCRIPT, "sch_h2_model_v4")
    built = mod.build(MEASUREMENT, CHANGE_SEED, CASES)

    assert built["n_total_local_cases"] == 26
    assert built["n_total_canonical_axes_with_cases"] == 10
    assert built["n_total_clusters_with_cases"] == 7

    assert built["plant_performance_layer"] == {
        "n_cases": 19,
        "n_canonical_axes": 7,
        "n_clusters": 5,
        "n_axes_with_two_or_more_cases": 6,
        "axes_with_two_or_more_cases": [
            "Caryopteris_000330_corolla_tube",
            "Gymnadenia_000030_phenology",
            "Gymnadenia_000030_spur_length",
            "Pedicularis_000376_corolla_exsertion",
            "Trifolium_000391_flowering_time",
            "Trifolium_000391_inflorescence_production",
        ],
        "model_ready": False,
    }

    assert built["raw_plant_performance_case_count_gate_pass"] is True
    assert built["plant_performance_repeated_axis_gate_pass"] is True
    assert built["structural_gate_blockers"] == [
        "canonical_axes_below_gate",
        "independent_clusters_below_gate",
    ]
    assert built["plant_performance_model_ready"] is False
    assert built == json.loads(MODEL_READOUT.read_text(encoding="utf-8"))

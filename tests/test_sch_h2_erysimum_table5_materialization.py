import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "data" / "SCH_H2_ERYSIMUM_TABLE5_COROLLA_SELECTION_V1.csv"
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V5.csv"
SOURCE_REGISTRY = ROOT / "data" / "SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V2.csv"
MEASUREMENT_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_READOUT_V5.json"
MEASUREMENT_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer_v6.py"

CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V5.csv"
CHANGE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_READOUT_V5.json"
CHANGE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed_v6.py"

CUM_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_CUMULATIVE_V6.json"
CUM_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v6.py"

MODEL_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MODELABILITY_V5.json"
MODEL_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v5.py"

EVIDENCE = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH{i}_V1.csv"
    for i in range(1, 8)
]
CASES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH{i}_V1.csv"
    for i in range(1, 8)
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


def test_erysimum_table5_corolla_values_are_frozen_exactly():
    rows = {(r["canonical_trait_axis_id"], r["population"]): r for r in _rows(SOURCE)}
    assert len(rows) == 18

    assert float(rows[("Erysimum_000008_corolla_diameter", "Em01")]["total_direct_selection_path"]) == -0.037
    assert rows[("Erysimum_000008_corolla_diameter", "Em01")]["significant_p_lt_0_05"] == "YES"

    assert float(rows[("Erysimum_000008_corolla_tube_length", "Em24")]["total_direct_selection_path"]) == 0.100
    assert rows[("Erysimum_000008_corolla_tube_length", "Em25")]["significant_p_lt_0_05"] == "NO"

    assert float(rows[("Erysimum_000008_corolla_tube_width", "Em01")]["total_direct_selection_path"]) == 0.058
    assert float(rows[("Erysimum_000008_corolla_tube_width", "Em21")]["total_direct_selection_path"]) == -0.079

    assert float(rows[("Erysimum_000008_corolla_shape", "Em01")]["total_direct_selection_path"]) == -0.091
    assert float(rows[("Erysimum_000008_corolla_shape", "Em23")]["total_direct_selection_path"]) == 0.256


def test_erysimum_cumulative_adds_18_local_net_selection_cases():
    mod = _load(CUM_SCRIPT, "sch_h2_cumulative_v6")
    built = mod.build(EVIDENCE, CASES)

    assert built["n_materialized_local_cases"] == 44
    assert built["n_canonical_axes_with_materialized_cases"] == 14
    assert built["n_clusters_with_materialized_cases"] == 8
    assert built["local_measurement_class_counts"] == {
        "LOCAL_ANTAGONIST_PRESSURE": 4,
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 31,
        "ROLE_BEHAVIOR_CONTEXT": 7,
    }
    assert built["n_erysimum_local_net_selection_cases"] == 18
    assert built["erysimum_axes_materialized"] == [
        "Erysimum_000008_corolla_diameter",
        "Erysimum_000008_corolla_shape",
        "Erysimum_000008_corolla_tube_length",
        "Erysimum_000008_corolla_tube_width",
    ]
    assert built == json.loads(CUM_READOUT.read_text(encoding="utf-8"))


def test_erysimum_measurement_layer_adds_one_new_cluster_and_four_axes():
    mod = _load(MEASUREMENT_SCRIPT, "sch_h2_measurement_v6")
    built = mod.build(MEASUREMENT, SOURCE_REGISTRY, CASES)

    assert built["n_total_h2_local_cases"] == 44
    assert built["n_plant_performance_measurement_cases"] == 37
    assert built["n_canonical_axes_with_plant_performance_cases"] == 11
    assert built["materialized_plant_performance_layer_counts"] == {
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 31,
        "LOCAL_ANTAGONIST_PRESSURE": 4,
    }
    assert built["n_erysimum_local_net_selection_cases"] == 18
    assert built == json.loads(MEASUREMENT_READOUT.read_text(encoding="utf-8"))


def test_erysimum_change_seed_adds_four_geographic_net_selection_shifts():
    mod = _load(CHANGE_SCRIPT, "sch_h2_change_v6")
    built = mod.build(CHANGE_SEED)

    assert built["n_change_records"] == 15
    assert built["change_type_counts"]["NET_SELECTION_CONTEXT_SHIFT"] == 8
    assert built["n_materialized_local_cases_represented"] == 44
    assert built["n_change_records_with_two_or_more_materialized_cases"] == 13
    assert built == json.loads(CHANGE_READOUT.read_text(encoding="utf-8"))


def test_h2_modelability_after_erysimum_has_only_cluster_gate_left():
    mod = _load(MODEL_SCRIPT, "sch_h2_model_v5")
    built = mod.build(MEASUREMENT, CHANGE_SEED, CASES)

    assert built["plant_performance_layer"] == {
        "n_cases": 37,
        "n_canonical_axes": 11,
        "n_clusters": 6,
        "n_axes_with_two_or_more_cases": 10,
        "axes_with_two_or_more_cases": [
            "Caryopteris_000330_corolla_tube",
            "Erysimum_000008_corolla_diameter",
            "Erysimum_000008_corolla_shape",
            "Erysimum_000008_corolla_tube_length",
            "Erysimum_000008_corolla_tube_width",
            "Gymnadenia_000030_phenology",
            "Gymnadenia_000030_spur_length",
            "Pedicularis_000376_corolla_exsertion",
            "Trifolium_000391_flowering_time",
            "Trifolium_000391_inflorescence_production",
        ],
        "model_ready": False,
    }
    assert built["raw_plant_performance_case_count_gate_pass"] is True
    assert built["plant_performance_axis_gate_pass"] is True
    assert built["plant_performance_repeated_axis_gate_pass"] is True
    assert built["structural_gate_blockers"] == ["independent_clusters_below_gate"]
    assert built == json.loads(MODEL_READOUT.read_text(encoding="utf-8"))

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PED_CASES = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH5_V1.csv"
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V3.csv"
SOURCE_REGISTRY = ROOT / "data" / "SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V2.csv"
CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V3.csv"

MEASUREMENT_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_READOUT_V3.json"
CUMULATIVE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_CUMULATIVE_V4.json"
CHANGE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_READOUT_V3.json"
MODEL_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MODELABILITY_V3.json"

MEASUREMENT_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer_v4.py"
CUMULATIVE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v4.py"
CHANGE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed_v4.py"
MODEL_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v3.py"

EVIDENCE = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH{i}_V1.csv"
    for i in range(1, 6)
]
CASES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH{i}_V1.csv"
    for i in range(1, 6)
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


def test_pedicularis_main_text_pressure_values_are_exactly_materialized():
    rows = {row["population_or_site"]: row for row in _rows(PED_CASES)}
    assert set(rows) == {"population_11", "population_3", "population_12", "population_5"}
    assert float(rows["population_11"]["effect_2"]) == 0.8
    assert float(rows["population_3"]["effect_2"]) == 1.36
    assert float(rows["population_12"]["effect_2"]) == 18.5
    assert float(rows["population_5"]["effect_2"]) == 27.42
    assert all(row["effect_metric"] == "SEED_PREDATION_PERCENT" for row in rows.values())
    assert all(row["conflict_detected"] == "UNRESOLVED" for row in rows.values())
    assert all(row["geometry_eligibility"] == "LOCAL_PRESSURE_ONLY_NOT_GEOMETRY" for row in rows.values())


def test_pedicularis_pressure_cases_preserve_label_linkage_boundary():
    rows = {row["population_or_site"]: row for row in _rows(PED_CASES)}
    assert "INDIVIDUAL_TRAIT_POLLINATION_SEED_LINK_PRESERVED" in rows["population_11"]["notes"]
    assert "INDIVIDUAL_TRAIT_POLLINATION_SEED_LINK_PRESERVED" in rows["population_3"]["notes"]
    assert "INDIVIDUAL_TRAIT_POLLINATION_SEED_LINK_PRESERVED" in rows["population_5"]["notes"]
    assert "LABELS_LOST_PRESSURE_ONLY" in rows["population_12"]["notes"]


def test_measurement_v4_promotes_four_pressure_cases_not_geometry():
    mod = _load(MEASUREMENT_SCRIPT, "sch_h2_measurement_v4")
    built = mod.build(MEASUREMENT, SOURCE_REGISTRY, CASES)
    assert built == json.loads(MEASUREMENT_READOUT.read_text(encoding="utf-8"))
    assert built["n_total_h2_local_cases"] == 22
    assert built["n_plant_performance_measurement_cases"] == 15
    assert built["materialized_plant_performance_layer_counts"] == {
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 9,
        "LOCAL_ANTAGONIST_PRESSURE": 4,
    }
    assert built["n_canonical_axes_with_plant_performance_cases"] == 5
    assert built["n_measurement_records_below_source_supported_layer"] == 2


def test_cumulative_v4_tracks_pressure_as_separate_measurement_class():
    mod = _load(CUMULATIVE_SCRIPT, "sch_h2_cumulative_v4")
    built = mod.build(EVIDENCE, CASES)
    assert built == json.loads(CUMULATIVE_READOUT.read_text(encoding="utf-8"))
    assert built["n_materialized_local_cases"] == 22
    assert built["n_canonical_axes_with_materialized_cases"] == 8
    assert built["n_clusters_with_materialized_cases"] == 6
    assert built["local_measurement_class_counts"] == {
        "LOCAL_ANTAGONIST_PRESSURE": 4,
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 9,
        "ROLE_BEHAVIOR_CONTEXT": 7,
    }
    assert built["n_pedicularis_antagonist_pressure_cases"] == 4


def test_change_seed_v4_promotes_pedicularis_weight_shift_with_pressure_cases():
    mod = _load(CHANGE_SCRIPT, "sch_h2_change_v4")
    built = mod.build(CHANGE_SEED)
    assert built == json.loads(CHANGE_READOUT.read_text(encoding="utf-8"))
    assert built["n_materialized_local_cases_represented"] == 22
    assert built["n_change_records_with_materialized_local_cases"] == 8
    assert built["n_change_records_with_two_or_more_materialized_cases"] == 7
    assert built["n_change_records_without_materialized_local_cases"] == 1


def test_h2_modelability_case_count_passes_but_structural_gates_still_fail():
    mod = _load(MODEL_SCRIPT, "sch_h2_model_v3")
    built = mod.build(MEASUREMENT, CHANGE_SEED, CASES)
    assert built == json.loads(MODEL_READOUT.read_text(encoding="utf-8"))
    assert built["raw_plant_performance_case_count_gate_pass"] is True
    assert built["plant_performance_layer"] == {
        "n_cases": 15,
        "n_canonical_axes": 5,
        "n_clusters": 4,
        "n_axes_with_two_or_more_cases": 4,
        "axes_with_two_or_more_cases": [
            "Caryopteris_000330_corolla_tube",
            "Gymnadenia_000030_phenology",
            "Gymnadenia_000030_spur_length",
            "Pedicularis_000376_corolla_exsertion",
        ],
        "model_ready": False,
    }
    assert built["structural_gate_blockers"] == [
        "canonical_axes_below_gate",
        "independent_clusters_below_gate",
        "repeated_axes_below_gate",
    ]
    assert built["plant_performance_model_ready"] is False

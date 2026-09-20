import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH4_V1.csv"
CASES4 = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH4_V1.csv"
CONTRASTS = ROOT / "data" / "SCH_MACROECOLOGY_GYMNADENIA_A2_MEDIATED_CONTRASTS_V1.csv"
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V2.csv"
SOURCE_REGISTRY = ROOT / "data" / "SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V2.csv"
MEASUREMENT_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_READOUT_V2.json"
MEASUREMENT_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer_v3.py"
CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V2.csv"
CHANGE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_READOUT_V2.json"
CHANGE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed_v3.py"
CUM_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_CUMULATIVE_V3.json"
CUM_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v3.py"
MODEL_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MODELABILITY_V2.json"
MODEL_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v2.py"

EVIDENCE_BATCHES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH{i}_V1.csv"
    for i in range(1, 5)
]
CASE_BATCHES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH{i}_V1.csv"
    for i in range(1, 5)
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


def test_gymnadenia_a2_materializes_eight_net_selection_cells():
    rows = _rows(CASES4)
    assert len(rows) == 8
    assert {row["canonical_trait_axis_id"] for row in rows} == {
        "Gymnadenia_000030_phenology",
        "Gymnadenia_000030_spur_length",
    }
    phen = {
        row["treatment_or_consumer_regime"]: (float(row["effect_1"]), float(row["effect_1_se"]))
        for row in rows
        if row["canonical_trait_axis_id"] == "Gymnadenia_000030_phenology"
    }
    assert phen == {
        "OPEN_POLLINATED_NATURAL_HERBIVORY": (-0.0042, 0.054),
        "OPEN_POLLINATED_HERBIVORES_EXCLUDED": (0.094, 0.031),
        "HAND_POLLINATED_NATURAL_HERBIVORY": (-0.16, 0.056),
        "HAND_POLLINATED_HERBIVORES_EXCLUDED": (-0.066, 0.028),
    }
    spur = {
        row["treatment_or_consumer_regime"]: (float(row["effect_1"]), float(row["effect_1_se"]))
        for row in rows
        if row["canonical_trait_axis_id"] == "Gymnadenia_000030_spur_length"
    }
    assert spur == {
        "OPEN_POLLINATED_NATURAL_HERBIVORY": (0.18, 0.057),
        "OPEN_POLLINATED_HERBIVORES_EXCLUDED": (0.077, 0.035),
        "HAND_POLLINATED_NATURAL_HERBIVORY": (0.083, 0.053),
        "HAND_POLLINATED_HERBIVORES_EXCLUDED": (-0.042, 0.029),
    }
    assert all(row["conflict_detected"] == "UNRESOLVED" for row in rows)
    assert all(row["alignment_detected"] == "UNRESOLVED" for row in rows)


def test_gymnadenia_mediated_contrasts_are_point_estimates_only():
    rows = _rows(CONTRASTS)
    assert len(rows) == 8
    values = {row["contrast_id"]: float(row["delta_beta"]) for row in rows}
    assert values["Gymnadenia_phenology_poll_H"] == 0.16
    assert values["Gymnadenia_phenology_poll_E"] == 0.16
    assert values["Gymnadenia_phenology_herb_C"] == -0.098
    assert values["Gymnadenia_phenology_herb_HP"] == -0.094
    assert values["Gymnadenia_spur_poll_H"] == 0.10
    assert values["Gymnadenia_spur_poll_E"] == 0.12
    assert values["Gymnadenia_spur_herb_C"] == 0.10
    assert values["Gymnadenia_spur_herb_HP"] == 0.13
    assert {row["contrast_uncertainty_status"] for row in rows} == {
        "SE_OR_COVARIANCE_NOT_REPORTED_IN_A2"
    }
    assert {row["claim_ceiling"] for row in rows} == {
        "POINT_ESTIMATE_DIRECTION_ONLY"
    }


def test_gymnadenia_source_object_is_exactly_extracted_without_binary_claim():
    rows = _rows(SOURCE_REGISTRY)
    gym = next(row for row in rows if row["source_object_id"] == "Gymnadenia_A2")
    assert gym["route_status"] == "TABLE_VALUES_SOURCE_INSPECTED"
    assert gym["binary_materialized"] == "NO"
    assert gym["exact_local_values_extracted"] == "YES"


def test_h2_cumulative_v3_reproduces_18_local_cases():
    mod = _load(CUM_SCRIPT, "sch_h2_cumulative_v3")
    built = mod.build(EVIDENCE_BATCHES, CASE_BATCHES)
    assert built == json.loads(CUM_READOUT.read_text(encoding="utf-8"))
    assert built["n_materialized_local_cases"] == 18
    assert built["n_canonical_axes_with_materialized_cases"] == 7
    assert built["n_clusters_with_materialized_cases"] == 5
    assert built["local_geometry_counts"]["UNRESOLVED"] == 8


def test_measurement_v3_promotes_gymnadenia_net_selection_only():
    mod = _load(MEASUREMENT_SCRIPT, "sch_h2_measurement_v3")
    built = mod.build(MEASUREMENT, SOURCE_REGISTRY, CASE_BATCHES)
    assert built == json.loads(MEASUREMENT_READOUT.read_text(encoding="utf-8"))
    assert built["n_total_h2_local_cases"] == 18
    assert built["n_plant_performance_measurement_cases"] == 11
    assert built["materialized_plant_performance_layer_counts"] == {
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 9,
        "LOCAL_ANTAGONIST_PRESSURE": 0,
    }
    assert built["n_source_objects_exact_local_values_extracted"] == 1


def test_change_seed_v3_adds_net_selection_context_shift():
    mod = _load(CHANGE_SCRIPT, "sch_h2_change_v3")
    built = mod.build(CHANGE_SEED)
    assert built == json.loads(CHANGE_READOUT.read_text(encoding="utf-8"))
    assert built["change_type_counts"]["NET_SELECTION_CONTEXT_SHIFT"] == 2
    assert built["n_materialized_local_cases_represented"] == 18


def test_h2_modelability_v2_still_fails_closed_after_gymnadenia():
    mod = _load(MODEL_SCRIPT, "sch_h2_model_v2")
    built = mod.build(MEASUREMENT, CHANGE_SEED, CASE_BATCHES)
    assert built == json.loads(MODEL_READOUT.read_text(encoding="utf-8"))
    assert built["plant_performance_layer"] == {
        "n_cases": 11,
        "n_canonical_axes": 4,
        "n_clusters": 3,
        "n_axes_with_two_or_more_cases": 3,
        "axes_with_two_or_more_cases": [
            "Caryopteris_000330_corolla_tube",
            "Gymnadenia_000030_phenology",
            "Gymnadenia_000030_spur_length",
        ],
        "model_ready": False,
    }
    assert built["primary_h2_status"] == "DESCRIPTIVE_WITHIN_SOURCE_CONTRASTS_ONLY"

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GRADIENTS = ROOT / "data" / "SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv"
CONTRASTS = ROOT / "data" / "SCH_H2_GYMNADENIA_A2_AGENT_CONTRASTS_V1.csv"
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V2.csv"
SOURCE_REGISTRY = ROOT / "data" / "SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V2.csv"
MEASUREMENT_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_READOUT_V2.json"
MEASUREMENT_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer_v3.py"
CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V2.csv"
CHANGE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_READOUT_V2.json"
CHANGE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed_v3.py"
CUMULATIVE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_CUMULATIVE_V3.json"
CUMULATIVE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v3.py"
MODELABILITY_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MODELABILITY_V2.json"
MODELABILITY_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v2.py"

EVIDENCE = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH{i}_V1.csv"
    for i in range(1, 5)
]
CASES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH{i}_V1.csv"
    for i in range(1, 5)
]


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _csv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_gymnadenia_a2_exact_treatment_gradients_are_frozen():
    rows = _csv(GRADIENTS)
    assert len(rows) == 20
    lookup = {(r["trait"], r["treatment"]): r for r in rows}

    assert float(lookup[("flowering_start", "C+H")]["beta"]) == -0.0042
    assert float(lookup[("flowering_start", "C+E")]["beta"]) == 0.094
    assert float(lookup[("flowering_start", "HP+H")]["beta"]) == -0.16
    assert float(lookup[("flowering_start", "HP+E")]["beta"]) == -0.066

    assert float(lookup[("spur_length", "C+H")]["beta"]) == 0.18
    assert float(lookup[("spur_length", "C+E")]["beta"]) == 0.077
    assert float(lookup[("spur_length", "HP+H")]["beta"]) == 0.083
    assert float(lookup[("spur_length", "HP+E")]["beta"]) == -0.042

    assert float(lookup[("flowering_start", "C+E")]["se"]) == 0.031
    assert float(lookup[("spur_length", "C+H")]["se"]) == 0.057


def test_gymnadenia_a2_agent_contrasts_preserve_direction_without_uncertainty():
    rows = {r["trait"]: r for r in _csv(CONTRASTS)}
    phen = rows["flowering_start"]
    spur = rows["spur_length"]

    assert float(phen["delta_beta_poll_H"]) == 0.16
    assert float(phen["delta_beta_poll_E"]) == 0.16
    assert float(phen["delta_beta_herb_C"]) == -0.098
    assert float(phen["delta_beta_herb_HP"]) == -0.094
    assert phen["geometry_interpretation"] == "OPPOSING_DIRECTIONAL_COMPONENTS"

    assert float(spur["delta_beta_poll_H"]) == 0.10
    assert float(spur["delta_beta_poll_E"]) == 0.12
    assert float(spur["delta_beta_herb_C"]) == 0.10
    assert float(spur["delta_beta_herb_HP"]) == 0.13
    assert spur["geometry_interpretation"] == "REINFORCING_DIRECTIONAL_COMPONENTS"

    assert phen["contrast_se_reported"] == "NO"
    assert spur["contrast_se_reported"] == "NO"


def test_measurement_layer_promotes_eight_gymnadenia_net_selection_cases():
    mod = _load(MEASUREMENT_SCRIPT, "sch_h2_measurement_v3")
    built = mod.build(MEASUREMENT, SOURCE_REGISTRY, CASES)

    assert built["n_total_h2_local_cases"] == 18
    assert built["n_plant_performance_measurement_cases"] == 11
    assert built["n_role_behavior_cases_separate"] == 7
    assert built["materialized_plant_performance_layer_counts"] == {
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 9,
        "LOCAL_ANTAGONIST_PRESSURE": 0,
    }
    assert built["gymnadenia_local_net_selection_cases_materialized"] == 8
    assert built["n_source_objects_exact_local_values_extracted"] == 1
    assert built == json.loads(MEASUREMENT_READOUT.read_text(encoding="utf-8"))


def test_cumulative_h2_counts_gymnadenia_as_local_net_selection_not_geometry():
    mod = _load(CUMULATIVE_SCRIPT, "sch_h2_cumulative_v3")
    built = mod.build(EVIDENCE, CASES)

    assert built["n_materialized_local_cases"] == 18
    assert built["n_canonical_axes_with_materialized_cases"] == 7
    assert built["n_clusters_with_materialized_cases"] == 5
    assert built["local_context_class_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONSUMER_REMOVED_NO_STATIC_GEOMETRY": 1,
        "LOCAL_NET_SELECTION": 8,
        "ROLE_BEHAVIOR_CONTEXT": 7,
    }
    assert built["n_gymnadenia_local_net_selection_cases"] == 8
    assert built == json.loads(CUMULATIVE_READOUT.read_text(encoding="utf-8"))


def test_change_seed_adds_two_net_selection_regime_shifts():
    mod = _load(CHANGE_SCRIPT, "sch_h2_change_v3")
    built = mod.build(CHANGE_SEED)

    assert built["n_change_records"] == 9
    assert built["n_materialized_local_cases_represented"] == 18
    assert built["change_type_counts"]["NET_SELECTION_SHIFT_ACROSS_CONSUMER_REGIME"] == 2
    assert built["n_change_records_with_two_or_more_materialized_cases"] == 6
    assert built == json.loads(CHANGE_READOUT.read_text(encoding="utf-8"))


def test_h2_modelability_improves_but_remains_fail_closed():
    mod = _load(MODELABILITY_SCRIPT, "sch_h2_modelability_v2")
    built = mod.build(MEASUREMENT, CHANGE_SEED, CASES)

    assert built["n_total_local_cases"] == 18
    assert built["n_total_canonical_axes_with_cases"] == 7
    assert built["n_total_clusters_with_cases"] == 5
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
    assert built["plant_performance_model_ready"] is False
    assert built["role_behavior_model_ready"] is False
    assert built["status"] == "H2_MODELABILITY_GATE_V2_GYMNADENIA_ADDED_FAIL_CLOSED"
    assert built == json.loads(MODELABILITY_READOUT.read_text(encoding="utf-8"))

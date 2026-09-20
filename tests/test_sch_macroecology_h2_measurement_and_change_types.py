import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V1.csv"
SOURCE_REGISTRY = ROOT / "data" / "SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V1.csv"
MEASUREMENT_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_READOUT_V1.json"
MEASUREMENT_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer.py"
CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V1.csv"
CHANGE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_READOUT_V1.json"
CHANGE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed.py"
CASES = [
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH2_V1.csv",
]


def _measurement():
    spec = importlib.util.spec_from_file_location("sch_h2_measurement", MEASUREMENT_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(MEASUREMENT, SOURCE_REGISTRY, CASES)


def _change():
    spec = importlib.util.spec_from_file_location("sch_h2_change", CHANGE_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(CHANGE_SEED)


def test_h2_measurement_layer_is_fail_closed():
    built = _measurement()
    assert built["n_measurement_records"] == 8
    assert built["n_canonical_axes"] == 6
    assert built["n_materialized_model_cases"] == 3
    assert built["source_supported_layer_counts"] == {
        "LOCAL_ANTAGONIST_PRESSURE": 1,
        "LOCAL_GEOMETRY": 3,
        "LOCAL_NET_SELECTION": 4,
    }
    assert built["materialized_layer_counts"] == {
        "CONTEXT_STRUCTURE_ONLY": 5,
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 1,
    }
    assert built["n_measurement_records_below_source_supported_layer"] == 5
    assert built["h2_model_ready"] is False


def test_pedicularis_measurement_layer_preserves_linkage_boundary():
    built = _measurement()
    assert built["pedicularis_context_structure"] == {
        "pollination_contexts_reported": 14,
        "seed_outcome_contexts_reported": 12,
        "individual_linked_contexts": 7,
        "population_specific_geometry_cases_materialized": 0,
    }
    assert "local_antagonist_pressure_is_not_local_two_function_geometry" in built["claim_ceiling"]


def test_pending_source_objects_do_not_create_model_cases():
    built = _measurement()
    assert built["n_source_objects"] == 6
    assert built["n_source_objects_binary_materialized"] == 0
    assert built["n_source_objects_exact_local_values_extracted"] == 0
    assert built["n_materialized_model_cases"] == 3


def test_h2_measurement_readout_is_reproducible():
    assert _measurement() == json.loads(MEASUREMENT_READOUT.read_text(encoding="utf-8"))


def test_h2_change_types_remain_mechanistically_distinct():
    built = _change()
    assert built["n_change_records"] == 4
    assert built["change_type_counts"] == {
        "COMPONENT_WEIGHT_SHIFT": 1,
        "COMPONENT_WEIGHT_SHIFT_WITH_EVOLUTIONARY_RESPONSE": 1,
        "GEOMETRY_CLASS_SWITCH": 1,
        "GEOMETRY_DISAPPEARANCE": 1,
    }
    assert built["n_materialized_local_cases_represented"] == 3
    assert built["n_change_records_without_materialized_local_cases"] == 2
    assert "geometry_class_switch_is_not_equivalent_to_component_weight_shift" in built["claim_ceiling"]


def test_h2_change_type_readout_is_reproducible():
    assert _change() == json.loads(CHANGE_READOUT.read_text(encoding="utf-8"))

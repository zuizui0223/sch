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
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH3_V1.csv",
]


def _measurement():
    spec = importlib.util.spec_from_file_location("sch_h2_measurement_v2", MEASUREMENT_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(MEASUREMENT, SOURCE_REGISTRY, CASES)


def _change():
    spec = importlib.util.spec_from_file_location("sch_h2_change_v2", CHANGE_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(CHANGE_SEED)


def test_h2_measurement_layer_reconciles_all_local_cases_without_collapsing_layers():
    built = _measurement()
    assert built["n_total_h2_local_cases"] == 10
    assert built["n_plant_performance_measurement_cases"] == 3
    assert built["n_role_behavior_cases_separate"] == 7
    assert built["n_canonical_axes_with_plant_performance_cases"] == 2
    assert built["n_canonical_axes_with_role_behavior_cases"] == 3
    assert built["status"] == "H2_MEASUREMENT_LAYER_V2_RECONCILED_ROLE_BEHAVIOR_SEPARATE"


def test_h2_measurement_layer_preserves_source_support_vs_materialization():
    built = _measurement()
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
    assert built["materialized_plant_performance_layer_counts"] == {
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 1,
        "LOCAL_ANTAGONIST_PRESSURE": 0,
    }


def test_role_behavior_cases_are_explicitly_separate_from_plant_performance_measurement():
    built = _measurement()
    assert built["role_behavior_case_ids"] == [
        "Blueberry_corolla_access_Bluecrop",
        "Blueberry_corolla_access_Duke",
        "Sesame_corolla_normal",
        "Sesame_corolla_short_no_landing",
        "Sesame_corolla_short_with_landing",
        "Sesame_nectar_high_nectar_high_pollen",
        "Sesame_nectar_low_resource_control",
    ]
    assert "plant_performance_cases_and_role_behavior_cases_are_separate_H2_layers" in built["claim_ceiling"]


def test_pedicularis_linkage_boundary_remains_fail_closed():
    built = _measurement()
    assert built["pedicularis_context_structure"] == {
        "pollination_contexts_reported": 14,
        "seed_outcome_contexts_reported": 12,
        "individual_linked_contexts": 7,
        "population_specific_geometry_cases_materialized": 0,
    }


def test_pending_source_objects_do_not_create_pseudo_cases():
    built = _measurement()
    assert built["n_source_objects"] == 6
    assert built["n_source_objects_binary_materialized"] == 0
    assert built["n_source_objects_exact_local_values_extracted"] == 0
    assert built["h2_model_ready"] is False


def test_measurement_readout_is_reproducible():
    assert _measurement() == json.loads(MEASUREMENT_READOUT.read_text(encoding="utf-8"))


def test_h2_change_seed_accounts_for_all_materialized_local_cases():
    built = _change()
    assert built["n_change_records"] == 7
    assert built["n_canonical_axes"] == 7
    assert built["n_materialized_local_cases_represented"] == 10
    assert built["n_change_records_with_materialized_local_cases"] == 5
    assert built["n_change_records_without_materialized_local_cases"] == 2


def test_h2_change_types_remain_mechanistically_distinct():
    built = _change()
    assert built["change_type_counts"] == {
        "COMPONENT_WEIGHT_SHIFT": 1,
        "COMPONENT_WEIGHT_SHIFT_WITH_EVOLUTIONARY_RESPONSE": 1,
        "CONSUMER_ROLE_BEHAVIOR_SHIFT": 3,
        "GEOMETRY_CLASS_SWITCH": 1,
        "GEOMETRY_DISAPPEARANCE": 1,
    }
    assert "consumer_role_behavior_shift_is_not_plant_fitness_geometry" in built["claim_ceiling"]


def test_change_type_readout_is_reproducible():
    assert _change() == json.loads(CHANGE_READOUT.read_text(encoding="utf-8"))

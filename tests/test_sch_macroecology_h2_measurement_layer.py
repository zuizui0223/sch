import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V1.csv"
SOURCE_REGISTRY = ROOT / "data" / "SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V1.csv"
CASES = [
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH2_V1.csv",
]
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_measurement_layer", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(MEASUREMENT, SOURCE_REGISTRY, CASES)


def test_h2_measurement_layer_separates_source_support_from_materialization():
    built = _build()
    assert built["n_measurement_records"] == 8
    assert built["n_canonical_axes"] == 6
    assert built["n_source_records"] == 6
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


def test_h2_measurement_layer_counts_only_actual_case_rows_as_model_n():
    built = _build()
    assert built["n_materialized_model_cases"] == 3
    assert built["materialized_case_ids"] == [
        "Caryopteris_corolla_tube_robbers_excluded",
        "Caryopteris_corolla_tube_robbers_present",
        "Gentiana_lutea_color_Torrestio",
    ]
    assert built["materialized_case_layer_counts"] == {
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 1,
        "LOCAL_ANTAGONIST_PRESSURE": 0,
    }


def test_h2_measurement_layer_preserves_pedicularis_linkage_boundary():
    built = _build()
    assert built["pedicularis_context_structure"] == {
        "pollination_contexts_reported": 14,
        "seed_outcome_contexts_reported": 12,
        "individual_linked_contexts": 7,
        "population_specific_geometry_cases_materialized": 0,
    }
    assert "local_antagonist_pressure_is_not_local_two_function_geometry" in built["claim_ceiling"]


def test_h2_source_objects_are_registered_but_not_pretended_extracted():
    built = _build()
    assert built["n_source_objects"] == 6
    assert built["n_source_objects_binary_materialized"] == 0
    assert built["n_source_objects_exact_local_values_extracted"] == 0
    assert built["source_object_route_status_counts"] == {
        "INDEX_RESOLVED_BINARY_CONTENT_PENDING": 1,
        "OBJECT_FILENAME_RESOLVED_BINARY_BLOCKED": 2,
        "PROGRAMME_OBJECTS_NOT_YET_FROZEN": 1,
        "ROUTE_RESOLVED_BINARY_BLOCKED": 2,
    }


def test_h2_measurement_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

POL = ROOT / "data" / "SCH_H2_POLYGALA_TABLE5_EXACT_V1.csv"
TAN = ROOT / "data" / "SCH_H2_TANACETUM_GERMINATION_TESTS_V1.csv"

MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V6.csv"
SOURCE_REGISTRY = ROOT / "data" / "SCH_H2_LOCAL_CONTEXT_SOURCE_OBJECTS_V2.csv"
CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V6.csv"

CUMULATIVE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_CUMULATIVE_V7.json"
MEASUREMENT_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_READOUT_V6.json"
CHANGE_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_READOUT_V6.json"
MODELABILITY_READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MODELABILITY_V6.json"

CUMULATIVE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v7.py"
MEASUREMENT_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer_v7.py"
CHANGE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed_v7.py"
MODELABILITY_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v6.py"

EVIDENCE = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH{i}_V1.csv"
    for i in range(1, 10)
]
CASES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH{i}_V1.csv"
    for i in range(1, 10)
]


def _mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_polygala_exact_population_coefficients_are_frozen():
    rows = {r["population"]: r for r in _rows(POL)}
    assert set(rows) == {"Montmajor", "Serrat_dels_Boixos", "Colldecarrera"}
    assert float(rows["Montmajor"]["nectar_gland_standardized_b"]) == 0.311
    assert float(rows["Serrat_dels_Boixos"]["nectar_gland_standardized_b"]) == 0.169
    assert float(rows["Colldecarrera"]["nectar_gland_standardized_b"]) == 0.255
    assert float(rows["Montmajor"]["p"]) == 0.001
    assert float(rows["Colldecarrera"]["p"]) == 0.011


def test_tanacetum_germination_proxy_tests_are_frozen():
    rows = {r["test"]: r for r in _rows(TAN)}
    assert (float(rows["germination_rate_by_chemotype"]["chisq"]), int(rows["germination_rate_by_chemotype"]["df"]), float(rows["germination_rate_by_chemotype"]["p"])) == (10.44, 4, 0.034)
    assert (float(rows["germination_rate_by_plot_type"]["chisq"]), int(rows["germination_rate_by_plot_type"]["df"]), float(rows["germination_rate_by_plot_type"]["p"])) == (0.61, 1, 0.434)
    assert float(rows["germination_rate_vs_pollinator_visits"]["p"]) == 0.025
    assert float(rows["germination_rate_vs_florivore_visits"]["p"]) == 0.356


def test_h2_cumulative_breadth_reaches_49_cases_without_collapsing_measurement_classes():
    built = _mod(CUMULATIVE_SCRIPT, "sch_h2_cumulative_v7").build(EVIDENCE, CASES)
    frozen = json.loads(CUMULATIVE_READOUT.read_text(encoding="utf-8"))

    assert built["n_materialized_local_cases"] == 49
    assert built["n_canonical_axes_with_materialized_cases"] == 17
    assert built["n_clusters_with_materialized_cases"] == 10
    assert built["local_measurement_class_counts"] == {
        "LOCAL_ANTAGONIST_PRESSURE": 4,
        "LOCAL_GEOMETRY": 2,
        "LOCAL_NET_SELECTION": 31,
        "LOCAL_REPRODUCTIVE_COMPONENT_EFFECT": 3,
        "LOCAL_REPRODUCTIVE_PERFORMANCE_PROXY": 2,
        "ROLE_BEHAVIOR_CONTEXT": 7,
    }
    for key in (
        "n_materialized_local_cases",
        "n_canonical_axes_with_materialized_cases",
        "n_clusters_with_materialized_cases",
        "local_measurement_class_counts",
        "n_polygala_reproductive_component_cases",
        "n_tanacetum_reproductive_performance_proxy_cases",
    ):
        assert built[key] == frozen[key]


def test_estimand_family_registry_prevents_numeric_pooling_by_breadth():
    built = _mod(MEASUREMENT_SCRIPT, "sch_h2_measurement_v7").build(
        MEASUREMENT, SOURCE_REGISTRY, CASES
    )
    frozen = json.loads(MEASUREMENT_READOUT.read_text(encoding="utf-8"))

    assert built["n_total_h2_local_cases"] == 49
    assert built["n_plant_performance_measurement_cases"] == 42
    assert built["n_canonical_axes_with_plant_performance_cases"] == 14
    assert built["estimand_family_materialized_counts"]["TOTAL_SELECTION_EFFECT"] == {
        "n_cases": 30,
        "n_axes": 8,
        "n_clusters": 3,
        "n_measurement_records": 8,
    }
    assert built["estimand_family_materialized_counts"]["REPRODUCTIVE_COMPONENT_EFFECT"]["n_clusters"] == 1
    assert built["estimand_family_materialized_counts"]["REPRODUCTIVE_PERFORMANCE_PROXY"]["n_clusters"] == 1
    assert built["numeric_pooling_family_materialized_counts"]["STANDARDIZED_SELECTION_GRADIENT"]["n_clusters"] == 2
    assert built["numeric_pooling_family_materialized_counts"]["TOTAL_SELECTION_PATH_COEFFICIENT"]["n_clusters"] == 1

    for key in (
        "n_total_h2_local_cases",
        "n_plant_performance_measurement_cases",
        "n_canonical_axes_with_plant_performance_cases",
        "estimand_family_materialized_counts",
        "numeric_pooling_family_materialized_counts",
    ):
        assert built[key] == frozen[key]


def test_breadth_gate_passes_but_commensurate_estimand_gate_fails():
    built = _mod(MODELABILITY_SCRIPT, "sch_h2_modelability_v6").build(
        MEASUREMENT, CHANGE_SEED, CASES
    )
    frozen = json.loads(MODELABILITY_READOUT.read_text(encoding="utf-8"))

    assert built["broad_plant_performance_structural_gate_pass"] is True
    assert built["plant_performance_layer"]["n_cases"] == 42
    assert built["plant_performance_layer"]["n_canonical_axes"] == 14
    assert built["plant_performance_layer"]["n_clusters"] == 8
    assert built["plant_performance_layer"]["n_axes_with_two_or_more_cases"] == 11

    assert built["commensurate_estimand_family_model_ready"] is False
    assert built["commensurate_numeric_pooling_model_ready"] is False
    assert built["plant_performance_model_ready"] is False
    assert built["primary_h2_status"] == "BREADTH_GATE_PASS_ESTIMAND_HARMONIZATION_FAIL"
    assert built["status"] == "H2_BREADTH_GATE_PASS_ESTIMAND_FAMILY_FAIL_CLOSED"
    assert built["estimand_family_modelability"]["TOTAL_SELECTION_EFFECT"]["n_clusters"] == 3

    for key in (
        "broad_plant_performance_structural_gate_pass",
        "commensurate_estimand_family_model_ready",
        "commensurate_numeric_pooling_model_ready",
        "primary_h2_status",
        "status",
        "estimand_gate_blockers",
    ):
        assert built[key] == frozen[key]


def test_polygala_change_seed_is_context_shift_not_final_fitness_shift():
    built = _mod(CHANGE_SCRIPT, "sch_h2_change_v7").build(CHANGE_SEED)
    frozen = json.loads(CHANGE_READOUT.read_text(encoding="utf-8"))

    assert built["n_change_records"] == 16
    assert built["change_type_counts"]["REPRODUCTIVE_COMPONENT_CONTEXT_SHIFT"] == 1
    assert built["n_materialized_local_cases_represented"] == 47
    assert built["n_change_records_without_materialized_local_cases"] == 1
    assert "tanacetum_single_performance_snapshots_are_not_change_records" in built["claim_ceiling"]

    for key in (
        "n_change_records",
        "n_canonical_axes",
        "change_type_counts",
        "n_materialized_local_cases_represented",
        "n_change_records_without_materialized_local_cases",
    ):
        assert built[key] == frozen[key]

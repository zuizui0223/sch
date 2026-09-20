import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OBJECTS = ROOT / "data" / "SCH_H2_PRIMULA_SOURCE_OBJECTS_V1.csv"
SUMMARY = ROOT / "data" / "SCH_H2_PRIMULA_MAIN_TEXT_SUMMARY_V1.csv"
READOUT = ROOT / "data" / "SCH_H2_PRIMULA_SOURCE_DECOMPOSITION_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_h2_primula_source_decomposition.py"


def _load():
    spec = importlib.util.spec_from_file_location("sch_primula_source_decomp", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_primula_programme_is_decomposed_without_pseudo_cases():
    built = _load().build(OBJECTS, SUMMARY)
    assert built["n_source_objects"] == 5
    assert built["n_model_cases_materialized"] == 0
    assert built["exact_local_value_status_counts"] == {"NO": 5}
    assert built["status"] == "PRIMULA_PROGRAMME_DECOMPOSED_LOCAL_VALUES_PENDING"


def test_primula_source_objects_separate_selection_and_evolutionary_layers():
    built = _load().build(OBJECTS, SUMMARY)
    assert built["source_supported_layer_counts"] == {
        "CONTEXT_STRUCTURE_ONLY": 1,
        "LOCAL_EVOLUTIONARY_RESPONSE": 1,
        "LOCAL_NET_SELECTION": 3,
    }
    assert built["main_text_exact_checks"] == {
        "survey_populations_2001": 69,
        "selection_population_years_2000": 37,
        "selection_population_years_2001": 46,
        "five_population_year_contexts": 25,
        "factorial_population_treatment_contexts": 16,
        "evolution_population_treatment_time_states": 36,
        "grazer_exclosure_populations": 9,
    }


def test_primula_main_text_programme_metrics_are_frozen():
    rows = {row["metric_id"]: row for row in _rows(SUMMARY)}

    assert float(rows["grazing_long_2000"]["value"]) == 0.209
    assert float(rows["grazing_long_2000"]["value_2"]) == 0.039
    assert int(rows["grazing_long_2000"]["n"]) == 37

    assert float(rows["grazing_long_2001"]["value"]) == 0.182
    assert float(rows["grazing_long_2001"]["value_2"]) == 0.039
    assert int(rows["grazing_long_2001"]["n"]) == 46

    assert float(rows["fitness_vs_grazing_2000"]["value"]) == 1.193
    assert float(rows["fitness_vs_grazing_2000"]["value_2"]) == 0.17
    assert rows["fitness_vs_grazing_2000"]["p_value"] == "P_EQ_0.007"

    assert float(rows["fitness_vs_grazing_2001"]["value"]) == 2.164
    assert float(rows["fitness_vs_grazing_2001"]["value_2"]) == 0.59
    assert rows["fitness_vs_grazing_2001"]["p_value"] == "P_LT_0.0001"

    assert float(rows["fitness_vs_evolution_5pop"]["value"]) == 0.90
    assert rows["fitness_vs_evolution_5pop"]["p_value"] == "P_EQ_0.037"

    assert (float(rows["exclosure_short_frequency"]["value"]), float(rows["exclosure_short_frequency"]["value_2"])) == (0.48, 0.36)
    assert (float(rows["control_short_frequency"]["value"]), float(rows["control_short_frequency"]["value_2"])) == (0.50, 0.48)


def test_primula_current_macro_denominator_is_not_expanded_by_auxiliary_sources():
    rows = _rows(OBJECTS)
    assert {row["source_id"] for row in rows} == {"SCHPRISMA-000523"}
    assert all(row["study_doi"] == "10.1073/pnas.1301421110" for row in rows)
    assert "auxiliary_older_programme_sources_are_not_added_to_current_macro_denominator" in _load().build(OBJECTS, SUMMARY)["claim_ceiling"]


def test_primula_source_decomposition_readout_is_reproducible():
    assert _load().build(OBJECTS, SUMMARY) == json.loads(READOUT.read_text(encoding="utf-8"))

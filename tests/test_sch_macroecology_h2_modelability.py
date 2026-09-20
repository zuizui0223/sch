import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MEASUREMENT_LAYER_V1.csv"
CHANGE_SEED = ROOT / "data" / "SCH_MACROECOLOGY_H2_CHANGE_TYPE_SEED_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_MODELABILITY_V1.json"
SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability.py"
CASES = [
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH2_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH3_V1.csv",
]


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_modelability", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(MEASUREMENT, CHANGE_SEED, CASES)


def test_h2_modelability_gate_separates_layers():
    built = _build()
    assert built["n_total_local_cases"] == 10
    assert built["n_total_canonical_axes_with_cases"] == 5
    assert built["n_total_clusters_with_cases"] == 4
    assert built["plant_performance_layer"] == {
        "n_cases": 3,
        "n_canonical_axes": 2,
        "n_clusters": 2,
        "n_axes_with_two_or_more_cases": 1,
        "axes_with_two_or_more_cases": ["Caryopteris_000330_corolla_tube"],
        "model_ready": False,
    }
    assert built["role_behavior_layer"]["n_cases"] == 7
    assert built["role_behavior_layer"]["n_canonical_axes"] == 3
    assert built["role_behavior_layer"]["n_clusters"] == 2


def test_h2_modelability_gate_tracks_within_axis_replication():
    built = _build()
    assert built["n_total_axes_with_two_or_more_local_cases"] == 4
    assert built["axes_with_two_or_more_local_cases"] == [
        "Blueberry_000076_corolla_access",
        "Caryopteris_000330_corolla_tube",
        "Sesame_000336_corolla_tube",
        "Sesame_000336_nectar_availability",
    ]
    assert built["n_change_records_with_two_or_more_materialized_cases"] == 4


def test_h2_modelability_gate_fails_closed():
    built = _build()
    assert built["combined_layer_model_permitted"] is False
    assert built["plant_performance_model_ready"] is False
    assert built["role_behavior_model_ready"] is False
    assert built["primary_h2_status"] == "DESCRIPTIVE_WITHIN_SOURCE_CONTRASTS_ONLY"
    assert "plant_performance_and_role_behavior_are_noncommensurate_estimands" == built["combined_layer_model_blocker"]


def test_h2_modelability_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

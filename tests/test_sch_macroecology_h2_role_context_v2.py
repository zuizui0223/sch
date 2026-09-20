import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = [
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH2_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH3_V1.csv",
]
CASES = [
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH2_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH3_V1.csv",
]
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_CUMULATIVE_V2.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v2.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_context_cumulative_v2", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(EVIDENCE, CASES)


def test_h2_role_context_v2_structure():
    built = _build()
    assert built["n_context_evidence_rows"] == 10
    assert built["n_canonical_axes_with_context_evidence"] == 9
    assert built["n_source_records_with_context_evidence"] == 8
    assert built["n_materialized_local_cases"] == 10
    assert built["n_canonical_axes_with_materialized_cases"] == 5
    assert built["n_clusters_with_materialized_cases"] == 4


def test_h2_role_context_v2_keeps_behavior_separate_from_fitness_geometry():
    built = _build()
    assert built["local_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONSUMER_REMOVED_NO_STATIC_GEOMETRY": 1,
        "ROLE_BEHAVIOR_CONTEXT": 7,
    }
    assert built["local_role_status_counts"] == {
        "NET_ANTAGONISTIC": 1,
        "ROLE_DEPENDENT": 9,
    }
    assert built["n_context_shift_from_reference_yes"] == 5


def test_h2_role_context_v2_remains_fail_closed():
    built = _build()
    assert built["n_evidence_rows_without_materialized_cases"] == 5
    assert built["n_evidence_rows_requiring_source_object"] == 5
    assert built["h2_model_ready"] is False
    assert "role_behavior_context_is_not_relabelled_as_plant_fitness_geometry" in built["claim_ceiling"]


def test_h2_role_context_v2_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

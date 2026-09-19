import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = [
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_EVIDENCE_BATCH2_V1.csv",
]
CASES = [
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_BATCH2_V1.csv",
]
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_CASES_CUMULATIVE_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_h2_context_cumulative", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(EVIDENCE, CASES)


def test_h2_cumulative_context_cases_track_only_materialized_local_rows():
    built = _build()
    assert built["n_context_evidence_rows"] == 7
    assert built["n_canonical_axes_with_context_evidence"] == 6
    assert built["n_materialized_local_cases"] == 3
    assert built["n_canonical_axes_with_materialized_cases"] == 2
    assert built["n_clusters_with_materialized_cases"] == 2


def test_h2_cumulative_context_cases_keep_role_and_geometry_boundaries():
    built = _build()
    assert built["local_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONSUMER_REMOVED_NO_STATIC_GEOMETRY": 1,
    }
    assert built["local_role_status_counts"] == {
        "NET_ANTAGONISTIC": 1,
        "ROLE_DEPENDENT": 2,
    }
    assert built["n_context_shift_from_reference_yes"] == 1


def test_h2_cumulative_context_cases_remain_fail_closed():
    built = _build()
    assert built["n_evidence_rows_without_materialized_cases"] == 5
    assert built["n_evidence_rows_requiring_source_object"] == 5
    assert built["h2_model_ready"] is False
    assert "reported_context_counts_are_not_model_cases" in built["claim_ceiling"]


def test_h2_cumulative_context_case_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

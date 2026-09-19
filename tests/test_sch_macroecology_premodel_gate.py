import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_TABLE_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_PREMODEL_GATE_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_premodel_gate.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_premodel_gate", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(TABLE)


def test_h1_multinomial_stays_fail_closed_under_sparse_alignment_support():
    built = _build()
    assert built["h1_static"]["axes"] == 18
    assert built["h1_static"]["clusters"] == 13
    assert built["h1_static"]["geometry_support"] == {
        "ALIGNMENT_REINFORCEMENT": {"axes": 2, "clusters": 2},
        "CONFLICT": {"axes": 8, "clusters": 7},
        "ONE_SIDED_OR_NULL": {"axes": 8, "clusters": 5},
    }
    assert built["h1_static"]["multinomial_status"] == "FAIL_CLOSED_SPARSE_OUTCOME_CLASS"


def test_h2_h3_stay_closed_for_structural_reasons():
    built = _build()
    assert built["h2_context"]["priority_axes"] == 30
    assert built["h2_context"]["priority_clusters"] == 14
    assert built["h2_context"]["model_status"] == "FAIL_CLOSED_CONTEXT_CASE_DECOMPOSITION_REQUIRED"
    assert built["h3_cancellation"]["directional_cancellation_axes"] == 1
    assert built["h3_cancellation"]["model_status"] == "FAIL_CLOSED_NUMERIC_COMPONENT_AND_COVARIANCE_RECOVERY_REQUIRED"


def test_premodel_gate_tracks_remaining_resolution_work():
    built = _build()
    assert built["remaining_structure"] == {
        "unresolved_canonical_axes": 14,
        "unresolved_clusters": 5,
        "role_boundary_axes": 13,
        "role_boundary_clusters": 7,
        "context_variable_axes": 2,
    }
    assert built["status"] == "PREMODEL_GATE_FROZEN_NO_FORCED_MODEL"


def test_premodel_gate_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

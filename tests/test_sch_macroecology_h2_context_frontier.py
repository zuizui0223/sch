import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_TRAIT_AXIS_LEDGER_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H2_CONTEXT_FRONTIER_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_frontier.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_h2_frontier", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(LEDGER)


def test_h2_frontier_has_30_context_axes():
    rows, receipt = _build()
    assert len(rows) == 30
    assert receipt["n_h2_queue_axes"] == 30
    assert receipt["n_h2_queue_clusters"] == 13
    assert receipt["h2_lane_counts"] == {
        "H2A_GEOMETRY_SWITCH_CONFIRMED": 1,
        "H2B_RESOLVED_GEOMETRY_CONTEXT_DEPENDENCE": 8,
        "H2C_CONTEXT_PRESENT_GEOMETRY_UNRESOLVED": 10,
        "H2D_CONSUMER_ROLE_CONTEXT": 11,
    }


def test_h2_frontier_separates_consumer_role_from_fixed_geometry():
    _, receipt = _build()
    assert receipt["antagonist_role_status_counts"] == {
        "BENEFIT_COST_COUPLED": 4,
        "NET_ANTAGONISTIC": 19,
        "ROLE_DEPENDENT": 7,
    }
    assert receipt["n_consumer_role_context_axes"] == 11
    assert receipt["n_geometry_switch_confirmed_axes"] == 1


def test_h2_frontier_is_not_model_ready_before_context_cases():
    _, receipt = _build()
    assert receipt["context_cases_materialized"] == 0
    assert receipt["h2_model_ready"] is False
    assert receipt["status"] == "H2_CONTEXT_FRONTIER_FROZEN_CONTEXT_CASES_PENDING"
    assert "context_shift_flag_is_not_a_context_case" in receipt["claim_ceiling"]


def test_h2_frontier_readout_is_reproducible():
    _, receipt = _build()
    assert receipt == json.loads(READOUT.read_text(encoding="utf-8"))

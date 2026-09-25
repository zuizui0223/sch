import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
FROZEN = PRISMA / "frozen_v2" / "SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv"
MACHINE_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_machine_pretriage.py"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_p1_gate_frontier.py"
BATCH1 = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH1_V1.csv"
BATCH2 = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH2_V1.csv"
P1_REMAINDER = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_P1_REMAINDER_V1.csv"
V26_HOLDOUT = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V26_HOLDOUT_V1.csv"
V28_BATCH_A = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V28_TA1_BATCH_A.csv"
V29_BATCH_B = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V29_TA1_BATCH_B.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_P1_MANUAL_GATE_FRONTIER_V1.json"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_p1_frontier", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(
        FROZEN,
        PRISMA,
        MACHINE_SCRIPT,
        [BATCH1, BATCH2, P1_REMAINDER, V26_HOLDOUT, V28_BATCH_A, V29_BATCH_B],
    )


def test_all_machine_p1_records_are_manually_gated():
    built = _build()
    assert built["n_machine_p1_records"] == 60
    assert built["n_p1_manual_gated"] == 60
    assert built["n_p1_missing_manual_gate"] == 0
    assert built["status"] == "ALL_CURRENT_P1_RECORDS_MANUALLY_GATED"


def test_p1_gate_recovers_bounded_h1_candidate_frontier():
    built = _build()
    assert built["geometry_eligibility_counts"] == {
        "BOUNDARY_BENEFIT_COST_COUPLED": 2,
        "ELIGIBLE_BOUNDED_COORDINATE": 28,
        "ELIGIBLE_SAME_COORDINATE": 11,
        "INELIGIBLE_MULTIVARIATE_UNRESOLVED": 5,
        "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY": 11,
        "UNRESOLVED_SOURCE": 3,
    }
    assert built["n_h1_geometry_candidate_records"] == 39
    assert built["n_h2_context_candidate_records"] == 28


def test_p1_gate_tracks_axis_decomposition_before_outcomes():
    built = _build()
    assert built["n_trait_axis_split_required_records"] == 33
    assert built["n_single_axis_records"] == 18
    assert "trait_axis_decomposition_required_before_ecological_model" in built["claim_ceiling"]


def test_p1_gate_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

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
        [BATCH1, BATCH2, P1_REMAINDER],
    )


def test_all_machine_p1_records_are_manually_gated():
    built = _build()
    assert built["n_machine_p1_records"] == 49
    assert built["n_p1_manual_gated"] == 49
    assert built["n_p1_missing_manual_gate"] == 0
    assert built["status"] == "ALL_CURRENT_P1_RECORDS_MANUALLY_GATED"


def test_p1_gate_recovers_bounded_h1_candidate_frontier():
    built = _build()
    assert built["geometry_eligibility_counts"] == {
        "BOUNDARY_BENEFIT_COST_COUPLED": 1,
        "ELIGIBLE_BOUNDED_COORDINATE": 24,
        "ELIGIBLE_SAME_COORDINATE": 10,
        "INELIGIBLE_MULTIVARIATE_UNRESOLVED": 5,
        "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY": 7,
        "UNRESOLVED_SOURCE": 2,
    }
    assert built["n_h1_geometry_candidate_records"] == 34
    assert built["n_h2_context_candidate_records"] == 22


def test_p1_gate_tracks_axis_decomposition_before_outcomes():
    built = _build()
    assert built["n_trait_axis_split_required_records"] == 27
    assert built["n_single_axis_records"] == 17
    assert "trait_axis_decomposition_required_before_ecological_model" in built["claim_ceiling"]


def test_p1_gate_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

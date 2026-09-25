import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
FROZEN = PRISMA / "frozen_v2" / "SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_MACHINE_PRETRIAGE_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_machine_pretriage.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_machine_pretriage", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(FROZEN, PRISMA)


def test_machine_pretriage_covers_all_current_primary_includes():
    rows, receipt = _build()
    assert len(rows) == 128
    assert receipt["n_current_primary_includes"] == 128
    assert len({row["record_id"] for row in rows}) == 128


def test_machine_pretriage_is_design_only():
    rows, receipt = _build()
    assert all(row["machine_pretriage_status"] == "DESIGN_ONLY_NOT_BIOLOGICAL_ELIGIBILITY" for row in rows)
    assert "does_not_read_selection_form_or_outcome_sign" in receipt["claim_ceiling"]
    assert "does_not_equal_geometry_eligibility" in receipt["claim_ceiling"]


def test_machine_pretriage_reproduces_current_design_funnel():
    _, receipt = _build()
    assert receipt["paired_response_status_counts"] == {
        "P1_BOTH_RESPONSES_COMMON_FITNESS": 57,
        "P2_BOTH_RESPONSES_NO_COMMON_FITNESS": 15,
        "P3_ANTAGONIST_ONLY": 16,
        "P3_POLLINATOR_ONLY": 29,
        "P4_UNSTRUCTURED_OR_NEITHER": 11,
    }
    assert receipt["n_paired_response_records"] == 72
    assert receipt["n_paired_response_with_common_fitness"] == 57
    assert receipt["n_paired_response_without_common_fitness"] == 15
    assert receipt["context_recode_priority_counts"] == {
        "NO_OR_UNRESOLVED": 93,
        "YES": 35,
    }


def test_machine_pretriage_readout_is_reproducible():
    _, receipt = _build()
    frozen = json.loads(READOUT.read_text(encoding="utf-8"))
    for key in (
        "n_current_primary_includes",
        "paired_response_status_counts",
        "n_paired_response_records",
        "n_paired_response_with_common_fitness",
        "n_paired_response_without_common_fitness",
        "context_recode_priority_counts",
        "trait_manipulation_status_counts",
        "evidence_lane_counts",
        "status",
        "claim_ceiling",
    ):
        assert receipt[key] == frozen[key]

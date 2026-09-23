import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
FROZEN = PRISMA / "frozen_v2" / "SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv"
QUEUE = ROOT / "data" / "SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv"
READOUT = ROOT / "data" / "SCH_H2_UNSCREENED_TA_PRIORITY_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_h2_unscreened_ta_priority.py"


def _load():
    spec = importlib.util.spec_from_file_location("sch_h2_unscreened_ta_priority", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _queue_rows():
    with QUEUE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_unscreened_priority_queue_reconstructs_v20_frontier_exactly():
    rows, receipt = _load().build(FROZEN, PRISMA)
    assert len(rows) == 463
    assert receipt["frozen_denominator"] == 868
    assert receipt["n_already_title_abstract_screened"] == 405
    assert receipt["n_unscreened_priority_queue"] == 463
    assert receipt["tier_counts"] == {
        "TA0_EXPLICIT_SELECTION": 32,
        "TA1_FINAL_PERFORMANCE": 25,
        "TA2_REPEATED_CONTEXT": 20,
        "TA3_REMAINDER": 386,
    }
    assert receipt["n_total_selection_priority"] == 57
    assert receipt["n_repeated_context_priority"] == 20


def test_priority_queue_is_review_order_only_and_outcome_blind():
    rows = _queue_rows()
    assert all(row["current_title_abstract_decision"] == "UNSCREENED" for row in rows)
    assert all(row["title_abstract_screening_status"] == "PENDING" for row in rows)
    assert all(row["outcome_blind_priority"] == "YES" for row in rows)
    assert all(row["priority_basis"] == "TITLE_PLUS_FROZEN_QUERY_METADATA_ONLY" for row in rows)
    forbidden = {
        "conflict_detected",
        "alignment_detected",
        "context_shift_detected",
        "statistical_significance",
        "screen_fulltext",
    }
    assert forbidden.isdisjoint(rows[0])


def test_explicit_selection_tier_is_frozen_before_screening():
    rows = _queue_rows()
    top = [row for row in rows if row["priority_tier"] == "TA0_EXPLICIT_SELECTION"]
    assert len(top) == 32
    assert [row["review_order"] for row in top] == [str(i) for i in range(1, 33)]
    assert top[0]["record_id"] == "SCHPRISMA-000428"
    assert top[-1]["record_id"] == "SCHPRISMA-000860"
    assert all(row["estimand_recovery_target"] == "TOTAL_SELECTION_EFFECT_CANDIDATE_UNCONFIRMED" for row in top)


def test_committed_queue_and_readout_match_builder():
    mod = _load()
    rows, receipt = mod.build(FROZEN, PRISMA)
    assert rows == _queue_rows()
    assert receipt == json.loads(READOUT.read_text(encoding="utf-8"))

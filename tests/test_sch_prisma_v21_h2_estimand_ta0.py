import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data" / "SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv"
V21 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V21_H2_ESTIMAND_TA0_TITLE_ABSTRACT.csv"
READOUT = ROOT / "data" / "SCH_PRISMA_V21_H2_ESTIMAND_TA0_READOUT.json"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle)]


def test_v21_screens_exactly_the_frozen_ta0_frontier():
    queue_ids = {
        row["record_id"]
        for row in _rows(QUEUE)
        if row["priority_tier"] == "TA0_EXPLICIT_SELECTION"
    }
    v21_ids = {row["record_id"] for row in _rows(V21)}
    assert len(queue_ids) == 32
    assert v21_ids == queue_ids


def test_v21_title_abstract_decisions_and_reasons_are_frozen():
    rows = _rows(V21)
    decisions = Counter(row["screen_title_abstract"] for row in rows)
    reasons = Counter(
        row["screen_title_abstract_reason"]
        for row in rows
        if row["screen_title_abstract"] == "EXCLUDE"
    )
    assert decisions == {"RETAIN_FULLTEXT": 20, "EXCLUDE": 12}
    assert reasons == {
        "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS": 3,
        "TA_NO_POLLINATOR_COMPONENT": 3,
        "TA_NO_ANTAGONIST_COMPONENT": 5,
        "TA_NOT_FLORAL_SIGNAL": 1,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_H2_ESTIMAND_TA0_V21_2026-09-23"
    }


def test_v21_exclusion_is_design_based_not_result_sign_based():
    rows = _rows(V21)
    allowed = {
        "",
        "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS",
        "TA_NO_POLLINATOR_COMPONENT",
        "TA_NO_ANTAGONIST_COMPONENT",
        "TA_NOT_FLORAL_SIGNAL",
    }
    assert {row["screen_title_abstract_reason"] for row in rows} <= allowed
    forbidden_text = ("positive result", "negative result", "significant conflict", "supports sch")
    notes = " ".join(row["decision_note"].lower() for row in rows)
    assert all(term not in notes for term in forbidden_text)


def test_v21_readout_matches_overlay():
    readout = json.loads(READOUT.read_text(encoding="utf-8"))
    rows = _rows(V21)
    assert readout["n_ta0_records"] == len(rows) == 32
    assert readout["n_retain_fulltext"] == sum(row["screen_title_abstract"] == "RETAIN_FULLTEXT" for row in rows)
    assert readout["n_exclude"] == sum(row["screen_title_abstract"] == "EXCLUDE" for row in rows)
    assert readout["current_prisma_state_after_v21"] == {
        "frozen_denominator": 868,
        "title_abstract_screened": 437,
        "retained_for_fulltext": 297,
        "title_abstract_excluded": 140,
        "title_abstract_unscreened": 431,
        "fulltext_included_primary": 117,
        "fulltext_decision_excluded": 131,
        "fulltext_unscreened": 49,
    }

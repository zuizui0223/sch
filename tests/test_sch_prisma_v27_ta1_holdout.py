import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V27 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V27_TA1_HOLDOUT.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v27_is_exactly_the_frozen_v3_ta1_tier_not_a_cherry_picked_subset():
    v27 = _rows(V27)
    frozen = _rows(V3_SOURCE)
    expected = [
        row["record_id"]
        for row in frozen
        if row["priority_tier"] == "TA1_FINAL_PERFORMANCE"
    ]
    assert len(expected) == 23
    assert [row["record_id"] for row in v27] == expected


def test_v27_ta1_decision_counts_are_frozen():
    rows = _rows(V27)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 21,
        "EXCLUDE": 2,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA1_HOLDOUT_SCREEN_V27_2026-09-25"
    }


def test_v27_exclusions_use_registered_primary_reasons():
    excluded = {
        row["record_id"]: row["screen_title_abstract_reason"]
        for row in _rows(V27)
        if row["screen_title_abstract"] == "EXCLUDE"
    }
    assert excluded == {
        "SCHPRISMA-000800": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000801": "TA_NO_POLLINATOR_COMPONENT",
    }


def test_v27_keeps_relevant_synthesis_and_duplicate_candidate_for_fulltext_adjudication():
    rows = {row["record_id"]: row for row in _rows(V27)}
    assert rows["SCHPRISMA-000780"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "meta-analysis" in rows["SCHPRISMA-000780"]["decision_note"].lower()
    assert rows["SCHPRISMA-000565"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "duplicate-report" in rows["SCHPRISMA-000565"]["decision_note"].lower()

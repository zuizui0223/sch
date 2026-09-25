import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V33 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V33_TA2_HOLDOUT.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v33_is_exactly_the_frozen_v3_ta2_tier_in_review_order():
    v33 = _rows(V33)
    frozen = _rows(V3_SOURCE)
    expected = [
        row["record_id"]
        for row in frozen
        if row["priority_tier"] == "TA2_REPEATED_CONTEXT"
    ]
    assert len(expected) == 20
    assert [row["record_id"] for row in v33] == expected


def test_v33_decision_counts_and_source_are_frozen():
    rows = _rows(V33)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 14,
        "EXCLUDE": 6,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA2_HOLDOUT_SCREEN_V33_2026-09-25"
    }


def test_v33_exclusion_reasons_follow_registered_ta_boundaries():
    excluded = {
        row["record_id"]: row["screen_title_abstract_reason"]
        for row in _rows(V33)
        if row["screen_title_abstract"] == "EXCLUDE"
    }
    assert excluded == {
        "SCHPRISMA-000455": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000461": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000524": "TA_NO_POLLINATOR_COMPONENT",
        "SCHPRISMA-000681": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000718": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000822": "TA_NO_ANTAGONIST_COMPONENT",
    }


def test_v33_retains_role_coupled_and_relevant_synthesis_records_for_fulltext():
    rows = {row["record_id"]: row for row in _rows(V33)}
    for rid in (
        "SCHPRISMA-000621",
        "SCHPRISMA-000622",
        "SCHPRISMA-000721",
        "SCHPRISMA-000733",
        "SCHPRISMA-000830",
        "SCHPRISMA-000863",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"

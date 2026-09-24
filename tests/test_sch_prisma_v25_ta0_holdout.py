import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V25 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V25_TA0_HOLDOUT.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"
V20_QUEUE = ROOT / "data" / "SCH_H2_UNSCREENED_TA_PRIORITY_QUEUE_V1.csv"

PRE_V25_TA0 = {
    "SCHPRISMA-000648",
    "SCHPRISMA-000659",
    "SCHPRISMA-000775",
    "SCHPRISMA-000812",
}


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v25_closes_exactly_the_still_unscreened_members_of_the_frozen_ta0_tier():
    v25 = _rows(V25)
    old = _rows(V20_QUEUE)
    ta0 = {row["record_id"] for row in old if row["priority_tier"] == "TA0_EXPLICIT_SELECTION"}
    v25_ids = {row["record_id"] for row in v25}

    assert len(ta0) == 32
    assert len(v25_ids) == 28
    assert v25_ids.isdisjoint(PRE_V25_TA0)
    assert v25_ids | PRE_V25_TA0 == ta0


def test_v25_uses_only_v3_active_holdout_sources():
    active = {row["record_id"] for row in _rows(V3_SOURCE)}
    v25_ids = {row["record_id"] for row in _rows(V25)}
    assert v25_ids <= active


def test_v25_decision_counts_and_reasons_are_frozen():
    rows = _rows(V25)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 20,
        "EXCLUDE": 8,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA0_HOLDOUT_SCREEN_V25_2026-09-25"
    }

    excluded = {
        row["record_id"]: row["screen_title_abstract_reason"]
        for row in rows
        if row["screen_title_abstract"] == "EXCLUDE"
    }
    assert excluded == {
        "SCHPRISMA-000568": "TA_NOT_FLORAL_SIGNAL",
        "SCHPRISMA-000598": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000650": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000660": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000665": "TA_NO_POLLINATOR_COMPONENT",
        "SCHPRISMA-000786": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000855": "TA_NO_ANTAGONIST_COMPONENT",
        "SCHPRISMA-000860": "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS",
    }


def test_relevant_syntheses_are_retained_at_ta_stage_not_misclassified_as_primary_exclusions():
    rows = {row["record_id"]: row for row in _rows(V25)}
    assert rows["SCHPRISMA-000503"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert rows["SCHPRISMA-000561"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "synthesis" in rows["SCHPRISMA-000503"]["decision_note"].lower()
    assert "synthesis" in rows["SCHPRISMA-000561"]["decision_note"].lower()

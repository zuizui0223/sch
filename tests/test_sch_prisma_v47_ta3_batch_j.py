import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V47 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V47_TA3_BATCH_J.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v47_is_exactly_the_tenth_25_frozen_ta3_records():
    v47 = _rows(V47)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[225:250]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v47] == expected
    assert int(frozen[225]["review_order"]) == 304
    assert int(frozen[249]["review_order"]) == 328


def test_v47_decision_counts_are_frozen():
    rows = _rows(V47)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 6,
        "EXCLUDE": 19,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_J_SCREEN_V47_2026-09-26"
    }


def test_v47_retains_multi_agent_and_fitness_candidates():
    rows = {row["record_id"]: row for row in _rows(V47)}
    for rid in (
        "SCHPRISMA-000692",
        "SCHPRISMA-000696",
        "SCHPRISMA-000700",
        "SCHPRISMA-000702",
        "SCHPRISMA-000704",
        "SCHPRISMA-000705",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v47_preserves_arabidopsis_programme_dependence():
    rows = {row["record_id"]: row for row in _rows(V47)}
    assert "SCHPRISMA-000664" in rows["SCHPRISMA-000704"]["decision_note"]


def test_v47_excludes_unmeasured_pollinator_or_antagonist_channels():
    rows = {row["record_id"]: row for row in _rows(V47)}
    assert rows["SCHPRISMA-000691"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000698"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000697"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"

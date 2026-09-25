import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V39 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V39_TA3_BATCH_B.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v39_is_exactly_the_second_25_frozen_ta3_records():
    v39 = _rows(V39)
    frozen = [
        row for row in _rows(V3_SOURCE)
        if row["priority_tier"] == "TA3_REMAINDER"
    ]
    frozen = sorted(frozen, key=lambda row: int(row["review_order"]))
    expected = [row["record_id"] for row in frozen[25:50]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v39] == expected
    assert [int(row["review_order"]) for row in frozen[25:50]] == list(range(103, 128))


def test_v39_decision_counts_are_frozen():
    rows = _rows(V39)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 10,
        "EXCLUDE": 15,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_B_SCREEN_V39_2026-09-25"
    }


def test_v39_keeps_known_report_pairs_for_explicit_fulltext_deduplication():
    rows = {row["record_id"]: row for row in _rows(V39)}
    assert rows["SCHPRISMA-000436"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "SCHPRISMA-000401" in rows["SCHPRISMA-000436"]["decision_note"]
    assert rows["SCHPRISMA-000456"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "SCHPRISMA-000424/000425" in rows["SCHPRISMA-000456"]["decision_note"]


def test_v39_retains_direct_mutualist_antagonist_and_context_candidates():
    rows = {row["record_id"]: row for row in _rows(V39)}
    for rid in (
        "SCHPRISMA-000432",
        "SCHPRISMA-000435",
        "SCHPRISMA-000436",
        "SCHPRISMA-000440",
        "SCHPRISMA-000442",
        "SCHPRISMA-000443",
        "SCHPRISMA-000448",
        "SCHPRISMA-000450",
        "SCHPRISMA-000453",
        "SCHPRISMA-000456",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v39_excludes_pollinator_only_omics_and_non_focal_records():
    rows = {row["record_id"]: row for row in _rows(V39)}
    assert rows["SCHPRISMA-000430"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000431"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000439"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000454"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000457"]["screen_title_abstract_reason"] == "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS"

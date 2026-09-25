import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V40 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V40_TA3_BATCH_C.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v40_is_exactly_the_third_25_frozen_ta3_records():
    v40 = _rows(V40)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[50:75]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v40] == expected
    assert [int(row["review_order"]) for row in frozen[50:75]] == list(range(128, 153))


def test_v40_decision_counts_are_frozen():
    rows = _rows(V40)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 13,
        "EXCLUDE": 12,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_C_SCREEN_V40_2026-09-26"
    }


def test_v40_keeps_known_report_pairs_for_explicit_fulltext_deduplication():
    rows = {row["record_id"]: row for row in _rows(V40)}
    assert rows["SCHPRISMA-000463"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "SCHPRISMA-000464" in rows["SCHPRISMA-000463"]["decision_note"]
    assert rows["SCHPRISMA-000464"]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v40_retains_role_boundary_and_fitness_candidates():
    rows = {row["record_id"]: row for row in _rows(V40)}
    for rid in (
        "SCHPRISMA-000459",
        "SCHPRISMA-000462",
        "SCHPRISMA-000469",
        "SCHPRISMA-000470",
        "SCHPRISMA-000476",
        "SCHPRISMA-000477",
        "SCHPRISMA-000480",
        "SCHPRISMA-000481",
        "SCHPRISMA-000482",
        "SCHPRISMA-000483",
        "SCHPRISMA-000484",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v40_excludes_non_measured_or_nonplant_endpoints():
    rows = {row["record_id"]: row for row in _rows(V40)}
    assert rows["SCHPRISMA-000465"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000474"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000475"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000478"]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"

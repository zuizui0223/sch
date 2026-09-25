import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V42 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V42_TA3_BATCH_E.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v42_is_exactly_the_fifth_25_frozen_ta3_records():
    v42 = _rows(V42)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[100:125]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v42] == expected
    assert [int(row["review_order"]) for row in frozen[100:125]] == list(range(178, 203))


def test_v42_decision_counts_are_frozen():
    rows = _rows(V42)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 19,
        "EXCLUDE": 6,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_E_SCREEN_V42_2026-09-26"
    }


def test_v42_retains_multifunctional_nectar_and_role_boundary_sources():
    rows = {row["record_id"]: row for row in _rows(V42)}
    for rid in (
        "SCHPRISMA-000514",
        "SCHPRISMA-000516",
        "SCHPRISMA-000520",
        "SCHPRISMA-000522",
        "SCHPRISMA-000530",
        "SCHPRISMA-000535",
        "SCHPRISMA-000544",
        "SCHPRISMA-000545",
        "SCHPRISMA-000547",
        "SCHPRISMA-000551",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v42_keeps_duplicate_hummingbird_nectar_reports_for_fulltext_resolution():
    rows = {row["record_id"]: row for row in _rows(V42)}
    assert rows["SCHPRISMA-000531"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert rows["SCHPRISMA-000532"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "000532" in rows["SCHPRISMA-000531"]["decision_note"]


def test_v42_excludes_nonfloral_or_missing_counterpart_records():
    rows = {row["record_id"]: row for row in _rows(V42)}
    assert rows["SCHPRISMA-000513"]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"
    assert rows["SCHPRISMA-000534"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000537"]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"
    assert rows["SCHPRISMA-000541"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"

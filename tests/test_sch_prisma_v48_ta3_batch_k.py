import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V48 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V48_TA3_BATCH_K.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v48_is_exactly_the_eleventh_25_frozen_ta3_records():
    v48 = _rows(V48)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[250:275]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v48] == expected
    assert int(frozen[250]["review_order"]) == 329
    assert int(frozen[274]["review_order"]) == 353


def test_v48_decision_counts_are_frozen():
    rows = _rows(V48)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 9,
        "EXCLUDE": 16,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_K_SCREEN_V48_2026-09-26"
    }


def test_v48_retains_conflict_and_role_boundary_sources():
    rows = {row["record_id"]: row for row in _rows(V48)}
    for rid in (
        "SCHPRISMA-000708",
        "SCHPRISMA-000713",
        "SCHPRISMA-000714",
        "SCHPRISMA-000715",
        "SCHPRISMA-000720",
        "SCHPRISMA-000725",
        "SCHPRISMA-000726",
        "SCHPRISMA-000728",
        "SCHPRISMA-000734",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v48_preserves_slippery_flower_report_pair_for_fulltext_deduplication():
    rows = {row["record_id"]: row for row in _rows(V48)}
    assert rows["SCHPRISMA-000725"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert rows["SCHPRISMA-000726"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "SCHPRISMA-000725" in rows["SCHPRISMA-000726"]["decision_note"]


def test_v48_excludes_one_channel_and_nonfloral_records():
    rows = {row["record_id"]: row for row in _rows(V48)}
    assert rows["SCHPRISMA-000716"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000727"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000739"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V38 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V38_TA3_BATCH_A.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v38_is_exactly_the_first_25_frozen_ta3_records():
    v38 = _rows(V38)
    frozen = [
        row for row in _rows(V3_SOURCE)
        if row["priority_tier"] == "TA3_REMAINDER"
    ]
    frozen = sorted(frozen, key=lambda row: int(row["review_order"]))
    expected = [row["record_id"] for row in frozen[:25]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v38] == expected
    assert [int(row["review_order"]) for row in frozen[:25]] == list(range(78, 103))


def test_v38_decision_counts_are_frozen():
    rows = _rows(V38)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 14,
        "EXCLUDE": 11,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_A_SCREEN_V38_2026-09-25"
    }


def test_v38_retains_boundary_rich_primary_and_synthesis_candidates():
    rows = {row["record_id"]: row for row in _rows(V38)}
    for rid in (
        "SCHPRISMA-000401",
        "SCHPRISMA-000403",
        "SCHPRISMA-000404",
        "SCHPRISMA-000407",
        "SCHPRISMA-000408",
        "SCHPRISMA-000409",
        "SCHPRISMA-000413",
        "SCHPRISMA-000414",
        "SCHPRISMA-000416",
        "SCHPRISMA-000422",
        "SCHPRISMA-000424",
        "SCHPRISMA-000425",
        "SCHPRISMA-000426",
        "SCHPRISMA-000427",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v38_exclusions_follow_registered_ta_boundaries():
    rows = {row["record_id"]: row for row in _rows(V38)}
    assert rows["SCHPRISMA-000405"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000410"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000419"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000423"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000415"]["screen_title_abstract_reason"] == "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS"

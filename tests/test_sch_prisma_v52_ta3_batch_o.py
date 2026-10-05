import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V52 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V52_TA3_BATCH_O.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v52_is_exactly_the_fifteenth_25_frozen_ta3_records():
    v52 = _rows(V52)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[350:375]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v52] == expected
    assert int(frozen[350]["review_order"]) == 429
    assert int(frozen[374]["review_order"]) == 453


def test_v52_decision_counts_are_frozen():
    rows = _rows(V52)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 14,
        "EXCLUDE": 11,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_O_SCREEN_V52_2026-10-05"
    }


def test_v52_retains_role_switching_partition_and_context_systems():
    rows = {row["record_id"]: row for row in _rows(V52)}
    for rid in (
        "SCHPRISMA-000826",
        "SCHPRISMA-000828",
        "SCHPRISMA-000829",
        "SCHPRISMA-000831",
        "SCHPRISMA-000832",
        "SCHPRISMA-000834",
        "SCHPRISMA-000835",
        "SCHPRISMA-000838",
        "SCHPRISMA-000840",
        "SCHPRISMA-000843",
        "SCHPRISMA-000848",
        "SCHPRISMA-000849",
        "SCHPRISMA-000850",
        "SCHPRISMA-000851",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v52_keeps_nonplant_antagonists_and_nonfloral_axes_out():
    rows = {row["record_id"]: row for row in _rows(V52)}
    assert rows["SCHPRISMA-000836"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000847"]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"
    assert rows["SCHPRISMA-000853"]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"


def test_v52_does_not_promote_chemistry_only_or_unmeasured_receiver_claims():
    rows = {row["record_id"]: row for row in _rows(V52)}
    for rid in ("SCHPRISMA-000827", "SCHPRISMA-000852"):
        assert rows[rid]["screen_title_abstract"] == "EXCLUDE"

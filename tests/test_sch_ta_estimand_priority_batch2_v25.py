import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OVERLAY = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V25_ESTIMAND_PRIORITY_BATCH2.csv"
FREEZE = ROOT / "data" / "SCH_TA_ESTIMAND_PRIORITY_BATCH2_V25_FREEZE.csv"


def _rows(path):
    with path.open(encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h))


def test_v25_uses_exact_next_six_outcome_blind_priority_records():
    frozen = _rows(FREEZE)
    assert [int(r["review_order_before_v25"]) for r in frozen] == list(range(1, 7))
    assert [r["record_id"] for r in frozen] == [
        "SCHPRISMA-000597",
        "SCHPRISMA-000503",
        "SCHPRISMA-000837",
        "SCHPRISMA-000428",
        "SCHPRISMA-000506",
        "SCHPRISMA-000528",
    ]
    assert {r["priority_tier"] for r in frozen} == {"TA0_EXPLICIT_SELECTION_FITNESS"}


def test_v25_ta_decisions_are_bounded_to_screening_not_outcomes():
    rows = _rows(OVERLAY)
    assert len(rows) == 6
    assert {r["decision_source"] for r in rows} == {
        "SOURCE_VERIFIED_ESTIMAND_PRIORITY_BATCH2_V25_2026-09-25"
    }
    decisions = {r["record_id"]: r["screen_title_abstract"] for r in rows}
    assert decisions == {
        "SCHPRISMA-000597": "EXCLUDE",
        "SCHPRISMA-000503": "RETAIN_FULLTEXT",
        "SCHPRISMA-000837": "RETAIN_FULLTEXT",
        "SCHPRISMA-000428": "RETAIN_FULLTEXT",
        "SCHPRISMA-000506": "RETAIN_FULLTEXT",
        "SCHPRISMA-000528": "RETAIN_FULLTEXT",
    }
    excluded = next(r for r in rows if r["record_id"] == "SCHPRISMA-000597")
    assert excluded["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V43 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V43_TA3_BATCH_F.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v43_is_exactly_the_sixth_25_frozen_ta3_records():
    v43 = _rows(V43)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[125:150]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v43] == expected
    assert [int(row["review_order"]) for row in frozen[125:150]] == list(range(203, 228))


def test_v43_decision_counts_are_frozen():
    rows = _rows(V43)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 10,
        "EXCLUDE": 15,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_F_SCREEN_V43_2026-09-26"
    }


def test_v43_retains_negative_controls_and_role_coupled_systems():
    rows = {row["record_id"]: row for row in _rows(V43)}
    for rid in (
        "SCHPRISMA-000557",
        "SCHPRISMA-000567",
        "SCHPRISMA-000576",
        "SCHPRISMA-000577",
        "SCHPRISMA-000580",
        "SCHPRISMA-000581",
        "SCHPRISMA-000582",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "little evidence" in rows["SCHPRISMA-000557"]["decision_note"].lower()


def test_v43_excludes_pollinator_only_or_nonplant_endpoints():
    rows = {row["record_id"]: row for row in _rows(V43)}
    assert rows["SCHPRISMA-000554"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000566"]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"
    assert rows["SCHPRISMA-000578"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"
    assert rows["SCHPRISMA-000583"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"

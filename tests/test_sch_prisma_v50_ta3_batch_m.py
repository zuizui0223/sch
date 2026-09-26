import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V50 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V50_TA3_BATCH_M.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v50_is_exactly_the_thirteenth_25_frozen_ta3_records():
    v50 = _rows(V50)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[300:325]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v50] == expected
    assert int(frozen[300]["review_order"]) == 379
    assert int(frozen[324]["review_order"]) == 403


def test_v50_decision_counts_are_frozen():
    rows = _rows(V50)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 15,
        "EXCLUDE": 10,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_M_SCREEN_V50_2026-09-26"
    }


def test_v50_retains_multi_agent_and_role_boundary_sources():
    rows = {row["record_id"]: row for row in _rows(V50)}
    for rid in (
        "SCHPRISMA-000766","SCHPRISMA-000767","SCHPRISMA-000768",
        "SCHPRISMA-000771","SCHPRISMA-000772","SCHPRISMA-000773",
        "SCHPRISMA-000776","SCHPRISMA-000778","SCHPRISMA-000779",
        "SCHPRISMA-000782","SCHPRISMA-000783","SCHPRISMA-000784",
        "SCHPRISMA-000788","SCHPRISMA-000792","SCHPRISMA-000793",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v50_keeps_nonplant_mimicry_out_of_floral_trait_pool():
    rows = {row["record_id"]: row for row in _rows(V50)}
    for rid in ("SCHPRISMA-000790", "SCHPRISMA-000791"):
        assert rows[rid]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"


def test_v50_excludes_pollinator_only_records():
    rows = {row["record_id"]: row for row in _rows(V50)}
    assert rows["SCHPRISMA-000770"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000785"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"

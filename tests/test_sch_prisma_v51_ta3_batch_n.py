import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V51 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V51_TA3_BATCH_N.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v51_is_exactly_the_fourteenth_25_frozen_ta3_records():
    v51 = _rows(V51)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[325:350]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v51] == expected
    assert int(frozen[325]["review_order"]) == 404
    assert int(frozen[349]["review_order"]) == 428


def test_v51_decision_counts_are_frozen():
    rows = _rows(V51)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 9,
        "EXCLUDE": 16,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_N_SCREEN_V51_2026-10-05"
    }


def test_v51_retains_context_and_coupled_role_systems():
    rows = {row["record_id"]: row for row in _rows(V51)}
    for rid in (
        "SCHPRISMA-000794",
        "SCHPRISMA-000799",
        "SCHPRISMA-000807",
        "SCHPRISMA-000810",
        "SCHPRISMA-000811",
        "SCHPRISMA-000817",
        "SCHPRISMA-000818",
        "SCHPRISMA-000819",
        "SCHPRISMA-000821",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v51_excludes_pollinator_only_and_nonplant_antagonist_records():
    rows = {row["record_id"]: row for row in _rows(V51)}
    for rid in (
        "SCHPRISMA-000795",
        "SCHPRISMA-000796",
        "SCHPRISMA-000797",
        "SCHPRISMA-000804",
        "SCHPRISMA-000805",
        "SCHPRISMA-000808",
        "SCHPRISMA-000820",
        "SCHPRISMA-000823",
        "SCHPRISMA-000825",
    ):
        assert rows[rid]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"


def test_v51_excludes_editorial_or_broad_nonfocused_material():
    rows = {row["record_id"]: row for row in _rows(V51)}
    for rid in (
        "SCHPRISMA-000798",
        "SCHPRISMA-000809",
        "SCHPRISMA-000813",
        "SCHPRISMA-000824",
    ):
        assert rows[rid]["screen_title_abstract_reason"] == "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS"

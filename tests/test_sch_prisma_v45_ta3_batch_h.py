import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V45 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V45_TA3_BATCH_H.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v45_is_exactly_the_eighth_25_frozen_ta3_records():
    v45 = _rows(V45)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[175:200]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v45] == expected
    assert [int(row["review_order"]) for row in frozen[175:200]] == list(range(253, 278))


def test_v45_decision_counts_are_frozen():
    rows = _rows(V45)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 11,
        "EXCLUDE": 14,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_H_SCREEN_V45_2026-09-26"
    }


def test_v45_retains_strong_same_trait_and_role_boundary_sources():
    rows = {row["record_id"]: row for row in _rows(V45)}
    for rid in (
        "SCHPRISMA-000624",
        "SCHPRISMA-000627",
        "SCHPRISMA-000629",
        "SCHPRISMA-000630",
        "SCHPRISMA-000633",
        "SCHPRISMA-000637",
        "SCHPRISMA-000638",
        "SCHPRISMA-000639",
        "SCHPRISMA-000642",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v45_primula_and_cucurbita_shared_trait_candidates_are_not_filtered_by_result():
    rows = {row["record_id"]: row for row in _rows(V45)}
    assert "seed predation" in rows["SCHPRISMA-000624"]["decision_note"].lower()
    assert "same floral volatiles" in rows["SCHPRISMA-000642"]["decision_note"].lower()


def test_v45_excludes_commentary_and_unmeasured_counterpart_functions():
    rows = {row["record_id"]: row for row in _rows(V45)}
    assert rows["SCHPRISMA-000619"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000640"]["screen_title_abstract_reason"] == "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS"
    assert rows["SCHPRISMA-000643"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"

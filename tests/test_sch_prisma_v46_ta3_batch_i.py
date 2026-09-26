import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V46 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V46_TA3_BATCH_I.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v46_is_exactly_the_ninth_25_frozen_ta3_records():
    v46 = _rows(V46)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[200:225]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v46] == expected
    assert int(frozen[200]["review_order"]) == 278
    assert int(frozen[224]["review_order"]) == 303


def test_v46_decision_counts_are_frozen():
    rows = _rows(V46)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 6,
        "EXCLUDE": 19,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_I_SCREEN_V46_2026-09-26"
    }


def test_v46_retains_multi_agent_and_coupled_role_sources():
    rows = {row["record_id"]: row for row in _rows(V46)}
    for rid in (
        "SCHPRISMA-000647",
        "SCHPRISMA-000664",
        "SCHPRISMA-000666",
        "SCHPRISMA-000670",
        "SCHPRISMA-000674",
        "SCHPRISMA-000675",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v46_preserves_report_dependence_for_impatiens():
    rows = {row["record_id"]: row for row in _rows(V46)}
    assert "SCHPRISMA-000723" in rows["SCHPRISMA-000647"]["decision_note"]


def test_v46_excludes_pollinator_only_and_nonplant_records():
    rows = {row["record_id"]: row for row in _rows(V46)}
    assert rows["SCHPRISMA-000645"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000652"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert rows["SCHPRISMA-000668"]["screen_title_abstract_reason"] == "TA_NOT_FLORAL_SIGNAL"
    assert rows["SCHPRISMA-000678"]["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V49 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V49_TA3_BATCH_L.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v49_is_exactly_the_twelfth_25_frozen_ta3_records():
    v49 = _rows(V49)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[275:300]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v49] == expected
    assert int(frozen[275]["review_order"]) == 354
    assert int(frozen[299]["review_order"]) == 378


def test_v49_decision_counts_are_frozen():
    rows = _rows(V49)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 9,
        "EXCLUDE": 16,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_L_SCREEN_V49_2026-09-26"
    }


def test_v49_retains_strong_conflict_and_role_boundary_sources():
    rows = {row["record_id"]: row for row in _rows(V49)}
    for rid in (
        "SCHPRISMA-000752",
        "SCHPRISMA-000756",
        "SCHPRISMA-000758",
        "SCHPRISMA-000759",
        "SCHPRISMA-000760",
        "SCHPRISMA-000761",
        "SCHPRISMA-000762",
        "SCHPRISMA-000763",
        "SCHPRISMA-000765",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v49_excludes_supplementary_tables_as_non_independent_records():
    rows = {row["record_id"]: row for row in _rows(V49)}
    for rid in ("SCHPRISMA-000748", "SCHPRISMA-000749"):
        assert rows[rid]["screen_title_abstract_reason"] == "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS"


def test_v49_keeps_pollinator_parasites_out_of_plant_antagonist_channel():
    row = {row["record_id"]: row for row in _rows(V49)}["SCHPRISMA-000747"]
    assert row["screen_title_abstract_reason"] == "TA_NO_ANTAGONIST_COMPONENT"
    assert "pollinator" in row["decision_note"].lower()

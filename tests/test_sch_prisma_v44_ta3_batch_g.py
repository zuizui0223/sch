import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V44 = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V44_TA3_BATCH_G.csv"
V3_SOURCE = ROOT / "data" / "SCH_H2_REVERSAL_HOLDOUT_SOURCE_V3.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v44_is_exactly_the_seventh_25_frozen_ta3_records():
    v44 = _rows(V44)
    frozen = sorted(
        [row for row in _rows(V3_SOURCE) if row["priority_tier"] == "TA3_REMAINDER"],
        key=lambda row: int(row["review_order"]),
    )
    expected = [row["record_id"] for row in frozen[150:175]]
    assert len(expected) == 25
    assert [row["record_id"] for row in v44] == expected
    assert [int(row["review_order"]) for row in frozen[150:175]] == list(range(228, 253))


def test_v44_decision_counts_are_frozen():
    rows = _rows(V44)
    assert Counter(row["screen_title_abstract"] for row in rows) == {
        "RETAIN_FULLTEXT": 10,
        "EXCLUDE": 15,
    }
    assert {row["decision_source"] for row in rows} == {
        "SOURCE_VERIFIED_TA3_BATCH_G_SCREEN_V44_2026-09-26"
    }


def test_v44_retains_selection_and_brood_pollination_boundaries():
    rows = {row["record_id"]: row for row in _rows(V44)}
    for rid in (
        "SCHPRISMA-000586",
        "SCHPRISMA-000596",
        "SCHPRISMA-000600",
        "SCHPRISMA-000601",
        "SCHPRISMA-000603",
        "SCHPRISMA-000604",
        "SCHPRISMA-000611",
        "SCHPRISMA-000612",
        "SCHPRISMA-000613",
        "SCHPRISMA-000614",
    ):
        assert rows[rid]["screen_title_abstract"] == "RETAIN_FULLTEXT"


def test_v44_keeps_preprint_and_published_selection_reports_for_fulltext_dedupe():
    rows = {row["record_id"]: row for row in _rows(V44)}
    assert rows["SCHPRISMA-000611"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert rows["SCHPRISMA-000612"]["screen_title_abstract"] == "RETAIN_FULLTEXT"
    assert "000612" in rows["SCHPRISMA-000611"]["decision_note"]


def test_v44_excludes_commentary_peer_review_and_single_channel_records():
    rows = {row["record_id"]: row for row in _rows(V44)}
    assert rows["SCHPRISMA-000591"]["screen_title_abstract_reason"] == "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS"
    assert rows["SCHPRISMA-000592"]["screen_title_abstract_reason"] == "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS"
    assert rows["SCHPRISMA-000606"]["screen_title_abstract_reason"] == "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS"
    assert rows["SCHPRISMA-000609"]["screen_title_abstract_reason"] == "TA_NO_POLLINATOR_COMPONENT"

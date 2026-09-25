import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V37_TA2_FULLTEXT_CLOSURE.csv"


def _rows():
    with PRISMA.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v37_closes_exactly_the_final_two_retained_ta2_records():
    rows = _rows()
    assert [row["record_id"] for row in rows] == [
        "SCHPRISMA-000844",
        "SCHPRISMA-000863",
    ]


def test_v37_mimulus_dissertation_is_composite_p2_not_h1_geometry():
    row = {row["record_id"]: row for row in _rows()}["SCHPRISMA-000844"]
    assert row["screen_fulltext"] == "INCLUDE"
    assert row["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"
    assert row["pollinator_response_measured"].startswith("YES_")
    assert row["antagonist_response_measured"].startswith("YES_")
    assert row["common_reproductive_outcome"] == "NO_COMMON_REPRODUCTIVE_OUTCOME"
    assert "separate chapters/experiments" in row["decision_note"].lower()


def test_v37_bioscience_synthesis_is_not_counted_as_primary():
    row = {row["record_id"]: row for row in _rows()}["SCHPRISMA-000863"]
    assert row["screen_fulltext"] == "EXCLUDE"
    assert row["screen_fulltext_reason"] == "FT_REVIEW_ONLY_NO_PRIMARY_ROLE"
    assert "review" in row["decision_note"].lower()

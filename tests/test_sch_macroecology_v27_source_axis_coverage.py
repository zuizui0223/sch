import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_V27_HOLDOUT_V1.csv"


def _rows():
    with BATCH.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v27_source_axis_batch_closes_exactly_four_new_h1_candidate_sources():
    rows = _rows()
    assert len(rows) == 4
    assert {row["source_id"] for row in rows} == {
        "SCHPRISMA-000649",
        "SCHPRISMA-000651",
        "SCHPRISMA-000661",
        "SCHPRISMA-000723",
    }
    assert {row["geometry_eligibility"] for row in rows} == {
        "ELIGIBLE_BOUNDED_COORDINATE"
    }
    assert {row["context_switch_eligibility"] for row in rows} == {
        "ELIGIBLE_MULTI_CONTEXT"
    }
    assert {row["trait_axis_action"] if "trait_axis_action" in row else "" for row in rows} == {""}


def test_v27_source_axis_batch_does_not_promote_outcome_geometry():
    rows = _rows()
    for row in rows:
        assert row["conflict_detected"] == "UNRESOLVED"
        assert row["alignment_detected"] == "UNRESOLVED"
        assert row["one_sided_or_null_detected"] == "UNRESOLVED"
        assert row["compromise_detected"] == "UNRESOLVED"
        assert row["cancellation_detected"] == "UNRESOLVED"
        assert row["shared_coordinate_status"] == "SPLIT_REQUIRED"


def test_v27_source_axis_batch_keeps_impatiens_numeric_source_pending():
    rows = {row["source_id"]: row for row in _rows()}
    assert rows["SCHPRISMA-000723"]["coding_status"] == "AXIS_SPLIT_REQUIRED_PENDING_NUMERIC_SOURCE"
    assert rows["SCHPRISMA-000649"]["coding_status"] == "AXIS_SPLIT_REQUIRED_NUMERIC_FREEZE"
    assert rows["SCHPRISMA-000651"]["coding_status"] == "AXIS_SPLIT_REQUIRED_NUMERIC_FREEZE"
    assert rows["SCHPRISMA-000661"]["coding_status"] == "AXIS_SPLIT_REQUIRED_NUMERIC_FREEZE"

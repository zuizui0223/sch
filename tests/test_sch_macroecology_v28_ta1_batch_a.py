import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V28_TA1_BATCH_A.csv"
AXIS = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_V28_TA1_BATCH_A.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v28_design_gate_is_methods_and_source_structure_only():
    rows = {row["record_id"]: row for row in _rows(DESIGN)}
    assert set(rows) == {
        "SCHPRISMA-000420",
        "SCHPRISMA-000429",
        "SCHPRISMA-000449",
    }
    assert rows["SCHPRISMA-000420"]["geometry_eligibility"] == "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"
    assert rows["SCHPRISMA-000429"]["geometry_eligibility"] == "ELIGIBLE_SAME_COORDINATE"
    assert rows["SCHPRISMA-000429"]["context_switch_eligibility"] == "ELIGIBLE_MULTI_CONTEXT"
    assert rows["SCHPRISMA-000449"]["geometry_eligibility"] == "UNRESOLVED_SOURCE"


def test_v28_does_not_force_composite_dissertation_into_h1():
    row = {row["record_id"]: row for row in _rows(DESIGN)}["SCHPRISMA-000449"]
    assert row["trait_axis_action"] == "SPLIT_REQUIRED"
    assert row["outcome_coding_status"] == "DEFERRED_PENDING_AXIS_SOURCE_RECODE"


def test_v28_vaccinium_is_single_same_coordinate_source_axis_with_unresolved_geometry():
    rows = _rows(AXIS)
    assert len(rows) == 1
    row = rows[0]
    assert row["source_id"] == "SCHPRISMA-000429"
    assert row["trait_domain"] == "PHENOLOGY"
    assert row["shared_coordinate_status"] == "SAME_COORDINATE"
    assert row["geometry_eligibility"] == "ELIGIBLE_SAME_COORDINATE"
    assert row["context_switch_eligibility"] == "ELIGIBLE_MULTI_CONTEXT"
    assert row["conflict_detected"] == "UNRESOLVED"
    assert row["alignment_detected"] == "UNRESOLVED"
    assert row["one_sided_or_null_detected"] == "UNRESOLVED"


def test_v28_source_axis_record_is_not_an_outcome_promotion():
    row = _rows(AXIS)[0]
    assert row["coding_status"] == "AXIS_FROZEN_OUTCOME_PENDING"
    assert "no conflict sign is assigned" in row["notes"].lower()

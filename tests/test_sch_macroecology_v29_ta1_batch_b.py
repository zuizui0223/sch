import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FT = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V29_TA1_FULLTEXT_BATCH_B.csv"
DESIGN = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V29_TA1_BATCH_B.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v29_fulltext_decisions_are_exactly_next_frozen_ta1_batch():
    rows = _rows(FT)
    assert [row["record_id"] for row in rows] == [
        "SCHPRISMA-000510",
        "SCHPRISMA-000538",
        "SCHPRISMA-000540",
        "SCHPRISMA-000542",
    ]
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["SCHPRISMA-000510"]["screen_fulltext"] == "EXCLUDE"
    assert by_id["SCHPRISMA-000510"]["screen_fulltext_reason"] == "FT_NO_ANTAGONIST_EVIDENCE"
    for rid in ("SCHPRISMA-000538","SCHPRISMA-000540","SCHPRISMA-000542"):
        assert by_id[rid]["screen_fulltext"] == "INCLUDE"
        assert by_id[rid]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_v29_design_gate_adds_role_boundary_not_h1_geometry():
    rows = {row["record_id"]: row for row in _rows(DESIGN)}
    assert set(rows) == {
        "SCHPRISMA-000538",
        "SCHPRISMA-000540",
        "SCHPRISMA-000542",
    }
    assert rows["SCHPRISMA-000538"]["geometry_eligibility"] == "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"
    assert rows["SCHPRISMA-000542"]["geometry_eligibility"] == "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"
    assert rows["SCHPRISMA-000540"]["geometry_eligibility"] == "BOUNDARY_BENEFIT_COST_COUPLED"
    assert rows["SCHPRISMA-000540"]["cancellation_eligibility"] == "INELIGIBLE_COUPLED_ROLE"


def test_v29_lonicera_role_boundary_is_not_promoted_to_trait_axis():
    row = {row["record_id"]: row for row in _rows(DESIGN)}["SCHPRISMA-000540"]
    assert row["trait_axis_action"] == "SPLIT_FOR_H4"
    assert row["outcome_coding_status"] == "DEFERRED_ROLE_BOUNDARY_ONLY"

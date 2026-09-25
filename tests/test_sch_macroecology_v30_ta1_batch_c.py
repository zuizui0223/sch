import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FT = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V30_TA1_FULLTEXT_BATCH_C.csv"
DESIGN = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V30_TA1_BATCH_C.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v30_fulltext_decisions_are_next_four_ta1_records():
    rows = _rows(FT)
    assert [row["record_id"] for row in rows] == [
        "SCHPRISMA-000543",
        "SCHPRISMA-000546",
        "SCHPRISMA-000548",
        "SCHPRISMA-000549",
    ]
    assert {row["screen_fulltext"] for row in rows} == {"INCLUDE"}
    assert {row["evidence_lanes"] for row in rows} == {"DIRECTIONAL_OR_NEAR_PASS"}


def test_v30_role_boundary_and_no_geometry_decisions_are_explicit():
    rows = {row["record_id"]: row for row in _rows(DESIGN)}
    assert rows["SCHPRISMA-000546"]["geometry_eligibility"] == "BOUNDARY_BENEFIT_COST_COUPLED"
    assert rows["SCHPRISMA-000546"]["trait_axis_action"] == "SPLIT_FOR_H4"
    for rid in ("SCHPRISMA-000543","SCHPRISMA-000548","SCHPRISMA-000549"):
        assert rows[rid]["geometry_eligibility"] == "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"
        assert rows[rid]["trait_axis_action"] == "NO_AXIS_PROMOTION"


def test_v30_clinopodium_adds_spatial_receiver_context_but_not_h1_trait_geometry():
    ft = {row["record_id"]: row for row in _rows(FT)}
    design = {row["record_id"]: row for row in _rows(DESIGN)}
    row = ft["SCHPRISMA-000549"]
    assert row["geographic_contrast"] == "ELEVATIONAL_GRADIENT_MULTI_SITE"
    assert row["receiver_assemblage_contrast"] == "ELEVATIONAL_VISITOR_COMMUNITY_TURNOVER"
    assert design["SCHPRISMA-000549"]["geometry_eligibility"] == "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"

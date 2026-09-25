import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V32_TA1_BATCH_E.csv"
PRISMA = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V32_TA1_FULLTEXT_BATCH_E.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v32_closes_all_remaining_ta1_fulltexts():
    rows = _rows(PRISMA)
    assert [row["record_id"] for row in rows] == [
        "SCHPRISMA-000663",
        "SCHPRISMA-000729",
        "SCHPRISMA-000736",
        "SCHPRISMA-000780",
        "SCHPRISMA-000839",
    ]
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["SCHPRISMA-000780"]["screen_fulltext"] == "EXCLUDE"
    assert by_id["SCHPRISMA-000780"]["screen_fulltext_reason"] == "FT_REVIEW_ONLY_NO_PRIMARY_ROLE"
    for rid in ("SCHPRISMA-000663","SCHPRISMA-000729","SCHPRISMA-000736","SCHPRISMA-000839"):
        assert by_id[rid]["screen_fulltext"] == "INCLUDE"
        assert by_id[rid]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_v32_role_boundaries_are_not_fixed_antagonist_h1_geometry():
    rows = {row["record_id"]: row for row in _rows(DESIGN)}
    for rid in ("SCHPRISMA-000663", "SCHPRISMA-000729"):
        assert rows[rid]["geometry_eligibility"] == "BOUNDARY_BENEFIT_COST_COUPLED"
        assert rows[rid]["cancellation_eligibility"] == "INELIGIBLE_COUPLED_ROLE"
        assert rows[rid]["outcome_coding_status"] == "DEFERRED_ROLE_BOUNDARY_ONLY"


def test_v32_spatial_context_records_do_not_gain_same_trait_h1_status():
    rows = {row["record_id"]: row for row in _rows(DESIGN)}
    assert rows["SCHPRISMA-000736"]["geometry_eligibility"] == "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"
    assert rows["SCHPRISMA-000839"]["geometry_eligibility"] == "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"
    assert rows["SCHPRISMA-000839"]["context_switch_eligibility"] == "ELIGIBLE_MULTI_CONTEXT"
    assert rows["SCHPRISMA-000839"]["trait_axis_action"] == "NO_AXIS_PROMOTION"


def test_v32_brassica_incana_is_context_evidence_not_trait_conflict_evidence():
    row = {row["record_id"]: row for row in _rows(DESIGN)}["SCHPRISMA-000839"]
    assert "15" in _rows(PRISMA)[-1]["decision_note"] or "Fifteen" in row["eligibility_rationale"]
    assert "no one declared floral trait coordinate" in row["eligibility_rationale"].lower()

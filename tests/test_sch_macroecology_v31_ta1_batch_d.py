import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FT = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V31_TA1_FULLTEXT_BATCH_D.csv"
DESIGN = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V31_TA1_BATCH_D.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v31_fulltext_decisions_are_next_four_ta1_records():
    rows = _rows(FT)
    assert [row["record_id"] for row in rows] == [
        "SCHPRISMA-000564",
        "SCHPRISMA-000565",
        "SCHPRISMA-000599",
        "SCHPRISMA-000610",
    ]
    by_id = {row["record_id"]: row for row in rows}
    assert by_id["SCHPRISMA-000565"]["screen_fulltext"] == "EXCLUDE"
    assert by_id["SCHPRISMA-000565"]["screen_fulltext_reason"] == "FT_DUPLICATE_DATASET_OR_REPORT"
    for rid in ("SCHPRISMA-000564","SCHPRISMA-000599","SCHPRISMA-000610"):
        assert by_id[rid]["screen_fulltext"] == "INCLUDE"
        assert by_id[rid]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_v31_design_gate_keeps_all_three_primary_studies_out_of_h1_geometry():
    rows = {row["record_id"]: row for row in _rows(DESIGN)}
    assert set(rows) == {
        "SCHPRISMA-000564",
        "SCHPRISMA-000599",
        "SCHPRISMA-000610",
    }
    assert {row["geometry_eligibility"] for row in rows.values()} == {
        "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"
    }
    assert {row["trait_axis_action"] for row in rows.values()} == {
        "NO_AXIS_PROMOTION"
    }


def test_v31_duplicate_preprint_is_explicitly_removed_at_fulltext_not_ta():
    by_id = {row["record_id"]: row for row in _rows(FT)}
    assert "version of record" in by_id["SCHPRISMA-000565"]["decision_note"].lower()
    assert "schprisma-000564" in by_id["SCHPRISMA-000565"]["decision_note"].lower()

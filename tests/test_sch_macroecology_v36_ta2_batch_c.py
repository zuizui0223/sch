import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V36_TA2_FULLTEXT_BATCH_C.csv"
DESIGN = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V36_TA2_BATCH_C.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v36_all_four_records_are_formally_included_with_correct_evidence_lanes():
    rows = {row["record_id"]: row for row in _rows(PRISMA)}
    assert set(rows) == {
        "SCHPRISMA-000745",
        "SCHPRISMA-000816",
        "SCHPRISMA-000830",
        "SCHPRISMA-000842",
    }
    assert {row["screen_fulltext"] for row in rows.values()} == {"INCLUDE"}
    assert rows["SCHPRISMA-000830"]["evidence_lanes"] == "EVOLUTIONARY_OUTCOME"
    for rid in ("SCHPRISMA-000745", "SCHPRISMA-000816", "SCHPRISMA-000842"):
        assert rows[rid]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_v36_anemone_is_role_boundary_not_fixed_antagonist_conflict():
    rows = {row["record_id"]: row for row in _rows(DESIGN)}
    row = rows["SCHPRISMA-000816"]
    assert row["geometry_eligibility"] == "BOUNDARY_BENEFIT_COST_COUPLED"
    assert row["context_switch_eligibility"] == "ELIGIBLE_MULTI_CONTEXT"
    assert row["cancellation_eligibility"] == "INELIGIBLE_COUPLED_ROLE"
    assert row["outcome_coding_status"] == "DEFERRED_ROLE_BOUNDARY_ONLY"


def test_v36_camissoniopsis_is_multi_context_but_not_new_h1_axis():
    rows = {row["record_id"]: row for row in _rows(DESIGN)}
    row = rows["SCHPRISMA-000842"]
    assert row["geometry_eligibility"] == "INELIGIBLE_MULTIVARIATE_UNRESOLVED"
    assert row["context_switch_eligibility"] == "ELIGIBLE_MULTI_CONTEXT"
    assert row["trait_axis_action"] == "SPLIT_REQUIRED"
    assert "SCHPRISMA-000287" in row["eligibility_rationale"]


def test_v36_leafflower_is_geographic_mosaic_outcome_not_common_fitness_geometry():
    row = {row["record_id"]: row for row in _rows(PRISMA)}["SCHPRISMA-000830"]
    assert row["evidence_lanes"] == "EVOLUTIONARY_OUTCOME"
    assert row["geographic_contrast"] == "SIXTEEN_POPULATION_GEOGRAPHIC_MOSAIC"
    assert row["receiver_assemblage_contrast"] == "MOTH_ASSEMBLAGE_CONTRAST_ACROSS_POPULATIONS"
    assert row["common_reproductive_outcome"] == "NO_COMMON_REPRODUCTIVE_OUTCOME"


def test_v36_annona_is_multiguild_p2_without_common_reproductive_endpoint():
    row = {row["record_id"]: row for row in _rows(PRISMA)}["SCHPRISMA-000745"]
    assert row["pollinator_response_measured"].startswith("YES_")
    assert row["antagonist_response_measured"].startswith("YES_")
    assert row["common_reproductive_outcome"] == "NO_COMMON_REPRODUCTIVE_OUTCOME"

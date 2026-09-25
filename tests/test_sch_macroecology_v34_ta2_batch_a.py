import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V34_TA2_FULLTEXT_BATCH_A.csv"
DESIGN = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V34_TA2_BATCH_A.csv"


def _rows(path: Path):
    with path.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v34_fulltext_decisions_preserve_duplicate_and_evidence_lane_boundaries():
    rows = {row["record_id"]: row for row in _rows(PRISMA)}
    assert set(rows) == {
        "SCHPRISMA-000569",
        "SCHPRISMA-000594",
        "SCHPRISMA-000621",
        "SCHPRISMA-000622",
    }
    assert rows["SCHPRISMA-000621"]["screen_fulltext"] == "EXCLUDE"
    assert rows["SCHPRISMA-000621"]["screen_fulltext_reason"] == "FT_DUPLICATE_DATASET_OR_REPORT"
    assert rows["SCHPRISMA-000594"]["screen_fulltext"] == "INCLUDE"
    assert rows["SCHPRISMA-000594"]["evidence_lanes"] == "EVOLUTIONARY_OUTCOME"
    assert rows["SCHPRISMA-000569"]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"
    assert rows["SCHPRISMA-000622"]["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_v34_isoplexis_is_broad_p1_but_not_same_trait_h1_geometry():
    rows = _rows(DESIGN)
    assert len(rows) == 1
    row = rows[0]
    assert row["record_id"] == "SCHPRISMA-000569"
    assert row["geometry_eligibility"] == "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY"
    assert row["context_switch_eligibility"] == "INELIGIBLE_GEOMETRY_NOT_ESTABLISHED"
    assert row["trait_axis_action"] == "NO_AXIS_PROMOTION"


def test_v34_solarium_service_cost_case_has_both_responses_without_common_fitness():
    row = {row["record_id"]: row for row in _rows(PRISMA)}["SCHPRISMA-000622"]
    assert row["pollinator_response_measured"].startswith("YES_")
    assert row["antagonist_response_measured"].startswith("YES_")
    assert row["common_reproductive_outcome"] == "NO_COMMON_REPRODUCTIVE_OUTCOME"
    assert "pollen" in row["decision_note"].lower()


def test_v34_tribulus_is_comparative_outcome_not_direct_receiver_geometry():
    row = {row["record_id"]: row for row in _rows(PRISMA)}["SCHPRISMA-000594"]
    assert row["evidence_lanes"] == "EVOLUTIONARY_OUTCOME"
    assert row["pollinator_response_measured"] == "NO_DIRECT_POLLINATOR_RESPONSE_TRAIT_PROXY_ONLY"
    assert row["antagonist_response_measured"] == "NO_DIRECT_GRANIVORE_RESPONSE_TRAIT_PROXY_ONLY"
    assert row["geographic_contrast"] == "ISLAND_VS_CONTINENTAL_POPULATION_COMPARISON"

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V35_TA2_FULLTEXT_BATCH_B.csv"


def _rows():
    with PRISMA.open(encoding="utf-8", newline="") as h:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(h)]


def test_v35_preserves_primary_vs_synthesis_boundary():
    rows = {row["record_id"]: row for row in _rows()}
    assert set(rows) == {
        "SCHPRISMA-000626",
        "SCHPRISMA-000628",
        "SCHPRISMA-000721",
        "SCHPRISMA-000733",
    }
    assert rows["SCHPRISMA-000733"]["screen_fulltext"] == "EXCLUDE"
    assert rows["SCHPRISMA-000733"]["screen_fulltext_reason"] == "FT_REVIEW_ONLY_NO_PRIMARY_ROLE"


def test_v35_sabatia_is_paired_response_without_common_fitness():
    row = {row["record_id"]: row for row in _rows()}["SCHPRISMA-000626"]
    assert row["screen_fulltext"] == "INCLUDE"
    assert row["pollinator_response_measured"].startswith("YES_")
    assert row["antagonist_response_measured"].startswith("YES_")
    assert row["common_reproductive_outcome"] == "NO_COMMON_REPRODUCTIVE_OUTCOME"
    assert row["evidence_lanes"] == "DIRECTIONAL_OR_NEAR_PASS"


def test_v35_hakea_is_evolutionary_outcome_not_direct_receiver_geometry():
    row = {row["record_id"]: row for row in _rows()}["SCHPRISMA-000628"]
    assert row["evidence_lanes"] == "EVOLUTIONARY_OUTCOME"
    assert row["pollinator_response_measured"] == "NO_DIRECT_POLLINATOR_RESPONSE_POLLINATION_SYNDROME_CLASSIFICATION"
    assert row["antagonist_response_measured"] == "NO_DIRECT_HERBIVORE_RESPONSE_DEFENCE_TRAIT_PROXY"
    assert row["common_reproductive_outcome"] == "NO_COMMON_REPRODUCTIVE_OUTCOME"


def test_v35_silene_hadena_focal_source_is_antagonist_side_only():
    row = {row["record_id"]: row for row in _rows()}["SCHPRISMA-000721"]
    assert row["screen_fulltext"] == "INCLUDE"
    assert row["pollinator_response_measured"] == "NO_POLLINATION_SERVICE_RESPONSE_MEASURED_IN_FOCAL_SOURCE"
    assert row["antagonist_response_measured"].startswith("YES_")
    assert row["common_reproductive_outcome"] == "NO_COMMON_REPRODUCTIVE_OUTCOME"
    assert "nursery pollinator" in row["decision_note"].lower()

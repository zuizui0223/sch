import csv
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRISMA = ROOT / "empirical" / "prisma"
FROZEN = PRISMA / "frozen_v2" / "SCH_PRISMA_V2_IDENTIFIED_CANDIDATES_FROZEN_2026-08-29.csv"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_primary_candidates.py"


def _module():
    spec = importlib.util.spec_from_file_location("sch_macro_candidates", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_macro_candidate_universe_keeps_every_current_fulltext_include():
    rows, receipt = _module().build(FROZEN, PRISMA)
    assert len(rows) == 131
    assert len({row["record_id"] for row in rows}) == 131
    assert receipt["n_primary_candidates"] == 131
    assert receipt["candidate_rule"] == "all_current_fulltext_INCLUDE_records_no_outcome_sign_filter"


def test_macro_candidate_universe_does_not_filter_by_existing_evidence_lane():
    rows, receipt = _module().build(FROZEN, PRISMA)
    lane_counts = receipt["evidence_lane_counts"]
    assert lane_counts["STRICT_LINKED_EXPERIMENT"] == 2
    assert lane_counts["DIRECTIONAL_OR_NEAR_PASS"] == 118
    assert lane_counts["EVOLUTIONARY_OUTCOME"] == 39
    assert lane_counts["HISTORICAL_TRANSITION"] == 4
    assert all(row["geometry_eligibility"] == "PENDING_SOURCE_RECODE" for row in rows)
    assert all(row["macro_coding_status"] == "UNADJUDICATED" for row in rows)


def test_macro_candidate_universe_preserves_existing_geography_without_using_it_as_eligibility():
    rows, receipt = _module().build(FROZEN, PRISMA)
    geo = receipt["existing_geography_coverage"]
    assert geo["positive_geographic_contrast_records"] == 27
    assert geo["positive_receiver_contrast_records"] == 25
    assert geo["joint_positive_records"] == 23
    assert len(rows) == 131


def test_macro_candidate_builder_populates_no_new_ecological_outcome():
    rows, receipt = _module().build(FROZEN, PRISMA)
    assert receipt["macro_outcome_fields_populated"] == 0
    assert "no_conflict_prevalence" in receipt["claim_ceiling"]
    assert "no_moderator_test_before_source_recode" in receipt["claim_ceiling"]


def test_candidate_csv_roundtrip(tmp_path):
    mod = _module()
    rows, _ = mod.build(FROZEN, PRISMA)
    out = tmp_path / "candidates.csv"
    mod._write_csv(out, rows)
    with out.open(encoding="utf-8", newline="") as handle:
        reread = list(csv.DictReader(handle))
    assert len(reread) == 131
    assert reread[0]["record_id"].startswith("SCHPRISMA-")
    assert reread[0]["geometry_eligibility"] == "PENDING_SOURCE_RECODE"
    assert reread[0]["design_audit_eligible"] == "YES_CURRENT_FULLTEXT_INCLUDE"


def test_recode_priority_uses_design_structure_not_result_sign():
    mod = _module()
    base = {
        "pollinator_response_measured": "YES",
        "antagonist_response_measured": "YES",
        "common_reproductive_outcome": "YES",
        "selection_form": "OPPOSING",
        "evidence_lanes": "DIRECTIONAL_OR_NEAR_PASS",
    }
    assert mod._recode_priority(base) == "P1_LINKED_GEOMETRY"
    changed = {**base, "selection_form": "REINFORCING", "evidence_lanes": "EVOLUTIONARY_OUTCOME"}
    assert mod._recode_priority(changed) == "P1_LINKED_GEOMETRY"
    no_fitness = {**base, "common_reproductive_outcome": "NO_COMMON_REPRODUCTIVE_OUTCOME"}
    assert mod._recode_priority(no_fitness) == "P2_SHARED_RESPONSE_NO_COMMON_FITNESS"

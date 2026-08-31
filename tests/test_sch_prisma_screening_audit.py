from __future__ import annotations

import csv
from pathlib import Path

from scripts.audit_sch_prisma_screening import audit
from scripts.harvest_sch_prisma_candidates import OUTPUT_FIELDS


def _base_row(i: int) -> dict[str, str]:
    row = {field: "" for field in OUTPUT_FIELDS}
    row.update(
        {
            "record_id": f"SCHPRISMA-{i:06d}",
            "doi": f"10.9999/{i}",
            "title": f"Candidate {i}",
            "year": "2020",
            "source_databases": "OPENALEX",
            "query_ids": "Q01",
            "identification_status": "UNSCREENED",
        }
    )
    return row


def _write_batches(directory: Path, rows: list[dict[str, str]]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "SCH_PRISMA_V2_SCREEN_BATCH_01.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_unscreened_workspace_is_not_started(tmp_path) -> None:
    rows = [_base_row(i) for i in range(1, 5)]
    _write_batches(tmp_path, rows)
    receipt = audit(tmp_path, expected_denominator=4)
    assert receipt["screening_status"] == "TITLE_ABSTRACT_NOT_STARTED"
    assert receipt["title_abstract"]["unscreened"] == 4
    assert receipt["prisma_flow"]["records_screened_title_abstract"] == 0
    assert receipt["prisma_flow"]["studies_included"] == 0


def test_title_abstract_reason_is_required_for_exclusion(tmp_path) -> None:
    rows = [_base_row(i) for i in range(1, 3)]
    rows[0]["screen_title_abstract"] = "EXCLUDE"
    _write_batches(tmp_path, rows)
    try:
        audit(tmp_path, expected_denominator=2)
    except ValueError as exc:
        assert "EXCLUDE requires one registered TA reason" in str(exc)
    else:
        raise AssertionError("missing exclusion reason must fail")


def test_included_fulltext_requires_available_status_and_evidence_lane(tmp_path) -> None:
    rows = [_base_row(i) for i in range(1, 3)]
    rows[0]["screen_title_abstract"] = "RETAIN_FULLTEXT"
    rows[0]["fulltext_status"] = "AVAILABLE"
    rows[0]["screen_fulltext"] = "INCLUDE"
    _write_batches(tmp_path, rows)
    try:
        audit(tmp_path, expected_denominator=2)
    except ValueError as exc:
        assert "requires at least one evidence_lane" in str(exc)
    else:
        raise AssertionError("included full text without lane must fail")


def test_complete_screening_separates_not_retrieved_from_assessed_reports(tmp_path) -> None:
    rows = [_base_row(i) for i in range(1, 5)]
    rows[0]["screen_title_abstract"] = "RETAIN_FULLTEXT"
    rows[0]["fulltext_status"] = "AVAILABLE"
    rows[0]["screen_fulltext"] = "INCLUDE"
    rows[0]["evidence_lanes"] = "STRICT_LINKED_EXPERIMENT;EVOLUTIONARY_OUTCOME"
    rows[0]["study_region"] = "Eastern North America"
    rows[0]["geographic_contrast"] = "MULTISITE_LATITUDINAL"
    rows[0]["receiver_assemblage_contrast"] = "NOT_REPORTED"

    rows[1]["screen_title_abstract"] = "RETAIN_FULLTEXT"
    rows[1]["fulltext_status"] = "UNAVAILABLE"
    rows[1]["screen_fulltext"] = "EXCLUDE"
    rows[1]["screen_fulltext_reason"] = "FT_FULLTEXT_UNAVAILABLE"

    rows[2]["screen_title_abstract"] = "EXCLUDE"
    rows[2]["screen_title_abstract_reason"] = "TA_NO_ANTAGONIST_COMPONENT"
    rows[3]["screen_title_abstract"] = "EXCLUDE"
    rows[3]["screen_title_abstract_reason"] = "TA_NOT_FLORAL_SIGNAL"

    _write_batches(tmp_path, rows)
    receipt = audit(tmp_path, expected_denominator=4)
    assert receipt["screening_status"] == "SCREENING_COMPLETE"
    assert receipt["fulltext"]["decision_excluded"] == 1
    assert receipt["fulltext"]["assessed_excluded"] == 0
    assert receipt["fulltext"]["unavailable"] == 1
    assert receipt["prisma_flow"] == {
        "records_identified_after_deduplication": 4,
        "records_screened_title_abstract": 4,
        "records_excluded_title_abstract": 2,
        "reports_sought_for_retrieval": 2,
        "reports_not_retrieved": 1,
        "reports_assessed_for_eligibility": 1,
        "reports_excluded_fulltext": 0,
        "studies_included": 1,
    }
    assert receipt["evidence_lane_counts"]["STRICT_LINKED_EXPERIMENT"] == 1
    assert receipt["geography"]["geographic_contrast_reported"] == 1
    assert receipt["geography"]["geographic_contrast_positive"] == 1
    assert receipt["geography"]["receiver_assemblage_contrast_reported"] == 0
    assert receipt["geography"]["receiver_assemblage_contrast_positive"] == 0


def test_available_report_cannot_use_fulltext_unavailable_reason(tmp_path) -> None:
    rows = [_base_row(1)]
    rows[0]["screen_title_abstract"] = "RETAIN_FULLTEXT"
    rows[0]["fulltext_status"] = "AVAILABLE"
    rows[0]["screen_fulltext"] = "EXCLUDE"
    rows[0]["screen_fulltext_reason"] = "FT_FULLTEXT_UNAVAILABLE"
    _write_batches(tmp_path, rows)
    try:
        audit(tmp_path, expected_denominator=1)
    except ValueError as exc:
        assert "requires status=UNAVAILABLE" in str(exc)
    else:
        raise AssertionError("available report using unavailable reason must fail")


def test_negative_or_non_geographic_codes_are_reported_but_not_positive(tmp_path) -> None:
    rows = [_base_row(i) for i in range(1, 4)]
    for row in rows:
        row["screen_title_abstract"] = "RETAIN_FULLTEXT"
        row["fulltext_status"] = "AVAILABLE"
        row["screen_fulltext"] = "INCLUDE"
        row["evidence_lanes"] = "DIRECTIONAL_OR_NEAR_PASS"

    rows[0]["geographic_contrast"] = "NO_REPLICATED_GEOGRAPHIC_CONTRAST"
    rows[0]["receiver_assemblage_contrast"] = "NO_DIRECT_SPATIAL_RECEIVER_REGIME_CONTRAST"
    rows[1]["geographic_contrast"] = "EXPERIMENTAL_SETTING_CONTRAST_NOT_GEOGRAPHIC"
    rows[1]["receiver_assemblage_contrast"] = "NO_DIRECT_SPATIAL_RECEIVER_REGIME_CONTRAST"
    rows[2]["geographic_contrast"] = "LOWLAND_WITH_SPIDERS_VS_HIGHLAND_WITHOUT_SPIDERS"
    rows[2]["receiver_assemblage_contrast"] = "CRAB_SPIDER_OCCURRENCE_REGIME_CONTRAST"

    _write_batches(tmp_path, rows)
    receipt = audit(tmp_path, expected_denominator=3)
    assert receipt["geography"]["geographic_contrast_reported"] == 3
    assert receipt["geography"]["geographic_contrast_positive"] == 1
    assert receipt["geography"]["receiver_assemblage_contrast_reported"] == 3
    assert receipt["geography"]["receiver_assemblage_contrast_positive"] == 1


def test_nonretained_record_cannot_carry_fulltext_decision(tmp_path) -> None:
    rows = [_base_row(1)]
    rows[0]["screen_title_abstract"] = "EXCLUDE"
    rows[0]["screen_title_abstract_reason"] = "TA_NOT_FLORAL_SIGNAL"
    rows[0]["fulltext_status"] = "AVAILABLE"
    _write_batches(tmp_path, rows)
    try:
        audit(tmp_path, expected_denominator=1)
    except ValueError as exc:
        assert "full-text fields require RETAIN_FULLTEXT" in str(exc)
    else:
        raise AssertionError("full-text leakage must fail closed")

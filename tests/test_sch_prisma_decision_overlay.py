from __future__ import annotations

import csv

import scripts.apply_sch_prisma_screening_decisions as overlay
from scripts.harvest_sch_prisma_candidates import OUTPUT_FIELDS


def _row(i: int) -> dict[str, str]:
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


def _write_base(path, rows):
    path.mkdir(parents=True, exist_ok=True)
    with (path / "SCH_PRISMA_V2_SCREEN_BATCH_01.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _write_overlay(path, rows):
    fields = ["record_id", *sorted(overlay.FORMAL_FIELDS), "decision_source", "decision_note"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def test_empty_overlay_preserves_unscreened_state(tmp_path) -> None:
    base = tmp_path / "base"
    _write_base(base, [_row(1), _row(2)])
    decisions = tmp_path / "decisions.csv"
    _write_overlay(decisions, [])
    receipt = overlay.apply(base, decisions, tmp_path / "out", expected_denominator=2)
    assert receipt["changed_record_count"] == 0
    assert receipt["screening_status"] == "TITLE_ABSTRACT_NOT_STARTED"
    assert receipt["prisma_flow"]["records_screened_title_abstract"] == 0


def test_overlay_requires_decision_source_for_formal_change(tmp_path) -> None:
    base = tmp_path / "base"
    _write_base(base, [_row(1)])
    decisions = tmp_path / "decisions.csv"
    _write_overlay(
        decisions,
        [{"record_id": "SCHPRISMA-000001", "screen_title_abstract": "EXCLUDE", "screen_title_abstract_reason": "TA_NOT_FLORAL_SIGNAL"}],
    )
    try:
        overlay.apply(base, decisions, tmp_path / "out", expected_denominator=1)
    except ValueError as exc:
        assert "decision_source required" in str(exc)
    else:
        raise AssertionError("formal decision without decision_source must fail")


def test_overlay_applies_registered_human_decision_and_audits_it(tmp_path) -> None:
    base = tmp_path / "base"
    _write_base(base, [_row(1), _row(2)])
    decisions = tmp_path / "decisions.csv"
    _write_overlay(
        decisions,
        [
            {
                "record_id": "SCHPRISMA-000001",
                "screen_title_abstract": "EXCLUDE",
                "screen_title_abstract_reason": "TA_NONBIOLOGICAL_OR_OFF_TOPIC",
                "decision_source": "AUTHOR_ADJUDICATION",
                "decision_note": "Title/abstract reviewed externally",
            }
        ],
    )
    receipt = overlay.apply(base, decisions, tmp_path / "out", expected_denominator=2)
    assert receipt["changed_record_count"] == 1
    assert receipt["screening_status"] == "TITLE_ABSTRACT_IN_PROGRESS"
    assert receipt["prisma_flow"]["records_screened_title_abstract"] == 1
    assert receipt["prisma_flow"]["records_excluded_title_abstract"] == 1


def test_overlay_cannot_reference_unknown_candidate(tmp_path) -> None:
    base = tmp_path / "base"
    _write_base(base, [_row(1)])
    decisions = tmp_path / "decisions.csv"
    _write_overlay(
        decisions,
        [{"record_id": "SCHPRISMA-999999", "decision_source": "AUTHOR_ADJUDICATION"}],
    )
    try:
        overlay.apply(base, decisions, tmp_path / "out", expected_denominator=1)
    except ValueError as exc:
        assert "unknown record IDs" in str(exc)
    else:
        raise AssertionError("unknown overlay record must fail")

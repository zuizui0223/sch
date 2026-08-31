from __future__ import annotations

import csv
from pathlib import Path

from scripts.build_sch_prisma_screening_batches import (
    KNOWN_ANCHOR_DOIS,
    build_batches,
)
from scripts.harvest_sch_prisma_candidates import OUTPUT_FIELDS


def _write_fixture(path: Path, n: int = 12) -> None:
    rows = []
    anchors = sorted(KNOWN_ANCHOR_DOIS)
    for i in range(n):
        row = {field: "" for field in OUTPUT_FIELDS}
        row.update(
            {
                "record_id": f"SCHPRISMA-{i+1:06d}",
                "doi": anchors[i] if i < len(anchors) else f"10.9999/{i}",
                "title": f"Candidate {i+1}",
                "year": "2020",
                "source_databases": "OPENALEX",
                "query_ids": "Q01",
                "identification_status": "UNSCREENED",
            }
        )
        rows.append(row)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def test_build_batches_is_deterministic_and_anchor_guarded(tmp_path) -> None:
    source = tmp_path / "candidates.csv"
    _write_fixture(source)
    manifest = build_batches(source, tmp_path / "screen", batch_size=5)
    assert manifest["screening_denominator"] == 12
    assert manifest["batch_count"] == 3
    assert manifest["screening_status"] == "TITLE_ABSTRACT_NOT_STARTED"
    assert manifest["title_abstract_remaining"] == 12
    assert manifest["known_anchor_sensitivity"]["recovered_anchor_count"] == 8
    assert manifest["known_anchor_sensitivity"]["all_known_anchors_recovered"] is True
    assert manifest["batches"][0]["first_record_id"] == "SCHPRISMA-000001"
    assert manifest["batches"][0]["last_record_id"] == "SCHPRISMA-000005"
    assert manifest["batches"][-1]["records"] == 2


def test_workspace_rejects_missing_known_anchor(tmp_path) -> None:
    source = tmp_path / "candidates.csv"
    _write_fixture(source, n=7)
    try:
        build_batches(source, tmp_path / "screen", batch_size=5)
    except ValueError as exc:
        assert "known-anchor sensitivity check failed" in str(exc)
    else:
        raise AssertionError("missing anchor must fail closed")


def test_workspace_rejects_preadjudicated_initial_ledger(tmp_path) -> None:
    source = tmp_path / "candidates.csv"
    _write_fixture(source)
    rows = list(csv.DictReader(source.open(encoding="utf-8")))
    rows[0]["identification_status"] = "SCREENED"
    with source.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    try:
        build_batches(source, tmp_path / "screen", batch_size=5)
    except ValueError as exc:
        assert "requires all records to be UNSCREENED" in str(exc)
    else:
        raise AssertionError("preadjudicated initialization must fail closed")

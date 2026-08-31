from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.compare_sch_prisma_v2_live_drift import compare


FIELDS = ["record_id", "doi", "title", "year"]


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def _receipt(path: Path, status: str, n: int | None = None) -> None:
    data = {"systematic_completion_status": status}
    if n is not None:
        data["deduplicated_unscreened_candidates"] = n
    path.write_text(json.dumps(data), encoding="utf-8")


def test_identical_live_index_does_not_change_screening_denominator(tmp_path) -> None:
    frozen = tmp_path / "frozen.csv"
    live = tmp_path / "live.csv"
    receipt = tmp_path / "live.json"
    rows = [
        {"record_id": "SCHPRISMA-000001", "doi": "10.1/a", "title": "A", "year": "2020"},
        {"record_id": "SCHPRISMA-000002", "doi": "", "title": "A Floral Title", "year": "2021"},
    ]
    _write_csv(frozen, rows)
    _write_csv(live, list(reversed(rows)))
    _receipt(receipt, "PRISMA_V2_IDENTIFICATION_COMPLETE", 2)
    result = compare(frozen, live, receipt, expected_frozen_denominator=2)
    assert result["live_status"] == "LIVE_INDEX_MATCHES_FROZEN"
    assert result["added_since_freeze"] == 0
    assert result["removed_since_freeze"] == 0
    assert result["screening_denominator_changed"] is False


def test_added_live_record_is_drift_not_new_screening_denominator(tmp_path) -> None:
    frozen = tmp_path / "frozen.csv"
    live = tmp_path / "live.csv"
    receipt = tmp_path / "live.json"
    base = [
        {"record_id": "SCHPRISMA-000001", "doi": "10.1/a", "title": "A", "year": "2020"},
        {"record_id": "SCHPRISMA-000002", "doi": "10.1/b", "title": "B", "year": "2021"},
    ]
    _write_csv(frozen, base)
    _write_csv(
        live,
        base + [{"record_id": "SCHPRISMA-000003", "doi": "10.1/c", "title": "C", "year": "2022"}],
    )
    _receipt(receipt, "PRISMA_V2_IDENTIFICATION_COMPLETE", 3)
    result = compare(frozen, live, receipt, expected_frozen_denominator=2)
    assert result["frozen_denominator"] == 2
    assert result["live_deduplicated_candidates"] == 3
    assert result["net_candidate_count_drift"] == 1
    assert result["added_since_freeze"] == 1
    assert result["live_status"] == "LIVE_INDEX_DRIFT_DETECTED"
    assert result["screening_denominator_changed"] is False


def test_live_retrieval_failure_is_monitoring_failure_not_cohort_failure(tmp_path) -> None:
    frozen = tmp_path / "frozen.csv"
    receipt = tmp_path / "live.json"
    _write_csv(
        frozen,
        [{"record_id": "SCHPRISMA-000001", "doi": "10.1/a", "title": "A", "year": "2020"}],
    )
    _receipt(receipt, "PRISMA_V2_RETRIEVAL_FAILED")
    result = compare(frozen, None, receipt, expected_frozen_denominator=1)
    assert result["frozen_cohort_status"] == "LOCKED"
    assert result["live_status"] == "LIVE_RETRIEVAL_FAILED_OR_INCOMPLETE"
    assert result["screening_denominator_changed"] is False


def test_frozen_denominator_mismatch_fails_closed(tmp_path) -> None:
    frozen = tmp_path / "frozen.csv"
    live = tmp_path / "live.csv"
    receipt = tmp_path / "live.json"
    rows = [{"record_id": "SCHPRISMA-000001", "doi": "10.1/a", "title": "A", "year": "2020"}]
    _write_csv(frozen, rows)
    _write_csv(live, rows)
    _receipt(receipt, "PRISMA_V2_IDENTIFICATION_COMPLETE", 1)
    try:
        compare(frozen, live, receipt, expected_frozen_denominator=2)
    except ValueError as exc:
        assert "frozen cohort denominator changed" in str(exc)
    else:
        raise AssertionError("frozen denominator drift must fail closed")

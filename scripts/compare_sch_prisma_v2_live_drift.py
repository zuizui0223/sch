"""Compare a live SCH PRISMA V2 identification result with the frozen cohort.

The frozen cohort is the only screening denominator. This script never mutates
record IDs or screening decisions. A later OpenAlex index can add/remove/reindex
records; such changes are reported as bibliographic drift, not silently folded
into the active PRISMA cohort.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

try:
    import harvest_sch_prisma_candidates as v1
except ModuleNotFoundError:
    from scripts import harvest_sch_prisma_candidates as v1


def _read_candidates(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path}: missing header")
        required = {"doi", "title", "year"}
        missing = required - set(reader.fieldnames)
        if missing:
            raise ValueError(f"{path}: missing fields {sorted(missing)}")
        return [{k: (v or "").strip() for k, v in row.items()} for row in reader]


def _stable_key(row: dict[str, str]) -> str:
    doi = v1.normalize_doi(row.get("doi"))
    if doi:
        return f"doi:{doi}"
    title = v1.normalize_title(row.get("title"))
    year = row.get("year", "").strip()
    return f"titleyear:{title}|{year}"


def _index(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        key = _stable_key(row)
        if key in result:
            raise ValueError(f"duplicate stable key within candidate file: {key}")
        result[key] = row
    return result


def _example(index: dict[str, dict[str, str]], key: str) -> dict[str, str]:
    row = index[key]
    return {
        "stable_key": key,
        "doi": v1.normalize_doi(row.get("doi")),
        "title": row.get("title", ""),
        "year": row.get("year", ""),
    }


def compare(
    frozen_csv: Path,
    live_csv: Path | None,
    live_receipt_json: Path,
    *,
    expected_frozen_denominator: int = 868,
) -> dict[str, Any]:
    frozen_rows = _read_candidates(frozen_csv)
    if len(frozen_rows) != expected_frozen_denominator:
        raise ValueError(
            f"frozen cohort denominator changed: expected {expected_frozen_denominator}, got {len(frozen_rows)}"
        )
    frozen = _index(frozen_rows)

    live_receipt = json.loads(live_receipt_json.read_text(encoding="utf-8"))
    live_status = live_receipt.get("systematic_completion_status", "UNKNOWN")
    if live_status != "PRISMA_V2_IDENTIFICATION_COMPLETE" or live_csv is None or not live_csv.exists():
        return {
            "analysis_id": "sch_prisma_v2_live_index_drift_v1",
            "frozen_cohort_status": "LOCKED",
            "frozen_denominator": len(frozen),
            "live_status": "LIVE_RETRIEVAL_FAILED_OR_INCOMPLETE",
            "live_identification_status": live_status,
            "live_deduplicated_candidates": live_receipt.get("deduplicated_unscreened_candidates"),
            "added_since_freeze": None,
            "removed_since_freeze": None,
            "screening_denominator_changed": False,
            "claim_boundary": (
                "Live retrieval failure/incompleteness does not alter the frozen PRISMA screening cohort. "
                "The active denominator remains locked until a separately versioned protocol intentionally opens a new cohort."
            ),
        }

    live_rows = _read_candidates(live_csv)
    live = _index(live_rows)
    frozen_keys = set(frozen)
    live_keys = set(live)
    added = sorted(live_keys - frozen_keys)
    removed = sorted(frozen_keys - live_keys)
    drift = bool(added or removed)
    return {
        "analysis_id": "sch_prisma_v2_live_index_drift_v1",
        "frozen_cohort_status": "LOCKED",
        "frozen_denominator": len(frozen),
        "live_status": "LIVE_INDEX_DRIFT_DETECTED" if drift else "LIVE_INDEX_MATCHES_FROZEN",
        "live_identification_status": live_status,
        "live_deduplicated_candidates": len(live),
        "net_candidate_count_drift": len(live) - len(frozen),
        "added_since_freeze": len(added),
        "removed_since_freeze": len(removed),
        "added_examples": [_example(live, key) for key in added[:10]],
        "removed_examples": [_example(frozen, key) for key in removed[:10]],
        "screening_denominator_changed": False,
        "claim_boundary": (
            "OpenAlex is a moving bibliographic index. Added/removed live records are monitoring information only. "
            "They do not renumber records, alter prior decisions, or change the frozen screening denominator."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frozen_csv", type=Path)
    parser.add_argument("live_csv", type=Path)
    parser.add_argument("live_receipt_json", type=Path)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("--expected-frozen-denominator", type=int, default=868)
    args = parser.parse_args(argv)
    live_csv: Path | None = args.live_csv if args.live_csv.exists() else None
    receipt = compare(
        args.frozen_csv,
        live_csv,
        args.live_receipt_json,
        expected_frozen_denominator=args.expected_frozen_denominator,
    )
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({
        "frozen": receipt["frozen_denominator"],
        "live": receipt.get("live_deduplicated_candidates"),
        "live_status": receipt["live_status"],
        "denominator_changed": receipt["screening_denominator_changed"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

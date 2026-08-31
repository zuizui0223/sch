"""Build deterministic title/abstract screening batches from a complete V2 ledger.

This script does not make inclusion decisions. It validates the V2 candidate
schema, checks that all records are UNSCREENED at initialization, partitions
records deterministically by record_id, and emits batch CSV files plus a
progress manifest. Screening decisions are later written into these same
fields under the frozen protocol codes.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_FIELDS = (
    "record_id",
    "doi",
    "title",
    "year",
    "venue",
    "source_databases",
    "query_ids",
    "openalex_id",
    "identification_status",
    "screen_title_abstract",
    "screen_title_abstract_reason",
    "fulltext_status",
    "screen_fulltext",
    "screen_fulltext_reason",
)

KNOWN_ANCHOR_DOIS = {
    "10.1093/aob/mcad064",
    "10.1890/11-0825.1",
    "10.1371/journal.pone.0098755",
    "10.1093/aob/mcq045",
    "10.1038/s41467-018-03792-x",
    "10.7554/elife.07641",
    "10.1111/j.1600-0706.2013.20780.x",
    "10.3732/ajb.1400171",
}


def read_candidates(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("candidate CSV has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")
        rows = [{k: (v or "").strip() for k, v in row.items()} for row in reader]
        fieldnames = list(reader.fieldnames)
    if not rows:
        raise ValueError("candidate CSV is empty")
    ids = [row["record_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("record_id must be unique")
    if any(row["identification_status"] != "UNSCREENED" for row in rows):
        raise ValueError("initial screening workspace requires all records to be UNSCREENED")
    return fieldnames, sorted(rows, key=lambda r: r["record_id"])


def anchor_recovery(rows: list[dict[str, str]]) -> dict[str, object]:
    observed = {row["doi"].lower() for row in rows if row["doi"]}
    recovered = sorted(KNOWN_ANCHOR_DOIS & observed)
    missing = sorted(KNOWN_ANCHOR_DOIS - observed)
    return {
        "expected_anchor_count": len(KNOWN_ANCHOR_DOIS),
        "recovered_anchor_count": len(recovered),
        "recovered_anchor_dois": recovered,
        "missing_anchor_dois": missing,
        "all_known_anchors_recovered": not missing,
    }


def build_batches(
    candidate_csv: Path,
    out_dir: Path,
    *,
    batch_size: int = 100,
) -> dict[str, object]:
    if batch_size < 1:
        raise ValueError("batch_size must be >= 1")
    fieldnames, rows = read_candidates(candidate_csv)
    anchors = anchor_recovery(rows)
    if not anchors["all_known_anchors_recovered"]:
        raise ValueError(f"known-anchor sensitivity check failed: {anchors['missing_anchor_dois']}")

    out_dir.mkdir(parents=True, exist_ok=True)
    batch_rows: list[dict[str, object]] = []
    for start in range(0, len(rows), batch_size):
        chunk = rows[start : start + batch_size]
        number = start // batch_size + 1
        name = f"SCH_PRISMA_V2_SCREEN_BATCH_{number:02d}.csv"
        path = out_dir / name
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(chunk)
        batch_rows.append(
            {
                "batch": number,
                "file": name,
                "first_record_id": chunk[0]["record_id"],
                "last_record_id": chunk[-1]["record_id"],
                "records": len(chunk),
                "title_abstract_decided": 0,
                "title_abstract_retained": 0,
                "title_abstract_excluded": 0,
            }
        )

    manifest = {
        "analysis_id": "sch_prisma_v2_screening_workspace_v1",
        "screening_denominator": len(rows),
        "batch_size": batch_size,
        "batch_count": len(batch_rows),
        "title_abstract_decided": 0,
        "title_abstract_remaining": len(rows),
        "fulltext_decided": 0,
        "screening_status": "TITLE_ABSTRACT_NOT_STARTED",
        "known_anchor_sensitivity": anchors,
        "batches": batch_rows,
        "claim_boundary": (
            "Batch generation is workflow organization only. UNSCREENED records are not exclusions; "
            "no PRISMA screening count changes until a protocol-valid decision and reason are written."
        ),
    }
    (out_dir / "SCH_PRISMA_V2_SCREENING_PROGRESS.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate_csv", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--batch-size", type=int, default=100)
    args = parser.parse_args(argv)
    manifest = build_batches(args.candidate_csv, args.out_dir, batch_size=args.batch_size)
    print(json.dumps({
        "screening_denominator": manifest["screening_denominator"],
        "batch_count": manifest["batch_count"],
        "anchors_recovered": manifest["known_anchor_sensitivity"]["recovered_anchor_count"],
        "status": manifest["screening_status"],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

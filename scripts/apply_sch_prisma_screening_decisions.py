"""Overlay version-controlled SCH PRISMA screening decisions onto generated batches.

Identification batches remain reproducible outputs from the frozen candidate
cohort. Human/author adjudications live in separate sparse CSVs keyed by
record_id. This script applies only nonblank overlay fields, requires a declared
decision_source for any changed record, preserves bibliographic fields, and
writes a fresh audited batch directory plus an application receipt.

Malformed CSV rows fail closed: extra columns, missing trailing columns, or
blank/misaligned provenance are never silently coerced into an apparently valid
scientific decision.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

try:
    import audit_sch_prisma_screening as audit_mod
except ModuleNotFoundError:
    from scripts import audit_sch_prisma_screening as audit_mod


DECISION_META_FIELDS = {"decision_source", "decision_note"}
FORMAL_FIELDS = {
    "screen_title_abstract",
    "screen_title_abstract_reason",
    "fulltext_status",
    "screen_fulltext",
    "screen_fulltext_reason",
    "evidence_lanes",
    "A_trait",
    "A_manipulated",
    "pollinator_response_measured",
    "antagonist_response_measured",
    "common_reproductive_outcome",
    "selection_form",
    "cue_architecture",
    "evolutionary_level",
    "causal_strength",
    "claim_ceiling",
    "study_region",
    "country_or_ocean_basin",
    "latitude_reported",
    "longitude_reported",
    "spatial_grain",
    "spatial_extent",
    "single_site_vs_multisite",
    "geographic_contrast",
    "receiver_assemblage_contrast",
    "biogeographic_context",
    "historical_or_phylogenetic_context",
}


def _load_overlay(path: Path) -> dict[str, dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "record_id" not in reader.fieldnames:
            raise ValueError("decision overlay must contain record_id")
        raw_rows = list(reader)

    rows: list[dict[str, str]] = []
    for line_number, raw in enumerate(raw_rows, start=2):
        if None in raw:
            raise ValueError(
                f"{path.name}:{line_number}: overlay row has extra CSV columns; "
                "do not infer shifted provenance"
            )
        missing_cells = [field for field in reader.fieldnames if raw.get(field) is None]
        if missing_cells:
            raise ValueError(
                f"{path.name}:{line_number}: overlay row is shorter than the header; "
                f"missing cells for {missing_cells}"
            )
        rows.append({k: (v or "").strip() for k, v in raw.items()})

    overlay: dict[str, dict[str, str]] = {}
    for row in rows:
        record_id = row.get("record_id", "")
        if not record_id:
            raise ValueError("decision overlay row has blank record_id")
        if record_id in overlay:
            raise ValueError(f"duplicate decision overlay record_id: {record_id}")
        unknown = set(row) - ({"record_id"} | FORMAL_FIELDS | DECISION_META_FIELDS)
        if unknown:
            raise ValueError(f"unknown overlay fields: {sorted(unknown)}")
        changed = any(row.get(field, "") for field in FORMAL_FIELDS)
        if changed and not row.get("decision_source", ""):
            raise ValueError(f"{record_id}: decision_source required when formal fields are populated")
        if row.get("decision_note", "") and not row.get("decision_source", ""):
            raise ValueError(f"{record_id}: decision_note requires decision_source")
        overlay[record_id] = row
    return overlay


def apply(base_dir: Path, overlay_csv: Path, out_dir: Path, *, expected_denominator: int = 868) -> dict[str, object]:
    overlay = _load_overlay(overlay_csv)
    paths = sorted(base_dir.glob("SCH_PRISMA_V2_SCREEN_BATCH_*.csv"))
    if not paths:
        raise ValueError("no generated screening batches found")
    out_dir.mkdir(parents=True, exist_ok=True)

    seen: set[str] = set()
    changed_ids: list[str] = []
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError(f"{path.name}: missing header")
            rows = [{k: (v or "").strip() for k, v in row.items()} for row in reader]
            fieldnames = list(reader.fieldnames)
        for row in rows:
            record_id = row["record_id"]
            seen.add(record_id)
            update = overlay.get(record_id)
            if not update:
                continue
            touched = False
            for field in FORMAL_FIELDS:
                value = update.get(field, "")
                if value:
                    row[field] = value
                    touched = True
            if touched:
                changed_ids.append(record_id)
        with (out_dir / path.name).open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    missing_overlay_ids = sorted(set(overlay) - seen)
    if missing_overlay_ids:
        raise ValueError(f"decision overlay contains unknown record IDs: {missing_overlay_ids[:5]}")

    receipt = audit_mod.audit(out_dir, expected_denominator=expected_denominator)
    return {
        "analysis_id": "sch_prisma_v2_decision_overlay_v1",
        "overlay_rows": len(overlay),
        "changed_record_count": len(set(changed_ids)),
        "changed_record_ids": sorted(set(changed_ids)),
        "screening_status": receipt["screening_status"],
        "prisma_flow": receipt["prisma_flow"],
        "claim_boundary": (
            "Only sparse version-controlled adjudications with decision_source are overlaid. "
            "Malformed CSV rows fail closed. The overlay never changes bibliographic identity "
            "or creates decisions from machine triage."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_batch_dir", type=Path)
    parser.add_argument("overlay_csv", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("out_receipt_json", type=Path)
    parser.add_argument("--expected-denominator", type=int, default=868)
    args = parser.parse_args(argv)
    receipt = apply(
        args.base_batch_dir,
        args.overlay_csv,
        args.out_dir,
        expected_denominator=args.expected_denominator,
    )
    args.out_receipt_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_receipt_json.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({"changed": receipt["changed_record_count"], "status": receipt["screening_status"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

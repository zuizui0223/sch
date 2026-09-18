"""Build the sign-independent SCH macroecology primary-study candidate universe.

This builder merges the frozen 868-record identification cohort with every
versioned PRISMA screening overlay. It exports every currently full-text
INCLUDE record. It deliberately does not classify conflict/alignment from the
existing evidence lane or notes: ecological outcomes remain pending a separate
source recode.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

VERSION_RE = re.compile(r"SCH_PRISMA_V2_SCREENING_DECISIONS_V(\d+)")

OUTPUT_FIELDS = [
    "record_id",
    "doi",
    "title",
    "year",
    "venue",
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
    "geometry_eligibility",
    "context_switch_eligibility",
    "cancellation_eligibility",
    "design_audit_eligible",
    "macro_cluster_id",
    "macro_context_cases_required",
    "macro_coding_status",
    "macro_coding_note",
]


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(handle)
        ]


def _version(path: Path) -> int:
    match = VERSION_RE.search(path.name)
    if not match:
        raise ValueError(f"cannot parse screening overlay version: {path.name}")
    return int(match.group(1))


def _merge_overlays(prisma_dir: Path) -> dict[str, dict[str, str]]:
    paths = sorted(
        prisma_dir.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"),
        key=_version,
    )
    versions = [_version(path) for path in paths]
    if versions != list(range(1, max(versions, default=0) + 1)):
        raise ValueError(f"screening overlay versions are not contiguous: {versions}")

    all_fields: set[str] = set()
    loaded: list[list[dict[str, str]]] = []
    for path in paths:
        rows = _read(path)
        loaded.append(rows)
        for row in rows:
            all_fields.update(row)

    merged: dict[str, dict[str, str]] = {}
    for rows in loaded:
        for update in rows:
            record_id = update.get("record_id", "")
            if not record_id:
                raise ValueError("screening overlay row lacks record_id")
            row = merged.setdefault(record_id, {field: "" for field in all_fields})
            for key, value in update.items():
                if value:
                    row[key] = value
    return merged


def _reported(value: str) -> bool:
    return bool(value) and value != "NOT_REPORTED"


def _positive_geo(value: str) -> bool:
    if not _reported(value):
        return False
    upper = value.upper()
    return not upper.startswith("NO_") and "NOT_GEOGRAPHIC" not in upper


def _positive_receiver(value: str) -> bool:
    return _reported(value) and not value.upper().startswith("NO_")


def build(frozen_path: Path, prisma_dir: Path) -> tuple[list[dict[str, str]], dict]:
    frozen = {row["record_id"]: row for row in _read(frozen_path)}
    overlays = _merge_overlays(prisma_dir)

    included: list[dict[str, str]] = []
    for record_id, update in overlays.items():
        if update.get("screen_fulltext") != "INCLUDE":
            continue
        if record_id not in frozen:
            raise ValueError(f"included record absent from frozen cohort: {record_id}")
        row = {**frozen[record_id], **update}
        row.update(
            {
                "geometry_eligibility": "PENDING_SOURCE_RECODE",
                "context_switch_eligibility": "PENDING_SOURCE_RECODE",
                "cancellation_eligibility": "PENDING_SOURCE_RECODE",
                "design_audit_eligible": "YES_CURRENT_FULLTEXT_INCLUDE",
                "macro_cluster_id": "",
                "macro_context_cases_required": "PENDING_SOURCE_RECODE",
                "macro_coding_status": "UNADJUDICATED",
                "macro_coding_note": "",
            }
        )
        included.append({field: row.get(field, "") for field in OUTPUT_FIELDS})

    included.sort(key=lambda row: row["record_id"])

    lanes: Counter[str] = Counter()
    for row in included:
        lanes.update(part for part in row["evidence_lanes"].split(";") if part)

    geo = [row for row in included if _positive_geo(row["geographic_contrast"])]
    receiver = [row for row in included if _positive_receiver(row["receiver_assemblage_contrast"])]
    receiver_ids = {row["record_id"] for row in receiver}

    receipt = {
        "analysis": "sch_macroecology_primary_candidate_universe_v1",
        "candidate_rule": "all_current_fulltext_INCLUDE_records_no_outcome_sign_filter",
        "n_primary_candidates": len(included),
        "evidence_lane_counts": dict(sorted(lanes.items())),
        "existing_structured_field_coverage": {
            "A_trait_reported": sum(_reported(row["A_trait"]) for row in included),
            "A_manipulated_reported": sum(_reported(row["A_manipulated"]) for row in included),
            "pollinator_response_measured_reported": sum(
                _reported(row["pollinator_response_measured"]) for row in included
            ),
            "antagonist_response_measured_reported": sum(
                _reported(row["antagonist_response_measured"]) for row in included
            ),
            "common_reproductive_outcome_reported": sum(
                _reported(row["common_reproductive_outcome"]) for row in included
            ),
        },
        "existing_geography_coverage": {
            "positive_geographic_contrast_records": len(geo),
            "positive_receiver_contrast_records": len(receiver),
            "joint_positive_records": sum(
                row["record_id"] in receiver_ids for row in geo
            ),
        },
        "macro_outcome_fields_populated": 0,
        "status": "PRIMARY_CANDIDATE_UNIVERSE_MATERIALIZABLE_MACRO_RECODE_PENDING",
        "claim_ceiling": [
            "candidate_universe_not_macro_design_eligible_universe_yet",
            "no_conflict_prevalence",
            "no_moderator_test_before_source_recode",
            "independence_clustering_required_before_model_fit",
        ],
    }
    return included, receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frozen", type=Path)
    parser.add_argument("prisma_dir", type=Path)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("out_json", type=Path)
    args = parser.parse_args()
    rows, receipt = build(args.frozen, args.prisma_dir)
    _write_csv(args.out_csv, rows)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

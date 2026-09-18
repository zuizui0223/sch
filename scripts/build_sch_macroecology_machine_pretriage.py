"""Build a sign-blind machine pretriage for the current SCH macroecology primary-study universe.

The pretriage uses only already-adjudicated study-design fields from the
versioned PRISMA overlays. It never reads selection_form, claim_ceiling,
decision_note, or any ecological outcome sign to prioritize studies.

This is a workflow accelerator, not a biological eligibility decision.
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
    "single_site_vs_multisite",
    "geographic_contrast",
    "receiver_assemblage_contrast",
    "paired_response_status",
    "trait_manipulation_status",
    "context_recode_priority",
    "manual_axis_recode_required",
    "machine_pretriage_status",
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
        raise ValueError(f"cannot parse overlay version from {path.name}")
    return int(match.group(1))


def _merge_overlays(prisma_dir: Path) -> dict[str, dict[str, str]]:
    paths = sorted(
        prisma_dir.glob("SCH_PRISMA_V2_SCREENING_DECISIONS_V*.csv"),
        key=_version,
    )
    versions = [_version(path) for path in paths]
    if versions != list(range(1, max(versions, default=0) + 1)):
        raise ValueError(f"screening overlays are not contiguous: {versions}")

    merged: dict[str, dict[str, str]] = {}
    all_fields: set[str] = set()
    loaded: list[list[dict[str, str]]] = []

    for path in paths:
        rows = _read(path)
        loaded.append(rows)
        for row in rows:
            all_fields.update(row)

    for rows in loaded:
        for update in rows:
            record_id = update.get("record_id", "")
            if not record_id:
                raise ValueError("overlay row lacks record_id")
            row = merged.setdefault(record_id, {field: "" for field in all_fields})
            for key, value in update.items():
                if value:
                    row[key] = value
    return merged


def _yes(value: str) -> bool:
    return value.upper().startswith("YES")


def _reported(value: str) -> bool:
    return bool(value) and value != "NOT_REPORTED"


def _positive_geo(value: str) -> bool:
    if not _reported(value):
        return False
    upper = value.upper()
    return not upper.startswith("NO_") and "NOT_GEOGRAPHIC" not in upper


def _positive_receiver(value: str) -> bool:
    return _reported(value) and not value.upper().startswith("NO_")


def _paired_response_status(row: dict[str, str]) -> str:
    pollinator = _yes(row.get("pollinator_response_measured", ""))
    antagonist = _yes(row.get("antagonist_response_measured", ""))
    common_fitness = _yes(row.get("common_reproductive_outcome", ""))

    if pollinator and antagonist and common_fitness:
        return "P1_BOTH_RESPONSES_COMMON_FITNESS"
    if pollinator and antagonist:
        return "P2_BOTH_RESPONSES_NO_COMMON_FITNESS"
    if pollinator:
        return "P3_POLLINATOR_ONLY"
    if antagonist:
        return "P3_ANTAGONIST_ONLY"
    return "P4_UNSTRUCTURED_OR_NEITHER"


def _trait_manipulation_status(row: dict[str, str]) -> str:
    value = row.get("A_manipulated", "")
    if _yes(value):
        return "DIRECT_TRAIT_MANIPULATION_REPORTED"
    if _reported(value):
        return "NON_DIRECT_OR_OBSERVATIONAL_TRAIT_STATE"
    return "NOT_REPORTED"


def _context_priority(row: dict[str, str]) -> str:
    if _positive_geo(row.get("geographic_contrast", "")):
        return "YES"
    if _positive_receiver(row.get("receiver_assemblage_contrast", "")):
        return "YES"
    if row.get("single_site_vs_multisite", "") in {"MULTISITE", "MULTIISLAND", "MULTISPECIES"}:
        return "YES"
    return "NO_OR_UNRESOLVED"


def _manual_axis_recode_required(row: dict[str, str]) -> str:
    trait = row.get("A_trait", "").lower()
    architecture = row.get("cue_architecture", "").lower()
    tokens = (
        " and ",
        "traits",
        "bundle",
        "multitrait",
        "multiple_",
        "morphology_and",
        "display_and",
        "phenology_",
    )
    return "YES" if any(token in trait or token in architecture for token in tokens) else "NO_OR_UNRESOLVED"


def build(
    frozen_path: Path,
    prisma_dir: Path,
) -> tuple[list[dict[str, str]], dict]:
    frozen = {row["record_id"]: row for row in _read(frozen_path)}
    overlays = _merge_overlays(prisma_dir)

    rows: list[dict[str, str]] = []
    for record_id, update in overlays.items():
        if update.get("screen_fulltext") != "INCLUDE":
            continue
        base = frozen.get(record_id)
        if base is None:
            raise ValueError(f"included record missing from frozen cohort: {record_id}")

        row = {**base, **update}
        row["paired_response_status"] = _paired_response_status(row)
        row["trait_manipulation_status"] = _trait_manipulation_status(row)
        row["context_recode_priority"] = _context_priority(row)
        row["manual_axis_recode_required"] = _manual_axis_recode_required(row)
        row["machine_pretriage_status"] = "DESIGN_ONLY_NOT_BIOLOGICAL_ELIGIBILITY"
        rows.append({field: row.get(field, "") for field in OUTPUT_FIELDS})

    rows.sort(key=lambda row: row["record_id"])

    lane_counts: Counter[str] = Counter()
    for row in rows:
        lane_counts.update(part for part in row["evidence_lanes"].split(";") if part)

    receipt = {
        "analysis": "sch_macroecology_machine_pretriage_v1",
        "n_current_primary_includes": len(rows),
        "paired_response_status_counts": dict(
            sorted(Counter(row["paired_response_status"] for row in rows).items())
        ),
        "trait_manipulation_status_counts": dict(
            sorted(Counter(row["trait_manipulation_status"] for row in rows).items())
        ),
        "context_recode_priority_counts": dict(
            sorted(Counter(row["context_recode_priority"] for row in rows).items())
        ),
        "manual_axis_recode_required_counts": dict(
            sorted(Counter(row["manual_axis_recode_required"] for row in rows).items())
        ),
        "evidence_lane_counts": dict(sorted(lane_counts.items())),
        "n_paired_response_records": sum(
            row["paired_response_status"].startswith(("P1_", "P2_")) for row in rows
        ),
        "n_paired_response_with_common_fitness": sum(
            row["paired_response_status"] == "P1_BOTH_RESPONSES_COMMON_FITNESS"
            for row in rows
        ),
        "n_paired_response_without_common_fitness": sum(
            row["paired_response_status"] == "P2_BOTH_RESPONSES_NO_COMMON_FITNESS"
            for row in rows
        ),
        "status": "MACHINE_PRETRIAGE_READY_HUMAN_SOURCE_RECODE_REQUIRED",
        "claim_ceiling": [
            "workflow_priority_only",
            "does_not_equal_geometry_eligibility",
            "does_not_read_selection_form_or_outcome_sign",
            "does_not_estimate_conflict_prevalence",
            "source_recode_required_before_H1_H4",
        ],
    }
    return rows, receipt


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
    args.out_json.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

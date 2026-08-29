"""Audit SCH PRISMA V2 screening decisions and derive flow counts.

The input is a directory of deterministic screening-batch CSVs. This script
validates allowed title/abstract and full-text decision codes, detects duplicate
or missing record IDs, checks reason/decision consistency, and emits a single
progress/PRISMA-flow receipt. It never infers a scientific decision from blank
fields.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
import re


TA_DECISIONS = {"", "RETAIN_FULLTEXT", "EXCLUDE"}
TA_EXCLUSION_REASONS = {
    "TA_NOT_FLORAL_SIGNAL",
    "TA_NO_POLLINATOR_COMPONENT",
    "TA_NO_ANTAGONIST_COMPONENT",
    "TA_NOT_PRIMARY_OR_RELEVANT_SYNTHESIS",
    "TA_NONBIOLOGICAL_OR_OFF_TOPIC",
}
FULLTEXT_STATUS = {"", "NOT_REQUESTED", "AVAILABLE", "UNAVAILABLE"}
FT_DECISIONS = {"", "INCLUDE", "EXCLUDE"}
FT_EXCLUSION_REASONS = {
    "FT_NO_DECLARED_FLORAL_COORDINATE",
    "FT_NO_POLLINATOR_EVIDENCE",
    "FT_NO_ANTAGONIST_EVIDENCE",
    "FT_NO_RELEVANT_OUTCOME_OR_EVOLUTIONARY_STATE",
    "FT_REVIEW_ONLY_NO_PRIMARY_ROLE",
    "FT_DUPLICATE_DATASET_OR_REPORT",
    "FT_FULLTEXT_UNAVAILABLE",
    "FT_OTHER_WITH_EXPLANATION",
}
EVIDENCE_LANES = {
    "STRICT_LINKED_EXPERIMENT",
    "DIRECTIONAL_OR_NEAR_PASS",
    "EVOLUTIONARY_OUTCOME",
    "HISTORICAL_TRANSITION",
}
RECORD_RE = re.compile(r"^SCHPRISMA-(\d{6})$")


def _read_batches(batch_dir: Path) -> list[dict[str, str]]:
    paths = sorted(batch_dir.glob("SCH_PRISMA_V2_SCREEN_BATCH_*.csv"))
    if not paths:
        raise ValueError("no SCH_PRISMA_V2_SCREEN_BATCH_*.csv files found")
    rows: list[dict[str, str]] = []
    header: list[str] | None = None
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError(f"{path.name} has no header")
            if header is None:
                header = list(reader.fieldnames)
            elif list(reader.fieldnames) != header:
                raise ValueError(f"batch header mismatch: {path.name}")
            rows.extend({key: (value or "").strip() for key, value in row.items()} for row in reader)
    return rows


def _validate_record_ids(rows: list[dict[str, str]], expected_denominator: int | None) -> None:
    ids = [row.get("record_id", "") for row in rows]
    if any(not RECORD_RE.match(record_id) for record_id in ids):
        raise ValueError("record_id must match SCHPRISMA-######")
    if len(ids) != len(set(ids)):
        duplicates = [key for key, count in Counter(ids).items() if count > 1]
        raise ValueError(f"duplicate record_id across batches: {duplicates[:5]}")
    numbers = sorted(int(RECORD_RE.match(record_id).group(1)) for record_id in ids)
    expected_numbers = list(range(1, len(rows) + 1))
    if numbers != expected_numbers:
        raise ValueError("screening batches do not contain one contiguous complete record_id sequence")
    if expected_denominator is not None and len(rows) != expected_denominator:
        raise ValueError(f"expected denominator {expected_denominator}, got {len(rows)}")


def _validate_title_abstract(row: dict[str, str]) -> None:
    decision = row.get("screen_title_abstract", "")
    reason = row.get("screen_title_abstract_reason", "")
    if decision not in TA_DECISIONS:
        raise ValueError(f"{row['record_id']}: invalid title/abstract decision {decision!r}")
    if decision == "EXCLUDE":
        if reason not in TA_EXCLUSION_REASONS:
            raise ValueError(f"{row['record_id']}: EXCLUDE requires one registered TA reason")
    elif reason:
        raise ValueError(f"{row['record_id']}: TA reason is only allowed when decision=EXCLUDE")


def _validate_fulltext(row: dict[str, str]) -> None:
    ta = row.get("screen_title_abstract", "")
    status = row.get("fulltext_status", "")
    decision = row.get("screen_fulltext", "")
    reason = row.get("screen_fulltext_reason", "")
    lanes = [value for value in row.get("evidence_lanes", "").split(";") if value]

    if status not in FULLTEXT_STATUS:
        raise ValueError(f"{row['record_id']}: invalid fulltext_status {status!r}")
    if decision not in FT_DECISIONS:
        raise ValueError(f"{row['record_id']}: invalid full-text decision {decision!r}")
    unknown_lanes = [lane for lane in lanes if lane not in EVIDENCE_LANES]
    if unknown_lanes:
        raise ValueError(f"{row['record_id']}: invalid evidence lanes {unknown_lanes}")

    if ta != "RETAIN_FULLTEXT":
        if status not in {"", "NOT_REQUESTED"} or decision or reason or lanes:
            raise ValueError(f"{row['record_id']}: full-text fields require RETAIN_FULLTEXT at TA stage")
        return

    if decision == "EXCLUDE":
        if reason not in FT_EXCLUSION_REASONS:
            raise ValueError(f"{row['record_id']}: full-text EXCLUDE requires one registered FT reason")
        if lanes:
            raise ValueError(f"{row['record_id']}: excluded full text cannot carry evidence_lanes")
    elif decision == "INCLUDE":
        if reason:
            raise ValueError(f"{row['record_id']}: included full text cannot have exclusion reason")
        if status != "AVAILABLE":
            raise ValueError(f"{row['record_id']}: included full text must be AVAILABLE")
        if not lanes:
            raise ValueError(f"{row['record_id']}: included full text requires at least one evidence_lane")
    else:
        if reason or lanes:
            raise ValueError(f"{row['record_id']}: undecided full text cannot carry reason/lanes")

    if status == "UNAVAILABLE" and decision not in {"", "EXCLUDE"}:
        raise ValueError(f"{row['record_id']}: unavailable full text cannot be included")
    if status == "UNAVAILABLE" and decision == "EXCLUDE" and reason != "FT_FULLTEXT_UNAVAILABLE":
        raise ValueError(f"{row['record_id']}: unavailable full text must use FT_FULLTEXT_UNAVAILABLE")


def _geography_counts(rows: list[dict[str, str]]) -> dict[str, int]:
    included = [row for row in rows if row.get("screen_fulltext") == "INCLUDE"]
    def reported(field: str) -> int:
        return sum(row.get(field, "") not in {"", "NOT_REPORTED"} for row in included)
    return {
        "included_fulltexts": len(included),
        "study_region_reported": reported("study_region"),
        "geographic_contrast_reported": reported("geographic_contrast"),
        "receiver_assemblage_contrast_reported": reported("receiver_assemblage_contrast"),
        "biogeographic_context_reported": reported("biogeographic_context"),
        "historical_or_phylogenetic_context_reported": reported("historical_or_phylogenetic_context"),
    }


def audit(batch_dir: Path, *, expected_denominator: int | None = 868) -> dict[str, object]:
    rows = _read_batches(batch_dir)
    _validate_record_ids(rows, expected_denominator)
    for row in rows:
        _validate_title_abstract(row)
        _validate_fulltext(row)

    ta_counts = Counter(row.get("screen_title_abstract", "") or "UNSCREENED" for row in rows)
    ft_eligible = [row for row in rows if row.get("screen_title_abstract") == "RETAIN_FULLTEXT"]
    ft_counts = Counter(row.get("screen_fulltext", "") or "UNSCREENED" for row in ft_eligible)
    ta_reason_counts = Counter(
        row["screen_title_abstract_reason"] for row in rows if row.get("screen_title_abstract") == "EXCLUDE"
    )
    ft_reason_counts = Counter(
        row["screen_fulltext_reason"] for row in ft_eligible if row.get("screen_fulltext") == "EXCLUDE"
    )
    lane_counts: Counter[str] = Counter()
    for row in ft_eligible:
        if row.get("screen_fulltext") == "INCLUDE":
            lane_counts.update(value for value in row.get("evidence_lanes", "").split(";") if value)

    ta_decided = ta_counts["RETAIN_FULLTEXT"] + ta_counts["EXCLUDE"]
    ft_decided = ft_counts["INCLUDE"] + ft_counts["EXCLUDE"]
    if ta_decided == 0:
        status = "TITLE_ABSTRACT_NOT_STARTED"
    elif ta_decided < len(rows):
        status = "TITLE_ABSTRACT_IN_PROGRESS"
    elif ft_decided < len(ft_eligible):
        status = "FULLTEXT_IN_PROGRESS"
    else:
        status = "SCREENING_COMPLETE"

    return {
        "analysis_id": "sch_prisma_v2_screening_audit_v1",
        "identified_records": len(rows),
        "title_abstract": {
            "retained_for_fulltext": ta_counts["RETAIN_FULLTEXT"],
            "excluded": ta_counts["EXCLUDE"],
            "unscreened": ta_counts["UNSCREENED"],
            "reason_counts": dict(sorted(ta_reason_counts.items())),
        },
        "fulltext": {
            "eligible_after_title_abstract": len(ft_eligible),
            "included": ft_counts["INCLUDE"],
            "excluded": ft_counts["EXCLUDE"],
            "unscreened": ft_counts["UNSCREENED"],
            "reason_counts": dict(sorted(ft_reason_counts.items())),
        },
        "evidence_lane_counts": dict(sorted(lane_counts.items())),
        "geography": _geography_counts(rows),
        "screening_status": status,
        "prisma_flow": {
            "records_identified_after_deduplication": len(rows),
            "records_screened_title_abstract": ta_decided,
            "records_excluded_title_abstract": ta_counts["EXCLUDE"],
            "reports_sought_for_retrieval": ta_counts["RETAIN_FULLTEXT"],
            "reports_assessed_for_eligibility": ft_decided,
            "reports_excluded_fulltext": ft_counts["EXCLUDE"],
            "studies_included": ft_counts["INCLUDE"],
        },
        "claim_boundary": (
            "Counts are valid only for protocol-coded decisions present in the batch files. "
            "UNSCREENED is not an exclusion. Screening completion does not itself authorize pooling; outcome-scale and independence gates remain separate."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch_dir", type=Path)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("--expected-denominator", type=int, default=868)
    args = parser.parse_args(argv)
    receipt = audit(args.batch_dir, expected_denominator=args.expected_denominator)
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps({"status": receipt["screening_status"], "identified": receipt["identified_records"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

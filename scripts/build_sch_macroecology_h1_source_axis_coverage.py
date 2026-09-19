from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

H1_STATUSES = {"ELIGIBLE_SAME_COORDINATE", "ELIGIBLE_BOUNDED_COORDINATE"}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def build(design_paths: list[Path], axis_paths: list[Path]) -> dict:
    design_rows: list[dict[str, str]] = []
    for path in design_paths:
        design_rows.extend(_read(path))

    h1_records = {
        row["record_id"]
        for row in design_rows
        if row["geometry_eligibility"] in H1_STATUSES
    }

    axis_rows: list[dict[str, str]] = []
    for path in axis_paths:
        axis_rows.extend(_read(path))

    represented = {row["source_id"] for row in axis_rows}
    covered = h1_records & represented
    missing = sorted(h1_records - represented)

    source_downgraded = {
        row["source_id"]
        for row in axis_rows
        if row["source_id"] in h1_records
        and row.get("coding_status", "").startswith("SOURCE_DOWNGRADED")
    }

    source_ids_with_model_axis = {
        row["source_id"]
        for row in axis_rows
        if row["source_id"] in h1_records
        and not row.get("geometry_eligibility", "").startswith("INELIGIBLE_")
    }

    return {
        "analysis": "sch_macroecology_h1_source_axis_coverage_v1",
        "n_record_level_h1_candidates": len(h1_records),
        "n_h1_candidates_with_source_axis_record": len(covered),
        "n_h1_candidates_missing_source_axis_record": len(missing),
        "missing_h1_record_ids": missing,
        "n_h1_source_records_with_model_axis": len(source_ids_with_model_axis),
        "n_h1_source_records_downgraded_after_source_audit": len(source_downgraded),
        "downgraded_h1_record_ids": sorted(source_downgraded),
        "n_source_axis_records_total": len(axis_rows),
        "n_source_axis_records_from_h1_candidate_records": sum(
            row["source_id"] in h1_records for row in axis_rows
        ),
        "status": (
            "ALL_RECORD_LEVEL_H1_CANDIDATES_SOURCE_AXIS_RECODED"
            if not missing
            else "H1_SOURCE_AXIS_RECODE_INCOMPLETE"
        ),
        "claim_ceiling": [
            "source_axis_coverage_complete_does_not_mean_outcome_resolution_complete",
            "record_level_h1_candidate_count_is_not_independent_axis_count",
            "canonicalization_required_before_modeling",
            "unresolved_axes_remain_missing_outcomes_not_negative_outcomes",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", type=Path, nargs="+", required=True)
    parser.add_argument("--axes", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.design, args.axes)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

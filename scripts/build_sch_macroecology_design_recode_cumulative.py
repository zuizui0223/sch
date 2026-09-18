from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def _count(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows).items()))


def build(paths: list[Path]) -> dict:
    rows: list[dict[str, str]] = []
    for path in paths:
        batch = _read(path)
        for row in batch:
            row["_batch_file"] = path.name
        rows.extend(batch)

    record_ids = [row["record_id"] for row in rows]
    if len(record_ids) != len(set(record_ids)):
        duplicates = sorted(r for r, n in Counter(record_ids).items() if n > 1)
        raise ValueError("record_id occurs in multiple recode batches: " + ", ".join(duplicates))

    geometry_eligible = [
        row for row in rows
        if row["geometry_eligibility"] in {
            "ELIGIBLE_SAME_COORDINATE",
            "ELIGIBLE_BOUNDED_COORDINATE",
        }
    ]

    return {
        "analysis": "sch_macroecology_design_recode_cumulative_v1",
        "n_batches": len(paths),
        "batch_files": [path.name for path in paths],
        "n_records": len(rows),
        "n_design_audit_eligible": sum(row["design_audit_eligible"] == "YES" for row in rows),
        "n_geometry_eligible": len(geometry_eligible),
        "geometry_eligibility_counts": _count(rows, "geometry_eligibility"),
        "context_switch_eligibility_counts": _count(rows, "context_switch_eligibility"),
        "cancellation_eligibility_counts": _count(rows, "cancellation_eligibility"),
        "trait_axis_action_counts": _count(rows, "trait_axis_action"),
        "outcome_coding_status_counts": _count(rows, "outcome_coding_status"),
        "n_context_switch_eligible": sum(
            row["context_switch_eligibility"] == "ELIGIBLE_MULTI_CONTEXT" for row in rows
        ),
        "n_outcomes_coded_in_design_batches": 0,
        "status": "CUMULATIVE_DESIGN_FRONTIER_DESCRIPTIVE_ONLY",
        "claim_ceiling": [
            "recode_batches_are_not_final_systematic_denominator",
            "design_gap_counts_not_natural_frequencies",
            "no_ecological_outcome_sign_used_for_eligibility",
            "all_recoded_records_retained_for_H4",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_paths", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.csv_paths)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

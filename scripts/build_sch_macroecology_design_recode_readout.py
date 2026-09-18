from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

REQUIRED = {
    "record_id",
    "geometry_eligibility",
    "context_switch_eligibility",
    "cancellation_eligibility",
    "design_audit_eligible",
    "trait_axis_action",
    "source_verification_state",
    "eligibility_rationale",
    "outcome_coding_status",
}


def _count(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows).items()))


def build(path: Path) -> dict:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or ())
        missing = sorted(REQUIRED - fields)
        if missing:
            raise ValueError("missing required columns: " + ", ".join(missing))
        rows = [{k: (v or "").strip() for k, v in row.items()} for row in reader]

    if len(rows) != len({row["record_id"] for row in rows}):
        raise ValueError("record_id must be unique in a design recode batch")

    forbidden = {
        "conflict_detected",
        "alignment_detected",
        "context_shift_detected",
        "compromise_detected",
        "cancellation_detected",
    }
    if forbidden & fields:
        raise ValueError("design-only recode must not contain ecological outcome fields")

    return {
        "analysis": "sch_macroecology_design_recode_batch1_v1",
        "n_records": len(rows),
        "geometry_eligibility_counts": _count(rows, "geometry_eligibility"),
        "context_switch_eligibility_counts": _count(rows, "context_switch_eligibility"),
        "cancellation_eligibility_counts": _count(rows, "cancellation_eligibility"),
        "design_audit_eligible_counts": _count(rows, "design_audit_eligible"),
        "trait_axis_action_counts": _count(rows, "trait_axis_action"),
        "outcome_coding_status_counts": _count(rows, "outcome_coding_status"),
        "n_geometry_eligible": sum(
            row["geometry_eligibility"] in {"ELIGIBLE_SAME_COORDINATE", "ELIGIBLE_BOUNDED_COORDINATE"}
            for row in rows
        ),
        "n_outcomes_coded": 0,
        "status": "DESIGN_RECODE_FROZEN_OUTCOME_BLIND",
        "claim_ceiling": [
            "design_eligibility_only",
            "no_conflict_or_alignment_result_yet",
            "not_final_macro_denominator",
            "trait_axis_recode_required_before_outcome_coding",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.csv_path)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

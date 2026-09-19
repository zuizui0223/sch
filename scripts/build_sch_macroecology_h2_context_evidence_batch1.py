from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

ALLOWED_RESOLUTION = {
    "LOCAL_CONTEXT_GEOMETRY_RESOLVED",
    "LOCAL_CONTEXT_TABLE_REQUIRED",
    "CONTEXT_STRUCTURE_RESOLVED_LOCAL_OUTCOMES_PENDING",
    "LOCAL_CONTEXT_SOURCE_EXTRACTION_REQUIRED",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def build(evidence_path: Path, case_path: Path) -> dict:
    evidence = _read(evidence_path)
    cases = _read(case_path)

    if len({row["evidence_id"] for row in evidence}) != len(evidence):
        raise ValueError("evidence_id must be unique")
    if len({row["case_id"] for row in cases}) != len(cases):
        raise ValueError("case_id must be unique")

    invalid = sorted({
        row["local_case_resolution"]
        for row in evidence
        if row["local_case_resolution"] not in ALLOWED_RESOLUTION
    })
    if invalid:
        raise ValueError("invalid local_case_resolution: " + ", ".join(invalid))

    declared_materialized = sum(int(row["local_cases_materialized"]) for row in evidence)
    if declared_materialized != len(cases):
        raise ValueError(
            f"declared materialized cases {declared_materialized} != actual case rows {len(cases)}"
        )

    evidence_axes = {row["canonical_trait_axis_id"] for row in evidence}
    case_axes = {row["canonical_trait_axis_id"] for row in cases}
    if not case_axes <= evidence_axes:
        raise ValueError("context case exists without Batch-1 evidence row")

    return {
        "analysis": "sch_macroecology_h2_context_evidence_batch1_v1",
        "n_context_evidence_rows": len(evidence),
        "n_canonical_axes_with_evidence": len(evidence_axes),
        "n_source_records": len({row["source_id"] for row in evidence}),
        "local_case_resolution_counts": dict(
            sorted(Counter(row["local_case_resolution"] for row in evidence).items())
        ),
        "n_local_context_cases_materialized": len(cases),
        "materialized_case_ids": sorted(row["case_id"] for row in cases),
        "materialized_canonical_axes": sorted(case_axes),
        "n_evidence_rows_requiring_source_object": sum(
            row["source_object_required"] != "NONE" for row in evidence
        ),
        "n_context_evidence_rows_not_yet_model_cases": sum(
            int(row["local_cases_materialized"]) == 0 for row in evidence
        ),
        "h2_model_ready": False,
        "status": "H2_CONTEXT_EVIDENCE_BATCH1_READY_LOCAL_CASES_FAIL_CLOSED",
        "claim_ceiling": [
            "reported_context_count_is_not_model_case_count",
            "one_source_resolved_local_case_is_materialized",
            "factorial_or_geographic_context_structure_does_not_license_local_outcomes",
            "source_tables_required_before_population_or_treatment_case_expansion",
            "H2_model_not_ready",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("cases", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.evidence, args.cases)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

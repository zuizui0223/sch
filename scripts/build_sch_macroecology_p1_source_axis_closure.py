from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


H1_ELIGIBLE = {"ELIGIBLE_SAME_COORDINATE", "ELIGIBLE_BOUNDED_COORDINATE"}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def build(design_paths: list[Path], trait_paths: list[Path]) -> dict:
    design_rows: list[dict[str, str]] = []
    for path in design_paths:
        design_rows.extend(_read(path))

    h1_candidates = {
        row["record_id"]
        for row in design_rows
        if row["geometry_eligibility"] in H1_ELIGIBLE
    }

    trait_rows: list[dict[str, str]] = []
    for path in trait_paths:
        trait_rows.extend(_read(path))

    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in trait_rows:
        by_source[row["source_id"]].append(row)

    represented = h1_candidates & set(by_source)
    missing = sorted(h1_candidates - represented)
    extra = sorted(set(by_source) - h1_candidates)

    if missing:
        raise ValueError(f"H1 candidate records missing source-axis recode: {missing}")
    if extra:
        raise ValueError(f"source-axis recode contains non-H1 design candidates: {extra}")

    fate_counts: Counter[str] = Counter()
    fully_downgraded: list[str] = []
    role_boundary_only: list[str] = []

    for source_id in sorted(h1_candidates):
        rows = by_source[source_id]
        model_rows = [
            row
            for row in rows
            if not row["geometry_eligibility"].startswith("INELIGIBLE_")
        ]
        fixed = [
            row
            for row in model_rows
            if row["antagonist_role_status"] == "NET_ANTAGONISTIC"
        ]
        boundary = [
            row
            for row in model_rows
            if row["antagonist_role_status"] != "NET_ANTAGONISTIC"
        ]

        if not model_rows:
            fate = "FULLY_DOWNGRADED"
            fully_downgraded.append(source_id)
        elif fixed:
            fate = "RETAINS_FIXED_ROLE_AXIS"
        elif boundary:
            fate = "ROLE_BOUNDARY_ONLY"
            role_boundary_only.append(source_id)
        else:
            raise ValueError(f"unclassifiable source fate: {source_id}")
        fate_counts[fate] += 1

    return {
        "analysis": "sch_macroecology_p1_source_axis_closure_v1",
        "n_h1_record_level_candidates": len(h1_candidates),
        "n_h1_candidates_source_axis_recoded": len(represented),
        "n_h1_candidates_missing_source_axis_recode": len(missing),
        "n_source_axis_records": len(trait_rows),
        "n_model_eligible_or_boundary_source_axes": sum(
            not row["geometry_eligibility"].startswith("INELIGIBLE_")
            for row in trait_rows
        ),
        "source_fate_counts": dict(sorted(fate_counts.items())),
        "fully_downgraded_source_ids": fully_downgraded,
        "role_boundary_only_source_ids": role_boundary_only,
        "status": "ALL_H1_RECORD_CANDIDATES_SOURCE_AUDITED",
        "claim_ceiling": [
            "record_level_H1_candidate_audit_complete",
            "source_axis_rows_are_not_independent_axes",
            "canonicalization_required_before_modeling",
            "fully_downgraded_sources_remain_H4_evidence",
            "not_prevalence",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--design", nargs="+", type=Path, required=True)
    parser.add_argument("--traits", nargs="+", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.design, args.traits)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

FIXED_ROLE = "NET_ANTAGONISTIC"


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def _source_geometry(row: dict[str, str]) -> str:
    if row["antagonist_role_status"] != FIXED_ROLE:
        return "ROLE_BOUNDARY"
    labels = {
        "CONFLICT": row["conflict_detected"],
        "ALIGNMENT_REINFORCEMENT": row["alignment_detected"],
        "ONE_SIDED_OR_NULL": row["one_sided_or_null_detected"],
    }
    yes = [name for name, value in labels.items() if value == "YES"]
    if len(yes) > 1:
        raise ValueError(f"geometry collision for {row['trait_axis_id']}")
    return yes[0] if yes else "UNRESOLVED"


def build(batch_paths: list[Path], override_path: Path) -> dict:
    rows: list[dict[str, str]] = []
    for path in batch_paths:
        rows.extend(_read(path))

    overrides = {
        row["source_trait_axis_id"]: row
        for row in _read(override_path)
    }

    source_ids = {row["trait_axis_id"] for row in rows}
    # Overrides may include axes added in later source batches. Historical partial
    # rebuilds ignore those entries; the complete-current build tests all active
    # overrides because every current source axis is present there.

    excluded = [
        row for row in rows
        if row.get("geometry_eligibility", "").startswith("INELIGIBLE_")
    ]
    model_rows = [row for row in rows if row not in excluded]

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in model_rows:
        override = overrides.get(row["trait_axis_id"])
        canonical = (
            override["canonical_trait_axis_id"]
            if override
            else row["trait_axis_id"]
        )
        grouped[canonical].append(row)

    canonical_geometry: Counter[str] = Counter()
    multi_source_axes: list[str] = []
    context_variable_axes: list[str] = []
    fixed_canonical = 0
    fixed_resolved = 0
    boundary_canonical = 0

    for canonical, members in grouped.items():
        if len(members) > 1:
            multi_source_axes.append(canonical)

        role_states = {row["antagonist_role_status"] for row in members}
        if role_states == {FIXED_ROLE}:
            fixed_canonical += 1
            classes = {
                _source_geometry(row)
                for row in members
                if _source_geometry(row) != "UNRESOLVED"
            }
            if len(classes) == 0:
                canonical_geometry["UNRESOLVED"] += 1
            elif len(classes) == 1:
                fixed_resolved += 1
                canonical_geometry[next(iter(classes))] += 1
            else:
                fixed_resolved += 1
                canonical_geometry["CONTEXT_VARIABLE"] += 1
                context_variable_axes.append(canonical)
        else:
            boundary_canonical += 1
            canonical_geometry["ROLE_BOUNDARY"] += 1

    return {
        "analysis": "sch_macroecology_canonical_trait_axis_v1",
        "n_source_axis_records": len(rows),
        "n_model_axis_source_records": len(model_rows),
        "n_source_records_excluded_before_canonical_axis": len(excluded),
        "excluded_source_axis_ids": sorted(row["trait_axis_id"] for row in excluded),
        "n_canonical_trait_axes": len(grouped),
        "n_axes_with_multiple_source_records": len(multi_source_axes),
        "multi_source_canonical_axes": sorted(multi_source_axes),
        "n_fixed_role_canonical_axes": fixed_canonical,
        "n_role_boundary_canonical_axes": boundary_canonical,
        "n_fixed_role_resolved_canonical_axes": fixed_resolved,
        "canonical_geometry_counts": dict(sorted(canonical_geometry.items())),
        "n_context_variable_canonical_axes": len(context_variable_axes),
        "context_variable_canonical_axes": sorted(context_variable_axes),
        "status": "CANONICAL_AXIS_LAYER_READY_INFERENCE_CLOSED",
        "claim_ceiling": [
            "source_axis_records_are_not_independent_trait_axes",
            "source_records_failing_geometry_eligibility_are_not_model_trait_axes",
            "cross_source_same_axis_records_are_collapsed_before_modeling",
            "context_variable_axes_are_not_forced_into_one_static_geometry",
            "not_prevalence",
            "full_systematic_recode_required_before_macro_model",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_csvs", type=Path, nargs="+")
    parser.add_argument("--overrides", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.batch_csvs, args.overrides)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


TRI = {"YES", "NO", "UNRESOLVED"}


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
        rows.extend(_read(path))

    ids = [row["trait_axis_id"] for row in rows]
    if len(ids) != len(set(ids)):
        duplicates = sorted(k for k, n in Counter(ids).items() if n > 1)
        raise ValueError("duplicate trait_axis_id across batches: " + ", ".join(duplicates))

    for field in (
        "conflict_detected",
        "alignment_detected",
        "one_sided_or_null_detected",
        "context_shift_detected",
        "compromise_detected",
        "cancellation_detected",
    ):
        invalid = sorted({row[field] for row in rows if row[field] not in TRI})
        if invalid:
            raise ValueError(f"{field} invalid: {invalid}")

    fixed = [row for row in rows if row["antagonist_role_status"] == "NET_ANTAGONISTIC"]
    resolved = []
    geometry_counts: Counter[str] = Counter()
    for row in fixed:
        labels = {
            "CONFLICT": row["conflict_detected"],
            "ALIGNMENT_REINFORCEMENT": row["alignment_detected"],
            "ONE_SIDED_OR_NULL": row["one_sided_or_null_detected"],
        }
        yes = [name for name, value in labels.items() if value == "YES"]
        if len(yes) > 1:
            raise ValueError(f"fixed-role geometry collision: {row['trait_axis_id']}")
        if len(yes) == 1:
            resolved.append(row)
            geometry_counts[yes[0]] += 1

    boundary = [row for row in rows if row["antagonist_role_status"] != "NET_ANTAGONISTIC"]
    boundary_clusters = {row["cluster_id"] for row in boundary}

    return {
        "analysis": "sch_macroecology_trait_axis_cumulative_v1",
        "n_batches": len(paths),
        "batch_files": [path.name for path in paths],
        "n_trait_axes": len(rows),
        "n_source_records": len({row["source_id"] for row in rows}),
        "n_biological_clusters": len({row["cluster_id"] for row in rows}),
        "conflict_detected_counts": _count(rows, "conflict_detected"),
        "alignment_detected_counts": _count(rows, "alignment_detected"),
        "one_sided_or_null_detected_counts": _count(rows, "one_sided_or_null_detected"),
        "context_shift_detected_counts": _count(rows, "context_shift_detected"),
        "compromise_detected_counts": _count(rows, "compromise_detected"),
        "cancellation_detected_counts": _count(rows, "cancellation_detected"),
        "antagonist_role_status_counts": _count(rows, "antagonist_role_status"),
        "coding_status_counts": _count(rows, "coding_status"),
        "n_fixed_role_axes": len(fixed),
        "n_fixed_role_geometry_resolved_axes": len(resolved),
        "n_fixed_role_geometry_resolved_clusters": len({row["cluster_id"] for row in resolved}),
        "resolved_fixed_role_geometry_counts": dict(sorted(geometry_counts.items())),
        "n_resolved_fixed_role_axes_with_context_shift": sum(
            row["context_shift_detected"] == "YES" for row in resolved
        ),
        "n_resolved_fixed_role_axes_with_cancellation": sum(
            row["cancellation_detected"] == "YES" for row in resolved
        ),
        "n_consumer_role_boundary_axes": len(boundary),
        "n_consumer_role_boundary_clusters": len(boundary_clusters),
        "consumer_role_boundary_axis_counts": {
            key: value
            for key, value in _count(boundary, "antagonist_role_status").items()
        },
        "status": "CUMULATIVE_TRAIT_AXIS_DESCRIPTIVE_PATTERN_READY_INFERENCE_CLOSED",
        "claim_ceiling": [
            "trait_axis_patterns_are_staged_descriptive_results",
            "not_prevalence",
            "fixed_role_and_role_boundary_strata_kept_separate",
            "unresolved_axes_retained",
            "full_systematic_recode_required_before_macro_model",
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

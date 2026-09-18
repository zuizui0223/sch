from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

REQUIRED = {
    "trait_axis_id",
    "cluster_id",
    "source_id",
    "trait_coordinate",
    "conflict_detected",
    "alignment_detected",
    "one_sided_or_null_detected",
    "context_shift_detected",
    "compromise_detected",
    "cancellation_detected",
    "antagonist_role_status",
    "geometry_eligibility",
    "coding_status",
}

TRI = {"YES", "NO", "UNRESOLVED"}


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

    if len(rows) != len({row["trait_axis_id"] for row in rows}):
        raise ValueError("trait_axis_id must be unique")

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
            raise ValueError(f"{field} has invalid values: {invalid}")

    fixed_role = [row for row in rows if row["antagonist_role_status"] == "NET_ANTAGONISTIC"]
    resolved_geometry = []
    for row in fixed_role:
        outcomes = [
            row["conflict_detected"],
            row["alignment_detected"],
            row["one_sided_or_null_detected"],
        ]
        n_yes = outcomes.count("YES")
        if n_yes > 1:
            raise ValueError(f"mutually exclusive geometry labels collide: {row['trait_axis_id']}")
        if n_yes == 1:
            resolved_geometry.append(row)

    geometry_class = Counter()
    for row in resolved_geometry:
        if row["conflict_detected"] == "YES":
            geometry_class["CONFLICT"] += 1
        elif row["alignment_detected"] == "YES":
            geometry_class["ALIGNMENT_REINFORCEMENT"] += 1
        else:
            geometry_class["ONE_SIDED_OR_NULL"] += 1

    resolved_cluster_ids = {row["cluster_id"] for row in resolved_geometry}

    return {
        "analysis": "sch_macroecology_trait_axis_recode_batch1_v1",
        "n_trait_axes": len(rows),
        "n_biological_clusters": len({row["cluster_id"] for row in rows}),
        "n_source_records": len({row["source_id"] for row in rows}),
        "conflict_detected_counts": _count(rows, "conflict_detected"),
        "alignment_detected_counts": _count(rows, "alignment_detected"),
        "one_sided_or_null_detected_counts": _count(rows, "one_sided_or_null_detected"),
        "context_shift_detected_counts": _count(rows, "context_shift_detected"),
        "compromise_detected_counts": _count(rows, "compromise_detected"),
        "cancellation_detected_counts": _count(rows, "cancellation_detected"),
        "antagonist_role_status_counts": _count(rows, "antagonist_role_status"),
        "coding_status_counts": _count(rows, "coding_status"),
        "n_fixed_role_geometry_resolved_axes": len(resolved_geometry),
        "n_fixed_role_geometry_resolved_clusters": len(resolved_cluster_ids),
        "resolved_fixed_role_geometry_counts": dict(sorted(geometry_class.items())),
        "n_resolved_axes_with_context_shift": sum(
            row["context_shift_detected"] == "YES" for row in resolved_geometry
        ),
        "n_resolved_axes_with_cancellation": sum(
            row["cancellation_detected"] == "YES" for row in resolved_geometry
        ),
        "n_role_dependent_boundary_axes": sum(
            row["antagonist_role_status"] == "ROLE_DEPENDENT" for row in rows
        ),
        "status": "TRAIT_AXIS_BATCH1_DESCRIPTIVE_RESULT_READY_NOT_INFERENTIAL_MACRO_SAMPLE",
        "claim_ceiling": [
            "batch1_descriptive_ecological_geometry_only",
            "not_prevalence",
            "not_H1_moderator_test",
            "cluster_dependence_not_ignored",
            "unresolved_axes_retained",
            "full_frozen_screen_required_before_inference",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.ledger)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

MIN_MULTINOMIAL_CLASS_CLUSTERS = 5


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def build(path: Path) -> dict:
    rows = _read(path)
    h1 = [row for row in rows if row["h1_static_eligible"] == "YES"]

    geometry = {}
    for label in ("CONFLICT", "ALIGNMENT_REINFORCEMENT", "ONE_SIDED_OR_NULL"):
        subset = [row for row in h1 if row["canonical_geometry"] == label]
        geometry[label] = {
            "axes": len(subset),
            "clusters": len({row["cluster_id"] for row in subset}),
        }

    min_class_clusters = min(value["clusters"] for value in geometry.values())
    h1_clusters = len({row["cluster_id"] for row in h1})
    h2 = [row for row in rows if row["h2_context_priority"] == "YES"]
    cancellation = [row for row in rows if row["cancellation_detected"] == "YES"]

    unresolved = [row for row in rows if row["canonical_geometry"] == "UNRESOLVED"]
    role_boundary = [row for row in rows if row["canonical_geometry"] == "ROLE_BOUNDARY"]
    context_variable = [row for row in rows if row["canonical_geometry"] == "CONTEXT_VARIABLE"]

    return {
        "analysis": "sch_macroecology_premodel_gate_v1",
        "h1_static": {
            "axes": len(h1),
            "clusters": h1_clusters,
            "geometry_support": geometry,
            "multinomial_minimum_class_clusters_required": MIN_MULTINOMIAL_CLASS_CLUSTERS,
            "minimum_observed_class_clusters": min_class_clusters,
            "multinomial_status": (
                "OPEN"
                if min_class_clusters >= MIN_MULTINOMIAL_CLASS_CLUSTERS
                else "FAIL_CLOSED_SPARSE_OUTCOME_CLASS"
            ),
            "binary_conflict_vs_other_status": "EXPLORATORY_ONLY_SYSTEMATIC_RECODE_INCOMPLETE",
        },
        "h2_context": {
            "priority_axes": len(h2),
            "priority_clusters": len({row["cluster_id"] for row in h2}),
            "context_case_table_status": "NOT_MATERIALIZED",
            "model_status": "FAIL_CLOSED_CONTEXT_CASE_DECOMPOSITION_REQUIRED",
        },
        "h3_cancellation": {
            "directional_cancellation_axes": len(cancellation),
            "model_status": "FAIL_CLOSED_NUMERIC_COMPONENT_AND_COVARIANCE_RECOVERY_REQUIRED",
        },
        "h4_design": {
            "current_primary_study_universe": 117,
            "status": "CURRENT_117_DESCRIPTIVE_READY_FINAL_SYSTEMATIC_INFERENCE_CLOSED",
        },
        "remaining_structure": {
            "unresolved_canonical_axes": len(unresolved),
            "unresolved_clusters": len({row["cluster_id"] for row in unresolved}),
            "role_boundary_axes": len(role_boundary),
            "role_boundary_clusters": len({row["cluster_id"] for row in role_boundary}),
            "context_variable_axes": len(context_variable),
        },
        "next_actions": [
            "resolve_high_information_unresolved_canonical_axes",
            "materialize_context_cases_for_H2_priority_axes",
            "recover_numeric_component_effects_and_covariance_for_H3",
            "complete_frozen_systematic_screen_before_final_macro_inference",
        ],
        "status": "PREMODEL_GATE_FROZEN_NO_FORCED_MODEL",
        "claim_ceiling": [
            "no_multinomial_H1_fit_under_sparse_alignment_support",
            "binary_H1_is_exploratory_only",
            "H2_requires_context_case_denominator",
            "H3_requires_numeric_component_uncertainty",
            "H4_final_frequency_waits_for_systematic_screen_completion",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical_table", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.canonical_table)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

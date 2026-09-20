from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for row in reader:
            if None in row:
                raise ValueError(f"CSV row has more fields than header in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def _local_context_class(row: dict[str, str]) -> str:
    yes = []
    if row["conflict_detected"] == "YES":
        yes.append("CONFLICT")
    if row["alignment_detected"] == "YES":
        yes.append("ALIGNMENT_REINFORCEMENT")
    if row["one_sided_or_null_detected"] == "YES":
        yes.append("ONE_SIDED_OR_NULL")
    if len(yes) > 1:
        raise ValueError(f"local geometry collision: {row['case_id']}")
    if yes:
        return yes[0]
    if row["function_2_direction_or_optimum"] == "REMOVED_BY_EXCLUSION":
        return "CONSUMER_REMOVED_NO_STATIC_GEOMETRY"
    if row["antagonist_role_status"] != "NET_ANTAGONISTIC":
        return "ROLE_BEHAVIOR_CONTEXT"
    if (
        row["effect_metric"] == "PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA"
        and row["effect_1"]
    ):
        return "LOCAL_NET_SELECTION"
    return "UNRESOLVED"


def build(evidence_paths: list[Path], case_paths: list[Path]) -> dict:
    evidence: list[dict[str, str]] = []
    for path in evidence_paths:
        evidence.extend(_read(path))

    cases: list[dict[str, str]] = []
    for path in case_paths:
        cases.extend(_read(path))

    evidence_ids = [row["evidence_id"] for row in evidence]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("duplicate H2 evidence_id across batches")
    case_ids = [row["case_id"] for row in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("duplicate H2 case_id across batches")

    evidence_axes = {row["canonical_trait_axis_id"] for row in evidence}
    if not {row["canonical_trait_axis_id"] for row in cases} <= evidence_axes:
        raise ValueError("materialized case lacks context-evidence provenance")

    declared = sum(int(row["local_cases_materialized"]) for row in evidence)
    if declared != len(cases):
        raise ValueError(
            f"declared local cases {declared} != materialized case rows {len(cases)}"
        )

    classes = Counter(_local_context_class(row) for row in cases)
    roles = Counter(row["antagonist_role_status"] for row in cases)

    gym = [row for row in cases if row["source_id"] == "SCHPRISMA-000030"]
    if len(gym) != 8:
        raise ValueError(f"expected 8 Gymnadenia Table A2 cases, found {len(gym)}")

    return {
        "analysis": "sch_macroecology_h2_context_cases_cumulative_v3",
        "n_evidence_batches": len(evidence_paths),
        "n_case_batches": len(case_paths),
        "n_context_evidence_rows": len(evidence),
        "n_canonical_axes_with_context_evidence": len(evidence_axes),
        "n_source_records_with_context_evidence": len({row["source_id"] for row in evidence}),
        "n_materialized_local_cases": len(cases),
        "n_canonical_axes_with_materialized_cases": len(
            {row["canonical_trait_axis_id"] for row in cases}
        ),
        "n_clusters_with_materialized_cases": len({row["cluster_id"] for row in cases}),
        "local_context_class_counts": dict(sorted(classes.items())),
        "local_role_status_counts": dict(sorted(roles.items())),
        "n_context_shift_from_reference_yes": sum(
            row["context_shift_from_reference"] == "YES" for row in cases
        ),
        "n_evidence_rows_without_materialized_cases": sum(
            int(row["local_cases_materialized"]) == 0 for row in evidence
        ),
        "n_evidence_rows_requiring_source_object": sum(
            row["source_object_required"] != "NONE" for row in evidence
        ),
        "n_gymnadenia_local_net_selection_cases": len(gym),
        "gymnadenia_axes_materialized": sorted(
            {row["canonical_trait_axis_id"] for row in gym}
        ),
        "h2_model_ready": False,
        "status": "H2_LOCAL_NET_SELECTION_EXPANDED_INFERENCE_FAIL_CLOSED",
        "claim_ceiling": [
            "materialized_case_count_is_the_only_current_local_H2_N",
            "reported_context_counts_are_not_model_cases",
            "local_net_selection_is_not_local_two_function_geometry",
            "consumer_removal_context_is_not_forced_into_static_two_function_geometry",
            "role_behavior_context_is_not_relabelled_as_plant_fitness_geometry",
            "agent_contrast_point_estimates_without_uncertainty_are_directional_only",
            "H2_model_not_ready",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence", type=Path, nargs="+", required=True)
    parser.add_argument("--cases", type=Path, nargs="+", required=True)
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

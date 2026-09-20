from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

MIN_LAYER_CASES = 12
MIN_LAYER_AXES = 8
MIN_LAYER_CLUSTERS = 8
MIN_REPEATED_AXES = 5


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for row in reader:
            if None in row:
                raise ValueError(f"CSV row has more fields than header in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def _axis_case_counts(rows: list[dict[str, str]]) -> Counter[str]:
    return Counter(row["canonical_trait_axis_id"] for row in rows)


def build(
    measurement_path: Path,
    change_seed_path: Path,
    case_paths: list[Path],
) -> dict:
    measurements = _read(measurement_path)
    changes = _read(change_seed_path)

    cases: list[dict[str, str]] = []
    for path in case_paths:
        cases.extend(_read(path))

    case_ids = [row["case_id"] for row in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("H2 case_id must be unique")

    performance_case_ids = {
        row["case_id"] for row in measurements if row["case_id"]
    }
    all_case_ids = set(case_ids)
    if not performance_case_ids <= all_case_ids:
        raise ValueError("measurement registry references missing H2 cases")

    performance = [row for row in cases if row["case_id"] in performance_case_ids]
    role_behavior = [row for row in cases if row["case_id"] not in performance_case_ids]

    performance_axis_counts = _axis_case_counts(performance)
    role_axis_counts = _axis_case_counts(role_behavior)
    all_axis_counts = _axis_case_counts(cases)

    performance_repeated = sorted(
        axis for axis, n in performance_axis_counts.items() if n >= 2
    )
    role_repeated = sorted(
        axis for axis, n in role_axis_counts.items() if n >= 2
    )
    all_repeated = sorted(
        axis for axis, n in all_axis_counts.items() if n >= 2
    )

    performance_clusters = {row["cluster_id"] for row in performance}
    role_clusters = {row["cluster_id"] for row in role_behavior}
    all_clusters = {row["cluster_id"] for row in cases}

    performance_ready = (
        len(performance) >= MIN_LAYER_CASES
        and len(performance_axis_counts) >= MIN_LAYER_AXES
        and len(performance_clusters) >= MIN_LAYER_CLUSTERS
        and len(performance_repeated) >= MIN_REPEATED_AXES
    )
    role_ready = (
        len(role_behavior) >= MIN_LAYER_CASES
        and len(role_axis_counts) >= MIN_LAYER_AXES
        and len(role_clusters) >= MIN_LAYER_CLUSTERS
        and len(role_repeated) >= MIN_REPEATED_AXES
    )

    change_counts = Counter(row["change_type"] for row in changes)
    change_records_with_two_or_more_cases = sum(
        int(row["local_cases_materialized"]) >= 2 for row in changes
    )

    return {
        "analysis": "sch_macroecology_h2_modelability_gate_v1",
        "project_gates": {
            "min_cases_per_layer": MIN_LAYER_CASES,
            "min_canonical_axes_per_layer": MIN_LAYER_AXES,
            "min_independent_clusters_per_layer": MIN_LAYER_CLUSTERS,
            "min_repeated_axes_per_layer": MIN_REPEATED_AXES,
        },
        "n_total_local_cases": len(cases),
        "n_total_canonical_axes_with_cases": len(all_axis_counts),
        "n_total_clusters_with_cases": len(all_clusters),
        "n_total_axes_with_two_or_more_local_cases": len(all_repeated),
        "axes_with_two_or_more_local_cases": all_repeated,
        "plant_performance_layer": {
            "n_cases": len(performance),
            "n_canonical_axes": len(performance_axis_counts),
            "n_clusters": len(performance_clusters),
            "n_axes_with_two_or_more_cases": len(performance_repeated),
            "axes_with_two_or_more_cases": performance_repeated,
            "model_ready": performance_ready,
        },
        "role_behavior_layer": {
            "n_cases": len(role_behavior),
            "n_canonical_axes": len(role_axis_counts),
            "n_clusters": len(role_clusters),
            "n_axes_with_two_or_more_cases": len(role_repeated),
            "axes_with_two_or_more_cases": role_repeated,
            "model_ready": role_ready,
        },
        "n_change_records": len(changes),
        "change_type_counts": dict(sorted(change_counts.items())),
        "n_change_records_with_two_or_more_materialized_cases": (
            change_records_with_two_or_more_cases
        ),
        "combined_layer_model_permitted": False,
        "combined_layer_model_blocker": (
            "plant_performance_and_role_behavior_are_noncommensurate_estimands"
        ),
        "plant_performance_model_ready": performance_ready,
        "role_behavior_model_ready": role_ready,
        "primary_h2_status": "DESCRIPTIVE_WITHIN_SOURCE_CONTRASTS_ONLY",
        "permitted_now": [
            "source-resolved_within-axis_context_descriptions",
            "within-source treatment or cultivar contrasts",
            "mechanistic change-type synthesis",
            "continued source-object recovery",
        ],
        "not_permitted_as_primary_now": [
            "mixed_effects_context_switch_model",
            "combined plant-performance plus role-behavior regression",
            "context-switch prevalence estimate",
            "treating reported but unmaterialized contexts as model rows",
        ],
        "reasons": [
            "only_4_independent_clusters_have_materialized_local_cases",
            "plant_performance_layer_has_only_3_cases_across_2_axes_and_2_clusters",
            "only_1_plant_performance_axis_has_two_or_more_local_cases",
            "role_behavior_layer_has_only_7_cases_across_3_axes_and_2_clusters",
            "plant_performance_and_role_behavior_are_different_estimands",
            "fixed_role source objects remain unmaterialized",
        ],
        "status": "H2_MODELABILITY_GATE_FROZEN_FAIL_CLOSED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("measurement", type=Path)
    parser.add_argument("change_seed", type=Path)
    parser.add_argument("--cases", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.measurement, args.change_seed, args.cases)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

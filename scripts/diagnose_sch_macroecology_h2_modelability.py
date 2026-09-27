from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
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


def _split_ids(row: dict[str, str]) -> list[str]:
    value = row.get("case_ids", row.get("case_id", ""))
    if not value:
        return []
    return [part for part in value.split(";") if part]


def _axis_case_counts(rows: list[dict[str, str]]) -> Counter[str]:
    return Counter(row["canonical_trait_axis_id"] for row in rows)


def _families(
    rows: list[dict[str, str]],
    field: str,
    gates: dict[str, int],
) -> dict[str, dict[str, object]]:
    out = defaultdict(
        lambda: {
            "cases": 0,
            "axes": set(),
            "clusters": set(),
            "repeated_axes": set(),
        }
    )
    for row in rows:
        ids = _split_ids(row)
        if not ids:
            continue
        key = row.get(field, "")
        if not key:
            continue
        out[key]["cases"] += len(ids)
        out[key]["axes"].add(row["canonical_trait_axis_id"])
        out[key]["clusters"].add(row["cluster_id"])
        if len(ids) >= 2:
            out[key]["repeated_axes"].add(row["canonical_trait_axis_id"])

    result = {}
    for key, value in sorted(out.items()):
        result[key] = {
            "n_cases": value["cases"],
            "n_axes": len(value["axes"]),
            "n_clusters": len(value["clusters"]),
            "n_repeated_axes": len(value["repeated_axes"]),
            "model_ready": (
                value["cases"] >= gates["min_cases_per_layer"]
                and len(value["axes"]) >= gates["min_canonical_axes_per_layer"]
                and len(value["clusters"]) >= gates["min_independent_clusters_per_layer"]
                and len(value["repeated_axes"]) >= gates["min_repeated_axes_per_layer"]
            ),
        }
    return result


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
        case_id
        for row in measurements
        for case_id in _split_ids(row)
    }
    all_case_ids = set(case_ids)
    if not performance_case_ids <= all_case_ids:
        raise ValueError("measurement registry references missing H2 cases")

    performance = [
        row for row in cases if row["case_id"] in performance_case_ids
    ]
    role_behavior = [
        row for row in cases if row["case_id"] not in performance_case_ids
    ]

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

    gates = {
        "min_cases_per_layer": MIN_LAYER_CASES,
        "min_canonical_axes_per_layer": MIN_LAYER_AXES,
        "min_independent_clusters_per_layer": MIN_LAYER_CLUSTERS,
        "min_repeated_axes_per_layer": MIN_REPEATED_AXES,
    }

    performance_ready_structural = (
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

    blockers = []
    if len(performance) < MIN_LAYER_CASES:
        blockers.append("case_count_below_gate")
    if len(performance_axis_counts) < MIN_LAYER_AXES:
        blockers.append("canonical_axes_below_gate")
    if len(performance_clusters) < MIN_LAYER_CLUSTERS:
        blockers.append("independent_clusters_below_gate")
    if len(performance_repeated) < MIN_REPEATED_AXES:
        blockers.append("repeated_axes_below_gate")

    change_counts = Counter(row["change_type"] for row in changes)

    result = {
        "analysis": "sch_macroecology_h2_modelability_gate",
        "project_gates": gates,
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
            "model_ready": performance_ready_structural,
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
        "n_change_records_with_two_or_more_materialized_cases": sum(
            int(row["local_cases_materialized"]) >= 2 for row in changes
        ),
        "combined_layer_model_permitted": False,
        "combined_layer_model_blocker": (
            "plant_performance_and_role_behavior_are_noncommensurate_estimands"
        ),
        "raw_plant_performance_case_count_gate_pass": (
            len(performance) >= MIN_LAYER_CASES
        ),
        "plant_performance_axis_gate_pass": (
            len(performance_axis_counts) >= MIN_LAYER_AXES
        ),
        "plant_performance_repeated_axis_gate_pass": (
            len(performance_repeated) >= MIN_REPEATED_AXES
        ),
        "broad_plant_performance_structural_gate_pass": (
            performance_ready_structural
        ),
        "structural_gate_blockers": blockers,
        "role_behavior_model_ready": role_ready,
        "permitted_now": [
            "source-resolved_within-axis_context_descriptions",
            "within-source treatment or cultivar contrasts",
            "treatment-cell net-selection comparison",
            "mechanistic change-type synthesis",
            "continued source-object recovery",
        ],
        "not_permitted_as_primary_now": [
            "mixed_effects_context_switch_model",
            "combined plant-performance plus role-behavior regression",
            "context-switch prevalence estimate",
            "mediated agent-contrast inference without valid contrast uncertainty",
            "local_antagonist_pressure_is_not_local_geometry",
            "treating reported but unmaterialized contexts as model rows",
        ],
    }

    has_estimand_fields = bool(measurements) and {
        "estimand_family",
        "numeric_pooling_family",
    } <= set(measurements[0])

    if has_estimand_fields:
        estimands = _families(measurements, "estimand_family", gates)
        pools = _families(measurements, "numeric_pooling_family", gates)
        estimand_ready = any(
            value["model_ready"] for value in estimands.values()
        )
        numeric_ready = any(value["model_ready"] for value in pools.values())

        result["estimand_family_modelability"] = estimands
        result["numeric_pooling_family_modelability"] = pools
        result["commensurate_estimand_family_model_ready"] = estimand_ready
        result["commensurate_numeric_pooling_model_ready"] = numeric_ready
        result["plant_performance_model_ready"] = (
            performance_ready_structural and estimand_ready
        )

        if performance_ready_structural and not estimand_ready:
            result["primary_h2_status"] = (
                "BREADTH_GATE_PASS_ESTIMAND_HARMONIZATION_FAIL"
            )
            result["status"] = (
                "H2_BREADTH_GATE_PASS_ESTIMAND_FAMILY_FAIL_CLOSED"
            )
            result["estimand_gate_blockers"] = [
                "no_single_estimand_family_meets_registered_case_axis_cluster_repeat_gates",
                "effect_metrics_are_not_numerically_commensurate_across_estimand_families",
                "antagonist_pressure_and_reproductive_proxy_rows_cannot_be_treated_as_selection_gradients",
            ]
        else:
            result["primary_h2_status"] = (
                "MODEL_READY"
                if result["plant_performance_model_ready"]
                else "DESCRIPTIVE_WITHIN_SOURCE_CONTRASTS_ONLY"
            )
            result["status"] = (
                "H2_MODELABILITY_CURRENT_OPEN"
                if result["plant_performance_model_ready"]
                else "H2_MODELABILITY_CURRENT_FAIL_CLOSED"
            )
            result["estimand_gate_blockers"] = [] if estimand_ready else [
                "no_single_estimand_family_meets_registered_case_axis_cluster_repeat_gates"
            ]
    else:
        result["commensurate_estimand_family_model_ready"] = False
        result["commensurate_numeric_pooling_model_ready"] = False
        result["plant_performance_model_ready"] = False
        result["primary_h2_status"] = "DESCRIPTIVE_WITHIN_SOURCE_CONTRASTS_ONLY"
        result["status"] = "H2_MODELABILITY_CURRENT_FAIL_CLOSED"
        result["estimand_gate_blockers"] = [
            "estimand_family_columns_not_available_in_this_historical_measurement_snapshot"
        ]

    result["reasons"] = [
        f"plant_performance_layer_has_{len(performance)}_cases_across_"
        f"{len(performance_axis_counts)}_axes_and_{len(performance_clusters)}_clusters",
        *blockers,
        "plant_performance_and_role_behavior_are_different_estimands",
    ]

    return result


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

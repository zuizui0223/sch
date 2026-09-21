from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

REGISTERED_LAYERS = {
    "LOCAL_GEOMETRY",
    "LOCAL_NET_SELECTION",
    "LOCAL_ANTAGONIST_PRESSURE",
}

MIN_CASES = 12
MIN_AXES = 8
MIN_CLUSTERS = 8
MIN_REPEATED_AXES = 5


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            if None in row:
                raise ValueError(f"malformed CSV row in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def _split(value: str) -> list[str]:
    return [x for x in value.split(";") if x] if value else []


def _summary(rows: list[dict[str, str]]) -> dict:
    axes = Counter(row["canonical_trait_axis_id"] for row in rows)
    clusters = {row["cluster_id"] for row in rows}
    return {
        "n_cases": len(rows),
        "n_axes": len(axes),
        "n_clusters": len(clusters),
        "n_repeated_axes": sum(n >= 2 for n in axes.values()),
        "axes": sorted(axes),
        "clusters": sorted(clusters),
        "gate_pass": (
            len(rows) >= MIN_CASES
            and len(axes) >= MIN_AXES
            and len(clusters) >= MIN_CLUSTERS
            and sum(n >= 2 for n in axes.values()) >= MIN_REPEATED_AXES
        ),
    }


def build(measurement_path: Path, case_paths: list[Path]) -> dict:
    measurements = _read(measurement_path)
    cases = []
    for path in case_paths:
        cases.extend(_read(path))
    case_map = {row["case_id"]: row for row in cases}

    if len(case_map) != len(cases):
        raise ValueError("duplicate case_id across H2 case files")

    layer_cases: dict[str, list[dict[str, str]]] = defaultdict(list)
    case_to_layer: dict[str, str] = {}

    for measurement in measurements:
        layer = measurement["highest_materialized_layer"]
        case_ids = _split(measurement["case_ids"])
        if not case_ids:
            continue
        if layer not in REGISTERED_LAYERS:
            raise ValueError(
                f"materialized plant-performance cases use unsupported layer {layer}: "
                f"{measurement['measurement_record_id']}"
            )
        for case_id in case_ids:
            if case_id not in case_map:
                raise ValueError(f"measurement registry references missing case {case_id}")
            if case_id in case_to_layer:
                raise ValueError(f"case assigned to multiple estimand layers: {case_id}")
            case_to_layer[case_id] = layer
            layer_cases[layer].append(case_map[case_id])

    layer_summary = {
        layer: _summary(layer_cases.get(layer, []))
        for layer in sorted(REGISTERED_LAYERS)
    }

    metric_summary: dict[str, dict[str, dict]] = {}
    for layer, rows in sorted(layer_cases.items()):
        by_metric: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in rows:
            by_metric[row["effect_metric"] or "EMPTY_EFFECT_METRIC"].append(row)
        metric_summary[layer] = {
            metric: _summary(metric_rows)
            for metric, metric_rows in sorted(by_metric.items())
        }

    net = layer_summary["LOCAL_NET_SELECTION"]
    numeric_metric_cluster_max = max(
        (
            info["n_clusters"]
            for info in metric_summary.get("LOCAL_NET_SELECTION", {}).values()
            if info["n_cases"] > 0
        ),
        default=0,
    )

    broad_plant_clusters = {
        row["cluster_id"]
        for layer in REGISTERED_LAYERS
        for row in layer_cases.get(layer, [])
    }

    return {
        "analysis": "sch_macroecology_h2_estimand_homogeneity_v1",
        "project_gates": {
            "min_cases": MIN_CASES,
            "min_axes": MIN_AXES,
            "min_clusters": MIN_CLUSTERS,
            "min_repeated_axes": MIN_REPEATED_AXES,
        },
        "n_materialized_plant_performance_cases": len(case_to_layer),
        "n_broad_plant_performance_clusters": len(broad_plant_clusters),
        "layer_summary": layer_summary,
        "effect_metric_summary": metric_summary,
        "local_net_selection_structural_gate_pass": net["gate_pass"],
        "max_clusters_in_any_exact_local_net_selection_metric_family": (
            numeric_metric_cluster_max
        ),
        "exact_effect_metric_cross_system_model_ready": (
            numeric_metric_cluster_max >= MIN_CLUSTERS
        ),
        "broad_plant_performance_pooling_permitted": False,
        "broad_pooling_blocker": (
            "LOCAL_GEOMETRY_LOCAL_NET_SELECTION_AND_LOCAL_ANTAGONIST_PRESSURE_"
            "ARE_DIFFERENT_ESTIMANDS"
        ),
        "primary_numeric_h2_model_ready": False,
        "primary_h2_status": "ESTIMAND_HOMOGENEITY_GATE_FAIL_CLOSED",
        "permitted_now": [
            "within_estimand descriptive summaries",
            "within_axis context contrasts",
            "scale_free mechanistic change_type synthesis",
            "prospective design of a common state_based H2 outcome",
        ],
        "not_permitted_as_primary_now": [
            "pooling geometry net_selection and antagonist_pressure as one response",
            "cross_system numeric effect_size model across incompatible effect metrics",
            "declaring H2 regression ready solely because broad cluster count reaches eight",
            "post_hoc metric collapse chosen after inspecting results",
        ],
        "reasons": [
            "broad plant_performance cluster count mixes three measurement layers",
            "LOCAL_NET_SELECTION currently spans incompatible effect metric families",
            "LOCAL_NET_SELECTION has only four independent clusters",
            "each exact LOCAL_NET_SELECTION effect metric family currently comes from one cluster",
        ],
        "status": "H2_ESTIMAND_HOMOGENEITY_GATE_FROZEN_V1",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("measurement", type=Path)
    parser.add_argument("--cases", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.measurement, args.cases)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V5_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v5.py"
ESTIMAND_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_estimand_homogeneity.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(
    measurement_path: Path,
    change_seed_path: Path,
    case_paths: list[Path],
) -> dict:
    broad = _load(V5_SCRIPT, "sch_h2_v5").build(
        measurement_path, change_seed_path, case_paths
    )
    estimand = _load(ESTIMAND_SCRIPT, "sch_h2_estimand").build(
        measurement_path, case_paths
    )

    net = estimand["layer_summary"]["LOCAL_NET_SELECTION"]
    required_clusters = estimand["project_gates"]["min_clusters"]
    additional_net_clusters = max(0, required_clusters - net["n_clusters"])

    return {
        "analysis": "sch_macroecology_h2_modelability_gate_v6_estimand_aware",
        "broad_structural_snapshot": {
            "n_total_local_cases": broad["n_total_local_cases"],
            "n_total_canonical_axes_with_cases": broad[
                "n_total_canonical_axes_with_cases"
            ],
            "n_total_clusters_with_cases": broad["n_total_clusters_with_cases"],
            "plant_performance_cases": broad["plant_performance_layer"]["n_cases"],
            "plant_performance_axes": broad["plant_performance_layer"][
                "n_canonical_axes"
            ],
            "broad_plant_performance_clusters": broad["plant_performance_layer"][
                "n_clusters"
            ],
            "repeated_plant_performance_axes": broad["plant_performance_layer"][
                "n_axes_with_two_or_more_cases"
            ],
            "broad_registered_case_gate_pass": broad[
                "raw_plant_performance_case_count_gate_pass"
            ],
            "broad_registered_axis_gate_pass": broad[
                "plant_performance_axis_gate_pass"
            ],
            "broad_registered_repeated_axis_gate_pass": broad[
                "plant_performance_repeated_axis_gate_pass"
            ],
            "broad_registered_cluster_gate_pass": (
                broad["plant_performance_layer"]["n_clusters"]
                >= broad["project_gates"]["min_independent_clusters_per_layer"]
            ),
        },
        "estimand_homogeneity": {
            layer: {
                "n_cases": info["n_cases"],
                "n_axes": info["n_axes"],
                "n_clusters": info["n_clusters"],
                "n_repeated_axes": info["n_repeated_axes"],
                "model_ready": info["gate_pass"],
            }
            for layer, info in estimand["layer_summary"].items()
        },
        "exact_local_net_selection_metric_cluster_counts": {
            metric: info["n_clusters"]
            for metric, info in estimand["effect_metric_summary"][
                "LOCAL_NET_SELECTION"
            ].items()
        },
        "broad_plant_performance_model_ready": False,
        "homogeneous_numeric_h2_model_ready": estimand[
            "exact_effect_metric_cross_system_model_ready"
        ],
        "primary_h2_model_ready": False,
        "primary_h2_status": "ESTIMAND_HOMOGENEITY_GATE_FAIL_CLOSED",
        "corrected_bottleneck": {
            "broad_structural_additional_clusters_to_eight": max(
                0,
                broad["project_gates"]["min_independent_clusters_per_layer"]
                - broad["plant_performance_layer"]["n_clusters"],
            ),
            "local_net_selection_additional_clusters_to_eight": (
                additional_net_clusters
            ),
            "max_clusters_in_one_exact_numeric_metric_family": estimand[
                "max_clusters_in_any_exact_local_net_selection_metric_family"
            ],
            "statement": (
                "Broad structural cluster count is not sufficient. "
                "Primary numeric H2 requires estimand-homogeneous replication."
            ),
        },
        "prospective_routes": [
            "recover additional independent LOCAL_NET_SELECTION clusters",
            "prospectively apply the frozen directional-state protocol",
            "retain LOCAL_GEOMETRY and LOCAL_ANTAGONIST_PRESSURE as separate strata",
        ],
        "not_permitted": estimand["not_permitted_as_primary_now"],
        "status": "H2_MODELABILITY_V6_ESTIMAND_AWARE_FAIL_CLOSED",
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

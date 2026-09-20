from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V3_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v3.py"


def _load_v3():
    spec = importlib.util.spec_from_file_location("sch_h2_modelability_v3", V3_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(measurement_path, change_seed_path, case_paths):
    result = _load_v3().build(measurement_path, change_seed_path, case_paths)
    result["analysis"] = "sch_macroecology_h2_modelability_gate_v4"
    result["status"] = "H2_MODELABILITY_GATE_V4_TRIFOLIUM_ADDED_FAIL_CLOSED"

    p = result["plant_performance_layer"]
    gates = result["project_gates"]
    blockers = []
    if p["n_cases"] < gates["min_cases_per_layer"]:
        blockers.append("case_count_below_gate")
    if p["n_canonical_axes"] < gates["min_canonical_axes_per_layer"]:
        blockers.append("canonical_axes_below_gate")
    if p["n_clusters"] < gates["min_independent_clusters_per_layer"]:
        blockers.append("independent_clusters_below_gate")
    if p["n_axes_with_two_or_more_cases"] < gates["min_repeated_axes_per_layer"]:
        blockers.append("repeated_axes_below_gate")
    result["structural_gate_blockers"] = blockers
    result["raw_plant_performance_case_count_gate_pass"] = (
        p["n_cases"] >= gates["min_cases_per_layer"]
    )
    result["plant_performance_repeated_axis_gate_pass"] = (
        p["n_axes_with_two_or_more_cases"] >= gates["min_repeated_axes_per_layer"]
    )
    result["reasons"] = [
        f"only_{result['n_total_clusters_with_cases']}_independent_clusters_have_materialized_local_cases",
        f"plant_performance_layer_has_{p['n_cases']}_cases_across_{p['n_canonical_axes']}_axes_and_{p['n_clusters']}_clusters",
        "plant_performance_case_count_and_repeated_axis_gates_pass_but_axis_and_cluster_gates_fail",
        f"role_behavior_layer_has_{result['role_behavior_layer']['n_cases']}_cases_across_{result['role_behavior_layer']['n_canonical_axes']}_axes_and_{result['role_behavior_layer']['n_clusters']}_clusters",
        "plant_performance_and_role_behavior_are_different_estimands",
        "Gentiana_and_Primula_exact_local_source_objects_remain_unmaterialized",
    ]
    return result


def main():
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

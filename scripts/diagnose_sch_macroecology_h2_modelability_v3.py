from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2_SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h2_modelability_v2.py"


def _load_v2():
    spec = importlib.util.spec_from_file_location("sch_h2_modelability_v2", V2_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(measurement_path: Path, change_seed_path: Path, case_paths: list[Path]) -> dict:
    result = _load_v2().build(measurement_path, change_seed_path, case_paths)
    result["analysis"] = "sch_macroecology_h2_modelability_gate_v3"
    result["status"] = "H2_MODELABILITY_GATE_V3_PEDICULARIS_PRESSURE_ADDED_FAIL_CLOSED"
    result["raw_plant_performance_case_count_gate_pass"] = (
        result["plant_performance_layer"]["n_cases"]
        >= result["project_gates"]["min_cases_per_layer"]
    )
    result["structural_gate_blockers"] = [
        "canonical_axes_below_gate",
        "independent_clusters_below_gate",
        "repeated_axes_below_gate",
    ]
    if "local_antagonist_pressure_is_not_local_geometry" not in result["not_permitted_as_primary_now"]:
        result["not_permitted_as_primary_now"].append(
            "local_antagonist_pressure_is_not_local_geometry"
        )
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

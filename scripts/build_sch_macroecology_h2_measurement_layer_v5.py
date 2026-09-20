from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer_v4.py"


def _load_v4():
    spec = importlib.util.spec_from_file_location("sch_h2_measurement_v4", V4_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(measurement_path, source_registry_path, case_paths):
    result = _load_v4().build(measurement_path, source_registry_path, case_paths)
    trif_ids = sorted(
        case_id for case_id in result["plant_performance_case_ids"]
        if case_id.startswith("Trifolium_")
    )
    if len(trif_ids) != 4:
        raise ValueError(f"expected 4 Trifolium measurement cases, found {len(trif_ids)}")
    result["analysis"] = "sch_macroecology_h2_measurement_layer_v5"
    result["n_trifolium_local_net_selection_cases"] = len(trif_ids)
    result["trifolium_case_ids"] = trif_ids
    result["status"] = "H2_MEASUREMENT_LAYER_V5_TRIFOLIUM_NET_SELECTION_MATERIALIZED"
    marker = "trifolium_exact_gradients_are_local_net_selection_not_two_function_geometry"
    if marker not in result["claim_ceiling"]:
        result["claim_ceiling"].insert(-1, marker)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("measurement", type=Path)
    parser.add_argument("source_registry", type=Path)
    parser.add_argument("--cases", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.measurement, args.source_registry, args.cases)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

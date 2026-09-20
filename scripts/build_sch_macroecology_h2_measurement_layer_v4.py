from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V3_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_measurement_layer_v3.py"


def _load_v3():
    spec = importlib.util.spec_from_file_location("sch_h2_measurement_v3", V3_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(measurement_path: Path, source_registry_path: Path, case_paths: list[Path]) -> dict:
    result = _load_v3().build(measurement_path, source_registry_path, case_paths)
    result["analysis"] = "sch_macroecology_h2_measurement_layer_v4"
    result["status"] = "H2_MEASUREMENT_LAYER_V4_PRIMULA_FIG4_MATERIALIZED"
    marker = "figure_direction_and_CI_status_are_local_net_selection_not_local_agent_geometry"
    if marker not in result["claim_ceiling"]:
        result["claim_ceiling"].insert(6, marker)
    return result


def main() -> None:
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

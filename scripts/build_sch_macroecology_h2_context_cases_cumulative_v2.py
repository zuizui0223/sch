from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative.py"


def _load_v1():
    spec = importlib.util.spec_from_file_location("sch_h2_context_cumulative_v1", V1_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(evidence_paths: list[Path], case_paths: list[Path]) -> dict:
    result = _load_v1().build(evidence_paths, case_paths)
    result["analysis"] = "sch_macroecology_h2_context_cases_cumulative_v2"
    result["status"] = "H2_ROLE_CONTEXT_CASES_EXPANDED_INFERENCE_FAIL_CLOSED"
    marker = "role_behavior_context_is_not_relabelled_as_plant_fitness_geometry"
    if marker not in result["claim_ceiling"]:
        result["claim_ceiling"].insert(3, marker)
    return result


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

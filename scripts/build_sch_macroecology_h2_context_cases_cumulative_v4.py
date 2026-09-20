from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V3_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v3.py"


def _load_v3():
    spec = importlib.util.spec_from_file_location("sch_h2_context_cumulative_v3", V3_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(evidence_paths: list[Path], case_paths: list[Path]) -> dict:
    result = _load_v3().build(evidence_paths, case_paths)
    result["analysis"] = "sch_macroecology_h2_context_cases_cumulative_v4"
    result["status"] = "H2_PRIMULA_FIG4_NET_SELECTION_CASES_EXPANDED_INFERENCE_FAIL_CLOSED"
    marker = "figure_sign_and_CI_status_are_materialized_without_bar_height_digitization"
    if marker not in result["claim_ceiling"]:
        result["claim_ceiling"].insert(5, marker)
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

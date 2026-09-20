from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v4.py"


def _load_v4():
    spec = importlib.util.spec_from_file_location("sch_h2_cumulative_v4", V4_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _read(paths):
    rows = []
    for path in paths:
        with path.open(encoding="utf-8", newline="") as handle:
            rows.extend({k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(handle))
    return rows


def build(evidence_paths, case_paths):
    result = _load_v4().build(evidence_paths, case_paths)
    cases = _read(case_paths)
    trif = [r for r in cases if r["source_id"] == "SCHPRISMA-000391"]
    if len(trif) != 4:
        raise ValueError(f"expected 4 Trifolium H2 cases, found {len(trif)}")
    result["analysis"] = "sch_macroecology_h2_context_cases_cumulative_v5"
    result["n_trifolium_local_net_selection_cases"] = len(trif)
    result["trifolium_axes_materialized"] = sorted({r["canonical_trait_axis_id"] for r in trif})
    result["status"] = "H2_TRIFOLIUM_NET_SELECTION_EXPANDED_INFERENCE_FAIL_CLOSED"
    marker = "trifolium_treatment_gradients_are_local_net_selection_not_local_geometry"
    if marker not in result["claim_ceiling"]:
        result["claim_ceiling"].insert(-1, marker)
    return result


def main():
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

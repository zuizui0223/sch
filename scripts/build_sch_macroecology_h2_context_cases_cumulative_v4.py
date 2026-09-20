from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V3_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_context_cases_cumulative_v3.py"


def _load_v3():
    spec = importlib.util.spec_from_file_location("sch_h2_cumulative_v3", V3_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            if None in row:
                raise ValueError(f"CSV row has more fields than header in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def _measurement_class(row: dict[str, str]) -> str:
    if (
        row["combined_or_net_response"] == "LOCAL_ANTAGONIST_PRESSURE_ONLY"
        or row["effect_metric"] == "SEED_PREDATION_PERCENT"
    ):
        return "LOCAL_ANTAGONIST_PRESSURE"
    if row["effect_metric"] == "PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA":
        return "LOCAL_NET_SELECTION"
    if row["function_2_direction_or_optimum"] == "REMOVED_BY_EXCLUSION":
        return "LOCAL_NET_SELECTION"
    if (
        row["conflict_detected"] == "YES"
        or row["alignment_detected"] == "YES"
        or row["one_sided_or_null_detected"] == "YES"
    ):
        return "LOCAL_GEOMETRY"
    if row["antagonist_role_status"] != "NET_ANTAGONISTIC":
        return "ROLE_BEHAVIOR_CONTEXT"
    return "UNRESOLVED"


def build(evidence_paths: list[Path], case_paths: list[Path]) -> dict:
    result = _load_v3().build(evidence_paths, case_paths)
    cases = []
    for path in case_paths:
        cases.extend(_read(path))
    classes = Counter(_measurement_class(row) for row in cases)
    result["analysis"] = "sch_macroecology_h2_context_cases_cumulative_v4"
    result["local_measurement_class_counts"] = dict(sorted(classes.items()))
    result["n_pedicularis_antagonist_pressure_cases"] = sum(
        row["source_id"] == "SCHPRISMA-000376"
        and _measurement_class(row) == "LOCAL_ANTAGONIST_PRESSURE"
        for row in cases
    )
    result["pedicularis_pressure_populations_materialized"] = sorted(
        row["population_or_site"]
        for row in cases
        if row["source_id"] == "SCHPRISMA-000376"
        and _measurement_class(row) == "LOCAL_ANTAGONIST_PRESSURE"
    )
    result["status"] = "H2_PEDICULARIS_PRESSURE_CASES_EXPANDED_INFERENCE_FAIL_CLOSED"
    marker = "local_antagonist_pressure_cases_are_not_local_geometry"
    if marker not in result["claim_ceiling"]:
        result["claim_ceiling"].insert(2, marker)
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

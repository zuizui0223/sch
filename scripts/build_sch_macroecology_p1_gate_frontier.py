from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from collections import Counter
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def _load_machine_module(path: Path):
    spec = importlib.util.spec_from_file_location("sch_macro_machine_pretriage", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def build(
    frozen_path: Path,
    prisma_dir: Path,
    machine_script: Path,
    recode_paths: list[Path],
) -> dict:
    machine = _load_machine_module(machine_script)
    machine_rows, _ = machine.build(frozen_path, prisma_dir)
    p1_ids = {
        row["record_id"]
        for row in machine_rows
        if row["paired_response_status"] == "P1_BOTH_RESPONSES_COMMON_FITNESS"
    }

    recodes: list[dict[str, str]] = []
    for path in recode_paths:
        recodes.extend(_read(path))

    ids = [row["record_id"] for row in recodes]
    if len(ids) != len(set(ids)):
        duplicates = sorted(k for k, n in Counter(ids).items() if n > 1)
        raise ValueError("duplicate record_id across design recodes: " + ", ".join(duplicates))

    p1_rows = [row for row in recodes if row["record_id"] in p1_ids]
    covered = {row["record_id"] for row in p1_rows}
    missing = sorted(p1_ids - covered)
    extra = sorted(covered - p1_ids)
    if missing or extra:
        raise ValueError(f"P1 gate mismatch: missing={missing}, extra={extra}")

    geometry_counts = dict(
        sorted(Counter(row["geometry_eligibility"] for row in p1_rows).items())
    )
    h1_status = {"ELIGIBLE_SAME_COORDINATE", "ELIGIBLE_BOUNDED_COORDINATE"}

    return {
        "analysis": "sch_macroecology_p1_manual_gate_frontier_v1",
        "n_machine_p1_records": len(p1_ids),
        "n_p1_manual_gated": len(p1_rows),
        "n_p1_missing_manual_gate": len(missing),
        "geometry_eligibility_counts": geometry_counts,
        "n_h1_geometry_candidate_records": sum(
            row["geometry_eligibility"] in h1_status for row in p1_rows
        ),
        "n_h2_context_candidate_records": sum(
            row["context_switch_eligibility"] == "ELIGIBLE_MULTI_CONTEXT"
            for row in p1_rows
        ),
        "n_trait_axis_split_required_records": sum(
            row["trait_axis_action"] == "SPLIT_REQUIRED" for row in p1_rows
        ),
        "n_single_axis_records": sum(
            row["trait_axis_action"] == "SINGLE_AXIS" for row in p1_rows
        ),
        "n_benefit_cost_coupled_boundary_records": sum(
            row["geometry_eligibility"] == "BOUNDARY_BENEFIT_COST_COUPLED"
            for row in p1_rows
        ),
        "status": "ALL_CURRENT_P1_RECORDS_MANUALLY_GATED",
        "claim_ceiling": [
            "record_level_candidate_frontier_not_independent_cluster_count",
            "trait_axis_decomposition_required_before_ecological_model",
            "programme_dependence_clustering_required",
            "no_conflict_prevalence",
            "no_H1_H2_model_fit_yet",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("frozen", type=Path)
    parser.add_argument("prisma_dir", type=Path)
    parser.add_argument("machine_script", type=Path)
    parser.add_argument("recode_csvs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        args.frozen,
        args.prisma_dir,
        args.machine_script,
        args.recode_csvs,
    )
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

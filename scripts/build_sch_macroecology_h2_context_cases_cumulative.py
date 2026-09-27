from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for row in reader:
            if None in row:
                raise ValueError(f"CSV row has more fields than header in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def _read_many(paths: list[Path]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths:
        rows.extend(_read(path))
    return rows


def _local_geometry(row: dict[str, str]) -> str:
    yes = []
    if row["conflict_detected"] == "YES":
        yes.append("CONFLICT")
    if row["alignment_detected"] == "YES":
        yes.append("ALIGNMENT_REINFORCEMENT")
    if row["one_sided_or_null_detected"] == "YES":
        yes.append("ONE_SIDED_OR_NULL")
    if len(yes) > 1:
        raise ValueError(f"local geometry collision: {row['case_id']}")
    if yes:
        return yes[0]
    if row["function_2_direction_or_optimum"] == "REMOVED_BY_EXCLUSION":
        return "CONSUMER_REMOVED_NO_STATIC_GEOMETRY"
    if row["antagonist_role_status"] != "NET_ANTAGONISTIC":
        return "ROLE_BEHAVIOR_CONTEXT"
    return "UNRESOLVED"


def _measurement_class(row: dict[str, str]) -> str:
    if (
        row["combined_or_net_response"] == "LOCAL_ANTAGONIST_PRESSURE_ONLY"
        or row["effect_metric"] == "SEED_PREDATION_PERCENT"
    ):
        return "LOCAL_ANTAGONIST_PRESSURE"
    if row["effect_metric"] in {
        "PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA",
        "STANDARDIZED_LINEAR_SELECTION_GRADIENT_BETA",
        "SEM_TOTAL_DIRECT_SELECTION_PATH_COEFFICIENT",
    }:
        return "LOCAL_NET_SELECTION"
    if row["effect_metric"] == "STANDARDIZED_REGRESSION_B_SUCCESSFUL_POLLINATION":
        return "LOCAL_REPRODUCTIVE_COMPONENT_EFFECT"
    if row["effect_metric"] == "LME_WALD_CHISQ_REPRODUCTIVE_PERFORMANCE_PROXY":
        return "LOCAL_REPRODUCTIVE_PERFORMANCE_PROXY"
    if row["function_2_direction_or_optimum"] == "REMOVED_BY_EXCLUSION":
        return "LOCAL_NET_SELECTION"
    if any(
        row[key] == "YES"
        for key in (
            "conflict_detected",
            "alignment_detected",
            "one_sided_or_null_detected",
        )
    ):
        return "LOCAL_GEOMETRY"
    if row["antagonist_role_status"] != "NET_ANTAGONISTIC":
        return "ROLE_BEHAVIOR_CONTEXT"
    return "UNRESOLVED"


def build(evidence_paths: list[Path], case_paths: list[Path]) -> dict:
    evidence = _read_many(evidence_paths)
    cases = _read_many(case_paths)

    evidence_ids = [row["evidence_id"] for row in evidence]
    if len(evidence_ids) != len(set(evidence_ids)):
        raise ValueError("duplicate H2 evidence_id across batches")
    case_ids = [row["case_id"] for row in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("duplicate H2 case_id across batches")

    evidence_axes = {row["canonical_trait_axis_id"] for row in evidence}
    if not {row["canonical_trait_axis_id"] for row in cases} <= evidence_axes:
        raise ValueError("materialized case lacks context-evidence provenance")

    declared = sum(int(row["local_cases_materialized"]) for row in evidence)
    if declared != len(cases):
        raise ValueError(
            f"declared local cases {declared} != materialized case rows {len(cases)}"
        )

    geometry = Counter(_local_geometry(row) for row in cases)
    roles = Counter(row["antagonist_role_status"] for row in cases)
    classes = Counter(_measurement_class(row) for row in cases)

    result = {
        "analysis": "sch_macroecology_h2_context_cases_cumulative",
        "n_evidence_batches": len(evidence_paths),
        "n_case_batches": len(case_paths),
        "n_context_evidence_rows": len(evidence),
        "n_canonical_axes_with_context_evidence": len(evidence_axes),
        "n_source_records_with_context_evidence": len(
            {row["source_id"] for row in evidence}
        ),
        "n_materialized_local_cases": len(cases),
        "n_canonical_axes_with_materialized_cases": len(
            {row["canonical_trait_axis_id"] for row in cases}
        ),
        "n_clusters_with_materialized_cases": len(
            {row["cluster_id"] for row in cases}
        ),
        "local_geometry_counts": dict(sorted(geometry.items())),
        "local_role_status_counts": dict(sorted(roles.items())),
        "local_measurement_class_counts": dict(sorted(classes.items())),
        "n_context_shift_from_reference_yes": sum(
            row["context_shift_from_reference"] == "YES" for row in cases
        ),
        "n_evidence_rows_without_materialized_cases": sum(
            int(row["local_cases_materialized"]) == 0 for row in evidence
        ),
        "n_evidence_rows_requiring_source_object": sum(
            row["source_object_required"] != "NONE" for row in evidence
        ),
        "h2_model_ready": False,
        "status": "H2_CONTEXT_CASES_CURRENT_FAIL_CLOSED",
        "claim_ceiling": [
            "materialized_case_count_is_the_only_current_local_H2_N",
            "reported_context_counts_are_not_model_cases",
            "local_antagonist_pressure_cases_are_not_local_geometry",
            "consumer_removal_context_is_not_forced_into_static_two_function_geometry",
            "role_behavior_context_is_not_relabelled_as_plant_fitness_geometry",
            "treatment_cell_net_selection_is_not_agent_mediated_geometry",
            "trifolium_treatment_gradients_are_local_net_selection_not_local_geometry",
            "erysimum_table5_paths_are_local_net_selection_not_local_agent_geometry",
            "polygala_successful_pollination_effect_is_reproductive_component_not_final_fitness",
            "tanacetum_germination_is_reproductive_performance_proxy_not_seed_set",
            "H2_model_not_ready",
        ],
    }

    expected_source_counts = {
        "SCHPRISMA-000376": 4,
        "SCHPRISMA-000391": 4,
        "SCHPRISMA-000008": 18,
        "SCHPRISMA-000334": 3,
        "SCHPRISMA-000352": 2,
    }
    present_source_ids = {row["source_id"] for row in cases}
    for source_id, expected in expected_source_counts.items():
        if source_id not in present_source_ids:
            continue
        observed = sum(row["source_id"] == source_id for row in cases)
        if observed != expected:
            raise ValueError(
                f"expected {expected} materialized cases for {source_id}, found {observed}"
            )

    pedicularis = [
        row
        for row in cases
        if row["source_id"] == "SCHPRISMA-000376"
        and _measurement_class(row) == "LOCAL_ANTAGONIST_PRESSURE"
    ]
    if pedicularis:
        result["n_pedicularis_antagonist_pressure_cases"] = len(pedicularis)
        result["pedicularis_pressure_populations_materialized"] = sorted(
            row["population_or_site"] for row in pedicularis
        )

    trifolium = [row for row in cases if row["source_id"] == "SCHPRISMA-000391"]
    if trifolium:
        result["n_trifolium_local_net_selection_cases"] = len(trifolium)
        result["trifolium_axes_materialized"] = sorted(
            {row["canonical_trait_axis_id"] for row in trifolium}
        )

    erysimum = [row for row in cases if row["source_id"] == "SCHPRISMA-000008"]
    if erysimum:
        result["n_erysimum_local_net_selection_cases"] = len(erysimum)
        result["erysimum_axes_materialized"] = sorted(
            {row["canonical_trait_axis_id"] for row in erysimum}
        )

    polygala = [row for row in cases if row["source_id"] == "SCHPRISMA-000334"]
    if polygala:
        result["n_polygala_reproductive_component_cases"] = len(polygala)

    tanacetum = [row for row in cases if row["source_id"] == "SCHPRISMA-000352"]
    if tanacetum:
        result["n_tanacetum_reproductive_performance_proxy_cases"] = len(tanacetum)

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

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

LAYERS = {
    "CONTEXT_STRUCTURE_ONLY": 0,
    "LOCAL_ANTAGONIST_PRESSURE": 1,
    "LOCAL_NET_SELECTION": 2,
    "LOCAL_GEOMETRY": 3,
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for row in reader:
            if None in row:
                raise ValueError(f"CSV row has more fields than header in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def _split_ids(value: str) -> list[str]:
    if not value or value == "NONE":
        return []
    return [part for part in value.split(";") if part]


def _is_role_behavior_case(row: dict[str, str]) -> bool:
    if row["antagonist_role_status"] == "NET_ANTAGONISTIC":
        return False
    if row["conflict_detected"] == "YES":
        return False
    if row["alignment_detected"] == "YES":
        return False
    if row["one_sided_or_null_detected"] == "YES":
        return False
    if row["function_2_direction_or_optimum"] == "REMOVED_BY_EXCLUSION":
        return False
    return True


def build(
    measurement_path: Path,
    source_registry_path: Path,
    case_paths: list[Path],
) -> dict:
    measurements = _read(measurement_path)
    source_objects = _read(source_registry_path)

    cases: list[dict[str, str]] = []
    for path in case_paths:
        cases.extend(_read(path))

    measurement_ids = [row["measurement_record_id"] for row in measurements]
    if len(measurement_ids) != len(set(measurement_ids)):
        raise ValueError("measurement_record_id must be unique")

    source_object_ids = [row["source_object_id"] for row in source_objects]
    if len(source_object_ids) != len(set(source_object_ids)):
        raise ValueError("source_object_id must be unique")
    source_object_set = set(source_object_ids)

    case_ids = [row["case_id"] for row in cases]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("context case_id must be unique")
    all_case_ids = set(case_ids)

    tracked_case_ids: set[str] = set()

    for row in measurements:
        supported = row["highest_source_supported_layer"]
        materialized = row["highest_materialized_layer"]
        if supported not in LAYERS or materialized not in LAYERS:
            raise ValueError(
                f"invalid H2 measurement layer for {row['measurement_record_id']}: "
                f"{supported} / {materialized}"
            )
        if LAYERS[materialized] > LAYERS[supported]:
            raise ValueError(
                f"materialized layer exceeds source-supported layer: "
                f"{row['measurement_record_id']}"
            )

        referenced = _split_ids(row["source_object_ids"])
        unknown_objects = sorted(set(referenced) - source_object_set)
        if unknown_objects:
            raise ValueError(
                f"unknown source object(s) for {row['measurement_record_id']}: "
                + ", ".join(unknown_objects)
            )

        row_case_ids = _split_ids(row["case_ids"])
        unknown_cases = sorted(set(row_case_ids) - all_case_ids)
        if unknown_cases:
            raise ValueError(
                f"measurement record points to missing context case(s): "
                f"{row['measurement_record_id']} -> {', '.join(unknown_cases)}"
            )
        overlap = tracked_case_ids & set(row_case_ids)
        if overlap:
            raise ValueError(
                "plant-performance context case referenced by multiple measurement records: "
                + ", ".join(sorted(overlap))
            )
        tracked_case_ids.update(row_case_ids)

        declared = (
            int(row["local_geometry_cases_materialized"])
            + int(row["local_net_selection_cases_materialized"])
            + int(row["local_antagonist_pressure_cases_materialized"])
        )
        if declared != len(row_case_ids):
            raise ValueError(
                f"{row['measurement_record_id']} declares {declared} cases but "
                f"lists {len(row_case_ids)} case IDs"
            )

    role_behavior_cases = [
        row for row in cases if row["case_id"] not in tracked_case_ids
    ]
    invalid_untracked = [
        row["case_id"] for row in role_behavior_cases if not _is_role_behavior_case(row)
    ]
    if invalid_untracked:
        raise ValueError(
            "untracked H2 case is not a role-behavior-only case: "
            + ", ".join(sorted(invalid_untracked))
        )

    supported_counts = Counter(
        row["highest_source_supported_layer"] for row in measurements
    )
    materialized_counts = Counter(
        row["highest_materialized_layer"] for row in measurements
    )
    source_status = Counter(row["route_status"] for row in source_objects)

    pedicularis = next(
        row
        for row in measurements
        if row["measurement_record_id"] == "Pedicularis_exsertion_geography"
    )

    gymnadenia_cases = sorted(
        case_id
        for case_id in tracked_case_ids
        if case_id.startswith("Gymnadenia_")
    )

    return {
        "analysis": "sch_macroecology_h2_measurement_layer_v3",
        "n_measurement_records": len(measurements),
        "n_canonical_axes": len(
            {row["canonical_trait_axis_id"] for row in measurements}
        ),
        "n_source_records": len({row["source_id"] for row in measurements}),
        "source_supported_layer_counts": dict(sorted(supported_counts.items())),
        "materialized_layer_counts": dict(sorted(materialized_counts.items())),
        "n_total_h2_local_cases": len(cases),
        "n_plant_performance_measurement_cases": len(tracked_case_ids),
        "plant_performance_case_ids": sorted(tracked_case_ids),
        "n_role_behavior_cases_separate": len(role_behavior_cases),
        "role_behavior_case_ids": sorted(row["case_id"] for row in role_behavior_cases),
        "n_canonical_axes_with_plant_performance_cases": len(
            {
                row["canonical_trait_axis_id"]
                for row in cases
                if row["case_id"] in tracked_case_ids
            }
        ),
        "n_canonical_axes_with_role_behavior_cases": len(
            {row["canonical_trait_axis_id"] for row in role_behavior_cases}
        ),
        "materialized_plant_performance_layer_counts": {
            "LOCAL_GEOMETRY": sum(
                int(row["local_geometry_cases_materialized"]) for row in measurements
            ),
            "LOCAL_NET_SELECTION": sum(
                int(row["local_net_selection_cases_materialized"])
                for row in measurements
            ),
            "LOCAL_ANTAGONIST_PRESSURE": sum(
                int(row["local_antagonist_pressure_cases_materialized"])
                for row in measurements
            ),
        },
        "n_measurement_records_below_source_supported_layer": sum(
            LAYERS[row["highest_materialized_layer"]]
            < LAYERS[row["highest_source_supported_layer"]]
            for row in measurements
        ),
        "n_source_objects": len(source_objects),
        "source_object_route_status_counts": dict(sorted(source_status.items())),
        "n_source_objects_binary_materialized": sum(
            row["binary_materialized"] == "YES" for row in source_objects
        ),
        "n_source_objects_exact_local_values_extracted": sum(
            row["exact_local_values_extracted"] == "YES" for row in source_objects
        ),
        "gymnadenia_local_net_selection_cases_materialized": len(gymnadenia_cases),
        "gymnadenia_case_ids": gymnadenia_cases,
        "pedicularis_context_structure": {
            "pollination_contexts_reported": int(
                pedicularis["n_contexts_function1_reported"]
            ),
            "seed_outcome_contexts_reported": int(
                pedicularis["n_contexts_function2_reported"]
            ),
            "individual_linked_contexts": int(
                pedicularis["n_contexts_individual_linked"]
            ),
            "population_specific_geometry_cases_materialized": int(
                pedicularis["local_geometry_cases_materialized"]
            ),
        },
        "h2_model_ready": False,
        "status": "H2_MEASUREMENT_LAYER_V3_GYMNADENIA_NET_SELECTION_MATERIALIZED",
        "claim_ceiling": [
            "measurement_layer_is_not_geometry_class",
            "treatment_group_net_selection_is_not_agent_specific_local_geometry",
            "source_supported_layer_can_exceed_materialized_layer",
            "local_antagonist_pressure_is_not_local_two_function_geometry",
            "local_net_selection_is_not_local_two_function_geometry",
            "plant_performance_cases_and_role_behavior_cases_are_separate_H2_layers",
            "only_materialized_plant_performance_rows_count_as_current_plant_performance_H2_N",
            "contrast_point_estimates_without_contrast_uncertainty_are_directional_only",
        ],
    }


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

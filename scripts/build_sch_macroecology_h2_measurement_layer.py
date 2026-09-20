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
    case_id_set = set(case_ids)

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
        unknown = sorted(set(referenced) - source_object_set)
        if unknown:
            raise ValueError(
                f"unknown source object(s) for {row['measurement_record_id']}: "
                + ", ".join(unknown)
            )

        if row["case_id"] and row["case_id"] not in case_id_set:
            raise ValueError(
                f"measurement record points to missing context case: "
                f"{row['measurement_record_id']} -> {row['case_id']}"
            )

    expected_case_count = sum(
        int(row["local_geometry_cases_materialized"])
        + int(row["local_net_selection_cases_materialized"])
        + int(row["local_antagonist_pressure_cases_materialized"])
        for row in measurements
    )
    if expected_case_count != len(cases):
        raise ValueError(
            f"measurement registry declares {expected_case_count} cases but "
            f"{len(cases)} context-case rows exist"
        )

    measurement_case_ids = {row["case_id"] for row in measurements if row["case_id"]}
    if measurement_case_ids != case_id_set:
        raise ValueError(
            "measurement registry case IDs do not exactly match materialized H2 cases"
        )

    supported_counts = Counter(
        row["highest_source_supported_layer"] for row in measurements
    )
    materialized_counts = Counter(
        row["highest_materialized_layer"] for row in measurements
    )

    source_status = Counter(row["route_status"] for row in source_objects)
    binary_materialized = sum(
        row["binary_materialized"] == "YES" for row in source_objects
    )
    exact_extracted = sum(
        row["exact_local_values_extracted"] == "YES" for row in source_objects
    )

    pedicularis = next(
        row
        for row in measurements
        if row["measurement_record_id"] == "Pedicularis_exsertion_geography"
    )

    return {
        "analysis": "sch_macroecology_h2_measurement_layer_v1",
        "n_measurement_records": len(measurements),
        "n_canonical_axes": len(
            {row["canonical_trait_axis_id"] for row in measurements}
        ),
        "n_source_records": len({row["source_id"] for row in measurements}),
        "source_supported_layer_counts": dict(sorted(supported_counts.items())),
        "materialized_layer_counts": dict(sorted(materialized_counts.items())),
        "n_materialized_model_cases": len(cases),
        "materialized_case_ids": sorted(case_id_set),
        "materialized_case_layer_counts": {
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
        "n_source_objects_binary_materialized": binary_materialized,
        "n_source_objects_exact_local_values_extracted": exact_extracted,
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
        "status": "H2_MEASUREMENT_LAYER_FROZEN_SOURCE_RECOVERY_FAIL_CLOSED",
        "claim_ceiling": [
            "measurement_layer_is_not_geometry_class",
            "source_supported_layer_can_exceed_materialized_layer",
            "local_antagonist_pressure_is_not_local_two_function_geometry",
            "local_net_selection_is_not_local_two_function_geometry",
            "only_materialized_case_rows_count_as_current_H2_model_N",
            "pending_source_objects_do_not_create_pseudo_cases",
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

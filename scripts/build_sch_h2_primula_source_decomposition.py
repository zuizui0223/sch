from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            if None in row:
                raise ValueError(f"malformed CSV row in {path}: {row[None]}")
            rows.append({k: (v or "").strip() for k, v in row.items()})
        return rows


def build(objects_path: Path, summary_path: Path) -> dict:
    objects = _read(objects_path)
    summary = _read(summary_path)

    object_ids = [row["primula_object_id"] for row in objects]
    if len(object_ids) != len(set(object_ids)):
        raise ValueError("Primula source-object IDs must be unique")

    if any(int(row["model_cases_materialized"]) != 0 for row in objects):
        raise ValueError(
            "Primula source-decomposition V1 must not create model cases before exact local extraction"
        )

    required = {
        "Primula_PNAS2013_Fig2_TableS2",
        "Primula_PNAS2013_Fig3_5pop",
        "Primula_PNAS2013_Fig4_factorial",
        "Primula_PNAS2013_Fig5_evolution",
        "Primula_PNAS2013_SI",
    }
    if set(object_ids) != required:
        raise ValueError("Primula source-object set drifted")

    source_layers = Counter(row["source_supported_layer"] for row in objects)
    statuses = Counter(row["exact_local_values_materialized"] for row in objects)

    metrics = {row["metric_id"]: row for row in summary}
    required_metrics = {
        "morph_frequency_2001",
        "grazing_long_2000",
        "grazing_long_2001",
        "fitness_vs_grazing_2000",
        "fitness_vs_grazing_2001",
        "fitness_vs_grazing_5pop_5yr",
        "control_relative_fitness_range",
        "morph_change_24pop_2006_2012",
        "fitness_vs_evolution_5pop",
        "exclosure_short_frequency",
        "control_short_frequency",
    }
    if not required_metrics <= set(metrics):
        raise ValueError("missing registered Primula main-text summary metrics")

    return {
        "analysis": "sch_h2_primula_source_decomposition_v1",
        "n_source_objects": len(objects),
        "source_supported_layer_counts": dict(sorted(source_layers.items())),
        "exact_local_value_status_counts": dict(sorted(statuses.items())),
        "n_model_cases_materialized": sum(
            int(row["model_cases_materialized"]) for row in objects
        ),
        "n_main_text_summary_metrics": len(summary),
        "registered_design_scopes": sorted(row["design_scope"] for row in objects),
        "main_text_exact_checks": {
            "survey_populations_2001": 69,
            "selection_population_years_2000": 37,
            "selection_population_years_2001": 46,
            "five_population_year_contexts": 25,
            "factorial_population_treatment_contexts": 16,
            "evolution_population_treatment_time_states": 36,
            "grazer_exclosure_populations": 9,
        },
        "status": "PRIMULA_PROGRAMME_DECOMPOSED_LOCAL_VALUES_PENDING",
        "claim_ceiling": [
            "programme_context_counts_are_not_model_N",
            "figure_only_local_values_are_not_exact_cases",
            "programme_aggregate_evolutionary_response_is_not_local_geometry",
            "auxiliary_older_programme_sources_are_not_added_to_current_macro_denominator",
            "exact_population_or_treatment_rows_require_source_table_or_exact_data",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("objects", type=Path)
    parser.add_argument("summary", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.objects, args.summary)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

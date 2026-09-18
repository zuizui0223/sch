from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

REQUIRED = {
    "cluster_id",
    "trait_domain",
    "function_pair_family",
    "antagonist_involved",
    "abiotic_function_involved",
    "shared_coordinate_status",
    "trait_manipulated",
    "consumer_context_manipulated",
    "common_fitness_endpoint",
    "multilevel_trait_surface",
    "spatial_replication",
    "temporal_replication",
    "conflict_detected",
    "alignment_detected",
    "context_shift_detected",
    "compromise_detected",
    "cancellation_detected",
    "source_pattern_class",
    "confidence",
    "coding_generation",
}

TERNARY = {"YES", "NO", "UNRESOLVED"}
TERNARY_FIELDS = {
    "antagonist_involved",
    "abiotic_function_involved",
    "trait_manipulated",
    "consumer_context_manipulated",
    "common_fitness_endpoint",
    "multilevel_trait_surface",
    "spatial_replication",
    "temporal_replication",
    "conflict_detected",
    "alignment_detected",
    "context_shift_detected",
    "compromise_detected",
    "cancellation_detected",
}


def _count(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows if row[field]).items()))


def _cross(rows: list[dict[str, str]], outcome: str, moderator: str) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for row in rows:
        out = row[outcome]
        mod = row[moderator]
        result.setdefault(out, {})
        result[out][mod] = result[out].get(mod, 0) + 1
    return {key: dict(sorted(value.items())) for key, value in sorted(result.items())}


def build(path: Path) -> dict:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or ())
        missing = sorted(REQUIRED - fields)
        if missing:
            raise ValueError("missing required columns: " + ", ".join(missing))
        rows = list(reader)

    if len({row["cluster_id"] for row in rows}) != len(rows):
        raise ValueError("cluster_id must be unique in the cluster seed ledger")

    for field in TERNARY_FIELDS:
        invalid = sorted({row[field] for row in rows if row[field] not in TERNARY})
        if invalid:
            raise ValueError(f"{field} has invalid values: {', '.join(invalid)}")

    conflict_adjudicated = [row for row in rows if row["conflict_detected"] in {"YES", "NO"}]
    context_positive = [row for row in rows if row["context_shift_detected"] == "YES"]

    return {
        "analysis": "sch_macroecology_cluster_seed_v1",
        "status": "SEED_SCHEMA_VALIDATED_NOT_INFERENTIAL_MACRO_SAMPLE",
        "n_clusters": len(rows),
        "trait_domain_counts": _count(rows, "trait_domain"),
        "function_pair_family_counts": _count(rows, "function_pair_family"),
        "antagonist_involved_counts": _count(rows, "antagonist_involved"),
        "abiotic_function_involved_counts": _count(rows, "abiotic_function_involved"),
        "shared_coordinate_status_counts": _count(rows, "shared_coordinate_status"),
        "conflict_detected_counts": _count(rows, "conflict_detected"),
        "alignment_detected_counts": _count(rows, "alignment_detected"),
        "context_shift_detected_counts": _count(rows, "context_shift_detected"),
        "compromise_detected_counts": _count(rows, "compromise_detected"),
        "cancellation_detected_counts": _count(rows, "cancellation_detected"),
        "design_feature_counts": {
            "trait_manipulated": _count(rows, "trait_manipulated"),
            "consumer_context_manipulated": _count(rows, "consumer_context_manipulated"),
            "common_fitness_endpoint": _count(rows, "common_fitness_endpoint"),
            "multilevel_trait_surface": _count(rows, "multilevel_trait_surface"),
            "spatial_replication": _count(rows, "spatial_replication"),
            "temporal_replication": _count(rows, "temporal_replication"),
        },
        "source_pattern_class_counts": _count(rows, "source_pattern_class"),
        "n_conflict_adjudicated_yes_or_no": len(conflict_adjudicated),
        "conflict_by_antagonist_seed_crosstab": _cross(conflict_adjudicated, "conflict_detected", "antagonist_involved"),
        "n_context_shift_yes": len(context_positive),
        "context_shift_yes_antagonist_counts": _count(context_positive, "antagonist_involved"),
        "claim_ceiling": [
            "seed_rows_are_reencoded_from_targeted_16_cluster_pattern_ledger",
            "not_sign_independent_macroecology_sample",
            "not_natural_prevalence",
            "no_ecological_moderator_causality",
            "full_primary_study_recode_required_before_H1_H4",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.ledger)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

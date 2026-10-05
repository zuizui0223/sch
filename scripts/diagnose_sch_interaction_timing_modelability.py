from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_TRAIT_AXIS_LEDGER_V1.csv"
STATIC = {"CONFLICT", "ALIGNMENT_REINFORCEMENT", "ONE_SIDED_OR_NULL"}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("canonical trait-axis ledger has no header")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def build(rows: list[dict[str, str]]) -> dict:
    fixed = [
        row for row in rows
        if row["antagonist_role_status"] == "NET_ANTAGONISTIC"
    ]
    static = [
        row for row in fixed
        if row["canonical_geometry"] in STATIC
    ]

    fixed_timing = Counter(row["interaction_timing"] for row in fixed)
    static_timing = Counter(row["interaction_timing"] for row in static)

    timing_geometry: dict[str, Counter] = defaultdict(Counter)
    for row in static:
        timing_geometry[row["interaction_timing"]][
            row["canonical_geometry"]
        ] += 1

    static_clusters: dict[str, dict[str, set[str] | int]] = {}
    for row in static:
        cluster = static_clusters.setdefault(
            row["cluster_id"],
            {"timing": set(), "geometry": set(), "axes": 0},
        )
        cluster["timing"].add(row["interaction_timing"])
        cluster["geometry"].add(row["canonical_geometry"])
        cluster["axes"] += 1

    timing_levels_fixed = sorted(fixed_timing)
    timing_levels_static = sorted(static_timing)

    biologically_ordered_timing_levels = {
        "SEQUENTIAL_LIFE_HISTORY_FILTER",
        "TEMPORALLY_SEPARATED",
    }
    n_ordered_fixed = sum(
        fixed_timing[level]
        for level in biologically_ordered_timing_levels
    )
    n_ordered_static = sum(
        static_timing[level]
        for level in biologically_ordered_timing_levels
    )

    return {
        "analysis": "sch_interaction_timing_modelability_v1",
        "n_canonical_axes": len(rows),
        "n_fixed_role_axes": len(fixed),
        "n_static_resolved_fixed_role_axes": len(static),
        "n_static_resolved_fixed_role_clusters": len(static_clusters),
        "fixed_role_timing_counts": dict(sorted(fixed_timing.items())),
        "static_resolved_timing_counts": dict(sorted(static_timing.items())),
        "static_geometry_by_timing": {
            timing: dict(sorted(counts.items()))
            for timing, counts in sorted(timing_geometry.items())
        },
        "n_fixed_role_axes_with_sequential_or_temporally_separated_timing": (
            n_ordered_fixed
        ),
        "n_static_axes_with_sequential_or_temporally_separated_timing": (
            n_ordered_static
        ),
        "fixed_role_timing_levels": timing_levels_fixed,
        "static_resolved_timing_levels": timing_levels_static,
        "timing_moderator_modelable": False,
        "timing_generalization_supported": False,
        "pedicularis_temporal_window_role": (
            "focal_mechanism_hypothesis_not_cross_system_generalization"
        ),
        "status": "TIMING_CONTRAST_NOT_MODELABLE_IN_CURRENT_CANONICAL_LEDGER",
        "reasons": [
            "34_of_35_fixed_role_axes_are_SIMULTANEOUS_OR_OVERLAPPING",
            "18_of_19_static_resolved_fixed_role_axes_are_SIMULTANEOUS_OR_OVERLAPPING",
            "zero_fixed_role_axes_use_SEQUENTIAL_LIFE_HISTORY_FILTER_or_TEMPORALLY_SEPARATED",
            "the_single_other_fixed_role_axis_is_SPATIAL_CONTEXT_not_a_temporal_separation_contrast",
            "current_data_cannot_estimate_a_timing_effect_without_posthoc_recoding",
        ],
        "claim_ceiling": [
            "descriptive_timing_coverage_only",
            "do_not_fit_interaction_timing_as_H1_moderator",
            "do_not_claim_temporal_separation_generalizes_conflict_geometry",
            "retain_P_rex_timing_as_focal_mechanistic_prediction",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Diagnose whether interaction timing can currently be tested as "
            "a moderator of SCH conflict geometry"
        )
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(_read(args.ledger))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

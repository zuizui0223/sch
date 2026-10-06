from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.audit_pedicularis_w1_w2_power_basis import (
    DEFAULT_LEDGER,
    _read,
)


GEOMETRY_GROUPS = {
    "FITNESS_VARIANCE",
    "FITNESS_GEOMETRY",
    "POLLEN_VARIANCE",
    "POLLEN_GEOMETRY",
    "INITIAL_SEED_VARIANCE",
    "INITIAL_SEED_GEOMETRY",
}

DIRECT_READY = {
    "DIRECT_SAME_CONTEXT_READY",
    "REGISTERED_THRESHOLD_READY",
    "PROSPECTIVE_DESIGN_FROZEN",
    "ROBUST_ENVELOPE_READY",
}


def _bound_class(row: dict[str, str]) -> str:
    status = row["current_status"]
    if status in DIRECT_READY:
        return "DIRECT_SAME_ESTIMAND_NUMERIC"
    if status.startswith("DIRECTION_ONLY"):
        return "DIRECTION_ONLY_NO_MAGNITUDE"
    if status in {
        "EXTERNAL_TOTAL_VARIANCE_ONLY",
        "EXTERNAL_RANGE_ONLY",
        "EXTERNAL_SENSITIVITY_ONLY",
    }:
        return "FOCAL_SCALE_OR_RANGE_ONLY"
    if status == "NO_DIRECT_BASIS":
        return "NO_NUMERIC_BOUND"
    return "OTHER_NOT_DIRECT"


def build(rows: list[dict[str, str]]) -> dict:
    focal = [
        row
        for row in rows
        if row["field_group"] in GEOMETRY_GROUPS
        and row["blocking_for_registered_n"] == "YES"
    ]
    if len(focal) != 18:
        raise ValueError(
            f"expected 18 blocking geometry/variance rows, found {len(focal)}"
        )

    classified = [
        {
            "config_path": row["config_path"],
            "field_group": row["field_group"],
            "current_status": row["current_status"],
            "current_source": row["current_source"],
            "bound_class": _bound_class(row),
            "notes": row["notes"],
        }
        for row in focal
    ]

    counts: dict[str, int] = {}
    for row in classified:
        counts[row["bound_class"]] = counts.get(row["bound_class"], 0) + 1

    direct = [
        row
        for row in classified
        if row["bound_class"] == "DIRECT_SAME_ESTIMAND_NUMERIC"
    ]
    direction = [
        row
        for row in classified
        if row["bound_class"] == "DIRECTION_ONLY_NO_MAGNITUDE"
    ]
    scale = [
        row
        for row in classified
        if row["bound_class"] == "FOCAL_SCALE_OR_RANGE_ONLY"
    ]
    unbounded = [
        row
        for row in classified
        if row["bound_class"] == "NO_NUMERIC_BOUND"
    ]

    fitness_surface_rows = [
        row for row in classified if row["field_group"] == "FITNESS_GEOMETRY"
    ]
    state_slope_rows = [
        row
        for row in classified
        if row["field_group"] in {
            "POLLEN_GEOMETRY",
            "INITIAL_SEED_GEOMETRY",
        }
    ]

    current_evidence_only_quantitative_envelope = (
        len(direct) == len(classified)
    )
    any_direct_causal_geometry = any(
        row["bound_class"] == "DIRECT_SAME_ESTIMAND_NUMERIC"
        for row in fitness_surface_rows + state_slope_rows
    )

    return {
        "analysis": "pedicularis_w1_w2_envelope_boundability_v1",
        "n_blocking_geometry_variance_rows": len(classified),
        "bound_class_counts": dict(sorted(counts.items())),
        "n_direct_same_estimand_numeric": len(direct),
        "n_direction_only_no_magnitude": len(direction),
        "n_focal_scale_or_range_only": len(scale),
        "n_no_numeric_bound": len(unbounded),
        "direct_same_estimand_numeric_paths": sorted(
            row["config_path"] for row in direct
        ),
        "direction_only_paths": sorted(
            row["config_path"] for row in direction
        ),
        "scale_or_range_only_paths": sorted(
            row["config_path"] for row in scale
        ),
        "no_numeric_bound_paths": sorted(
            row["config_path"] for row in unbounded
        ),
        "n_fitness_surface_rows": len(fitness_surface_rows),
        "n_state_slope_rows": len(state_slope_rows),
        "any_direct_numeric_causal_geometry_bound": any_direct_causal_geometry,
        "current_evidence_alone_supports_quantitative_robust_envelope": (
            current_evidence_only_quantitative_envelope
        ),
        "current_evidence_route_B_state": (
            "NOT_NUMERICALLY_BOUNDABLE_FROM_CURRENT_EVIDENCE_ALONE"
            if not current_evidence_only_quantitative_envelope
            else "NUMERICALLY_BOUNDABLE"
        ),
        "geometry_pilot_information_target": {
            "n_paths_directly_resolvable": 18,
            "target_groups": sorted(GEOMETRY_GROUPS),
            "purpose": (
                "replace direction/scale/no-basis rows with same-context "
                "same-estimand numerical geometry and variance"
            ),
        },
        "interpretation": (
            "Current focal literature supplies useful directions and endpoint "
            "scales but no direct same-estimand numerical bound for the randomized "
            "four-state causal geometry. A sensitivity envelope can still be used "
            "as a value-of-information exercise, but its key geometry bounds "
            "require additional independent scientific assumptions or direct pilot "
            "data rather than being identified by the current evidence."
        ),
        "claim_ceiling": [
            "bounded_evidence_inventory_not_proof_no_other_source_exists",
            "direction_is_not_promoted_to_causal_magnitude",
            "pooled_SD_is_not_promoted_to_plant_residual_variance_decomposition",
            "population_range_is_not_promoted_to_randomized_state_slope",
            "does_not_choose_geometry_pilot_sample_size",
            "does_not_register_P2_n",
        ],
        "rows": classified,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit how tightly current P. rex evidence can numerically bound "
            "the W1/W2 robust power-envelope geometry and variance inputs"
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

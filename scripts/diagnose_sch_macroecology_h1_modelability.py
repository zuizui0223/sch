from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

STATIC = {"CONFLICT", "ALIGNMENT_REINFORCEMENT", "ONE_SIDED_OR_NULL"}

# Conservative project gates fixed before fitting H1.
MIN_MULTINOMIAL_CLASS_N = 5
MIN_BINARY_OUTCOME_N = 10
MIN_INDEPENDENT_CLUSTERS = 20
MIN_MODERATOR_LEVEL_N = 3


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def _count(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(row[field] for row in rows).items()))


def build(path: Path) -> dict:
    rows = _read(path)
    fixed = [r for r in rows if r["antagonist_role_status"] == "NET_ANTAGONISTIC"]
    static = [r for r in fixed if r["canonical_geometry"] in STATIC]

    geometry = Counter(r["canonical_geometry"] for r in static)
    n_conflict = geometry["CONFLICT"]
    n_nonconflict = (
        geometry["ALIGNMENT_REINFORCEMENT"] + geometry["ONE_SIDED_OR_NULL"]
    )
    cluster_counts = Counter(r["cluster_id"] for r in static)
    multi_axis_clusters = sorted(k for k, n in cluster_counts.items() if n > 1)

    trait_domain = Counter(r["trait_domain"] for r in static)
    antagonist_family = Counter(r["antagonist_guild_family"] for r in static)

    multinomial_ready = (
        len(geometry) == 3
        and min(geometry.values()) >= MIN_MULTINOMIAL_CLASS_N
        and len(cluster_counts) >= MIN_INDEPENDENT_CLUSTERS
    )
    binary_ready = (
        min(n_conflict, n_nonconflict) >= MIN_BINARY_OUTCOME_N
        and len(cluster_counts) >= MIN_INDEPENDENT_CLUSTERS
    )
    trait_domain_ready = (
        len(trait_domain) >= 2
        and min(trait_domain.values()) >= MIN_MODERATOR_LEVEL_N
    )
    antagonist_family_ready = (
        len(antagonist_family) >= 2
        and min(antagonist_family.values()) >= MIN_MODERATOR_LEVEL_N
    )

    if multinomial_ready:
        primary_status = "MULTINOMIAL_MODEL_GATE_PASS"
    elif binary_ready and trait_domain_ready and antagonist_family_ready:
        primary_status = "BINARY_MODEL_GATE_PASS_MULTINOMIAL_FAIL"
    else:
        primary_status = "REGRESSION_GATE_FAIL_DESCRIPTIVE_EXACT_ONLY"

    return {
        "analysis": "sch_macroecology_h1_modelability_gate_v1",
        "project_gates": {
            "min_multinomial_class_n": MIN_MULTINOMIAL_CLASS_N,
            "min_binary_outcome_n": MIN_BINARY_OUTCOME_N,
            "min_independent_clusters": MIN_INDEPENDENT_CLUSTERS,
            "min_moderator_level_n": MIN_MODERATOR_LEVEL_N,
        },
        "n_canonical_axes": len(rows),
        "n_fixed_role_axes": len(fixed),
        "n_static_resolved_fixed_role_axes": len(static),
        "n_static_resolved_fixed_role_clusters": len(cluster_counts),
        "n_multi_axis_static_clusters": len(multi_axis_clusters),
        "multi_axis_static_clusters": multi_axis_clusters,
        "static_geometry_counts": dict(sorted(geometry.items())),
        "binary_conflict_count": n_conflict,
        "binary_nonconflict_count": n_nonconflict,
        "trait_domain_counts": dict(sorted(trait_domain.items())),
        "antagonist_guild_family_counts": dict(sorted(antagonist_family.items())),
        "multinomial_geometry_model_ready": multinomial_ready,
        "binary_conflict_model_ready": binary_ready,
        "trait_domain_moderator_ready_without_collapse": trait_domain_ready,
        "antagonist_guild_moderator_ready_without_collapse": antagonist_family_ready,
        "primary_h1_status": primary_status,
        "permitted_now": [
            "canonical_geometry_descriptive_counts",
            "cluster-aware_case_synthesis",
            "pre-registered_exact_or_fisher_sensitivity_after_moderator_collapse",
        ],
        "not_permitted_as_primary_now": [
            "multinomial_regression",
            "multivariable_logistic_regression",
            "unregistered_post_hoc_category_collapse",
            "conflict_prevalence_claim",
        ],
        "reasons": [
            "reinforcement_class_is_sparse",
            "only_13_independent_clusters_contribute_static_resolved_axes",
            "multiple_static_axes_occur_within_some_clusters",
            "trait_domain_has_sparse_levels",
            "antagonist_guild_family_has_sparse_levels",
            "15_fixed_role_canonical_axes_remain_unresolved",
            "full_frozen_868_screen_is_not_complete",
        ],
        "status": "H1_MODELABILITY_GATE_FROZEN_V1",
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

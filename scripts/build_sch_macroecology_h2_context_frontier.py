from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(handle)
        ]


def classify(row: dict[str, str]) -> tuple[str, str]:
    if row["context_shift_status"] != "YES":
        return "NOT_H2_QUEUE", "P4"

    if row["antagonist_role_status"] != "NET_ANTAGONISTIC":
        return "H2D_CONSUMER_ROLE_CONTEXT", "P1"

    if row["canonical_geometry"] == "CONTEXT_VARIABLE":
        return "H2A_GEOMETRY_SWITCH_CONFIRMED", "P1"

    if row["model_h1_status"] == "STATIC_RESOLVED_FIXED_ROLE":
        return "H2B_RESOLVED_GEOMETRY_CONTEXT_DEPENDENCE", "P2"

    if row["model_h1_status"] == "UNRESOLVED_FIXED_ROLE":
        return "H2C_CONTEXT_PRESENT_GEOMETRY_UNRESOLVED", "P1"

    return "H2E_OTHER_CONTEXT", "P3"


def build(path: Path) -> tuple[list[dict[str, str]], dict]:
    rows = _read(path)
    queue: list[dict[str, str]] = []

    for row in rows:
        lane, priority = classify(row)
        if lane == "NOT_H2_QUEUE":
            continue
        queue.append(
            {
                "canonical_trait_axis_id": row["canonical_trait_axis_id"],
                "cluster_id": row["cluster_id"],
                "plant_taxon": row["plant_taxon"],
                "trait_coordinate": row["trait_coordinate"],
                "trait_domain": row["trait_domain"],
                "canonical_geometry": row["canonical_geometry"],
                "antagonist_role_status": row["antagonist_role_status"],
                "antagonist_guild_family": row["antagonist_guild_family"],
                "source_count": row["source_count"],
                "source_ids": row["source_ids"],
                "h2_lane": lane,
                "h2_priority": priority,
                "context_case_materialization": "PENDING",
                "context_case_unit": "population_or_site/year_or_season/treatment_or_consumer_regime",
                "notes": "",
            }
        )

    queue.sort(key=lambda r: (r["h2_priority"], r["h2_lane"], r["canonical_trait_axis_id"]))

    lane_counts = Counter(row["h2_lane"] for row in queue)
    priority_counts = Counter(row["h2_priority"] for row in queue)
    role_counts = Counter(row["antagonist_role_status"] for row in queue)
    domain_counts = Counter(row["trait_domain"] for row in queue)

    receipt = {
        "analysis": "sch_macroecology_h2_context_frontier_v1",
        "n_canonical_axes": len(rows),
        "n_h2_queue_axes": len(queue),
        "n_h2_queue_clusters": len({row["cluster_id"] for row in queue}),
        "h2_lane_counts": dict(sorted(lane_counts.items())),
        "h2_priority_counts": dict(sorted(priority_counts.items())),
        "antagonist_role_status_counts": dict(sorted(role_counts.items())),
        "trait_domain_counts": dict(sorted(domain_counts.items())),
        "n_geometry_switch_confirmed_axes": lane_counts["H2A_GEOMETRY_SWITCH_CONFIRMED"],
        "n_fixed_role_resolved_context_axes": lane_counts["H2B_RESOLVED_GEOMETRY_CONTEXT_DEPENDENCE"],
        "n_fixed_role_unresolved_context_axes": lane_counts["H2C_CONTEXT_PRESENT_GEOMETRY_UNRESOLVED"],
        "n_consumer_role_context_axes": lane_counts["H2D_CONSUMER_ROLE_CONTEXT"],
        "context_cases_materialized": 0,
        "h2_model_ready": False,
        "status": "H2_CONTEXT_FRONTIER_FROZEN_CONTEXT_CASES_PENDING",
        "claim_ceiling": [
            "context_shift_flag_is_not_a_context_case",
            "axes_with_one_observed_context_are_not_negative_switching_cases",
            "consumer_role_context_is_separate_from_fixed_role_geometry_switching",
            "context_case_materialization_required_before_H2_model",
            "no_H2_prevalence_claim",
        ],
    }
    return queue, receipt


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("empty H2 queue")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("canonical_ledger", type=Path)
    parser.add_argument("--out-csv", type=Path, required=True)
    parser.add_argument("--out-json", type=Path, required=True)
    args = parser.parse_args()

    rows, receipt = build(args.canonical_ledger)
    write_csv(args.out_csv, rows)
    args.out_json.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()

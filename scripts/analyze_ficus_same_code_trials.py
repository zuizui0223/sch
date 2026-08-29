"""Analyze trial-level Ficus same-code receiver assays under a fail-closed contract.

Input is one CSV package for one plant species, one focal pollinator chemical
code, one pollinator taxon, and one focal NPFW taxon. Each introduced wasp is a
row and ``choice`` is CODE, CONTROL, or NO_CHOICE.

The analysis keeps no-choice counts, uses a cluster bootstrap over a declared
``cluster_id`` for uncertainty among decisive choices, calculates separate
95% directional and 90% equivalence intervals, and passes those intervals to
the registered same-code classifier.

This is a prespecified first-pass analysis for the prospective SCH experiment.
A richer hierarchical model may replace the bootstrap for a real data set, but
it must preserve the same estimand, positive-control gates, confidence levels,
and fail-closed classification rules.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import asdict
import json
import math
from pathlib import Path
import random
from typing import Iterable

from scripts.classify_ficus_same_code_receiver import (
    Interval,
    classify_same_code_receiver,
)


REQUIRED_FIELDS = (
    "trial_id",
    "species",
    "receiver_taxon",
    "receiver_guild",
    "assay_role",
    "code_id",
    "cluster_id",
    "assay_day",
    "assay_batch",
    "fig_stage",
    "apparatus_id",
    "stimulus_id",
    "control_id",
    "choice",
)
ROLES = ("POLLINATOR_CODE", "NPFW_POSITIVE_CONTROL", "NPFW_SAME_CODE")
CHOICES = {"CODE", "CONTROL", "NO_CHOICE"}
ROLE_GUILD = {
    "POLLINATOR_CODE": "POLLINATOR",
    "NPFW_POSITIVE_CONTROL": "NPFW",
    "NPFW_SAME_CODE": "NPFW",
}
ROLE_SEED_OFFSET = {
    "POLLINATOR_CODE": 101,
    "NPFW_POSITIVE_CONTROL": 211,
    "NPFW_SAME_CODE": 307,
}


def _read_trials(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("input CSV has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(f"missing required fields: {', '.join(missing)}")
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise ValueError("input CSV contains no trials")
    return rows


def _validate_trials(rows: list[dict[str, str]]) -> dict[str, str]:
    trial_ids = [row["trial_id"] for row in rows]
    if any(not value for value in trial_ids):
        raise ValueError("trial_id cannot be blank")
    if len(set(trial_ids)) != len(trial_ids):
        raise ValueError("trial_id must be unique")

    for field in REQUIRED_FIELDS:
        if field == "choice":
            continue
        if any(not row[field] for row in rows):
            raise ValueError(f"{field} cannot be blank")

    for row in rows:
        if row["choice"] not in CHOICES:
            raise ValueError(f"invalid choice {row['choice']!r}")
        if row["assay_role"] not in ROLES:
            raise ValueError(f"invalid assay_role {row['assay_role']!r}")
        expected = ROLE_GUILD[row["assay_role"]]
        if row["receiver_guild"] != expected:
            raise ValueError(
                f"{row['assay_role']} requires receiver_guild={expected}, "
                f"got {row['receiver_guild']}"
            )

    role_set = {row["assay_role"] for row in rows}
    if role_set != set(ROLES):
        raise ValueError(f"input must contain exactly the three assay roles; got {sorted(role_set)}")

    species = {row["species"] for row in rows}
    code_ids = {row["code_id"] for row in rows}
    if len(species) != 1:
        raise ValueError("one analysis package must contain exactly one plant species")
    if len(code_ids) != 1:
        raise ValueError("pollinator and NPFW assays must use one frozen code_id")

    pollinator_taxa = {
        row["receiver_taxon"] for row in rows if row["assay_role"] == "POLLINATOR_CODE"
    }
    npfw_taxa = {
        row["receiver_taxon"] for row in rows if row["assay_role"].startswith("NPFW_")
    }
    if len(pollinator_taxa) != 1:
        raise ValueError("POLLINATOR_CODE rows must contain exactly one pollinator taxon")
    if len(npfw_taxa) != 1:
        raise ValueError("NPFW positive-control and same-code rows must use the same focal NPFW taxon")

    for role in ROLES:
        decisive = [
            row for row in rows if row["assay_role"] == role and row["choice"] != "NO_CHOICE"
        ]
        if not decisive:
            raise ValueError(f"{role} has zero decisive choices")

    return {
        "species": next(iter(species)),
        "code_id": next(iter(code_ids)),
        "pollinator_taxon": next(iter(pollinator_taxa)),
        "npfw_taxon": next(iter(npfw_taxa)),
    }


def _quantile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("cannot take a quantile of an empty sequence")
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    fraction = position - lower
    return ordered[lower] * (1.0 - fraction) + ordered[upper] * fraction


def _cluster_bootstrap_interval(
    rows: list[dict[str, str]],
    *,
    confidence: float,
    iterations: int,
    seed: int,
    min_decisive_clusters: int,
) -> tuple[float, Interval, int]:
    decisive = [row for row in rows if row["choice"] != "NO_CHOICE"]
    groups: dict[str, list[int]] = {}
    for row in decisive:
        groups.setdefault(row["cluster_id"], []).append(1 if row["choice"] == "CODE" else 0)
    cluster_ids = sorted(groups)
    if len(cluster_ids) < min_decisive_clusters:
        raise ValueError(
            f"need at least {min_decisive_clusters} decisive clusters; got {len(cluster_ids)}"
        )

    all_values = [value for cluster in cluster_ids for value in groups[cluster]]
    point = sum(all_values) / len(all_values)
    rng = random.Random(seed)
    bootstrap: list[float] = []
    for _ in range(iterations):
        sampled_ids = [rng.choice(cluster_ids) for _ in cluster_ids]
        values = [value for cluster_id in sampled_ids for value in groups[cluster_id]]
        if values:
            bootstrap.append(sum(values) / len(values))
    if len(bootstrap) < max(100, int(iterations * 0.95)):
        raise RuntimeError("too many bootstrap replicates had no decisive choices")

    alpha = 1.0 - confidence
    interval = Interval(
        _quantile(bootstrap, alpha / 2.0),
        _quantile(bootstrap, 1.0 - alpha / 2.0),
    )
    return point, interval, len(cluster_ids)


def _role_summary(
    rows: list[dict[str, str]],
    *,
    role: str,
    iterations: int,
    seed: int,
    min_decisive_clusters: int,
) -> dict[str, object]:
    selected = [row for row in rows if row["assay_role"] == role]
    introduced = len(selected)
    code_choices = sum(row["choice"] == "CODE" for row in selected)
    control_choices = sum(row["choice"] == "CONTROL" for row in selected)
    no_choice = sum(row["choice"] == "NO_CHOICE" for row in selected)
    decisive = code_choices + control_choices

    point95, interval95, cluster_count = _cluster_bootstrap_interval(
        selected,
        confidence=0.95,
        iterations=iterations,
        seed=seed + ROLE_SEED_OFFSET[role],
        min_decisive_clusters=min_decisive_clusters,
    )
    if role == "NPFW_SAME_CODE":
        point90, interval90, cluster_count90 = _cluster_bootstrap_interval(
            selected,
            confidence=0.90,
            iterations=iterations,
            seed=seed + ROLE_SEED_OFFSET[role] + 1009,
            min_decisive_clusters=min_decisive_clusters,
        )
        if cluster_count90 != cluster_count or abs(point90 - point95) > 1e-12:
            raise RuntimeError("directional and equivalence summaries disagree on the point estimand")
    else:
        interval90 = None

    return {
        "receiver_taxon": selected[0]["receiver_taxon"],
        "introduced": introduced,
        "decisive": decisive,
        "code_choices": code_choices,
        "control_choices": control_choices,
        "no_choice": no_choice,
        "no_choice_fraction": no_choice / introduced,
        "decisive_cluster_count": cluster_count,
        "choice_probability": point95,
        "directional_95pct_cluster_bootstrap": asdict(interval95),
        "equivalence_90pct_cluster_bootstrap": (
            asdict(interval90) if interval90 is not None else None
        ),
    }


def analyze_trials(
    rows: list[dict[str, str]],
    *,
    iterations: int = 10000,
    seed: int = 20260829,
    min_decisive_clusters: int = 4,
    equivalence_margin: float = 0.10,
) -> dict[str, object]:
    if iterations < 1000:
        raise ValueError("bootstrap iterations must be at least 1000")
    if min_decisive_clusters < 2:
        raise ValueError("min_decisive_clusters must be at least 2")
    identity = _validate_trials(rows)

    summaries = {
        role: _role_summary(
            rows,
            role=role,
            iterations=iterations,
            seed=seed,
            min_decisive_clusters=min_decisive_clusters,
        )
        for role in ROLES
    }
    pollinator = summaries["POLLINATOR_CODE"]
    control = summaries["NPFW_POSITIVE_CONTROL"]
    npfw = summaries["NPFW_SAME_CODE"]
    decision = classify_same_code_receiver(
        pollinator_code=Interval(**pollinator["directional_95pct_cluster_bootstrap"]),
        npfw_positive_control=Interval(**control["directional_95pct_cluster_bootstrap"]),
        npfw_code_directional=Interval(**npfw["directional_95pct_cluster_bootstrap"]),
        npfw_code_equivalence=Interval(**npfw["equivalence_90pct_cluster_bootstrap"]),
        equivalence_margin=equivalence_margin,
    )

    decisive_n = int(npfw["decisive"])
    return {
        "analysis_id": "ficus_same_code_trial_analysis_v1",
        "data_contract": "one_species_one_frozen_code_one_pollinator_one_npfw_taxon",
        **identity,
        "interval_method": "cluster_percentile_bootstrap_on_declared_cluster_id",
        "bootstrap_iterations": iterations,
        "bootstrap_seed": seed,
        "minimum_decisive_clusters": min_decisive_clusters,
        "roles": summaries,
        "decision": asdict(decision),
        "planning_benchmarks": {
            "privacy_80pct_power_decisive_choices": 206,
            "privacy_90pct_power_decisive_choices": 260,
            "npfw_same_code_decisive_choices": decisive_n,
            "meets_privacy_80pct_planning_benchmark": decisive_n >= 206,
            "meets_privacy_90pct_planning_benchmark": decisive_n >= 260,
        },
        "claim_boundary": (
            "The classifier concerns behavioural response to one frozen chemical code. "
            "The cluster bootstrap is a prespecified first-pass dependence adjustment, not proof that all tree/day/batch structure is exhausted. "
            "No-choice observations are retained diagnostically. Behavioral equivalence is not chemical imperceptibility, and one contemporary same-code state is not L4."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260829)
    parser.add_argument("--min-decisive-clusters", type=int, default=4)
    parser.add_argument("--equivalence-margin", type=float, default=0.10)
    args = parser.parse_args(argv)

    rows = _read_trials(args.input_csv)
    result = analyze_trials(
        rows,
        iterations=args.iterations,
        seed=args.seed,
        min_decisive_clusters=args.min_decisive_clusters,
        equivalence_margin=args.equivalence_margin,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(result["decision"]["status"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

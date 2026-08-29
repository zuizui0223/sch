"""Prospective sample-size planner for Ficus same-code receiver assays.

The planner separates two goals that require very different sample sizes:

1. detect attraction/interception when the true choice probability is > 0.5;
2. support behavioural nonresponse by showing a 90% Wilson interval lies
   wholly inside a predeclared equivalence zone around 0.5.

Calculations use exact binomial probabilities over possible decisive-choice
counts. They do not account for tree/day/batch clustering directly; an explicit
planning design-effect and decisive-choice fraction inflate the required number
of introduced wasps.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import NormalDist


def wilson_interval(k: int, n: int, confidence: float) -> tuple[float, float]:
    if not 0 <= k <= n or n <= 0:
        raise ValueError("require 0 <= k <= n and n > 0")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    p = k / n
    denominator = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denominator
    half = z * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n)) / denominator
    return center - half, center + half


def binomial_pmf(k: int, n: int, p: float) -> float:
    return math.comb(n, k) * (p**k) * ((1.0 - p) ** (n - k))


def equivalence_success_probability(
    n: int,
    *,
    true_p: float = 0.5,
    null_p: float = 0.5,
    margin: float = 0.10,
    confidence: float = 0.90,
) -> float:
    low_target = null_p - margin
    high_target = null_p + margin
    success = 0.0
    for k in range(n + 1):
        low, high = wilson_interval(k, n, confidence)
        if low >= low_target and high <= high_target:
            success += binomial_pmf(k, n, true_p)
    return success


def attraction_success_probability(
    n: int,
    *,
    true_p: float,
    null_p: float = 0.5,
    confidence: float = 0.95,
) -> float:
    success = 0.0
    for k in range(n + 1):
        low, _ = wilson_interval(k, n, confidence)
        if low > null_p:
            success += binomial_pmf(k, n, true_p)
    return success


def minimum_n(probability_fn, target_power: float, *, max_n: int = 5000) -> tuple[int, float]:
    if not 0.0 < target_power < 1.0:
        raise ValueError("target_power must lie in (0, 1)")
    for n in range(2, max_n + 1):
        achieved = probability_fn(n)
        if achieved >= target_power:
            return n, achieved
    raise RuntimeError("target power not reached before max_n")


def introduced_count(decisive_n: int, *, design_effect: float, decisive_fraction: float) -> int:
    if design_effect < 1.0:
        raise ValueError("design_effect must be >= 1")
    if not 0.0 < decisive_fraction <= 1.0:
        raise ValueError("decisive_fraction must lie in (0, 1]")
    return math.ceil(decisive_n * design_effect / decisive_fraction)


def build_plan(
    *,
    equivalence_margin: float = 0.10,
    design_effect: float = 1.5,
    decisive_fraction: float = 0.75,
) -> dict[str, object]:
    equivalence_rows = []
    for power in (0.80, 0.90):
        n, achieved = minimum_n(
            lambda x: equivalence_success_probability(
                x,
                true_p=0.5,
                null_p=0.5,
                margin=equivalence_margin,
                confidence=0.90,
            ),
            power,
        )
        equivalence_rows.append(
            {
                "target_power": power,
                "decisive_choices": n,
                "achieved_probability": round(achieved, 6),
                "planned_introductions": introduced_count(
                    n, design_effect=design_effect, decisive_fraction=decisive_fraction
                ),
            }
        )

    attraction_rows = []
    for true_p in (0.60, 0.65, 0.70):
        for power in (0.80, 0.90):
            n, achieved = minimum_n(
                lambda x, p=true_p: attraction_success_probability(
                    x, true_p=p, null_p=0.5, confidence=0.95
                ),
                power,
            )
            attraction_rows.append(
                {
                    "true_choice_probability": true_p,
                    "target_power": power,
                    "decisive_choices": n,
                    "achieved_probability": round(achieved, 6),
                    "planned_introductions": introduced_count(
                        n, design_effect=design_effect, decisive_fraction=decisive_fraction
                    ),
                }
            )

    return {
        "analysis_id": "ficus_same_code_assay_power_v1",
        "equivalence_definition": {
            "null_preference": 0.5,
            "margin": equivalence_margin,
            "confidence_interval": "90pct_Wilson",
            "success_rule": "interval_wholly_inside_equivalence_zone",
        },
        "attraction_definition": {
            "null_preference": 0.5,
            "confidence_interval": "95pct_Wilson",
            "success_rule": "lower_bound_above_0.5",
        },
        "inflation": {
            "design_effect": design_effect,
            "decisive_choice_fraction": decisive_fraction,
        },
        "equivalence_rows": equivalence_rows,
        "attraction_rows": attraction_rows,
        "claim_boundary": (
            "These are prospective decisive-choice calculations. Introduced-wasp counts are explicit inflation scenarios, "
            "not guarantees under tree/day/batch clustering. A nonsignificant attraction test is not equivalence; "
            "behavioral privacy requires the dedicated equivalence rule plus a validated NPFW positive control."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out_json", type=Path)
    parser.add_argument("--design-effect", type=float, default=1.5)
    parser.add_argument("--decisive-fraction", type=float, default=0.75)
    args = parser.parse_args(argv)
    plan = build_plan(
        design_effect=args.design_effect,
        decisive_fraction=args.decisive_fraction,
    )
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    args.out_json.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(json.dumps(plan, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

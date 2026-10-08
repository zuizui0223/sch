"""Exact conditional one-fruit *optimum shift* tipping points for SCH P. rex.

Given completely validated frozen fruit-fate rows, vary the final intact seed
count of exactly ONE unresolved fruit from its verified integer lower to upper
bound. Retain all other unmeasured fruits at original bounds. Return exhaustive
integer outcome *ranges*, not a hypothetical likelihood distribution.

The status of the possible finite-grid reproductive optima only changes at
a few algebraically identified rank-competition thresholds. This script
partitions potentially huge integer seed-count intervals without enumerating
every possible count, and compares exposed versus excluded optima directly.

Sharpness is conditional on independent biologically feasible completion
of each individual flower's bounded viable count, absent interference.
This is descriptive finite-allocation geometry, NOT P0/G causal validation,
sampling inference or pure-function optima.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from scripts.bound_pedicularis_fruit_fate_selection import (
    _interpret, build as fruit_fate_build, read as read_fate,
)
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256

SCHEMA = "PEDICULARIS_ONE_FRUIT_OPTIMUM_SHIFT_TIPPING_V1"
G_STATES = ("EXCLUDED", "EXPOSED")


def _original_means(fate_receipt: dict) -> dict[str, dict[int, tuple[Fraction, Fraction]]]:
    return {
        g: {
            int(rank): (
                Fraction(v["mean_viable_seeds_per_flower_bounds"][0]["exact"]),
                Fraction(v["mean_viable_seeds_per_flower_bounds"][1]["exact"]),
            )
            for rank, v in fate_receipt["mean_fitness_by_predator_treatment_and_z"][g].items()
        }
        for g in G_STATES
    }


def _optima(values: dict[int, tuple[Fraction, Fraction]]) -> dict:
    benchmark = max(lo for lo, _ in values.values())
    possible = sorted(k for k, (_, hi) in values.items() if hi >= benchmark)
    if not possible:
        raise AssertionError("at least one discrete optimum must be possible")
    unique = [
        k for k, (lo, _) in values.items()
        if all(lo > other_hi for j, (_, other_hi) in values.items() if k != j)
    ]
    return {
        "possible_optimum_ranks": possible,
        "guaranteed_unique_optimum_rank": unique[0] if len(unique) == 1 else None,
    }


def _shift(values: dict[str, dict[int, tuple[Fraction, Fraction]]]) -> dict:
    excluded = _optima(values["EXCLUDED"])
    exposed = _optima(values["EXPOSED"])
    xp = excluded["possible_optimum_ranks"]
    ep = exposed["possible_optimum_ranks"]
    low, high = min(xp) - max(ep), max(xp) - min(ep)
    if low > 0:
        label = "GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
    elif high < 0:
        label = "GUARANTEED_NEGATIVE_EXCLUSION_SHIFT"
    elif low == high == 0:
        label = "GUARANTEED_ZERO_EXCLUSION_SHIFT"
    elif low >= 0:
        label = "NONNEGATIVE_SHIFT_ZERO_STILL_POSSIBLE"
    elif high <= 0:
        label = "NONPOSITIVE_SHIFT_ZERO_STILL_POSSIBLE"
    else:
        label = "BOTH_POSITIVE_AND_NEGATIVE_SHIFT_POSSIBLE"
    return {
        "excluded": excluded,
        "exposed": exposed,
        "excluded_minus_exposed_rank_shift_outer_interval": [low, high],
        "classification": label,
    }


def _floor(q: Fraction) -> int:
    return q.numerator // q.denominator


def outcome_ranges(
    *,
    source_means: dict[str, dict[int, tuple[Fraction, Fraction]]],
    target_g: str,
    target_rank: int,
    n_fruits_in_cell: int,
    viable_lower: int,
    viable_upper: int,
) -> list[dict]:
    """Exact partition of all integer x into equal optimum-rank-set ranges.

    Only target cell changes under exact ascertainment; both its lower and
    upper mean bounds move linearly with x, slope 1/n. Every rank
    competition can change only when target lower crosses another rank
    upper, or target upper crosses another rank lower. Integer floors
    and their successors partition all possible outcome counts.
    """
    if (
        target_g not in G_STATES
        or target_rank not in source_means.get(target_g, {})
        or type(n_fruits_in_cell) is not int or n_fruits_in_cell < 1
        or type(viable_lower) is not int or type(viable_upper) is not int
        or viable_lower < 0 or viable_upper <= viable_lower
        or set(source_means) != set(G_STATES)
    ):
        raise ValueError("invalid single-fruit optimum-shift source bounds")
    original_lower, original_upper = source_means[target_g][target_rank]
    a, b, n = viable_lower, viable_upper, n_fruits_in_cell
    if original_upper - original_lower < Fraction(b - a, n):
        raise ValueError("target source cell bounds are narrower than fruit uncertainty")

    cuts = {a, b+1}
    for rank, (other_lower, other_upper) in source_means[target_g].items():
        if rank == target_rank:
            continue
        # new lower(target) = old lower + (x-a)/n
        # new upper(target) = old upper - (b-x)/n
        crossing_lower_vs_upper = Fraction(a) + n*(other_upper - original_lower)
        crossing_upper_vs_lower = Fraction(b) + n*(other_lower - original_upper)
        for t in (crossing_lower_vs_upper, crossing_upper_vs_lower):
            pivot = _floor(t)
            for point in (pivot, pivot+1):
                if a <= point <= b:
                    cuts.add(point)
    ordered = sorted(cuts)
    segments = []
    for left, next_start in zip(ordered, ordered[1:]):
        right = next_start - 1
        if right < left:
            continue
        values = {g: dict(source_means[g]) for g in G_STATES}
        values[target_g][target_rank] = (
            original_lower + Fraction(left-a, n),
            original_upper - Fraction(b-left, n),
        )
        label = _shift(values)
        segments.append({
            "minimum_viable_seeds_if_observed": left,
            "maximum_viable_seeds_if_observed": right,
            "n_integer_outcome_values": right-left+1,
            **label,
        })

    # Merge redundant cuts: the output is the coarsest adjacent partition
    # with constant optimum-rank uncertainty and shift classification.
    compact: list[dict] = []
    for item in segments:
        if compact and (
            all(compact[-1][key] == item[key] for key in (
                "excluded", "exposed",
                "excluded_minus_exposed_rank_shift_outer_interval", "classification"
            ))
            and compact[-1]["maximum_viable_seeds_if_observed"] + 1
            == item["minimum_viable_seeds_if_observed"]
        ):
            compact[-1]["maximum_viable_seeds_if_observed"] = item[
                "maximum_viable_seeds_if_observed"
            ]
            compact[-1]["n_integer_outcome_values"] += item["n_integer_outcome_values"]
        else:
            compact.append(item)
    if (
        not compact or compact[0]["minimum_viable_seeds_if_observed"] != a
        or compact[-1]["maximum_viable_seeds_if_observed"] != b
        or sum(item["n_integer_outcome_values"] for item in compact) != b-a+1
    ):
        raise AssertionError("optimum tipping ranges do not partition all integers")
    return compact


def build(rows: list[dict[str, str]], allocation: dict) -> dict:
    # Reuse all provenance, flower identity, seed cap, G and z-grid checks.
    base = fruit_fate_build(rows, allocation)
    source_means = _original_means(base)
    current_shift = _shift(source_means)
    candidates = []
    for row in rows:
        fruit = _interpret(row)
        a, b = fruit["seed_fitness_lower"], fruit["seed_fitness_upper"]
        if a == b:
            continue
        g, rank = fruit["predator_treatment"], fruit["assigned_z_rank"]
        n = base["mean_fitness_by_predator_treatment_and_z"][g][str(rank)][
            "n_all_allocated_flowers"
        ]
        ranges = outcome_ranges(
            source_means=source_means,
            target_g=g,
            target_rank=rank,
            n_fruits_in_cell=n,
            viable_lower=a,
            viable_upper=b,
        )
        strict = ("GUARANTEED_POSITIVE_EXCLUSION_SHIFT",
                  "GUARANTEED_NEGATIVE_EXCLUSION_SHIFT",
                  "GUARANTEED_ZERO_EXCLUSION_SHIFT")
        resolving = [
            range_ for range_ in ranges
            if range_["classification"] in strict
            and range_["classification"] != current_shift["classification"]
        ]
        candidates.append({
            "flower_id": fruit["flower_id"],
            "plant_id": fruit["plant_id"],
            "predator_treatment": g,
            "assigned_z_rank": rank,
            "current_fate_status": fruit["fate_status"],
            "unobserved_viable_seed_count_interval": [a,b],
            "integer_outcome_ranges_after_exact_one_fruit_ascertainment": ranges,
            "n_integer_outcomes_in_strict_shift_classifications": sum(
                x["n_integer_outcome_values"]
                for x in ranges if x["classification"] in strict
            ),
            "n_integer_outcomes_that_newly_certify_shift_or_zero": sum(
                x["n_integer_outcome_values"] for x in resolving
            ),
            "some_single_fruit_outcome_newly_identifies_shift": bool(resolving),
            "total_integer_outcome_values_not_a_probability": b-a+1,
            "other_unknown_fruits_are_not_imputed": True,
        })
    candidates.sort(
        key=lambda r: (
            -int(r["some_single_fruit_outcome_newly_identifies_shift"]),
            -r["n_integer_outcomes_that_newly_certify_shift_or_zero"],
            -len(r["integer_outcome_ranges_after_exact_one_fruit_ascertainment"]),
            r["flower_id"],
        )
    )
    for i, candidate in enumerate(candidates, start=1):
        candidate["optimum_shift_information_priority_rank"] = i
    return {
        "receipt_schema": SCHEMA,
        "status": "NON_GATING_FINITE_SAMPLE_OPTIMUM_SHIFT_TIPPING_V1",
        "population_id": base["population_id"],
        "season_id": base["season_id"],
        "source_fate_bounds_receipt_sha256": _semantic_sha256(base),
        "n_original_allocated_flowers": base["n_all_allocated_flowers"],
        "n_currently_uncertain_fruits": len(candidates),
        "baseline": current_shift,
        "prioritized_missing_fruit_optimum_shift_assessments": candidates,
        "one_fruit_integer_outcome_ranges_are_not_probabilities": True,
        "outcomes_already_observed_in_p_rex": False,
        "no_joint_recovery_of_other_missing_fruits_assumed": True,
        "claim_ceiling": [
            "all_randomized_plant_and_flower_ids_retained_from_source_fate_receipt",
            "source_caps_field_authenticity_not_independently_verified",
            "exact_future_maturity_seed_count_may_be_unrecoverable",
            "single_flower_assessment_does_not_fix_other_censored_flower_fates",
            "possible_optimum_ranks_not_function_specific_optima",
            "no_probability_or_cost_based_expected_information_claim",
            "finite_grid_finite_sample_interval_not_population_CI",
            "independent_completion_of_bounded_flower_outcomes_assumed",
            "no_P0_G_P2_W1_W2_SCH_L_SLK_architecture_promotion",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("complete_allocated_fruit_fate_csv", type=Path)
    parser.add_argument("frozen_fruit_allocation_receipt_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(
        read_fate(args.complete_allocated_fruit_fate_csv),
        json.loads(args.frozen_fruit_allocation_receipt_json.read_text(encoding="utf-8")),
    )
    data = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data, encoding="utf-8")
    else:
        print(data, end="")


if __name__ == "__main__":
    main()

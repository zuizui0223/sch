"""Exact finite-fruit integer-constrained bounds for unpaired seed-stage margins.

Scientific use: countable, completely fate-resolved fruits with ONE known
common number N of ovules per fruit within both z settings. Marginal
initiation is an unordered multiset of *integer* counts; predation is
an unordered multiset of *exact rational* fractions from other fruits.
No source pairing is invented. A pair (initiation k, predation q)
is feasible only if k*q is an integer in [0,k].

Dynamic programming solves minimum and maximum total viable seeds over
*all perfect matchings*. It can tighten a relaxed continuous rearrangement
interval, but is limited to small groups (n<=14), known equal fruit weights,
and full, unambiguous fates. This is not population inference.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from fractions import Fraction
import json
import math
from pathlib import Path

from scripts.bound_sch_unpaired_seed_stage_selection import stage_bounds

SCHEMA = "SCH_INTEGER_SEED_STAGE_MARGINS_V1"
OUTPUT_SCHEMA = "SCH_INTEGER_FEASIBLE_SELECTION_BOUNDS_V1"
MAX_EXACT_FRUITS_PER_SETTING = 14


def _count(value: object, name: str, *, minimum: int, maximum: int) -> int:
    if type(value) is not int or value < minimum or value > maximum:
        raise ValueError(
            f"{name} must be an exact integer between {minimum} and {maximum}"
        )
    return value


def _ratio(value: object) -> Fraction:
    # Explicit numerator/denominator strings preserve exact biological
    # damaged-seed counts; rounded 0.3333 must NOT be silently 1/3.
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        raise ValueError("predation fraction requires a string or exact integer")
    try:
        q = Fraction(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("predation must be exact rational e.g. '1/3'") from exc
    if not 0 <= q <= 1:
        raise ValueError("predation fraction must be within [0,1]")
    return q


def integer_stage_bounds(
    initiated_counts: list[int],
    predation_fractions: list[str],
    ovules_per_fruit: int,
) -> dict:
    """Find sharp bounds on equal-weight viable-seed fraction via bitmask DP."""
    n_ovules = _count(
        ovules_per_fruit, "ovules_per_fruit", minimum=1, maximum=1000000
    )
    if (
        not isinstance(initiated_counts, list)
        or not isinstance(predation_fractions, list)
        or len(initiated_counts) != len(predation_fractions)
        or not 1 <= len(initiated_counts) <= MAX_EXACT_FRUITS_PER_SETTING
    ):
        raise ValueError("integer stage margins require 1..14 equal-length fruits")
    counts = tuple(sorted(_count(
        c, "initiated_seeds", minimum=1, maximum=n_ovules
    ) for c in initiated_counts))
    fractions = tuple(sorted(_ratio(q) for q in predation_fractions))
    n = len(counts)
    # Future validation is based solely on integer seed fates, not floating
    # approximations that could turn 1/3 into 0.3333333333333333.
    can_pair: dict[tuple[int, int], int] = {}
    for i, initiated in enumerate(counts):
        for j, q in enumerate(fractions):
            numerator = initiated * q.numerator
            if numerator % q.denominator == 0:
                damaged = numerator // q.denominator
                can_pair[(i, j)] = initiated - damaged
    @lru_cache(maxsize=None)
    def solve(used_q_mask: int):
        i = used_q_mask.bit_count()
        if i == n:
            return (0, 0, (), ())
        min_result = None
        max_result = None
        for j in range(n):
            if used_q_mask & (1 << j) or (i,j) not in can_pair:
                continue
            child = solve(used_q_mask | (1 << j))
            if child is None:
                continue
            viable = can_pair[(i,j)]
            cand_min = viable + child[0]
            cand_max = viable + child[1]
            if min_result is None or cand_min < min_result[0]:
                min_result = (cand_min, (j,) + child[2])
            if max_result is None or cand_max > max_result[0]:
                max_result = (cand_max, (j,) + child[3])
        if min_result is None:
            return None
        return min_result[0], max_result[0], min_result[1], max_result[1]

    answer = solve(0)
    if answer is None:
        raise ValueError(
            "NO_INTEGER_FEASIBLE_PERFECT_MATCHING: source q ratios cannot all "
            "be assigned to these initiated seed counts; check rounding, "
            "fate definitions and common-ovule assumption"
        )
    min_total, max_total, min_idx, max_idx = answer
    denom = n * n_ovules
    def witness(index_assignment: tuple[int, ...]) -> list[dict]:
        return [
            {
                "initiated_count": count,
                "q_fraction": str(fractions[j]),
                "damaged_count": count - can_pair[(i,j)],
                "viable_count": can_pair[(i,j)],
                "ovule_count": n_ovules,
            }
            for i, (count,j) in enumerate(zip(counts,index_assignment,strict=True))
        ]
    relaxed = stage_bounds(
        [c/n_ovules for c in counts],
        [float(q) for q in fractions],
    )
    min_fitness, max_fitness = min_total/denom, max_total/denom
    if (
        min_fitness < relaxed["minimum_possible_mean_viable_seed_fraction"] - 1e-12
        or max_fitness > relaxed["maximum_possible_mean_viable_seed_fraction"] + 1e-12
    ):
        raise AssertionError("integer constrained interval must lie within relaxation")
    return {
        "n_equal_weight_fruits": n,
        "ovules_per_fruit": n_ovules,
        "observed_initiation_count_multiset": list(counts),
        "observed_predation_ratio_multiset": [str(q) for q in fractions],
        "integer_viable_total_seeds_extrema": [min_total, max_total],
        "sharp_integer_feasible_mean_viable_fraction": [
            min_fitness, max_fitness
        ],
        "unrestricted_fractional_rearrangement_bounds": [
            relaxed["minimum_possible_mean_viable_seed_fraction"],
            relaxed["maximum_possible_mean_viable_seed_fraction"],
        ],
        "minimum_fitness_attaining_matching": witness(min_idx),
        "maximum_fitness_attaining_matching": witness(max_idx),
        "source_fruit_matches_reconstructed": False,
        "matching_is_just_a_feasible_witness": True,
        "n_dp_states_evaluated": solve.cache_info().currsize,
        "method": "EXACT_BITMASK_PERFECT_MATCHING_EQUAL_OVULES",
    }


def compare_settings_integer(
    low_initiated: list[int],
    low_q: list[str],
    high_initiated: list[int],
    high_q: list[str],
    ovules_per_fruit: int,
) -> dict:
    low = integer_stage_bounds(low_initiated, low_q, ovules_per_fruit)
    high = integer_stage_bounds(high_initiated, high_q, ovules_per_fruit)
    l0,l1 = low["sharp_integer_feasible_mean_viable_fraction"]
    h0,h1 = high["sharp_integer_feasible_mean_viable_fraction"]
    d0,d1 = h0-l1,h1-l0
    relaxed_low = low["unrestricted_fractional_rearrangement_bounds"]
    relaxed_high = high["unrestricted_fractional_rearrangement_bounds"]
    dr0,dr1 = relaxed_high[0]-relaxed_low[1],relaxed_high[1]-relaxed_low[0]
    if d0 > 0:
        sign = "POSITIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    elif d1 < 0:
        sign = "NEGATIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    else:
        sign = "SIGN_NOT_IDENTIFIED_ACROSS_INTEGER_FEASIBLE_COUPLINGS"
    return {
        "schema": OUTPUT_SCHEMA,
        "status": "SHARP_INTEGER_FEASIBLE_FINITE_SAMPLE_BOUNDS_ONLY",
        "low": low,
        "high": high,
        "integer_feasible_high_minus_low_interval": [d0,d1],
        "fractionally_relaxed_high_minus_low_interval": [dr0,dr1],
        "integer_constraint_changes_sign_identifiability": (
            dr0 <= 0 <= dr1 and (d0 > 0 or d1 < 0)
        ),
        "high_minus_low_direction_given_margins": sign,
        "claim_ceiling": [
            "same_known_ovule_count_for_each_fruit_in_each_setting_required",
            "exact_unrounded_predation_rational_values_required",
            "no_zero_initiated_unrecognizable_full_destruction_or_0_over_0_fruits",
            "only_countable_intact_and_damaged_initiated_seeds_allowed",
            "at_most_fourteen_fruits_per_setting_due_to_exponential_runtime",
            "attaining_matches_are_math_witnesses_not_true_fruit_identifications",
            "equal_fruit_weight_not_weighted_population_reproductive_success",
            "finite_sample_bound_not_confidence_interval_or_causal_effect",
            "z_manipulation_randomization_required_for_causal_trait_selection",
        ],
    }


def build(payload: dict) -> dict:
    if not isinstance(payload, dict) or payload.get("schema") != SCHEMA:
        raise ValueError("expected integer seed-stage schema")
    kind = payload.get("data_kind")
    if kind not in {"SYNTHETIC_DEMONSTRATION", "OBSERVED_UNPAIRED_MARGINS"}:
        raise ValueError("data_kind must distinguish synthetic from actual margins")
    if kind == "OBSERVED_UNPAIRED_MARGINS":
        if payload.get("complete_fruit_fate_adjudication") is not True:
            raise ValueError("field margins require complete fruit-fate adjudication")
        if not payload.get("source_population") or not payload.get("source_season"):
            raise ValueError("field margins require population/season provenance")
    margin = payload.get("setting_margins")
    if not isinstance(margin, dict) or set(margin) != {"LOW", "HIGH"}:
        raise ValueError("both LOW/HIGH setting margins required")
    for state in ("LOW","HIGH"):
        if not isinstance(margin[state], dict) or set(margin[state]) != {
            "initiated_seed_counts", "predation_fractions"
        }:
            raise ValueError("each setting needs count and ratio marginal arrays")
    result = compare_settings_integer(
        margin["LOW"]["initiated_seed_counts"],
        margin["LOW"]["predation_fractions"],
        margin["HIGH"]["initiated_seed_counts"],
        margin["HIGH"]["predation_fractions"],
        payload.get("ovules_per_fruit"),
    )
    result["source_data_kind"] = kind
    result["user_claims_observed_margins"] = kind == "OBSERVED_UNPAIRED_MARGINS"
    result["observed_field_data_independently_verified"] = False
    result["field_selection_effect_identified"] = False
    return result


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input_json", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = build(json.loads(args.input_json.read_text(encoding="utf-8")))
    serialized = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    else:
        print(serialized, end="")


if __name__ == "__main__":
    main()

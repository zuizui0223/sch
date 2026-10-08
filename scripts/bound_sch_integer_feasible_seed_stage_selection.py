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


def integer_stage_bounds_variable_ovules(
    ovule_and_initiated_counts: list[dict[str, int]],
    predation_fractions: list[str],
) -> dict:
    """Sharp mean intact-seed *fraction* under variable measured ovule counts.

    Ovule count and initiation count stay paired to the same fruit;
    predation ratios are a second unpaired multiset within this z cell.
    """
    if (
        not isinstance(ovule_and_initiated_counts, list)
        or not isinstance(predation_fractions, list)
        or len(ovule_and_initiated_counts) != len(predation_fractions)
        or not 1 <= len(ovule_and_initiated_counts) <= MAX_EXACT_FRUITS_PER_SETTING
    ):
        raise ValueError("integer stage margins require 1..14 equal-length fruits")
    pairs = []
    for fruit in ovule_and_initiated_counts:
        if not isinstance(fruit, dict) or set(fruit) != {"ovules", "initiated"}:
            raise ValueError("each fruit must pair ovules and initiated counts")
        n_ovules = _count(fruit["ovules"], "ovules", minimum=1, maximum=1000000)
        initiated = _count(
            fruit["initiated"], "initiated", minimum=1, maximum=n_ovules
        )
        pairs.append((n_ovules, initiated))
    pairs = tuple(sorted(pairs))
    fractions = tuple(sorted(_ratio(q) for q in predation_fractions))
    n = len(pairs)
    feasible: dict[tuple[int, int], tuple[int, Fraction]] = {}
    for i, (ovules, initiated) in enumerate(pairs):
        for j, q in enumerate(fractions):
            numerator = initiated * q.numerator
            if numerator % q.denominator == 0:
                damaged = numerator // q.denominator
                viable = initiated - damaged
                feasible[(i, j)] = (viable, Fraction(viable, ovules))

    @lru_cache(maxsize=None)
    def solve(used_mask: int):
        i = used_mask.bit_count()
        if i == n:
            return Fraction(0), Fraction(0), (), ()
        minimum, maximum = None, None
        for j in range(n):
            if used_mask & (1 << j) or (i, j) not in feasible:
                continue
            rest = solve(used_mask | (1 << j))
            if rest is None:
                continue
            contribution = feasible[(i, j)][1]
            candidate_min = contribution + rest[0]
            candidate_max = contribution + rest[1]
            if minimum is None or candidate_min < minimum[0]:
                minimum = candidate_min, (j,) + rest[2]
            if maximum is None or candidate_max > maximum[0]:
                maximum = candidate_max, (j,) + rest[3]
        if minimum is None:
            return None
        return minimum[0], maximum[0], minimum[1], maximum[1]

    # A second, independent matching optimization is essential when
    # ovule denominators vary. SCH primary fitness is intact seed
    # *count per flower*, not the fraction of a flower's ovules surviving.
    @lru_cache(maxsize=None)
    def solve_seed_counts(used_mask: int):
        i = used_mask.bit_count()
        if i == n:
            return 0, 0, (), ()
        minimum, maximum = None, None
        for j in range(n):
            if used_mask & (1 << j) or (i, j) not in feasible:
                continue
            rest = solve_seed_counts(used_mask | (1 << j))
            if rest is None:
                continue
            viable_count = feasible[(i, j)][0]
            candidate_min = viable_count + rest[0]
            candidate_max = viable_count + rest[1]
            if minimum is None or candidate_min < minimum[0]:
                minimum = candidate_min, (j,) + rest[2]
            if maximum is None or candidate_max > maximum[0]:
                maximum = candidate_max, (j,) + rest[3]
        if minimum is None:
            return None
        return minimum[0], maximum[0], minimum[1], maximum[1]

    result = solve(0)
    if result is None:
        raise ValueError(
            "NO_INTEGER_FEASIBLE_PERFECT_MATCHING: source q ratios cannot all "
            "be assigned to these initiated seed counts; check rounding, "
            "fate definitions and any ovule-count assumptions"
        )
    count_result = solve_seed_counts(0)
    if count_result is None:
        raise AssertionError("seed-count and fraction feasible graphs must agree")
    count_min, count_max, count_min_idx, count_max_idx = count_result
    sum_min, sum_max, min_idx, max_idx = result
    def witness(assignment: tuple[int, ...]) -> list[dict]:
        return [
            {
                "ovule_count": ovules,
                "initiated_count": initiated,
                "q_fraction": str(fractions[j]),
                "damaged_count": initiated - feasible[(i, j)][0],
                "viable_count": feasible[(i, j)][0],
            }
            for i, ((ovules, initiated), j) in enumerate(
                zip(pairs, assignment, strict=True)
            )
        ]
    min_witness, max_witness = witness(min_idx), witness(max_idx)
    min_count_witness = witness(count_min_idx)
    max_count_witness = witness(count_max_idx)
    low, high = float(sum_min/n), float(sum_max/n)
    relaxed = stage_bounds(
        [initiated / ovules for ovules, initiated in pairs],
        [float(q) for q in fractions],
    )
    relaxed_interval = [
        relaxed["minimum_possible_mean_viable_seed_fraction"],
        relaxed["maximum_possible_mean_viable_seed_fraction"],
    ]
    counts_sorted = sorted(initiated for _, initiated in pairs)
    q_sorted = list(fractions)
    mean_initiated = Fraction(sum(counts_sorted), n)
    count_relax_min = mean_initiated - sum(
        (k * q for k, q in zip(counts_sorted, q_sorted, strict=True)),
        Fraction(0)
    ) / n
    count_relax_max = mean_initiated - sum(
        (k * q for k, q in zip(counts_sorted, reversed(q_sorted), strict=True)),
        Fraction(0)
    ) / n
    count_relax_bounds = [float(count_relax_min), float(count_relax_max)]
    if (
        count_min/n < count_relax_bounds[0] - 1e-12
        or count_max/n > count_relax_bounds[1] + 1e-12
    ):
        raise AssertionError("integer seed count bounds outside relaxed count bounds")
    if low < relaxed_interval[0] - 1e-12 or high > relaxed_interval[1] + 1e-12:
        raise AssertionError("integer feasible bounds must lie in relaxed bounds")
    unique_ovules = {ovules for ovules, _ in pairs}
    output = {
        "n_equal_weight_fruits": n,
        "ovules_per_fruit": next(iter(unique_ovules)) if len(unique_ovules) == 1 else None,
        "ovule_count_heterogeneous": len(unique_ovules) > 1,
        "observed_ovule_initiation_pairs": [
            {"ovules": ovules, "initiated": initiated}
            for ovules, initiated in pairs
        ],
        "observed_initiation_count_multiset": [initiated for _, initiated in pairs],
        "observed_predation_ratio_multiset": [str(q) for q in fractions],
        "sharp_integer_feasible_mean_viable_fraction": [low, high],
        "exact_fractional_mean_viability_extrema": [
            str(sum_min/n), str(sum_max/n)
        ],
        "unrestricted_fractional_rearrangement_bounds": relaxed_interval,
        "unrestricted_fractional_rearrangement_mean_seed_count_bounds": (
            count_relax_bounds
        ),
        "sharp_integer_feasible_mean_viable_seeds_per_flower": [
            count_min/n, count_max/n
        ],
        "minimum_seed_count_attaining_matching": min_count_witness,
        "maximum_seed_count_attaining_matching": max_count_witness,
        "minimum_fitness_attaining_matching": min_witness,
        "maximum_fitness_attaining_matching": max_witness,
        "source_fruit_matches_reconstructed": False,
        "matching_is_just_a_feasible_witness": True,
        "n_dp_states_evaluated": solve.cache_info().currsize,
        "n_seed_count_dp_states_evaluated": solve_seed_counts.cache_info().currsize,
        "method": "EXACT_BITMASK_PERFECT_MATCHING_INTEGER_SEED_FATES",
    }
    if len(unique_ovules) == 1:
        output["integer_viable_total_seeds_extrema"] = [
            count_min, count_max
        ]
    return output


def integer_stage_bounds(
    initiated_counts: list[int],
    predation_fractions: list[str],
    ovules_per_fruit: int,
) -> dict:
    """Backward-compatible uniform-ovule special case."""
    n_ovules = _count(
        ovules_per_fruit, "ovules_per_fruit", minimum=1, maximum=1000000
    )
    if not isinstance(initiated_counts, list):
        raise ValueError("integer stage margins require 1..14 equal-length fruits")
    return integer_stage_bounds_variable_ovules(
        [{"ovules": n_ovules, "initiated": c} for c in initiated_counts],
        predation_fractions,
    )


def compare_settings_integer(
    low_initiated: list[int],
    low_q: list[str],
    high_initiated: list[int],
    high_q: list[str],
    ovules_per_fruit: int,
) -> dict:
    low = integer_stage_bounds(low_initiated, low_q, ovules_per_fruit)
    high = integer_stage_bounds(high_initiated, high_q, ovules_per_fruit)
    return _compare_stage_outputs(low, high)


def compare_settings_variable_ovules(
    low_fruits: list[dict[str, int]],
    low_q: list[str],
    high_fruits: list[dict[str, int]],
    high_q: list[str],
) -> dict:
    low = integer_stage_bounds_variable_ovules(low_fruits, low_q)
    high = integer_stage_bounds_variable_ovules(high_fruits, high_q)
    return _compare_stage_outputs(low, high)


def _compare_stage_outputs(low: dict, high: dict) -> dict:
    l0,l1 = low["sharp_integer_feasible_mean_viable_fraction"]
    h0,h1 = high["sharp_integer_feasible_mean_viable_fraction"]
    d0,d1 = h0-l1,h1-l0
    relaxed_low = low["unrestricted_fractional_rearrangement_bounds"]
    relaxed_high = high["unrestricted_fractional_rearrangement_bounds"]
    dr0,dr1 = relaxed_high[0]-relaxed_low[1],relaxed_high[1]-relaxed_low[0]
    clow = low["unrestricted_fractional_rearrangement_mean_seed_count_bounds"]
    chigh = high["unrestricted_fractional_rearrangement_mean_seed_count_bounds"]
    relaxed_count_delta = [chigh[0]-clow[1],chigh[1]-clow[0]]
    count_l0,count_l1 = low["sharp_integer_feasible_mean_viable_seeds_per_flower"]
    count_h0,count_h1 = high["sharp_integer_feasible_mean_viable_seeds_per_flower"]
    count_delta = [count_h0-count_l1,count_h1-count_l0]
    if count_delta[0] > 0:
        count_sign = "POSITIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    elif count_delta[1] < 0:
        count_sign = "NEGATIVE_FOR_ALL_INTEGER_FEASIBLE_COUPLINGS"
    else:
        count_sign = "SIGN_NOT_IDENTIFIED_ACROSS_INTEGER_FEASIBLE_COUPLINGS"
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
        "integer_feasible_high_minus_low_seed_count_per_flower_interval": count_delta,
        "SCH_primary_fitness_endpoint": "UNDAMAGED_MATURE_SEED_COUNT_PER_FLOWER",
        "SCH_primary_seed_count_selection_direction": count_sign,
        "per_flower_viable_fraction_selection_direction": sign,
        "count_and_fraction_direction_agree": count_sign == sign,
        "fractionally_relaxed_high_minus_low_interval": [dr0,dr1],
        "fractionally_relaxed_high_minus_low_seed_count_per_flower_interval": (
            relaxed_count_delta
        ),
        "integer_constraint_changes_SCH_primary_seed_count_sign_identifiability": (
            relaxed_count_delta[0] <= 0 <= relaxed_count_delta[1]
            and (count_delta[0] > 0 or count_delta[1] < 0)
        ),
        "integer_constraint_changes_sign_identifiability": (
            dr0 <= 0 <= dr1 and (d0 > 0 or d1 < 0)
        ),
        "high_minus_low_direction_given_margins": sign,
        "claim_ceiling": [
            "each_ovule_count_must_be_matched_to_its_own_initiated_count",
            "identical_ovules_per_fruit_not_required_in_variable_mode",
            "exact_unrounded_predation_rational_values_required",
            "no_zero_initiated_unrecognizable_full_destruction_or_0_over_0_fruits",
            "only_countable_intact_and_damaged_initiated_seeds_allowed",
            "at_most_fourteen_fruits_per_setting_due_to_exponential_runtime",
            "attaining_matches_are_math_witnesses_not_true_fruit_identifications",
            "equal_fruit_weight_not_weighted_population_reproductive_success",
            "viable_seed_counts_and_viable_seed_fractions_are_distinct_fitness_estimands",
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
    mode = payload.get("ovule_count_mode", "COMMON_OVULES_PER_FRUIT")
    if mode == "COMMON_OVULES_PER_FRUIT":
        for state in ("LOW", "HIGH"):
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
    elif mode == "VARIABLE_OVULES_PER_FRUIT":
        for state in ("LOW", "HIGH"):
            if not isinstance(margin[state], dict) or set(margin[state]) != {
                "ovule_and_initiated_counts", "predation_fractions"
            }:
                raise ValueError("each setting needs ovule/initiation pairs and ratios")
        result = compare_settings_variable_ovules(
            margin["LOW"]["ovule_and_initiated_counts"],
            margin["LOW"]["predation_fractions"],
            margin["HIGH"]["ovule_and_initiated_counts"],
            margin["HIGH"]["predation_fractions"],
        )
    else:
        raise ValueError("unregistered ovule_count_mode")
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

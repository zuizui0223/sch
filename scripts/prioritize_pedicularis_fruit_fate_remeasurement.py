"""Exact one-fruit ascertainment tipping points for SCH P. rex.

Given the source-locked nonconfirmatory allocation and factual viable-seed
intervals, quantify what a *complete maturity assessment* of a single
currently uncertain fruit could establish about pre-defined contrasts.

Unlike assigning a probability to an unknown fate, this reports INTEGER
ranges of possible observed surviving seed counts that would force a
positive or negative sign despite every *other* unresolved fruit outcome.
It also gives the exact decrease in contrast-interval width that measuring
a fruit would produce, independently of the result.

No one-fruit ascertainment guarantees resolving a currently unresolved
sign for all possible outcomes. "Would certify IF observed" !=
"will certify", and some destroyed fruits are impossible to recover.
"""
from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path

from scripts.bound_pedicularis_fruit_fate_selection import (
    _interpret, build as fitness_bounds, read as read_fate,
)
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256


SCHEMA="PEDICULARIS_FRUIT_FATE_ONE_FLOWER_TIPPING_POINT_V1"


def _exact(value: dict) -> Fraction:
    return Fraction(value["exact"])


def _floor(q: Fraction) -> int:
    return q.numerator // q.denominator


def _ceil(q: Fraction) -> int:
    return -((-q.numerator) // q.denominator)


def _allowed_integer_range(
    minimum: int, maximum: int, *, threshold: Fraction, relation: str
) -> dict | None:
    """Inclusive integer solution to x > threshold or x < threshold."""
    if relation == "GT":
        lo, hi = max(minimum, _floor(threshold) + 1), maximum
    elif relation == "LT":
        lo, hi = minimum, min(maximum, _ceil(threshold) - 1)
    else:
        raise ValueError("unknown threshold relation")
    if lo > hi:
        return None
    return {
        "minimum_viable_seeds_if_measured": lo,
        "maximum_viable_seeds_if_measured": hi,
        "n_integer_values": hi-lo+1,
    }


def one_fruit_sign_tipping(
    *,
    contrast_lower: Fraction,
    contrast_upper: Fraction,
    n_fruits_in_target_cell: int,
    current_viable_lower: int,
    current_viable_upper: int,
    cell_direction: int,
) -> dict:
    """Return exact conditional single-fruit certification thresholds.

    "cell_direction" is +1 when target cell contributes positively to
    the contrast (high-z or EXCLUDED), -1 when it contributes negatively
    (low-z or EXPOSED).
    """
    if (
        not isinstance(contrast_lower, Fraction)
        or not isinstance(contrast_upper, Fraction)
        or contrast_lower > contrast_upper
        or type(n_fruits_in_target_cell) is not int or n_fruits_in_target_cell < 1
        or type(current_viable_lower) is not int
        or type(current_viable_upper) is not int
        or current_viable_lower < 0
        or current_viable_upper < current_viable_lower
        or cell_direction not in (-1, 1)
    ):
        raise ValueError("invalid interval or signed contrast input")
    a,b=current_viable_lower,current_viable_upper
    n=n_fruits_in_target_cell
    if cell_direction == 1:
        # After x is observed:
        # lower(x) = original_lower + (x-a)/n
        # upper(x) = original_upper - (b-x)/n
        positive = _allowed_integer_range(
            a,b,threshold=Fraction(a)-n*contrast_lower,relation="GT"
        )
        negative = _allowed_integer_range(
            a,b,threshold=Fraction(b)-n*contrast_upper,relation="LT"
        )
    else:
        # lower(x) = original_lower + (b-x)/n
        # upper(x) = original_upper - (x-a)/n
        positive = _allowed_integer_range(
            a,b,threshold=Fraction(b)+n*contrast_lower,relation="LT"
        )
        negative = _allowed_integer_range(
            a,b,threshold=Fraction(a)+n*contrast_upper,relation="GT"
        )
    pos_count=0 if positive is None else positive["n_integer_values"]
    neg_count=0 if negative is None else negative["n_integer_values"]
    total=b-a+1
    unresolved=total-pos_count-neg_count
    if unresolved < 0:
        raise AssertionError("sign-certifying outcome ranges overlap")
    return {
        "possible_measured_viable_seed_interval": [a,b],
        "total_integer_viable_seed_outcomes": total,
        "would_certify_positive_if_observed_count_in": positive,
        "would_certify_negative_if_observed_count_in": negative,
        "n_measured_values_that_would_leave_sign_unresolved": unresolved,
        "n_measured_values_that_would_certify_either_sign": pos_count+neg_count,
        "maximum_contrast_interval_width_reduction": {
            "exact": str(Fraction(b-a,n)),
            "value": float(Fraction(b-a,n)),
        },
        "sign_certification_is_conditional_on_future_observed_value": True,
        "outcome_value_enumeration_is_not_a_predictive_probability": True,
    }


def _contrast_sign(lower: Fraction,upper: Fraction) -> str:
    if lower>0:
        return "ALREADY_POSITIVE"
    if upper<0:
        return "ALREADY_NEGATIVE"
    return "CURRENTLY_UNRESOLVED"


def build(rows: list[dict[str,str]], allocation: dict) -> dict:
    base=fitness_bounds(rows,allocation)  # strict all-flower source checks
    n_z=allocation["n_z_levels"]
    if type(n_z) is not int or n_z < 5:
        raise ValueError("n_z_levels must be frozen positive integer")
    candidates=[]
    for row in rows:
        x=_interpret(row)
        lo,hi=x["seed_fitness_lower"],x["seed_fitness_upper"]
        if hi<=lo:
            continue
        rank=x["assigned_z_rank"]
        g=x["predator_treatment"]
        n=base["mean_fitness_by_predator_treatment_and_z"][g][str(rank)][
            "n_all_allocated_flowers"
        ]
        affected=[]
        if rank in (0,n_z-1):
            contrast=base["extreme_z_fitness_selection_contrasts"][g]
            b=contrast["high_minus_low_viable_seed_count_per_flower_bounds"]
            lower,upper=_exact(b[0]),_exact(b[1])
            t=one_fruit_sign_tipping(
                contrast_lower=lower,contrast_upper=upper,
                n_fruits_in_target_cell=n,
                current_viable_lower=lo,current_viable_upper=hi,
                cell_direction=(1 if rank==n_z-1 else -1)
            )
            affected.append({
                "contrast":"HIGH_MINUS_LOW_Z",
                "predator_treatment":g,
                "current_sign":_contrast_sign(lower,upper),
                "conditional_ascertainment":t,
            })
        pred=base["predator_exclusion_fitness_differences_by_z"][str(rank)]
        b=pred["excluded_minus_exposed_viable_seed_count_bounds"]
        lower,upper=_exact(b[0]),_exact(b[1])
        t=one_fruit_sign_tipping(
            contrast_lower=lower,contrast_upper=upper,
            n_fruits_in_target_cell=n,
            current_viable_lower=lo,current_viable_upper=hi,
            cell_direction=(1 if g=="EXCLUDED" else -1)
        )
        affected.append({
            "contrast":"EXCLUDED_MINUS_EXPOSED_AT_Z",
            "rank":rank,
            "current_sign":_contrast_sign(lower,upper),
            "conditional_ascertainment":t,
        })
        unresolved_current=sum(
            item["current_sign"]=="CURRENTLY_UNRESOLVED"
            for item in affected
        )
        resolvable_current=sum(
            item["current_sign"]=="CURRENTLY_UNRESOLVED"
            and item["conditional_ascertainment"][
                "n_measured_values_that_would_certify_either_sign"
            ]>0
            for item in affected
        )
        reduction=Fraction(hi-lo,n)
        candidates.append({
            "flower_id":x["flower_id"],
            "plant_id":x["plant_id"],
            "assigned_z_rank":rank,
            "predator_treatment":g,
            "current_fate_status":x["fate_status"],
            "observed_viable_seed_lower":lo,
            "observed_viable_seed_upper":hi,
            "n_other_unresolved_fruits_not_assumed_resolved":True,
            "maximum_cell_mean_bound_width_reduction":{
                "exact":str(reduction),"value":float(reduction)
            },
            "n_affected_currently_unresolved_contrasts":unresolved_current,
            "n_unresolved_contrasts_with_attainable_single_fruit_sign_certification":resolvable_current,
            "affected_prespecified_contrasts":affected,
            "actual_cause_or_P_exposure_cannot_be_ascertained_by_viable_yield_alone":True,
        })
    candidates.sort(
        key=lambda item: (
            -item["n_unresolved_contrasts_with_attainable_single_fruit_sign_certification"],
            -item["n_affected_currently_unresolved_contrasts"],
            -Fraction(item["maximum_cell_mean_bound_width_reduction"]["exact"]),
            item["flower_id"],
        )
    )
    for i,row in enumerate(candidates,start=1):
        row["conditional_measurement_priority_rank"]=i
    return {
        "receipt_schema":SCHEMA,
        "status":"NON_GATING_ONE_FLOWER_OUTCOME_TIPPING_POINTS",
        "population_id":base["population_id"],
        "season_id":base["season_id"],
        "source_fate_bounds_receipt_sha256":_semantic_sha256(base),
        "n_original_allocated_flowers":base["n_all_allocated_flowers"],
        "n_currently_uncertain_viable_fruit_outcomes":len(candidates),
        "prioritized_conditional_remeasurements":candidates,
        "current_finite_sample_optimum_shift_outer_bound":base[
            "excluded_minus_exposed_optimum_rank_shift_outer_bound"
        ],
        "optimum_shift_after_one_remeasurement_not_claimed":True,
        "future_measurement_result_probabilities_calculated":False,
        "a_completely_lost_fruit_may_be_unrecoverable_retrospectively":True,
        "claim_ceiling":[
            "each_tipping_range_is_conditional_on_exact_ascertainment_of_one_fruit",
            "other_unknown_fruit_outcomes_remain_at_original_bounds",
            "number_of_possible_integer_values_is_not_a_probability",
            "priority_is_information_geometry_not_expected_field_value_or_cost",
            "confirmed_zero_viable_fitness_does_not_identify_predation_q",
            "source_caps_and_field_provenance_not_independently_authenticated",
            "optimizing_sign_certification_not_statistical_power_or_population_CI",
            "no_p0_p1_g_w1_w2_or_pure_function_promotion",
        ],
    }


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("complete_fruit_fate_csv",type=Path)
    parser.add_argument("frozen_fruit_allocation_json",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=build(
        read_fate(args.complete_fruit_fate_csv),
        json.loads(args.frozen_fruit_allocation_json.read_text(encoding="utf-8")),
    )
    serialized=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized,encoding="utf-8")
    else:
        print(serialized,end="")


if __name__=="__main__":
    main()

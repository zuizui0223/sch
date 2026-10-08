"""Conditional missing-capsule sensitivity for published P. rex predation extremes.

Sun et al. (2016) could not score up to five entirely consumed capsules per
population. This is NOT raw-data correction: exact countable n, excluded m,
and population aggregation grain are unavailable. Calculates transparent
equal-capsule-weight envelopes under explicitly hypothetical denominators.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


DOI = "10.1093/aob/mcw097"
LOW_PUBLISHED = {"population": 11, "reported_fraction": 0.0080}
HIGH_PUBLISHED = {"population": 5, "reported_fraction": 0.2742}
MAX_UNSCORABLE_PER_POPULATION = 5


def envelope(reported_fraction: float, assessable_capsules: int, missing: int) -> dict:
    if not isinstance(assessable_capsules, int) or assessable_capsules <= 0:
        raise ValueError("assessable_capsules must be a positive integer")
    if not isinstance(missing, int) or not 0 <= missing <= 5:
        raise ValueError("missing must lie in the published [0, 5] range")
    if not math.isfinite(reported_fraction) or not 0 <= reported_fraction <= 1:
        raise ValueError("reported predation fraction must lie in [0, 1]")
    n, m, p = assessable_capsules, missing, reported_fraction
    return {
        "hypothetical_assessable_capsules": n,
        "hypothetical_unscorable_capsules": m,
        "published_fraction_among_assessable": p,
        "bounds_if_unscorable_unit_risks_can_be_anywhere_0_to_1": [
            n * p / (n + m),
            (n * p + m) / (n + m),
        ],
        "hypothetical_all_missing_fully_predated_fraction": (n * p + m) / (n + m),
        "source_probability_mean_is_assumed_equal_capsule_weighted": True,
    }


def build(
    hypothetical_assessable_n: int = 115,
    maximum_missing_per_population: int = MAX_UNSCORABLE_PER_POPULATION,
) -> dict:
    if maximum_missing_per_population != MAX_UNSCORABLE_PER_POPULATION:
        raise ValueError("source-published maximum missing-capsule count must remain five")
    if not isinstance(hypothetical_assessable_n, int) or hypothetical_assessable_n <= 0:
        raise ValueError("assessable denominator scenario must be positive integer")
    low = envelope(LOW_PUBLISHED["reported_fraction"],
                   hypothetical_assessable_n, maximum_missing_per_population)
    high = envelope(HIGH_PUBLISHED["reported_fraction"],
                    hypothetical_assessable_n, maximum_missing_per_population)
    high_min = high["bounds_if_unscorable_unit_risks_can_be_anywhere_0_to_1"][0]
    low_max = low["bounds_if_unscorable_unit_risks_can_be_anywhere_0_to_1"][1]
    gap = high_min - low_max
    raw_gap = HIGH_PUBLISHED["reported_fraction"] - LOW_PUBLISHED["reported_fraction"]
    smallest_integer_n_with_positive_worst_case_gap = (
        math.floor(maximum_missing_per_population / raw_gap) + 1
    )
    # If each population has at least this many assessable capsules,
    # and at most five missing, the high source population remains
    # above the low source population under the explicit equal-weight
    # capsule aggregation model. Not a proof for plant-averaged rates.
    assert smallest_integer_n_with_positive_worst_case_gap == 19

    return {
        "analysis": "pedicularis_2016_population_extremes_missing_capsule_bound_v1",
        "source_doi": DOI,
        "reported_low_population": LOW_PUBLISHED,
        "reported_high_population": HIGH_PUBLISHED,
        "source_reported_max_unscorable_capsules_per_population": 5,
        "original_usual_field_collection": (
            "approximately_six_capsules_on_twenty_plants_per_population_"
            "not_equal_to_verified_analyzable_n"
        ),
        "scenario_countable_capsules_per_population": hypothetical_assessable_n,
        "scenario_bounds_for_low": low,
        "scenario_bounds_for_high": high,
        "worst_case_high_minus_low_fraction": gap,
        "minimum_assessable_n_per_population_to_preserve_ranking_under_model": (
            smallest_integer_n_with_positive_worst_case_gap
        ),
        "worst_case_high_still_greater_than_low_under_model": gap > 0,
        "assumptions": [
            "population_published_rate_is_unweighted_mean_of_assessable_capsule_fractions",
            "each_missing_capsule_fraction_is_in_0_to_1",
            "at_most_five_missing_capsules_in_each_population",
            "published_percentages_represent_same_sample_definition",
            "hypothetical_n_not_verified_per_population",
        ],
        "no_claims": [
            "not_an_actual_correction_of_published_rates",
            "does_not_estimate_source_missingness_or_latent_censored_seed_counts",
            "plant_level_weighting_or_unknown_fruit_fate_invalidates_equal_capsule_envelope",
            "no_inference_about_exsertion_specific_selection_or_causal_G",
        ],
        "status": "MISSING_CAPSULE_SENSITIVITY_ONLY_RAW_GRAIN_NOT_VERIFIED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hypothetical-assessable-n", type=int, default=115)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.hypothetical_assessable_n)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

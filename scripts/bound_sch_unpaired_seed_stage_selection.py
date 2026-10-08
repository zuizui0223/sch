"""Sharp finite-sample bounds for fitness selection when seed formation and
predation margins are measured, but NOT matched by fruit.

For the same equally weighted set of n hypothetical/observed fruit-stage
units within each randomized trait-setting rank, define
I_i = fraction of ovules with distinguishably initiated seeds (>0),
q_i = fraction of distinguishably initiated seeds predated.
Fitness F_i = I_i (1-q_i) = final intact seed fraction (given complete fates).

When only the unordered empirical multisets {I_i} and {q_i} are available,
the rearrangement inequality gives SHARP bounds for E[F]:
maximal product E[I q] by similarly sorting I and q, minimal product
by opposite sorting. No independence or invented within-fruit matching.

This bound is NOT an estimator of causal selection for observational z, and
does not by itself resolve 0/0 fruit fate, hidden predation or unequal weights.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import mean

SCHEMA = "SCH_UNPAIRED_SEED_STAGE_MARGINAL_BOUNDS_V1"
STATUS = "SHARP_EMPIRICAL_COUPLING_BOUNDS_NOT_A_CAUSAL_SELECTION_TEST"
ALLOWED_CHANNELS = ("INITIATION_FRACTION", "PREDATION_FRACTION")


def _fraction(x: object, name: str, *, strictly_positive: bool = False) -> float:
    try:
        val = float(x)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name}: fraction must be numeric") from exc
    if not math.isfinite(val) or not (0 <= val <= 1):
        raise ValueError(f"{name}: fraction must be finite in [0,1]")
    if strictly_positive and val == 0:
        raise ValueError(
            "seed-predation fraction is not defined with zero distinguishable "
            "initiated seeds; retain ambiguous fruits separately"
        )
    return val


def stage_bounds(
    initiation: list[float],
    predation: list[float],
) -> dict:
    """Sharp equal-weight coupling bounds with complete positive-I fates."""
    if not initiation or len(initiation) != len(predation):
        raise ValueError("equal-length nonempty stage marginal samples required")
    s = sorted(_fraction(x, "initiation", strictly_positive=True) for x in initiation)
    q = sorted(_fraction(x, "predation") for x in predation)
    n = len(s)
    mean_i = mean(s)
    mean_q = mean(q)
    comonotone_product = sum(a*b for a,b in zip(s,q,strict=True))/n
    countermonotone_product = sum(a*b for a,b in zip(s,reversed(q),strict=True))/n
    minimum_fitness = mean_i-comonotone_product
    maximum_fitness = mean_i-countermonotone_product
    if minimum_fitness < -1e-12 or maximum_fitness > 1+1e-12:
        raise ValueError("bound violates physical fitness range")
    return {
        "n_equal_weight_fruit_units": n,
        "mean_initiation": mean_i,
        "mean_predation": mean_q,
        "minimum_possible_mean_viable_seed_fraction": max(0.0, minimum_fitness),
        "maximum_possible_mean_viable_seed_fraction": min(1.0, maximum_fitness),
        "max_covariance": comonotone_product - mean_i*mean_q,
        "min_covariance": countermonotone_product - mean_i*mean_q,
        "bound_method": "REARRANGEMENT_SHARP_EQUAL_WEIGHT_UNPAIRED_MARGINALS",
        "not_per_fruit_fitness_observation": True,
    }


def compare_settings(
    low_initiation: list[float],
    low_predation: list[float],
    high_initiation: list[float],
    high_predation: list[float],
) -> dict:
    low = stage_bounds(low_initiation, low_predation)
    high = stage_bounds(high_initiation, high_predation)
    delta_lower = (
        high["minimum_possible_mean_viable_seed_fraction"]
        - low["maximum_possible_mean_viable_seed_fraction"]
    )
    delta_upper = (
        high["maximum_possible_mean_viable_seed_fraction"]
        - low["minimum_possible_mean_viable_seed_fraction"]
    )
    if delta_lower > 0:
        status = "POSITIVE_HIGH_MINUS_LOW_SIGN_FIXED_ACROSS_ALL_COUPLINGS"
    elif delta_upper < 0:
        status = "NEGATIVE_HIGH_MINUS_LOW_SIGN_FIXED_ACROSS_ALL_COUPLINGS"
    else:
        status = "TRAIT_FITNESS_SIGN_NOT_IDENTIFIED_BY_MARGINALS"
    return {
        "schema": SCHEMA,
        "status": STATUS,
        "low_z_setting": low,
        "high_z_setting": high,
        "sharp_high_minus_low_fitness_interval": [delta_lower, delta_upper],
        "selection_sign_given_only_stage_marginals": status,
        "sign_is_a_causal_selection_response_without_randomized_z": False,
        "claim_ceiling": [
            "source_lists_must_be_actual_unweighted_equal_size_marginals_not_just_means",
            "different_sample_units_or_weights_need_new_coupling_bounds",
            "integer_ovule_and_seed_constraints_can_tighten_continuous_fraction_pairing_bounds",
            "matching_not_reconstructed_by_arbitrary_pairing",
            "I_positive_and_true_fruit_fate_required_for_predation_q",
            "unrecognized_total_consumption_breaks_I_q_observability",
            "physical_z_assignment_needed_for_causal_trait_response",
            "sharp_finite_empirical_bounds_not_population_confidence_intervals",
            "does_not_identify_pollination_agent_or_SCH_pure_function_optima",
        ],
    }


def _read(path: Path) -> dict[str, dict[str, list[float]]]:
    """Read long-form empirical marginal samples (never pair by row number)."""
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or not {
            "setting", "channel", "value"
        }.issubset(reader.fieldnames):
            raise ValueError("marginal CSV requires setting,channel,value")
        out = {
            "LOW": {ch: [] for ch in ALLOWED_CHANNELS},
            "HIGH": {ch: [] for ch in ALLOWED_CHANNELS},
        }
        for row in reader:
            setting = row["setting"].strip()
            channel = row["channel"].strip()
            if setting not in out or channel not in ALLOWED_CHANNELS:
                raise ValueError("unregistered setting/channel in marginal sample")
            out[setting][channel].append(_fraction(row["value"], channel))
    return out


def build_from_csv(path: Path) -> dict:
    observations = _read(path)
    L, H = observations["LOW"], observations["HIGH"]
    return compare_settings(
        L["INITIATION_FRACTION"], L["PREDATION_FRACTION"],
        H["INITIATION_FRACTION"], H["PREDATION_FRACTION"],
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("marginal_csv", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = build_from_csv(args.marginal_csv)
    text = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

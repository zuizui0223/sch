"""Variance-aware, patch-cluster simultaneous P. rex reproductive-optimum bands.

This is a non-gating companion to the source-locked Hoeffding certificate.
Each independently randomized/sampled ten-mother patch-stage batch provides
ONE observation of every G-by-z mean. For each predator arm, 10 unordered
within-arm rank differences are analysed, with their source-valid missing
maturity lower/upper envelopes kept intact.

The one-sided empirical Bernstein inequality (Maurer & Pontil 2009, Thm. 11)
with failure probability delta=alpha/40 per endpoint gives, for independent
bounded batch contrasts X_b in [-K,K], B>=2:

    E[X] >= mean(X) - sqrt(2 s^2 log(2/delta)/B)
                       - 7 (2K) log(2/delta)/(3(B-1)),

and its upper-tail counterpart. Apply to the 20 lower and 20 upper
source-fate envelopes, protecting all 40 endpoints by a union bound.
The resulting 20 paired intervals enclose the contrast of mean viable seed
output under the source-validated assumptions. The pairwise-bound rank
projection is inherited from the existing SCH Hoeffding implementation.

Independent PATCH sampling/randomization and a true precommitted physical
seed cap are conditional assumptions, not established by a GitHub receipt.
For non-identically distributed independent patches the result targets the
mean of enrolled-patch expectations; population transport additionally
requires representative patch sampling. There is NO P. rex field evidence.
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

from scripts.certify_pedicularis_simultaneous_optimum_rank import (
    STATES,
    Z_RANKS,
    _rank_sets_from_pair_bands,
    simultaneous_from_batch_cell_bounds,
    build as _source_locked_hoeffding_build,
)

SCHEMA = "PEDICULARIS_TWO_FLOWER_PATCH_EMPIRICAL_BERNSTEIN_OPTIMUM_V1"
METHOD = "MAURER_PONTIL_PATCH_CONTRAST_EMPIRICAL_BERNSTEIN_40_ENDPOINTS"


def empirical_bernstein_one_sided_radius(
    sample: list[Fraction], *, global_seed_cap: int, endpoint_delta: float
) -> dict:
    """Valid one-sided bound for a contrast in [-K,K], B>=2.

    sample variance is UNBIASED (B-1 denominator); do not use numpy's
    ddof=0 default. Never substitute the *observed* range for 2K.
    """
    if type(global_seed_cap) is not int or global_seed_cap <= 0:
        raise ValueError("global seed cap must be a positive integer")
    if not 0 < endpoint_delta < 1 or not math.isfinite(endpoint_delta):
        raise ValueError("endpoint_delta must be in (0,1)")
    if len(sample) < 2:
        raise ValueError("at least two independent patch observations required")
    if any(not -global_seed_cap <= value <= global_seed_cap for value in sample):
        raise ValueError("contrast exceeds registered global seed cap")
    n = len(sample)
    center = sum(sample, Fraction(0)) / n
    variance = sum(((value-center)**2 for value in sample), Fraction(0))/(n-1)
    t = math.log(2.0/endpoint_delta)
    stochastic = math.sqrt(2.0*float(variance)*t/n)
    bounded = 14.0*global_seed_cap*t/(3.0*(n-1))
    return {
        "empirical_mean": float(center),
        "sample_variance_ddof1": float(variance),
        "variance_term": stochastic,
        "range_term": bounded,
        "one_sided_radius_before_physical_clipping": stochastic+bounded,
    }


def empirical_bernstein_from_patch_cell_bounds(
    patch_batches: list[dict], *,
    registered_global_viable_seed_cap: int,
    alpha: float = .05,
) -> dict:
    """Produce jointly covered best-rank outer sets from independent patches.

    The existing source-aware companion validates all patch identifiers,
    stage provenance, five ranks, both predator states, intervals and K.
    Its Hoeffding result is retained as a separate diagnostic, not
    intersected with these 95%-at-alpha empirical Bernstein intervals:
    intersecting two individually 95% methods WOULD NOT preserve 95%.
    """
    baseline = simultaneous_from_batch_cell_bounds(
        patch_batches,
        registered_global_viable_seed_cap=registered_global_viable_seed_cap,
        alpha=alpha,
    )
    B = baseline["n_independent_patch_stage_batches"]
    K = registered_global_viable_seed_cap
    m = baseline["n_simultaneous_two_sided_pairwise_difference_bands"]
    assert m == 20
    endpoint_delta = alpha/(2*m)
    pairs: dict[tuple[str,int,int],tuple[float,float]] = {}
    rows = []
    for g in STATES:
        for a in Z_RANKS:
            for b in Z_RANKS:
                if a >= b:
                    continue
                # Fraction handles source-fate averaged half-seeds exactly.
                lower = [
                    Fraction(batch["cells"][(g,a)][0])
                    - Fraction(batch["cells"][(g,b)][1])
                    for batch in patch_batches
                ]
                upper = [
                    Fraction(batch["cells"][(g,a)][1])
                    - Fraction(batch["cells"][(g,b)][0])
                    for batch in patch_batches
                ]
                lo_stats = empirical_bernstein_one_sided_radius(
                    lower, global_seed_cap=K, endpoint_delta=endpoint_delta,
                )
                hi_stats = empirical_bernstein_one_sided_radius(
                    upper, global_seed_cap=K, endpoint_delta=endpoint_delta,
                )
                lo = max(-float(K), lo_stats["empirical_mean"]
                         - lo_stats["one_sided_radius_before_physical_clipping"])
                hi = min(float(K), hi_stats["empirical_mean"]
                         + hi_stats["one_sided_radius_before_physical_clipping"])
                if lo > hi:
                    raise AssertionError("simultaneous empirical Bernstein band inverted")
                pairs[(g,a,b)] = (lo,hi)
                rows.append({
                    "predator_treatment": g,
                    "rank_a": a,
                    "rank_b": b,
                    "finite_allocated_batch_mean_fate_interval": [
                        lo_stats["empirical_mean"],hi_stats["empirical_mean"]
                    ],
                    "conditional_joint_coverage_band": [lo,hi],
                    "lower_endpoint_sample_variance_ddof1": lo_stats["sample_variance_ddof1"],
                    "upper_endpoint_sample_variance_ddof1": hi_stats["sample_variance_ddof1"],
                    "lower_endpoint_radius_before_clipping": lo_stats[
                        "one_sided_radius_before_physical_clipping"
                    ],
                    "upper_endpoint_radius_before_clipping": hi_stats[
                        "one_sided_radius_before_physical_clipping"
                    ],
                })
    rank_sets = _rank_sets_from_pair_bands(pairs)
    return {
        "receipt_schema": SCHEMA,
        "status": "SYNTHETIC_TESTED_CONDITIONAL_NOT_FIELD_CERTIFIED",
        "method": METHOD,
        "alpha": alpha,
        "nominal_simultaneous_coverage_given_independent_batches_and_valid_cap": 1-alpha,
        "n_independent_patch_stage_batches": B,
        "n_original_distinct_mother_plants_per_batch": 10,
        "n_original_fruit_flowers_per_batch": 20,
        "n_simultaneous_pairs": m,
        "n_one_sided_endpoints": 2*m,
        "bonferroni_failure_probability_per_endpoint": endpoint_delta,
        "registered_global_viable_seed_cap": K,
        "all_contrast_intervals": rows,
        "patch_level_simultaneous_enrolled_batch_mean_rank_sets": rank_sets,
        "positive_optimum_shift_certified_conditional_on_assumptions": (
            rank_sets["simultaneous_rank_shift_direction"]
            == "GUARANTEED_POSITIVE_OPTIMUM_RANK_SHIFT_WITHIN_BAND"
        ),
        "hoeffding_companion_positive_certificate_at_same_nominal_alpha": baseline[
            "positive_optimum_shift_certified_conditional_on_assumptions"
        ],
        "hoeffding_companion_does_not_share_joint_coverage_with_this_interval": True,
        "no_field_verified_G_selectivity_z_first_stage_or_maturity_cap": True,
        "not_a_plant_label_Fisher_randomization_test": True,
        "not_a_focal_P_rex_field_effect_or_recruitment_recommendation": True,
        "claim_ceiling": [
            "source_valid_K_binds_all_potential_mature_viable_seed_counts",
            "independent_complete_patch_stage_batch_vector_is_only_replicate",
            "repeated_patch_at_different_stage_not_independent",
            "within_patch_flower_and_mother_covariance_allowed",
            "20_pairwise_contrasts_and_40_one_sided_endpoints_familywise_protected",
            "source_unknown_fates_retained_as_lower_and_upper_bounds",
            "per_endpoint_variances_are_from_patch_contrasts_not_seed_or_flower_level",
            "source_representation_must_be_justified_for_population_transport",
            "band_family_not_intersected_with_same_alpha_hoeffding_family",
            "effect_magnitude_variance_and_cap_in_synthetic_examples_are_hypothetical",
            "no_SCH_function_optimum_L_or_SLK_architecture_promotion",
        ],
    }


def build(
    source_flower_rows: list[dict], frozen_allocation_receipt: dict, *,
    registered_global_viable_seed_cap: int,
    alpha: float = .05,
) -> dict:
    """Source-lock all flowers, intact seed intervals and z/G assignment."""
    from scripts.analyze_pedicularis_two_flower_cyclic_fruit_bounds import (
        build as verify_candidate_fruit_fates,
    )
    baseline = _source_locked_hoeffding_build(
        source_flower_rows,
        frozen_allocation_receipt,
        registered_global_viable_seed_cap=registered_global_viable_seed_cap,
        alpha=alpha,
    )
    source = verify_candidate_fruit_fates(source_flower_rows,frozen_allocation_receipt)
    patches = []
    for entry in source["patch_stage_cell_sensitivity"]:
        cells = {
            (cell["predator_treatment"],cell["assigned_z_rank"]): tuple(
                Fraction(v) for v in cell["mean_intact_seed_count_bounds"]
            )
            for cell in entry["cells"]
        }
        patches.append({
            "patch_id":entry["patch_id"],
            "stage_block_id":entry["stage_block_id"],
            "cells":cells,
        })
    result = empirical_bernstein_from_patch_cell_bounds(
        patches,
        registered_global_viable_seed_cap=registered_global_viable_seed_cap,
        alpha=alpha,
    )
    result.update({
        "source_population": baseline["source_population"],
        "source_season": baseline["source_season"],
        "source_allocation_identity_sha256":baseline["source_allocation_identity_sha256"],
        "source_fate_analysis_sha256":baseline["source_fate_analysis_sha256"],
        "original_registered_flower_count":baseline["original_registered_flower_count"],
        "n_source_fruit_outcomes_unresolved":baseline["n_source_fruit_outcomes_unresolved"],
    })
    return result


def main() -> None:
    from scripts.plan_pedicularis_two_flower_cyclic_blocks import _rows_csv
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("allocated_fruit_fate_csv",type=Path)
    p.add_argument("frozen_two_flower_design_receipt",type=Path)
    p.add_argument("--registered-seed-cap",type=int,required=True)
    p.add_argument("--alpha",type=float,default=.05)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    report=build(
        _rows_csv(a.allocated_fruit_fate_csv),
        json.loads(a.frozen_two_flower_design_receipt.read_text(encoding="utf-8")),
        registered_global_viable_seed_cap=a.registered_seed_cap,
        alpha=a.alpha,
    )
    content=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(content,encoding="utf-8")
    else:
        print(content,end="")


if __name__=="__main__":
    main()

"""Simultaneous uncertainty bands for ALL P. rex finite-grid reproductive optima.

Designed for the candidate 2-flower/cyclic experiment with whole-plant
predator G randomization. First validate every source-locked allocated flower
and its exact/zero/censored mature seed fate with the existing two-flower
fruit outcome analyzer. Aggregate two *distinct plants* at every z x G within
each independently sampled/assigned patch-stage batch, NEVER independent
flowers or ten z x G cells as independent observations.

At all 20 UNORDERED z-vs-z comparisons (10 per G), form lower/upper
batch differences of the intact seed count/flower outcome, including unknown
fruit outcomes as their registered [0, seed-potential-cap] intervals.

Conditional on:
 - pre-specified global intact seed cap K bounding EVERY eligible source
   flower in ALL population/assignment draws (not max observed count);
 - independent PATCH-STAGE batch outcome vectors, each with valid prospective
   two-flower/plant randomization, bounded intact viable seed count;
 - comparable patch/stage target populations and no between-plant G spillover;
the one-sided Hoeffding union bound over 2 endpoints x 20 comparisons yields
a simultaneous (1-alpha) confidence enclosure of each *population-average*
G-conditional z-rank mean difference.

For batch count B and differences in [-K,K]:
    eps = K * sqrt(2 log(40 / alpha) / B)
and each pair (g,za,zb) is enclosed by
 [mean_b(lower_ga - upper_gb) - eps,
  mean_b(upper_ga - lower_gb) + eps], clipped to [-K,K].

Because each of the twenty pairwise differences is simultaneously covered,
a true maximizing rank cannot be eliminated by a lower bound showing another
rank strictly better. Comparing the remaining best-rank sets between G
states provides a conservative confidence-backed *direction* of the
optimum displacement. This is NOT a conditional Fisher randomization
test, not an efficient small-B interval, not evidence of qualified G/P0,
and not a confidence band on pure pollination/antagonist optima.

Most importantly, NEVER turn a sample-level argmax or a p-value from a
different Fisher sharp null into a weak-null optimum-shift conclusion.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from fractions import Fraction
from pathlib import Path

from scripts.analyze_pedicularis_two_flower_cyclic_fruit_bounds import (
    build as verify_candidate_fruit_fates,
)
from scripts.plan_pedicularis_two_flower_cyclic_blocks import _rows_csv
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256

SCHEMA = "PEDICULARIS_TWO_FLOWER_SIMULTANEOUS_OPTIMUM_CERTIFICATE_V1"
STATES = ("EXCLUDED", "EXPOSED")
Z_RANKS = tuple(range(5))
N_UNORDERED_PAIRS_PER_ARM = 10
N_TOTAL_SIMULTANEOUS_PAIRS = 20
KIND = "DISTRIBUTION_FREE_HOEFFDING_PATCH_BLOCK_BOUNDED_RESPONSE"


def _finite_int(value: object, label: str, min_value: int, max_value: int) -> int:
    if type(value) is not int or not min_value <= value <= max_value:
        raise ValueError(
            f"{label} must be integer within [{min_value}, {max_value}]"
        )
    return value


def _probability(alpha: object) -> float:
    if type(alpha) not in (int,float) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("simultaneous alpha must be a finite number in (0,1)")
    return float(alpha)


def _rank_sets_from_pair_bands(
    pairs: dict[tuple[str,int,int], tuple[float,float]]
) -> dict:
    """Eliminate only a rank proved inferior to another at SAME G.

    For F_a-F_b confidence band [l,u] with a<b:
        F_a>F_b certified if l>0;
        F_b>F_a certified if u<0.
    Remaining rank set jointly includes ALL true optimizing ranks whenever
    all 20 simultaneous bands cover their mean differences.
    """
    surviving = {}
    exclusions = {}
    for g in STATES:
        possible = []
        eliminated = []
        for rank in Z_RANKS:
            better = []
            for contender in Z_RANKS:
                if contender == rank:
                    continue
                a,b = sorted((rank,contender))
                if (g,a,b) not in pairs:
                    raise ValueError("must provide all twenty within-G z pair bands")
                lo,hi = pairs[(g,a,b)]
                if not lo<=hi:
                    raise ValueError("inverted simultaneous difference interval")
                # Contender has strictly greater mean than focal rank.
                if ((contender == a and lo > 0)
                    or (contender == b and hi < 0)):
                    better.append(contender)
            if better:
                eliminated.append({
                    "z_rank": rank,
                    "individually_certified_better_rank_candidates": better,
                })
            else:
                possible.append(rank)
        if not possible:
            raise AssertionError("simultaneous rank comparisons removed all optima")
        surviving[g]=possible
        exclusions[g]=eliminated
    ex,ep = surviving["EXCLUDED"],surviving["EXPOSED"]
    low,high=min(ex)-max(ep), max(ex)-min(ep)
    if low>0:
        direction="GUARANTEED_POSITIVE_OPTIMUM_RANK_SHIFT_WITHIN_BAND"
    elif high<0:
        direction="GUARANTEED_NEGATIVE_OPTIMUM_RANK_SHIFT_WITHIN_BAND"
    elif low==high==0:
        direction="GUARANTEED_ZERO_SHIFT_WITHIN_BAND"
    else:
        direction="OPTIMUM_SHIFT_DIRECTION_NOT_IDENTIFIED_WITHIN_BAND"
    return {
        "possible_optimum_ranks":surviving,
        "exclusions":exclusions,
        "excluded_minus_exposed_rank_shift_outer_interval":[low,high],
        "simultaneous_rank_shift_direction":direction,
        "optimum_rank_confidence_set_may_include_nonmaximizing_ranks":True,
    }


def simultaneous_from_batch_cell_bounds(
    patch_batches: list[dict],
    *,
    registered_global_viable_seed_cap: int,
    alpha: float = .05,
) -> dict:
    """Infer simultaneously over all 5 z levels in both G states.

    Input is a sequence of independently sourced patch/stage observations.
    For every batch: cells[(g,z)]= [lower viable seed mean, upper viable
    seed mean] of the two plants' flowers assigned to that z x G.
    These 2-outcome bounds are mandatory; no free sample-size multiplier
    from 2 flowers per treatment cell is allowed.
    """
    cap=_finite_int(registered_global_viable_seed_cap,
                    "registered global intact-seed cap",1,1000000)
    alpha=_probability(alpha)
    if not isinstance(patch_batches,list) or len(patch_batches)<2:
        raise ValueError("at least two independent patch-stage batches are required")
    if len(patch_batches)>20000:
        raise ValueError("source exceeds 20000 registered independent batches")

    ids=set()
    matrices=[]
    for batch in patch_batches:
        if not isinstance(batch,dict) or set(batch)!={
            "patch_id","stage_block_id","cells"
        }:
            raise ValueError("each batch requires patch, stage and full 10-cell matrix")
        patch=batch["patch_id"]
        stage=batch["stage_block_id"]
        if not isinstance(patch,str) or not patch or not isinstance(stage,str) or not stage:
            raise ValueError("patch and developmental-stage provenance must be nonempty")
        if patch in ids:
            raise ValueError(
                "same patch cannot serve as two independent batches; "
                "split-stage data may be correlated"
            )
        ids.add(patch)
        cell_map=batch["cells"]
        if not isinstance(cell_map,dict) or len(cell_map)!=10:
            raise ValueError("all five ranks in both G arms must be present per batch")
        converted={}
        for key,value in cell_map.items():
            if (
                not isinstance(key,tuple) or len(key)!=2
                or key[0] not in STATES or type(key[1]) is not int
                or key[1] not in Z_RANKS
                or not isinstance(value,(tuple,list)) or len(value)!=2
            ):
                raise ValueError("unregistered z x G cell or invalid fate interval")
            lo,hi=value
            if (not all(type(x) in (int,float,Fraction) for x in (lo,hi))
                or not all(math.isfinite(float(x)) for x in (lo,hi))
                or not 0<=lo<=hi<=cap):
                raise ValueError("seed fate means must lie within precommitted global cap")
            converted[key]=(Fraction(lo),Fraction(hi))
        if set(converted)!={(g,z) for g in STATES for z in Z_RANKS}:
            raise ValueError("missing or duplicated registered treatment cell")
        matrices.append(converted)
    B=len(matrices)
    m=len(STATES)*len(Z_RANKS)*(len(Z_RANKS)-1)//2
    if m!=N_TOTAL_SIMULTANEOUS_PAIRS:
        raise AssertionError("wrong number of familywise z-rank comparisons")
    # One-sided Hoeffding for each of 40 endpoints, difference range 2K.
    # P(E[L] < avg(L)-eps) <= exp(-B*eps^2/(2*K^2)).
    # P(E[U] > avg(U)+eps) <= exp(-B*eps^2/(2*K^2)).
    # Union over 2*m endpoints => eps below.
    eps=cap*math.sqrt((2.0/B)*math.log((2*m)/alpha))
    empirical={}
    population_band={}
    intervals=[]
    for g in STATES:
        for a in Z_RANKS:
            for b in Z_RANKS:
                if a>=b:
                    continue
                lower=[matrix[(g,a)][0]-matrix[(g,b)][1]
                       for matrix in matrices]
                upper=[matrix[(g,a)][1]-matrix[(g,b)][0]
                       for matrix in matrices]
                l=sum(lower,Fraction(0))/B
                u=sum(upper,Fraction(0))/B
                lo=max(-float(cap),float(l)-eps)
                hi=min(float(cap),float(u)+eps)
                if lo>hi:
                    raise AssertionError("concentration band is inverted")
                empirical[(g,a,b)]=(float(l),float(u))
                population_band[(g,a,b)]=(lo,hi)
                intervals.append({
                    "predator_treatment":g,
                    "rank_a":a, "rank_b":b,
                    "contrast_definition":"MEAN_VIABLE_SEEDS_AT_A_MINUS_AT_B",
                    "finite_allocated_batch_mean_fate_interval":[float(l),float(u)],
                    "conditional_population_mean_simultaneous_band":[lo,hi],
                    "n_source_patch_stage_batches":B,
                })
    sample=_rank_sets_from_pair_bands(empirical)
    simultaneous=_rank_sets_from_pair_bands(population_band)
    return {
        "receipt_schema":SCHEMA,
        "status":"CONDITIONAL_DISTRIBUTION_FREE_PATCH_BATCH_SIMULTANEOUS_ENCLOSURE",
        "method":KIND,
        "alpha":alpha,
        "nominal_simultaneous_coverage_given_all_registered_assumptions":1-alpha,
        "n_independent_patch_stage_batches":B,
        "n_original_distinct_mother_plants_per_batch":10,
        "n_original_fruit_flowers_per_batch":20,
        "n_simultaneous_two_sided_pairwise_difference_bands":m,
        "n_one_sided_endpoints_protected_by_union_bound":2*m,
        "registered_global_viable_seed_cap":cap,
        "per_contrast_Hoeffding_half_width_before_physical_clipping":eps,
        "no_fruit_level_pseudoreplication_or_bootstrap_imputation":True,
        "all_contrast_intervals":intervals,
        "descriptive_finite_allocated_sample_rank_sets":sample,
        "patch_level_simultaneous_population_rank_sets":simultaneous,
        "positive_optimum_shift_certified_conditional_on_assumptions":(
            simultaneous["simultaneous_rank_shift_direction"]
            =="GUARANTEED_POSITIVE_OPTIMUM_RANK_SHIFT_WITHIN_BAND"
        ),
        "negative_optimum_shift_certified_conditional_on_assumptions":(
            simultaneous["simultaneous_rank_shift_direction"]
            =="GUARANTEED_NEGATIVE_OPTIMUM_RANK_SHIFT_WITHIN_BAND"
        ),
        "is_conditional_Fisher_plant_G_label_randomization_test":False,
        "is_population_weak_null_optimum_direction_inference_under_assumptions":True,
        "observed_P_rex_field_data_independently_verified":False,
        "claim_ceiling":[
            "global_seed_count_cap_must_bound_all_eligible_population_draws_not_only_observed",
            "patches_must_be_independent_units_no_repeated_patch_at_different_stage",
            "patch_sampling_randomization_and_target_comparability_are_field_assumptions",
            "within_patch_plant_and_flower_correlation_allowed_with_no_extra_n_credit",
            "all_20_pairwise_contrasts_protected_simultaneously_not_unadjusted_t_tests",
            "bounded_unknown_maturity_outcomes_remain_interval_censored",
            "sample_argmax_may_change_under_population_sampling_uncertainty",
            "distribution_free_bound_extremely_conservative_at_realistic_B_and_K",
            "not_conditional_Fisher_randomization_or_pure_function_optimum",
            "G_selectivity_P0_exsertion_first_stage_and_interference_unverified",
            "no_SCH_P1_P2_W1_W2_L_SLK_architecture_promotion",
        ],
    }


def build(rows:list[dict],receipt:dict, *,
          registered_global_viable_seed_cap:int,
          alpha:float=.05) -> dict:
    base=verify_candidate_fruit_fates(rows,receipt)
    # Verify per-flower *prospective* seed caps, never infer K from the
    # observed highest viable count. Conditional confidence certification
    # requires an externally justified population-wide registered K.
    if type(registered_global_viable_seed_cap) is not int:
        raise ValueError("global K must be a prospectively registered integer")
    K=registered_global_viable_seed_cap
    for row in rows:
        v=row["seed_potential_upper"]
        if not v.isascii() or not v.isdecimal() or int(v)>K:
            raise ValueError("source flower seed cap exceeds registered global K")
    patch_batches=[]
    for entry in base["patch_stage_cell_sensitivity"]:
        matrix={}
        for cell in entry["cells"]:
            g=cell["predator_treatment"]
            z=cell["assigned_z_rank"]
            matrix[(g,z)]=tuple(
                Fraction(x) for x in cell["mean_intact_seed_count_bounds"]
            )
        patch_batches.append({
            "patch_id":entry["patch_id"],
            "stage_block_id":entry["stage_block_id"],
            "cells":matrix,
        })
    report=simultaneous_from_batch_cell_bounds(
        patch_batches,registered_global_viable_seed_cap=K,alpha=alpha,
    )
    report["source_population"]=receipt["population_id"]
    report["source_season"]=receipt["season_id"]
    report["source_allocation_identity_sha256"]=receipt["allocation_identity_sha256"]
    report["source_fate_analysis_sha256"]=_semantic_sha256(base)
    report["original_registered_flower_count"]=base["n_fruit_flowers"]
    report["n_source_fruit_outcomes_unresolved"]=sum(
        cell["n_unresolved_fruit_fates"]
        for g in STATES
        for cell in base["mean_fitness_by_predator_state_and_z"][g].values()
    )
    return report


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("allocated_fruit_fate_csv",type=Path)
    p.add_argument("frozen_two_flower_design_receipt",type=Path)
    p.add_argument("--registered-seed-cap",type=int,required=True)
    p.add_argument("--alpha",type=float,default=.05)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    report=build(
        _rows_csv(args.allocated_fruit_fate_csv),
        json.loads(args.frozen_two_flower_design_receipt.read_text(encoding="utf-8")),
        registered_global_viable_seed_cap=args.registered_seed_cap,
        alpha=args.alpha,
    )
    serialized=json.dumps(report,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(serialized,encoding="utf-8")
    else:
        print(serialized,end="")


if __name__=="__main__":
    main()

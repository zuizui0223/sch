"""Conditional simultaneous five-rank reproductive-optimum confidence bands.

For each of ten plant-level predator G x flower-level exsertion z cells,
the precommitted connected-cycle candidate supplies TWO different parent
plants per patch-stage batch. Treat the whole randomized batch as ONE
bounded sampling unit. Under INDEPENDENT genuinely randomized batches,
fixed source-eligible potential outcomes, no between-batch interference,
and a pre-treatment known universal seed-count bound 0<=Y<=K:

  X_b(g,z) = mean of the two flowers assigned (g,z) in batch b,
  E_R[X_b(g,z)] = finite-source/batch randomization marginal mu_b(g,z).

No iid ecology or independent flowers is assumed; the B batches' RANDOM
ASSIGNMENTS must be independent. Hoeffding + union bound over 10 cells:

  P_R(for every g,z, |mean_b X_b - mean_b mu_b| <= r) >= 1-alpha
  r = K sqrt(log(2*10/alpha)/(2*B)).

When realized flower counts are missing but bounded [l,u], plug
[mean_b lower(X_b)-r, mean_b upper(X_b)+r] into each cell.
The coverage remains conservative because the genuine unobserved
X_b lies between observed lower and upper, regardless of the mechanism
causing the missingness, provided all caps are valid.

Simultaneous outer rank-optimum sets and shift intervals follow.
These are FINITE ENROLLED BATCH assignment-marginal mean optima, NOT
unrestricted population optima, causal pure function optima, bootstrap
CIs, or calibrated sample-size recommendations.

IMPORTANT: the algorithm that created a source receipt is deterministic
given its string seed; source hashes do not establish randomization.
The 1-alpha interpretation is entirely conditional on actual, genuinely
random, independent precommitted patch-stage allocations, physical z
first-stage and a valid GLOBAL bound K for ALL potential seed outcomes.
"""
from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path

from scripts.analyze_pedicularis_two_flower_cyclic_fruit_bounds import (
    build as source_fate_bounds,
)
from scripts.plan_pedicularis_two_flower_cyclic_blocks import _rows_csv
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256

SCHEMA="SCH_PEDICULARIS_FIVE_Z_SIMULTANEOUS_DESIGN_BOUNDS_V1"
CONFIG_SCHEMA="SCH_PEDICULARIS_FIVE_Z_SIMULTANEOUS_BOUNDS_CONFIG_V1"
G=("EXCLUDED","EXPOSED")
Z=tuple(range(5))
CAP_PROVENANCE="PRE_TREATMENT_REGISTERED_GLOBAL_POTENTIAL_SEED_CAP"
STATUS="CONDITIONAL_RANDOMIZATION_SIMULTANEOUS_INTERVAL_NOT_FIELD_QUALIFIED"


def _config(raw:dict)->dict:
    if not isinstance(raw,dict) or raw.get("schema")!=CONFIG_SCHEMA:
        raise ValueError("simultaneous confidence config schema mismatch")
    alpha=raw.get("simultaneous_alpha")
    cap=raw.get("global_max_intact_seeds_per_flower")
    if type(alpha) not in (float,int) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("simultaneous_alpha must lie strictly between 0 and 1")
    if type(cap) is not int or not 1<=cap<=1000000:
        raise ValueError("global_max_intact_seeds_per_flower must be positive integer")
    if raw.get("global_cap_source_status")!=CAP_PROVENANCE:
        raise ValueError("global biological cap must be prospectively registered")
    if raw.get("independent_batch_randomization_assumed") is not True:
        raise ValueError("independent source batch randomization must be an explicit assumption")
    kind=raw.get("cap_assumption_kind")
    if kind not in (
        "SYNTHETIC_NOT_FIELD_VERIFIED",
        "PROSPECTIVE_FIELD_CAP_CLAIM_NOT_EXTERNALLY_VERIFIED",
    ):
        raise ValueError("cap_assumption_kind must retain synthetic or user-attested provenance")
    return {"alpha":float(alpha),"cap":cap,"cap_assumption_kind":kind}


def hoeffding_radius(*,batches:int,seed_cap:int,alpha:float,n_cells:int=10)->float:
    if (
        type(batches) is not int or batches<1
        or type(seed_cap) is not int or seed_cap<1
        or type(n_cells) is not int or n_cells<2
        or type(alpha) not in (int,float) or not math.isfinite(alpha)
        or not 0<alpha<1
    ):
        raise ValueError("Hoeffding requires B>=1, K>=1, cells>=2 and 0<alpha<1")
    return seed_cap*math.sqrt(math.log(2*n_cells/alpha)/(2*batches))


def sufficient_batches_for_symmetric_gap(
    *,hypothetical_gap:float,seed_cap:int,alpha:float,n_cells:int=10
)->int:
    """Number making 2*r < Delta *if* sample means equal guessed true means.

    This is an optimistic radius-only algebraic feasibility condition,
    NOT a power calculation. Does NOT include noise, selection bias,
    missing maturity outcomes, G intervention validity or optima effect.
    """
    if (
        type(hypothetical_gap) not in (float,int)
        or not math.isfinite(hypothetical_gap) or hypothetical_gap<=0
    ):
        raise ValueError("hypothetical gap must be finite and positive")
    hoeffding_radius(batches=1,seed_cap=seed_cap,alpha=alpha,n_cells=n_cells)
    threshold=(2*seed_cap**2*math.log(2*n_cells/alpha))/(hypothetical_gap**2)
    target=int(math.floor(threshold))+1
    # Floating strict inequality: exact threshold rounding can be fragile
    while 2*hoeffding_radius(batches=target,seed_cap=seed_cap,
                             alpha=alpha,n_cells=n_cells)>=hypothetical_gap:
        target+=1
    while target>1 and 2*hoeffding_radius(batches=target-1,seed_cap=seed_cap,
                                          alpha=alpha,n_cells=n_cells)<hypothetical_gap:
        target-=1
    return target


def simultaneous_cell_intervals(
    batches:list[dict], *,seed_cap:int,alpha:float
)->dict:
    """Ten simultaneous intervals from whole-batch marginal fate envelopes.

    Input source batch keys map (G,z) to source intact-seed-per-flower
    lower/upper values. This pure method can also be tested separately
    from fruit-fate source authentication; production build checks source.
    """
    if not batches:
        raise ValueError("at least one randomized complete batch required")
    target={(g,z) for g in G for z in Z}
    for b in batches:
        if set(b)!=target:
            raise ValueError("batch missing a registered predator state or z rank")
        for lo,hi in b.values():
            if not (0<=lo<=hi<=seed_cap):
                raise ValueError("source per-batch outcome envelope outside global potential cap")
    n=len(batches)
    r=hoeffding_radius(batches=n,seed_cap=seed_cap,alpha=alpha)
    cells={g:{} for g in G}
    for g,z in sorted(target):
        l=sum(float(batch[(g,z)][0]) for batch in batches)/n
        u=sum(float(batch[(g,z)][1]) for batch in batches)/n
        # Numerical safeguards allow exact zero or cap at endpoints.
        lower=max(0.0,l-r)
        upper=min(float(seed_cap),u+r)
        cells[g][str(z)]={
            "mean_observed_fate_lower":l,
            "mean_observed_fate_upper":u,
            "simultaneous_lower":lower,
            "simultaneous_upper":upper,
            "radius_before_cap_clipping":r,
            "n_batch_randomization_units":n,
        }
    return {
        "cells":cells,
        "n_independently_randomized_batches_assumed":n,
        "n_simultaneous_cell_means":len(target),
        "hoeffding_radius_seeds_per_flower":r,
        "simultaneous_nominal_coverage":1-alpha,
        "formula":"K_SQRT_LOG_2M_OVER_ALPHA_DIVIDED_BY_2B",
        "batch_unit_not_flower_or_parent_unit":True,
    }


def possible_optimum_rank_set(cells:dict[str,dict])->dict:
    """Conservative possible rank sets using JOINT confidence bands."""
    states={}
    for g in G:
        perrank=cells[g]
        if set(perrank)!={str(z) for z in Z}:
            raise ValueError("incomplete simultaneous five-rank fitness curves")
        lower={z:perrank[str(z)]["simultaneous_lower"] for z in Z}
        upper={z:perrank[str(z)]["simultaneous_upper"] for z in Z}
        if any(lower[z]>upper[z] for z in Z):
            raise ValueError("invalid joint cell interval")
        # If all true means lie inside the 10 simultaneous intervals,
        # their argmax set is contained by these possible ranks.
        benchmark=max(lower.values())
        possible=[z for z in Z if upper[z]>=benchmark-1e-12]
        unique=[
            z for z in Z
            if all(lower[z]>upper[k]+1e-12 for k in Z if k!=z)
        ]
        states[g]={
            "possible_optimum_ranks":possible,
            "guaranteed_unique_optimum_rank":unique[0] if len(unique)==1 else None,
        }
    excluded=states["EXCLUDED"]["possible_optimum_ranks"]
    exposed=states["EXPOSED"]["possible_optimum_ranks"]
    low=min(excluded)-max(exposed)
    high=max(excluded)-min(exposed)
    if low>0:
        classification="POSITIVE_SHIFT_SIMULTANEOUSLY_CERTIFIED"
    elif high<0:
        classification="NEGATIVE_SHIFT_SIMULTANEOUSLY_CERTIFIED"
    elif low==high==0:
        classification="ZERO_SHIFT_SIMULTANEOUSLY_CERTIFIED"
    else:
        classification="OPTIMUM_DISPLACEMENT_NOT_SIMULTANEOUSLY_IDENTIFIED"
    return {
        "states":states,
        "excluded_minus_exposed_optimum_rank_shift_outer_interval":[low,high],
        "optimum_shift_classification":classification,
        "zero_optimum_displacement_ruled_out":low>0 or high<0,
        "conditional_inference_valid_only_with_all_assumptions":True,
    }


def build(rows:list[dict],source_design_receipt:dict,raw_config:dict)->dict:
    cfg=_config(raw_config)
    # Reuse source-locked flower identity, plant-level G and true-zero/fate
    # interpretation, retaining every assigned fruit in its denominator.
    source=source_fate_bounds(rows,source_design_receipt)
    cap=cfg["cap"]
    for row in rows:
        try:
            source_cap=int(row["seed_potential_upper"])
        except (ValueError,TypeError,KeyError) as exc:
            raise ValueError("each assigned flower must have an observed source cap") from exc
        if source_cap>cap:
            raise ValueError("source potential seed cap exceeds prospectively declared global cap")
    source_groups=source["patch_stage_cell_sensitivity"]
    if len(source_groups)!=source["n_patch_stage_batches"]:
        raise ValueError("source patch-stage group count mismatch")
    batches=[]
    for group in source_groups:
        source_cells=group["cells"]
        if len(source_cells)!=10:
            raise ValueError("each source patch-stage batch needs ten z by G cells")
        values={}
        for cell in source_cells:
            key=(cell["predator_treatment"],cell["assigned_z_rank"])
            if key in values:
                raise ValueError("source has duplicated z x G treatment cell")
            a,b=cell["mean_intact_seed_count_bounds"]
            values[key]=(Fraction(a),Fraction(b))
        batches.append(values)

    joint=simultaneous_cell_intervals(
        batches,seed_cap=cap,alpha=cfg["alpha"]
    )
    result=possible_optimum_rank_set(joint["cells"])
    return {
        "receipt_schema":SCHEMA,
        "status":STATUS,
        "source_population":source["population_id"],
        "source_season":source["season_id"],
        "original_source_design_sha256":_semantic_sha256(source_design_receipt),
        "validated_fruit_source_sha256":source["source_fate_rows_sha256"],
        "global_seed_cap_K":cap,
        "cap_provenance_user_declared":CAP_PROVENANCE,
        "global_seed_cap_assumption_kind":cfg["cap_assumption_kind"],
        "actual_pre_treatment_cap_authentication_completed":False,
        "batch_assignments_independently_randomized_verified":False,
        "physical_z_first_stage_and_G_selectivity_verified":False,
        "target":"ASSIGNMENT_AVERAGED_MEAN_INTACT_MATURE_SEEDS_ACROSS_FIXED_ENROLLED_BATCHES",
        "alpha":cfg["alpha"],
        "simultaneous_result":joint,
        "optimum_result":result,
        "legacy_descriptive_optimum_outer_interval":source[
            "excluded_minus_exposed_possible_optimum_shift_outer_interval"
        ],
        "design_based_claim_only_conditional_on_genuine_randomization":True,
        "superpopulation_or_true_natural_pure_function_optima_estimated":False,
        "claim_ceiling":[
            "all_ten_G_z_means_protected_by_single_Bonferroni_Hoeffding_event",
            "each_batch_average_counts_once_regardless_of_twenty_flower_subunits",
            "genuinely_independent_randomization_across_patch_stage_batches_required",
            "random_seed_SHA256_sorting_not_proof_of_randomization_or_independence",
            "no_interference_across_batches_and_valid_potential_seed_cap_required",
            "within_plant_z_companion_interference_changes_the_pure_trait_estimand",
            "bound_K_must_cover_every_potential_seed_count_NOT_just_observed_count",
            "source_reported_cap_provenance_not_independently_authenticated",
            "unknown_maturity_fates_retained_as_real_upper_lower_envelopes",
            "finite_enrolled_batch_design_expectation_not_population_CI",
            "very_conservative_maximum_seed_cap_inequality_not_field_power",
            "no_G_or_z_first_stage_validation_or_SCH_L_W1_W2_Slk_unlock",
        ],
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("complete_candidate_fruit_fate_csv",type=Path)
    p.add_argument("source_two_flower_allocation_receipt_json",type=Path)
    p.add_argument("prospective_inference_config_json",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    r=build(
        _rows_csv(args.complete_candidate_fruit_fate_csv),
        json.loads(args.source_two_flower_allocation_receipt_json.read_text(
            encoding="utf-8")),
        json.loads(args.prospective_inference_config_json.read_text(
            encoding="utf-8")),
    )
    data=json.dumps(r,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding="utf-8")
    else:
        print(data,end="")


if __name__=="__main__":
    main()

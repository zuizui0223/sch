"""Nonasymptotic simultaneous five-rank peak confidence sets for SCH P. rex.

Source design: ten whole plants per patch-stage batch, two flowers per
mother, one predator G arm per plant, and a balanced connected cyclic
two-z design. Each patch-stage batch supplies exactly two fruit outcomes
to each of the 10 z x G cells.

Under GENUINELY RANDOM, INDEPENDENT treatment assignment across B
precommitted batches, fixed bounded potential intact mature seed counts
in [0,K], and well-defined no-interference outcomes:

    X_(b,G,z) := that batch's two-flower sample mean in [0,K].
    mu_(G,z) := B**-1 sum_b E_randomization[X_(b,G,z)].

BATCHES are independent; the two flower records in a batch are NOT.
Hoeffding + a union bound gives, simultaneously for 10 cells:

    Pr( forall G,z : abs(bar(X) - mu) <= eps ) >= 1-alpha
    eps = K sqrt(log(20/alpha) / (2 B)).

When a flower's true viable seed count is censored but known to lie
in [l_i,u_i], the unknown observed batch means satisfy L<=bar(X)<=U.
Thus each target mean lies in [max(0,L-eps),min(K,U+eps)] on the same
joint event. No imputation, independence across flowers or bootstrap.

All ten intervals are projected onto possible within-G optimal z ranks
and a confidence set on EXCLUDED-minus-EXPOSED optimal-rank displacement.
This is a SIMULTANEOUS finite-eligible-cohort DESIGN-EXPECTATION set,
NOT a CI for a randomly sampled landscape population, the literal
realized finite allocation's descriptive peak, or a valid weak-null
hypothesis test of equal population optimum under general interference.

The seed cap K must be a prospectively defensible uniform upper bound
for ALL potential intact seed outcomes under both G arms and all z;
the supplied source labels and SHA receipt cannot authenticate this.
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

SCHEMA="SCH_P_REX_SIMULTANEOUS_RANDOMIZATION_PEAK_SETS_V1"
SYNTHETIC_SCHEMA="SCH_P_REX_ORACLE_SIMULTANEOUS_PEAK_ASSUMPTIONS_V1"
ARMS=("EXCLUDED","EXPOSED")
RANKS=range(5)
N_CELLS=len(ARMS)*len(RANKS)
TOL=1e-12


def _alpha(alpha:float)->float:
    if type(alpha) not in (int,float) or not math.isfinite(alpha) or not 0<alpha<1:
        raise ValueError("simultaneous alpha must be a finite number in (0,1)")
    return float(alpha)


def _positive_integer(v,name:str,maximum:int=10_000_000)->int:
    if type(v) is not int or not 1<=v<=maximum:
        raise ValueError(f"{name}: positive integer 1..{maximum} required")
    return v


def radius(*,n_independent_batches:int,global_potential_seed_cap:int,
           alpha:float)->float:
    B=_positive_integer(n_independent_batches,"independent batches")
    cap=_positive_integer(global_potential_seed_cap,"potential outcome cap")
    a=_alpha(alpha)
    return cap*math.sqrt(math.log(2*N_CELLS/a)/(2*B))


def _validated_cells(
    means:dict,
    *,
    seed_cap:int,
)->dict[str,dict[int,tuple[float,float]]]:
    if not isinstance(means,dict) or set(means)!=set(ARMS):
        raise ValueError("both predator-state five-rank curves are required")
    out={}
    for g in ARMS:
        if not isinstance(means[g],dict):
            raise ValueError("each predator-state curve must be keyed by z rank")
        try:
            keys={int(k) for k in means[g]}
        except (TypeError,ValueError) as exc:
            raise ValueError("cell means require z ranks 0..4") from exc
        if keys!=set(RANKS) or len(means[g])!=5:
            raise ValueError("cell means require five distinct z ranks 0..4")
        out[g]={}
        for z in RANKS:
            item=means[g].get(z,means[g].get(str(z)))
            if not isinstance(item,(list,tuple)) or len(item)!=2:
                raise ValueError("each cell must carry lower/upper viable seed means")
            lo,hi=item
            if not all(type(x) in (int,float) and math.isfinite(x) for x in (lo,hi)):
                raise ValueError("cell endpoints must be finite numeric fractions")
            if lo < 0 or hi > seed_cap or lo > hi:
                raise ValueError("source viable mean interval outside seed potential cap")
            out[g][z]=(float(lo),float(hi))
    return out


def _possible_optima(intervals:dict[str,dict[int,tuple[float,float]]])->dict:
    out={}
    for g in ARMS:
        cells=intervals[g]
        max_lower=max(l for l,_ in cells.values())
        possible=[z for z in RANKS if cells[z][1] >= max_lower-TOL]
        unique=[
            z for z in RANKS
            if all(cells[z][0]>cells[j][1]+TOL for j in RANKS if j!=z)
        ]
        if not possible or len(unique)>1:
            raise AssertionError("invalid simultaneous rank confidence set")
        out[g]={
            "possible_peak_ranks":possible,
            "guaranteed_unique_peak_rank":unique[0] if unique else None,
        }
    ex=out["EXCLUDED"]["possible_peak_ranks"]
    ep=out["EXPOSED"]["possible_peak_ranks"]
    low,high=min(ex)-max(ep),max(ex)-min(ep)
    return {
        "state_peak_confidence_sets":out,
        "peak_rank_shift_outer_confidence_interval":[low,high],
        "positive_shift_certified":low>0,
        "negative_shift_certified":high<0,
        "zero_shift_excluded":low>0 or high<0,
        "possible_zero_shift":low<=0<=high,
        "both_state_peaks_unique":all(
            out[g]["guaranteed_unique_peak_rank"] is not None for g in ARMS
        ),
    }


def simultaneous_from_fate_cell_means(
    source_means:dict,
    *,
    n_independent_batches:int,
    global_potential_seed_cap:int,
    alpha:float=0.05,
    shadow_radius_multiplier:float=1.0,
)->dict:
    """Compute joint 1-alpha region or the 2*eps oracle stress envelope.

    shadow_radius_multiplier=2 is ONLY for the no-missing oracle
    sample-size sufficient-condition demonstration. It is NOT
    an observed source confidence region or coverage claim.
    """
    K=_positive_integer(global_potential_seed_cap,"potential outcome cap")
    B=_positive_integer(n_independent_batches,"independent batches")
    if type(shadow_radius_multiplier) not in (int,float) or not (
        shadow_radius_multiplier in (1,2)
    ):
        raise ValueError("envelope multiplier must be 1 or 2")
    intervals=_validated_cells(source_means,seed_cap=K)
    base_radius=radius(
        n_independent_batches=B,global_potential_seed_cap=K,alpha=alpha,
    )
    e=base_radius*shadow_radius_multiplier
    confidence={
        g:{
            z:(max(0.0,lo-e),min(float(K),hi+e))
            for z,(lo,hi) in intervals[g].items()
        }
        for g in ARMS
    }
    result=_possible_optima(confidence)
    return {
        "n_independent_patch_stage_assignment_batches":B,
        "n_eligible_plants_in_design":10*B,
        "n_fruit_flowers_in_design":20*B,
        "n_fruit_observations_per_G_z_cell":2*B,
        "per_cell_Hoeffding_halfwidth_before_clipping":base_radius,
        "applied_radius_multiplier":shadow_radius_multiplier,
        "simultaneous_interval_endpoints_by_G_z":{
            g:{str(z):[lo,hi] for z,(lo,hi) in confidence[g].items()}
            for g in ARMS
        },
        **result,
        "target_population":
            "MEAN_OF_BATCH_RANDOMIZATION_EXPECTATIONS_FOR_ELIGIBLE_REGISTERED_FLOWERS",
        "joint_coverage_at_least_1_minus_alpha_if_assumptions_hold":
            shadow_radius_multiplier==1,
        "probability_of_any_cell_miscoverage_upper_bound":_alpha(alpha),
        "n_familywise_two_sided_bounds":2*N_CELLS,
        "independent_assignment_unit":"PATCH_STAGE_BATCH_NOT_INDIVIDUAL_FLOWER",
        "source_fate_censoring_is_not_imputed":True,
        "cell_intervals_not_assumed_independent_across_G_or_z":True,
    }


def _source_means_to_float(summary:dict)->dict:
    return {
        g:{
            z:tuple(float(Fraction(v["exact"])) for v in summary[
                "mean_fitness_by_predator_state_and_z"
            ][g][str(z)]["mean_viable_seed_count_per_flower_bounds"])
            for z in RANKS
        }
        for g in ARMS
    }


def build(
    rows:list[dict[str,str]],receipt:dict,
    *,
    alpha:float=0.05,
    global_potential_seed_cap:int,
)->dict:
    # Strict identity + source-fate checks reused, including the entire
    # original flower cohort and each source treatment assignment.
    summary=source_fate_bounds(rows,receipt)
    K=_positive_integer(global_potential_seed_cap,"potential outcome cap")
    for row in rows:
        if int(row["seed_potential_upper"])>K:
            raise ValueError(
                "global seed bound cannot be below a source-registered "
                "individual flower's possible mature seed count"
            )
    confidence=simultaneous_from_fate_cell_means(
        _source_means_to_float(summary),
        n_independent_batches=summary["n_patch_stage_batches"],
        global_potential_seed_cap=K,
        alpha=alpha,
    )
    return {
        "receipt_schema":SCHEMA,
        "status":"CONDITIONAL_NONASYMPTOTIC_JOINT_PEAK_SET_NOT_FIELD_QUALIFIED",
        "population_id":summary["population_id"],
        "season_id":summary["season_id"],
        "source_design_receipt_sha256":_semantic_sha256(receipt),
        "source_outcomes_sha256":summary["source_fate_rows_sha256"],
        "n_source_fate_missing":sum(
            v["n_unresolved_fruit_fates"]
            for g in ARMS
            for v in summary["mean_fitness_by_predator_state_and_z"][g].values()
        ),
        "descriptive_finite_allocation_peak_sets":summary[
            "possible_state_specific_optima"
        ],
        "design_randomization_simultaneous_inference":confidence,
        "field_independence_of_batch_randomization_authenticated":False,
        "all_potential_seed_outcomes_proven_bounded_by_input_K":False,
        "source_seed_and_G_physical_selectivity_independently_verified":False,
        "claim_ceiling":[
            "true_independent_uniform_randomized_batches_required_for_coverage",
            "source_SHA_manifest_validity_does_not_authenticate_randomness",
            "seed_cap_must_bound_every_unobserved_potential_outcome_not_just_observed",
            "within_batch_mother_and_two_flower_dependence_automatically_allowed",
            "confidence_covers_design_expectations_of_fixed_eligible_cohort_not_landscape_population",
            "joint_confidence_peak_set_not_identical_to_descriptive_finite_source_optimum",
            "post_treatment_unknown_mature_fates_retained_as_source_interval_bounds",
            "uniform_20_tail_Hoeffding_union_bound_deliberately_very_conservative",
            "no_smoothness_or_unimodality_omitted_rank_assumption",
            "positive_peak_confidence_not_P0_G_or_P2_qualification",
            "no_pure_pollinator_predator_optima_SCH_L_or_SLK_architecture_value",
        ],
    }


def _oracle_curve(scenario:dict)->dict:
    if not isinstance(scenario,dict) or scenario.get("schema")!=SYNTHETIC_SCHEMA:
        raise ValueError("prospective oracle scenario schema required")
    if scenario.get("data_kind")!="SYNTHETIC_ASSUMPTIONS_NOT_FIELD_DATA":
        raise ValueError("oracle means must be labelled as hypothetical")
    curves=scenario.get("assumed_complete_maturity_seed_means")
    if not isinstance(curves,dict) or set(curves)!=set(ARMS):
        raise ValueError("oracle needs complete five-rank G response curves")
    return {
        g:{
            z:(float(value),float(value))
            for z,value in enumerate(curves[g])
        } for g in ARMS
    }


def _first_certified(
    assumed_exact_means:dict,
    *,
    cap:int,alpha:float,
    max_batches:int,
    shadow_radius_multiplier:int,
    property_name:str,
)->int|None:
    if property_name not in ("positive_shift_certified","both_state_peaks_unique"):
        raise ValueError("unsupported oracle certification property")
    _positive_integer(max_batches,"maximum search batches",maximum=10_000_000)
    def works(b:int)->bool:
        res=simultaneous_from_fate_cell_means(
            assumed_exact_means,
            n_independent_batches=b,
            global_potential_seed_cap=cap,
            alpha=alpha,
            shadow_radius_multiplier=shadow_radius_multiplier,
        )
        return res[property_name] is True
    if not works(max_batches):
        return None
    l,r=1,max_batches
    while l<r:
        mid=(l+r)//2
        if works(mid):
            r=mid
        else:
            l=mid+1
    return l


def synthetic_oracle(scenario:dict)->dict:
    curves=_oracle_curve(scenario)
    cap=_positive_integer(scenario.get("global_potential_seed_cap"),
                          "potential outcome cap")
    alpha=_alpha(scenario.get("familywise_alpha"))
    maxb=_positive_integer(scenario.get("max_batches_to_examine"),
                           "maximum oracle batches")
    for g in ARMS:
        if (not isinstance(scenario["assumed_complete_maturity_seed_means"][g],list)
            or len(scenario["assumed_complete_maturity_seed_means"][g])!=5):
            raise ValueError("oracle requires exactly five z seed means per G")
    grid=scenario.get("candidate_batch_counts")
    if not isinstance(grid,list) or not grid or len(grid)!=len(set(grid)):
        raise ValueError("oracle trial batch counts must be unique and nonempty")
    for b in grid:
        _positive_integer(b,"candidate batch count")
    # Verify values are physical before computing any result.
    _validated_cells(curves,seed_cap=cap)
    status={}
    for property_name in ("positive_shift_certified","both_state_peaks_unique"):
        status[property_name]={
            "oracle_source_means_equal_to_observed_cell_means":{
                "first_batch_count":_first_certified(
                    curves,cap=cap,alpha=alpha,max_batches=maxb,
                    shadow_radius_multiplier=1,property_name=property_name,
                ),
                "interpretation":"IDEALIZED_UNNOISY_OBSERVATION_NOT_A_DETECTION_GUARANTEE",
            },
            "sufficient_for_probability_at_least_1_minus_alpha":{
                "first_batch_count":_first_certified(
                    curves,cap=cap,alpha=alpha,max_batches=maxb,
                    shadow_radius_multiplier=2,property_name=property_name,
                ),
                "interpretation":"ONLY_IF_TRUE_MEAN_CURVES_K_AND_RANDOMIZATION_ASSUMPTIONS_HOLD",
            },
        }
    return {
        "schema":SYNTHETIC_SCHEMA,
        "status":"SYNTHETIC_HOEFFDING_SAMPLE_REQUIREMENT_NOT_P_REX_RECOMMENDATION",
        "source_assumptions":scenario,
        "per_candidate_batch":{
            str(b):simultaneous_from_fate_cell_means(
                curves,n_independent_batches=b,
                global_potential_seed_cap=cap,alpha=alpha,
            ) for b in sorted(grid)
        },
        "idealized_certification_thresholds":status,
        "no_detectability_guarantee_with_persistent_missing_fates":True,
        "no_real_P_rex_recruitment_requirement_estimated":True,
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("source_fate_csv",nargs="?",type=Path)
    p.add_argument("frozen_candidate_allocation_receipt",nargs="?",type=Path)
    p.add_argument("--seed-cap",type=int)
    p.add_argument("--alpha",type=float,default=0.05)
    p.add_argument("--synthetic-oracle",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    if a.synthetic_oracle is not None:
        if a.source_fate_csv or a.frozen_candidate_allocation_receipt:
            p.error("oracle and source-fate analysis cannot be mixed")
        out=synthetic_oracle(json.loads(a.synthetic_oracle.read_text(encoding="utf-8")))
    else:
        if not all((a.source_fate_csv,a.frozen_candidate_allocation_receipt)) or a.seed_cap is None:
            p.error("source analysis requires fruit CSV, allocation receipt and --seed-cap")
        out=build(
            _rows_csv(a.source_fate_csv),
            json.loads(a.frozen_candidate_allocation_receipt.read_text(encoding="utf-8")),
            alpha=a.alpha,global_potential_seed_cap=a.seed_cap,
        )
    rendered=json.dumps(out,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(rendered,encoding="utf-8")
    else:
        print(rendered,end="")


if __name__=="__main__":
    main()

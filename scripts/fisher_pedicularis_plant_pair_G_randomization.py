"""Conditional whole-plant Fisher sharp-null test for the SCH two-flower design.

In each original patch x developmental-stage x cyclic-z-edge stratum
one plant received excluded G and one exposed G. CONDITIONAL on the
pre-outcome assigned z-edge of every plant and z assignment of its two
distinct flowers, the plant-level G labels can be exchanged as a pair.

Under the *SHARP null* that G changes NO flower's mature intact seed
count, the fixed observations can be re-assigned. This tests the sharp
null of no G effect for any flower, with a preselected one-sided
peak-rank-shift statistic. It is NOT a valid test of the weak null of
'no change in population optimum', zero average effect, or pure
pollinator-vs-predator function. Flower-level permutation is forbidden.

Maturity outcomes must be exactly counted or pre-dispersal
zero-verified; any truly unknown final viable count fails closed.
Neither verified q nor causal z manipulation effectiveness follows
from the recorded mature-seed endpoint.
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
from collections import defaultdict
from pathlib import Path

from scripts.analyze_pedicularis_two_flower_cyclic_fruit_bounds import (
    build as verify_candidate_source,
)
from scripts.bound_pedicularis_fruit_fate_selection import _interpret
from scripts.plan_pedicularis_two_flower_cyclic_blocks import _rows_csv
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256

SCHEMA="PEDICULARIS_PLANT_G_MATCHED_FISHER_SHARP_NULL_V1"
EXACT_MAX_PAIRS=15
DEFAULT_MONTE_CARLO_PERMUTATIONS=9999


def _pairs(rows:list[dict],receipt:dict)->list[dict]:
    # First verify all 20*B original allocated flower IDs and G/z methods
    # with the existing prospective candidate source-specific analyzer.
    verify_candidate_source(rows,receipt)
    plant=defaultdict(list)
    for row in rows:
        v=_interpret(row)
        if v["seed_fitness_lower"]!=v["seed_fitness_upper"]:
            raise ValueError(
                "Fisher sharp-null test requires verified exact mature seed "
                "output for every allocated flower; no censoring imputation"
            )
        plant[(row["patch_id"],row["stage_block_id"],
               int(row["pair_cycle_edge"]),row["plant_id"])].append(
            (
                int(row["assigned_z_rank"]),
                v["seed_fitness_lower"],
                row["predator_treatment"],
                int(row["seed_potential_upper"]),
            )
        )
    matched=defaultdict(dict)
    for (patch,stage,edge,pid),outcomes in plant.items():
        if len(outcomes)!=2:
            raise ValueError("source plant needs two outcome flowers")
        labels={g for _,_,g,_ in outcomes}
        if len(labels)!=1:
            raise ValueError("G cannot vary within parent plant")
        g=labels.pop()
        if set(z for z,_,_,_ in outcomes)!={edge,(edge+1)%5}:
            raise ValueError("source pair cycle rank mismatch")
        group=(patch,stage,edge)
        if g in matched[group]:
            raise ValueError("cycle edge needs one separate plant in each G arm")
        matched[group][g]={
            "plant_id":pid,
            "by_z":{z:y for z,y,_,_ in outcomes},
            "cap_by_z":{z:cap for z,_,_,cap in outcomes},
        }
    expected=5*receipt["n_patch_stage_batches"]
    if len(matched)!=expected or any(set(v)!={"EXCLUDED","EXPOSED"}
                                       for v in matched.values()):
        raise ValueError("matched design requires one exposed/excluded plant per edge")
    return [
        {
            "patch_id":patch,"stage_block_id":stage,"edge":edge,
            "excluded":group["EXCLUDED"],"exposed":group["EXPOSED"],
        }
        for (patch,stage,edge),group in sorted(matched.items())
    ]


def _peak_midrank(values:list[float])->float:
    best=max(values)
    positions=[z for z,v in enumerate(values) if v==best]
    return sum(positions)/len(positions)


def statistic(pairs:list[dict],flip_bits:int=0)->dict:
    """The pre-specified directional distance between five-rank maxima.

    Each whole-plant pair swap changes BOTH flowers and preserves z.
    Five rank-specific means have equal known denominator 2*n_batches.
    """
    totals={"EXCLUDED":[0]*5,"EXPOSED":[0]*5}
    counts={"EXCLUDED":[0]*5,"EXPOSED":[0]*5}
    for j,pair in enumerate(pairs):
        flip=bool(flip_bits & (1<<j))
        for g,source in (
            ("EXCLUDED",pair["exposed" if flip else "excluded"]),
            ("EXPOSED",pair["excluded" if flip else "exposed"]),
        ):
            for z,y in source["by_z"].items():
                totals[g][z]+=y
                counts[g][z]+=1
    if any(len(set(counts[g]))!=1 or counts[g][0]==0
           for g in ("EXCLUDED","EXPOSED")):
        raise AssertionError("conditional swap must retain balanced rank incidence")
    means={g:[totals[g][z]/counts[g][z] for z in range(5)]
           for g in ("EXCLUDED","EXPOSED")}
    p0=_peak_midrank(means["EXCLUDED"])
    p1=_peak_midrank(means["EXPOSED"])
    return {
        "exclusion_minus_exposure_peak_midrank":p0-p1,
        "predator_excluded_discrete_peak_midrank":p0,
        "predator_exposed_discrete_peak_midrank":p1,
        "seed_means_by_predator_arm":means,
        "tie_rule":"MIDRANK_OF_ALL_EXACTLY_EQUAL_MAXIMUM_CELLS",
    }


def _p_from_stats(observed:float,replicates:list[float], *, exact:bool)->dict:
    k=sum(x>=observed-1e-12 for x in replicates)
    if exact:
        p=k/len(replicates)
    else:
        p=(k+1)/(len(replicates)+1)
    return {
        "upper_tail_at_least_as_directionally_shifted":k,
        "n_randomization_statistics":len(replicates),
        "one_sided_Fisher_sharp_null_p":p,
        "p_calculation":(
            "EXACT_CONDITIONAL_ENUMERATION" if exact
            else "MONTE_CARLO_PLUS_ONE_INCLUDE_OBSERVED_REFERENCE"
        ),
    }


def fisher_from_pairs(
    pairs:list[dict], *,
    monte_carlo_permutations:int=DEFAULT_MONTE_CARLO_PERMUTATIONS,
    random_seed:int=20261009,
    exact_max_pairs:int=EXACT_MAX_PAIRS,
)->dict:
    """Exact <=15 matched plant pairs; else conditional Monte Carlo."""
    if not pairs or any(not isinstance(p,dict) for p in pairs):
        raise ValueError("source needs nonempty plant-edge pairs")
    if type(monte_carlo_permutations) is not int or not 999<=monte_carlo_permutations<=100000:
        raise ValueError("Monte Carlo permutations must be 999..100000")
    if type(random_seed) is not int or not 0<=random_seed<=2**63-1:
        raise ValueError("random_seed must be a nonnegative integer")
    if exact_max_pairs!=EXACT_MAX_PAIRS:
        raise ValueError("fixed exact enumeration cutoff must remain 15 pairs")
    observed=statistic(pairs)
    n_pairs=len(pairs)
    exact=n_pairs<=EXACT_MAX_PAIRS
    if exact:
        flips=range(1<<n_pairs)
    else:
        rng=random.Random(random_seed)
        flips=(rng.getrandbits(n_pairs) for _ in range(monte_carlo_permutations))
    shifts=[statistic(pairs,x)["exclusion_minus_exposure_peak_midrank"]
            for x in flips]
    inference=_p_from_stats(
        observed["exclusion_minus_exposure_peak_midrank"],shifts,exact=exact
    )
    return {
        "observed_predeclared_peak_statistic":observed,
        "n_matched_plant_pairs":n_pairs,
        "n_parent_plants":2*n_pairs,
        "n_fruit_flowers":4*n_pairs,
        "observed_peak_shift_direction":(
            "POSITIVE" if observed["exclusion_minus_exposure_peak_midrank"]>0
            else "NEGATIVE" if observed["exclusion_minus_exposure_peak_midrank"]<0
            else "ZERO_OR_TIED_MIDRANK"
        ),
        **inference,
        "sharp_null":"NO_PREDATOR_G_EFFECT_ON_MATURE_SEED_COUNT_OF_ANY_STUDY_FLOWER",
        "conditional_randomization_unit":"WHOLE_PLANT_PAIR_SWAPPED_WITHIN_PATCH_STAGE_CYCLIC_Z_EDGE",
        "z_physical_setting_and_flower_assignment_held_fixed":True,
        "only_original_exclusion_status_exchanged_between_matched_plants":True,
        "valid_weak_null_of_zero_optimum_shift_test":False,
        "valid_weak_null_of_zero_average_G_effect_test":False,
        "valid_only_if_random_G_assignment_and_no_spillover":True,
        "post_selection_biological_G_qualifications_not_certified":True,
    }


def uniform_additive_G_sensitivity(
    pairs:list[dict], *,
    monte_carlo_permutations:int=DEFAULT_MONTE_CARLO_PERMUTATIONS,
    random_seed:int=20261009,
    maximum_tau_candidates:int=101,
)->dict:
    """Conservative union-of-sharp-null test, constant INTEGER seed gain tau.

    H0(tau): Y_i(EXCLUDED,z)=Y_i(EXPOSED,z)+tau for EVERY
    allocated flower. This hypothesis implies the same
    argmax z in each individual potential-outcome response
    under perfect observation, but the finite sample may differ.
    Maximizing a Fisher p-value over feasible tau tests the
    UNION of constant-additive sharp nulls conservatively.

    Even rejection need not imply z-specific G interaction:
    heterogeneous G effects by plant unrelated to z can also
    violate a universal common tau. This is not a test of
    the weak null of equal population optimum.
    """
    if type(maximum_tau_candidates) is not int or not 1<=maximum_tau_candidates<=1000:
        raise ValueError("constant-tau maximum candidate limit must be 1..1000")
    ranges=[]
    for pair in pairs:
        for g,key in (("EXCLUDED","excluded"),("EXPOSED","exposed")):
            item=pair[key]
            for z,y in item["by_z"].items():
                cap=item["cap_by_z"][z]
                if not (0<=y<=cap):
                    raise ValueError("source outcome exceeds per-flower seed cap")
                if g=="EXCLUDED":
                    ranges.append((y-cap,y))
                else:
                    ranges.append((-y,cap-y))
    tau_min=max(a for a,b in ranges)
    tau_max=min(b for a,b in ranges)
    if tau_min>tau_max:
        raise AssertionError("zero effect must fit counted source outcomes")
    if tau_max-tau_min+1>maximum_tau_candidates:
        raise ValueError(
            "too many physically feasible constant-additive tau values; "
            "increase registered budget or restrict genuine source seed caps"
        )

    observed_stat=statistic(pairs)["exclusion_minus_exposure_peak_midrank"]
    scans=[]
    for tau in range(tau_min,tau_max+1):
        # Impute each original EXCLUDED flower's untreated seed outcome
        # under the hypothesized constant additive tau. Under a swap,
        # the newly assigned EXCLUDED gets +tau on *every z rank*.
        # That uniform +tau cannot change the argmax, so evaluating
        # the baselines is exactly equivalent for the peak statistic.
        imputed=[]
        for pair in pairs:
            item=dict(pair)
            item["excluded"]={
                **pair["excluded"],
                "by_z":{
                    z:y-tau for z,y in pair["excluded"]["by_z"].items()
                },
            }
            imputed.append(item)
        test=fisher_from_pairs(
            imputed,
            monte_carlo_permutations=monte_carlo_permutations,
            random_seed=random_seed,
        )
        if abs(
            test["observed_predeclared_peak_statistic"][
                "exclusion_minus_exposure_peak_midrank"
            ]-observed_stat
        )>1e-12:
            raise AssertionError("constant additive tau changed the observed peak")
        scans.append({
            "hypothesized_constant_seed_gain_per_flower":tau,
            "one_sided_sharp_null_p":test["one_sided_Fisher_sharp_null_p"],
        })
    worst=max(scans,key=lambda x:x["one_sided_sharp_null_p"])
    return {
        "tested_null":"UNION_OF_SHARP_UNIFORM_ADDITIVE_G_SEED_COUNT_EFFECTS",
        "feasible_integer_tau_interval":[tau_min,tau_max],
        "n_evaluated_tau_values":len(scans),
        "conditional_p_upper_over_constant_tau_nulls":worst["one_sided_sharp_null_p"],
        "most_conservative_integer_tau":worst["hypothesized_constant_seed_gain_per_flower"],
        "individual_sharp_tau_sensitivity":scans,
        "rejecting_uniform_tau_is_not_proof_of_G_by_z_interaction":True,
        "not_test_of_weak_same_population_peak_null":True,
        "tau_zero_is_included_in_source_compatible_nulls":tau_min<=0<=tau_max,
        "only_integer_seed_gain_common_to_every_flower_considered":True,
    }


def build(rows:list[dict],receipt:dict, *,
          monte_carlo_permutations:int=DEFAULT_MONTE_CARLO_PERMUTATIONS,
          random_seed:int=20261009,
          test_uniform_additive_constant:bool=False)->dict:
    pairs=_pairs(rows,receipt)
    results=fisher_from_pairs(
        pairs,monte_carlo_permutations=monte_carlo_permutations,
        random_seed=random_seed,
    )
    additive=(
        uniform_additive_G_sensitivity(
            pairs,
            monte_carlo_permutations=monte_carlo_permutations,
            random_seed=random_seed,
        ) if test_uniform_additive_constant else None
    )
    return {
        "receipt_schema":SCHEMA,
        "status":"NON_GATING_SHARP_NULL_CONDITIONAL_RANDOMIZATION_ONLY",
        "uniform_additive_seed_gain_sharp_null_sensitivity":additive,
        "source_population":receipt["population_id"],
        "source_season":receipt["season_id"],
        "source_design_receipt_sha256":_semantic_sha256(receipt),
        "source_complete_mature_outcomes_sha256":_semantic_sha256(
            sorted(rows,key=lambda r:(r["plant_id"],r["flower_id"]))
        ),
        "observed_field_data_independently_verified":False,
        **results,
        "claim_ceiling":[
            "source_G_randomization_probability_depends_on_precommitted_seed",
            "conditional_on_original_z_pair_slot_and_within_plant_flower_z",
            "mathematically_exact_under_sharp_no_G_effect_only",
            "not_weak_null_test_of_zero_reproductive_optimum_displacement",
            "not_weak_null_test_of_mean_zero_G_effect",
            "every_plant_two_flower_seed_outcome_must_be_exactly_known",
            "no_missing_seed_fates_censored_outcomes_or_complete_destruction_imputed",
            "between_plant_predator_spillover_could_violate_sharp_null_imputation",
            "plant_z_treatment_first_stage_and_causal_G_selectivity_unverified",
            "randomization_p_does_not_imply_pure_pollinator_or_predator_optima",
            "constant_additive_sharp_tau_union_not_the_weak_null_of_no_G_by_z_effect",
            "no_P0_G_P2_W1_W2_SCH_L_or_SLK_architecture_promotion",
        ],
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("complete_fruit_fate_csv",type=Path)
    p.add_argument("candidate_frozen_allocation_receipt_json",type=Path)
    p.add_argument("--monte-carlo-permutations",type=int,default=DEFAULT_MONTE_CARLO_PERMUTATIONS)
    p.add_argument("--seed",type=int,default=20261009)
    p.add_argument("--test-uniform-additive-constant",action="store_true")
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    source= _rows_csv(args.complete_fruit_fate_csv)
    receipt=json.loads(args.candidate_frozen_allocation_receipt_json.read_text(encoding="utf-8"))
    result=build(
        source,receipt,
        monte_carlo_permutations=args.monte_carlo_permutations,
        random_seed=args.seed,
        test_uniform_additive_constant=args.test_uniform_additive_constant,
    )
    data=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data,encoding="utf-8")
    else:
        print(data,end="")


if __name__=="__main__":
    main()

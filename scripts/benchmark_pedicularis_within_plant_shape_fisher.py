"""Benchmark two different plant-pair Fisher statistics under identical simulations.

Compare previous *peak-midrank* sharp no-G-effect test with a new
within-plant cyclic difference statistic testing the sharp null of no
G effect on each mother's z-pair seed fitness DIFFERENCE.

These tests address DIFFERENT sharp nulls. The new one permits arbitrary
mother-specific constant integer G gains, but neither proves a change in
the population optimum. A separate exact integer maternal-gain
control is generated from the original no-G-effect source schedule
without clipping-induced violation of the within-plant null.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path

from scripts.simulate_pedicularis_plant_pair_fisher_calibration import (
    _validate, _subseed, _wilson, simulate_pairs,
)
from scripts.fisher_pedicularis_plant_pair_G_randomization import (
    fisher_from_pairs,
)
from scripts.fisher_pedicularis_within_plant_z_shape import (
    fisher_within_plant_shape_pairs,
)

SCHEMA="SCH_PEDICULARIS_PLANT_FISHER_SHAPE_STAT_BENCHMARK_V1"
MATERNAL_NULL="MATERNAL_INTEGER_ADDITIVE_G_GAIN"
MISSING_FATE_POLICY="REQUIRE_EXACT_SURVIVING_SEED_COUNT_ALL_ALLOCATED_FLOWERS"


def integer_maternal_additive_control(pairs:list[dict],seed:int)->list[dict]:
    """Exact counterfactual contrast-null: gain is arbitrary per mother.

    Starting from a SHARP no-G-effect source schedule, add a
    mother-specific integer gain to both original EXCLUDED flowers,
    carefully preserving the corresponding source seed-count caps.
    Within-plant z contrast cancels the common gain exactly.
    """
    cloned=deepcopy(pairs)
    for p in cloned:
        mom=p["excluded"]
        gain=1+(_subseed(seed,"MATERNAL_TAU",mom["plant_id"])%6)
        headroom=min(
            mom["cap_by_z"][z]-y
            for z,y in mom["by_z"].items()
        )
        gain=min(gain,headroom)
        if gain<0:
            raise AssertionError("source baseline exceeded available seed cap")
        for z in mom["by_z"]:
            mom["by_z"][z]+=gain
    return cloned


def build(config:dict)->dict:
    c=_validate(config)
    summary=[]
    modes=[*c["modes"],MATERNAL_NULL]
    if len(modes)!=len(set(modes)):
        raise ValueError("benchmark maternal additive control duplicates another mode")
    for mode in modes:
        for batches in c["batches"]:
            peak_p=[]
            shape_p=[]
            positive_peak=[]
            positive_shape=[]
            for iteration in range(c["replicates"]):
                seed=_subseed(c["seed"],mode,str(batches),str(iteration))
                source_mode=(
                    "SHARP_NO_G_EFFECT" if mode==MATERNAL_NULL else mode
                )
                pairs=simulate_pairs(
                    scenario_mode=source_mode,n_batches=batches,
                    seed=seed,cap=c["cap"],
                    patch_sd=c["patch_sd"],plant_sd=c["plant_sd"],
                    flower_sd=c["flower_sd"],
                    heterogeneous_G_sd=c["heterogeneous_G_sd"],
                )
                if mode==MATERNAL_NULL:
                    pairs=integer_maternal_additive_control(pairs,seed)
                pseed=_subseed(seed,"SAME_CONDITIONAL_RANDOMIZATION")
                peak=fisher_from_pairs(
                    pairs,monte_carlo_permutations=c["mc"],
                    random_seed=pseed,
                )
                shape=fisher_within_plant_shape_pairs(
                    pairs,monte_carlo_permutations=c["mc"],
                    random_seed=pseed,
                )
                peak_p.append(peak["one_sided_Fisher_sharp_null_p"])
                shape_p.append(shape["one_sided_Fisher_sharp_null_p"])
                positive_peak.append(
                    peak["observed_predeclared_peak_statistic"][
                        "exclusion_minus_exposure_peak_midrank"
                    ]>0
                )
                positive_shape.append(
                    shape["observed_relative_exsertion_advantage_count_per_flower"]>0
                )
            n=len(peak_p)
            k_peak=sum(p<=c["alpha"] for p in peak_p)
            k_shape=sum(p<=c["alpha"] for p in shape_p)
            summary.append({
                "mode":mode,
                "n_patch_stage_batches":batches,
                "n_eligible_plants":10*batches,
                "n_simulated_assignments":n,
                "one_sided_alpha":c["alpha"],
                "n_peak_midrank_Fisher_rejections":k_peak,
                "fraction_peak_midrank_Fisher_rejections":k_peak/n,
                "n_within_plant_shape_Fisher_rejections":k_shape,
                "fraction_within_plant_shape_Fisher_rejections":k_shape/n,
                "shape_rejection_Wilson95_simulation_interval":_wilson(k_shape,n),
                "n_descriptive_positive_peak_shifts":sum(positive_peak),
                "n_positive_z4_vs_z2_G_shape_contrasts":sum(positive_shape),
                "fraction_peak_positive_and_shape_Fisher_rejected":
                    sum(x and p<=c["alpha"]
                        for x,p in zip(positive_peak,shape_p,strict=True))/n,
                "null_of_peak_midrank":"SHARP_NO_G_EFFECT_ON_ANY_FLOWER",
                "null_of_shape":
                    "SHARP_NO_G_EFFECT_ON_WITHIN_MATERNAL_Z_PAIR_DIFFERENCE",
                "outcome_fates_exact_by_construction":True,
                "source_reproduction_source":"ACTUAL_CYCLIC_TWO_FLOWER_ALLOCATOR",
            })
    return {
        "receipt_schema":SCHEMA,
        "status":"SYNTHETIC_CONTRAST_STATISTIC_COMPARISON_NOT_FIELD_INFERENCE",
        "source_simulation_config":config,
        "n_generated_simulated_studies":len(summary)*c["replicates"],
        "scenario_grid":summary,
        "shape_statistic":"G_RESPONSE_INTERACTION_Z4_MINUS_Z2_VIA_FIVE_EDGE_CYCLE",
        "two_nulls_are_distinct_and_must_not_be_CONFLATED":True,
        "maternal_integer_null_sharp_for_pair_differences":True,
        "tested_population_optimum_shift_weak_null":False,
        "claim_ceiling":[
            "peak_midrank_test_null_is_stronger_than_within_plant_shape_contrast_null",
            "maternal_additive_G_gain_cancels_both_flower_differences",
            "shape_z4_vs_z2_selected_as_synthetic_biology_hypothesis_NOT_field_preregistered",
            "shape_contrast_rejection_not_proof_of_any_fitness_argmax_change",
            "input_fitness_curves_variances_and_missingness_all_synthetic",
            "rounded_clipped_gaussian_heterogeneous_gain_may_not_satisfy_exact_difference_null",
            "sharp_difference_null_type_I_control_requires_valid_plant_randomization",
            "model_comparison_statistics_should_be_prespecified_prior_to_real_field_outcomes",
            "no_pilot_G_selectivity_z_first_stage_plant_spillover_verification",
            "no_weak_optimum_null_population_confidence_intervals_or_W1_W2_releases",
        ],
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("synthetic_scenario_config",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=build(json.loads(
        a.synthetic_scenario_config.read_text(encoding="utf-8")
    ))
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(text,encoding="utf-8")
    else:
        print(text,end="")


if __name__=="__main__":
    main()

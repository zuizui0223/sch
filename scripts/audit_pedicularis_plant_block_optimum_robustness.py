"""Plant-block jackknife of bounded P. rex reproductive optimum displacement.

Purpose: a finite-sample robustness diagnostic when randomized z x G
flowers share the same plant. An apparent predator-induced optimum shift
over all flowers may be driven by one biologically atypical plant.

Validate all *original* allocated flower IDs and their fate bounds first,
then exclude one entire plant block at a time and recompute all z x G
means and both state-specific possible-optimum sets. Do not reinterpret a
plant-deleted subset as a new frozen randomized experiment.

This is leave-one-PLANT-out, not leave-one-flower-out, and is NOT an
inferential plant-cluster confidence interval or proof of population-level
transportability. It does not establish causal exclusion selectivity.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

from scripts.bound_pedicularis_fruit_fate_selection import (
    _interpret, build as fruit_fate_build, read as read_fate,
)
from scripts.prioritize_pedicularis_optimum_shift_remeasurement import (
    _shift, _original_means,
)
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256

SCHEMA = "PEDICULARIS_PLANT_BLOCK_OPTIMUM_SHIFT_JACKKNIFE_V1"
G_STATES = ("EXCLUDED", "EXPOSED")


def _from_source_subset(
    interpreted: list[dict],
    n_z_levels: int,
) -> tuple[dict, dict]:
    """Pure descriptive margins after source validation, not a new receipt."""
    by_cell: dict[tuple[str,int],list[tuple[int,int]]] = defaultdict(list)
    retained_plants = {x["plant_id"] for x in interpreted}
    if not retained_plants:
        raise ValueError("plant-block jackknife cannot use an empty subset")
    for x in interpreted:
        by_cell[(x["predator_treatment"],x["assigned_z_rank"])].append(
            (x["seed_fitness_lower"],x["seed_fitness_upper"])
        )
    means: dict[str,dict[int,tuple[Fraction,Fraction]]] = {
        g:{} for g in G_STATES
    }
    cell_data: dict[str,dict[str,dict]] = {g:{} for g in G_STATES}
    for g in G_STATES:
        for z in range(n_z_levels):
            sample=by_cell[(g,z)]
            if len(sample)!=len(retained_plants):
                raise ValueError(
                    "projected jackknife subset is missing randomized "
                    "z x G flower observations on retained plants"
                )
            lo=Fraction(sum(a for a,_ in sample),len(sample))
            hi=Fraction(sum(b for _,b in sample),len(sample))
            means[g][z]=lo,hi
            cell_data[g][str(z)]={
                "mean_viable_seeds_per_flower_bounds_exact":[str(lo),str(hi)],
                "n_retained_fruit_observations":len(sample),
                "n_fruits_with_unresolved_viable_yield":sum(a!=b for a,b in sample),
            }
    return _shift(means),cell_data


def build(rows:list[dict[str,str]], allocation:dict) -> dict:
    base=fruit_fate_build(rows,allocation)
    if not isinstance(allocation.get("n_z_levels"),int):
        raise ValueError("source z ranks must have integer count")
    interpreted=[_interpret(r) for r in rows]
    plants=sorted({x["plant_id"] for x in interpreted})
    if len(plants)<2:
        raise ValueError(
            "plant-block jackknife needs at least two complete plant blocks"
        )
    all_shift=_shift(_original_means(base))
    if all_shift["excluded_minus_exposed_rank_shift_outer_interval"] != base[
        "excluded_minus_exposed_optimum_rank_shift_outer_bound"
    ]:
        raise AssertionError("jackknife baseline differs from primary source receipt")
    sensitivity=[]
    for plant in plants:
        retained=[x for x in interpreted if x["plant_id"]!=plant]
        condition,cells=_from_source_subset(retained,allocation["n_z_levels"])
        sensitivity.append({
            "omitted_plant_id":plant,
            "n_retained_plant_blocks":len(plants)-1,
            "n_retained_allocated_flowers":len(retained),
            "conditional_optimum_shift":condition,
            "bounded_mean_seed_fitness_by_z_and_G":cells,
            "does_preserve_baseline_shift_class": (
                condition["classification"]==all_shift["classification"]
            ),
            "does_preserve_baseline_guaranteed_positive":(
                all_shift["classification"]=="GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
                and condition["classification"]=="GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
            ),
            "is_original_precommitted_allocation_receipt":False,
        })
    pos=sum(x["conditional_optimum_shift"]["classification"]==
            "GUARANTEED_POSITIVE_EXCLUSION_SHIFT" for x in sensitivity)
    neg=sum(x["conditional_optimum_shift"]["classification"]==
            "GUARANTEED_NEGATIVE_EXCLUSION_SHIFT" for x in sensitivity)
    zero=sum(x["conditional_optimum_shift"]["classification"]==
            "GUARANTEED_ZERO_EXCLUSION_SHIFT" for x in sensitivity)
    weak=[x["omitted_plant_id"] for x in sensitivity
          if not x["does_preserve_baseline_shift_class"]]
    baseline_positive=all_shift["classification"]=="GUARANTEED_POSITIVE_EXCLUSION_SHIFT"
    baseline_negative=all_shift["classification"]=="GUARANTEED_NEGATIVE_EXCLUSION_SHIFT"
    robust_positive=baseline_positive and pos==len(plants)
    robust_negative=baseline_negative and neg==len(plants)
    return {
        "receipt_schema":SCHEMA,
        "status":"NON_GATING_FINITE_SAMPLE_PLANT_DELETION_DIAGNOSTIC",
        "population_id":base["population_id"],
        "season_id":base["season_id"],
        "original_source_fate_bounds_sha256":_semantic_sha256(base),
        "original_fruit_data_sha256":base["source_outcome_rows_sha256"],
        "n_source_plant_blocks":len(plants),
        "n_full_original_allocated_flowers":base["n_all_allocated_flowers"],
        "baseline_original_all_plant_shift":all_shift,
        "per_omitted_plant_sensitivity":sensitivity,
        "n_jackknife_subsets_with_guaranteed_positive_shift":pos,
        "n_jackknife_subsets_with_guaranteed_negative_shift":neg,
        "n_jackknife_subsets_with_guaranteed_zero_shift":zero,
        "omitted_plants_that_change_baseline_classification":weak,
        "full_sample_guaranteed_positive_shift_robust_to_every_single_plant_deletion":robust_positive,
        "full_sample_guaranteed_negative_shift_robust_to_every_single_plant_deletion":robust_negative,
        "observed_plant_heterogeneity_demonstrated":False,
        "field_data_independently_verified":False,
        "claim_ceiling":[
            "subsets_are_descriptive_projections_not_new_frozen_allocations",
            "all_original_flowers_and_plant_IDs_validated_before_deletion",
            "whole_plant_blocks_omitted_not_individual_flower_pseudoreplicates",
            "n_two_plant_jackknife_subsets_each_have_only_one_retained_plant",
            "jackknife_sign_stability_not_population_CI_or_design_power",
            "cohort_representativeness_and_resource_interference_unverified",
            "verified_zero_mature_yield_not_predation_cause",
            "capsule_missingness_bound_depends_on_real_source_caps",
            "full_sample_shift_not_a_causal_predator_trait_selection_proof",
            "no_P0_G_P2_W1_W2_or_SCH_pure_function_promotion",
        ],
    }


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("complete_allocated_fruit_fate_csv",type=Path)
    parser.add_argument("frozen_fruit_allocation_receipt_json",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    out=build(
        read_fate(args.complete_allocated_fruit_fate_csv),
        json.loads(args.frozen_fruit_allocation_receipt_json.read_text(encoding="utf-8"))
    )
    text=json.dumps(out,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding="utf-8")
    else:
        print(text,end="")


if __name__=="__main__":
    main()

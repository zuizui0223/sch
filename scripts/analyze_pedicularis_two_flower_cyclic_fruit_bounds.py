"""Nonconfirmatory z x G seed-fitness bounds for two-flower cyclic plant blocks.

This is a NEW design's analysis, not a replacement for the original
complete 10-flower-per-plant P. rex estimator. Randomized predator
treatment belongs to the PLANT; two z settings are assigned to two
flowers within each plant. Every patch x stage design batch has
exactly two distinct plants contributing to each z x G cell.

A mean per z x G is a descriptive finite-sample estimator. Under the
prospective plant/flower randomization and interference assumptions,
a treatment assignment ensemble supports an expectation of marginal
potential-outcome means; **this single allocation** is neither a
randomization p-value nor a population-level confidence interval.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

from scripts.plan_pedicularis_two_flower_cyclic_blocks import (
    SCHEMA as DESIGN_SCHEMA,
    STATUS as DESIGN_STATUS,
    ALLOC_FIELDS,
    _rows_csv,
)
from scripts.bound_pedicularis_fruit_fate_selection import _interpret, _as_stat
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256

OUTPUT_SCHEMA="PEDICULARIS_TWO_FLOWER_CONNECTED_CYCLE_FRUIT_BOUNDS_V1"
FATE_FIELDS={
    "fate_status", "intact_seeds", "damaged_seeds", "seed_stage_proof",
    "viable_lower", "viable_upper", "seed_potential_upper",
    "seed_potential_upper_basis", "zero_fate_proof", "partial_interval_proof",
}


def _optima(means:dict[int,tuple[Fraction,Fraction]])->dict:
    max_lower=max(v[0] for v in means.values())
    possible=sorted(z for z,(_,hi) in means.items() if hi>=max_lower)
    unique=[
        z for z,(lo,_) in means.items()
        if all(lo>other_hi for w,(_,other_hi) in means.items() if w!=z)
    ]
    return {
        "possible_discrete_optimum_ranks":possible,
        "guaranteed_unique_optimum_rank":unique[0] if len(unique)==1 else None,
    }


def build(
    rows:list[dict[str,str]], receipt:dict,
) -> dict:
    if (
        receipt.get("receipt_schema")!=DESIGN_SCHEMA
        or receipt.get("status")!=DESIGN_STATUS
        or receipt.get("G_randomization_unit")!="PLANT"
        or receipt.get("z_assignment_unit")!="FLOWER_WITHIN_PLANT_AFTER_Z_PAIR_SLOT"
    ):
        raise ValueError("needs frozen prospective two-flower candidate design receipt")
    if not rows or any(
        not (set(ALLOC_FIELDS)|FATE_FIELDS).issubset(r) for r in rows
    ):
        raise ValueError("two-flower fate rows must include source IDs and fate fields")
    if len({r["flower_id"] for r in rows}) != len(rows):
        raise ValueError("two-flower fate rows must have unique flower IDs")
    freeze=sorted([
        {field:r[field] for field in ALLOC_FIELDS}
        for r in rows
    ],key=lambda r:(r["plant_id"],r["flower_id"]))
    if (
        freeze!=receipt.get("expected_frozen_rows")
        or _semantic_sha256(freeze)!=receipt.get("allocation_identity_sha256")
        or len(rows)!=receipt.get("n_allocated_fruit_flowers")
    ):
        raise ValueError("two-flower outcome assignment differs from frozen source manifest")
    if any(
        (r["population_id"],r["season_id"])
        != (receipt["population_id"],receipt["season_id"])
        for r in rows
    ):
        raise ValueError("two-flower outcome population/season differs from source")
    groups:dict[tuple[str,str],dict[str,list[dict[str,str]]]]=defaultdict(
        lambda:defaultdict(list)
    )
    for r in rows:
        groups[(r["patch_id"],r["stage_block_id"])][r["plant_id"]].append(r)
    if len(groups)!=receipt.get("n_patch_stage_batches"):
        raise ValueError("unregistered source patch/stage blocks")
    interpreted=[_interpret(r) for r in rows]
    lookup={r["flower_id"]:r for r in interpreted}
    bycell:dict[tuple[str,str,str,int],list[dict]]=defaultdict(list)
    strata=[]
    for key,plants in sorted(groups.items()):
        if len(plants)!=10:
            raise ValueError("two-flower audit requires ten plants per batch")
        incidence=Counter()
        for plant,entries in plants.items():
            if len(entries)!=2 or len({
                x["predator_treatment"] for x in entries
            })!=1:
                raise ValueError("predator G must be constant within each plant")
            ranks=[int(e["assigned_z_rank"]) for e in entries]
            if len(set(ranks))!=2 or sorted(ranks) not in (
                [0,1],[1,2],[2,3],[3,4],[0,4]
            ):
                raise ValueError("source z incidence must be cyclic two-rank pair")
            for r in entries:
                incidence[(r["predator_treatment"],int(r["assigned_z_rank"]))]+=1
                bycell[(*key,r["predator_treatment"],int(r["assigned_z_rank"]))].append(
                    lookup[r["flower_id"]]
                )
        if set(incidence)!={(g,z) for g in ("EXCLUDED","EXPOSED") for z in range(5)} or any(
            val!=2 for val in incidence.values()
        ):
            raise ValueError("cyclic design must have two independent plants per z x G")
        strata.append({"patch_id":key[0],"stage_block_id":key[1],
                       "n_plant_units":10,"n_fruit_units":20})

    # With equally balanced batches, equal-weight averaging of each batch
    # coincides with the pooled per-treatment sample mean.
    means={}
    bystate={g:{} for g in ("EXCLUDED","EXPOSED")}
    bypatch=[]
    for (patch,stage) in sorted(groups):
        report={"patch_id":patch,"stage_block_id":stage,"cells":[]}
        for g in ("EXCLUDED","EXPOSED"):
            for z in range(5):
                fruit=bycell[(patch,stage,g,z)]
                lo=Fraction(sum(x["seed_fitness_lower"] for x in fruit),2)
                hi=Fraction(sum(x["seed_fitness_upper"] for x in fruit),2)
                report["cells"].append({
                    "predator_treatment":g,
                    "assigned_z_rank":z,
                    "n_distinct_plants":2,
                    "mean_intact_seed_count_bounds":[str(lo),str(hi)],
                })
        bypatch.append(report)

    cells={}
    for g in ("EXCLUDED","EXPOSED"):
        cells[g]={}
        for z in range(5):
            all_fruit=[
                x for key in sorted(groups)
                for x in bycell[(*key,g,z)]
            ]
            n=len(all_fruit)
            lo=Fraction(sum(x["seed_fitness_lower"] for x in all_fruit),n)
            hi=Fraction(sum(x["seed_fitness_upper"] for x in all_fruit),n)
            bystate[g][z]=(lo,hi)
            cells[g][str(z)]={
                "n_fruits":n,
                "n_distinct_plant_units":n,
                "mean_viable_seed_count_per_flower_bounds":[_as_stat(lo),_as_stat(hi)],
                "n_unresolved_fruit_fates":sum(
                    x["seed_fitness_lower"]<x["seed_fitness_upper"]
                    for x in all_fruit
                ),
            }
    states={g:_optima(bystate[g]) for g in ("EXCLUDED","EXPOSED")}
    ex=states["EXCLUDED"]["possible_discrete_optimum_ranks"]
    ep=states["EXPOSED"]["possible_discrete_optimum_ranks"]
    dlow,dhigh=min(ex)-max(ep),max(ex)-min(ep)
    per_rank_g={}
    for z in range(5):
        excl,expo=bystate["EXCLUDED"][z],bystate["EXPOSED"][z]
        per_rank_g[str(z)]={
            "excluded_minus_exposed_intact_seed_count_bounds":[
                _as_stat(excl[0]-expo[1]),_as_stat(excl[1]-expo[0])
            ],
            "experimental_G_unit":"PLANT_NOT_FLOWER",
        }
    return {
        "receipt_schema":OUTPUT_SCHEMA,
        "status":"NON_GATING_TWO_FLOWER_PLANT_RANDOMIZED_CANDIDATE_DESCRIPTIVE",
        "population_id":receipt["population_id"],
        "season_id":receipt["season_id"],
        "source_design_receipt_sha256":_semantic_sha256(receipt),
        "source_fate_rows_sha256":_semantic_sha256(sorted(
            rows,key=lambda r:(r["plant_id"],r["flower_id"])
        )),
        "n_plants":receipt["n_plants"],
        "n_fruit_flowers":len(rows),
        "n_patch_stage_batches":len(groups),
        "G_randomization_unit":"PLANT",
        "z_assignment_unit":"FLOWER_WITHIN_PLANT",
        "strata":strata,
        "patch_stage_cell_sensitivity":bypatch,
        "mean_fitness_by_predator_state_and_z":cells,
        "possible_state_specific_optima":states,
        "excluded_minus_exposed_possible_optimum_shift_outer_interval":[dlow,dhigh],
        "guaranteed_positive_rank_shift_conditional_on_fate_caps":dlow>0,
        "G_between_plant_fitness_contrasts_by_z":per_rank_g,
        "full_randomization_inference_and_plant_cluster_CI_implemented":False,
        "observed_field_data_independently_verified":False,
        "claim_ceiling":[
            "candidate_method_not_qualified_P0_z_first_stage",
            "plant_level_predator_G_not_qualified_exclusion_or_spillover",
            "plant_level_G_contrast_is_not_a_paired_within_plant_comparison",
            "within_plant_z_pair_treatments_can_interfere_through_resources",
            "patch_stage_balanced_but_not_pairwise_BIBD",
            "n_two_per_cell_per_stratum_not_prospective_power",
            "multiple_patch_stage_batches_do_not_prove_population_representativeness",
            "fruit_fate_proof_labels_not_independently_authenticated",
            "finite_assigned_sample_not_randomization_p_or_superpopulation_CI",
            "pollen_sentinel_sampling_and_exchangeability_not_in_this_program",
            "no_P2_W1_W2_L_or_SCH_pure_function_optima",
        ],
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("complete_candidate_fruit_fate_csv",type=Path)
    p.add_argument("source_candidate_design_receipt_json",type=Path)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=build(
        _rows_csv(a.complete_candidate_fruit_fate_csv),
        json.loads(a.source_candidate_design_receipt_json.read_text(encoding="utf-8"))
    )
    payload=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")


if __name__=="__main__":
    main()

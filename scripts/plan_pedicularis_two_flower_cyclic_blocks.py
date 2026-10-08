"""Non-gating P. rex prospective *two-flower-per-plant* design candidate.

Five z settings crossed with two predator G arms produce ten treatments.
Within each fixed patch x developmental-stage stratum, require 10
eligible plants with two treatment-blind flowers each. Assign exactly
five PLANTS to each G arm by a precommitted salted SHA-256 permutation.
Within G, plant z-pairs form a 5-cycle: (0,1),(1,2),(2,3),(3,4),(4,0).
Every z x G cell thus has TWO flowers from distinct plants per stratum.

This is an equireplicate *connected cyclic incomplete-block* design,
NOT a balanced incomplete block design: most pairs of z levels never
share a plant. G is randomized BETWEEN plants, not within plants.
Random assignment of z to the two registered flowers is within plant.

This is only an allocation DESIGN with candidate methods, not a qualified
P0 physical first stage, G-selectivity pilot, or confirmatory W1/W2 plan.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter,defaultdict
from pathlib import Path

from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256

SCHEMA="SCH_PEDICULARIS_TWO_FLOWER_CYCLIC_FRUIT_DESIGN_V1"
STATUS="PROSPECTIVE_INCOMPLETE_BLOCK_DESIGN_NOT_FIELD_QUALIFIED"
ALLOC_FIELDS=(
    "population_id","season_id","patch_id","stage_block_id",
    "plant_id","flower_id","flower_position_code","assigned_z_level",
    "assigned_z_rank","manipulation_setting_id","sham_control",
    "pollination_treatment","predator_treatment","exclusion_method",
    "randomization_slot","pair_cycle_edge",
)


def _rows_csv(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as fh:
        r=csv.DictReader(fh)
        if not r.fieldnames:
            raise ValueError("no CSV header")
        rows=[{k:(v or "").strip() for k,v in row.items()} for row in r]
    if not rows:
        raise ValueError("empty flower or level manifest")
    return rows


def _hashkey(seed:str,*values:str)->str:
    return hashlib.sha256(
        json.dumps([seed,*values],ensure_ascii=False,separators=(",",":")).encode("utf-8")
    ).hexdigest()


def _settings(levels:list[dict[str,str]])->list[dict]:
    required={"assigned_z_level","assigned_z_rank","manipulation_setting_id","sham_control"}
    if len(levels)!=5 or any(not required.issubset(v) for v in levels):
        raise ValueError("cyclic two-flower pilot currently requires exactly five z settings")
    try:
        levels=sorted(levels,key=lambda v:int(v["assigned_z_rank"]))
        ranks=[int(v["assigned_z_rank"]) for v in levels]
    except (TypeError,ValueError) as e:
        raise ValueError("z ranks must be exactly 0..4") from e
    if ranks!=list(range(5)):
        raise ValueError("z ranks must be exactly 0..4")
    if len({v["assigned_z_level"] for v in levels})!=5 or len({
        v["manipulation_setting_id"] for v in levels
    })!=5 or any(v["sham_control"] not in {"0","1"} for v in levels):
        raise ValueError("z setting labels, methods and sham codes must be distinct/valid")
    if any(not v["assigned_z_level"] or not v["manipulation_setting_id"] for v in levels):
        raise ValueError("z setting label/physical setting cannot be blank")
    return [{
        "assigned_z_level":v["assigned_z_level"],
        "assigned_z_rank":int(v["assigned_z_rank"]),
        "manipulation_setting_id":v["manipulation_setting_id"],
        "sham_control":v["sham_control"],
    } for v in levels]


def build(
    manifest:list[dict[str,str]],
    level_plan:list[dict[str,str]],
    *,
    allocation_seed:str,
    g_exclusion_candidate_method:str,
    g_exposed_sham_candidate_method:str,
) -> tuple[list[dict[str,str]],dict]:
    if (
        type(allocation_seed) is not str or len(allocation_seed.strip())<12
        or allocation_seed=="REQUIRED_BEFORE_USE"
    ):
        raise ValueError("prospective assignment needs a resolved seed >=12 characters")
    if not g_exclusion_candidate_method or not g_exposed_sham_candidate_method or (
        g_exclusion_candidate_method==g_exposed_sham_candidate_method
    ):
        raise ValueError("prospective G exclusion and sham candidates must differ")
    settings=_settings(level_plan)
    columns={
        "population_id","season_id","patch_id","stage_block_id",
        "plant_id","flower_id","flower_position_code",
    }
    if not manifest or any(not columns.issubset(r) for r in manifest):
        raise ValueError("flower manifest lacks source stratum/plant/position identity")
    ids=[r["flower_id"] for r in manifest]
    if any(not r for r in ids) or len(set(ids))!=len(ids):
        raise ValueError("each flower requires a globally unique source ID")
    contexts={(r["population_id"],r["season_id"]) for r in manifest}
    if len(contexts)!=1 or any(not a or not b for a,b in contexts):
        raise ValueError("single qualified candidate population/season needed")
    (population,season),=contexts
    grouped:dict[tuple[str,str],dict[str,list[dict[str,str]]]]=defaultdict(
        lambda:defaultdict(list)
    )
    plants_seen={}
    for r in manifest:
        if any(not r[c] for c in columns):
            raise ValueError("flower stratum, plant and positional fields cannot be blank")
        key=(r["patch_id"],r["stage_block_id"])
        plant=r["plant_id"]
        if plant in plants_seen and plants_seen[plant]!=key:
            raise ValueError("one plant may not occur in two patch-stage batches")
        plants_seen[plant]=key
        grouped[key][plant].append(r)

    output=[]
    stratum_counts=[]
    for (patch,stage),plant_map in sorted(grouped.items()):
        if len(plant_map)!=10:
            raise ValueError(
                "each connected incomplete-block stratum must have exactly ten plants"
            )
        if any(len(flowers)!=2 or len({
            r["flower_position_code"] for r in flowers
        })!=2 for flowers in plant_map.values()):
            raise ValueError("each plant must have exactly two distinguishable flowers")
        # Random permutations are stable across input row order. Plant
        # IDs/flower positions must be registered before outcomes are seen.
        plants=sorted(
            plant_map,key=lambda p:_hashkey(
                allocation_seed,"PLANT",population,season,patch,stage,p
            )
        )
        for slot,plant_id in enumerate(plants):
            arm="EXCLUDED" if slot<5 else "EXPOSED"
            edge=slot%5
            ranks=(edge,(edge+1)%5)
            ordered=sorted(
                plant_map[plant_id],
                key=lambda r:_hashkey(
                    allocation_seed,"FLOWER",population,season,patch,stage,
                    plant_id,r["flower_id"]
                )
            )
            for flower,z in zip(ordered,ranks,strict=True):
                setting=settings[z]
                output.append({
                    "population_id":population,
                    "season_id":season,
                    "patch_id":patch,
                    "stage_block_id":stage,
                    "plant_id":plant_id,
                    "flower_id":flower["flower_id"],
                    "flower_position_code":flower["flower_position_code"],
                    "assigned_z_level":setting["assigned_z_level"],
                    "assigned_z_rank":str(z),
                    "manipulation_setting_id":setting["manipulation_setting_id"],
                    "sham_control":setting["sham_control"],
                    "pollination_treatment":"NATURAL",
                    "predator_treatment":arm,
                    "exclusion_method":(
                        g_exclusion_candidate_method if arm=="EXCLUDED"
                        else g_exposed_sham_candidate_method
                    ),
                    "randomization_slot":str(slot),
                    "pair_cycle_edge":str(edge),
                })
        stratum_counts.append({"patch_id":patch,"stage_block_id":stage,
                               "n_plants":10,"n_fruit_flowers":20})
    assert len(output)==len(manifest)
    counts=Counter(
        (r["patch_id"],r["stage_block_id"],r["predator_treatment"],
         r["assigned_z_rank"]) for r in output
    )
    if any(c!=2 for c in counts.values()) or len(counts)!=10*len(grouped):
        raise AssertionError("cyclic z x G cell incidence not equal or incomplete")
    freeze=sorted(
        [{field:r[field] for field in ALLOC_FIELDS} for r in output],
        key=lambda r:(r["plant_id"],r["flower_id"])
    )
    receipt={
        "receipt_schema":SCHEMA,
        "status":STATUS,
        "analysis":"candidate_connected_cycle_plant_level_G_two_flower_z_v1",
        "population_id":population,
        "season_id":season,
        "n_patch_stage_batches":len(grouped),
        "n_plants":len(plants_seen),
        "n_allocated_fruit_flowers":len(output),
        "max_required_fruit_flowers_per_plant":2,
        "n_per_z_by_G_per_patch_stage_batch":2,
        "z_physical_setting_candidates":settings,
        "g_exclusion_candidate_method":g_exclusion_candidate_method,
        "g_exposed_sham_candidate_method":g_exposed_sham_candidate_method,
        "allocation_seed_sha256":_semantic_sha256(allocation_seed),
        "allocation_algorithm":"SHA256_SORT_PLANTS_AND_FLOWERS_CYCLIC_FIVE_EDGE",
        "source_identity_fields":list(ALLOC_FIELDS),
        "expected_frozen_rows":freeze,
        "allocation_identity_sha256":_semantic_sha256(freeze),
        "strata":stratum_counts,
        "G_randomization_unit":"PLANT",
        "z_assignment_unit":"FLOWER_WITHIN_PLANT_AFTER_Z_PAIR_SLOT",
        "plant_incidence_graph":"CONNECTED_FIVE_CYCLE_NOT_PAIRWISE_BALANCED",
        "status_not_field_qualification":True,
        "claim_ceiling":[
            "not_a_P0_z_manipulation_validity_or_first_stage_receipt",
            "not_a_qualified_independent_G_or_P2_execution",
            "plant_level_G_avoids_within_plant_mixed_G_but_not_between_plant_spillover",
            "two_flower_supply_not_verified_in_focal_population",
            "no_power_or_positive_field_fitness_estimate",
            "one_batch_two_fruits_per_cell_is_not_a_sufficient_power_claim",
            "patch_stage_batches_are_design_strata_not_independent_landscapes",
            "plant_level_G_effect_is_between_plants_and_requires_randomization",
            "not_a_BIBD_and_not_full_within_plant_z_comparison",
            "no_W1_W2_or_SCH_pure_optimum_promotion",
        ],
    }
    return output,receipt


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("two_flower_treatment_blind_manifest_csv",type=Path)
    parser.add_argument("five_level_candidate_plan_csv",type=Path)
    parser.add_argument("--allocation-seed",required=True)
    parser.add_argument("--g-exclusion-candidate-method",required=True)
    parser.add_argument("--g-exposed-sham-candidate-method",required=True)
    parser.add_argument("--allocations-out",required=True,type=Path)
    parser.add_argument("--receipt-out",required=True,type=Path)
    args=parser.parse_args()
    allocated,receipt=build(
        _rows_csv(args.two_flower_treatment_blind_manifest_csv),
        _rows_csv(args.five_level_candidate_plan_csv),
        allocation_seed=args.allocation_seed,
        g_exclusion_candidate_method=args.g_exclusion_candidate_method,
        g_exposed_sham_candidate_method=args.g_exposed_sham_candidate_method,
    )
    args.allocations_out.parent.mkdir(parents=True,exist_ok=True)
    with args.allocations_out.open("w",encoding="utf-8",newline="") as fh:
        writer=csv.DictWriter(fh,fieldnames=list(allocated[0]))
        writer.writeheader()
        writer.writerows(allocated)
    args.receipt_out.parent.mkdir(parents=True,exist_ok=True)
    args.receipt_out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",
                                encoding="utf-8")


if __name__=="__main__":
    main()

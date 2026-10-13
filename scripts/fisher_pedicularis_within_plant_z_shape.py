"""Fisher test of predator-dependent relative floral exsertion value.

The two-flower cyclic P. rex design randomizes predator G to MOTHER
PLANTS, then z levels to two distinct flowers within each plant.
Take the within-plant viable-seed contrast D_i = Y_i(z_b)-Y_i(z_a)
for the two pre-assigned adjacent cyclic ranks a=edge, b=(edge+1)%5.

Sharp *contrast* null:
    D_i(EXCLUDED) == D_i(EXPOSED)  for EVERY eligible plant i.
This permits arbitrary plant-specific, z-INDEPENDENT additive G gains in
absolute seed count, and is therefore weaker than the "no G effect on any
flower" sharp null in the earlier Fisher test. Conditional on preassigned
z pairs, under the sharp D-null, exchange the TWO MOTHER-PLANT G labels
within each matched patch-stage-cycle-edge pair; never permute flowers.

Predeclared functional contrast:
  theta = [mu_EXCLUDED(z4)-mu_EXCLUDED(z2)]
          -[mu_EXPOSED(z4)-mu_EXPOSED(z2)].
A symmetric two-route graph representation uses edge difference weights
(-1,-1,+1,+1,-1)/2, on cyclic edges z0->z1, ..., z4->z0.
All five pairs per batch contribute; T is in viable seeds per flower.

Positive theta means the relative fitness of high exsertion z4 versus
intermediate z2 is greater when predators are excluded. It is NOT a
test of the weak hypothesis of the full population optimum rank shift.
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from scripts.fisher_pedicularis_plant_pair_G_randomization import (
    _pairs as verified_source_pairs,
    _p_from_stats,
    DEFAULT_MONTE_CARLO_PERMUTATIONS,
    EXACT_MAX_PAIRS,
)
from scripts.plan_pedicularis_two_flower_cyclic_blocks import _rows_csv
from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256


SCHEMA="PEDICULARIS_MATERNAL_PAIR_WITHIN_Z_SHAPE_FISHER_V1"
CYCLE_WEIGHTS_TWICE=(-1,-1,+1,+1,-1)
TARGET_RANKS=(4,2)


def _validate_edge_pairs(pairs:list[dict])->int:
    if not pairs or len(pairs)%5:
        raise ValueError("Fisher shape statistic needs complete 5-edge cyclic batches")
    groups={}
    for p in pairs:
        if (not isinstance(p,dict) or
            type(p.get("edge")) is not int or not 0<=p["edge"]<5):
            raise ValueError("edge pair needs valid integer rank")
        a=p["edge"]; b=(a+1)%5
        for g in ("excluded","exposed"):
            if g not in p or set(p[g].get("by_z",{}))!={a,b}:
                raise ValueError("both plants must have same cyclic two-z pair")
            if any(type(y) is not int or y<0
                   for y in p[g]["by_z"].values()):
                raise ValueError("seed counts must be nonnegative integers")
        if p["excluded"].get("plant_id")==p["exposed"].get("plant_id"):
            raise ValueError("predator arms cannot share a mother plant")
        group=(p.get("patch_id"),p.get("stage_block_id"))
        if any(not x for x in group):
            raise ValueError("matched edge needs registered source patch and stage")
        groups.setdefault(group,set())
        if a in groups[group]:
            raise ValueError("cyclic rank edge is duplicated in patch-stage batch")
        groups[group].add(a)
    if any(v!=set(range(5)) for v in groups.values()):
        raise ValueError("patch-stage batch has incomplete rank cycle")
    return len(groups)


def _per_pair_raw_terms(pairs:list[dict])->tuple[int,list[int]]:
    """Integer twice-T contributions; exact denominators are 2*n_batches."""
    batches=_validate_edge_pairs(pairs)
    contributions=[]
    for p in pairs:
        a=p["edge"];b=(a+1)%5
        ds={}
        for g in ("excluded","exposed"):
            y=p[g]["by_z"]
            ds[g]=y[b]-y[a]
        contributions.append(
            CYCLE_WEIGHTS_TWICE[a]*(ds["excluded"]-ds["exposed"])
        )
    return batches,contributions


def fisher_within_plant_shape_pairs(
    pairs:list[dict], *,
    monte_carlo_permutations:int=DEFAULT_MONTE_CARLO_PERMUTATIONS,
    random_seed:int=20261013,
)->dict:
    if (
        type(monte_carlo_permutations) is not int
        or not 999<=monte_carlo_permutations<=100000
        or type(random_seed) is not int
        or not 0<=random_seed<=2**63-1
    ):
        raise ValueError("Fisher permutations or random seed invalid")
    batches,terms=_per_pair_raw_terms(pairs)
    n_pairs=len(terms)
    observed_twice=sum(terms)
    exact=n_pairs<=EXACT_MAX_PAIRS
    if exact:
        configs=range(1<<n_pairs)
    else:
        rng=random.Random(random_seed)
        configs=(rng.getrandbits(n_pairs)
                 for _ in range(monte_carlo_permutations))
    # Under sharp D-null, swapping whole-plant G labels reverses
    # the observed D_E-D_X sign of this edge, not its magnitude.
    statistics=[
        sum(-term if bits&(1<<i) else term
            for i,term in enumerate(terms))
        for bits in configs
    ]
    test=_p_from_stats(observed_twice,statistics,exact=exact)
    return {
        "population_target_under_unconditional_z_slot_randomization":
            "(mu_excluded_z4-mu_excluded_z2)-(mu_exposed_z4-mu_exposed_z2)",
        "finite_source_statistic_is_symmetrically_weighted_within_plant_path_score":True,
        "finite_source_score_not_identical_to_raw_cell_mean_difference":True,
        "source_contrast_ranks":{"high":4,"intermediate":2},
        "observed_relative_exsertion_advantage_count_per_flower":
            observed_twice/(2*batches),
        "observed_exact_twice_weighted_numerator":observed_twice,
        "target_sign":"POSITIVE" if observed_twice>0 else (
            "NEGATIVE" if observed_twice<0 else "ZERO"
        ),
        "n_patch_stage_batches":batches,
        "n_matched_plant_pairs":n_pairs,
        "n_distinct_mother_plants":2*n_pairs,
        "n_assigned_fruit_flowers":4*n_pairs,
        "cycle_twice_weights":list(CYCLE_WEIGHTS_TWICE),
        **test,
        "tested_sharp_null":
            "ALL_PLANTS_SAME_WITHIN_Z_PAIR_SEED_COUNT_DIFFERENCE_ACROSS_G",
        "plant_specific_common_additive_G_seed_gain_allowed_under_null":True,
        "randomization_unit":"WHOLE_MATERNAL_PLANT_PAIRED_WITHIN_PATCH_STAGE_EDGE",
        "individual_flower_permutation_prohibited":True,
        "weak_null_of_no_mean_G_by_Z_contrast_tested":False,
        "weak_null_of_equal_population_optimum_ranks_tested":False,
        "shape_contrast_not_pure_function_optimum":True,
    }


def build(rows:list[dict],receipt:dict, *,
          monte_carlo_permutations:int=DEFAULT_MONTE_CARLO_PERMUTATIONS,
          random_seed:int=20261013)->dict:
    pairs=verified_source_pairs(rows,receipt)
    result=fisher_within_plant_shape_pairs(
        pairs,monte_carlo_permutations=monte_carlo_permutations,
        random_seed=random_seed,
    )
    return {
        "receipt_schema":SCHEMA,
        "status":"NON_GATING_SHARP_WITHIN_PLANT_RESPONSE_NULL_ONLY",
        "source_population":receipt["population_id"],
        "source_season":receipt["season_id"],
        "source_allocation_identity_sha256":
            receipt["allocation_identity_sha256"],
        "source_complete_seed_fate_rows_sha256":_semantic_sha256(
            sorted(rows,key=lambda r:(r["plant_id"],r["flower_id"]))
        ),
        "source_field_data_independently_verified":False,
        **result,
        "claim_ceiling":[
            "all_original_assigned_flower_and_plant_ids_verified_first",
            "exact_final_mature_seed_counts_required_no_missing_fates_imputed",
            "G_randomization_must_truly_pair_whole_plants_by_z_edge",
            "no_between_plant_G_spillover_or_trait_geometry_interference_verified",
            "within_plant_pair_difference_null_not_population_mean_shape_null",
            "conditional_edge_pair_score_not_raw_z4_z2_cell_mean_difference",
            "arbitrary_plant_specific_common_additive_G_gain_cancels_in_D",
            "observed_G_by_z_shape_effect_not_proof_of_changed_fitness_optimum",
            "pilot_z_manipulation_first_stage_and_G_selectivity_unqualified",
            "no_P0_P1_G_P2_W1_W2_SCH_L_or_SLK_architecture_inference",
        ],
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("exact_fruit_fate_csv",type=Path)
    p.add_argument("frozen_two_flower_design_receipt_json",type=Path)
    p.add_argument("--monte-carlo-permutations",type=int,
                   default=DEFAULT_MONTE_CARLO_PERMUTATIONS)
    p.add_argument("--seed",type=int,default=20261013)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    rows=_rows_csv(a.exact_fruit_fate_csv)
    receipt=json.loads(a.frozen_two_flower_design_receipt_json.read_text(
        encoding="utf-8"
    ))
    r=build(rows,receipt,monte_carlo_permutations=a.monte_carlo_permutations,
            random_seed=a.seed)
    serialized=json.dumps(r,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(serialized,encoding="utf-8")
    else:
        print(serialized,end="")


if __name__=="__main__":
    main()

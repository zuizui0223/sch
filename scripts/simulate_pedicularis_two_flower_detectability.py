"""Scenario-dependent detectability for the SCH two-flower cyclic design.

Simulation is a DESIGN SENSITIVITY study, never observed P. rex seed data and
never a calibrated 80%-power calculation. Uses the exact live candidate
plant-level G / within-plant cyclic z allocator for every replicate.

Outcomes are rounded, bounded synthetic intact seed counts with:
  - correlated maternal effects shared by the two flowers on each plant;
  - independent patch-stage effects shared by ten plants;
  - flower-level residual variation;
  - optional outcome-dependent missing mature-fruit fate;
  - all allocated missing fruits retained as [0, seed_cap].

For each simulated realization compute:
  (a) positive finite-grid optimum shift using complete latent outcomes,
  (b) source-fate-bound *guaranteed* positive shift,
  (c) whether (b) persists after deletion of ANY entire plant.

These are proportions of scenarios where a DESCRIPTIVE sign is determined,
not population 95% CIs, Type I-calibrated significance or confirmatory power.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from scripts.plan_pedicularis_two_flower_cyclic_blocks import build as allocate

SCHEMA = "SCH_TWO_FLOWER_SCENARIO_DETECTABILITY_CONFIG_V1"
RESULT_SCHEMA = "SCH_TWO_FLOWER_SCENARIO_DETECTABILITY_V1"
PROFILE_KEYS = ("EXCLUDED", "EXPOSED")


def _number(value, name: str, *, minimum: float = 0) -> float:
    if type(value) not in (int, float) or not math.isfinite(value) or value < minimum:
        raise ValueError(f"{name}: finite numeric value >= {minimum} required")
    return float(value)


def _integer(value, name: str, *, minimum: int, maximum: int) -> int:
    if type(value) is not int or not minimum <= value <= maximum:
        raise ValueError(f"{name}: integer in [{minimum},{maximum}] required")
    return value


def _config(raw: dict) -> dict:
    if not isinstance(raw, dict) or raw.get("schema") != SCHEMA:
        raise ValueError("two-flower scenario config schema mismatch")
    grid = raw.get("patch_stage_batch_grid")
    if (not isinstance(grid, list) or not grid or len(grid) != len(set(grid))):
        raise ValueError("patch-stage batch grid must be unique and nonempty")
    for b in grid:
        _integer(b, "batch_grid", minimum=1, maximum=200)
    replicates = _integer(raw.get("replicates_per_grid_point"), "replicates",
                          minimum=10, maximum=2000)
    seed = _integer(raw.get("random_seed"), "random_seed",
                    minimum=0, maximum=2**63-1)
    cap = _integer(raw.get("maximum_intact_seeds_per_flower"),
                   "maximum_intact_seeds_per_flower",minimum=1,maximum=100000)
    scenarios = raw.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("at least one simulation scenario is required")
    validated = []
    seen = set()
    for scene in scenarios:
        if not isinstance(scene, dict):
            raise ValueError("scenario must be a named object")
        sid = scene.get("scenario_id")
        if not isinstance(sid, str) or not sid or sid in seen:
            raise ValueError("scenario ID must be unique and resolved")
        seen.add(sid)
        profiles = scene.get("fitness_curve_seed_counts")
        if not isinstance(profiles, dict) or set(profiles) != set(PROFILE_KEYS):
            raise ValueError("scenario must have EXCLUDED and EXPOSED curves")
        for g in PROFILE_KEYS:
            if not isinstance(profiles[g], list) or len(profiles[g]) != 5:
                raise ValueError("each curve needs five physically registered z ranks")
            for val in profiles[g]:
                _number(val, "curve mean")
                if val > cap:
                    raise ValueError("scenario mean seed count exceeds source cap")
        mode = scene.get("missingness_mechanism")
        if mode not in ("MCAR", "OUTCOME_DEPENDENT"):
            raise ValueError("missingness must be MCAR or OUTCOME_DEPENDENT")
        p = _number(scene.get("maturity_fate_missing_rate"),
                    "maturity_fate_missing_rate")
        if p >= 1:
            raise ValueError("missingness probability must be <1")
        for v in ("patch_sd","plant_sd","flower_sd"):
            _number(scene.get(v),v)
        validated.append(scene)
    eligibility = raw.get("eligible_two_flower_plant_rate_scenarios", [])
    if not isinstance(eligibility, list) or any(
        type(x) not in (int, float) or not math.isfinite(x) or not 0 < x <= 1
        for x in eligibility
    ) or len(eligibility) != len(set(eligibility)):
        raise ValueError("eligibility plant-rate assumptions must be unique in (0,1]")
    confidence = _number(
        raw.get("target_probability_all_strata_can_fill", 0.95),
        "target_probability_all_strata_can_fill"
    )
    if not 0 < confidence < 1:
        raise ValueError("eligibility target must be in (0,1)")
    return {
        "grid": sorted(grid), "replicates":replicates, "seed":seed,
        "cap":cap, "scenarios":validated,
        "eligibility_rates":eligibility, "target_eligibility":confidence,
    }


def _prob_at_least_k_eligible(screened:int,k:int,p:float)->float:
    """Exact binomial design assumption, not verified P. rex flower supply."""
    if screened<k:
        return 0.0
    if p==1:
        return 1.0
    # Only k-1 lower failures; exact combinatorial expression.
    failed=sum(
        math.comb(screened,j)*p**j*(1-p)**(screened-j)
        for j in range(k)
    )
    return max(0.0,min(1.0,1.0-failed))


def _screening_requirement(batches:int,eligible_rate:float,target:float)->dict:
    """Minimal screen count per independently eligible patch-stage stratum.

    Assumes iid Bernoulli eligibility within each stratum and identical p
    across strata, so the chance all B strata have >=10 eligible plants
    is [P(Binomial(n,p)>=10)]**B. This does not solve sampling bias.
    """
    if batches<1 or not 0<eligible_rate<=1 or not 0<target<1:
        raise ValueError("invalid plant supply assumption")
    minimum=10
    while minimum<=10000:
        per=_prob_at_least_k_eligible(minimum,10,eligible_rate)
        if per**batches+1e-12>=target:
            return {
                "n_patch_stage_batches":batches,
                "assumed_independent_plant_two_flower_eligibility_rate":eligible_rate,
                "minimal_plants_screened_per_batch":minimum,
                "total_plants_screened_across_batches":minimum*batches,
                "required_eligible_plants_per_batch":10,
                "assumed_probability_every_batch_can_fill":per**batches,
                "binomial_eligibility_screening_is_not_field_observation":True,
            }
        minimum+=1
    raise ValueError("eligibility scenario needs >10000 plant screens per batch")


def _derive_seed(seed:int,*names:str) -> int:
    value=hashlib.sha256(json.dumps([seed,*names],
                                     separators=(",",":")).encode()).digest()
    return int.from_bytes(value[:8],"big")


def _manifest(n_batches:int) -> list[dict[str,str]]:
    return [
        {
            "population_id":"SYNTHETIC_P_REX",
            "season_id":"SYNTHETIC_YEAR",
            "patch_id":f"INDEPENDENT_PATCH_{batch:03d}",
            "stage_block_id":"MATCHED_STAGE",
            "plant_id":f"PATCH{batch:03d}_PLANT{plant:02d}",
            "flower_id":f"PATCH{batch:03d}_PLANT{plant:02d}_F{flower}",
            "flower_position_code":f"POSITION_{flower}",
        }
        for batch in range(n_batches)
        for plant in range(10)
        for flower in range(2)
    ]


def _settings() -> list[dict[str,str]]:
    return [
        {
            "assigned_z_level":f"Z{z}",
            "assigned_z_rank":str(z),
            "manipulation_setting_id":f"SYNTHETIC_Z{z}_NOT_QUALIFIED",
            "sham_control":"1" if z == 4 else "0",
        }
        for z in range(5)
    ]


def _possible_optima(cells:dict[str,dict[int,tuple[float,float]]]) -> dict:
    states = {}
    for g in PROFILE_KEYS:
        benchmark=max(lo for lo,hi in cells[g].values())
        possible=sorted(z for z,(lo,hi) in cells[g].items()
                        if hi>=benchmark-1e-10)
        if not possible:
            raise AssertionError("every source state needs possible optimum")
        states[g]=possible
    ex,ep=states["EXCLUDED"],states["EXPOSED"]
    return {
        "excluded_possible":ex, "exposed_possible":ep,
        "outer_rank_shift":[min(ex)-max(ep),max(ex)-min(ep)],
        "guaranteed_positive":min(ex)>max(ep),
        "guaranteed_negative":max(ex)<min(ep),
        "both_state_optima_unique":len(ex)==len(ep)==1,
    }


def _means(records:list[dict], *, omitted_plant:str | None=None,
           use_latent_outcomes:bool=False) -> dict:
    bins=defaultdict(list)
    for r in records:
        if r["plant_id"]==omitted_plant:
            continue
        g,z=r["predator_treatment"],r["z"]
        if use_latent_outcomes:
            bins[(g,z)].append((r["latent_count"],r["latent_count"]))
        else:
            bins[(g,z)].append((r["bound_lower"],r["bound_upper"]))
    result={g:{} for g in PROFILE_KEYS}
    for g in PROFILE_KEYS:
        for z in range(5):
            b=bins[(g,z)]
            if not b:
                raise ValueError("design realization lacks data in z x G cell")
            result[g][z]=(sum(x for x,y in b)/len(b),
                          sum(y for x,y in b)/len(b))
    return result


def _one_replicate(
    *,
    scene:dict, n_batches:int, cap:int, seed:int,
    check_plant_deletion:bool,
) -> dict:
    rng=random.Random(seed)
    assignments,_=allocate(
        _manifest(n_batches),_settings(),
        allocation_seed=f"POWER_SCENARIO_FROZEN_{seed:020d}",
        g_exclusion_candidate_method="SYNTHETIC_G_EXCLUSION_UNQUALIFIED",
        g_exposed_sham_candidate_method="SYNTHETIC_G_EXPOSED_UNQUALIFIED",
    )
    patch_effects={}
    plant_effects={}
    records=[]
    p=scene["maturity_fate_missing_rate"]
    for row in sorted(assignments,key=lambda x:x["flower_id"]):
        patch,plant=row["patch_id"],row["plant_id"]
        if patch not in patch_effects:
            patch_effects[patch]=rng.gauss(0,scene["patch_sd"])
        if plant not in plant_effects:
            plant_effects[plant]=rng.gauss(0,scene["plant_sd"])
        z=int(row["assigned_z_rank"])
        g=row["predator_treatment"]
        latent=(
            scene["fitness_curve_seed_counts"][g][z]
            +patch_effects[patch]+plant_effects[plant]
            +rng.gauss(0,scene["flower_sd"])
        )
        y=max(0,min(cap,int(math.floor(latent+0.5))))
        prob=p
        if scene["missingness_mechanism"]=="OUTCOME_DEPENDENT":
            # Higher predation burden / weaker seed yield -> more likely
            # that maturity outcome is unascertainable. This assumption
            # deliberately violates MCAR, yet the interval method does
            # not impute using either mechanism.
            prob=min(0.95,p*(0.5+1.5*(1-y/cap)))
        missing=rng.random()<prob
        records.append({
            "plant_id":plant,"predator_treatment":g,"z":z,
            "latent_count":y,
            "bound_lower":0 if missing else y,
            "bound_upper":cap if missing else y,
            "missing":missing,
        })
    complete=_possible_optima(_means(records,use_latent_outcomes=True))
    bounded=_possible_optima(_means(records))
    stable=False
    if check_plant_deletion and bounded["guaranteed_positive"]:
        plants=sorted({r["plant_id"] for r in records})
        stable=all(_possible_optima(
            _means(records,omitted_plant=plant)
        )["guaranteed_positive"] for plant in plants)
    return {
        "full_latent_positive":complete["guaranteed_positive"],
        "source_bounded_positive":bounded["guaranteed_positive"],
        "plant_deletion_stable_positive":stable,
        "all_mature_fates_counted":not any(r["missing"] for r in records),
        "n_lost_fruit_outcomes":sum(r["missing"] for r in records),
    }


def _limiting_identification(scene:dict,cap:int)->dict:
    """Large-n *plug-in* under uniform cell missing fraction m.

    For each hypothetical z x G mean mu, complete-case rate (1-m)
    and worst-case missing viable count [0,cap] produce asymptotic
    bounds [(1-m)*mu,(1-m)*mu+m*cap]. This remains a sensitivity
    statement even if the actual missingness is outcome-dependent.
    """
    p=scene["maturity_fate_missing_rate"]
    result={g:{} for g in PROFILE_KEYS}
    for g in PROFILE_KEYS:
        for z,mu in enumerate(scene["fitness_curve_seed_counts"][g]):
            result[g][z]=((1-p)*mu,(1-p)*mu+p*cap)
    return _possible_optima(result)


def build(config:dict)->dict:
    cfg=_config(config)
    results=[]
    for scene in cfg["scenarios"]:
        for batches in cfg["grid"]:
            runs=[
                _one_replicate(
                    scene=scene,
                    n_batches=batches,cap=cfg["cap"],
                    seed=_derive_seed(cfg["seed"],scene["scenario_id"],
                                      str(batches),str(i)),
                    check_plant_deletion=(
                        scene.get("include_plant_deletion_diagnostic",False)
                    ),
                ) for i in range(cfg["replicates"])
            ]
            n=cfg["replicates"]
            results.append({
                "scenario_id":scene["scenario_id"],
                "n_patch_stage_batches":batches,
                "n_plants":10*batches,
                "n_assigned_fruit_flowers":20*batches,
                "n_per_z_by_G":2*batches,
                "n_synthetic_replicates":n,
                "fraction_complete_latent_guaranteed_positive_shift":
                    sum(x["full_latent_positive"] for x in runs)/n,
                "fraction_fate_bounded_guaranteed_positive_shift":
                    sum(x["source_bounded_positive"] for x in runs)/n,
                "fraction_fate_bounded_positive_and_stable_to_plant_deletion":
                    sum(x["plant_deletion_stable_positive"] for x in runs)/n,
                "mean_fraction_missing_mature_fruit_outcomes":
                    sum(x["n_lost_fruit_outcomes"] for x in runs)/
                    (n*20*batches),
                "simulation_success_probabilities_not_calibrated_power":True,
            })
    limiting={
        s["scenario_id"]:{
            "uniform_missing_fraction_plug_in":s["maturity_fate_missing_rate"],
            **_limiting_identification(s,cfg["cap"]),
            "not_an_asymptotic_claim_for_outcome_dependent_missingness":(
                s["missingness_mechanism"]=="OUTCOME_DEPENDENT"
            ),
        } for s in cfg["scenarios"]
    }
    supply=[
        _screening_requirement(b,p,cfg["target_eligibility"])
        for b in cfg["grid"] for p in cfg["eligibility_rates"]
    ]
    return {
        "receipt_schema":RESULT_SCHEMA,
        "status":"SYNTHETIC_HIERARCHICAL_DESIGN_DETECTABILITY_NOT_POWER",
        "config":config,
        "design":"ACTUAL_TWO_FLOWER_CYCLIC_ALLOCATOR_PLANT_G_FLOWER_Z",
        "n_unique_scenarios":len(cfg["scenarios"]),
        "n_random_synthetic_datasets":len(results)*cfg["replicates"],
        "scenario_grid":results,
        "hypothetical_two_flower_plant_supply":supply,
        "uniform_cell_missingness_analytic_limit":limiting,
        "no_nominal_alpha_or_valid_p_values_computed":True,
        "sample_size_requirement_calibrated_from_focal_empirical_variance":False,
        "no_field_effect_or_optimum_observed":True,
        "claim_ceiling":[
            "all_fitness_curves_and_variance_components_are_user_hypotheses_not_P_rex_data",
            "patch_groups_in_simulation_are_independent_by_construction_not_field_evidence",
            "plant_randomized_G_not_a_within_plant_comparison",
            "within_plant_z_residuals_share_a_maternal_random_effect",
            "missing_fates_are_bounded_zero_to_per_flower_seed_cap_not_imputed_zero",
            "source_cap_too_high_relative_to_biological_gap_can_block_sign_at_any_n",
            "simulation_rate_is_not_design_based_confidence_or_confirmatory_power",
            "conditional_plant_deletion_stability_is_not_a_cluster_bootstrap_CI",
            "null_scenario_positive_rate_is_not_calibrated_type_I_error",
            "plant_eligibility_rate_independence_is_hypothetical_and_not_a_sampling_frame",
            "no_P0_G_P2_W1_W2_or_SCH_architecture_promotion",
        ],
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("scenario_config_json",type=Path)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    result=build(json.loads(args.scenario_config_json.read_text(encoding="utf-8")))
    text=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding="utf-8")
    else:
        print(text,end="")


if __name__=="__main__":
    main()

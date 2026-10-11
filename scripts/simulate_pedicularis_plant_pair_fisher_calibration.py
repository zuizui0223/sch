"""Design-faithful synthetic Fisher sharp-null calibration for P. rex.

This exercise REUSES the original plant-level cyclic z/G randomizer and the
actual source-compatible plant-pair Fisher test, not the earlier descriptive
optimum-shift identification fractions. It simulates complete mature seed
counts only: any censored or unobserved outcome must fail closed in the
real Fisher routine, not be imputed to a generated value.

The five scenario labels distinguish (i) true Fisher sharp null,
(ii) constant nonzero G seed gain without a true optimum shift,
(iii) G effects varying across plants but not driven by z,
(iv) z-varying G effects with the same specified optimum, and
(v) a truly different peak. Sharp-null calibration can be measured;
rejection in other scenarios only rejects a strong sharp null and
is NOT automatically evidence of population-optimum displacement.
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
from scripts.simulate_pedicularis_two_flower_detectability import (
    _manifest, _settings,
)
from scripts.fisher_pedicularis_plant_pair_G_randomization import (
    fisher_from_pairs, statistic,
)

SCHEMA="SCH_P_REX_MATCHED_PLANT_FISHER_SIMULATION_CONFIG_V1"
RESULT="SCH_P_REX_MATCHED_PLANT_FISHER_SIMULATION_RESULTS_V1"
MODES={
    "SHARP_NO_G_EFFECT",
    "COMMON_ADDITIVE_G_GAIN",
    "HETEROGENEOUS_PLANT_G_GAIN",
    "CHANGED_G_BY_Z_SAME_PEAK",
    "PREDATOR_EXCLUSION_SHIFTS_PEAK",
}
EXPOSED_CURVE=(5,8,13,8,5)
POTENTIAL_EXCLUDED={
    "SHARP_NO_G_EFFECT":(5,8,13,8,5),
    "COMMON_ADDITIVE_G_GAIN":(8,11,16,11,8),
    "HETEROGENEOUS_PLANT_G_GAIN":(8,11,16,11,8),
    "CHANGED_G_BY_Z_SAME_PEAK":(8,10,17,12,9),
    "PREDATOR_EXCLUSION_SHIFTS_PEAK":(5,7,10,14,19),
}


def _integer(v,name,lo,hi):
    if type(v) is not int or not lo<=v<=hi:
        raise ValueError(f"{name}: integer required in [{lo},{hi}]")
    return v


def _num(v,name,lo=0):
    if type(v) not in (int,float) or not math.isfinite(v) or v<lo:
        raise ValueError(f"{name}: nonnegative finite numeric required")
    return float(v)


def _validate(config):
    if not isinstance(config,dict) or config.get("schema")!=SCHEMA:
        raise ValueError("Fisher design calibration config schema mismatch")
    nrep=_integer(config.get("replicates_per_condition"),"replicates",10,3000)
    seed=_integer(config.get("random_seed"),"seed",0,2**63-1)
    cap=_integer(config.get("intact_seeds_upper_cap"),"cap",25,1000)
    alpha=_num(config.get("one_sided_alpha"),"alpha")
    if not 0<alpha<=0.2:
        raise ValueError("one-sided alpha must be in (0,0.2]")
    mc=_integer(config.get("monte_carlo_permutations"),"Monte Carlo",999,100000)
    batches=config.get("patch_stage_batch_grid")
    if (not isinstance(batches,list) or not batches
        or len(batches)!=len(set(batches))):
        raise ValueError("distinct nonempty batch grid required")
    for n in batches:
        _integer(n,"batch count",1,20)
    modes=config.get("scenario_modes")
    if (not isinstance(modes,list) or not modes
        or len(modes)!=len(set(modes)) or any(m not in MODES for m in modes)):
        raise ValueError("scenario modes must be recognized and distinct")
    maternal=_num(config.get("plant_sd"),"plant_sd")
    floral=_num(config.get("flower_sd"),"flower_sd")
    patch=_num(config.get("patch_sd"),"patch_sd")
    hetero=_num(config.get("G_gain_plant_heterogeneity_sd"),"heterogeneity_sd")
    return {
        "replicates":nrep,"seed":seed,"cap":cap,"alpha":alpha,"mc":mc,
        "batches":sorted(batches),"modes":modes,
        "plant_sd":maternal,"flower_sd":floral,"patch_sd":patch,
        "heterogeneous_G_sd":hetero,
    }


def _subseed(seed,*tokens):
    s=json.dumps([seed,*tokens],separators=(",",":"))
    return int.from_bytes(hashlib.sha256(s.encode()).digest()[:8],"big")


def _outcome(latent,cap):
    return max(0,min(cap,int(math.floor(latent+0.5))))


def simulate_pairs(*,scenario_mode,n_batches,seed,cap,
                   patch_sd,plant_sd,flower_sd,heterogeneous_G_sd):
    """Generate a paired source-compatible assignment under a fixed potential model.

    All G effects are constructed as potential outcomes BEFORE inspecting
    the assigned G label. In SHARP_NO_G_EFFECT the two potential seed
    outcomes are exactly the same for each individual flower.
    """
    if scenario_mode not in MODES:
        raise ValueError("unknown potential-outcome scenario")
    rng=random.Random(seed)
    assigned,_=allocate(
        _manifest(n_batches),_settings(),
        allocation_seed=f"SHARP_FISHER_DESIGN_SEED_{seed:020d}",
        g_exclusion_candidate_method="SYNTHETIC_INDEPENDENT_G_UNQUALIFIED",
        g_exposed_sham_candidate_method="SYNTHETIC_G_EXPOSED_SHAM",
    )
    patches={}
    mothers={}
    treatment_gain={}
    paired=defaultdict(dict)
    for row in sorted(assigned,key=lambda r:r["flower_id"]):
        patch,plant=row["patch_id"],row["plant_id"]
        if patch not in patches:
            patches[patch]=rng.gauss(0,patch_sd)
        if plant not in mothers:
            mothers[plant]=rng.gauss(0,plant_sd)
            treatment_gain[plant]=rng.gauss(0,heterogeneous_G_sd)
        z=int(row["assigned_z_rank"])
        # The potential outcomes are defined at this assigned z setting.
        baseline=(EXPOSED_CURVE[z]+patches[patch]+mothers[plant]
                  +rng.gauss(0,flower_sd))
        if scenario_mode=="SHARP_NO_G_EFFECT":
            gain=0
        elif scenario_mode=="COMMON_ADDITIVE_G_GAIN":
            gain=3
        elif scenario_mode=="HETEROGENEOUS_PLANT_G_GAIN":
            gain=3+treatment_gain[plant]
        else:
            gain=POTENTIAL_EXCLUDED[scenario_mode][z]-EXPOSED_CURVE[z]
        # Rounding and finite ovule/seed cap make seed counts discrete.
        # For an additive effect, extreme clipping can break *exact*
        # constant-additivity on realized potential counts, so we do
        # not label those outputs a perfect constant-tau Fisher null.
        y0=_outcome(baseline,cap)
        y1=_outcome(baseline+gain,cap)
        observed=(y1 if row["predator_treatment"]=="EXCLUDED" else y0)
        key=(row["patch_id"],row["stage_block_id"],
             int(row["pair_cycle_edge"]))
        g=row["predator_treatment"]
        entity=paired[key].setdefault(g,{
            "plant_id":plant,"by_z":{},"cap_by_z":{},
        })
        if entity["plant_id"]!=plant:
            raise AssertionError("cyclic edge assigned multiple plants to one G arm")
        entity["by_z"][z]=observed
        entity["cap_by_z"][z]=cap
        if scenario_mode=="SHARP_NO_G_EFFECT" and y0!=y1:
            raise AssertionError("sharp no-G-effect potential outcomes drifted")
    if len(paired)!=5*n_batches or any(set(v)!={"EXCLUDED","EXPOSED"}
                                      for v in paired.values()):
        raise AssertionError("source cyclic design no longer matches Fisher pairs")
    pairs=[
        {"patch_id":patch,"stage_block_id":stage,"edge":edge,
         "excluded":g["EXCLUDED"],"exposed":g["EXPOSED"]}
        for (patch,stage,edge),g in sorted(paired.items())
    ]
    if any(
        set(p["excluded"]["by_z"])!=set(p["exposed"]["by_z"])
        or set(p["excluded"]["by_z"])!={p["edge"],(p["edge"]+1)%5}
        or p["excluded"]["plant_id"]==p["exposed"]["plant_id"]
        for p in pairs
    ):
        raise AssertionError("Fisher input pairs do not preserve source cyclic z assignments")
    return pairs


def _wilson(k,n):
    """Monte Carlo uncertainty on a simulated probability, NOT field-effect CI."""
    z=1.959963984540054
    p=k/n
    d=1+z*z/n
    center=(p+z*z/(2*n))/d
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return [max(0,center-half),min(1,center+half)]


def build(config:dict)->dict:
    cfg=_validate(config)
    result=[]
    for mode in cfg["modes"]:
        for batch in cfg["batches"]:
            rows=[]
            for iteration in range(cfg["replicates"]):
                seed=_subseed(cfg["seed"],mode,str(batch),str(iteration))
                pairs=simulate_pairs(
                    scenario_mode=mode,n_batches=batch,seed=seed,cap=cfg["cap"],
                    patch_sd=cfg["patch_sd"],plant_sd=cfg["plant_sd"],
                    flower_sd=cfg["flower_sd"],
                    heterogeneous_G_sd=cfg["heterogeneous_G_sd"],
                )
                test=fisher_from_pairs(
                    pairs,monte_carlo_permutations=cfg["mc"],
                    random_seed=_subseed(seed,"FISHER_SWAPS"),
                )
                s=test["observed_predeclared_peak_statistic"][
                    "exclusion_minus_exposure_peak_midrank"
                ]
                rows.append({
                    "positive_peak":s>0,
                    "sharp_null_rejected":test["one_sided_Fisher_sharp_null_p"]<=cfg["alpha"],
                    "p":test["one_sided_Fisher_sharp_null_p"],
                    "n_pairs":test["n_matched_plant_pairs"],
                    "exact":test["p_calculation"]=="EXACT_CONDITIONAL_ENUMERATION",
                })
            rejects=sum(x["sharp_null_rejected"] for x in rows)
            positive=sum(x["positive_peak"] for x in rows)
            both=sum(x["sharp_null_rejected"] and x["positive_peak"] for x in rows)
            result.append({
                "mode":mode,"n_patch_stage_batches":batch,
                "n_eligible_plants":10*batch,
                "n_fruit_flowers":20*batch,
                "n_matched_plant_pairs":5*batch,
                "n_simulated_allocations":cfg["replicates"],
                "tested_null":"FISHER_SHARP_NO_G_EFFECT_ON_ANY_FLOWER",
                "source_G_label_permutation_unit":"WHOLE_PLANT_WITHIN_Z_PAIR",
                "exact_assignment_enumeration":rows[0]["exact"],
                "one_sided_alpha":cfg["alpha"],
                "n_positive_descriptive_peak_shifts":positive,
                "fraction_positive_descriptive_peak_shifts":positive/len(rows),
                "n_Fisher_sharp_null_rejections":rejects,
                "fraction_Fisher_sharp_null_rejections":rejects/len(rows),
                "simulation_rejection_fraction_Wilson95":_wilson(rejects,len(rows)),
                "n_both_rejected_and_descriptively_positive":both,
                "fraction_both_rejected_and_descriptively_positive":both/len(rows),
                "Monte_Carlo_replicates_per_P_value_when_nonexact":(
                    None if rows[0]["exact"] else cfg["mc"]
                ),
                "weak_null_same_optimum_tested":False,
            })
    return {
        "receipt_schema":RESULT,
        "status":"SYNTHETIC_FISHER_SHARP_NULL_CALIBRATION_NOT_FIELD_POWER",
        "source_synthetic_config":config,
        "n_total_generated_synthetic_datasets":len(result)*cfg["replicates"],
        "scenario_grid":result,
        "null_and_effect_interpretation":{
            "SHARP_NO_G_EFFECT":"actual Fisher sharp null true; rejection fraction estimates its Type-I error in this generator",
            "COMMON_ADDITIVE_G_GAIN":"sharp no-effect null false but designated population peak same; rejection does not prove shift",
            "HETEROGENEOUS_PLANT_G_GAIN":"sharp null false; heterogeneous plant gain without designed z-specific effect",
            "CHANGED_G_BY_Z_SAME_PEAK":"trait-conditioned G differences but designated best z unchanged",
            "PREDATOR_EXCLUSION_SHIFTS_PEAK":"different designated optimal ranks in potential-outcome mean curves",
        },
        "claim_ceiling":[
            "all_curves_sd_and_maturity_counts_synthetic_not_P_rex_observations",
            "calibration_applies_to_Fisher_sharp_no_G_effect_only",
            "no_weak_null_test_for_equal_population_optimum_ranks",
            "rejecting_sharp_no_effect_with_positive_T_does_not_prove_population_peak_shift",
            "nonsharp_effect_cases_report_rejection_frequency_not_optimum_shift_power",
            "plant_G_pair_assignments_not_independent_flower_randomization",
            "complete_final_seed_counts_required_missing_maturity_not_imputed",
            "seed_caps_and_rounded_outcomes_can_modify_exact_potential_curves",
            "simulated_patch_effects_do_not_substitute_for_independent_field_patches",
            "no_empirical_sample_size_recommendation_and_no_P0_G_W1_W2_upgrade",
        ],
    }


def main()->None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("synthetic_config",type=Path)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    r=build(json.loads(args.synthetic_config.read_text(encoding="utf-8")))
    s=json.dumps(r,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s,encoding="utf-8")
    else:
        print(s,end="")


if __name__=="__main__":
    main()

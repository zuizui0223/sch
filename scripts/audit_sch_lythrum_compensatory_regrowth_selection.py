"""Real source-linked Lythrum simulated herbivory / selection-response fork.

Thomsen & Sargent (2017), Annals of Botany doi:10.1093/aob/mcx026,
source Tables 1 and 2 and article methods. This is ONE biological study.

The experiment imposed apical-meristem clipping (not randomized natural
herbivore attack) and paired within-plant floral pollen supplementation.
Original natural-damage reassignments (n=8) limit a strict ITT claim.
No raw plant/capsule rows are available; only published mean/SE and direct
ANCOVA gradient contrasts are compared without fabricating covariance.

Scientific object: contrast the *change in mean phenotype* and
*trait-specific selection gradient* across a simulated damage regime,
versus pollen limitation and nondetected pollinator-mediated selection.
These are different responses and must not be treated as equivalent.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[1]
PHENOTYPES = ROOT / "data/SCH_LYTHRUM_THOMSEN_2017_TREATMENT_MEANS_TABLE1_V1.csv"
SELECTION = ROOT / "data/SCH_H2_LYTHRUM_THOMSEN_2017_SELECTION_GRADIENTS_V1.csv"
DOI = "10.1093/aob/mcx026"
TRAITS = {
    "number_of_inflorescences": ("count_per_plant",8.0,.51,5.4,.72,"F_17.65","<0.0001","SQRT_FOR_F_TEST"),
    "flowering_start_julian": ("day_of_year",196.,1.06,191.,.98,"W_3497","<0.0001","NONPARAMETRIC"),
    "flowering_end_julian": ("day_of_year",236.,.75,236.,.68,"W_2187","0.4159","NONPARAMETRIC"),
    "number_of_flowers": ("count_per_plant",1048.,83.4,825.,80.6,"W_2943","0.0244","NONPARAMETRIC"),
    "number_of_fruit": ("count_per_plant",584.,46.9,445.,43.2,"F_4.967","0.0275","LOG_FOR_F_TEST"),
    "inflorescence_height_cm": ("cm",111.6,3.18,121.8,2.78,"F_5.623","0.0191","UNTRANSFORMED"),
    "seeds_per_fruit": ("count_per_fruit",43.7,2.65,39.6,3.02,"F_1.010","0.3168","UNTRANSFORMED"),
}
# Exact original table 2 values, including author/source significance codes.
# All three columns of mediated contrasts are direct author ANCOVA output,
# and not differences of independently re-estimated treatment slopes.
SELECTION_VALUES = {
    "number_of_inflorescences": {
        "CLIPPED":(.20,.07,"P_LT_0.01"),
        "CONTROL":(.47,.07,"P_LT_0.001"),
        "DAMAGE_TREATMENT_X_TRAIT":(.27,.10,"P_LT_0.01"),
        "POLLINATION_TREATMENT_X_TRAIT":(-.01,.05,"NS"),
        "POLLINATION_X_DAMAGE_X_TRAIT":(-.12,.12,"NS"),
    },
    "inflorescence_height": {
        "CLIPPED":(.22,.06,"P_LT_0.001"),
        "CONTROL":(.33,.09,"P_LT_0.001"),
        "DAMAGE_TREATMENT_X_TRAIT":(.11,.11,"NS"),
        "POLLINATION_TREATMENT_X_TRAIT":(.00,.06,"NS"),
        "POLLINATION_X_DAMAGE_X_TRAIT":(.11,.13,"NS"),
    },
    "flowering_start_time": {
        "CLIPPED":(-.28,.06,"P_LT_0.001"),
        "CONTROL":(-.03,.08,"NS"),
        "DAMAGE_TREATMENT_X_TRAIT":(.25,.10,"P_LT_0.05"),
        "POLLINATION_TREATMENT_X_TRAIT":(-.07,.06,"NS"),
        "POLLINATION_X_DAMAGE_X_TRAIT":(.01,.12,"NS"),
    },
}
CONTRAST_TO_ROLE = {
    "CLIPPED":"TOTAL_SELECTION",
    "CONTROL":"TOTAL_SELECTION",
    "DAMAGE_TREATMENT_X_TRAIT":"MEDIATED_CONTRAST",
    "POLLINATION_TREATMENT_X_TRAIT":"MEDIATED_CONTRAST",
    "POLLINATION_X_DAMAGE_X_TRAIT":"MEDIATED_CONTRAST",
}
TREATMENT_N = {"clipped_final":87, "control_final":86, "final_total":173,
               "original_selected_stems":178,"original_control_reassigned":8,
               "pollen_pair_count":429}
POLLEN_LIMITATION_RELATIVE_PCT = 17.4
POLLEN_LIMITATION_DAMAGE_DIFFERENCE_SOURCE_P = .2718


def _rows(path:Path) -> list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as fh:
        return list(csv.DictReader(fh))


def _fixed_num(record:dict[str,str],key:str)->float:
    value=float(record[key])
    if not math.isfinite(value):
        raise ValueError("nonfinite source value")
    return value


def _exact(received:float,expected:float)->bool:
    return math.isclose(received,expected,rel_tol=0,abs_tol=1e-10)


def _phenotype_index(rows:list[dict[str,str]]) -> dict[str,dict]:
    if len(rows)!=len(TRAITS):
        raise ValueError("Table 1 seven complete source rows required")
    out={}
    for row in rows:
        name=row.get("trait","")
        if name not in TRAITS or name in out:
            raise ValueError("unknown or duplicate original Table 1 phenotype")
        (unit,clip,cse,ctrl,tse,test,p,trans)=TRAITS[name]
        if (row.get("source_doi")!=DOI
            or row.get("source_table")!="Table_1"
            or row.get("plant_taxon")!="Lythrum salicaria"
            or (row.get("unit"),row.get("source_test"),
                row.get("source_p"),row.get("model_transform"))
                !=(unit,test,p,trans)):
            raise ValueError("original phenotype identity or test drift")
        for field,expected in (
            ("clipped_mean",clip),("clipped_se",cse),
            ("control_mean",ctrl),("control_se",tse),
        ):
            if not _exact(_fixed_num(row,field),expected):
                raise ValueError("original Table 1 published mean/SE drift")
        out[name]={
            "clipped_mean":clip,
            "control_mean":ctrl,
            "clipped_se":cse,
            "control_se":tse,
            "clipped_minus_control":round(clip-ctrl,5),
            "relative_change_percent_vs_control":(
                round((clip/ctrl-1)*100,5) if ctrl>0 and unit=="count_per_plant" else None
            ),
            "original_source_p":p,
            "source_test":test,
            "statistical_test_used_transformation":trans,
        }
    return out


def _selection_index(rows:list[dict[str,str]])->dict[str,dict]:
    if len(rows)!=15:
        raise ValueError("Table 2 original 3 traits x 5 terms incomplete")
    out={}
    for row in rows:
        name=row.get("trait","")
        key=row.get("context_or_contrast","")
        if (name not in SELECTION_VALUES or key not in CONTRAST_TO_ROLE
            or key in out.get(name,{})):
            raise ValueError("source Table 2 unknown or duplicate selection term")
        beta,se,flag=SELECTION_VALUES[name][key]
        if (row.get("doi")!=DOI
            or row.get("source_table")!="Table_2"
            or row.get("source_id")!="SCHPRISMA-000284"
            or row.get("programme_id")!="Lythrum_salicaria_Thomsen_selection_program"
            or row.get("estimand_role")!=CONTRAST_TO_ROLE[key]
            or row.get("fitness_measure")!="relative_total_seed_production"
            or row.get("trait_standardization")!="WITHIN_TREATMENT_Z_SCORE"
            or row.get("significance")!=flag):
            raise ValueError("original Table 2 source role/significance drift")
        if (not _exact(_fixed_num(row,"beta_or_delta"),beta)
            or not _exact(_fixed_num(row,"se"),se)):
            raise ValueError("original published Table 2 beta/SE drift")
        out.setdefault(name,{})[key]={"beta":beta,"se":se,"source_significance":flag}
    if {t:set(rows) for t,rows in out.items()}!={t:set(row) for t,row in SELECTION_VALUES.items()}:
        raise ValueError("Table 2 source term identities incomplete")
    for name,coeffs in out.items():
        # Source author reports damage contrast as CONTROL minus CLIPPED.
        observed=coeffs["CONTROL"]["beta"]-coeffs["CLIPPED"]["beta"]
        if not _exact(observed,coeffs["DAMAGE_TREATMENT_X_TRAIT"]["beta"]):
            raise ValueError("original damage contrast does not equal source arm difference")
    return out


def _last_printed_step(val:float)->float:
    # Table 2 SEs and beta contrast cells each print two decimals.
    return .01


def build(phenotypes:list[dict[str,str]],
          selections:list[dict[str,str]])->dict:
    p=_phenotype_index(phenotypes)
    s=_selection_index(selections)
    onset=p["flowering_start_julian"]
    end=p["flowering_end_julian"]
    if not (_exact(end["clipped_minus_control"],0)
            and _exact(onset["clipped_minus_control"],5)):
        raise ValueError("published start and end response changed")
    gradient={}
    z3=NormalDist().inv_cdf(1-.05/(2*3))
    z9=NormalDist().inv_cdf(1-.05/(2*9))
    for trait,coeff in s.items():
        damage=coeff["DAMAGE_TREATMENT_X_TRAIT"]
        beta,se=damage["beta"],damage["se"]
        p_norm=math.erfc(abs(beta)/(math.sqrt(2)*se))
        min_beta=max(0.,abs(beta)-_last_printed_step(beta)/2)
        max_se=se+_last_printed_step(se)/2
        gradient[trait]={
            "clipped_beta":coeff["CLIPPED"]["beta"],
            "control_beta":coeff["CONTROL"]["beta"],
            "damage_control_minus_clipped_delta":beta,
            "damage_source_direct_contrast_se":se,
            "damage_original_source_flag":damage["source_significance"],
            "damage_source_delta_normal_p_diagnostic":round(p_norm,9),
            "bonferroni_three_damage_tests_conditional_95pct":
                [round(beta-z3*se,7),round(beta+z3*se,7)],
            "bonferroni_three_damage_tests_nominal_difference_supported":
                abs(beta)>z3*se,
            "bonferroni_three_damage_tests_rounding_robust":
                min_beta>z3*max_se,
            "bonferroni_all_nine_source_interactions_difference_supported":
                abs(beta)>z9*se,
            "pollination_treatment_x_trait_source_beta":
                coeff["POLLINATION_TREATMENT_X_TRAIT"]["beta"],
            "pollination_treatment_x_trait_source_flag":
                coeff["POLLINATION_TREATMENT_X_TRAIT"]["source_significance"],
            "pollination_x_damage_x_trait_source_flag":
                coeff["POLLINATION_X_DAMAGE_X_TRAIT"]["source_significance"],
            "direct_source_interaction_not_imputed_from_separate_arm_se":True,
        }
    if not all(gradient[t]["pollination_treatment_x_trait_source_flag"]=="NS"
               and gradient[t]["pollination_x_damage_x_trait_source_flag"]=="NS"
               for t in gradient):
        raise ValueError("source contradicts no-detected-pollination-interaction")
    num=gradient["number_of_inflorescences"]
    flow=gradient["flowering_start_time"]
    if not (
        num["damage_original_source_flag"]=="P_LT_0.01"
        and flow["damage_original_source_flag"]=="P_LT_0.05"
        and num["damage_control_minus_clipped_delta"]>0
        and flow["damage_control_minus_clipped_delta"]>0
    ):
        raise ValueError("two damage-conditioned selection responses not recovered")
    group_mean_window={
        "control_end_minus_start":end["control_mean"]-onset["control_mean"],
        "clipped_end_minus_start":end["clipped_mean"]-onset["clipped_mean"],
        "differential_mean_calendar_span_days":(
            (end["clipped_mean"]-onset["clipped_mean"])
            -(end["control_mean"]-onset["control_mean"])
        ),
        "not_plant_level_flowering_duration_distribution":True,
    }
    return {
        "analysis":"sch_lythrum_apical_damage_regrowth_vs_selection_fork_v1",
        "source_doi":DOI,
        "original_study_count":1,
        "study":"Thomsen_Sargent_2017",
        "biological_experiment":"RANDOM_ASSIGNED_APICAL_MERISTEM_CLIPPING_WITH_SOURCE_REASSIGNMENTS",
        "clipping_reassignment_violates_pure_initial_ITT_interpretation":True,
        "source_design_counts":TREATMENT_N,
        "paired_within_plant_pollen_supplementation_not_independent_plant_randomization":True,
        "mean_seed_set_hand_pollen_gain_percent":POLLEN_LIMITATION_RELATIVE_PCT,
        "pollen_limitation_between_damage_groups_original_p":POLLEN_LIMITATION_DAMAGE_DIFFERENCE_SOURCE_P,
        "pollen_limitation_no_difference_detected_is_not_equivalence":True,
        "original_table_1_reported_phenotypes":p,
        "original_table_2_selection_responses":gradient,
        "mean_calendar_window_proxy":group_mean_window,
        "n_damage_interactions_with_original_p_below_0_05":sum(
            v["damage_original_source_flag"] not in ("NS","P_EQ_0.057")
            for v in gradient.values()
        ),
        "n_3_damage_test_bonferroni_normal_supported":sum(
            v["bonferroni_three_damage_tests_nominal_difference_supported"]
            for v in gradient.values()
        ),
        "n_3_damage_test_bonferroni_rounding_robust":sum(
            v["bonferroni_three_damage_tests_rounding_robust"]
            for v in gradient.values()
        ),
        "n_all_9_contrast_bonferroni_supported":sum(
            abs(s[trait][key]["beta"])>z9*s[trait][key]["se"]
            for trait in s
            for key in (
                "DAMAGE_TREATMENT_X_TRAIT",
                "POLLINATION_TREATMENT_X_TRAIT",
                "POLLINATION_X_DAMAGE_X_TRAIT",
            )
        ),
        "ecological_signature":[
            "apical_damage_increases_mean_inflorescences_but_reduces_positive_selection_for_more",
            "apical_damage_delays_mean_flowering_onset_but_increases_selection_for_earlier_onset",
            "later_start_same_group_mean_end_implies_shorter_calendar_window_proxy",
            "pollen_limitation_coexists_with_nondetected_pollinator_mediated_trait_selection",
            "herbivory_tolerance_growth_shift_is_plausible_not_causally_isolated_mediator",
        ],
        "claim_ceiling":[
            "one_published_study_not_an_additional_V27_pollination_programme",
            "artificial_apical_meristem_damage_not_random_natural_herbivory_exposure",
            "eight_natural_attack_controls_reassigned_to_clipped_source_group",
            "plant_level_compensation_mediation_not_identified_without_original_raw_data",
            "differential_mean_flowering_span_not_direct_per_plant_duration_test",
            "seed_set_17_4_percent_gain_not_pollinator_mediated_selection",
            "no_detected_pollinator_interaction_is_not_pollen_equivalence",
            "flower_pair_pollination_treatment_is_within_plant_not_crossed_whole_plant_P",
            "normal_bonferroni_diagnostics_are_secondary_not_original_ancova_p",
            "no_new_measured_phenotype_optima_or_direct_do_z_causality",
            "no_shared_conflict_budget_L_or_Slk_architecture_outcome",
        ],
        "status":"REAL_SOURCE_TOLERANCE_ROUTE_SELECTION_REDIRECTION_NOT_PURE_FUNCTION_OPTIMA",
    }


def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--phenotypes",type=Path,default=PHENOTYPES)
    ap.add_argument("--selection",type=Path,default=SELECTION)
    ap.add_argument("--output",type=Path)
    args=ap.parse_args()
    result=build(_rows(args.phenotypes),_rows(args.selection))
    payload=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")


if __name__=="__main__":
    main()

"""Experimental floral-selection meta pilot, eight independent original programmes.

Primary question (source-data-reanalysis, not unselected systematic meta):
Does additional hand pollination *attenuate the absolute magnitude* of
directional selection across experimental plant programmes, and how many
observed gradient sign changes are statistically supported in BOTH arms?

Outcome-biased study selection is prohibited WITHIN included sources:
include every eligible matched source trait/context pair.
The initial literature roster was purposively assembled in SCH, NOT a
probability-sampled published ecology universe.

Eight independent programmes:
Dactylorhiza, Primula alpicola, Trillium, Gymnadenia [four-programme
frozen audit], Lobelia cardinalis, Trifolium repens (HCN+ stratum),
Aconitum gymnandrum, Lobelia siphilitica (seeds per plant main).
Different fitness model link families (Trillium conditional Poisson),
missing SEs (Trifolium), source-selected traits and two strata in
Gymnadenia make a generic pooled cross-study beta **invalid**.

Study-level direction of mean(|beta_open|-|beta_hand|) is compared by an
exact, two-sided study-cluster sign test. Programme is the independent
scientific unit; 41 matched axis/context comparisons are NOT n=41 studies.
Conditional numerical synthesis for a *narrow common floral count axis*
uses FIVE studies (Dactylorhiza, Primula, Gymnadenia, Lobelia cardinalis,
Aconitum) and source covariance-agnostic SE upper bounds:
    SE(average weighted delta) <= sum(|a_j| SE_j)
normal-Wald inference is conditional on source reported marginal SEs,
Gaussian slopes and independent original programmes.
No unobserved coefficient covariance is assumed zero.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from statistics import NormalDist

from scripts.audit_sch_h2_cross_programme_pollination_edges import (
    SOURCE as V27_SOURCE, READOUT as V27_READOUT,
    read_csv as read_v27,
)
from scripts.audit_sch_four_programme_selection_spectrum import (
    GYM_SOURCE, build as four_build, read_gym,
)

ROOT=Path(__file__).resolve().parents[1]
LOB=ROOT/"data/SCH_H2_LOBELIA_BARTKOWSKA_2012_SELECTION_GRADIENTS_V1.csv"
TRIF=ROOT/"data/SCH_H2_TRIFOLIUM_EXACT_SELECTION_V1.csv"
ACON=ROOT/"data/SCH_META_ACONITUM_2016_SOURCE_TABLE3_SELECTION_V1.csv"
BROWN=ROOT/"data/SCH_META_LOBELIA_SIPHILITICA_2023_SOURCE_TABLE2_SELECTION_V1.csv"

STUDIES=(
    "Aconitum","Dactylorhiza","Gymnadenia","Lobelia_cardinalis",
    "Lobelia_siphilitica","Primula","Trifolium","Trillium",
)
DATA_DOIS={
    "Aconitum":"10.1038/srep34499",
    "Dactylorhiza":"10.1111/j.1469-8137.2010.03296.x",
    "Gymnadenia":"10.1890/14-0119.1",
    "Lobelia_cardinalis":"10.1111/j.1469-8137.2011.04013.x",
    "Lobelia_siphilitica":"10.1002/ece3.10706",
    "Primula":"10.1038/s41598-017-13340-0",
    "Trifolium":"10.1111/jeb.13392",
    "Trillium":"10.1002/ajb2.16101",
}
ACON_TRAITS=frozenset((
    "flower_number","galea_height","mean_nectar_volume",
    "nectar_position_difference",
))
BROWN_TRAITS=frozenset((
    "inflorescence_height","daily_floral_display","petal_brightness",
    "petal_chroma","corolla_projected_area","corolla_tube_length",
))
REGIMES=("HAND_SUPPLEMENTED","AMBIENT_OPEN","REDUCED_OPEN")
BROWN_FITNESS=("relative_seeds_per_plant","relative_fruits_per_plant")
N_ABUNDANCE_PROGRAMMES=5
MAIN_STUDY_N=8


def load(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as fh:
        return list(csv.DictReader(fh))


def number(s:str)->float:
    try:
        x=float(s)
    except (TypeError,ValueError):
        raise ValueError("missing source number") from None
    if not math.isfinite(x):
        raise ValueError("nonfinite source number")
    return x


def edge(study:str,trait:str,context:str,metric:str,openb:float,
         handb:float,opense:float|None,handse:float|None,
         doi:str)->dict:
    if study not in STUDIES or (opense is None)!=(handse is None):
        raise ValueError("invalid programme or partial uncertainty")
    if opense is not None and (opense<=0 or handse<=0):
        raise ValueError("nonpositive source selection gradient SE")
    d=openb-handb
    e={
        "programme":study,"trait":trait,"fixed_background":context,
        "source_link_metric":metric,"source_doi":doi,
        "beta_open":openb,"beta_hand":handb,
        "delta_open_minus_hand":d,
        "magnitude_delta":abs(openb)-abs(handb),
        "point_sign_change":openb*handb<0,
        "source_SE_open":opense,"source_SE_hand":handse,
        "source_signs_both_nominally_supported":(
            openb*handb<0 and abs(openb)>1.96*opense
            and abs(handb)>1.96*handse
            if opense is not None else None),
        "unknown_source_cell_covariance":True,
        "independent_experiment_unit":study,
    }
    if opense is not None:
        e["delta_standard_error_upper"]=opense+handse
        e["conditional_worst_covariance_p_upper"]=math.erfc(
            abs(d)/(math.sqrt(2)*(opense+handse)))
    else:
        e["delta_standard_error_upper"]=None
        e["conditional_worst_covariance_p_upper"]=None
    return e


def preexisting_frozen_edges()->list[dict]:
    four=four_build(
        read_v27(V27_SOURCE),
        json.loads(V27_READOUT.read_text(encoding="utf-8")),
        read_gym(GYM_SOURCE),
    )
    if four["totals"]["n_within_axis_fixed_context_pollination_edges"]!=24:
        raise ValueError("previous frozen 24-edge primary source audit drift")
    all_edges=[]
    for x in four["contrasts"]:
        name=x["programme_id"].split("_")[0]
        if name not in STUDIES:
            raise ValueError("unknown original biological programme")
        if x["metric_family"].startswith("POISSON"):
            metric="POISSON_LOG_LINK_FEMALE_SEEDS"
        else:
            metric="STANDARDIZED_LINEAR_FEMALE_FITNESS"
        e=edge(name,x["canonical_axis"],x["fixed_context"],metric,
               x["beta_open"],x["beta_supplemented"],
               x["se_open"],x["se_supplemented"],x["source_doi"])
        if e["point_sign_change"]!=x["point_selection_sign_switch"]:
            raise ValueError("frozen four-programme sign readout changed")
        all_edges.append(e)
    return all_edges


def new_lobelia_cardinalis(rows:list[dict[str,str]])->list[dict]:
    if len(rows)!=12:
        raise ValueError("full original Lobelia cardinalis 6x2 table missing")
    mapped=defaultdict(dict)
    for r in rows:
        k=r["trait"]
        c=r["pollination_context"]
        if c not in ("NATURAL","HAND_SUPPLEMENTED") or c in mapped[k]:
            raise ValueError("invalid/duplicated Lobelia source arm")
        if r["source_table"]!="Table_2" or r["doi"]!=DATA_DOIS["Lobelia_cardinalis"]:
            raise ValueError("original Lobelia source identity drift")
        mapped[k][c]=r
    if len(mapped)!=6 or any(set(v)!={"NATURAL","HAND_SUPPLEMENTED"} for v in mapped.values()):
        raise ValueError("incomplete original Lobelia source paired traits")
    return [edge("Lobelia_cardinalis",k,"NATURAL_VS_HAND",
                 "STANDARDIZED_LINEAR_RELATIVE_FEMALE_SEED_NUMBER",
                 number(v["NATURAL"]["beta"]),number(v["HAND_SUPPLEMENTED"]["beta"]),
                 number(v["NATURAL"]["se"]),number(v["HAND_SUPPLEMENTED"]["se"]),
                 DATA_DOIS["Lobelia_cardinalis"])
            for k,v in sorted(mapped.items())]


def new_trifolium(rows:list[dict[str,str]])->list[dict]:
    matched=[r for r in rows if r["axis"]=="flowering_time_HCNplus"]
    if len(rows)!=4 or len(matched)!=2:
        raise ValueError("Trifolium source numeric/HNC+ study scope drift")
    arms={r["context"]:r for r in matched}
    if set(arms)!={"OPEN_POLLINATION","SUPPLEMENTAL_POLLINATION"}:
        raise ValueError("original Trifolium pollen arm incomplete")
    # No standard errors appear in this source. Never manufacture them.
    return [edge("Trifolium","HCNpositive_flowering_time","HCN_POSITIVE_ONLY",
                 "STANDARDIZED_LINEAR_SOURCE_BETA_NO_SE",
                 number(arms["OPEN_POLLINATION"]["beta"]),
                 number(arms["SUPPLEMENTAL_POLLINATION"]["beta"]),
                 None,None,DATA_DOIS["Trifolium"])]


def new_aconitum(rows:list[dict[str,str]])->list[dict]:
    if len(rows)!=8:return _raise("original Aconitum 4x2 source incomplete")
    d=defaultdict(dict)
    for r in rows:
        t,c=r["trait"],r["context"]
        if t not in ACON_TRAITS or c not in ("OPEN_POLLINATED","HAND_SUPPLEMENTED") or c in d[t]:
            raise ValueError("unregistered Aconitum trait or duplicate treatment")
        if r["doi"]!=DATA_DOIS["Aconitum"] or r["source_table"]!="Table_3":
            raise ValueError("Aconitum source DOI and table identity changed")
        d[t][c]=r
    if set(d)!=ACON_TRAITS or any(len(v)!=2 for v in d.values()):
        raise ValueError("Aconitum treatment source axes incomplete")
    edges=[]
    for t,v in sorted(d.items()):
        a,b=v["OPEN_POLLINATED"],v["HAND_SUPPLEMENTED"]
        if a["source_interaction_p"]!=b["source_interaction_p"]:
            raise ValueError("Aconitum author's direct trait-by-treatment test drift")
        edges.append(edge("Aconitum",t,"ONE_FIXED_SOURCE_FIELD_YEAR",
                          "STANDARDIZED_LINEAR_RELATIVE_LIFETIME_FEMALE_FITNESS",
                          number(a["beta"]),number(b["beta"]),
                          number(a["se"]),number(b["se"]),DATA_DOIS["Aconitum"]))
    return edges


def _raise(msg):
    raise ValueError(msg)


def new_lobelia_siphilitica(rows:list[dict[str,str]],fitness:str,
                           open_arm:str="AMBIENT_OPEN")->list[dict]:
    if len(rows)!=36:
        raise ValueError("full Brown and Caruso 6x3x2 table incomplete")
    d=defaultdict(dict)
    for r in rows:
        k=(r["fitness_endpoint"],r["trait"])
        c=r["context"]
        if (r["fitness_endpoint"] not in BROWN_FITNESS
            or r["trait"] not in BROWN_TRAITS
            or c not in REGIMES or c in d[k]):
            raise ValueError("unregistered/duplicated Lobelia siphilitica cell")
        if (r["doi"]!=DATA_DOIS["Lobelia_siphilitica"]
            or r["source_table"]!="Table_2"):
            raise ValueError("Lobelia siphilitica source identity drift")
        number(r["beta"]);number(r["se"])
        d[k][c]=r
    if len(d)!=12 or any(set(v)!=set(REGIMES) for v in d.values()):
        raise ValueError("Brown and Caruso 2023 complete 36-cell table required")
    if fitness not in BROWN_FITNESS or open_arm not in REGIMES[1:]:
        raise ValueError("study source outcome/regime unregistered")
    result=[]
    for trait in sorted(BROWN_TRAITS):
        a,b=d[(fitness,trait)][open_arm],d[(fitness,trait)]["HAND_SUPPLEMENTED"]
        result.append(edge("Lobelia_siphilitica",trait,fitness+"_"+open_arm,
                           "STANDARDIZED_LINEAR_"+fitness.upper(),
                           number(a["beta"]),number(b["beta"]),
                           number(a["se"]),number(b["se"]),
                           DATA_DOIS["Lobelia_siphilitica"]))
    return result


def sign_test(successes:int, trials:int)->dict:
    if trials<1 or not 0<=successes<=trials:
        raise ValueError("invalid experiment count")
    high=max(successes,trials-successes)
    upper=sum(math.comb(trials,k) for k in range(high,trials+1))/(2**trials)
    return {"n_programmes":trials,"n_positive_strength_change":successes,
            "point_tendency_positive_fraction":successes/trials,
            "exploratory_one_sided_p_at_or_above_majority":upper,
            "exploratory_two_sided_exact_sign_p":min(1.,2*upper),
            "null":"exchangeable independent study signs not random world prevalence"}


def group_summary(edges:list[dict])->dict:
    groups=defaultdict(list)
    for e in edges:
        groups[e["programme"]].append(e)
    if set(groups)!=set(STUDIES):
        raise ValueError("the eight independent source programmes not complete")
    summaries={}
    for study in sorted(groups):
        x=groups[study]
        distinct={v["trait"] for v in x}
        signed=sum(v["delta_open_minus_hand"] for v in x)/len(x)
        magnitude=sum(v["magnitude_delta"] for v in x)/len(x)
        summaries[study]={
            "n_matched_axis_context_pairs":len(x),
            "n_distinct_trait_axes":len(distinct),
            "source_doi":DATA_DOIS[study],
            "metric_families":sorted({v["source_link_metric"] for v in x}),
            "study_mean_delta_signed_source_beta":signed,
            "study_mean_absolute_gradient_attenuation":magnitude,
            "study_mean_attenuation_sign":"POSITIVE" if magnitude>0 else "NEGATIVE" if magnitude<0 else "ZERO",
            "point_sign_crossings":sum(v["point_sign_change"] for v in x),
            "opposite_cell_signs_individually_nominally_supported":sum(
                v["source_signs_both_nominally_supported"] is True for v in x),
            "n_pairs_without_standard_errors":sum(v["source_SE_open"] is None for v in x),
            "not_population_prevalence":True,
        }
    return summaries


def flower_number_partial_meta(edges:list[dict])->dict:
    requested={
        "Dactylorhiza":"Dactylorhiza_000649_flower_number",
        "Primula":"Primula_000651_flower_number",
        "Gymnadenia":"Gymnadenia_000030_number_of_flowers",
        "Lobelia_cardinalis":"flower_number",
        "Aconitum":"flower_number",
    }
    result={}
    for study,axis in requested.items():
        found=[x for x in edges if x["programme"]==study and x["trait"]==axis]
        if len(found)!=(2 if study=="Gymnadenia" else 1):
            raise ValueError("one matched floriferous display trait missing "+study)
        delta=sum(x["delta_open_minus_hand"] for x in found)/len(found)
        # Sum bound for the weighted average across treatment arms, with
        # completely unknown covariance within original biological study.
        upper=sum(x["delta_standard_error_upper"] for x in found)/len(found)
        if upper<=0:
            raise ValueError("source SE unavailable for common floral count")
        result[study]={
            "study_delta_open_minus_hand":delta,
            "within_study_uncertainty_upper":upper,
            "n_backgrounds_in_source":len(found),
            "axis":axis,
        }
    weights={name:1/(x["within_study_uncertainty_upper"]**2)
             for name,x in result.items()}
    total=sum(weights.values())
    value=sum(result[k]["study_delta_open_minus_hand"]*w
              for k,w in weights.items())/total
    # studies independent, but never assume within-source beta covariance=0.
    se=1/math.sqrt(total)
    z=value/se
    p=math.erfc(abs(z)/math.sqrt(2))
    critical=NormalDist().inv_cdf(.975)
    ci=[value-critical*se,value+critical*se]
    return {
        "analysis":"conditional_fixed_effect_floral_number_selection_response_pilot",
        "n_independent_programmes":len(result),
        "n_study_source_trait_coordinates":len(result),
        "study_estimates":result,
        "source_conservative_SE_weight_fraction":{
            k:weights[k]/total for k in sorted(result)},
        "source_selection_normal_approximation_assumed":True,
        "study_independence_assumed":True,
        "source_cell_covariance_not_assumed_zero":True,
        "common_fitness_estimand":"relative_female_reproductive_performance_standardized_flower_number",
        "within_study_canonical_trait":"lifetime_flowers_per_plant_or_number_of_flowers",
        "weighted_mean_source_beta_delta":value,
        "covariance_worst_case_SE_upper":se,
        "conditional_normal_95pct_interval":ci,
        "conditional_normal_p_upper":p,
        "source_precision_and_study_heterogeneity_not_complete_population_uncertainty":True,
        "random_effects_population_mean_identified":False,
        "caveats":[
            "four older studies potentially overlap pre2018 floral-selection review",
            "prospectively_unselected_taxa_study_denominator_not_available",
            "source_specific_fitness_standardization_and_traits_not_exactly_identical",
            "two Gymnadenia herbivory backgrounds are correlated within programme",
            "unknown_original_covariance_allows_SE_up_to_sum_of_arm_SEs",
            "conditional_fixed_effect_mean_not_population_random_effects",
            "no_general_ecological_phenotype_optimum_or_L_measured",
        ],
    }


def build()->dict:
    edges=preexisting_frozen_edges()
    lcard=new_lobelia_cardinalis(load(LOB))
    trif=new_trifolium(load(TRIF))
    acon=new_aconitum(load(ACON))
    brownall=load(BROWN)
    brown=new_lobelia_siphilitica(brownall,"relative_seeds_per_plant")
    brownfruit=new_lobelia_siphilitica(brownall,"relative_fruits_per_plant")
    brownreduced=new_lobelia_siphilitica(
        brownall,"relative_seeds_per_plant","REDUCED_OPEN")
    edges.extend(lcard+trif+acon+brown)
    if len(edges)!=41 or len({x["programme"] for x in edges})!=MAIN_STUDY_N:
        raise ValueError("all eight programmes and 41 eligible edges required")
    if any(e["source_doi"]!=DATA_DOIS[e["programme"]] for e in edges):
        raise ValueError("source DOI programme cross-walk failed")
    counts={name:sum(x["programme"]==name for x in edges) for name in STUDIES}
    expected={"Aconitum":4,"Dactylorhiza":5,"Gymnadenia":10,
              "Lobelia_cardinalis":6,"Lobelia_siphilitica":6,
              "Primula":4,"Trifolium":1,"Trillium":5}
    if counts!=expected:
        raise ValueError("pair counts are non-independent or incomplete")
    summaries=group_summary(edges)
    positives=sum(v["study_mean_absolute_gradient_attenuation"]>0
                  for v in summaries.values())
    point_flips=sum(e["point_sign_change"] for e in edges)
    both_supported=sum(e["source_signs_both_nominally_supported"] is True
                       for e in edges)
    se_edges=[e for e in edges if e["source_SE_open"] is not None]
    if len(se_edges)!=40:
        raise ValueError("all source SEs except Trifolium required")
    z=NormalDist().inv_cdf(1-.05/(2*len(se_edges)))
    family_supported=[
        f'{e["programme"]}::{e["trait"]}::{e["fixed_background"]}'
        for e in se_edges
        if abs(e["delta_open_minus_hand"])>z*e["delta_standard_error_upper"]
    ]
    return {
        "analysis":"sch_eight_programme_experimental_pollen_selection_context_meta_pilot_v1",
        "source_status":"SECONDARY_SELECTED_STUDY_EXPERIMENTAL_SLOPE_COMPARISON",
        "main_metric":"within_source_study_mean_abs_beta_open_minus_abs_beta_hand",
        "independent_study_units":MAIN_STUDY_N,
        "n_matched_trait_context_edges":len(edges),
        "n_matched_edges_with_original_SEs":len(se_edges),
        "n_distinct_original_DOIs_with_verified_primary_metadata":8,
        "Trifolium_primary_DOI_correspondence_confirmed_by_source_document_and_publisher":True,
        "Trifolium_original_primary_DOI_not_present_in_frozen_numeric_csv":True,
        "n_point_sign_crossings":point_flips,
        "n_both_arm_signs_nominally_supported":both_supported,
        "n_source_evaluable_for_both_arm_signs":len(se_edges),
        "forty_edge_conditional_bonferroni_critical_z":z,
        "forty_edge_covariance_worst_case_change_certificates":family_supported,
        "study_strength_directions":sign_test(positives,MAIN_STUDY_N),
        "study_strength_sensitivity_excluding_SE_missing_Trifolium":sign_test(
            positives,MAIN_STUDY_N-1),
        "programme_summaries":summaries,
        "common_flower_number_conditional_fixed_effect":flower_number_partial_meta(edges),
        "Brown_2023_seed_vs_fruit_study_sensitivity":{
            "seed_absolute_gradient_attenuation":summaries["Lobelia_siphilitica"][
                "study_mean_absolute_gradient_attenuation"],
            "fruit_absolute_gradient_attenuation":sum(x["magnitude_delta"] for x in brownfruit)/len(brownfruit),
            "reduced_pollination_absolute_gradient_attenuation":sum(
                x["magnitude_delta"] for x in brownreduced)/len(brownreduced),
            "all_same_independent_biological_programme":True,
            "n_new_source_table2_records":len(brownall),
            "n_seed_6_eligible_trait_axes":len(brown),
            "n_fruit_6_sensitivity_axes":len(brownfruit),
        },
        "matched_source_edges":edges,
        "generalization_blockers":[
            "purposively_collected_study_family_not_a_systematic_fresh_2019_2026_meta_search",
            "earlier_caruso_meta_2018_original_workbook_Dryad_401_403_not_recovered",
            "source_programmes_are_independent_biological_units_not_41_edge_replicates",
            "Trifolium_HCN_positive_only_genotype_and_no_source_beta_SE",
            "Trillium_conditional_Poisson_coefficients_not_poolable_with_linear_slopes",
            "Primula_2017_pollen_arms_have_different_style_morph_composition",
            "Gymnadenia_two_herbivory_backgrounds_correlated_within_source",
            "Lobelia_siphilitica_2023_two_fitness_components_and_three_regimes_same_study",
            "beta_and_SE_source_original_printed_rounding_and_covariance_limits",
            "no_meta_analytic_natural_prevalence_or_random_effects_generalization",
            "no_new_field_trait_randomization_or_pure_function_optima_or_SCH_L",
        ],
        "status":"ORIGINAL_SOURCE_MATCHED_META_PILOT_DONE_GENERAL_POPULATION_META_NOT_READY",
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    result=build()
    text=json.dumps(result,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(text,encoding="utf-8")
    else:
        print(text,end="")


if __name__=="__main__":
    main()

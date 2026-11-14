"""Reanalyse the ORIGINAL unduplicated plant functional-selection meta database.

Original publication: Caruso, Maherali & Martin 2020, 10.1086/706199.
Original data: Dryad 10.5061/dryad.sn02v6x0q, Zenodo record 5000217.
Analysis is new, source is authors' previously compiled published gradients.

Scientific question: Are within-study experimental *sign changes* in selection
more common under manipulations of biotic than abiotic environments?
Each datum is a matched trait/year/population/sex/fitness source *pair*;
statistical replication is by PAPER ID, not 572 coefficients or pairs.

The sign of treatment code 1 versus 2 is not an ecological exposure axis.
DO NOT interpret beta2-beta1 as "more pollinators", "higher water", etc.
Agent families are assigned using ORIGINAL source descriptor labels before
inspecting numerical beta signs; ambiguous multi-driver designs are excluded
from the biotic-versus-abiotic estimand, not silently forced into a class.

Because beta1/beta2 covariance is unreported, the maximum contrast SE is
SE1+SE2 (Cauchy-Schwarz). Conditional normal-Wald Bonferroni certificates
do not assume covariance=0, but source normal SE validity is needed.
Point sign changes, two separately nonzero opposite cell slopes, and changes
in gradients are three DIFFERENT objects.

A paper-label permutation compares per-paper sign-flip rates ONLY when
original publications are exclusive to one classified agent family.
If a publication contributes multiple classes, those data stay descriptive
but are not incorrectly treated as independent papers in that comparison.
This is an exploratory, noncausal selected-literature meta reanalysis.
"""
from __future__ import annotations

import argparse
import collections
import csv
from decimal import Decimal, InvalidOperation
import json
import math
import random
import statistics
from pathlib import Path
from statistics import NormalDist

from scripts.audit_sch_plant_functional_meta_grain import (
    ID_FIELDS,SOURCE_MASTER,SOURCE_OBS,SOURCE_DUP,
    source_rows,number,strkey,
)

DATA_DOI="10.5061/dryad.sn02v6x0q"
PAPER_DOI="10.1086/706199"
MIN_PAPERS_COMPARISON=3
N_PERM=9999
RANDOM_SEED=20261114
CRITICAL_ALPHA=0.05
EXPERIMENTAL_N=572

# Exact original study-source strings, not invented natural categories.
BIOTIC={
    "Pollinators",
    "Herb",
    "Predation",
    "Presence of competitor",
    "Presence of herbivores",
    "browsing/herbivory",
    "insect herbivory",
    "Species diversity",
    "Pollinators and herbivores",
    "Clipping, Seed fly, and Lepidopteran",
}
ABIOTIC={
    "Erosion",
    "Light",
    "Nutrient availability",
    "Percentage Sunlight",
    "Soil moisture",
    "Temperature",
    "Watering regime",
    "light conditions",
    "mois",
    "environmental stress",
    "Temp + Mois",
    "water stress X nutrient limitation",
}
MIXED_OR_UNKNOWN={
    "Dens",
    "Density",
    "CO2 and competition",
    "Competition, Shading, and Soil depth",
    "Pollinators and vegetation height",
    "Resources and Pollinators",
    "Soil moisture and interspecific density",
}
ORIGINAL_AGENT_NAMES=BIOTIC|ABIOTIC|MIXED_OR_UNKNOWN
TRAIT_CODES={"PH":"PHENOLOGY","PY":"PHYSIOLOGY","S":"PLANT_SIZE",
             "MO":"LEAF_MORPHOLOGY","CH":"LEAF_CHEMISTRY"}
CONTEXT_CODES={"A":"INDOOR_CONTROLLED","B":"OUTDOOR_SEMICONTROLLED",
               "C":"IN_SITU_NATURAL_POPULATION"}


def original_agent_group(label:str)->str:
    if label in BIOTIC:return "BIOTIC"
    if label in ABIOTIC:return "ABIOTIC"
    if label in MIXED_OR_UNKNOWN:return "UNRESOLVED_OR_MIXED"
    raise ValueError("unregistered original agent.label: "+label)


def stored_decimal_half_unit(value)->float:
    """Half last visible source-archive decimal unit, a SENSITIVITY only.

    This is not original study sampling error. Numeric Excel cells do not
    preserve intentional unprinted trailing zeroes; therefore a passing
    result is only robust to the stored decimal representation, NOT
    necessarily all source-published rounding conventions.
    """
    try:
        v=Decimal(str(value).strip())
        if not v.is_finite():
            raise ValueError("nonfinite original stored numeric precision")
        return float(Decimal("0.5")*(Decimal(10)**v.as_tuple().exponent))
    except (InvalidOperation,TypeError) as exc:
        raise ValueError("invalid original stored numeric precision") from exc


def source_pairs(master:list[dict])->tuple[list[dict],dict]:
    if len(master)!=EXPERIMENTAL_N:
        raise ValueError("must use exactly the unduplicated original master records")
    row_ids=[strkey(r.get("row.id")) for r in master]
    if len(set(row_ids))!=EXPERIMENTAL_N or any(not x for x in row_ids):
        raise ValueError("original unduplicated metadata row IDs not unique")
    original_agents={strkey(x["agent.selection.defined"]) for x in master}
    if original_agents!=ORIGINAL_AGENT_NAMES:
        raise ValueError("original agent taxonomy changed; class must be re-adjudicated")
    groups=collections.defaultdict(list)
    for row in master:
        key=tuple(strkey(row.get(field)) for field in ID_FIELDS)
        if any(not x for x in key):
            raise ValueError("original study matching fields missing")
        groups[key].append(row)
    rejected=collections.Counter()
    pair_rows=[]
    considered_exact=0
    for key,rows in sorted(groups.items()):
        if len(rows)!=2:
            rejected["not_exactly_two_study_rows"]+=1
            continue
        codes=[strkey(r["generic.treatment"]) for r in rows]
        if len(set(codes))!=2:
            rejected["duplicate_treatment_code"]+=1
            continue
        considered_exact+=1
        r1,r2=sorted(rows,key=lambda r:strkey(r["generic.treatment"]))
        # Each original paired selection comparison must have an identical
        # phenotype and biological setting except the declared treatment.
        consistency=(
            "authors","pub.year","journal","species","trait.name",
            "trait.class","fitness.measure.defined","fitness.component",
            "agent.selection.defined","experimental.context",
        )
        if any(strkey(r1[x])!=strkey(r2[x]) for x in consistency):
            rejected["mismatched_original_source_or_fitness_context"]+=1
            continue
        if strkey(r1["treatment.defined"])==strkey(r2["treatment.defined"]):
            rejected["treatment_labels_same_in_source"]+=1
            continue
        agent=strkey(r1["agent.selection.defined"])
        src_cat=original_agent_group(agent)
        trait_code=strkey(r1["trait.class"])
        context_code=strkey(r1["experimental.context"])
        if trait_code not in TRAIT_CODES or context_code not in CONTEXT_CODES:
            raise ValueError("original phenotype/context code outside documented dictionary")
        b1,b2=[number(r["grad.linear.value"]) for r in (r1,r2)]
        s1,s2=[number(r["grad.linear.se"]) for r in (r1,r2)]
        if any(v is None for v in (b1,b2,s1,s2)):
            rejected["missing_original_linear_gradient_or_se"]+=1
            continue
        if s1<=0 or s2<=0:
            raise ValueError("original source selection gradient SE invalid")
        if strkey(r1["Paper ID"])!=strkey(r2["Paper ID"]):
            raise ValueError("original paper mismatch")
        d=b2-b1
        worst_se=s1+s2
        beta_round_half=sum(stored_decimal_half_unit(
            r["grad.linear.value"]) for r in (r1,r2))
        se_round_half=sum(stored_decimal_half_unit(
            r["grad.linear.se"]) for r in (r1,r2))
        p_upper=math.erfc(abs(d)/(math.sqrt(2)*worst_se))
        pair_rows.append({
            "paper_id":strkey(r1["Paper ID"]),
            "authors":strkey(r1["authors"]),
            "published_year":strkey(r1["pub.year"]),
            "species":strkey(r1["species"]),
            "trait":strkey(r1["trait.name"]),
            "trait_class":TRAIT_CODES[trait_code],
            "fitness_component":strkey(r1["fitness.component"]),
            "fitness_measure":strkey(r1["fitness.measure.defined"]),
            "source_context":CONTEXT_CODES[context_code],
            "source_agent":agent,
            "agent_category":src_cat,
            "original_row_ids":[strkey(r1["row.id"]),strkey(r2["row.id"])],
            "source_treatment_codes":codes if codes==sorted(codes) else sorted(codes),
            "original_treatment_names":[strkey(r1["treatment.defined"]),
                                         strkey(r2["treatment.defined"])],
            "beta1":b1,"beta2":b2,
            "se1":s1,"se2":s2,
            "delta_beta_code2_minus_code1":d,
            "absolute_delta":abs(d),
            "conservative_se_upper":worst_se,
            "two_sided_normal_p_upper":p_upper,
            "source_stored_decimal_rounding_min_absolute_delta":
                max(0,abs(d)-beta_round_half),
            "source_stored_decimal_rounding_max_worst_case_se":
                worst_se+se_round_half,
            "point_sign_flip":b1*b2<0,
            "source_both_arm_opposite_signs_nominal95":(
                b1*b2<0 and abs(b1)>1.96*s1 and abs(b2)>1.96*s2),
            "noncausal_observational_selection_slopes_inside_experimental_context":True,
        })
    if considered_exact!=172:
        raise ValueError("previous source grain expected exactly 172 candidate pairs")
    if len({z for p in pair_rows for z in p["original_row_ids"]})!=len(pair_rows)*2:
        raise ValueError("one original source beta row reused in two pseudo-pairs")
    return pair_rows,{
        "n_all_original_rows":len(master),
        "n_candidate_two_row_two_treatment_keys":considered_exact,
        "rejected_pair_counts":dict(sorted(rejected.items())),
        "n_eligible_fully_matched_gradient_and_se_pairs":len(pair_rows),
        "n_original_source_rows_used_in_paired_analysis":2*len(pair_rows),
    }


def _average(xs:list[float])->float:
    if not xs:raise ValueError("empty cross-study outcome")
    return math.fsum(xs)/len(xs)


def per_paper_summary(pairs:list[dict])->list[dict]:
    grouped=collections.defaultdict(list)
    for r in pairs:
        grouped[r["paper_id"]].append(r)
    res=[]
    for paper,rr in sorted(grouped.items()):
        cats={x["agent_category"] for x in rr}
        for cat in sorted(cats):
            sub=[x for x in rr if x["agent_category"]==cat]
            res.append({
                "paper_id":paper,
                "authors":rr[0]["authors"],
                "publication_year":rr[0]["published_year"],
                "agent_category":cat,
                "n_pairs":len(sub),
                "n_species":len({r["species"] for r in sub}),
                "n_point_sign_flips":sum(r["point_sign_flip"] for r in sub),
                "n_nominal_both_arm_supported_reversals":sum(
                    r["source_both_arm_opposite_signs_nominal95"] for r in sub),
                "fraction_point_sign_flips":_average([
                    float(r["point_sign_flip"]) for r in sub]),
                "original_paper_has_multiple_agent_categories":len(cats)>1,
            })
    return res


def _quantile(xs:list[float],q:float)->float:
    ys=sorted(xs)
    if not ys:return float("nan")
    a=q*(len(ys)-1)
    lo,hi=math.floor(a),math.ceil(a)
    return ys[lo]*(hi-a)+ys[hi]*(a-lo) if lo!=hi else ys[lo]


def study_label_exploration(
    papers:list[dict],permutations:int=N_PERM,seed:int=RANDOM_SEED
)->dict:
    # source papers with both category axes are kept outside this test
    all_groups=collections.defaultdict(set)
    for r in papers:
        all_groups[r["paper_id"]].add(r["agent_category"])
    pure=[r for r in papers if len(all_groups[r["paper_id"]])==1
          and r["agent_category"] in {"BIOTIC","ABIOTIC"}]
    grouped={"BIOTIC":[r for r in pure if r["agent_category"]=="BIOTIC"],
             "ABIOTIC":[r for r in pure if r["agent_category"]=="ABIOTIC"]}
    a,b=[grouped[x] for x in ("BIOTIC","ABIOTIC")]
    if min(len(a),len(b))<MIN_PAPERS_COMPARISON:
        return {
            "status":"NOT_MODELABLE_UNDER_INDEPENDENT_PAPER_LABEL_PERMUTATION",
            "independent_biotic_papers":len(a),
            "independent_abiotic_papers":len(b),
            "n_permutations_run":0,
        }
    observed=_average([x["fraction_point_sign_flips"] for x in a])-_average([
        x["fraction_point_sign_flips"] for x in b])
    rates=[r["fraction_point_sign_flips"] for r in a+b]
    n_a=len(a)
    rng=random.Random(seed)
    extreme=0
    for _ in range(permutations):
        shuffled=rates.copy()
        rng.shuffle(shuffled)
        delta=_average(shuffled[:n_a])-_average(shuffled[n_a:])
        if abs(delta)>=abs(observed)-1e-13:extreme+=1
    p=(extreme+1)/(permutations+1)
    # Descriptive paper bootstrap under original study selection, not a
    # population-representative confidence interval.
    boot=[]
    for _ in range(3000):
        arrA=[rng.choice(a)["fraction_point_sign_flips"] for _ in a]
        arrB=[rng.choice(b)["fraction_point_sign_flips"] for _ in b]
        boot.append(_average(arrA)-_average(arrB))
    return {
        "status":"PAPER_LEVEL_EXPLORATORY_ASSOCIATION_ONLY",
        "contrast":"paper_equal_weight_biotic_minus_abiotic_point_sign_flip_fraction",
        "observed_difference":observed,
        "n_permutations_run":permutations,
        "two_sided_p_given_paper_label_exchangeability":p,
        "paper_bootstrap_percentile_interval_descriptive":[
            _quantile(boot,.025),_quantile(boot,.975)],
        "n_included_pure_category_independent_papers":len(pure),
        "independent_biotic_papers":len(a),
        "independent_abiotic_papers":len(b),
        "excluded_mixed_or_multiple_agent_category_papers":len(
            {r["paper_id"] for r in papers}- {r["paper_id"] for r in pure}),
        "assumes_paper_category_label_exchangeability_not_random_assignment":True,
    }


def execute(master:list[dict],*,permutations:int=N_PERM)->dict:
    pairs,flow=source_pairs(master)
    if not pairs:
        raise ValueError("original meta contains no eligible source pairs")
    N=len(pairs)
    z=NormalDist().inv_cdf(1-CRITICAL_ALPHA/(2*N))
    for r in pairs:
        r["full_family_source_covariance_worst_case_normal_05"]=(
            abs(r["delta_beta_code2_minus_code1"])>
            z*r["conservative_se_upper"]
        )
        r["bonferroni_adjusted_p_upper"]=min(1,N*r["two_sided_normal_p_upper"])
        r["certificate_robust_to_stored_source_decimal_rounding"]=(
            r["source_stored_decimal_rounding_min_absolute_delta"]>
            z*r["source_stored_decimal_rounding_max_worst_case_se"])
    papers=per_paper_summary(pairs)
    cats=sorted({r["agent_category"] for r in pairs})
    bycat={}
    for cat in cats:
        group=[r for r in pairs if r["agent_category"]==cat]
        paper=[r for r in papers if r["agent_category"]==cat]
        bycat[cat]={
            "n_matched_trait_context_pairs":len(group),
            "n_independent_original_papers":len(paper),
            "n_original_species":len({r["species"] for r in group}),
            "n_point_sign_flips":sum(r["point_sign_flip"] for r in group),
            "n_cellwise_two_nonzero_opposite_directions":sum(
                r["source_both_arm_opposite_signs_nominal95"] for r in group),
            "n_familywise_covariance_worstcase_change_certificates":sum(
                r["full_family_source_covariance_worst_case_normal_05"] for r in group),
            "pair_weighted_flip_fraction_descriptive":_average([
                float(r["point_sign_flip"]) for r in group]),
            "paper_equal_weight_flip_fraction_descriptive":_average([
                r["fraction_point_sign_flips"] for r in paper]),
            "n_original_study_in_situ_context_pairs":sum(
                r["source_context"]=="IN_SITU_NATURAL_POPULATION" for r in group),
        }
    trait_bycat={}
    for category in cats:
        trait_bycat[category]={}
        for t in sorted({r["trait_class"] for r in pairs}):
            x=[r for r in pairs if r["agent_category"]==category and r["trait_class"]==t]
            if x:
                trait_bycat[category][t]={
                    "n_pairs":len(x),"n_papers":len({r["paper_id"] for r in x}),
                    "n_point_sign_flips":sum(r["point_sign_flip"] for r in x),
                    "n_source_nominal_both_signs":sum(
                        r["source_both_arm_opposite_signs_nominal95"] for r in x),
                }
    bycontext={}
    for label in CONTEXT_CATEGORIES:
        x=[r for r in pairs if r["source_context"]==label]
        bycontext[label]={
            "n_pairs":len(x),
            "n_papers":len({r["paper_id"] for r in x}),
            "n_point_sign_flips":sum(r["point_sign_flip"] for r in x),
        }
    comparison=study_label_exploration(papers,permutations=permutations)
    certificates=[{
        "paper_id":r["paper_id"],"authors":r["authors"],
        "published_year":r["published_year"],
        "species":r["species"],"trait":r["trait"],
        "trait_class":r["trait_class"],"fitness_measure":r["fitness_measure"],
        "fitness_component":r["fitness_component"],
        "source_agent":r["source_agent"],
        "agent_category":r["agent_category"],
        "source_context":r["source_context"],
        "original_row_ids":r["original_row_ids"],
        "original_treatment_names":r["original_treatment_names"],
        "beta1":r["beta1"],"beta2":r["beta2"],
        "se1":r["se1"],"se2":r["se2"],
        "contrast_difference":r["delta_beta_code2_minus_code1"],
        "worst_covariance_se":r["conservative_se_upper"],
        "adjusted_137_family_normal_p_upper":r["bonferroni_adjusted_p_upper"],
        "point_sign_flip":r["point_sign_flip"],
        "stored_source_decimal_rounding_robust":
            r["certificate_robust_to_stored_source_decimal_rounding"],
        "two_opposite_individually_supported_slopes":
            r["source_both_arm_opposite_signs_nominal95"],
    } for r in pairs if r["full_family_source_covariance_worst_case_normal_05"]]
    return {
        "analysis":"sch_original_2020_functional_trait_master_biotic_abiotic_direction_v1",
        "source_data_doi":DATA_DOI,
        "source_paper_doi":PAPER_DOI,
        "source_unduplicated_experimental_rows":EXPERIMENTAL_N,
        "source_duplicate_1014_rows_not_used":True,
        "source_observational_815_rows_not_pooled":True,
        "input_grain":"original_pub_study_x_year_x_species_x_population_x_trait_x_sex_x_fitness",
        "source_pair_screening":flow,
        "eligible_matched_pair_total":N,
        "eligible_paper_units":len({r["paper_id"] for r in pairs}),
        "eligible_species_units":len({r["species"] for r in pairs}),
        "all_source_point_sign_flips":sum(r["point_sign_flip"] for r in pairs),
        "all_source_both_arm_nominal_opp_signs":sum(
            r["source_both_arm_opposite_signs_nominal95"] for r in pairs),
        "source_95pct_normal_bonferroni_critical_z":z,
        "all_source_familywise_contrast_certificates":sum(
            r["full_family_source_covariance_worst_case_normal_05"] for r in pairs),
        "source_reconstructed_familywise_contrast_certificate_details":certificates,
        "n_papers_with_familywise_source_contrast_certificates":len({
            x["paper_id"] for x in certificates}),
        "n_source_certificates_robust_to_stored_decimal_rounding":sum(
            x["stored_source_decimal_rounding_robust"] for x in certificates),
        "stored_decimal_rounding_is_not_original_printing_precision_proof":True,
        "all_source_observed_gradient_coefficient_precisions_as_in_archive":True,
        "eligible_agent_category_counts":bycat,
        "trait_class_by_agent_category":trait_bycat,
        "experimental_context_counts":bycontext,
        "paper_level_independence_protected_comparison":comparison,
        "per_paper_source_summary":papers,
        "source_matched_pairs":pairs,
        "inferential_limits":[
            "original_published_meta_source_not_independent_new_field_experiment",
            "source_2019_or_2020_assembled_nonrandom_literature_not_global_prevalence",
            "same_paper_axes_populations_and_trials_correlated_not_independent_n_pairs",
            "study_category_membership_not_random_or_exchangeable_by_design",
            "biotic_abiotic_study_contrast_exploratory_and_confounded_by_trait_design",
            "point_estimate_sign_flip_not_inferential_sign_reversal",
            "two_significant_opposite_cell_slopes_not_proof_of_causal_direct_function",
            "unknown_source_pair_slope_covariance_use_sum_SE_upper",
            "normal_approximation_and_source_SEs_are_assumptions",
            "source_decimal_printing_rounding_not_independently_audited",
            "source_genetic_or_phylogenetic_nonindependence_unresolved",
            "source_pub_bias_and_site_selection_not_adjusted",
            "no_pure_function_component_optima_or_SCH_loss_L",
        ],
        "status":"ORIGINAL_MASTER_META_REANALYSIS_NOT_CAUSAL_OR_NATURAL_PREVALENCE",
    }


CONTEXT_CATEGORIES=tuple(CONTEXT_CODES.values())


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--outdir",type=Path,required=True,
                   help="Directory containing MD5-verified original source Excel files")
    p.add_argument("--output",type=Path)
    p.add_argument("--permutations",type=int,default=N_PERM)
    a=p.parse_args()
    rows,_=source_rows(a.outdir/SOURCE_MASTER)
    result=execute(rows,permutations=a.permutations)
    payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(payload,encoding="utf-8")
    print("BEGIN_SCH_2020_FUNCTIONAL_META_RESULT")
    # Print a compact scientific summary; preserve all source rows in JSON file.
    print(json.dumps({k:v for k,v in result.items() if k not in {
        "source_matched_pairs","per_paper_source_summary"}},indent=2,sort_keys=True))
    print("END_SCH_2020_FUNCTIONAL_META_RESULT")


if __name__=="__main__":
    main()

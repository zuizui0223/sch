"""Source-author resolution of apparent selection-direction reversals in SCH.

Verifies the frozen 137 original published experimental gradient pairs,
then separates three DIFFERENT biological observables:
  (1) weak marginal-β point sign crossing (not source-fitted reversal),
  (2) author-fitted context moderation with direction retained,
  (3) opposite PHENOTYPIC selection gradients for two fitness components
      on the same trait and sampled 31 female Marchantia individuals.

Also resolves a total-versus-direct selection sign-change distinction:
a source author reports a significant SHADE × AREA difference for TOTAL
selection but NOT direct selection on male Marchantia plant area.

Reference primary studies:
Fuselier & McLetchie 2002, AJB 89:592–601 DOI 10.3732/ajb.89.4.592
Salgado-Luarte & Gianoli 2012, Am Nat 180:E42-E53 DOI 10.1086/666612
Trunschke et al. 2017 NPH DOI 10.1111/nph.14479
Primary Caruso 2020 source archive DOI 10.5061/dryad.sn02v6x0q.

Claims are limited to original-source reported tests and published numbers.
This script does not refit original plant rows or estimate SCH compromise L.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import csv
import json
import math

ROOT=Path(__file__).resolve().parents[1]
PAIRS=ROOT/"data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv"
CANDIDATES=ROOT/"data/SCH_2020_FIVE_STRONGEST_POINT_FLIPS_SOURCE_V1.csv"
MODERATION=ROOT/"data/SCH_2020_SOURCE_DIRECT_MODERATION_2002_2012_V1.csv"
COMPONENTS=ROOT/"data/SCH_2002_MARCHANTIA_SAME_TRAIT_TWO_FITNESS_COMPONENTS_V1.csv"
INDIRECT=ROOT/"data/SCH_2002_MARCHANTIA_TOTAL_VS_DIRECT_AREA_V1.csv"

EXPECTED_CANDIDATES={
  ("21","295","301"):("10.3732/ajb.89.4.592","Age at first split","MALE_DIRECT_SPLIT_X_SHADE","F=1.79","NO_P_MARK","NO_ORIGINAL_SIGN_SWITCH_CERTIFICATE"),
  ("33","429","430"):("10.1111/nph.14479","Flowering start","POOLED_12_SPECIES_FLOWERING_X_POLLINATION","F=6.62","0.010","POOLED_TEST_NOT_SPECIES_CERTIFICATE"),
  ("41","530","542"):("10.1086/666612","Transpiration","UNREPORTED_SPECIFIC_HERBIVORY_X_TRANSPIRATION","NOT_REPORTED","NOT_REPORTED","NO_ORIGINAL_SIGN_SWITCH_CERTIFICATE"),
  ("41","533","545"):("10.1086/666612","Internode length","UNREPORTED_SPECIFIC_HERBIVORY_X_INTERNODE","NOT_REPORTED","NOT_REPORTED","NO_ORIGINAL_SIGN_SWITCH_CERTIFICATE"),
  ("41","535","547"):("10.1086/666612","Amax","UNREPORTED_SPECIFIC_HERBIVORY_X_AMAX","NOT_REPORTED","NOT_REPORTED","NO_ORIGINAL_SIGN_SWITCH_CERTIFICATE"),
}
EXPECTED_MOD={
  ("21","294","300"):{
    "doi":"10.3732/ajb.89.4.592","trait":"Cup onset",
    "b1":(-.82,.104),"b2":(-.215,.092),
    "phenotype":("PHENOTYPIC_CUP_X_SHADE","F=13.57","<0.001"),
    "genotype":("GENOTYPIC_CUP_X_SHADE","F=4.14","<0.05"),
    "selection_endpoint":"NUMBER_OF_ASEXUAL_CUPS","source":"Table3_and_Table4",
  },
  ("41","537","549"):{
    "doi":"10.1086/666612","trait":"SLA",
    "b1":(.12,.026),"b2":(.24,.031),
    "phenotype":("HERBIVORY_X_SLA_IN_SHADE","chi2=16.10","0.008"),
    "genotype":("NOT_REPORTED","NOT_REPORTED","NOT_REPORTED"),
    "selection_endpoint":"SEEDLING_SURVIVAL","source":"Table1_and_Table3",
  },
}

def csv_read(path):
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))

def approximate(x,y):
    return abs(float(x)-y)<1e-10

def pairkey(row):
    return row["paper_id"],row["source_row_id_1"],row["source_row_id_2"]

def run(pairs,candidates,moderation,components,indirect):
    if [len(pairs),len(candidates),len(moderation),len(components),len(indirect)]!=[137,5,2,2,1]:
        raise ValueError("frozen source denominators 137/5/2/2/1 drift")
    frozen={}
    flips=[]
    for p in pairs:
        k=pairkey(p)
        if k in frozen:
            raise ValueError("duplicate original published source row IDs")
        frozen[k]=p
        vals=[float(p[field]) for field in ("beta1","se1","beta2","se2")]
        if not all(math.isfinite(x) for x in vals) or vals[1]<=0 or vals[3]<=0:
            raise ValueError("original published beta/SE invalid")
        if (vals[0]*vals[2]<0)!=(p["point_sign_flip"].lower()=="true"):
            raise ValueError("sign-flip recorded classification drift")
        if vals[0]*vals[2]<0:flips.append(p)
    if len(frozen)!=137 or len({x["paper_id"] for x in pairs})!=26 or len(flips)!=41:
        raise ValueError("published original 137-pair population or 41 crossings drift")

    zmin=lambda p:min(abs(float(p["beta1"])/float(p["se1"])),
                      abs(float(p["beta2"])/float(p["se2"])))
    weak=[x for x in flips if zmin(x)<1]
    half=[x for x in flips if 1<=zmin(x)<1.96]
    both=[x for x in flips if zmin(x)>=1.96]
    if (len(weak),len(half),len(both))!=(36,5,0):
        raise ValueError("marginal gradient strength partition drift")
    actual_five={pairkey(x) for x in half}
    if actual_five!=set(EXPECTED_CANDIDATES):
        raise ValueError("high-information source candidate IDs changed")
    candidate_seen=set()
    candidate_receipts=[]
    for source in candidates:
        k=pairkey(source)
        if k not in EXPECTED_CANDIDATES or k in candidate_seen:
            raise ValueError("unexpected or duplicate moderate-confidence point sign")
        candidate_seen.add(k)
        doi,trait,scope,stat,pval,classification=EXPECTED_CANDIDATES[k]
        if (source["primary_doi"],source["author_test_scope"],
            source["author_test_stat"],source["author_reported_p"],
            source["source_certificate_class"])!=(doi,scope,stat,pval,classification):
            raise ValueError("original author-fitted interaction provenance drift")
        gradient=frozen[k]
        if gradient["trait"]!=trait or source["source_trait_context"]=="":
            raise ValueError("source context or trait mismatch")
        candidate_receipts.append({
            "source_key":list(k),"original_trait":trait,
            "original_study":source["primary_doi"],
            "source_z_min":round(zmin(gradient),8),
            "published_beta1":float(gradient["beta1"]),
            "published_beta2":float(gradient["beta2"]),
            "author_test_scope":scope,
            "author_direct_stat":stat,
            "author_original_p":pval,
            "interpretation":classification,
            "species_level_original_author_fitted_reversal_certified":False,
        })
    if candidate_seen!=set(EXPECTED_CANDIDATES):
        raise ValueError("missing one of five original point-sign candidates")

    moderation_seen=set()
    direct_moderation=[]
    for src in moderation:
        k=pairkey(src)
        if k not in EXPECTED_MOD or k in moderation_seen:
            raise ValueError("unexpected or duplicate original direct moderation system")
        moderation_seen.add(k)
        exp=EXPECTED_MOD[k]
        if (src["primary_doi"]!=exp["doi"] or
            src["author_treatment_trait_test"]!=exp["phenotype"][0] or
            src["author_direct_stat"]!=exp["phenotype"][1] or
            src["author_direct_p"]!=exp["phenotype"][2] or
            (src["original_author_secondary_test"],src["secondary_stat"],src["secondary_p"])!=exp["genotype"] or
            src["source_location"]!=exp["source"] or
            src["selection_endpoint"]!=exp["selection_endpoint"]):
            raise ValueError("source author fitted interaction or outcome type drift")
        paired=frozen.get(k)
        if paired is None or paired["trait"]!=exp["trait"]:
            raise ValueError("source original paired gradients not identified")
        for x,y in zip(("beta1","se1"),exp["b1"]):
            if not approximate(paired[x],y):
                raise ValueError("reported primary beta1/se1 do not match 137-pair ledger")
        for x,y in zip(("beta2","se2"),exp["b2"]):
            if not approximate(paired[x],y):
                raise ValueError("reported primary beta2/se2 do not match 137-pair ledger")
        b1,b2=exp["b1"][0],exp["b2"][0]
        if b1*b2<=0:
            raise ValueError("original source moderation must retain directional sign")
        direct_moderation.append({
            "paper_id":k[0],"source_pair_ids":[k[1],k[2]],
            "source_doi":exp["doi"],"trait":exp["trait"],
            "fitness_endpoint":exp["selection_endpoint"],
            "source_beta1":b1,"source_beta2":b2,
            "author_original_direct_interaction":exp["phenotype"],
            "author_original_secondary_interaction":exp["genotype"],
            "treatment_sign_crossing":False,
            "source_context_selected":src["original_author_trait_and_context"],
        })

    original_fit={"SEXUAL":(-.915,"<0.02","Number of sexual structures","Table6"),
                  "ASEXUAL":(.496,"<0.05","Number of asexual cups","Results_Sexual_fitness_section")}
    component_seen=set()
    component_rows=[]
    for src in components:
        c=src["fitness_component"]
        if c not in original_fit or c in component_seen:
            raise ValueError("duplicate or non-original fitness-component model")
        component_seen.add(c)
        beta,p,proxy,location=original_fit[c]
        if (src["paper_id"]!="21" or src["primary_doi"]!="10.3732/ajb.89.4.592" or
            src["source_organism"]!="Marchantia inflexa" or
            src["sex"]!="FEMALE" or src["shade_percent"]!="55" or
            src["n_sex_expressing_individuals"]!="31" or
            src["same_trait_coordinate"]!="SEXUAL_REPRODUCTION_ONSET" or
            src["trait_orientation"]!="Later means higher number of days" or
            src["fitness_proxy"]!=proxy or src["author_reported_p"]!=p or
            src["source_location"]!=location or
            src["phenotypic_or_genotypic"]!="PHENOTYPIC_SELECTION" or
            src["direct_function_optimum_measured"]!="NO" or
            not approximate(src["original_standardized_beta"],beta)):
            raise ValueError("2002 same z/individuals or original outcome-gradient mismatch")
        component_rows.append({
            "fitness_component":c,
            "fitness_proxy":proxy,"beta_pheno":beta,
            "published_nominal_significance":p,"original_source_location":location,
        })
    if component_seen!=set(original_fit):
        raise ValueError("original two component outcomes not recovered")
    if not (original_fit["SEXUAL"][0]<0<original_fit["ASEXUAL"][0]):
        raise ValueError("original source opposite fitness-component gradients changed")
    # This is only an arithmetic contrast of TWO distinct fitness endpoints;
    # no shared covariance for this contrast was published.
    arithmetic_component_gradient_difference=original_fit["ASEXUAL"][0]-original_fit["SEXUAL"][0]

    row=indirect[0]
    ikey=pairkey(row)
    if ikey!=("21","296","302"):
        raise ValueError("wrong original male area context")
    original=frozen[ikey]
    if original["trait"]!="Area at day 49" or not (
        approximate(original["beta1"],.640) and approximate(original["beta2"],-.199)):
        raise ValueError("male area original direct beta not aligned")
    expected={
        "primary_doi":"10.3732/ajb.89.4.592","source_sex":"MALE",
        "environment_1":"73pct_shade","environment_2":"55pct_shade",
        "fitness_component":"ASEXUAL_CUPS","trait":"Area at day 49",
        "direct_gradient_beta1":"0.640","direct_gradient_beta2":"-0.199",
        "author_direct_area_x_shade_F":"3.31","author_direct_area_x_shade_p":"NO_P_MARK",
        "total_selection_s1":"0.631","total_selection_s2":"-0.135",
        "author_total_area_x_shade_F":"3.90","author_total_area_x_shade_p":"<0.05",
        "original_table":"Table3_and_Table4",
    }
    if any(row[k]!=v for k,v in expected.items()):
        raise ValueError("original 2002 total vs direct F/sign evidence differs")
    indirect_readout={
        "source_pair_ids":["296","302"],
        "male_area_direct_beta_73pct":.640,
        "male_area_direct_beta_55pct":-.199,
        "author_direct_area_x_shade_F":3.31,
        "original_direct_interaction_significant":False,
        "male_area_total_s_73pct":.631,
        "male_area_total_s_55pct":-.135,
        "author_total_area_x_shade_F":3.90,
        "original_total_selection_interaction_reported_p":"<0.05",
        "interpretation":"change_in_TOTAL_selection_can_occur_without_direct_slope_interaction",
        "two_individually_supported_opposite_total_slopes":False,
    }
    return {
        "analysis":"sch_2020_reverse_sign_source_mechanism_adjudication_v1",
        "published_compilation_source_doi":"10.5061/dryad.sn02v6x0q",
        "n_original_source_papers":26,
        "n_original_matched_beta_pairs":137,
        "n_source_point_sign_crossings":41,
        "n_crossings_with_min_arm_z_below_one":len(weak),
        "n_crossings_with_min_arm_z_between_one_and_1_96":len(half),
        "n_crossings_with_both_arm_z_at_least_1_96":len(both),
        "n_high_information_point_crossing_candidates_with_source_primary_qa":len(candidate_receipts),
        "n_high_information_crossings_with_author_certified_own_trait_reversal":0,
        "source_crossing_audit":sorted(candidate_receipts,key=lambda r:r["source_key"]),
        "n_original_papers_with_stronger_selection_context_without_flip_added_here":2,
        "source_verified_same_sign_treatment_modulation":sorted(direct_moderation,key=lambda r:r["paper_id"]),
        "same_female_individuals_sexual_vs_asexual_fitness_components":{
            "n_individuals":31,
            "trait":"age_at_first_sexual_expression",
            "same_trait_orientation":"higher_days_later",
            "both_source_gradients_nominally_individually_reported_nonzero_opposite":True,
            "component_gradients":component_rows,
            "arithmetic_beta_asexual_minus_beta_sexual":round(arithmetic_component_gradient_difference,6),
            "direct_fitness_component_difference_p_reported":False,
            "genotype_level_dual_component_confirmation_reported":False,
            "original_trait_z_randomized":False,
            "pure_component_optima_measured":False,
            "measured_SCH_conflict_loss_L":False,
            "status":"SOURCE_PHENOTYPIC_SAME_COORDINATE_COMPONENT_OPPOSITION_NOT_CAUSAL_L",
        },
        "same_study_male_direct_vs_total_selection":indirect_readout,
        "critical_limits":[
            "apparent_weak_arm_sign_crossings_are_not_direct_context_reversals",
            "absence_of_selected_model_specific_direct_test_not_proof_of_no_effect",
            "2017_pooled_12_species_flowering_interaction_not_Neottia_specific",
            "2002_male_split_shade_original_F_1_79_not_significant",
            "2002_Marchantia_male_area_total_selection_differs_from_direct_gradient",
            "2002_sexual_structure_count_is_proxy_not_verified_total_offspring",
            "2002_asexual_cup_count_is_proxy_not_verified_total_offspring",
            "two_fitness_components_share_same_31_female_individuals_not_two_independent_studies",
            "component_opposed_beta_coefficients_not_direct_optimum_or_joint_gradient_test",
            "2002_genotypic_sexual_selection_not_detected",
            "2012_pesticide_treatment_cannot_isolate_offtarget_effects_without_controls",
            "no_pure_function_optima_or_SCH_L_identified",
            "original_source_author_results_not_new_field_measurements",
        ],
        "status":"NEW_ORIGINAL_SOURCE_BIOLOGICAL_COMPONENT_OPPOSITION_AND_CONTEXT_MODULATION__NO_CAUSAL_L"
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--pairs",type=Path,default=PAIRS)
    p.add_argument("--candidates",type=Path,default=CANDIDATES)
    p.add_argument("--moderation",type=Path,default=MODERATION)
    p.add_argument("--components",type=Path,default=COMPONENTS)
    p.add_argument("--indirect",type=Path,default=INDIRECT)
    p.add_argument("--output",type=Path)
    a=p.parse_args()
    d=run(csv_read(a.pairs),csv_read(a.candidates),
          csv_read(a.moderation),csv_read(a.components),csv_read(a.indirect))
    result=json.dumps(d,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(result,encoding="utf-8")
    print(result)

if __name__=="__main__":
    main()

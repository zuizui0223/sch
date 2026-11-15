"""Audit matched SAME-trait fitness component estimates in the ORIGINAL 2020 meta workbook.

This is the next empirical upgrade for SCH, not a review-only example search:
scan all 572 unduplicated published experimental coefficient rows and ask
whether the same source paper/year/species/population/trait/sex/treatment
reports selection gradients on two different fitness endpoints.

Original Caruso, Maherali & Martin (2020):
    source DOI 10.5061/dryad.sn02v6x0q
    archived original 5000217, master MD5
      7f680c344c0a418a3d8742649de24d52
Here we never combine heterogeneous fitness endpoints as one effect, and
never turn source row counts into independent papers or plants.

The source 572 source rows are fetched (once) by the existing
ingest_sch_plant_functional_selection_2020_raw.py with pinned MD5.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path

from scripts.audit_sch_plant_functional_meta_grain import (
    SOURCE_MASTER,REQUIRED_SCHEMA,source_rows,strkey,number,
)
from scripts.ingest_sch_plant_functional_selection_2020_raw import (
    fetch,FILENAMES,docx_notes,
)

DOI="10.5061/dryad.sn02v6x0q"
STUDY_FIELDS=(
    "Paper ID","generic.year","generic.spp","generic.population",
    "generic.trait","generic.sex","generic.treatment",
    "agent.selection.defined","treatment.defined","experimental.context",
)
MEASURE_FIELDS=("generic.fitness.measure","fitness.measure.defined",
                "fitness.component")
FROZEN_N=572
FROZEN_PAPERS=43
FROZEN_SPECIES=46


def metadata(row):
    return {
        "row_id":strkey(row["row.id"]),
        "source_paper_id":strkey(row["Paper ID"]),
        "source_authors":strkey(row["authors"]),
        "source_species":strkey(row["species"]),
        "trait_name":strkey(row["trait.name"]),
        "trait_class":strkey(row["trait.class"]),
        "source_fitness_code":strkey(row["generic.fitness.measure"]),
        "source_fitness_measure":strkey(row["fitness.measure.defined"]),
        "source_fitness_component":strkey(row["fitness.component"]),
        "source_within_study_id":strkey(row["within.study.id"]),
        "gradient_beta":number(row["grad.linear.value"]),
        "gradient_se":number(row["grad.linear.se"]),
    }


def source_id_check(rows):
    if len(rows)!=FROZEN_N:
        raise ValueError("original source 572 experimental master changed")
    if len({strkey(r["row.id"]) for r in rows})!=FROZEN_N:
        raise ValueError("original row ids not unique")
    if len({strkey(r["Paper ID"]) for r in rows})!=FROZEN_PAPERS:
        raise ValueError("original source paper count not 43")
    if len({strkey(r["species"]) for r in rows})!=FROZEN_SPECIES:
        raise ValueError("original source species count not 46")
    for r in rows:
        if set(REQUIRED_SCHEMA)-set(r):
            raise ValueError("missing original 26 column source schema")
        if number(r["grad.linear.se"]) is not None and number(r["grad.linear.se"])<=0:
            raise ValueError("original reported gradient SE nonpositive")


def qualifies(a,b):
    """Different reported fitness *measure* AND original code required."""
    m1=(strkey(a["generic.fitness.measure"]),strkey(a["fitness.measure.defined"]))
    m2=(strkey(b["generic.fitness.measure"]),strkey(b["fitness.measure.defined"]))
    return (m1!=m2 and all(m1) and all(m2))


def audit_groups(rows,keys,strict_distinct_source_study_id=False):
    groups=defaultdict(list)
    excluded_blank=0
    for r in rows:
        key=tuple(strkey(r[k]) for k in keys)
        # Preserve blank source fields as a literal/recorded original stratum,
        # not as grounds to manufacture matches across different papers.
        if not strkey(r["Paper ID"]) or not strkey(r["generic.spp"]) or not strkey(r["generic.trait"]):
            excluded_blank+=1
            continue
        groups[key].append(r)
    multis=[]
    matched=[]
    ambiguous=[]
    overlap_count=0
    group_multis=Counter()
    for key,items in sorted(groups.items()):
        if len(items)<2:
            continue
        m=[metadata(r) for r in items]
        distinct={strkey(r["generic.fitness.measure"]) for r in items}
        if len(distinct)<2:
            continue
        group_multis[len(distinct)]+=1
        outcomes=[]
        seen=set()
        for r in items:
            outcome=(strkey(r["generic.fitness.measure"]),strkey(r["fitness.measure.defined"]))
            if outcome in seen:
                ambiguous.append({
                    "group":dict(zip(keys,key)),
                    "duplicate_source_fitness_outcome":list(outcome),
                    "status":"MULTIPLE_SOURCE_ROWS_FOR_SAME_OUTCOME_NOT_INDEPENDENT",
                })
            seen.add(outcome)
        for i,a in enumerate(items):
            for b in items[i+1:]:
                if not qualifies(a,b):
                    continue
                pair={"source_group":dict(zip(keys,key)),
                      "source_rows":[metadata(a),metadata(b)],
                      "two_original_fitness_component_codes_distinct":
                          strkey(a["fitness.component"])!=strkey(b["fitness.component"]),
                      "two_source_within_study_ids_identical":
                          strkey(a["within.study.id"])==strkey(b["within.study.id"]),
                      "original_outcome_currency_comparable":"NOT_ESTABLISHED"}
                beta_a=number(a["grad.linear.value"])
                beta_b=number(b["grad.linear.value"])
                se_a=number(a["grad.linear.se"])
                se_b=number(b["grad.linear.se"])
                pair["both_linear_betas_available"]=beta_a is not None and beta_b is not None
                pair["both_reported_betas_and_SEs_available"]=all(
                    x is not None for x in (beta_a,beta_b,se_a,se_b))
                pair["point_opposite_beta_signs"]=bool(
                    beta_a is not None and beta_b is not None and
                    beta_a*beta_b<0)
                pair["two_marginal_normal_95_opposite_betas"]=bool(
                    pair["point_opposite_beta_signs"] and
                    pair["both_reported_betas_and_SEs_available"] and
                    abs(beta_a/se_a)>1.96 and abs(beta_b/se_b)>1.96)
                pair["source_has_same_actual_original_plants"]="NOT_VERIFIED"
                pair["source_author_fitted_component_difference_test"]="NOT_RECOVERED"
                matched.append(pair)
        multis.append({
            "source_group":dict(zip(keys,key)),
            "source_rows":m,
            "n_original_rows":len(items),
            "n_distinct_source_fitness_codes":len(distinct),
            "n_distinct_fitness_measure_labels":len({
                strkey(r["fitness.measure.defined"]) for r in items}),
        })
    paper_ids={x["source_group"]["Paper ID"] for x in matched}
    species=set()
    for item in matched:
        species.add(item["source_rows"][0]["source_species"])
    return {
      "n_original_rows":len(rows),
      "n_source_strata":len(groups),
      "n_source_strata_with_two_or_more_fitness_codes":len(multis),
      "n_naive_distinct_measure_row_pairs":len(matched),
      "n_original_papers_with_multiple_outcomes_matched":len(paper_ids),
      "n_original_species_with_multiple_outcomes_matched":len(species),
      "n_source_outcome_pair_both_beta_SE_available":sum(
          x["both_reported_betas_and_SEs_available"] for x in matched),
      "n_source_outcome_pair_point_opposite_beta":sum(
          x["point_opposite_beta_signs"] for x in matched),
      "n_source_outcome_pair_both_arm_nominal_nonzero_opposite_beta":sum(
          x["two_marginal_normal_95_opposite_betas"] for x in matched),
      "n_source_outcome_pair_distinct_fitness_component_category":sum(
          x["two_original_fitness_component_codes_distinct"] for x in matched),
      "n_source_outcome_pair_exact_same_source_within_study_id":sum(
          x["two_source_within_study_ids_identical"] for x in matched),
      "source_groups_with_multiple_distinct_fitness_codes":multis[:100],
      "source_fitness_outcome_pairs":matched[:150],
      "duplicate_outcome_source_row_warnings":ambiguous[:100],
      "source_blank_crucial_groups_excluded":excluded_blank,
      "n_distinct_outcome_codes_distribution":dict(sorted(group_multis.items())),
      "original_row_pairs_are_not_independent_programmes":True,
      "cross_component_conflict_identified":False,
      "source_author_fitted_component_difference_recovered":False,
    }


def run(rows):
    source_id_check(rows)
    raw=audit_groups(rows,STUDY_FIELDS)
    strict=audit_groups(rows,STUDY_FIELDS+("within.study.id",))
    if strict["n_naive_distinct_measure_row_pairs"]>raw["n_naive_distinct_measure_row_pairs"]:
        raise ValueError("strict source strata produced more candidate row pairs")
    if (raw["n_source_strata"]!=514 or
        raw["n_source_strata_with_two_or_more_fitness_codes"]!=44 or
        raw["n_naive_distinct_measure_row_pairs"]!=75 or
        raw["n_original_papers_with_multiple_outcomes_matched"]!=3 or
        raw["n_original_species_with_multiple_outcomes_matched"]!=5 or
        raw["n_source_outcome_pair_point_opposite_beta"]!=16 or
        raw["n_source_outcome_pair_both_arm_nominal_nonzero_opposite_beta"]!=1 or
        strict["n_naive_distinct_measure_row_pairs"]!=0):
        raise ValueError("real archived original endpoint match structure changed")
    source_supported=[x for x in raw["source_fitness_outcome_pairs"]
                      if x["two_marginal_normal_95_opposite_betas"]]
    if len(source_supported)!=1:
        raise ValueError("strong opposite-stage candidate source count changed")
    signature=source_supported[0]
    if (signature["source_group"]["Paper ID"]!="4" or
        signature["source_group"]["treatment.defined"]!="Resource supplementation" or
        signature["source_rows"][0]["source_species"]!="Asclepias syriaca" or
        signature["source_rows"][0]["trait_name"]!="Length of flowering period" or
        [x["row_id"] for x in signature["source_rows"]]!=["29","35"] or
        [x["source_fitness_measure"] for x in signature["source_rows"]]
          !=["Pollinia inserted","Fruits initiated"]):
        raise ValueError("same-trait female fitness-stage original identity drift")
    a,b=signature["source_rows"]
    if not (abs(a["gradient_beta"]+.533)<1e-10 and
            abs(a["gradient_se"]-.173)<1e-10 and
            abs(b["gradient_beta"]-.362)<1e-10 and
            abs(b["gradient_se"]-.113)<1e-10):
        raise ValueError("source original female stage gradients or SE changed")
    z_bound=abs(b["gradient_beta"]-a["gradient_beta"])/(a["gradient_se"]+b["gradient_se"])
    marginal_p_upper=math.erfc(z_bound/math.sqrt(2))
    source_result={
        "primary_article_doi":"10.1007/s00442-005-0183-4",
        "source_paper_id":4,
        "species":"Asclepias syriaca",
        "trait":"Length of flowering period",
        "environment_treatment":"Resource supplementation",
        "source_archived_row_ids":[29,35],
        "source_female_stage_one":"Pollinia inserted",
        "source_female_stage_two":"Fruits initiated",
        "stage_one_beta":a["gradient_beta"],
        "stage_one_se":a["gradient_se"],
        "stage_two_beta":b["gradient_beta"],
        "stage_two_se":b["gradient_se"],
        "delta_beta_late_female_minus_early_female":round(b["gradient_beta"]-a["gradient_beta"],6),
        "conditioned_max_contrast_SE_sum":round(a["gradient_se"]+b["gradient_se"],6),
        "conditional_normal_z_lower_bound_if_comparable_SEs":round(z_bound,8),
        "conditional_single_edge_normal_two_sided_p_upper":round(marginal_p_upper,8),
        "both_marginal_betas_separately_nonzero_opposite_sign_at_1_96":True,
        "source_actual_same_plant_rows_verified":False,
        "source_fitted_direct_fitness_stage_contrast_p_recovered":False,
        "original_contrast_covariance_available":False,
        "fitness_measures_same_currency":False,
        "female_stages_not_male_versus_female":True,
        "selection_on_heritable_trait_identified":False,
        "source_conflict_optima_identified":False,
        "status":"ONE_ORIGINAL_SAME_TRAIT_TWO_FEMALE_STAGES_OPPOSITE_ASSOCIATIONS_ONLY",
    }
    # Full original source-published 3 x 3 regime × reproductive-stage matrix.
    # These are repeated outcomes from ONE paper, not nine independent papers.
    original_regimes={
      "Control":{
        "Pollinia removed":("19",-.088,.099),
        "Pollinia inserted":("25",-.062,.135),
        "Fruits initiated":("31",+.308,.097),
      },
      "Decreased pollinator access":{
        "Pollinia removed":("21",+.072,.175),
        "Pollinia inserted":("27",-.082,.233),
        "Fruits initiated":("33",+.287,.122),
      },
      "Resource supplementation":{
        "Pollinia removed":("23",-.075,.070),
        "Pollinia inserted":("29",-.533,.173),
        "Fruits initiated":("35",+.362,.113),
      },
    }
    source_matrix=[]
    for treatment,expected in original_regimes.items():
        source_group=next((g for g in raw["source_groups_with_multiple_distinct_fitness_codes"]
             if g["source_group"]["Paper ID"]=="4" and
                g["source_group"]["treatment.defined"]==treatment and
                g["source_rows"][0]["trait_name"]=="Length of flowering period"),None)
        if source_group is None or len(source_group["source_rows"])!=3:
            raise ValueError("three-treatment Asclepias female-stage source group missing")
        original={x["source_fitness_measure"]:x for x in source_group["source_rows"]}
        if set(original)!=set(expected):
            raise ValueError("original Asclepias male/female stage inventory differs")
        for measure,(row_id,beta,se) in expected.items():
            recorded=original[measure]
            if (recorded["row_id"]!=row_id or
                abs(recorded["gradient_beta"]-beta)>1e-10 or
                abs(recorded["gradient_se"]-se)>1e-10):
                raise ValueError("original resource-dependent source 2005 stage beta drift")
        early=original["Pollinia inserted"]
        late=original["Fruits initiated"]
        both_supported=(early["gradient_beta"]*late["gradient_beta"]<0
          and abs(early["gradient_beta"]/early["gradient_se"])>1.96
          and abs(late["gradient_beta"]/late["gradient_se"])>1.96)
        source_matrix.append({
          "source_original_paper_id":4,"primary_article_doi":"10.1007/s00442-005-0183-4",
          "trait":"Length of flowering period","treatment":treatment,
          "reported_source_stage_rows":original,
          "female_stage_opposite_point_signs":early["gradient_beta"]*late["gradient_beta"]<0,
          "both_female_stage_slopes_individually_nominally_supported_opposite":both_supported,
          "later_fruits_minus_earlier_insertions":round(late["gradient_beta"]-early["gradient_beta"],6),
          "original_stage_gradient_covariance":"NOT_RECOVERED",
          "original_fitted_treatment_x_female_stage_test":"NOT_RECOVERED",
        })
    if (sum(x["female_stage_opposite_point_signs"] for x in source_matrix)!=3 or
        sum(x["both_female_stage_slopes_individually_nominally_supported_opposite"]
            for x in source_matrix)!=1):
        raise ValueError("female-stage three-regime source selection pattern changed")
    return {
      "analysis":"sch_2020_real_original_experimental_multi_fitness_source_audit_v1",
      "original_published_article":"10.1086/706199",
      "original_source_data_doi":DOI,
      "n_unduplicated_original_experimental_rows":len(rows),
      "n_primary_original_papers":FROZEN_PAPERS,
      "n_original_reported_species":FROZEN_SPECIES,
      "same_paper_species_population_trait_sex_treatment_agent_context":raw,
      "source_strongest_same_trait_stage_opposition":source_result,
      "one_original_Asclepias_paper_three_context_female_stage_comparison":source_matrix,
      "n_Asclepias_flowering_duration_regimes_point_stage_opposition":3,
      "n_Asclepias_regimes_both_stage_gradient_signs_individually_supported":1,
      "also_match_original_within_study_id":strict,
      "preliminary_conclusion":"ONE_SOURCE_FEMALE_STAGE_OPPOSITION_PRESENT_NO_CAUSAL_IDENTIFICATION",
      "fitness_components_share_same_individuals":"NOT_IDENTIFIED",
      "direct_component_gradient_contrast_covariance":"NOT_RECOVERED",
      "opposite_sign_candidate_is_not_fitness_compromise_proof":True,
      "no_new_SCH_L_or_pure_function_optima":True,
      "status":"SOURCE_UNDUPLICATED_MULTI_FITNESS_GROUP_SCREENED_ONE_OPPOSITE_SIGN_CANDIDATE_NO_CAUSAL_PROMOTION",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path)
    p.add_argument("--outdir",type=Path,default=Path("artifacts/sch_2020_fitness_components"))
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    if args.source is None:
        raw,url=fetch(SOURCE_MASTER)
        original=args.outdir/SOURCE_MASTER
        original.write_bytes(raw)
        receipt={"source_download_url":url,
                 "original_source_bytes":len(raw),
                 "original_source_md5":hashlib.md5(raw).hexdigest(),
                 "original_source_sha256":hashlib.sha256(raw).hexdigest()}
    else:
        original=args.source
        raw=original.read_bytes()
        checksum=hashlib.md5(raw).hexdigest()
        if checksum!=FILENAMES[SOURCE_MASTER][0]:
            raise ValueError("user supplied original source workbook MD5 not identical")
        receipt={"source_download_url":"EXPLICIT_CHECKSUM_VERIFIED_SOURCE",
                 "original_source_bytes":len(raw),
                 "original_source_md5":checksum,
                 "original_source_sha256":hashlib.sha256(raw).hexdigest()}
    records,headers=source_rows(original)
    result=run(records)
    original_readme,readme_url=fetch("Dryad_ReadMe.docx")
    readme_path=args.outdir/"Dryad_ReadMe.docx"
    readme_path.write_bytes(original_readme)
    definitions=docx_notes(readme_path)["original_dictionary_text_first_30000_chars"]
    result["original_dictionary_term_excerpts"]=[
        line for line in definitions.splitlines()
        if any(q in line.lower() for q in ("within.study.id","fitness.component","fitness.measure"))
    ][:35]
    result["original_readme_provenance"]={
        "source_download_url":readme_url,
        "source_readme_md5":hashlib.md5(original_readme).hexdigest(),
        "source_readme_sha256":hashlib.sha256(original_readme).hexdigest(),
    }
    result["original_workbook_provenance"]=receipt
    output=(args.output or args.outdir/"original_multi_fitness_source_audit.json")
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",
                      encoding="utf-8")
    print("BEGIN_SCH_ORIGINAL_MULTI_FITNESS_AUDIT")
    print(output.read_text(encoding="utf-8"))
    print("END_SCH_ORIGINAL_MULTI_FITNESS_AUDIT")


if __name__=="__main__":
    main()

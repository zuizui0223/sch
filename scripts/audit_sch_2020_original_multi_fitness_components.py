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
    fetch,FILENAMES,
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
    return {
      "analysis":"sch_2020_real_original_experimental_multi_fitness_source_audit_v1",
      "original_published_article":"10.1086/706199",
      "original_source_data_doi":DOI,
      "n_unduplicated_original_experimental_rows":len(rows),
      "n_primary_original_papers":FROZEN_PAPERS,
      "n_original_reported_species":FROZEN_SPECIES,
      "same_paper_species_population_trait_sex_treatment_agent_context":raw,
      "also_match_original_within_study_id":strict,
      "preliminary_conclusion":"ORIGINAL_FITNESS_ENDPOINT_GRAIN_ONLY",
      "fitness_components_share_same_individuals":"NOT_IDENTIFIED",
      "direct_component_gradient_contrast_covariance":"NOT_RECOVERED",
      "opposite_sign_candidate_is_not_fitness_compromise_proof":True,
      "no_new_SCH_L_or_pure_function_optima":True,
      "status":"SOURCE_UNDUPLICATED_MULTI_FITNESS_GROUP_SCREENED_NO_CAUSAL_PROMOTION",
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

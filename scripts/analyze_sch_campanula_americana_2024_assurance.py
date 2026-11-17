"""Real original 2024 Campanula experimental colonization pollen limitation analysis.

Makowski, Lamb & Galloway (2024), American Journal of Botany,
article DOI:10.1002/ajb2.16351.
Source exact CC-BY-4.0 Zenodo record:10814705,
PLdataindividual.csv (MD5 b84fa5c83513dbe75c0bf7840d1c74aa)
pollinator.csv (MD5 81e0deaa78a6a97e1211484cb9d0d3b3).

Strong biological-unit contract:
- 237 original flower-level seed counts DO NOT represent 237 independent
  colonization experiments.
- Each experimental population/site is a cluster, carrying within-plant
  hand-supplemented vs natural-control floral treatments. Individual plant
  and flower-level pairing is tested, never fabricated.
- Four original *genetic* source populations, with autonomy category
  potentially confounded with genotype. They cannot be 4 independent papers.
- 56 pollinator rows are at original experimental-population grain; they
  are not direct per-flower visitation counts for the 237 seed records.

Main exploratory biological estimand: for each original experimental
population with both treated and untreated flowers, Delta =
mean(seednumber|supplemented) - mean(seednumber|control); compare Delta
in autonomous-selfing high/low x founded population single/small cells.
The interaction (Delta_low_single-Delta_low_small)-
(Delta_high_single-Delta_high_small) tests a Baker-law assurance pattern
but is NOT a causal effect of genetically changing self-compatibility.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import defaultdict,Counter
from pathlib import Path

from scripts.ingest_sch_campanula_americana_2024 import (
    ARTICLE_DOI,DATA_DOI,MANIFEST,_csv_rows
)

SEED=20261117
N_BOOT=3999
EXPECTED_SEED_N=237
EXPECTED_VISITOR_N=56
EXPECTED_SOURCE_POPS=4
EXPECTED_SITE_COUNT=10
SIZE_LEVELS=("single","small")
AUTONOMY_LEVELS=("high","low")
TREATMENT_CODES=("C","S")


def _genuine_rows(folder,name):
    source=Path(folder)/name
    b=source.read_bytes()
    if hashlib.md5(b).hexdigest()!=MANIFEST[name]:
        raise ValueError("Archived original 2024 Campanula MD5 mismatch "+name)
    rows,headers,encoding=_csv_rows(b)
    return rows,headers,hashlib.sha256(b).hexdigest()

def _key(row):
    return (row["site"].strip(),row["experimental.population"].strip())

def _meta(row):
    return (row["source.population"].strip(),row["autonomy"].strip(),
            row["size"].strip())

def _mean(x):
    return sum(x)/len(x) if x else None

def _cells_for_population(rows):
    groups=defaultdict(list)
    for row in rows:
        groups[_key(row)].append(row)
    data=[]
    for key,source in sorted(groups.items()):
        metas={_meta(x) for x in source}
        if len(metas)!=1:
            raise ValueError("Original experimental population changed source ancestry/autonomy/density")
        source_pop,autonomy,size=next(iter(metas))
        if autonomy not in AUTONOMY_LEVELS or size not in SIZE_LEVELS:
            raise ValueError("Source autonomy/size labels not original high/low, single/small")
        if source_pop=="":
            raise ValueError("Blank source genetic population")
        treated=defaultdict(list)
        plants=defaultdict(lambda:defaultdict(list))
        days=set()
        for r in source:
            t=r["treatment"].strip().upper()
            if t not in TREATMENT_CODES:
                raise ValueError("Original source treatment other than C/S")
            try:
                y=float(r["seednumber"].strip())
            except ValueError as exc:
                raise ValueError("Original seednumber not numeric") from exc
            if not math.isfinite(y) or y<0 or int(y)!=y:
                raise ValueError("Original seed count nonnegative-integer guard")
            treated[t].append(int(y))
            plants[r["individual"].strip()][t].append(int(y))
            days.add(r["dayfromstartofexperiment"].strip())
        pairs=[]
        for plant,tx in plants.items():
            if "C" in tx and "S" in tx:
                pairs.append({
                    "source_individual_label":plant,
                    "seed_delta_within_individual":_mean(tx["S"])-_mean(tx["C"]),
                    "n_original_control_flowers":len(tx["C"]),
                    "n_original_supplemented_flowers":len(tx["S"]),
                })
        values={
          "source_site":key[0],
          "experimental_population":key[1],
          "original_genetic_source_population":source_pop,
          "autonomy":autonomy,
          "founded_size":size,
          "source_original_n_individual_labels":len(plants),
          "source_original_n_seed_rows":len(source),
          "source_original_n_control_flowers":len(treated["C"]),
          "source_original_n_supplemented_flowers":len(treated["S"]),
          "control_mean_seeds":_mean(treated["C"]),
          "supplemented_mean_seeds":_mean(treated["S"]),
          "source_original_n_plant_labels_with_both_treatments":len(pairs),
          "paired_individual_mean_seed_delta":_mean([
              x["seed_delta_within_individual"] for x in pairs]),
          "population_seed_delta":(
              _mean(treated["S"])-_mean(treated["C"])
              if treated["S"] and treated["C"] else None),
          "n_original_start_days_observed":len(days),
          "original_flower_treatment_plant_pairs":pairs[:50],
        }
        data.append(values)
    return data


def _cell_effect(populations,field):
    groups=defaultdict(list)
    for row in populations:
        v=row[field]
        if v is not None:
            groups[(row["autonomy"],row["founded_size"])].append(v)
    out={}
    for a in AUTONOMY_LEVELS:
        for size in SIZE_LEVELS:
            vals=groups.get((a,size),[])
            out[a+"_"+size]={
                "n_experimental_population_clusters":len(vals),
                "population_equal_mean":_mean(vals),
                "population_values":vals[:150],
            }
    return out


def _effect(cell):
    keys=("high_single","high_small","low_single","low_small")
    if any(cell[k]["population_equal_mean"] is None for k in keys):
        return None
    h1=cell["high_single"]["population_equal_mean"]
    h2=cell["high_small"]["population_equal_mean"]
    l1=cell["low_single"]["population_equal_mean"]
    l2=cell["low_small"]["population_equal_mean"]
    return {
      "high_single_minus_small":h1-h2,
      "low_single_minus_small":l1-l2,
      "single_low_minus_high":l1-h1,
      "small_low_minus_high":l2-h2,
      "difference_in_differences_low_vs_high_density_response":
          (l1-l2)-(h1-h2),
    }


def _stratified_bootstrap(rows,boot,seed):
    randomizer=random.Random(seed)
    groups=defaultdict(list)
    for row in rows:
        if row["population_seed_delta"] is not None:
            groups[(row["autonomy"],row["founded_size"])].append(
                row["population_seed_delta"])
    if len(groups)!=4 or any(len(v)<3 for v in groups.values()):
        raise ValueError("Source balanced 2×2 original group contrast not identifiable")
    estimates=defaultdict(list)
    for _ in range(boot):
        matrix={}
        for (autonomy,size),values in groups.items():
            draws=randomizer.choices(values,k=len(values))
            matrix[autonomy+"_"+size]={"population_equal_mean":_mean(draws)}
        c=_effect(matrix)
        for k,v in c.items():
            estimates[k].append(v)
    def pct(arr,p):
        q=sorted(arr)
        i=(len(q)-1)*p
        lo=int(math.floor(i))
        hi=int(math.ceil(i))
        return q[lo]*(hi-i)+q[hi]*(i-lo) if lo!=hi else q[lo]
    return {
      "resampling_unit":"original_experimental_population_within_autonomy_and_founder_size",
      "source_plant_or_flower_rows_never_resampled_independently":True,
      "bootstrap_requested":boot,
      "bootstrap_completed":boot,
      "population_stratified_percentile95":{
        k:[pct(v,.025),pct(v,.975)] for k,v in estimates.items()},
    }


def _site_bootstrap(rows,boot,seed):
    randomizer=random.Random(seed)
    sites=sorted({x["source_site"] for x in rows})
    source_by_site=defaultdict(list)
    for r in rows:
        source_by_site[r["source_site"]].append(r)
    results=defaultdict(list)
    fails=0
    for _ in range(boot):
        which=randomizer.choices(sites,k=len(sites))
        replica=[x for site in which for x in source_by_site[site]]
        eff=_effect(_cell_effect(replica,"population_seed_delta"))
        if eff is None:
            fails+=1
            continue
        for k,v in eff.items():results[k].append(v)
    n=boot-fails
    def empirical95(vals):
        x=sorted(vals)
        if not x:return None
        def interp(p):
            at=(len(x)-1)*p;i=int(at);j=min(i+1,len(x)-1)
            return x[i]*(1-(at-i))+x[j]*(at-i)
        return [interp(.025),interp(.975)]
    return {
      "source_sites_resampled":len(sites),
      "bootstrap_requested":boot,
      "bootstrap_valid_all_four_cells":n,
      "bootstrap_unbalanced_site_resamples":fails,
      "source_site_95_intervals_only_if_at_least_80pct_draws_valid":
          {k:empirical95(x) for k,x in results.items()} if n>=.8*boot else None,
      "source_site_bootstrap_inference_qualified":n>=.8*boot,
    }


def _visitation_summary(seed_rows,poll_rows):
    idx={}
    for r in poll_rows:
        key=(r["site"].strip(),r["experimental.population"].strip())
        if key in idx:
            raise ValueError("Repeated original population visit record")
        idx[key]=r
    joined=[]
    grouped=defaultdict(list)
    nmissing=0
    metadata_mismatch=0
    for row in seed_rows:
        key=(row["source_site"],row["experimental_population"])
        source=idx.get(key)
        if source is None:
            nmissing+=1
            continue
        if (row["original_genetic_source_population"]!=source["source population"].strip()
            or row["autonomy"]!=source["autonomy"].strip()
            or row["founded_size"]!=source["size"].strip()):
            metadata_mismatch+=1
            continue
        visits=source["visits.per.flower"].strip()
        value=None
        try:
            value=float(visits)
            if not math.isfinite(value) or value<0:value=None
        except ValueError:
            pass
        joined.append({
           "source_site":key[0],"experimental_population":key[1],
           "autonomy":row["autonomy"],"founded_size":row["founded_size"],
           "source_plant_population_visitor_per_flower":value,
           "source_population_control_mean_seeds":row["control_mean_seeds"],
           "source_population_pollen_supplement_delta":row["population_seed_delta"],
        })
        if value is not None:
            grouped[(row["autonomy"],row["founded_size"])].append(value)
    result={
        "n_original_visitor_population_rows":len(poll_rows),
        "n_original_visitor_population_IDs_unique":len(idx),
        "n_seed_populations_with_visitor_source_record":len(joined),
        "n_seed_populations_without_visitor_source_record":nmissing,
        "n_population_source_metadata_mismatches":metadata_mismatch,
        "n_matched_visit_records_with_nonmissing_visit_per_flower":
            sum(r["source_plant_population_visitor_per_flower"] is not None for r in joined),
        "original_visits_per_flower_mean_by_autonomy_founder_size":{
          a+"_"+size:{"n_nonmissing_population_records":len(grouped[(a,size)]),
                       "mean_population_visits_per_flower":_mean(grouped[(a,size)])}
          for a in AUTONOMY_LEVELS for size in SIZE_LEVELS},
        "source_population_visitor_records_not_individual_seed_flower_visits":True,
        "visit_to_seed_causal_mediation_estimated":False,
    }
    if metadata_mismatch:
        raise ValueError("Source experimental population metadata mismatch between files")
    return result


def run(folder,boot=N_BOOT):
    if not 100<=boot<=20000:
        raise ValueError("Original population bootstrap outside bounded range")
    seed,seedhead,seedsha=_genuine_rows(folder,"PLdataindividual.csv")
    poll,pollhead,pollsha=_genuine_rows(folder,"pollinator.csv")
    if len(seed)!=EXPECTED_SEED_N or len(poll)!=EXPECTED_VISITOR_N:
        raise ValueError("Original source 2024 Campanula row counts changed")
    populations=_cells_for_population(seed)
    if len({x["source_site"] for x in populations})!=EXPECTED_SITE_COUNT:
        raise ValueError("Original ten experimental sites changed")
    genetic={x["original_genetic_source_population"] for x in populations}
    if len(genetic)!=EXPECTED_SOURCE_POPS:
        raise ValueError("Original four genetic source populations changed")
    nmatched=sum(x["population_seed_delta"] is not None for x in populations)
    unmatched=[x for x in populations if x["population_seed_delta"] is None]
    matched=[x for x in populations if x["population_seed_delta"] is not None]
    pairing={
      "n_source_experimental_population_clusters":len(populations),
      "n_original_population_clusters_with_both_supp_and_control":nmatched,
      "n_population_clusters_without_both_treatments":len(unmatched),
      "n_original_flower_rows_within_matched_populations":sum(x["source_original_n_seed_rows"] for x in matched),
      "n_original_individuals_with_both_flower_treatments":sum(
          x["source_original_n_plant_labels_with_both_treatments"] for x in populations),
      "n_source_population_cells_by_autonomy_size":{
        a+"_"+s:sum(x["autonomy"]==a and x["founded_size"]==s
                   for x in matched) for a in AUTONOMY_LEVELS for s in SIZE_LEVELS},
      "genetic_source_population_to_autonomy":{
         source:sorted({x["autonomy"] for x in populations
                        if x["original_genetic_source_population"]==source})
         for source in sorted(genetic)},
      "original_source_unmatched_population_labels":[
        x["source_site"]+"|"+x["experimental_population"] for x in unmatched],
    }
    seed_cell=_cell_effect(matched,"population_seed_delta")
    control=_cell_effect(matched,"control_mean_seeds")
    supplement=_cell_effect(matched,"supplemented_mean_seeds")
    difference=_effect(seed_cell)
    if difference is None:
        raise ValueError("Missing source 2x2 original supplement cell")
    bootpop=_stratified_bootstrap(matched,boot,SEED)
    bootsite=_site_bootstrap(matched,boot,SEED)
    site_loo=[]
    for site in sorted({x["source_site"] for x in matched}):
        z=_effect(_cell_effect([x for x in matched if x["source_site"]!=site],
                              "population_seed_delta"))
        site_loo.append({"excluded_source_site":site,"effect":z})
    group_loo=[]
    for gen in sorted(genetic):
        z=_effect(_cell_effect([
            x for x in matched if x["original_genetic_source_population"]!=gen],
            "population_seed_delta"))
        group_loo.append({"excluded_source_genetic_population":gen,
                          "2x2_estimand_identifiable":z is not None,
                          "effect":z})
    visits=_visitation_summary(populations,poll)
    original_seeds=Counter(int(float(r["seednumber"])) for r in seed)
    experiment_levels=Counter((r["autonomy"].strip(),r["size"].strip(),r["treatment"].strip())
                              for r in seed)
    return {
      "analysis":"sch_campanula_americana_2024_original_colonization_assurance_v1",
      "article_DOI":ARTICLE_DOI,"original_zenodo_data_DOI":DATA_DOI,
      "original_seed_MD5":MANIFEST["PLdataindividual.csv"],
      "original_pollinator_MD5":MANIFEST["pollinator.csv"],
      "verified_source_SHA256_seed":seedsha,
      "verified_source_SHA256_visitor":pollsha,
      "n_original_seed_flower_rows":len(seed),
      "n_original_visitor_population_records":len(poll),
      "original_genetic_source_population_count":len(genetic),
      "n_original_experimental_site_IDs":EXPECTED_SITE_COUNT,
      "original_seed_count_range":[min(original_seeds),max(original_seeds)],
      "source_original_zero_seed_flower_rows":original_seeds[0],
      "source_original_treatment_code_interpretation":{"C":"control","S":"pollen supplemented"},
      "original_flower_level_autonomy_size_treatment_cell_counts":{
        "|".join(k):n for k,n in sorted(experiment_levels.items())},
      "source_matched_population_grain":pairing,
      "population_equal_seed_benefit_by_autonomy_and_founder_size":seed_cell,
      "population_equal_control_seed_set_by_autonomy_and_founder_size":control,
      "population_equal_supplemented_seed_set_by_autonomy_and_founder_size":supplement,
      "source_population_equal_difference_in_differences":difference,
      "population_stratified_bootstrap":bootpop,
      "site_block_bootstrap":bootsite,
      "leave_entire_original_site_out":site_loo,
      "leave_entire_original_genetic_source_population_out":group_loo,
      "source_separate_experimental_population_pollinator_observations":visits,
      "source_population_estimates":populations,
      "original_founded_density_and_selfing_category_causal_interaction_identified":False,
      "source_selfing_category_not_randomly_assigned_genetic_source_background":True,
      "original_supplemented_flower_seed_counts_are_not_single_flower_pollen_tube_deposition":True,
      "no_SCH_same_coordinate_dual_function_optima_or_loss_L":True,
      "critical_limits":[
       "only_four_genetic_source_populations_high_vs_low_autonomy_not_randomized",
       "flower_rows_repeated_within_experimental_populations_plant_ids_and_field_sites",
       "population_cluster_bootstrap_not_independent_of_common_genetic_source_background",
       "ten_site_bootstrap_has_limited_spatial_blocks_and_invalid_draws_possible",
       "site_initiation_time_can_confounds_availability_and_pollinator_activity",
       "population_supplemented_minus_control_seed_number_is_not_individual_seed_fitness_total",
       "visitation_data_source_population_level_different_from_seed_treatment_flower_risk_set",
       "no_common_manipulated_morphological_trait_or_two_pure_function_optima",
      ],
      "status":"REAL_ORIGINAL_INDEPENDENT_CAMPANULA_EXPERIMENTAL_COLONIZATION_SOURCE_REANALYSIS_NOT_SCH_L",
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=Path("artifacts/sch_campanula_2024"))
    p.add_argument("--out",type=Path,default=Path("artifacts/sch_campanula_2024/assurance_population_reanalysis.json"))
    p.add_argument("--bootstrap",type=int,default=N_BOOT)
    a=p.parse_args()
    result=run(a.source,a.bootstrap)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    compact={k:v for k,v in result.items()
             if k not in ("source_population_estimates",)}
    print("BEGIN_SCH_CAMPANULA_2024_REAL_POPULATION_ASSURANCE")
    print(json.dumps(compact,indent=2,sort_keys=True,ensure_ascii=False))
    print("END_SCH_CAMPANULA_2024_REAL_POPULATION_ASSURANCE")

if __name__=="__main__":
    main()

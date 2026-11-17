"""Source-original blueberry first-visit versus subsequent-visit gate.

Kendall et al. (2020), JAE DOI 10.1111/1365-2664.13751.
The original tagged flower is the same flower followed to fruit set.
The correct original multiple-visit CSV and pollination CSV are recovered from
a prior MD5-verified original source artifact; raw_source rechecks MD5.

For visits <=5, fit in ONE binomial logistic model:
 logit P(fruit_i=1) =
   source_type x year x block intercept +
   source_type coefficient * 1(visits_i>=1) +
   source_type coefficient * log(visits_i) * 1(visits_i>=1).

The first coefficient compares exactly zero visits with one legitimate
recorded visit within source type and source site/year; the second describes
the additional 1..5 visit response conditional on already >=1 recorded visit.
The sum of two separate regressions is NOT an equivalent test of the
coefficient contrast, hence a single joint model is essential.

0-visit bagged controls are not necessarily an exchangeable natural
zero-visitation sample. Cultivar type, pollinator identity, site/year and
genetic mating system are not randomized. Plant-label-cluster robust inference
does not repair unmeasured source site or genotype confounding.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
import json
import math
from pathlib import Path

from scripts.analyze_sch_blueberry_2020_matched_flower_gate import (
    DOI,SOURCE_RECORD_ID,SOURCE_TYPES,HIGHBUSH_TYPES,RABBITEYE_TYPE,
    raw_source,plant_key,fruit,_visit_count
)

try:
    import numpy as np
except ModuleNotFoundError:
    np=None

N_SOURCE_VISIT=2080
N_SOURCE_POLLINATION=2125
N_VISITS_0TO5=1849
N_VISITS_1TO5=1080
N_PLANT_SOURCE_LABELS_0TO5=238
N_ORIGINAL_PROGRAMMES=1
N_0_VISITS=769

def _two_part_design(rows):
    """Site-specific intercept and paired, cultivar-specific visit processes."""
    if np is None:raise RuntimeError("numpy needed for source numeric analysis")
    sites=sorted({"|".join((r["Species"].strip(),r["Year"].strip(),
                           r["Block"].strip())) for r in rows})
    n=len(rows)
    p=len(sites)
    code={v:i for i,v in enumerate(sites)}
    X=np.zeros((n,p+2*len(SOURCE_TYPES)),dtype=float)
    y=np.empty(n,dtype=int)
    groups=[]
    visit_table=Counter()
    site_support=defaultdict(lambda:{"zero":0,"one":0,"two_to_five":0})
    source_risk=defaultdict(lambda:{"n_zero":0,"set_zero":0,"n_one":0,"set_one":0})
    for i,row in enumerate(rows):
        typ=row["Species"].strip()
        if typ not in SOURCE_TYPES:raise ValueError("Original cultivar type changed")
        v=_visit_count(row)
        if v>5:raise ValueError("Source predeclared support is 0..5")
        site="|".join((typ,row["Year"].strip(),row["Block"].strip()))
        X[i,code[site]]=1.
        j=SOURCE_TYPES.index(typ)
        if v>=1:X[i,p+j]=1.
        if v>=2:X[i,p+len(SOURCE_TYPES)+j]=math.log(v)
        y[i]=fruit(row)
        groups.append(plant_key(row))
        visit_table[(typ,v)]+=1
        if v==0:
            site_support[site]["zero"]+=1
            source_risk[typ]["n_zero"]+=1
            source_risk[typ]["set_zero"]+=y[i]
        elif v==1:
            site_support[site]["one"]+=1
            source_risk[typ]["n_one"]+=1
            source_risk[typ]["set_one"]+=y[i]
        else:site_support[site]["two_to_five"]+=1
    if np.linalg.matrix_rank(X)!=X.shape[1]:
        raise ValueError("Source site/first-visit/extra-visit design rank deficient")
    if len(set(groups))!=N_PLANT_SOURCE_LABELS_0TO5:
        raise ValueError("Original 0..5 plant-label uncertainty grain changed")
    per_type={}
    for typ in SOURCE_TYPES:
        x=source_risk[typ]
        if not x["n_zero"] or not x["n_one"]:
            raise ValueError("Source type missing zero or first-visit flowers")
        per_type[typ]={
          **x,
          "fruit_rate_zero_visits":x["set_zero"]/x["n_zero"],
          "fruit_rate_exactly_one_visit":x["set_one"]/x["n_one"],
          "observed_one_visit_minus_bagged_zero_difference":
              x["set_one"]/x["n_one"]-x["set_zero"]/x["n_zero"],
        }
    return X,y,np.asarray(groups,dtype=str),sites,dict(site_support),per_type,dict(visit_table)

def _source_fit(rows):
    import statsmodels.api as sm
    from scipy.stats import norm,chi2
    X,y,group,sites,sitesupport,counts,visits=_two_part_design(rows)
    fit=sm.GLM(y,X,family=sm.families.Binomial()).fit(
       maxiter=300,cov_type="cluster",cov_kwds={"groups":group})
    if not fit.converged:raise ValueError("Original source two-part logit did not converge")
    b=np.asarray(fit.params,dtype=float)
    cov=np.asarray(fit.cov_params(),dtype=float)
    n_sites=len(sites)
    def regression_coeff(index):
        beta=float(b[index])
        se=float(math.sqrt(cov[index,index]))
        if not math.isfinite(se) or se<=0:raise ValueError("Invalid source SE")
        return {
          "logit_beta":beta,"source_plant_label_cluster_SE":se,
          "nominal_two_sided_p":float(2*norm.sf(abs(beta/se))),
          "cluster_robust_95CI":[beta-1.96*se,beta+1.96*se],
          "odds_multiplier_per_unit_term":float(math.exp(beta)),
        }
    per_type={}
    for j,typ in enumerate(SOURCE_TYPES):
        per_type[typ]={
          "first_visit_vs_bagged_zero":regression_coeff(n_sites+j),
          "incremental_log_visit_dose_among_visited":
             regression_coeff(n_sites+len(SOURCE_TYPES)+j),
          "original_raw_zero_vs_one_source_rates":counts[typ],
          "n_source_plant_labels":len(set(group[
              np.asarray([r["Species"].strip()==typ for r in rows],bool)])),
        }
    def contrast_weights(process):
        idx=n_sites+(0 if process=="first" else len(SOURCE_TYPES))
        weights=np.zeros(len(b))
        weights[idx+SOURCE_TYPES.index(RABBITEYE_TYPE)]=1.
        for typ in HIGHBUSH_TYPES:
            weights[idx+SOURCE_TYPES.index(typ)]-=.5
        return weights
    diffs={}
    heterogeneity={}
    for process in ("first","additional"):
        w=contrast_weights(process)
        delta=float(w@b)
        var=float(w@cov@w)
        if not math.isfinite(var) or var<=0:raise ValueError("Invalid source contrast variance")
        se=math.sqrt(var)
        idx=n_sites+(0 if process=="first" else len(SOURCE_TYPES))
        L=np.zeros((2,len(b)))
        L[0,idx+1]=1.;L[0,idx+0]=-1.
        L[1,idx+2]=1.;L[1,idx+0]=-1.
        v=L@cov@L.T
        if np.linalg.matrix_rank(v)!=2:
            raise ValueError("Source cultivar slope covariance singular")
        wald=float((L@b)@np.linalg.solve(v,L@b))
        diffs[process]={
          "rabbiteye_minus_mean_highbush_beta":delta,
          "source_plant_cluster_SE":se,
          "nominal_two_sided_P":float(2*norm.sf(abs(delta/se))),
          "source_cluster_95CI":[delta-1.96*se,delta+1.96*se],
        }
        heterogeneity[process]={
          "all_three_type_effects_equal_chi2":wald,
          "degrees_of_freedom":2,
          "nominal_chi2_P":float(chi2.sf(wald,2)),
        }
    overlaps={}
    for typ in SOURCE_TYPES:
        site_rows={k:v for k,v in sitesupport.items()
                   if k.split("|")[0]==typ}
        overlaps[typ]={
            "n_original_site_year_blocks":len(site_rows),
            "n_blocks_with_both_0_and_1_visits":sum(
                v["zero"]>0 and v["one"]>0 for v in site_rows.values()),
            "n_blocks_with_zero_and_1to5_visits":sum(
                v["zero"]>0 and v["one"]+v["two_to_five"]>0
                for v in site_rows.values()),
            "original_site_visit_bin_counts":site_rows,
        }
    return {
      "n_original_flower_rows":len(rows),
      "n_original_plant_labels":len(set(group)),
      "n_original_source_type_year_block_intercepts":n_sites,
      "all_source_visit_count_distribution":{
         str(v):sum(c for (typ,k),c in visits.items() if k==v)
         for v in range(6)},
      "original_within_site_zero_first_visit_overlap":overlaps,
      "source_type_first_and_additional_visit_effects":per_type,
      "source_rabbiteye_vs_highbush_effect_differences":diffs,
      "three_source_type_effect_heterogeneity":heterogeneity,
      "actual_model":"same_original_0to5_flowers_joint_first_plus_incremental_binomial_logit",
      "independent_cluster_unit":"original_plant_label_nested_type_year_block",
      "first_visit_not_randomized_compatible_pollinium_deposition":True,
      "zero_visit_bagged_control_may_differ_from_visit_treatment_process":True,
      "source_visitors_confounded_with_original_cultivar_type":True,
    }

def _pollination_raw_controls(rows):
    """All original four labelled pollen source treatments, no fake matching."""
    treatments=("No pollination","Self pollination","Cross pollination",
                "Open pollination")
    by={}
    for typ in SOURCE_TYPES:
        sample=[r for r in rows if r["Species"].strip()==typ]
        cells={}
        sites={}
        for trt in treatments:
            sub=[r for r in sample if r["TREATMENT"].strip()==trt]
            if not sub:raise ValueError("Missing original pollination treatment")
            site_counts=defaultdict(lambda:{"fruit":0,"n":0})
            for r in sub:
                site="|".join((typ,r["Year"].strip(),r["Block"].strip()))
                site_counts[site]["n"]+=1
                site_counts[site]["fruit"]+=fruit(r)
            n=len(sub);k=sum(fruit(r) for r in sub)
            cells[trt]={
              "source_tagged_flower_count":n,
              "source_fruit_count":k,
              "observed_fruit_rate":k/n,
              "source_plant_label_count":len(set(plant_key(r) for r in sub)),
            }
            sites[trt]=dict(site_counts)
        site_overlap={}
        for a,b in (("Self pollination","No pollination"),
                    ("Cross pollination","No pollination"),
                    ("Open pollination","No pollination"),
                    ("Cross pollination","Self pollination")):
            ka=set(sites[a]);kb=set(sites[b]);both=ka&kb
            key=a+"__minus__"+b
            site_overlap[key]={
              "n_original_site_year_blocks_with_both_treatments":len(both),
              "site_year_block_names":sorted(both),
              "n_pooled_source_flower_rows_on_overlapping_sites":sum(
                 sites[a][site]["n"]+sites[b][site]["n"] for site in both),
              "unadjusted_source_risk_difference_all_sites":
                 cells[a]["observed_fruit_rate"]-cells[b]["observed_fruit_rate"],
            }
            if both:
                weighted=0.;total=0.
                for site in both:
                    za=sites[a][site];zb=sites[b][site]
                    w=za["n"]*zb["n"]/(za["n"]+zb["n"])
                    weighted+=w*(za["fruit"]/za["n"]-zb["fruit"]/zb["n"])
                    total+=w
                site_overlap[key]["source_site_harmonic_weighted_risk_difference"]=weighted/total
            else:
                site_overlap[key]["source_site_harmonic_weighted_risk_difference"]=None
        by[typ]={"original_source_four_treatment_fruit_rates":cells,
                 "source_site_year_block_overlap_audits":site_overlap}
    return {
        "n_original_flower_rows":len(rows),
        "original_four_pollination_protocols":list(treatments),
        "source_type_four_treatment_comparison":by,
        "no_pollination_bagged_not_emasculated_like_hand_cross_self":True,
        "cross_self_hand_pollen_sourced_from_different_cultivars_of_same_type":True,
        "cross_no_pollen_difference_is_not_isolated_pollen_compatibility_effect":True,
        "source_mating_system_cultivar_identity_not_randomized":True,
    }

def run(folder):
    multiple,mm,ms=raw_source(folder,"multiple")
    poll,pm,ps=raw_source(folder,"pollination")
    short=[r for r in multiple if _visit_count(r)<=5]
    if len(multiple)!=N_SOURCE_VISIT or len(short)!=N_VISITS_0TO5:
        raise ValueError("Original 2020 tagged flower visit sample changed")
    if len([r for r in short if _visit_count(r)>=1])!=N_VISITS_1TO5:
        raise ValueError("Original visited-only source denominator changed")
    if len([r for r in short if _visit_count(r)==0])!=N_0_VISITS:
        raise ValueError("Original bagged-zero denominator changed")
    if len(poll)!=N_SOURCE_POLLINATION:
        raise ValueError("Original 2020 hand-pollination sample changed")
    model=_source_fit(short)
    controls=_pollination_raw_controls(poll)
    return {
      "analysis":"sch_blueberry_source_first_visit_vs_incremental_gate_v1",
      "source_paper_DOI":DOI,
      "source_original_zenodo_record_id":SOURCE_RECORD_ID,
      "original_source_multiple_visits_sha256":ms,
      "original_source_pollination_protocol_sha256":ps,
      "n_original_published_programmes":N_ORIGINAL_PROGRAMMES,
      "n_original_tagged_flower_visit_rows":len(multiple),
      "n_original_tagged_flower_pollination_rows":len(poll),
      "source_visit_0to5_piecewise":model,
      "source_original_four_pollination_protocols":controls,
      "not_an_original_author_fitted_piecewise_test":True,
      "no_compatible_pollen_fertilization_or_mechanistic_gate_measured":True,
      "no_global_between_species_mating_system_causal_inference":True,
      "no_SCH_same_trait_function_specific_optima_or_loss_L":True,
      "critical_limits":[
       "zero_visit_control_was_rebagged_and_may_differ_from_positive_visit_protocol",
       "source_tagged_flower_is_outcome_unit_plant_label_cluster_is_uncertainty_unit",
       "cultivar_identity_and_pollinator_species_not_independently_randomized",
       "source_flower_samples_nested_in_sites_years_and_original_plant_labels",
       "separate_hand_cross_self_controls_do_not_share_same_flowers_as_visit_doses",
       "hand_cross_self_emasculation_protocol_differs_from_bagged_no_pollen_controls",
       "piecewise_first_visit_is_not_a_true_randomized_effect_of_one_compatible_pollen_load",
       "each_source_cultivar_is_one_cultivar_not_a_random_biogeographical_species_sample",
       "multiple_slopes_are_exploratory_and_not_prospective_familywise_tests",
       "fruit_set_is_binary_and_does_not_measure_viable_seed_or_descendant_fitness",
       "sch_compromise_L_and_causal_trait_specific_function_conflict_unidentified",
      ],
      "status":"ORIGINAL_TAGGED_FLOWER_TWO_VISIT_GATE_AND_FOUR_POLLINATION_PROTOCOLS_FITTED_SCOPE_LIMITED",
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source_dir",type=Path,default=Path("artifacts/sch_blueberry_original"))
    p.add_argument("--output",type=Path,default=Path("artifacts/sch_blueberry_original/first_vs_additional_visits.json"))
    a=p.parse_args()
    result=run(a.source_dir)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("BEGIN_SCH_SOURCE_FIRST_ADDITIONAL_VISIT_GATE")
    print(json.dumps({
      "site_adjusted_piecewise":result["source_visit_0to5_piecewise"],
      "source_pollination_four_protocols":result["source_original_four_pollination_protocols"],
      "status":result["status"]},
      sort_keys=True,indent=2,ensure_ascii=False))
    print("END_SCH_SOURCE_FIRST_ADDITIONAL_VISIT_GATE")

if __name__=="__main__":
    main()

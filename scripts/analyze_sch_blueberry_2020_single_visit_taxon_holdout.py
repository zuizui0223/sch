"""Test a *separate* single-visit blueberry experiment on authentic tagged flowers.

Original source: Kendall et al. (2020), J Appl Ecol,
DOI 10.1111/1365-2664.13751. Dataset Zenodo 3987488,
original Dryad DOI 10.5061/dryad.tmpg4f4wj.

Source single-visit data: 1,309 original individually tagged flowers,
338 fruits, 971 no fruits, 219 original plant labels. Source SPEC.COM
'HB' is one honeybee Apis mellifera, 'Other' is one bumblebee
Bombus terrestris in Blue Rose, or one stingless bee Tetragonula
carbonaria in Powder Blue/Snowchaser; 'UP' is an unpollinated bagged
control. Roles verified against publisher's source README.pdf.

Compare within source site/year/cultivar and with source plant-label
cluster robust inference:
  honeybee one visit vs bagged unpollinated,
  alternative one bee visit vs bagged unpollinated,
  alternative vs honeybee among *visited* flowers.

Only sites with BOTH source treatments are retained per comparison,
so site intercept does not extrapolate contrasts across disjoint sites.
Original floral visitor taxon is NOT randomly assigned; cultivar,
site/year, mating system and visitor context are partly confounded.
No effective pollen load or SCH loss L is inferred.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter,defaultdict
from pathlib import Path

from scripts.analyze_sch_blueberry_2020_matched_flower_gate import (
    DOI,SOURCE_RECORD_ID,SOURCE_TYPES,HIGHBUSH_TYPES,RABBITEYE_TYPE,
    raw_source,plant_key,fruit,
)

try:
    import numpy as np
except ModuleNotFoundError:
    np=None

SOURCE_MD5="d7ed02c7aa254a963043539c06c99ed7"
SOURCE_SHA256="8e063d82256ef72edad3d429d754b3882888205f78c559bb61aea643c09594c3"
EXPECTED_N=1309
EXPECTED_FRUIT=338
EXPECTED_N_PLANT_LABELS=219
EXPECTED_VISIT_COUNTS={"HB":179,"Other":152,"UP":978}
EXPECTED_BLUEBERRY_COUNTS={"Blue Rose":334,"Powder Blue":391,"Snowchaser":584}
ORIGINAL_VISITOR_NAMES={
    "Blue Rose":{"HB":"Apis mellifera","Other":"Bombus terrestris","UP":"bagged unpollinated"},
    "Powder Blue":{"HB":"Apis mellifera","Other":"Tetragonula carbonaria","UP":"bagged unpollinated"},
    "Snowchaser":{"HB":"Apis mellifera","Other":"Tetragonula carbonaria","UP":"bagged unpollinated"},
}
COMPARISONS=(
   ("HB_vs_UP","HB","UP"),
   ("Other_vs_UP","Other","UP"),
   ("Other_vs_HB","Other","HB"),
)
N_BOOTSTRAP=1999
SEED=20261117


def read_authentic(folder):
    rows,meta,sha=raw_source(folder,"single")
    if sha!=SOURCE_SHA256:
        raise ValueError("Original single-visit source SHA256 drift")
    if len(rows)!=EXPECTED_N or len({plant_key(r) for r in rows})!=EXPECTED_N_PLANT_LABELS:
        raise ValueError("Original single-visit source plant/flower counts changed")
    if sum(fruit(r) for r in rows)!=EXPECTED_FRUIT:
        raise ValueError("Original source fruit-set tally changed")
    counts=Counter(r["SPEC.COM"].strip() for r in rows)
    if dict(counts)!=EXPECTED_VISIT_COUNTS:
        raise ValueError("Original source HB/Other/UP codes/counts changed")
    types=Counter(r["Species"].strip() for r in rows)
    if dict(types)!=EXPECTED_BLUEBERRY_COUNTS:
        raise ValueError("Original source cultivar types/counts changed")
    if meta["n_composite_flower_identity_ambiguous_duplicate_keys"]!=0:
        raise ValueError("Original same-flower identity duplicated")
    for r in rows:
        if r["SPEC.COM"].strip() not in ORIGINAL_VISITOR_NAMES[r["Species"].strip()]:
            raise ValueError("Unsupported visitor or source blueberry cultivar")
    return rows,{
       "original_rows":len(rows),
       "n_original_plant_labels":len(set(plant_key(r) for r in rows)),
       "original_SHA256":sha,
       "original_source_MD5":SOURCE_MD5,
       "source_original_cultivar_counts":dict(types),
       "original_visitor_counts":dict(counts),
       "source_binary_fruit_count":EXPECTED_FRUIT,
       "source_no_fruit_count":EXPECTED_N-EXPECTED_FRUIT,
    }


def all_source_cells(rows):
    """One row per cultivar × visitor code with the ORIGINAL denominators."""
    counts={}
    site_cells=defaultdict(lambda:{"n":0,"fruit":0,"source_plant_labels":set()})
    for r in rows:
        typ=r["Species"].strip()
        visit=r["SPEC.COM"].strip()
        key=(typ,visit)
        z=counts.setdefault(key,{"n":0,"fruit":0,"plant_labels":set()})
        z["n"]+=1
        z["fruit"]+=fruit(r)
        z["plant_labels"].add(plant_key(r))
        site="|".join((typ,r["Year"].strip(),r["Block"].strip()))
        z=site_cells[(site,visit)]
        z["n"]+=1
        z["fruit"]+=fruit(r)
        z["source_plant_labels"].add(plant_key(r))
    original=[]
    for typ in SOURCE_TYPES:
        for v in ("UP","HB","Other"):
            c=counts.get((typ,v))
            if not c:
                raise ValueError("Missing source visitor code within blueberry cultivar")
            original.append({
                "source_cultivar":typ,
                "original_visitor_code":v,
                "visitor_taxon":ORIGINAL_VISITOR_NAMES[typ][v],
                "original_tagged_flowers":c["n"],
                "original_fruit_set_count":c["fruit"],
                "original_binary_fruit_set_rate":c["fruit"]/c["n"],
                "source_plant_label_groups":len(c["plant_labels"]),
            })
    source_by_site=[]
    for (site,visit),z in sorted(site_cells.items()):
        source_by_site.append({
            "original_cultivar":site.split("|")[0],
            "original_site_year_block":site,
            "original_visitor_code":visit,
            "original_tagged_flower_n":z["n"],
            "original_fruit_set_count":z["fruit"],
            "original_flower_fruit_rate":z["fruit"]/z["n"],
            "source_plant_label_n":len(z["source_plant_labels"]),
        })
    return original,source_by_site


def _overlap_group(rows,treated,baseline):
    """Retain only site/year blocks where BOTH source treatments appear."""
    source=defaultdict(lambda:Counter())
    for row in rows:
        code=row["SPEC.COM"].strip()
        if code not in (treated,baseline):continue
        site="|".join((row["Species"].strip(),row["Year"].strip(),row["Block"].strip()))
        source[site][code]+=1
    matched={k for k,v in source.items() if v[treated]>0 and v[baseline]>0}
    chosen=[r for r in rows if r["SPEC.COM"].strip() in (treated,baseline)
            and "|".join((r["Species"].strip(),r["Year"].strip(),
                          r["Block"].strip())) in matched]
    if len(chosen)<100:
        raise ValueError("No useful original source site-matched comparison")
    return chosen,matched,source


def _fit_source_logit(rows,treated,baseline):
    import numpy as np
    import statsmodels.api as sm
    from scipy.stats import norm,chi2
    source,matched,sitecount=_overlap_group(rows,treated,baseline)
    sites=sorted(matched)
    labels=sorted(SOURCE_TYPES)
    site_index={key:i for i,key in enumerate(sites)}
    n=len(source)
    p=len(sites)
    X=np.zeros((n,p+3))
    y=np.zeros(n,float)
    clusters=[]
    type_treated=Counter()
    type_baseline=Counter()
    counts=defaultdict(lambda:{"n_treatment":0,"fruit_treatment":0,
                               "n_baseline":0,"fruit_baseline":0,"plant_labels":set()})
    for i,row in enumerate(source):
        typ=row["Species"].strip()
        site="|".join((typ,row["Year"].strip(),row["Block"].strip()))
        X[i,site_index[site]]=1.
        visitor=row["SPEC.COM"].strip()
        if visitor==treated:
            X[i,p+SOURCE_TYPES.index(typ)]=1.
            type_treated[typ]+=1
            counts[typ]["n_treatment"]+=1
            counts[typ]["fruit_treatment"]+=fruit(row)
        elif visitor==baseline:
            type_baseline[typ]+=1
            counts[typ]["n_baseline"]+=1
            counts[typ]["fruit_baseline"]+=fruit(row)
        else:raise ValueError("Unexpected visitor category")
        y[i]=fruit(row)
        label=plant_key(row)
        clusters.append(label)
        counts[typ]["plant_labels"].add(label)
    if np.linalg.matrix_rank(X)!=X.shape[1]:
        raise ValueError("Original source matched site + visitor design rank deficient")
    if min(type_treated.values())<5 or min(type_baseline.values())<5:
        raise ValueError("Source visitor treatment sparse in one blueberry cultivar")
    fit=sm.GLM(y,X,family=sm.families.Binomial()).fit(
        maxiter=300,cov_type="cluster",
        cov_kwds={"groups":np.asarray(clusters,dtype=str)})
    if not fit.converged:
        raise ValueError("Original single-visit logistic model failed")
    coeff=np.asarray(fit.params,float)
    cov=np.asarray(fit.cov_params(),float)
    stats={}
    for typ in SOURCE_TYPES:
        idx=p+SOURCE_TYPES.index(typ)
        beta=float(coeff[idx])
        se=math.sqrt(float(cov[idx,idx]))
        if not math.isfinite(se) or se<=0:
            raise ValueError("Invalid original source plant cluster SE")
        stat=counts[typ]
        if stat["n_treatment"]<5 or stat["n_baseline"]<5:
            raise ValueError("Missing original source per-type treatment opportunity")
        stats[typ]={
            "source_type":typ,
            "source_visitor_treated":ORIGINAL_VISITOR_NAMES[typ][treated],
            "source_visitor_baseline":ORIGINAL_VISITOR_NAMES[typ][baseline],
            "original_flower_rows_treatment":stat["n_treatment"],
            "original_fruit_set_treatment":stat["fruit_treatment"],
            "original_flower_rows_baseline":stat["n_baseline"],
            "original_fruit_set_baseline":stat["fruit_baseline"],
            "original_source_plant_label_clusters":len(stat["plant_labels"]),
            "empirical_treated_minus_baseline_fruit_rate":
               stat["fruit_treatment"]/stat["n_treatment"]-
               stat["fruit_baseline"]/stat["n_baseline"],
            "source_site_year_adjusted_logit_beta":beta,
            "source_ID_cluster_robust_SE":se,
            "nominal_two_sided_normal_P":float(2*norm.sf(abs(beta/se))),
            "source_cluster_95CI":[beta-1.96*se,beta+1.96*se],
        }
    L=np.zeros((2,len(coeff)))
    L[0,p+1]=1;L[0,p+0]=-1
    L[1,p+2]=1;L[1,p+0]=-1
    Vs=L@cov@L.T
    if np.linalg.matrix_rank(Vs)!=2:
        raise ValueError("Original three-cultivar visitor effect covariance singular")
    W=float((L@coeff)@np.linalg.solve(Vs,L@coeff))
    weights=np.zeros(len(coeff))
    weights[p+SOURCE_TYPES.index("Powder Blue")]=1
    weights[p+SOURCE_TYPES.index("Blue Rose")]=-.5
    weights[p+SOURCE_TYPES.index("Snowchaser")]=-.5
    contrast=float(weights@coeff)
    contrast_se=math.sqrt(float(weights@cov@weights))
    if not math.isfinite(contrast_se) or contrast_se<=0:
        raise ValueError("Original cultivar-level source visitor contrast SE invalid")
    source_sites={}
    for typ in SOURCE_TYPES:
        relevant=sorted(k for k in matched if k.split("|")[0]==typ)
        source_sites[typ]={
            "n_matched_year_block_sites":len(relevant),
            "original_site_year_block_names":relevant,
            "site_treatment_n":{site:sitecount[site][treated] for site in relevant},
            "site_baseline_n":{site:sitecount[site][baseline] for site in relevant},
        }
    return {
       "contrast":treated+"_vs_"+baseline,
       "source_role":("honeybee_single_visit" if treated=="HB" else
                      "type_specific_other_bee_single_visit"),
       "n_original_site_matched_tagged_flower_rows":n,
       "n_original_source_plant_label_clusters":len(set(clusters)),
       "n_source_site_year_block_intercepts":len(sites),
       "source_types":stats,
       "source_year_block_treatment_overlap":source_sites,
       "all_three_cultivar_effects_equal_Wald_chi2":W,
       "all_three_cultivar_effects_equal_Wald_df":2,
       "all_three_cultivar_effects_equal_nominal_P":float(chi2.sf(W,2)),
       "powder_minus_mean_highbush_logit_delta":contrast,
       "powder_minus_mean_highbush_cluster_SE":contrast_se,
       "powder_minus_mean_highbush_nominal_P":float(2*norm.sf(abs(contrast/contrast_se))),
       "powder_minus_mean_highbush_cluster95":[contrast-1.96*contrast_se,
                                                contrast+1.96*contrast_se],
       "source_plant_cluster_robust_within_year_block":True,
       "original_pollen_species_randomized_in_biological_experiment":False,
    }


def _plant_label_bootstrap_risks(rows,treated,baseline,boot=N_BOOTSTRAP):
    """Nonparametric original-source rate differences on per-flower outcome."""
    import numpy as np
    source,sites,_=_overlap_group(rows,treated,baseline)
    group_by_type=defaultdict(lambda:defaultdict(lambda:np.zeros(4,dtype=int)))
    for row in source:
        typ=row["Species"].strip()
        key=plant_key(row)
        i=0 if row["SPEC.COM"].strip()==treated else 2
        group_by_type[typ][key][i]+=1
        group_by_type[typ][key][i+1]+=fruit(row)
    arrays={}
    for typ in SOURCE_TYPES:
        group=group_by_type[typ]
        if len(group)<15:
            raise ValueError("Too few original plant-label units for bootstrap")
        arrays[typ]=np.asarray([group[k] for k in sorted(group)],int)
    rng=np.random.default_rng(SEED)
    estimates={typ:[] for typ in SOURCE_TYPES}
    contrasts=[]
    invalid=0
    for _ in range(boot):
        current={}
        for typ in SOURCE_TYPES:
            A=arrays[typ]
            ix=rng.integers(0,len(A),len(A))
            n=A[ix].sum(axis=0)
            if n[0]<=0 or n[2]<=0:
                break
            current[typ]=n[1]/n[0]-n[3]/n[2]
        if len(current)!=len(SOURCE_TYPES):
            invalid+=1
            continue
        for typ in SOURCE_TYPES:
            estimates[typ].append(current[typ])
        contrasts.append(current["Powder Blue"]-
                         .5*(current["Blue Rose"]+current["Snowchaser"]))
    if len(contrasts)<.90*boot:
        raise ValueError("Too few source cluster bootstrap draws with visitor matches")
    return {
      "n_requested_source_ID_bootstrap":boot,
      "n_valid_source_ID_bootstrap":len(contrasts),
      "n_missing_treatment_resamples_excluded":invalid,
      "original_source_within_type_risk_diff_bootstrap":{
        typ:{
          "cluster_bootstrap95":list(map(float,np.percentile(estimates[typ],[2.5,97.5]))),
          "source_type":"ONE_ORIGINAL_CULTIVAR_NOT_ONE_INDEPENDENT_SPECIES",
        } for typ in SOURCE_TYPES
      },
      "powder_minus_mean_highbush_risk_diff_source_bootstrap95":
         list(map(float,np.percentile(contrasts,[2.5,97.5]))),
      "no_cross_source_file_independence_claim":True,
    }


def run(folder,boot=N_BOOTSTRAP):
    if np is None:
        raise RuntimeError("Source original flower numeric analysis requires numpy")
    if boot<100 or boot>9999:
        raise ValueError("Original flower source bootstrap count out of bounds")
    records,source=read_authentic(folder)
    original_cells,site_cells=all_source_cells(records)
    models={}
    boot_results={}
    for name,treated,baseline in COMPARISONS:
        model=_fit_source_logit(records,treated,baseline)
        models[name]=model
        boot_results[name]=_plant_label_bootstrap_risks(
            records,treated,baseline,boot)
    return {
       "analysis":"sch_original_2020_single_visit_tagged_flower_honeybee_holdout_v1",
       "original_paper_DOI":DOI,
       "original_zenodo_record_id":SOURCE_RECORD_ID,
       "original_archived_source":source,
       "n_original_source_experimental_programmes":1,
       "same_tagged_flower_visitor_and_binary_fruit_set":True,
       "source_readme_verified_visitor_codes":ORIGINAL_VISITOR_NAMES,
       "original_source_cultivar_by_visitor_raw_flower_rates":original_cells,
       "original_source_year_block_by_visitor_raw_flower_rates":site_cells,
       "year_block_plant_label_cluster_aware_source_contrasts":models,
       "original_plant_label_bootstrap_per_contrast":boot_results,
       "source_visitor_identity_not_randomized_independent_of_cultivar_or_site":True,
       "source_bagged_UP_control_may_have_nonzero_fruit":True,
       "same_study_multiple_visits_data_not_independent_programme_replication":True,
       "all_331_single_visitor_flower_IDs_also_in_multiple_visits_one_visit_records":True,
       "source_unvisited_controls_reused_with_multiple_visits_and_hand_pollination":True,
       "single_visit_taxon_subgroup_analysis_not_independent_external_validation":True,
       "crossfile_audit_required_before_synthesizing_any_validation_evidence":True,
       "no_compatible_pollen_load_germination_or_fertilization_measured":True,
       "source_fruit_outcome_not_viable_seed_or_descendant_fitness":True,
       "no_flower_trait_manipulation_or_SCH_conflict_loss_L":True,
       "critical_limits":[
          "one_original_published_programme_three_cultivars_not_three_independent_species_studies",
          "actual_visitor_taxon_fixed_honeybee_HB_but_source_site_and_cultivar_context_not_randomized",
          "source_Other_is_bumblebee_in_Blue_Rose_but_stingless_bee_in_Powder_Blue_Snowchaser",
          "bagged_unvisited_UP_controls_differ_procedurally_from_insect_visited_flowers",
          "source_same_flower_fruit_set_binary_does_not_measure_effective_pollinia_or_embryos",
          "source_site_year_and_plant_clusters_do_not_establish_independent_genets",
          "cluster_bootstrap_on_source_plant_label_may_underestimate_shared_site_heterogeneity",
          "source_visitor_species_And_floral_traits_not_independently_randomized",
          "three_exploratory_visitor_contrasts_without_confirmatory_familywise_control",
          "SCH_loss_L_requires_independently_causal_common_trait_function_optima",
       ],
       "status":"SOURCE_REAL_SINGLE_VISIT_VISITOR_IDENTITY_FLOWER_FATE_VALIDATED_OBSERVATIONAL_CAUSAL_LIMIT",
    }


def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument("--source",type=Path,
                   default=Path("artifacts/sch_original_blueberry_source"))
    a.add_argument("--out",type=Path,
                   default=Path("artifacts/sch_original_blueberry_source/single_visit_reanalysis.json"))
    a.add_argument("--boot",type=int,default=N_BOOTSTRAP)
    args=a.parse_args()
    result=run(args.source,args.boot)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",
                        encoding="utf-8")
    print("BEGIN_SCH_ORIGINAL_SINGLE_VISIT_BLUEBERRY_SOURCE")
    print(json.dumps({
      "source":result["original_archived_source"],
      "visitor_rates":result["original_source_cultivar_by_visitor_raw_flower_rates"],
      "modelled_effects":result["year_block_plant_label_cluster_aware_source_contrasts"],
      "plant_cluster_bootstrap":result["original_plant_label_bootstrap_per_contrast"],
      "status":result["status"],
    },sort_keys=True,indent=2,ensure_ascii=False))
    print("END_SCH_ORIGINAL_SINGLE_VISIT_BLUEBERRY_SOURCE")

if __name__=="__main__":
    main()

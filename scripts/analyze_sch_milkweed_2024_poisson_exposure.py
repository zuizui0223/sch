"""Count-link sensitivity for 2024 milkweed selection under unequal flower exposure.

The observed ten-flower pollinium sample is not the fruit initiation risk set
of the whole plant. This source-backed model tests whether the nominal
fruit-vs-insertion inflorescence-count gradient depends on total floral
exposure and using OLS instead of a count log link.

Official García et al. (2024), J Poll Ecol, DOI
10.26786/1920-7603(2024)758, published Appendix II 103 rows/102 ID labels,
SHA256 d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb.

This is an observational Poisson-mean model with cluster-robust sandwich
inference. Robust SE does not prove the log-link mean correctly specified;
results are a sensitivity and NOT a true pollen-to-fruit probability, a
randomized floral trait intervention or SCH conflict loss L.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

from scripts.analyze_sch_milkweed_2024_paired_stage import (
    raw_bytes,unpack_original,select_complete,normalize_design,TRAIT_CODES
)
from scripts.analyze_sch_milkweed_2024_flower_opportunity import (
    source_opportunity
)

DOI="10.26786/1920-7603(2024)758"
SOURCE_SHA256="d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb"
N_SOURCE_ROWS=103
N_PLANT_ID_LABELS=102
N_TRAITS=10
SAMPLED_FLOWERS=10


def original_block_design(X,fruit,insertion,total,offset_corrected,subset=None):
    """Two separate rate models estimated jointly, to preserve covariance."""
    import numpy as np
    if subset is None:
        subset=np.arange(X.shape[0])
    x=X[subset]
    n=len(subset)
    p=x.shape[1]
    model=np.zeros((2*n,2*p),float)
    model[:n,:p]=x
    model[n:,p:]=x
    y=np.concatenate([fruit[subset],insertion[subset]])
    if offset_corrected:
        expo=np.concatenate([total[subset],np.full(n,SAMPLED_FLOWERS)])
    else:
        expo=np.ones(2*n)
    offset=np.log(expo)
    return model,y,offset


def fit_stacked_model(X,fruits,insertions,total,labels,offset_corrected=True,keep=None):
    import numpy as np
    import statsmodels.api as sm
    from scipy.stats import chi2
    if keep is None:
        keep=np.arange(X.shape[0])
    model,y,offset=original_block_design(
        X,fruits,insertions,total,offset_corrected,keep)
    group=np.asarray(labels,dtype=str)[keep]
    cluster_groups=np.concatenate([group,group])
    if len(set(cluster_groups))<95:
        raise ValueError("Too few source plant label blocks for robust model")
    fit=sm.GLM(y,model,offset=offset,
               family=sm.families.Poisson()).fit(
                   maxiter=300,cov_type="cluster",
                   cov_kwds={"groups":cluster_groups})
    if not fit.converged or not np.all(np.isfinite(fit.params)):
        raise ValueError("Original count link failed to converge")
    cov=np.asarray(fit.cov_params(),float)
    param=np.asarray(fit.params,float)
    p=X.shape[1]
    N=len(keep)
    L=np.zeros((p-1,2*p),float)
    for j in range(1,p):
        L[j-1,j]=1
        L[j-1,p+j]=-1
    effects=L@param
    diff_cov=L@cov@L.T
    if np.linalg.matrix_rank(diff_cov)!=p-1:
        raise ValueError("Original 10-trait stage difference covariance singular")
    test=float(effects@np.linalg.solve(diff_cov,effects))
    global_p=float(chi2.sf(test,p-1))
    fitted=np.asarray(fit.fittedvalues,float)
    if len(fitted)!=2*N or np.any(fitted<=0):
        raise ValueError("Original Poisson model invalid fitted means")
    # Diagnostics: robust SE guards variance heterogeneity; mean model
    # remains Poisson and highly zero-heavy outcomes may challenge fit.
    overdisp_fruit=float(np.sum((fruits[keep]-fitted[:N])**2/fitted[:N])/max(N-p,1))
    overdisp_insert=float(np.sum((insertions[keep]-fitted[N:])**2/fitted[N:])/max(N-p,1))
    from scipy.stats import norm
    result=[]
    for j,name in enumerate(TRAIT_CODES,start=1):
        se=math.sqrt(max(0,float(diff_cov[j-1,j-1])))
        if se<=0:raise ValueError("No robust source SE for stage contrast")
        slopeF=float(param[j])
        slopeI=float(param[p+j])
        result.append({
          "trait":name,
          "log_fruit_count_per_peak_flower_slope" if offset_corrected else "log_fruit_count_slope":slopeF,
          "log_insertion_per_ten_flower_slope" if offset_corrected else "log_insertion_count_slope":slopeI,
          "fruit_minus_insertion_log_slope":float(effects[j-1]),
          "cluster_robust_se":se,
          "cluster_robust_normal_p":float(2*norm.sf(abs(effects[j-1]/se))),
          "cluster_robust_95_normal_interval":[float(effects[j-1]-1.96*se),
                                              float(effects[j-1]+1.96*se)],
        })
    return {
      "n_source_rows_per_fitness_stage":N,
      "n_independent_original_plant_label_groups":len(set(group)),
      "offset_corrected_to_observed_flower_opportunity":offset_corrected,
      "n_parameters":int(param.size),
      "likelihood_family":"Poisson_log_mean",
      "inference":"source_plant_label_cluster_robust_sandwich",
      "n_original_trait_axes":p-1,
      "joint_ten_trait_stage_Wald_chi2":test,
      "joint_ten_trait_stage_Wald_chi2_df":p-1,
      "joint_ten_trait_stage_approx_P":global_p,
      "fruit_count_Pearson_overdispersion_diagnostic":overdisp_fruit,
      "insertion_count_Pearson_overdispersion_diagnostic":overdisp_insert,
      "n_ten_trait_Bonferroni_P_below_0_005":sum(
          x["cluster_robust_normal_p"]<.005 for x in result),
      "trait_effects":result,
    }


def run_original(records):
    import numpy as np
    rows,ids,missing,fields=select_complete(records)
    X,Y,_,_,_=normalize_design(rows)
    total,opps,diagnostics=source_opportunity(records)
    if len(ids)!=N_SOURCE_ROWS or len(set(ids))!=N_PLANT_ID_LABELS:
        raise ValueError("Original 103 rows / 102 IDs changed")
    fruits=opps[:,5];insertions=opps[:,6]
    if len(fruits)!=len(rows) or np.any(fruits!=np.floor(fruits)) or np.any(insertions!=np.floor(insertions)):
        raise ValueError("Published fitness count endpoints noninteger or misaligned")
    idx68=[i for i,pid in enumerate(ids) if pid=="68"]
    if len(idx68)!=2:raise ValueError("Original ID 68 ambiguity was altered")
    adjusted=fit_stacked_model(X,fruits,insertions,total,ids,True)
    unadjusted=fit_stacked_model(X,fruits,insertions,total,ids,False)
    sensitivity=[]
    for drop in idx68:
        kept=np.asarray([i for i in range(len(ids)) if i!=drop])
        m=fit_stacked_model(X,fruits,insertions,total,ids,True,keep=kept)
        focal=m["trait_effects"][0]
        sensitivity.append({
          "excluded_original_source_row_zero_index":drop,
          "n_source_rows":len(kept),
          "n_original_distinct_ID_labels":m["n_independent_original_plant_label_groups"],
          "count_rate_inflorescence_number_delta":focal["fruit_minus_insertion_log_slope"],
          "count_rate_inflorescence_number_P":focal["cluster_robust_normal_p"],
        })
    return {
      "analysis":"sch_milkweed2024_original_poisson_clustered_flower_exposure_v1",
      "source_original_paper_DOI":DOI,
      "source_original_appendix_sha256":SOURCE_SHA256,
      "n_source_rows":len(records),
      "n_distinct_plant_labels":len(set(ids)),
      "n_original_duplicate_ID68_source_records":len(idx68),
      "source_observed_flower_opportunity_quality":diagnostics,
      "original_2024_103row_unadjusted_poisson_count_comparison":unadjusted,
      "original_2024_103row_exposure_offset_poisson_rate_comparison":adjusted,
      "source_duplicate_ID68_exclusion_sensitivity":sensitivity,
      "original_2024_trial_risk_sets_aligned":False,
      "data_are_103_observational_stems_not_random_trait_assignments":True,
      "fruit_offset_log_peak_flower_proxy_not_tracked_fruit_fate":True,
      "ten_flower_pollinia_offset_constant":True,
      "count_model_overdispersion_protected_by_cluster_robust_se":True,
      "log_mean_model_misspecification_not_ruled_out":True,
      "no_pollen_to_fruit_conversion_probability_estimated":True,
      "source_original_author_fitted_count_model":False,
      "no_pure_function_optima_or_SCH_L":True,
      "status":"REAL_2024_PAIRED_POISSON_EXPOSURE_RATE_SENSITIVITY_ONLY",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path)
    p.add_argument("--output",type=Path,
                   default=Path("artifacts/sch_milkweed_2024_count_rate_v1.json"))
    args=p.parse_args()
    raw,url=raw_bytes(args.source)
    records,headers=unpack_original(raw)
    result=run_original(records)
    result["original_download_source_url"]=url
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("BEGIN_SCH_MILKWEED_ORIGINAL_COUNT_RATE")
    print(json.dumps({
       "source_n_rows":result["n_source_rows"],
       "source_n_distinct_labels":result["n_distinct_plant_labels"],
       "unadjusted":result["original_2024_103row_unadjusted_poisson_count_comparison"],
       "exposure_normalized":result["original_2024_103row_exposure_offset_poisson_rate_comparison"],
       "duplicate_sensitivity":result["source_duplicate_ID68_exclusion_sensitivity"],
       "status":result["status"]},indent=2,sort_keys=True,ensure_ascii=False))
    print("END_SCH_MILKWEED_ORIGINAL_COUNT_RATE")


if __name__=="__main__":
    main()

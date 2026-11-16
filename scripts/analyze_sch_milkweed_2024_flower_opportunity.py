"""Audit denominator mismatch in genuine 2024 Asclepias plant-stage selection.

Question: Does stronger selection on inflorescence number for fruit *counts*
than for insertions from a fixed 10-flower sample persist after accounting for
the total number of flowers at peak bloom?  This is a source-backed
exposure-standardization SENSITIVITY, not a causal postpollination probability.

Source original DOI 10.26786/1920-7603(2024)758, official Appendix II
SHA256 d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb.
"""
from __future__ import annotations
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path

from scripts.analyze_sch_milkweed_2024_paired_stage import (
    raw_bytes,unpack_original,select_complete,normalize_design,
    fit_ols_hc3,number_or_none,TRAIT_CODES,OUTCOMES,SOURCE_SHA256
)

try:
    import numpy as np
except ModuleNotFoundError:
    np=None

SEED=20261116
BOOT=1999
EXPECTED_SOURCE_N=103
EXPECTED_DISTINCT_IDS=102


def normal_p(beta,se):
    return math.erfc(abs(float(beta/se))/math.sqrt(2)) if se>0 else None


def source_opportunity(records):
    needed=("flwrs","buds","tot.flws","inflor.nu","inflor.size","fruit.init","insertions_t")
    matrix=[]
    for r in records:
        nums=[number_or_none(r.get(k)) for k in needed]
        if any(v is None for v in nums):
            raise ValueError("Published total flower opportunity columns incomplete")
        matrix.append(nums)
    arr=np.asarray(matrix,float)
    if arr.shape!=(103,len(needed)) or not np.isfinite(arr).all():
        raise ValueError("Original flower count source row shape or values drift")
    opened,buds,total,ninf,size,fruits,insertion=arr.T
    if np.any(total<=0) or np.any(ninf<=0) or np.any(size<=0):
        raise ValueError("Cannot normalize by nonpositive floral opportunities")
    if np.any(fruits<0) or np.any(insertion<0):
        raise ValueError("Original reproductive outcomes must be nonnegative")
    residual=total-(opened+buds)
    ratio_residual=size-total/ninf
    diagnostics={
      "source_total_flowers_measured_at_peak_flowering":True,
      "original_exposure_columns":list(needed),
      "n_total_flower_measurements":len(total),
      "total_flower_count_min":float(total.min()),
      "total_flower_count_median":float(np.median(total)),
      "total_flower_count_max":float(total.max()),
      "number_open_flower_min":float(opened.min()),
      "total_flowers_minus_open_plus_buds_abs_max":float(np.abs(residual).max()),
      "inflorescence_size_minus_total_per_inflorescence_abs_max":float(np.abs(ratio_residual).max()),
      "n_fruits_greater_than_measured_total_flower_count":int(np.sum(fruits>total)),
      "n_fruits_zero":int(np.sum(fruits==0)),
      "n_insertions_zero":int(np.sum(insertion==0)),
      "n_positive_fruits":int(np.sum(fruits>0)),
      "fruit_init_count_mean":float(fruits.mean()),
      "fruit_init_count_variance_sample":float(fruits.var(ddof=1)),
      "flower_denominator_is_approximate_peak_count_not_tracked_flowers":True,
      "pollinia_insertions_have_fixed_ten_sampled_flowers":True,
      "no_per_pollinium_or_per_flower_conversion_rate_estimated":True,
    }
    # These two algebraic checks certify column definitions. If the archive
    # differs, stop rather than redefine flower opportunity after seeing results.
    if diagnostics["total_flowers_minus_open_plus_buds_abs_max"]>1e-8:
        raise ValueError("Original peak flower definition is not opened+buds")
    if diagnostics["inflorescence_size_minus_total_per_inflorescence_abs_max"]>0.015:
        raise ValueError("Source inflorescence size no longer total/ninf within publication rounding")
    return total,arr,diagnostics


def collect_models(records,boot=BOOT):
    if np is None:
        raise RuntimeError("numpy is required only by source-backed numerical analysis")
    if boot<100 or boot>9999:
        raise ValueError("Bootstrap count outside bounded reproducibility range")
    matrix,ids,missing,fields=select_complete(records)
    if len(records)!=103 or len(ids)!=103 or len(set(ids))!=102:
        raise ValueError("The 103-row/102-source-plant-ID cohort has changed")
    X,Y,mu,sd,means=normalize_design(matrix)
    total,opps,check=source_opportunity(records)
    if X.shape!=(103,11) or Y.shape!=(103,3):
        raise ValueError("Original 10 predictor/3 outcome shape changed")
    # Original published count-based selection, reference signal PR #252.
    raw_delta=Y[:,0]-Y[:,1]
    beta_raw,se_raw,cov_raw,_=fit_ols_hc3(X,raw_delta)
    if abs(float(beta_raw[1])-.48358370490138486)>1e-7:
        raise ValueError("Previous source PR #252 baseline effect not reproduced")
    # Descriptive per-flower opportunity rather than whole-plant fruit number.
    # The observed flower count is itself the focal display phenotype's output.
    # It is NOT an actual flower-level fruit-conversion probability.
    rate=opps[:,5]/total
    if rate.mean()<=0:raise ValueError("Zero fruit initiation per flower opportunity")
    relative_fruit_rate=rate/rate.mean()
    # Ten-flower insertion sampling offset is constant; relative insertion
    # count and insertion rate have exactly the same normalized regression.
    relative_ten_flower_insertions=opps[:,6]/opps[:,6].mean()
    rate_delta=relative_fruit_rate-relative_ten_flower_insertions
    beta_rate,se_rate,cov_rate,_=fit_ols_hc3(X,rate_delta)
    rate_fruit_beta,_,_,_=fit_ols_hc3(X,relative_fruit_rate)
    insert_beta,_,_,_=fit_ols_hc3(X,relative_ten_flower_insertions)
    # Alternative conditioning on log flower opportunities (NOT intervention).
    logtotal=np.log(total)
    logtotal_std=(logtotal-logtotal.mean())/logtotal.std(ddof=1)
    Xplus=np.column_stack((X,logtotal_std))
    if np.linalg.matrix_rank(Xplus)!=12:
        raise ValueError("Log flower opportunity adds no independent linear degree of freedom")
    bet_plus,se_plus,_,_=fit_ols_hc3(Xplus,raw_delta)
    fruit_plus,_,_,_=fit_ols_hc3(Xplus,Y[:,0])
    # Common original 102 label blocks; no duplication fixed by fiat.
    group=defaultdict(list)
    for i,pid in enumerate(ids):group[pid].append(i)
    names=sorted(group)
    if len(names)!=102 or len(group["68"])!=2:
        raise ValueError("Source individual labels or duplicated ID68 changed")
    rng=np.random.default_rng(SEED)
    boots_raw=[];boots_rate=[];boots_plus=[]
    for _ in range(boot):
        labels=rng.integers(0,len(names),size=len(names))
        ix=np.asarray([row for j in labels for row in group[names[j]]],int)
        Xb,Xpb=X[ix],Xplus[ix]
        if np.linalg.matrix_rank(Xb)<11 or np.linalg.matrix_rank(Xpb)<12:
            continue
        boots_raw.append(np.linalg.lstsq(Xb,raw_delta[ix],rcond=None)[0])
        boots_rate.append(np.linalg.lstsq(Xb,rate_delta[ix],rcond=None)[0])
        boots_plus.append(np.linalg.lstsq(Xpb,raw_delta[ix],rcond=None)[0])
    if len(boots_rate)<.8*boot:
        raise ValueError("Too few plant-label bootstrap draws")
    ci_raw=np.percentile(np.asarray(boots_raw),[2.5,97.5],axis=0)
    ci_rate=np.percentile(np.asarray(boots_rate),[2.5,97.5],axis=0)
    ci_plus=np.percentile(np.asarray(boots_plus),[2.5,97.5],axis=0)

    dup_idx=group["68"]
    duplicate_sensitivity=[]
    for drop in dup_idx:
        keep=np.ones(len(ids),bool);keep[drop]=False
        beta101=np.linalg.lstsq(X[keep],rate_delta[keep],rcond=None)[0]
        beta_plus101=np.linalg.lstsq(Xplus[keep],raw_delta[keep],rcond=None)[0]
        duplicate_sensitivity.append({
          "source_zero_index_dropped":int(drop),
          "n_source_rows_after_drop":int(keep.sum()),
          "rate_delta_inflorescence_number":float(beta101[1]),
          "logflower_adjusted_raw_delta_inflorescence_number":float(beta_plus101[1]),
        })
    effects=[]
    for j,name in enumerate(TRAIT_CODES,start=1):
        effects.append({
          "trait":name,
          "source_original_trait":TRAIT_CODES[name],
          "raw_count_based_paired_delta":float(beta_raw[j]),
          "raw_count_based_paired_hc3_se":float(se_raw[j]),
          "raw_count_based_paired_p_nominal":normal_p(beta_raw[j],se_raw[j]),
          "raw_count_based_bootstrap95":[float(ci_raw[0,j]),float(ci_raw[1,j])],
          "fruit_per_peak_flower_proxy_beta":float(rate_fruit_beta[j]),
          "ten_flower_pollinia_insertion_beta":float(insert_beta[j]),
          "opportunity_normalized_paired_delta":float(beta_rate[j]),
          "opportunity_normalized_paired_hc3_se":float(se_rate[j]),
          "opportunity_normalized_paired_p_nominal":normal_p(beta_rate[j],se_rate[j]),
          "opportunity_normalized_plant_label_bootstrap95":[float(ci_rate[0,j]),float(ci_rate[1,j])],
          "logtotal_conditioned_original_paired_delta":float(bet_plus[j]),
          "logtotal_conditioned_paired_hc3_se":float(se_plus[j]),
          "logtotal_conditioned_bootstrap95":[float(ci_plus[0,j]),float(ci_plus[1,j])],
        })
    def fwer(effects,key):
        return int(sum(e[key] is not None and e[key]<.005 for e in effects))
    e=effects[0]
    # Intentionally no expected direction imposed: opposite outcomes
    # are allowed if the purported exposure artifact is not supported.
    return {
      "analysis":"sch_milkweed_2024_flower_opportunity_denominator_sensitivity_v1",
      "original_source_doi":"10.26786/1920-7603(2024)758",
      "original_source_SHA256":"d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb",
      "n_original_published_rows":len(records),
      "n_distinct_source_plant_labels":len(names),
      "n_original_plant_label_duplicate_groups":1,
      "n_successful_plant_label_bootstrap":len(boots_rate),
      "original_source_flower_opportunity_diagnostics":check,
      "original_ten_floral_traits":list(TRAIT_CODES),
      "published_selection_original_raw_inflorescence_delta":float(beta_raw[1]),
      "source_sample_ten_flower_insertion_offset_constant":10,
      "source_total_flower_opportunity_proxy_exposure_adjusted":True,
      "unadjusted_count_based_paired_stage_contrast_per_trait":effects,
      "n_traits_familywise_passed_raw_count_comparison":fwer(effects,"raw_count_based_paired_p_nominal"),
      "n_traits_familywise_passed_per_peak_flower_proxy_comparison":fwer(effects,"opportunity_normalized_paired_p_nominal"),
      "posthoc_bonferroni_10_traits_alpha":.005,
      "correlation_fruit_count_vs_total_peak_flower_count":float(np.corrcoef(opps[:,5],total)[0,1]),
      "correlation_insertion_count_vs_total_peak_flower_count":float(np.corrcoef(opps[:,6],total)[0,1]),
      "correlation_inflorescence_number_vs_total_peak_flower_count":float(np.corrcoef(matrix[:,0],total)[0,1]),
      "fixed_design_condition_number":float(np.linalg.cond(X)),
      "augmented_design_condition_number":float(np.linalg.cond(Xplus)),
      "source_logflower_adjusted_delta_inflorescence_number":float(bet_plus[1]),
      "source_logflower_adjusted_delta_inflorescence_number_HC3_se":float(se_plus[1]),
      "source_logflower_adjusted_delta_inflorescence_number_bootstrap95":[float(ci_plus[0,1]),float(ci_plus[1,1])],
      "source_duplicate_ID68_row_exclusion_sensitivities":duplicate_sensitivity,
      "source_fruit_per_peak_flower_is_not_fruit_per_pollinium":True,
      "flower_opportunity_is_post_trait_display_mediator_not_randomized":True,
      "no_causal_stage_conversion_rate":True,
      "no_pure_function_optima_or_SCH_L":True,
      "status":"REAL_ORIGINAL_103_ROW_OPPORTUNITY_DENOMINATOR_SENSITIVITY_NOT_CAUSAL_CONVERSION",
      "interpretation_limits":[
        "fruit_init_whole_plant_vs_ten_flower_pollinia_insertion_differ_in_risk_set",
        "total_flws_is_peak_open_plus_buds_proxy_not_exact_seasonal_cumulative_flowers",
        "inflorescence_size_algebraically_derived_from_total_flws_per_inflorescence",
        "conditioning_on_total_flowers_changes_estimand_and_can_remove_display_mediated_effect",
        "fruit_per_peak_flower_is_not_same_floral_fate_compatible_pollinia_conversion",
        "one_field_population_103_original_rows_but_102_distinct_ID_labels",
        "paired_bootstrap_groups_duplicate_ID68_without_silent_source_repair",
        "ten_traits_not_independent_hypotheses_statistical_multiplicity_posthoc",
        "observational_trait_regression_not_randomized_phenotypic_manipulation",
        "source_fit_count_outcomes_have_zero_inflation_overdispersion_possible",
        "no_genetic_interactions_or_SCH_fitness_compromise_L_identified",
      ],
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source",type=Path)
    ap.add_argument("--output",type=Path,
                    default=Path("artifacts/sch_milkweed_2024_flower_denominator_v1.json"))
    ap.add_argument("--boot",type=int,default=BOOT)
    args=ap.parse_args()
    raw,url=raw_bytes(args.source)
    records,cols=unpack_original(raw)
    result=collect_models(records,args.boot)
    result["verified_original_download_source_url"]=url
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print("BEGIN_SCH_SOURCE_FLOWER_DENOMINATOR")
    print(json.dumps({
        "source_original_published_rows":result["n_original_published_rows"],
        "source_original_distinct_IDs":result["n_distinct_source_plant_labels"],
        "source_opportunity_diagnostics":result["original_source_flower_opportunity_diagnostics"],
        "n_bootstrap":result["n_successful_plant_label_bootstrap"],
        "original_source_correlation_fruits_total_flowers":result["correlation_fruit_count_vs_total_peak_flower_count"],
        "original_source_correlation_insertions_total_flowers":result["correlation_insertion_count_vs_total_peak_flower_count"],
        "ten_original_trait_effects":result["unadjusted_count_based_paired_stage_contrast_per_trait"],
        "source_logflowers_adjusted_inflorescence_count_delta":result["source_logflower_adjusted_delta_inflorescence_number"],
        "source_logflowers_adjusted_bootstrap95":result["source_logflower_adjusted_delta_inflorescence_number_bootstrap95"],
        "source_duplicate_ID68_sensitivities":result["source_duplicate_ID68_row_exclusion_sensitivities"],
        "status":result["status"],
    },sort_keys=True,indent=2,ensure_ascii=False))
    print("END_SCH_SOURCE_FLOWER_DENOMINATOR")


if __name__=="__main__":
    main()

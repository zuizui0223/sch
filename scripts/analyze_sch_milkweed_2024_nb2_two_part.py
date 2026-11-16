"""Authentic 2024 milkweed negative-binomial and two-part count sensitivity.

Scientific aim: after equalizing observed opportunities, is the apparent
inflorescence-number female-stage coefficient difference an artifact of
Poisson variance assumptions or zero-initiated-fruit stems?

Three distinct descriptive estimands (NOT a causal conversion probability):
1. Paired two-outcome NB2 working-mean rate regressions, with source-specific
   overdispersion alpha from Poisson source residual moments. Joint sandwich
   covariance preserves correlation between the two outcome stages for the
   SAME 102 source-plant labels; 103 original published rows.
2. Probability of >=1 initiated fruit, unconditional and conditioning on
   observed total peak flowers (logistic regression). No per-flower Bernoulli
   trial is assumed; log-flowers is a phenotype-linked covariate.
3. Fruit count among fruit-positive source stems, fitted as a descriptive
   conditional NB2 working mean with peak-flower offset. This is NOT a
   formally specified zero-truncated NB hurdle likelihood.

Do not interpret a resulting association as conditional fertilization,
self-compatibility, genetic selection, or SCH loss L.
Source: García et al. 2024 J Poll Ecol 10.26786/1920-7603(2024)758.
Original XLSX publisher galley 478 exact SHA256 is validated by
scripts.analyze_sch_milkweed_2024_paired_stage.raw_bytes().
"""
from __future__ import annotations

import argparse
import json
import math
import warnings
from collections import defaultdict
from pathlib import Path

from scripts.analyze_sch_milkweed_2024_paired_stage import (
    raw_bytes,unpack_original,select_complete,normalize_design,TRAIT_CODES
)
from scripts.analyze_sch_milkweed_2024_flower_opportunity import source_opportunity
from scripts.analyze_sch_milkweed_2024_poisson_exposure import fit_stacked_model

DOI="10.26786/1920-7603(2024)758"
SOURCE_SHA256="d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb"
N=103
N_LABELS=102
N_TRAITS=10
SEED=20261117
BOOT=499
ALPHA_GRID=(0.25,0.5,1.0,2.0)

def _fit_nb_stage(y,X,offset,alpha):
    import statsmodels.api as sm
    import numpy as np
    if not 0<alpha<=10:
        raise ValueError("invalid NB2 working dispersion")
    result=sm.GLM(y,X,offset=offset,
                  family=sm.families.NegativeBinomial(alpha=alpha)).fit(
                      maxiter=300,disp=0)
    if not result.converged:
        raise ValueError("source NB2 stage-mean fit did not converge")
    beta=np.asarray(result.params,float)
    mu=np.asarray(result.fittedvalues,float)
    if not (np.isfinite(beta).all() and np.isfinite(mu).all() and (mu>0).all()):
        raise ValueError("invalid source count-link fitted mean")
    return beta,mu

def _moment_alpha(y,X,offset):
    """Pre-specified moment alpha from original Poisson fitted residuals."""
    import numpy as np
    import statsmodels.api as sm
    fit=sm.GLM(y,X,offset=offset,
               family=sm.families.Poisson()).fit(maxiter=300)
    mu=np.asarray(fit.fittedvalues,float)
    value=float(np.sum((y-mu)**2-y)/np.sum(mu**2))
    if not math.isfinite(value):
        raise ValueError("nonfinite source NB moment dispersion")
    return float(max(.05,min(5,value))),value

def _nb_score_bread(y,X,mu,alpha):
    import numpy as np
    score=X*((y-mu)/(1+alpha*mu))[:,None]
    weights=mu/(1+alpha*mu)
    bread=X.T@(X*weights[:,None])
    return score,bread

def _fit_joint_nb(X,F,I,T,plant_labels,alpha_f,alpha_i,keep=None):
    """Block-diagonal NB2 working means with joint ID-cluster score meat."""
    import numpy as np
    from scipy.stats import chi2,norm
    if keep is None:
        keep=np.arange(X.shape[0])
    x=X[keep,:]
    yF=np.asarray(F[keep],float)
    yI=np.asarray(I[keep],float)
    t=np.asarray(T[keep],float)
    labels=np.asarray(plant_labels,dtype=str)[keep]
    G=len(set(labels))
    if G<90:raise ValueError("too few independent original plant-ID labels")
    p=x.shape[1]
    bF,muF=_fit_nb_stage(yF,x,np.log(t),alpha_f)
    bI,muI=_fit_nb_stage(yI,x,np.full(len(x),math.log(10)),alpha_i)
    scoreF,breadF=_nb_score_bread(yF,x,muF,alpha_f)
    scoreI,breadI=_nb_score_bread(yI,x,muI,alpha_i)
    bread=np.zeros((2*p,2*p),float)
    bread[:p,:p]=breadF
    bread[p:,p:]=breadI
    if np.linalg.matrix_rank(bread)!=2*p:
        raise ValueError("stage NB2 bread singular")
    # One joint cluster score for BOTH endpoints on the same plant.
    block=defaultdict(lambda:np.zeros(2*p,float))
    for i,pid in enumerate(labels):
        block[pid][:p]+=scoreF[i]
        block[pid][p:]+=scoreI[i]
    sc=np.asarray(list(block.values()),float)
    bInv=np.linalg.inv(bread)
    # Asymptotic cluster sandwich, source label is the sampling unit.
    cov=bInv@(sc.T@sc)@bInv
    cov*= (G/(G-1))*((2*len(x)-1)/(2*len(x)-2*p))
    L=np.zeros((p-1,2*p),float)
    for j in range(1,p):
        L[j-1,j]=1
        L[j-1,p+j]=-1
    b=np.concatenate([bF,bI])
    delta=L@b
    V=L@cov@L.T
    if np.linalg.matrix_rank(V)!=p-1 or not np.isfinite(V).all():
        raise ValueError("stage NB2 joint robust contrast covariance singular")
    wald=float(delta@np.linalg.solve(V,delta))
    p_global=float(chi2.sf(wald,p-1))
    effects=[]
    for j,trait in enumerate(TRAIT_CODES):
        se=math.sqrt(max(0,float(V[j,j])))
        if se<=0:raise ValueError("source joint NB2 contrast SE nonpositive")
        z=float(delta[j]/se)
        effects.append({
          "trait":trait,
          "log_fruit_rate_beta":float(bF[j+1]),
          "log_insertion_tenflower_rate_beta":float(bI[j+1]),
          "fruit_minus_insertion_log_rate_beta":float(delta[j]),
          "joint_plant_label_cluster_sandwich_se":se,
          "nominal_two_sided_normal_p":float(2*norm.sf(abs(z))),
          "nominal_95_interval":[float(delta[j]-1.96*se),
                                 float(delta[j]+1.96*se)],
        })
    return {
      "source_rows":len(x),
      "source_plant_label_groups":G,
      "nb2_alpha_fruit_fixed":float(alpha_f),
      "nb2_alpha_insertions_fixed":float(alpha_i),
      "two_stage_gradient_joint_Wald_chi2":wald,
      "two_stage_gradient_joint_Wald_df":p-1,
      "two_stage_gradient_joint_asymptotic_p":p_global,
      "n_ten_trait_exploratory_Bonferroni_p_below_0_005":sum(
        x["nominal_two_sided_normal_p"]<.005 for x in effects),
      "trait_effects":effects,
      "inference":"joint_two_stage_cluster_sandwich_meat_summed_by_source_plant_label",
      "model":"NB2_quasi_likelihood_fixed_alpha_two_separate_working_means",
    }

def _binary_fruit_part(X,F,T,labels):
    import numpy as np
    import statsmodels.api as sm
    from scipy.stats import norm
    indicator=(F>0).astype(float)
    logT=np.log(T)
    normalized=(logT-logT.mean())/logT.std(ddof=1)
    models={}
    for name,Z in (
        ("any_fruit_unadjusted_display",X),
        ("any_fruit_conditioned_on_log_peak_flowers",
         np.column_stack([X,normalized]))):
        if np.linalg.matrix_rank(Z)!=Z.shape[1]:
            raise ValueError("binary fruit display design singular")
        fit=sm.GLM(indicator,Z,family=sm.families.Binomial()).fit(
            maxiter=300,cov_type="cluster",
            cov_kwds={"groups":labels})
        if not fit.converged:
            raise ValueError("fruit positive logistic model did not converge")
        b=float(fit.params[1])
        se=float(fit.bse[1])
        if not (math.isfinite(b) and math.isfinite(se) and se>0):
            raise ValueError("fruit positive coefficient invalid")
        models[name]={
          "log_odds_inflorescence_count_beta":b,
          "source_ID_cluster_SE":se,
          "nominal_p":float(2*norm.sf(abs(b/se))),
          "inflorescence_coefficient_95_interval":[b-1.96*se,b+1.96*se],
          "n_rows":len(indicator),
          "n_fruit_positive":int(indicator.sum()),
          "n_fruit_zero":int(len(indicator)-indicator.sum()),
          "n_source_plant_labels":len(set(labels)),
          "log_total_peak_flower_count_in_conditioning_set":name.endswith("flowers"),
          "biological_interpretation":"association_with_any_whole_stem_fruit_not_conditional_fertilization",
        }
    return models

def _conditional_positive_count_part(X,F,T,labels,alpha):
    """Two working conditional means on F>0; NOT a true NB hurdle likelihood."""
    import numpy as np
    import statsmodels.api as sm
    from scipy.stats import norm
    keep=np.asarray(F>0)
    p=int(keep.sum())
    if p<50:raise ValueError("too few source fruit-positive stems")
    z=X[keep];y=F[keep]
    group=np.asarray(labels,dtype=str)[keep]
    stage={}
    for name,off in (
         ("fruit_positive_whole_plant_count",np.zeros(p)),
         ("fruit_positive_per_peak_flower_count",np.log(T[keep]))):
        fit=sm.GLM(y,z,offset=off,
                   family=sm.families.NegativeBinomial(alpha=alpha)).fit(
                       maxiter=300,cov_type="cluster",
                       cov_kwds={"groups":group})
        if not fit.converged:
            raise ValueError("positive source NB working mean did not converge")
        b=float(fit.params[1]);se=float(fit.bse[1])
        if not(math.isfinite(b) and math.isfinite(se) and se>0):
            raise ValueError("conditional positive fruit count effect invalid")
        stage[name]={
            "inflorescence_number_beta":b,
            "source_ID_cluster_SE":se,
            "nominal_two_sided_normal_P":float(2*norm.sf(abs(b/se))),
            "nominal_95_interval":[b-1.96*se,b+1.96*se],
            "model_exposure":("log_peak_open_plus_buds_offset" if np.any(off) else "whole_plant_count"),
            "n_observations":p,
            "n_source_plant_labels":len(set(group)),
        }
    grid=[]
    for alternative in ALPHA_GRID:
        fit=sm.GLM(y,z,offset=np.log(T[keep]),
                family=sm.families.NegativeBinomial(alpha=alternative)).fit(
                    maxiter=300,cov_type="cluster",
                    cov_kwds={"groups":group})
        if not fit.converged:raise ValueError("source subset alpha grid did not converge")
        b=float(fit.params[1]);se=float(fit.bse[1])
        grid.append({
            "alpha_fixed":alternative,
            "per_peak_flower_focal_beta":b,
            "cluster_robust_normal_P":float(2*norm.sf(abs(b/se))),
        })
    return {
      "n_fruit_positive_stems":p,
      "n_positive_source_plant_labels":len(set(group)),
      "working_NB2_alpha_full_source_fixed":alpha,
      "two_outcome_definitions":stage,
      "per_peak_flower_fixed_alpha_grid":grid,
      "not_a_correctly_normalized_zero_truncated_NB_likelihood":True,
      "selection_on_F_greater_than_zero_can_induce_collider_bias":True,
      "plot_or_estimate_as_proof_of_allocation_tradeoff":False,
      "interpretation":"positive_stem_conditional_mean_with_and_without_flower_opportunity_proxy",
    }


def _focal_bootstrap(X,F,I,T,labels,af,ai,n_boot=BOOT):
    import numpy as np
    grouped=defaultdict(list)
    for i,pid in enumerate(labels):grouped[str(pid)].append(i)
    names=sorted(grouped)
    if len(names)!=N_LABELS or grouped["68"] is None or len(grouped["68"])!=2:
        raise ValueError("Original source ID68 duplicate grain changed")
    rng=np.random.default_rng(SEED)
    differences=[];failures=0
    for i in range(n_boot):
        selected=rng.integers(0,len(names),len(names))
        index=np.asarray([j for k in selected for j in grouped[names[k]]],int)
        z=X[index,:]
        if np.linalg.matrix_rank(z)!=z.shape[1]:
            failures+=1
            continue
        try:
            bF,_=_fit_nb_stage(F[index],z,np.log(T[index]),af)
            bI,_=_fit_nb_stage(I[index],z,np.full(len(index),math.log(10)),ai)
            diff=float(bF[1]-bI[1])
            if math.isfinite(diff):differences.append(diff)
            else:failures+=1
        except (ValueError,RuntimeError):
            failures+=1
    if len(differences)<.8*n_boot:
        raise ValueError("too few original paired NB bootstraps")
    ci=np.percentile(differences,[2.5,97.5])
    return {
      "n_requested":n_boot,"n_completed":len(differences),
      "n_failed_or_singular":failures,
      "ID_label_resampling_includes_ID68_together":True,
      "source_focal_log_rate_difference_bootstrap95":[float(ci[0]),float(ci[1])],
      "percentile_excludes_zero":bool(ci[0]>0 or ci[1]<0),
    }

def run(records,boot=BOOT):
    import numpy as np
    rows,ids,missing,cols=select_complete(records)
    X,Y,_,_,_=normalize_design(rows)
    total,original,source_diag=source_opportunity(records)
    F=original[:,5];I=original[:,6]
    if (len(records)!=N or len(ids)!=N or len(set(ids))!=N_LABELS or
        sum(i=="68" for i in ids)!=2 or len(np.unique(X[:,1:]))<2):
        raise ValueError("Original 103 source rows 102 plant IDs not retained")
    if not(np.isfinite(F).all() and np.isfinite(I).all() and
           np.all(F>=0) and np.all(I>=0)):
        raise ValueError("source count variables invalid")
    if np.any(F!=np.floor(F)) or np.any(I!=np.floor(I)):
        raise ValueError("source observed fitness counts noninteger")
    offsetF=np.log(total);offsetI=np.full(N,math.log(10))
    af,momentF=_moment_alpha(F,X,offsetF)
    ai,momentI=_moment_alpha(I,X,offsetI)
    fitted=_fit_joint_nb(X,F,I,total,ids,af,ai)
    grid=[]
    for alpha in ALPHA_GRID:
        test=_fit_joint_nb(X,F,I,total,ids,alpha,alpha)
        grid.append({
          "common_predeclared_NB2_alpha":alpha,
          "focal_inflorescence_count_log_rate_delta":
              test["trait_effects"][0]["fruit_minus_insertion_log_rate_beta"],
          "focal_cluster_robust_P":
              test["trait_effects"][0]["nominal_two_sided_normal_p"],
          "global_ten_trait_joint_P":
              test["two_stage_gradient_joint_asymptotic_p"],
          "n_familywise_passed":test["n_ten_trait_exploratory_Bonferroni_p_below_0_005"],
        })
    # Point estimates also evaluated for source ID68 ambiguity.
    ambiguous=[]
    for j in np.flatnonzero(np.asarray(ids)=="68"):
        keep=np.asarray([i for i in range(N) if i!=j],int)
        fit=_fit_joint_nb(X,F,I,total,ids,af,ai,keep=keep)
        ambiguous.append({
          "source_zero_based_row_excluded":int(j),
          "n_original_source_rows_retained":int(len(keep)),
          "focal_log_rate_delta":fit["trait_effects"][0]["fruit_minus_insertion_log_rate_beta"],
          "focal_robust_P":fit["trait_effects"][0]["nominal_two_sided_normal_p"],
        })
    binary=_binary_fruit_part(X,F,total,ids)
    conditional=_conditional_positive_count_part(X,F,total,ids,af)
    bootstrap=_focal_bootstrap(X,F,I,total,ids,af,ai,n_boot=boot)
    reference=fit_stacked_model(X,F,I,total,ids,offset_corrected=True)
    if abs(reference["trait_effects"][0]["fruit_minus_insertion_log_slope"]-
           .08315327964461583)>1e-7:
        raise ValueError("Original Poisson exposure negative control changed")
    return {
      "analysis":"sch_original_2024_milkweed_nb2_two_part_selection_exposure_v1",
      "source_original_DOI":DOI,
      "source_original_xlsx_SHA256":"d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb",
      "n_original_source_rows":N,
      "n_original_plant_ID_labels":N_LABELS,
      "source_ID68_duplicated_two_rows":True,
      "observed_fruit_zero_stems":int((F==0).sum()),
      "observed_insertion_zero_stems":int((I==0).sum()),
      "peak_flower_count_source_quality":source_diag,
      "fruit_moment_alpha_initial_unclipped":momentF,
      "insertion_moment_alpha_initial_unclipped":momentI,
      "fruit_NB2_working_alpha_used":af,
      "insertion_NB2_working_alpha_used":ai,
      "original_source_NB2_joint_plant_cluster_stage_contrast":fitted,
      "original_source_predeclared_alpha_grid_sensitivity":grid,
      "source_plant_ID68_row_exclusion_sensitivity":ambiguous,
      "source_focal_paired_plant_ID_bootstrap":bootstrap,
      "original_source_fruit_positive_logit_two_part_diagnostic":binary,
      "original_source_fruit_positive_only_NB_working_mean":conditional,
      "poisson_source_previous_focal_exposure_log_rate_delta":
            reference["trait_effects"][0]["fruit_minus_insertion_log_slope"],
      "poisson_source_previous_focal_exposure_P":
            reference["trait_effects"][0]["cluster_robust_normal_p"],
      "zero_and_positive_descriptive_parts_are_not_full_hurdle_NB_likelihood":True,
      "source_plant_outcomes_observational_not_randomized":True,
      "sampled_insertion_ten_flowers_whole_plant_fruit_risk_sets_mismatched":True,
      "all_fitted_count_models_are_sensitivity_not_effective_pollinium_to_fruit_transition":True,
      "no_causal_reproductive_component_difference_or_sch_L":True,
      "status":"REAL_SOURCE_NB2_AND_TWO_PART_MEAN_SENSITIVITY_NO_CAUSAL_CONVERSION",
      "critical_limits":[
        "fixed_alpha_estimated_by_Poisson_residual_moments_not_full_NB2_MLE",
        "cluster_sandwich_not_sufficient_against_link_or_mean_misspecification",
        "logistic_part_is_any_fruit_on_stem_not_per_flower_fruit_probability",
        "positive_only_NB_regression_is_working_conditional_mean_not_truncated_NB_hurdle_likelihood",
        "only_F_positive_subset_can_create_selection_or_colliding_conditioning_bias",
        "peak_total_flowers_open_plus_buds_is_snapshot_not_tracked_seasonal_flower_risk_set",
        "conditioning_on_log_total_flowers_may_block_legitimate_trait_display_mechanism",
        "common_trait_gradient_does_not_identify_biological_allocation_or_pure_function_optima",
        "one_observational_source_population_103_rows_102_plant_labels_genets_unknown",
        "zero_stems_and_original_ID68_ambiguity_preserved_not_imputed",
        "posthoc_multitrait_comparisons_do_not_form_a_confirmatory_meta_effect",
      ],
    }

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path)
    p.add_argument("--out",type=Path,default=Path("artifacts/sch_original_milkweed_nb2_two_part.json"))
    p.add_argument("--boot",type=int,default=BOOT)
    a=p.parse_args()
    raw,url=raw_bytes(a.source)
    records,_=unpack_original(raw)
    result=run(records,a.boot)
    result["verified_original_source_url"]=url
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("BEGIN_SCH_2024_ORIGINAL_NB2_TWOPART")
    print(json.dumps({
      "source_n":result["n_original_source_rows"],
      "source_plant_IDs":result["n_original_plant_ID_labels"],
      "source_NB2_joint":result["original_source_NB2_joint_plant_cluster_stage_contrast"],
      "source_alpha_grid":result["original_source_predeclared_alpha_grid_sensitivity"],
      "source_zero_and_positive_two_parts":{
        "fruit_any":result["original_source_fruit_positive_logit_two_part_diagnostic"],
        "fruit_positive_count":result["original_source_fruit_positive_only_NB_working_mean"]},
      "source_ID68_sensitivities":result["source_plant_ID68_row_exclusion_sensitivity"],
      "source_cluster_bootstrap":result["source_focal_paired_plant_ID_bootstrap"],
      "status":result["status"],
    },indent=2,sort_keys=True,ensure_ascii=False))
    print("END_SCH_2024_ORIGINAL_NB2_TWOPART")

if __name__=="__main__":
    main()

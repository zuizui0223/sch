"""Proper zero-truncated NB2 check of the prior milkweed positive-fruit pattern.

Source: García et al. (2024), J Poll Ecol DOI
10.26786/1920-7603(2024)758. The only source is its verified official
Appendix II XLSX, as previously recovered and checksum pinned:
d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb.

A fruit-positive-only ordinary NB-GLM is NOT a zero-truncated likelihood.
This script fits the actual conditional PMF:
 P(Y=y | Y>0,mu,alpha) = NB2(y;mu,alpha)/(1-P_NB2(Y=0)), y>=1
with count mean mu=exp(X beta + offset), p0=(1+alpha*mu)**(-1/alpha).
The source's 102 plant ID labels (duplicate ID68) are respected. Its
positive subset is 63 rows from 62 observed labels.

Crucial biological boundary: it is a statistical analysis of aggregate
whole-stem fruit counts, NOT same-flower compatible pollen receipt-to-fruit
conversion. Flower opportunities estimated at flowering peak are trait-
dependent and not experimentally randomized. No direct fitness trade-off
or SCH loss L is measured.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path

from scripts.analyze_sch_milkweed_2024_paired_stage import (
    raw_bytes,unpack_original,select_complete,normalize_design
)
from scripts.analyze_sch_milkweed_2024_flower_opportunity import source_opportunity
from scripts.analyze_sch_milkweed_2024_nb2_two_part import (
    _moment_alpha, _conditional_positive_count_part,
    _binary_fruit_part, ALPHA_GRID
)

SOURCE_DOI="10.26786/1920-7603(2024)758"
SOURCE_SHA256="d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb"
N_SOURCE=103
N_SOURCE_LABELS=102
N_POSITIVE=63
N_POSITIVE_LABELS=62
SEED=20261117
N_BOOT=199


def _pieces(beta,X,y,log_offset,alpha):
    """Return log truncated NB pmf, individual score, expected information.

    The analytically derived gradient must match finite difference tests.
    The expected beta information is I=sum(x x' dE[Y|Y>0]/deta
                                      /(1+alpha*mu)).
    Alpha is a FIXED nuisance parameter: not promoted to an NB MLE.
    """
    import numpy as np
    from scipy.special import gammaln
    if not (0<alpha<=10):
        raise ValueError("invalid fixed NB2 dispersion")
    y=np.asarray(y,float)
    if len(y)!=X.shape[0] or not np.all(y>=1) or not np.all(y==np.floor(y)):
        raise ValueError("source positive count likelihood requires integer y>=1")
    eta=X@beta+log_offset
    if not np.all(np.isfinite(eta)) or np.any(abs(eta)>200):
        raise ValueError("overflow-risk source linear predictor")
    mu=np.exp(eta)
    r=1/alpha
    log1pmu=np.log1p(alpha*mu)
    logp0=-log1pmu/alpha
    p0=np.exp(logp0)
    q=-np.expm1(logp0)
    if not np.all(q>0):
        raise ValueError("numerically vanished positive-count truncation probability")
    logpmf=(
        gammaln(y+r)-gammaln(r)-gammaln(y+1)
        -r*log1pmu
        +y*(math.log(alpha)+eta-log1pmu)
    )
    logtrunc=logpmf-np.log(q)
    mean_pos=mu/q
    scalar_score=(y-mean_pos)/(1+alpha*mu)
    mprime=mean_pos*(1 - p0*mu/((1+alpha*mu)*q))
    weights=mprime/(1+alpha*mu)
    if not (np.all(np.isfinite(logtrunc)) and
            np.all(np.isfinite(scalar_score)) and
            np.all(np.isfinite(weights)) and np.all(weights>0)):
        raise ValueError("invalid source truncated NB score/information")
    return logtrunc,scalar_score,weights,mean_pos


def _objective(beta,X,y,offset,alpha):
    import numpy as np
    try:
        lp,scalar,_,_=_pieces(beta,X,y,offset,alpha)
        return -float(np.sum(lp)), -(X.T@scalar)
    except ValueError:
        return 1e25, np.zeros_like(beta)


def _fit_truncated(X,y,log_offset,labels,alpha):
    import numpy as np
    import statsmodels.api as sm
    from scipy.optimize import minimize
    from scipy.stats import norm
    if len(y)<55 or len(set(labels))<55:
        raise ValueError("insufficient positive source plant clusters")
    if np.linalg.matrix_rank(X)!=X.shape[1]:
        raise ValueError("source positive stage ten-predictor design singular")
    # A standard untruncated NB fit provides a stable starting point only.
    initial=sm.GLM(y,X,offset=log_offset,
                   family=sm.families.NegativeBinomial(alpha=alpha)).fit(
                       maxiter=300).params
    bounds=[(-15,8)]+[(-7,7)]*(X.shape[1]-1)
    fit=minimize(_objective,initial,args=(X,y,log_offset,alpha),
                 jac=True,method="L-BFGS-B",bounds=bounds,
                 options={"maxiter":1600,"ftol":1e-12,"gtol":1e-8})
    beta=np.asarray(fit.x,float)
    if not np.all(np.isfinite(beta)) or (not fit.success and
        np.linalg.norm(fit.jac,ord=np.inf)>5e-5):
        raise ValueError("source truncated NB MLE failed or gradient did not settle")
    ll,score,weights,mean_pos=_pieces(beta,X,y,log_offset,alpha)
    # Expected Hessian bread and the clustered empirical score outer products.
    bread=X.T@(X*weights[:,None])
    if np.linalg.matrix_rank(bread)!=X.shape[1]:
        raise ValueError("truncated NB2 expected information singular")
    clusters=defaultdict(lambda:np.zeros(X.shape[1],float))
    for pid,sc in zip(labels,X*score[:,None]):
        clusters[str(pid)]+=sc
    stacked=np.asarray(list(clusters.values()),float)
    n_cl=len(clusters)
    n=len(y)
    p=X.shape[1]
    inverse=np.linalg.inv(bread)
    cov=inverse@(stacked.T@stacked)@inverse
    cov*=n_cl/(n_cl-1)*(n-1)/(n-p)
    if not np.all(np.isfinite(cov)) or cov[1,1]<=0:
        raise ValueError("nonfinite original-source cluster sandwich covariance")
    se=math.sqrt(float(cov[1,1]))
    focal=float(beta[1])
    grad_norm=float(np.linalg.norm(X.T@score,ord=np.inf))
    if grad_norm>1e-4:
        raise ValueError(
            f"truncated NB2 analytic score not settled: norm={grad_norm:.7g} "+
            f"fit_success={fit.success}; message={fit.message}; "+
            f"params={beta.tolist()}; optimizer_grad_inf={float(np.linalg.norm(fit.jac,ord=np.inf)):.5g}"
        )
    return {
       "alpha_fixed":alpha,
       "n_plant_rows":n,
       "n_distinct_plant_labels":n_cl,
       "log_likelihood_correctly_zero_truncated":float(np.sum(ll)),
       "optimization_converged":bool(fit.success or grad_norm<1e-4),
       "source_gradient_inf_norm":grad_norm,
       "focal_inflorescence_beta":focal,
       "focal_label_cluster_SE":se,
       "focal_label_cluster_normal_p":float(2*norm.sf(abs(focal/se))),
       "focal_label_cluster_95CI":[focal-1.96*se,focal+1.96*se],
       "focal_expected_positive_count_change_per_one_trait_SD":math.exp(focal),
       "all_original_trait_parameters":beta.tolist(),
       "P_count_gt0_model_truncation_normalizer_in_likelihood":True,
       "expected_source_positive_count_min":float(mean_pos.min()),
       "expected_source_positive_count_max":float(mean_pos.max()),
       "formula":"logNB(y)-log(1-NB(0)); E[Y|Y>0]=mu/(1-p0)",
    }


def _focal_bootstrap(X,y,log_offset,labels,alpha,nboot=N_BOOT):
    """Source label-block bootstrap; use observed 62 labels, not 63 rows."""
    import numpy as np
    from scipy.optimize import minimize
    from scipy.stats import norm
    grouped=defaultdict(list)
    for i,pid in enumerate(labels):
        grouped[str(pid)].append(i)
    names=sorted(grouped)
    if len(names)<60:
        raise ValueError("source positive labels insufficient")
    rng=np.random.default_rng(SEED)
    # Fit original proper truncated likelihood once; subsequent bootstrap
    # starts from original MLE, avoiding repeated untruncated GLM starts.
    point=_fit_truncated(X,y,log_offset,labels,alpha)
    init=np.asarray(point["all_original_trait_parameters"],float)
    bounds=[(-15,8)]+[(-7,7)]*(X.shape[1]-1)
    estimates=[]
    for _ in range(nboot):
        sample=rng.integers(0,len(names),len(names))
        ix=np.asarray([i for j in sample for i in grouped[names[j]]],int)
        x,yb,off=X[ix],y[ix],log_offset[ix]
        if np.linalg.matrix_rank(x)!=x.shape[1]:
            continue
        fit=minimize(_objective,init,args=(x,yb,off,alpha),
                     jac=True,method="L-BFGS-B",bounds=bounds,
                     options={"maxiter":750,"ftol":1e-10,"gtol":1e-7})
        if not np.all(np.isfinite(fit.x)):
            continue
        try:
            _,scalar,_,_=_pieces(fit.x,x,yb,off,alpha)
            if np.linalg.norm(x.T@scalar,ord=np.inf)<3e-4:
                estimates.append(float(fit.x[1]))
        except ValueError:
            pass
    if len(estimates)<.8*nboot:
        raise ValueError("source ID-block truncated NB bootstrap did not qualify")
    lo,hi=np.percentile(estimates,[2.5,97.5])
    return {
        "original_plant_ID_labels_resampled":len(names),
        "bootstrap_requested":nboot,
        "bootstrap_fit_converged":len(estimates),
        "focal_zero_truncated_log_count_rate_bootstrap95":[float(lo),float(hi)],
        "bootstrap_interval_excludes_zero":bool(lo>0 or hi<0),
        "selection_on_fruit_positive_noncausal":True,
    }


def run(records,nboot=N_BOOT):
    import numpy as np
    matrix,ids,_,_=select_complete(records)
    X,Y,_,_,_=normalize_design(matrix)
    total,opps,diag=source_opportunity(records)
    fruit=opps[:,5]
    if len(records)!=N_SOURCE or len(set(ids))!=N_SOURCE_LABELS or \
       sum(pid=="68" for pid in ids)!=2 or np.sum(fruit>0)!=N_POSITIVE:
        raise ValueError("genuine original 103-row source or fruit-positive grain drift")
    pos=fruit>0
    labels=np.asarray(ids,dtype=str)[pos]
    if len(set(labels))!=N_POSITIVE_LABELS:
        raise ValueError("genuine original 62 fruit-positive plant labels drift")
    Xp=X[pos]
    yp=fruit[pos]
    offset=np.log(total[pos])
    alpha,raw_alpha=_moment_alpha(fruit,X,np.log(total))
    expected_source_alpha=.43988020874428213
    if abs(alpha-expected_source_alpha)>1e-7:
        raise ValueError("source-published original NB2 moment alpha changed")
    # Original untruncated working NB2 result is an explicit negative control.
    naive=_conditional_positive_count_part(X,fruit,total,ids,alpha)
    ref=naive["two_outcome_definitions"]
    if abs(ref["fruit_positive_per_peak_flower_count"]["inflorescence_number_beta"]+
           .3290555717436509)>1e-7:
        raise ValueError("earlier positive-subset working model not replicated")
    fitted=_fit_truncated(Xp,yp,offset,labels,alpha)
    no_offset=_fit_truncated(Xp,yp,np.zeros_like(offset),labels,alpha)
    grid=[]
    for a in ALPHA_GRID:
        s=_fit_truncated(Xp,yp,offset,labels,a)
        grid.append({
            "source_predeclared_alpha_fixed":a,
            "proper_truncated_focal_beta":s["focal_inflorescence_beta"],
            "proper_truncated_cluster_normal_p":s["focal_label_cluster_normal_p"],
            "proper_truncated_focal_95CI":s["focal_label_cluster_95CI"],
        })
    binary=_binary_fruit_part(X,fruit,total,ids)
    dup=[]
    index68=np.flatnonzero(np.asarray(ids)=="68")
    for ix in index68:
        original_keep=np.ones(len(ids),bool);original_keep[ix]=False
        fit_idx=np.where(original_keep & pos)[0]
        # Need map full original design to positive-selected subset: alpha is
        # fixed from the full source, while the subject subset varies by drop.
        fit=_fit_truncated(X[fit_idx],fruit[fit_idx],
                           np.log(total[fit_idx]),np.asarray(ids)[fit_idx],alpha)
        dup.append({
          "source_row_zero_index_excluded":int(ix),
          "source_positive_rows_after_exclusion":int(len(fit_idx)),
          "proper_truncated_focal_beta":fit["focal_inflorescence_beta"],
          "proper_truncated_cluster_normal_p":fit["focal_label_cluster_normal_p"],
        })
    bootstrap=_focal_bootstrap(Xp,yp,offset,labels,alpha,nboot=nboot)
    return {
      "analysis":"sch_2024_milkweed_proper_zero_truncated_nb2_v1",
      "source_DOI":SOURCE_DOI,
      "original_source_xlsx_sha256":SOURCE_SHA256,
      "source_total_rows":N_SOURCE,
      "source_unique_plant_ID_labels":N_SOURCE_LABELS,
      "source_zero_fruit_rows":N_SOURCE-N_POSITIVE,
      "source_positive_fruit_rows":N_POSITIVE,
      "source_positive_fruit_ID_labels":N_POSITIVE_LABELS,
      "source_moment_NB2_alpha_fixed":alpha,
      "source_alpha_raw_unclipped":raw_alpha,
      "prior_nontruncated_positive_only_working_NB2":{
          "whole_stem_fruit_number":ref["fruit_positive_whole_plant_count"],
          "per_peak_flower_count":ref["fruit_positive_per_peak_flower_count"],
          "not_truncated_likelihood":True,
      },
      "proper_positive_only_zero_truncated_NB2_per_peak_flower":fitted,
      "proper_positive_only_zero_truncated_NB2_whole_stem_count":no_offset,
      "proper_truncated_per_peak_flower_alpha_grid":grid,
      "proper_truncated_ID68_source_row_deletion_sensitivity":dup,
      "proper_truncated_source_label_block_bootstrap":bootstrap,
      "whole_sample_any_fruit_logistic_models":binary,
      "source_flower_opportunity_quality":diag,
      "source_positive_conditional_parts_can_be_combined_as_hurdle_likelihood":True,
      "unconditional_hurdle_fruit_conversion_probability_identified":False,
      "source_plant_ID68_ambiguous_original_rows_not_relabelled":True,
      "no_randomized_flower_traits_or_pure_optima":True,
      "no_SCH_conflict_loss_L":True,
      "critical_limits":[
        "fixed_dispersion_not_jointly_MLE_and_its_uncertainty_not_included_in_standard_error",
        "observed_63_positive_source_records_do_not_form_an_independent_ecological_study",
        "selected_F_gt_0_source_cohort_may_induce_selection_bias",
        "truncated_NB_uses_log_mean_of_latent_untruncated_count_not_log_mean_of_positive_subset",
        "fruit_count_whole_stem_and_ten_flower_pollinia_counts_do_not_share_a_flower_risk_set",
        "total_peak_open_plus_buds_is_not_observed_true_seasonal_flower_opportunity",
        "source_ID68_duplicated_fruit_count_identity_unresolved",
        "same_floral_trait_regression_is_association_not_causal_allocation_tradeoff",
      ],
      "status":"SOURCE_2024_ZERO_TRUNCATED_NB2_POSITIVE_FRUIT_SENSITIVITY_NO_CAUSAL_CONFLICT",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path)
    p.add_argument("--output",type=Path,
                   default=Path("artifacts/sch_milkweed_2024_proper_truncated_v1.json"))
    p.add_argument("--boot",type=int,default=N_BOOT)
    a=p.parse_args()
    raw,url=raw_bytes(a.source)
    rows,_=unpack_original(raw)
    out=run(rows,a.boot)
    out["verified_source_file_url_or_origin"]=url
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("BEGIN_SCH_MILKWEED_PROPER_TRUNCATED_NB2")
    print(json.dumps({
        "source_rows":out["source_total_rows"],
        "positive_rows":out["source_positive_fruit_rows"],
        "positive_label_groups":out["source_positive_fruit_ID_labels"],
        "prior_naive_model":out["prior_nontruncated_positive_only_working_NB2"],
        "proper_truncated_per_peak_flower":
             out["proper_positive_only_zero_truncated_NB2_per_peak_flower"],
        "proper_truncated_whole_stem_count":
             out["proper_positive_only_zero_truncated_NB2_whole_stem_count"],
        "dispersion_grid":out["proper_truncated_per_peak_flower_alpha_grid"],
        "original_source_ID68":out["proper_truncated_ID68_source_row_deletion_sensitivity"],
        "original_plant_label_bootstrap":out["proper_truncated_source_label_block_bootstrap"],
        "status":out["status"],
    },ensure_ascii=False,indent=2,sort_keys=True))
    print("END_SCH_MILKWEED_PROPER_TRUNCATED_NB2")


if __name__=="__main__":
    main()

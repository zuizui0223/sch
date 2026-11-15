"""Reanalyse matched original 2024 milkweed individuals at two female fitness stages.

Source: García, Dow, Vézina & Parachnowitsch (2024), J Poll Ecol,
DOI 10.26786/1920-7603(2024)758, official Appendix II, galley 478.
Source was retrieved as a two-sheet XLSX whose 'milkweed.selectiondata'
sheet stores ONE COMMA-DELIMITED RECORD PER EXCEL A-CELL (104 lines incl
header). This script decodes THAT layout and confirms authentic SHA-256.

Science:
- 103 matched plant IDs, not 103 separate experimental treatments
- two outcomes at SAME plants: pollinia insertions I and fruits initiated F
- multivariate standardized trait selections on I, F (and R as context)
- paired within-plant outcome difference wF-wI retains sampling covariance
- HC3 uncertainty and paired individual bootstrap
- observational fitness-component difference, NOT causal conversion gate
- no SCH pure function optima, randomized trait or compromise L
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

try:
    import numpy as np
except ModuleNotFoundError:
    # The global SCH code contract CI intentionally installs only pytest.
    # Numerical original-plant reanalysis installs numpy in its own source CI.
    np=None

from scripts.ingest_sch_milkweed_2024_original_appendix import (
    CANDIDATES, get, classify
)

SOURCE_DOI="10.26786/1920-7603(2024)758"
SOURCE_SHA256="d5beb695f1c5f81f03eb74a18937582e99fc2cd1c23bda3598e33ef904bfadfb"
SOURCE_BYTES=38955
ORIGINAL_SHEET="milkweed.selectiondata"
N_EXPECT=103
SEED=20261115
B_BOOT=1999

TRAIT_CODES={
    "Inflorescence number":"inflor.nu",
    "Inflorescence size":"inflor.size",
    "Hood length":"hood_l",
    "Hood width":"hood_w",
    "Petal width":"petal",
    "Nectar concentration":"nec.resid",
    "Floral wet latex":"flw.latex.wet",
    "Leaf wet latex":"leaf.latex.wet",
    "Plant height":"height",
    "Damage index":"damage.index",
}
OUTCOMES={
    "fruits_initiated":"fruit.init",
    "pollinia_inserted":"insertions_t",
    "pollinaria_removed":"removals_t",
}
# Source paper original Table 1 published variance-standardized partial betas
# use diagnostic signatures only; a paper may transform some raw trait axes.
PUBLISHED_SOURCE_SIGNATURES={
    "Inflorescence number":{"fruits_initiated":.464,"pollinia_inserted":-.016},
    "Inflorescence size":{"fruits_initiated":.291,"pollinia_inserted":-.001},
    "Petal width":{"fruits_initiated":.070,"pollinia_inserted":-.235},
    "Floral wet latex":{"fruits_initiated":.056,"pollinia_inserted":.326},
}


def raw_bytes(source_path=None):
    if source_path is not None:
        raw=Path(source_path).read_bytes()
        src="SOURCE_FILE_PROVIDED"
    else:
        info,raw=get(CANDIDATES[0])
        if raw is None or info.get("status") == "HTTP_ERROR":
            raise ConnectionError("Cannot get original JPE Appendix II")
        src=CANDIDATES[0]
    if len(raw)!=SOURCE_BYTES or hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:
        raise ValueError("Original 2024 appendix content SHA256/size drift")
    if classify(raw)!="XLSX":
        raise ValueError("Original primary source is not the expected genuine XLSX")
    return raw,src


def unpack_original(raw):
    import openpyxl
    book=openpyxl.load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
    if ORIGINAL_SHEET not in book.sheetnames:
        raise ValueError("Source appendix individual-data sheet missing")
    sheet=book[ORIGINAL_SHEET]
    if sheet.max_column!=1 or sheet.max_row!=N_EXPECT+1:
        raise ValueError("JPE 2024 original Excel one-cell CSV line structure drift")
    strings=[]
    for cells in sheet.iter_rows(min_col=1,max_col=1,values_only=True):
        text=cells[0]
        if not isinstance(text,str):
            raise ValueError("Original JPE sheet has unparsed non-string CSV row")
        strings.append(text)
    book.close()
    text="\n".join(strings)+"\n"
    reader=csv.DictReader(io.StringIO(text))
    if not reader.fieldnames or len(set(reader.fieldnames))!=len(reader.fieldnames):
        raise ValueError("Original source CSV headers missing or repeated")
    cols={col.strip() for col in reader.fieldnames}
    expected=set(TRAIT_CODES.values())|set(OUTCOMES.values())|{"plant_id"}
    if not expected<=cols:
        raise ValueError("Original biological traits/fitness columns not recovered: "+
                         ",".join(sorted(expected-cols)))
    records=list(reader)
    if len(records)!=N_EXPECT:
        raise ValueError("Original individual plant n not 103")
    if any(None in row for row in records):
        raise ValueError("Unparsed original CSV row has more columns than header")
    ids=[str(row["plant_id"]).strip() for row in records]
    from collections import Counter
    co=Counter(ids)
    duplicated={k:v for k,v in co.items() if v>1}
    if (any(not x for x in ids) or
        len(co)!=102 or duplicated!={"68":2}):
        raise ValueError("Original 2024 plant identifiers drift: "+
                         f"n_unique={len(co)} duplicated={str(duplicated)[:200]}")
    # Two source rows bear the same ID=68. Do not invent which is a
    # different individual or silently remove a source record.
    return records,list(reader.fieldnames)


def number_or_none(val):
    if val is None or str(val).strip() in {"","NA","N/A","nan","NaN","NULL","."}:
        return None
    try:
        n=float(val)
        return n if math.isfinite(n) else None
    except (TypeError,ValueError):
        return None


def select_complete(records):
    values=[];ids=[];missing={x:0 for x in list(TRAIT_CODES.values())+list(OUTCOMES.values())}
    fields=list(TRAIT_CODES.values())+list(OUTCOMES.values())
    for row in records:
        out={x:number_or_none(row.get(x)) for x in fields}
        for field in fields:
            if out[field] is None:missing[field]+=1
        if all(out[x] is not None for x in fields):
            ids.append(str(row["plant_id"]).strip())
            values.append([out[x] for x in fields])
    if not values:
        raise ValueError("No complete original plant observations")
    arr=np.asarray(values,float)
    if not np.all(np.isfinite(arr)):
        raise ValueError("Nonfinite original 2024 plant rows")
    if len(ids)<60:
        raise ValueError("Insufficient comparable complete-case 2024 plant n")
    if np.any(arr[:,-3:]<0):
        raise ValueError("Negative original fitness count")
    return arr,ids,missing,fields


def normalize_design(arr):
    n=arr.shape[0];k=len(TRAIT_CODES)
    rawX=arr[:,:k]
    mu=rawX.mean(axis=0)
    sd=rawX.std(axis=0,ddof=1)
    if np.any(sd<=0):
        raise ValueError("A source trait has zero SD")
    standardized=(rawX-mu)/sd
    X=np.column_stack([np.ones(n),standardized])
    if np.linalg.matrix_rank(X)<k+1:
        raise ValueError("Original multiple trait matrix rank deficient")
    rawY=arr[:,k:]
    ym=rawY.mean(axis=0)
    if np.any(ym<=0):
        raise ValueError("Original plant fitness endpoint zero mean")
    Y=rawY/ym
    return X,Y,dict(zip(TRAIT_CODES,mu.tolist())),dict(zip(TRAIT_CODES,sd.tolist())),dict(zip(OUTCOMES,ym.tolist()))


def fit_ols_hc3(X,y):
    """Return OLS coef, HC3 sandwich covariance, residual df."""
    XtXi=np.linalg.inv(X.T@X)
    coef=XtXi@X.T@y
    res=y-X@coef
    h=np.einsum("ij,jk,ik->i",X,XtXi,X)
    if np.any(h>=1):
        raise ValueError("Extreme original plant leverage equals or exceeds one")
    score=X*(res/(1-h))[:,None]
    cov=XtXi@(score.T@score)@XtXi
    se=np.sqrt(np.maximum(0,np.diag(cov)))
    return coef,se,cov,int(X.shape[0]-X.shape[1])


def run_from_raw(raw,source_url,outdir,boot=B_BOOT):
    if np is None:
        raise RuntimeError("original individual-level analysis requires numpy")
    records,original_fields=unpack_original(raw)
    matrix,plant_ids,missing,fields=select_complete(records)
    X,Y,mu,sd,ym=normalize_design(matrix)
    n=X.shape[0]
    if Y.shape!=(n,3):
        raise ValueError("Original source outcomes/order differ")
    model={}
    for i,name in enumerate(OUTCOMES):
        beta,se,cov,df=fit_ols_hc3(X,Y[:,i])
        model[name]={"coef":beta.tolist(),"SE_HC3":se.tolist(),
                     "residual_df":df,
                     "n_original_matching_plants":n}
    contrast=Y[:,0]-Y[:,1]
    beta,se,cov,df=fit_ols_hc3(X,contrast)
    corr=np.corrcoef(Y.T)
    # Same plants, both response types aligned; this tests conditional
    # *association*, not true per-pollinium fruit initiation conversion.
    conditionalX=np.column_stack([X,Y[:,1]])
    conditional_b,conditional_se,conditional_cov,conditional_df=fit_ols_hc3(
        conditionalX,Y[:,0])
    # HC3 joint Wald diagnostic for all 10 trait×female-stage differences.
    # The covariance is estimated directly from the paired response
    # difference wF-wI, preserving within-record cross-stage covariance.
    stage_cov=cov[1:,1:]
    if np.linalg.matrix_rank(stage_cov)!=len(TRAIT_CODES):
        raise ValueError("Paired stage HC3 contrast covariance singular")
    joint_stat=float(beta[1:]@np.linalg.solve(stage_cov,beta[1:]))
    if not math.isfinite(joint_stat) or joint_stat<0:
        raise ValueError("Invalid original paired ten-trait Wald statistic")
    # df=10, even-degree chi-square upper-tail exact mathematical survival
    # function (still an asymptotic HC3 Wald calibration).
    half=joint_stat/2.0
    joint_p=math.exp(-half)*sum(half**j/math.factorial(j) for j in range(5))
    # Exact same-individual paired bootstrap; do not independently resample
    # the two outcomes (that would destroy their estimated covariance).
    rng=np.random.default_rng(SEED)
    # Resample the *plant label* (102 unique IDs, including the one
    # duplicated label 68 as a single unit of uncertain identity), not
    # the 103 rows independently. This protects a plausible repeated plant.
    groups={}
    for ix,pid in enumerate(plant_ids):
        groups.setdefault(pid,[]).append(ix)
    group_keys=list(groups)
    n_groups=len(group_keys)
    if n_groups!=102:
        raise ValueError("Complete-case original ID cluster count drift")
    boot_coef=[]
    for t in range(boot):
        sampled=rng.integers(0,n_groups,n_groups)
        ix=np.asarray([j for i in sampled for j in groups[group_keys[i]]],int)
        B=X[ix,:]
        y=contrast[ix]
        try:
            if np.linalg.matrix_rank(B)!=B.shape[1]:continue
            fit=np.linalg.lstsq(B,y,rcond=None)[0]
            if np.all(np.isfinite(fit)):
                boot_coef.append(fit)
        except np.linalg.LinAlgError:
            continue
    if len(boot_coef)<max(250,int(.8*boot)):
        raise ValueError("Too few valid original paired individual bootstrap draws")
    b=np.asarray(boot_coef)
    lo,hi=np.percentile(b,[2.5,97.5],axis=0)
    # Two 102-row analyses exclude each of the ambiguous ID=68 rows
    # alternately, without guessing whether either record is erroneous.
    duplicate_ix=[ix for ix,pid in enumerate(plant_ids) if pid=="68"]
    if len(duplicate_ix)!=2:
        raise ValueError("ID 68 duplicate did not survive source filtering")
    leave_duplicate=[]
    for drop in duplicate_ix:
        mask=np.ones(n,bool)
        mask[drop]=False
        coef102,_,_,_=fit_ols_hc3(X[mask],contrast[mask])
        leave_duplicate.append({
            "dropped_original_data_row_index_zero_based":int(drop),
            "source_n_after_one_row_drop":int(mask.sum()),
            "beta_difference_vector_fixed_103row_trait_standardization":coef102.tolist()})
    source_duplicates=[r for r in records if str(r["plant_id"]).strip()=="68"]
    differing_fields=[
        k for k in original_fields
        if source_duplicates[0].get(k)!=source_duplicates[1].get(k)]
    selected=[]
    for i,(label,code) in enumerate(TRAIT_CODES.items(),start=1):
        selected.append({
            "trait":label,"source_column":code,
            "original_fruit_beta":float(model["fruits_initiated"]["coef"][i]),
            "original_insertion_beta":float(model["pollinia_inserted"]["coef"][i]),
            "original_removal_beta":float(model["pollinaria_removed"]["coef"][i]),
            "paired_fruit_minus_insertion_beta":float(beta[i]),
            "paired_difference_HC3_SE":float(se[i]),
            "paired_plant_bootstrap_percentile95":[float(lo[i]),float(hi[i])],
            "bootstrap_excludes_zero":bool(lo[i]>0 or hi[i]<0),
            "simple_normal_approx_HC3_p":math.erfc(abs(float(beta[i]/se[i]))/math.sqrt(2))
                if se[i]>0 else None,
            "original_paper_published_table1_beta":{
                k:v for k,v in PUBLISHED_SOURCE_SIGNATURES.get(label,{}).items()},
        })
    out={
      "analysis":"sch_asclepias_2024_original_103plant_paired_stage_comparison_v1",
      "paper_doi":SOURCE_DOI,
      "source_original_official_url":source_url,
      "verified_original_xlsx_sha256":SOURCE_SHA256,
      "verified_original_xlsx_bytes":SOURCE_BYTES,
      "n_original_journal_data_plant_rows":len(records),
      "n_original_distinct_source_plant_ID_labels":len({r["plant_id"] for r in records}),
      "n_original_duplicate_id_labels":1,
      "original_duplicate_label":"68",
      "duplicate_id68_rows_different_fields":differing_fields,
      "original_duplicate_id68_rows_exactly_identical":len(differing_fields)==0,
      "n_complete_case_source_rows":n,
      "n_complete_case_distinct_source_plant_labels":n_groups,
      "one_ambiguous_label_two_102row_source_sensitivities":leave_duplicate,
      "n_traits_multivariate":len(TRAIT_CODES),
      "n_paired_bootstrap_draws":len(boot_coef),
      "bootstrap_resampling_unit":"original_plant_ID_label_102_groups_not_103_rows",
      "random_seed":SEED,
      "source_original_embedded_csv_column_count":len(original_fields),
      "original_trait_fitness_missingness":missing,
      "fitness_endpoint_means":ym,
      "pearson_fruits_vs_insertions":float(corr[0,1]),
      "pearson_pollinia_removed_vs_inserted":float(corr[1,2]),
      "published_raw_all_119_flower_sampled_correlation_not_same_n103":True,
      "pollinia_sampled_denominator":"10 flowers per stem",
      "fruit_initiation_denominator":"all inflorescences on plant",
      "direct_fruit_per_measured_inserted_pollinium_conversion_rate":False,
      "independent_source_2005_three_experimental_regimes_retested":False,
      "source_2024_plant_matched_partial_association_fruits_given_insertions_and_ten_traits":{
        "inserted_pollinia_relative_fitness_coefficient":float(conditional_b[-1]),
        "HC3_SE":float(conditional_se[-1]),
        "conditional_HC3_normal_p":math.erfc(
          abs(float(conditional_b[-1]/conditional_se[-1]))/math.sqrt(2))
          if conditional_se[-1]>0 else None,
        "n_source_rows":n,
        "correlation_is_not_plant_fruit_conversion_probability":True,
      },
      "paired_ten_trait_stage_difference_joint_HC3_Wald":{
        "statistic":joint_stat,
        "degrees_of_freedom_asymptotic_chi2":10,
        "conditional_asymptotic_P":joint_p,
        "original_study_direct_stage_interaction_test":False,
      },
      "published_authors_insertion_fruit_raw_r":-.12,
      "published_authors_removal_insertion_raw_r":.44,
      "raw_2024_models":model,
      "trait_level_fruit_vs_pollinium_comparison":selected,
      "n_traits_passing_posthoc_ten_test_Bonferroni_HC3_normal":sum(
        x["simple_normal_approx_HC3_p"] is not None and
        x["simple_normal_approx_HC3_p"]<.005 for x in selected),
      "ten_trait_Bonferroni_p_threshold":.005,
      "no_new_2005_published_treatment_effect_estimated":True,
      "original_raw_individuals_observational_not_randomized_traits":True,
      "is_between_stage_different_from_zero_estimated_on_same_plant":True,
      "source_2005_and_2017_not_independently_raw_refitted":True,
      "conditional_fruit_formation_mechanism_not_established":True,
      "source_method_mismatch_to_paper_original_models_possible":True,
      "source_fit_proxy_does_not_establish_causal_compromise_L":True,
      "claim_limits":[
        "paper2024_one_observational_population_103_rows_102_distinct_IDs_not_independent_species",
        "source_id68_is_duplicated_true_individual_identity_unresolved",
        "both_duplicate_row_deletions_are_sensitivity_not_source_correction",
        "relative_fruit_and_insertion_endpoints_are_distinct_fitness_currencies",
        "joint_onset_trait_fitness_process_not_intervened",
        "matching_original_2024_study_processing_and_imputation_must_be_audited",
        "fruit_init_is_not_mature_fruits_and_may_include_future_abortion",
        "ten_flower_pollinium_sampling_and_whole_plant_fruit_counts_have_different_denominators",
        "published_2024_pollinia_fruit_correlation_n119_differs_from_source_103_complete_case_cohort",
        "HC3_joint_Wald_is_asymptotic_not_randomized_trait_stages",
        "pollinia_received_need_not_be_compatible_or_effectively_germinated",
        "residual_variance_and_count_data_may_violate_OLS_distribution",
        "bootstrap_plant_unit_may_ignore_unmeasured_clonal_or_spatial_correlation",
        "no_randomized_interaction_state_or_heritable_trait_optima_estimated",
        "no_SCH_L_identified",
      ],
      "status":"REAL_ORIGINAL_2024_JPE_103_PLANT_PAIRED_TWO_FEMALE_STAGE_REGRESSION_WITH_CAUSAL_LIMITS",
    }
    p=outdir/"original_2024_103plant_paired_fitness_stage_v1.json"
    p.write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    return out


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path)
    p.add_argument("--outdir",type=Path,default=Path("artifacts/sch_jpe2024_plant_raw"))
    p.add_argument("--boot",type=int,default=B_BOOT)
    args=p.parse_args()
    args.outdir.mkdir(parents=True,exist_ok=True)
    raw,url=raw_bytes(args.source)
    output=run_from_raw(raw,url,args.outdir,boot=args.boot)
    summary={key:value for key,value in output.items()
             if key not in {"raw_2024_models"}}
    print("BEGIN_SCH_ORIGINAL_2024_ASCLEPIAS_PAIRED_STAGE")
    print(json.dumps(summary,ensure_ascii=False,indent=2,sort_keys=True))
    print("END_SCH_ORIGINAL_2024_ASCLEPIAS_PAIRED_STAGE")

if __name__=="__main__":
    main()

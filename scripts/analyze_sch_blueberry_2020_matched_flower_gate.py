"""Reanalyse genuine matched-flower visitation and self/cross gates in blueberries.

Original 2020 authors' source: Kendall et al., J Applied Ecology
DOI 10.1111/1365-2664.13751. Original openly archived CC0 data
on Zenodo record 3987488 / Dryad DOI 10.5061/dryad.tmpg4f4wj.

The SAME tagged flower is followed to binary fruit set, unlike source
2024 milkweed data that joined 10-flower visits to whole-plant fruit.
This original-data analysis does not establish compatible pollen-grain
deposition, fertilization or SCH causal functional optimum/fitness L.

Independent unit for standard errors is an original source plant label
nested in source blueberry type x year x block. This does not ensure
independent genets or across-type randomized mating-system identity.
Cross/self comparison is of pollen-source interventions within source
blueberry type, not a random assignment of cultivar or mating system.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
import math
from pathlib import Path

from scripts.ingest_sch_2020_blueberry_original_flower import (
    EXPECTED,parse_original,source_schema,
)

try:
    import numpy as np
except ModuleNotFoundError:
    np=None

DOI="10.1111/1365-2664.13751"
SOURCE_RECORD_ID=3987488
SOURCE_TYPES=("Blue Rose","Powder Blue","Snowchaser")
HIGHBUSH_TYPES=("Blue Rose","Snowchaser")
RABBITEYE_TYPE="Powder Blue"
VISIT_BINS=((0,0,"0"),(1,1,"1"),(2,3,"2-3"),
            (4,5,"4-5"),(6,10,"6-10"),(11,15,"11-15"))
SEED=20261117
B_BOOT=1999
FILENAMES={
 "multiple":"fruit_set_multiple_visits_experiments_JAPPL-2020-00197.csv",
 "pollination":"fruit_set_pollination_experiments_JAPPL-2020-00197.csv",
 "single":"fruit_set_single_visit_experiments_JAPPL-2020-00197.csv",
}
EXPECTED_SOURCE={
 "multiple":(2080,992,1088,0),
 "pollination":(2125,1209,916,0),
 "single":(1309,338,971,0),
}

def raw_source(folder,kind):
    path=Path(folder)/FILENAMES[kind]
    b=path.read_bytes()
    if hashlib.md5(b).hexdigest()!=EXPECTED[FILENAMES[kind]]:
        raise ValueError("Original flower fruit-set source MD5 changed "+kind)
    rows,columns,enc=parse_original(b)
    schema=source_schema(rows,columns)
    n,pos,zero,dups=EXPECTED_SOURCE[kind]
    if (schema["n_original_rows"]!=n or
        schema["n_original_fruit_positive"]!=pos or
        schema["n_original_fruit_zero"]!=zero or
        schema["n_composite_flower_identity_ambiguous_duplicate_keys"]!=dups):
        raise ValueError("Original source tagged flower counts/identity changed "+kind)
    if set(schema["original_species_counts"])!=set(SOURCE_TYPES):
        raise ValueError("Original blueberry source type composition changed")
    for r in rows:
        if r[schema["qualified_column_roles"]["binary_fruit_set"]].strip() not in {"0","1"}:
            raise ValueError("Original source flower fruit outcome missing")
    return rows,schema,hashlib.sha256(b).hexdigest()

def plant_key(row):
    """Plant source ID nested in type/year/block; never use flower Tag for cluster."""
    keys=("Species","Year","Block","RP")
    vals=[str(row[k]).strip() for k in keys]
    if any(not v or v.lower() in ("na","nan","null") for v in vals):
        # The source itself has the separate observed row and plant fields.
        fallback=(str(row["Row"]).strip(),str(row["Plant.number"]).strip())
        if any(not v for v in fallback):
            raise ValueError("Original source plant identity cannot be qualified")
        vals=[str(row[k]).strip() for k in ("Species","Year","Block")]+[
             "source_row_plant:"+str(fallback)]
    return "|".join(vals)

def fruit(row):
    z=row["FS"].strip()
    if z not in ("0","1"):raise ValueError("Original flower FS not binary")
    return int(z)

def _visit_count(row):
    v=row["sumvisits"].strip()
    if not v.isdigit() or not 0<=int(v)<=15:
        raise ValueError("Original source visitation count invalid or missing")
    return int(v)


def pollination_source_risk_differences(rows,boot=B_BOOT):
    """Within-cultivar self versus cross randomized pollen source descriptors.

    Source plant-ID-block bootstrap preserves repeated flowers within plants.
    No pretend independent 2,125 flower-level standard errors.
    """
    if np is None:raise RuntimeError("source analysis numpy dependency missing")
    target={"Cross pollination","Self pollination"}
    sub=[r for r in rows if r["TREATMENT"].strip() in target]
    if len(sub)!=676:
        raise ValueError("Original 320 cross and 356 self flower source count changed")
    by_type={}
    for typ in SOURCE_TYPES:
        sample=[r for r in sub if r["Species"].strip()==typ]
        treatments={t:[r for r in sample if r["TREATMENT"].strip()==t] for t in target}
        if min(len(v) for v in treatments.values())<20:
            raise ValueError("Original source type lacks usable cross/self flowers")
        observed={}
        for trt,part in treatments.items():
            vals=[fruit(x) for x in part]
            observed[trt]={"n_original_flowers":len(vals),
                           "n_fruits":sum(vals),
                           "per_tagged_flower_fruit_rate":sum(vals)/len(vals)}
        diff=(observed["Cross pollination"]["per_tagged_flower_fruit_rate"]-
              observed["Self pollination"]["per_tagged_flower_fruit_rate"])
        # Report source year x block overlap of hand-cross and hand-self.
        # The raw cross/self rate difference is not automatically a site-
        # standardized randomized compatibility effect.
        by_site=defaultdict(lambda:np.zeros(4,dtype=int))
        for r in sample:
            site=str(r["Year"]).strip()+"|"+str(r["Block"]).strip()
            j=0 if r["TREATMENT"].strip()=="Cross pollination" else 2
            by_site[site][j]+=1
            by_site[site][j+1]+=fruit(r)
        site_rows=[]
        weighted=0.
        wtotal=0.
        for name,counts in sorted(by_site.items()):
            nC,fC,nS,fS=map(int,counts)
            both=nC>0 and nS>0
            site_rd=fC/nC-fS/nS if both else None
            weight=nC*nS/(nC+nS) if both else 0.
            if both:
                weighted+=weight*site_rd
                wtotal+=weight
            site_rows.append({
              "original_year_block":name,
              "n_hand_cross":nC,"n_fruit_cross":fC,
              "n_hand_self":nS,"n_fruit_self":fS,
              "within_original_site_risk_difference":site_rd,
              "both_pollen_sources_observed_within_site":both,
              "harmonic_n_weight_for_site_standardization":weight,
            })
        if wtotal<=0:
            raise ValueError("No overlapping source year-block pollen treatments")
        site_weighted_diff=weighted/wtotal
        eligible_row_fraction=sum(x["n_hand_cross"]+x["n_hand_self"] for x in site_rows
            if x["both_pollen_sources_observed_within_site"])/len(sample)
        # Each block is a source-labelled PLANT and may contain repeated
        # tagged flowers and (in some plants) multiple floral treatments.
        group=defaultdict(lambda:np.zeros(4,dtype=int))
        for r in sample:
            i=0 if r["TREATMENT"].strip()=="Cross pollination" else 2
            group[plant_key(r)][i]+=1
            group[plant_key(r)][i+1]+=fruit(r)
        keys=sorted(group)
        matrix=np.asarray([group[key] for key in keys])
        if len(keys)<20:
            raise ValueError("Original source plant-cluster count too small")
        by_type[typ]={
          "source_original_paper":DOI,
          "n_original_distinct_source_plant_labels":len(keys),
          "raw_cross_vs_self":observed,
          "risk_difference_cross_minus_self":diff,
          "source_year_block_coverage":site_rows,
          "source_original_sites_with_both_cross_and_self":sum(x["both_pollen_sources_observed_within_site"] for x in site_rows),
          "source_overlapping_site_fraction_of_cross_self_flower_rows":eligible_row_fraction,
          "source_harmonic_weighted_original_site_cross_self_risk_difference":site_weighted_diff,
          "group_counts":matrix,
        }
    rng=np.random.default_rng(SEED)
    bvalues={s:[] for s in SOURCE_TYPES}
    contrast=[]
    fails=0
    for _ in range(boot):
        new={}
        for typ in SOURCE_TYPES:
            matrix=by_type[typ]["group_counts"]
            ix=rng.integers(0,len(matrix),len(matrix))
            n=matrix[ix].sum(axis=0)
            if n[0]==0 or n[2]==0:
                fails+=1
                break
            new[typ]=n[1]/n[0]-n[3]/n[2]
        if len(new)!=3:
            continue
        for typ in SOURCE_TYPES:bvalues[typ].append(new[typ])
        contrast.append(new[RABBITEYE_TYPE]-.5*(new["Blue Rose"]+new["Snowchaser"]))
    if len(contrast)<.95*boot:
        raise ValueError("Source plant-level bootstrap cross/self missing many draws")
    summary={}
    for typ in SOURCE_TYPES:
        x=by_type[typ]
        boot_ci=np.percentile(bvalues[typ],[2.5,97.5])
        summary[typ]={
           "n_original_independent_source_plant_labels":x["n_original_distinct_source_plant_labels"],
           "source_observed_treatment":x["raw_cross_vs_self"],
           "original_flower_risk_difference_cross_minus_self":x["risk_difference_cross_minus_self"],
           "source_original_year_block_treatment_overlap":x["source_year_block_coverage"],
           "n_source_year_block_strata_with_both_treatments":x["source_original_sites_with_both_cross_and_self"],
           "original_source_site_overlapping_flower_fraction":x["source_overlapping_site_fraction_of_cross_self_flower_rows"],
           "source_year_block_harmonic_weighted_risk_difference":x["source_harmonic_weighted_original_site_cross_self_risk_difference"],
           "source_plant_label_bootstrap95":[float(boot_ci[0]),float(boot_ci[1])],
           "source_plant_label_bootstrap_interval_excludes_zero":
             bool(boot_ci[0]>0 or boot_ci[1]<0),
        }
    dif0=(summary[RABBITEYE_TYPE]["original_flower_risk_difference_cross_minus_self"]-
          .5*(summary["Blue Rose"]["original_flower_risk_difference_cross_minus_self"]+
              summary["Snowchaser"]["original_flower_risk_difference_cross_minus_self"]))
    bci=np.percentile(contrast,[2.5,97.5])
    return {
       "source_study_papers":1,
       "original_cross_self_flower_rows":len(sub),
       "n_requested_cluster_bootstrap":boot,
       "n_valid_cluster_bootstrap":len(contrast),
       "n_source_bootstrap_rejected_missing_treatment":fails,
       "three_cultivar_type_reproduction":summary,
       "rabbiteye_minus_mean_highbush_cross_self_risk_difference":dif0,
       "rabbiteye_vs_highbush_cluster_bootstrap95":[float(bci[0]),float(bci[1])],
       "rabbiteye_vs_highbush_bootstrap_CI_excludes_zero":
         bool(bci[0]>0 or bci[1]<0),
       "source_type_not_randomly_assigned_or_mating_system_identified":True,
       "experimental_pollen_source_treatment_not_heritable_self_compatibility_causal_effect":True,
    }


def visit_source(rows):
    """Empirical flower risk set and plant-cluster-aware binomial slopes.

    Primary analysis restricts the observed 0-5 visit support, avoiding
    extrapolation from sparse high-count 6-15 visit cells. Positive-only
    1-5 visits is separately fitted to distinguish zero-exposure contrasts
    from incremental visits.
    """
    import statsmodels.api as sm
    from scipy.stats import chi2,norm
    if np is None:raise RuntimeError("source numpy dependency missing")
    if len(rows)!=2080:raise ValueError("Original 2020 multiple-visit count changed")
    values=Counter(_visit_count(x) for x in rows)
    if dict(values)!={0:769,1:331,2:272,3:205,4:142,5:130,
                     6:32,7:36,8:33,9:23,10:27,11:16,
                     12:10,13:7,14:3,15:44}:
        raise ValueError("Source original 0-15 visit distribution changed")
    binned=[]
    for typ in SOURCE_TYPES:
        for a,b,name in VISIT_BINS:
            subset=[x for x in rows if x["Species"].strip()==typ and
                    a<=_visit_count(x)<=b]
            if not subset:
                binned.append({"blueberry_type":typ,"visit_bin":name,
                               "n_tagged_flowers":0,"n_set_fruit":0,
                               "observed_source_flower_fruit_rate":None})
                continue
            k=sum(fruit(x) for x in subset)
            binned.append({"blueberry_type":typ,"visit_bin":name,
                           "n_tagged_flowers":len(subset),"n_set_fruit":k,
                           "observed_source_flower_fruit_rate":k/len(subset)})
    fits={}
    for lower in (0,1):
        sub=[x for x in rows if lower<=_visit_count(x)<=5]
        names=sorted({
            "|".join((x["Species"].strip(),x["Year"].strip(),x["Block"].strip()))
            for x in sub})
        site_ix={s:i for i,s in enumerate(names)}
        X=np.zeros((len(sub),len(names)+3))
        y=np.empty(len(sub),int)
        labels=[]
        source_counts=Counter()
        for i,r in enumerate(sub):
            typ=r["Species"].strip()
            site="|".join((typ,r["Year"].strip(),r["Block"].strip()))
            X[i,site_ix[site]]=1
            X[i,len(names)+SOURCE_TYPES.index(typ)]=math.log1p(_visit_count(r))
            y[i]=fruit(r)
            labels.append(plant_key(r))
            source_counts[typ]+=1
        if np.linalg.matrix_rank(X)!=X.shape[1]:
            raise ValueError("Original source site-intercept/visit treatment design not full rank")
        if len(set(labels))<100:raise ValueError("Source plant labels too few for clustered regression")
        fit=sm.GLM(y,X,family=sm.families.Binomial()).fit(
            maxiter=300,cov_type="cluster",cov_kwds={"groups":labels})
        if not fit.converged:raise ValueError("Source visit-fruit binomial model not converged")
        b=np.asarray(fit.params);c=np.asarray(fit.cov_params())
        slopes={}
        for j,typ in enumerate(SOURCE_TYPES):
            ix=len(names)+j
            se=math.sqrt(max(0,c[ix,ix]))
            if se<=0:raise ValueError("Source cluster standard error invalid")
            slopes[typ]={
               "source_flower_rows":source_counts[typ],
               "source_plant_cluster_count":len(set(plant_key(x) for x in sub
                                               if x["Species"].strip()==typ)),
               "slope_log1plus_visits_to_log_odds_fruit":float(b[ix]),
               "plant_label_cluster_robust_SE":se,
               "nominal_two_sided_P":float(2*norm.sf(abs(b[ix]/se))),
               "nominal_95_interval":[float(b[ix]-1.96*se),float(b[ix]+1.96*se)],
            }
        # Direct contrast between the Powder Blue slope and the average of
        # Blue Rose & Snowchaser slope (each is one cultivar, not n species).
        v=np.zeros(len(b))
        v[len(names)+SOURCE_TYPES.index(RABBITEYE_TYPE)]=1.
        for typ in HIGHBUSH_TYPES:
            v[len(names)+SOURCE_TYPES.index(typ)]=-.5
        delta=float(v@b)
        sd=math.sqrt(float(v@c@v))
        if not math.isfinite(sd) or sd<=0:raise ValueError("Source slope difference variance invalid")
        # Test all three site-adjusted slopes equal.
        L=np.zeros((2,len(b)))
        L[0,len(names)+1]=1;L[0,len(names)+0]=-1
        L[1,len(names)+2]=1;L[1,len(names)+0]=-1
        V=L@c@L.T
        if np.linalg.matrix_rank(V)!=2:raise ValueError("Source slope heterogeneity covariance singular")
        wald=float((L@b)@np.linalg.solve(V,L@b))
        fits[("visits_0to5" if lower==0 else "visits_1to5")]={
           "n_original_flower_rows":len(sub),
           "n_source_independent_plant_ID_labels":len(set(labels)),
           "n_original_species_type_programmes":1,
           "n_source_site_intercepts":len(names),
           "original_source_visit_support":[lower,5],
           "source_CI_status":"plant_label_cluster_robust_binomial_logit",
           "site_fixed_intercepts":True,
           "source_blueberry_type_visit_logit_slopes":slopes,
           "rabbiteye_vs_equal_highbush_logvisit_slope_contrast":delta,
           "rabbiteye_vs_highbush_slope_contrast_nominal_P":
             float(2*norm.sf(abs(delta/sd))),
           "rabbiteye_vs_highbush_slope_contrast_cluster_95CI":
             [delta-1.96*sd,delta+1.96*sd],
           "all_three_slopes_equal_Wald_chi2":wald,
           "all_three_slopes_equal_Wald_chi2_df":2,
           "all_three_slopes_equal_nominal_P":float(chi2.sf(wald,2)),
        }
    return {
       "original_2080_matched_flower_visit_distribution":dict(values),
       "original_source_binned_visit_to_fruit_raw_risks":binned,
       "site_and_plant_cluster_aware_binomial_models":fits,
       "visitor_taxon_and_blueberry_cultivar_type_confounded_in_study":True,
       "visit_number_not_a_measured_compatible_pollen_grain_exposure":True,
       "no_pre_registered_confirmatory_visit_threshold_detected":True,
    }


def run(source_folder,boot=B_BOOT):
    source={}
    for typ in FILENAMES:
        records,meta,sha=raw_source(source_folder,typ)
        source[typ]={"rows":records,"schema":meta,"sha256":sha}
    visit=visit_source(source["multiple"]["rows"])
    pollination=pollination_source_risk_differences(
       source["pollination"]["rows"],boot=boot)
    original_receipt={
      k:{
         "file":FILENAMES[k],"sha256":source[k]["sha256"],
         "n_tagged_flower_rows":len(source[k]["rows"]),
         "n_original_flower_composite_keys_unique":
           source[k]["schema"]["n_composite_flower_identity_unique"],
         "n_original_source_plant_cluster_labels":len(set(
             plant_key(r) for r in source[k]["rows"])),
      } for k in FILENAMES
    }
    return {
      "analysis":"sch_blueberry_2020_same_tagged_flower_visitation_fruit_gate_v1",
      "source_article_DOI":DOI,
      "source_zenodo_record_id":SOURCE_RECORD_ID,
      "source_original_Dryad_DOI":"10.5061/dryad.tmpg4f4wj",
      "n_independent_source_research_programmes":1,
      "original_source_file_receipts":original_receipt,
      "n_original_source_files":3,
      "original_visit_count_to_same_flower_fruit_set":visit,
      "original_same_flower_hand_cross_versus_self_fruit_set":pollination,
      "covariates_and_visit_count_not_randomized_causal_compatibility":True,
      "site_and_year_nested_original_cultivar_design_not_randomized":True,
      "no_individual_flower_pollen_deposition_or_fertilization_measured":True,
      "no_SCH_pure_function_optima_or_empirical_loss_L":True,
      "critical_limits":[
          "original_2020_single_published_study_three_files_not_independent_studies",
          "source_tagged_flower_is_outcome_unit_plant_cluster_is_uncertainty_unit",
          "cultivar_type_not_experimentally_randomized_to_compatibility_state",
          "source_mating_system_cultivar_year_block_alternatives_not_fully_separable",
          "visitor_type_differs_across_blueberry_cultivars_and_visit_regimes",
          "visit_zero_bagged_controls_not_positive_visits_from_an_identical_visitation_mechanism",
          "no_direct_compatible_pollen_count_pollen_tube_or_same_flower_fertilization_measured",
          "visitor_effectiveness_does_not_measure_direct_trait_specific_causal_optima",
          "original_fruit_set_binary_not_mature_seed_survival_or_descendant_fitness",
          "bootstrap_and_logistic_Wald_CIs_are_exploratory_and_do_not_control_source_multiplicity",
      ],
      "status":"REAL_ZENODO_AUTHENTIC_TAGGED_FLOWER_FRUIT_SET_AND_COMPATIBILITY_GATE_REANALYSIS",
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source_dir",type=Path,
                   default=Path("artifacts/sch_original_blueberry_flower"))
    p.add_argument("--out",type=Path,
                   default=Path("artifacts/sch_original_blueberry_flower/gate_reanalysis.json"))
    p.add_argument("--bootstrap",type=int,default=B_BOOT)
    a=p.parse_args()
    result=run(a.source_dir,a.bootstrap)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",
                     encoding="utf-8")
    print("BEGIN_SCH_ORIGINAL_BLUEBERRY_GATE_REANALYSIS")
    print(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False))
    print("END_SCH_ORIGINAL_BLUEBERRY_GATE_REANALYSIS")


if __name__=="__main__":
    main()

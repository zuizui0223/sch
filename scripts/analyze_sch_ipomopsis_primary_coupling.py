"""Original-data exploratory test of within-cohort reproductive-stage coupling.

SOURCE: Campbell et al. public original Ipomopsis dataset 10.7280/D1KM49,
Zenodo record 5083399, source CSV MD5 12ed3dbe6d269c5f808f9c6b230d468c.

Research hypothesis, fixed before viewing individual-row coefficient estimates:
Does within-site/year/type matching of original plant seed initiation and
FRUIT-level escape yield an excess/deficit in the product proxy compared to
the same stage marginals independently paired within those strata?

Importantly, escape is fraction of FRUITS, not SEED survival. The product
P_i = initiated_seeds_i * fruit_escape_fraction_i is only a proxy. The
reported total-seeds variable does NOT obey this identity in most plants,
and 40/375 matched rows can exceed initial seeds. Never interpret the
proxy as observed final viable seed fitness, or as a causal functional L.

Primary statistic C (dimensionless), averaged EQUALLY across eligible
original site × year × plant-type cohorts (>=8 stage-complete rows):
   Irelative_i = I_i / mean(I within cohort)
   C_cohort = mean(Irelative_i * escape_i) - mean(escape)
Null: plant-level stages randomly paired within each source cohort.
A conditional within-cohort permutation (default 4999 iterations) tests
C=0 under exchangeability of plant escape values; this is not population
randomization or confirmation of a natural selection mechanism.

Secondary, two-sided test (same family of 2 tests): within each cohort,
split non-tied corolla width below/above its original median; retain
cohorts with >=3 observations in EACH bin. Compare the two within-bin
coupling terms (high-width minus low-width). Shuffles preserve width-bin
marginals and cohort, so they target coupling, not mean stage selection.
Use simple two-hypothesis Bonferroni p values. Stage-proxy selection
differences are compared to source-measured final seed direction only
descriptively. Year-cluster bootstrap and leave-year-out are sensitivities.

This is a post-publication observational reanalysis of genuine raw data,
not independent experimental validation of a general ecological law.
It is not a causal effect of the floral trait, the predator, or the consumer
regime; source plants were not randomly assigned to trait values.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import defaultdict, Counter
from pathlib import Path

from scripts.audit_sch_ipomopsis_source_grain import read, _num

SOURCE_DOI="10.7280/D1KM49"
SRC_FIELDS=("Site","Year","Type")
PRIMARY_MIN_N=8
SECONDARY_BIN_MIN_N=3
SEED=20261028


def mean(values: list[float])->float:
    if not values:
        raise ValueError("empty original-data estimator")
    return math.fsum(values)/len(values)


def covariance(a:list[float],b:list[float])->float:
    if len(a)!=len(b) or not a:
        raise ValueError("paired samples required for stage covariance")
    av,bv=mean(a),mean(b)
    return mean([(x-av)*(y-bv) for x,y in zip(a,b)])


def normalize_initiation(cohort:list[dict])->list[float]:
    m=mean([r["init"] for r in cohort])
    if m<=0:
        raise ValueError("zero-mean stage initiation cohort")
    return [r["init"]/m for r in cohort]


def stage_coupling(cohort:list[dict],permuted_escape:list[float]|None=None)->float:
    initiative=normalize_initiation(cohort)
    escape=permuted_escape if permuted_escape is not None else [r["escape"] for r in cohort]
    return covariance(initiative,escape)


def eligible_groups(original:list[dict[str,str]],min_n:int=PRIMARY_MIN_N)->tuple[list[dict],dict]:
    groups=defaultdict(list)
    excluded_counts=Counter()
    for row in original:
        key=tuple(row[x] for x in SRC_FIELDS)
        i=_num(row["seedsinit"])
        e=_num(row["flyescape"])
        width=_num(row["width"])
        final=_num(row["seeds"])
        if i is None or e is None:
            excluded_counts["incomplete_stage_pair"]+=1
            continue
        if i<0 or e<0 or e>1:
            raise ValueError("impossible original stage measurement")
        groups[key].append({"init":i,"escape":e,"width":width,"final":final})
    included=[]
    for key,rows in sorted(groups.items()):
        if len(rows)<min_n:
            excluded_counts["in_small_group"]+=len(rows)
            continue
        if mean([x["init"] for x in rows])==0:
            excluded_counts["all_zero_initiation"]+=len(rows)
            continue
        included.append({"key":key,"rows":rows,"n":len(rows)})
    return included,dict(sorted(excluded_counts.items()))


def width_split_group(rows:list[dict],minimum:int=SECONDARY_BIN_MIN_N)->dict|None:
    candidates=[r for r in rows if r["width"] is not None]
    if len(candidates)<2*minimum:
        return None
    midpoint=statistics.median([r["width"] for r in candidates])
    lo=[r for r in candidates if r["width"]<midpoint]
    hi=[r for r in candidates if r["width"]>midpoint]
    tied=len(candidates)-len(lo)-len(hi)
    if len(lo)<minimum or len(hi)<minimum:
        return None
    # Normalization across the SAME original cohort; independent of trait bin.
    norm=mean([r["init"] for r in candidates])
    if norm<=0: return None
    def pieces(group):
        I=[x["init"]/norm for x in group]
        e=[x["escape"] for x in group]
        return {"n":len(group),"mean_I":mean(I),
                "mean_e":mean(e),"mean_product":mean([a*b for a,b in zip(I,e)]),
                "coupling":covariance(I,e)}
    high,low=pieces(hi),pieces(lo)
    observed=high["mean_product"]-low["mean_product"]
    marginals=high["mean_I"]*high["mean_e"]-low["mean_I"]*low["mean_e"]
    covdiff=high["coupling"]-low["coupling"]
    if abs(observed-marginals-covdiff)>1e-9:
        raise AssertionError("exact within-cohort covariance identity failed")
    finalhi=[x["final"] for x in hi if x["final"] is not None]
    finallo=[x["final"] for x in lo if x["final"] is not None]
    measured=(mean(finalhi)-mean(finallo)
              if len(finalhi)>=minimum and len(finallo)>=minimum else None)
    return {"width_median":midpoint,"n_width_tied_dropped":tied,
            "low":lo,"high":hi,"high_stats":high,"low_stats":low,
            "coupling_delta_high_minus_low":covdiff,
            "proxy_stage_response_high_minus_low":observed,
            "independent_marginal_stage_prediction_delta":marginals,
            "measured_final_seeds_high_minus_low":measured,
            "proxy_and_final_seed_sign_agree":(
                (observed>0)==(measured>0)
                if measured is not None and abs(observed)>1e-12 and abs(measured)>1e-12
                else None)}


def _sign(x:float)->str:
    if x>1e-12:return "POSITIVE"
    if x<-1e-12:return "NEGATIVE"
    return "NEAR_ZERO"


def _quantile(sorted_data:list[float],prob:float)->float:
    if not sorted_data:return float("nan")
    x=prob*(len(sorted_data)-1)
    a,b=int(math.floor(x)),int(math.ceil(x))
    return sorted_data[a]*(b-x)+sorted_data[b]*(x-a) if a!=b else sorted_data[a]


def analyze(original:list[dict[str,str]], *, permutations:int=4999,
            bootstraps:int=3000, seed:int=SEED)->dict:
    if len(original)!=437:
        raise ValueError("original public archive must have 437 rows")
    if permutations<99 or bootstraps<99:
        raise ValueError("insufficient Monte Carlo resolution")
    cohorts,excluded=eligible_groups(original)
    if len(cohorts)<5:
        raise ValueError("cohort replication too low for registered analysis")
    for c in cohorts:
        c["normalized_coupling"]=stage_coupling(c["rows"])
        c["width"]=width_split_group(c["rows"])
    primary=mean([c["normalized_coupling"] for c in cohorts])
    secondary_cohorts=[c for c in cohorts if c["width"] is not None]
    if len(secondary_cohorts)<5:
        raise ValueError("too few eligible corolla width cohorts")
    secondary=mean([c["width"]["coupling_delta_high_minus_low"]
                    for c in secondary_cohorts])
    rng=random.Random(seed)
    extreme_primary=extreme_secondary=0
    for _ in range(permutations):
        Cp=[]
        Cs=[]
        for c in cohorts:
            x=[r["escape"] for r in c["rows"]]
            rng.shuffle(x)
            Cp.append(stage_coupling(c["rows"],x))
            if c["width"] is not None:
                w=c["width"]
                # Retain the two observed width bins and their source mean
                # values. Break only the within-bin I × escape pairing.
                lo,hi=w["low"],w["high"]
                l_esc=[v["escape"] for v in lo]
                h_esc=[v["escape"] for v in hi]
                rng.shuffle(l_esc);rng.shuffle(h_esc)
                norm=mean([r["init"] for r in c["rows"] if r["width"] is not None])
                lI=[v["init"]/norm for v in lo]
                hI=[v["init"]/norm for v in hi]
                Cs.append(covariance(hI,h_esc)-covariance(lI,l_esc))
        if abs(mean(Cp))>=abs(primary)-1e-13:extreme_primary+=1
        if abs(mean(Cs))>=abs(secondary)-1e-13:extreme_secondary+=1
    p_primary=(extreme_primary+1)/(permutations+1)
    p_secondary=(extreme_secondary+1)/(permutations+1)
    # Bootstrap entire year blocks, not 437 individual plants or 15
    # allegedly independent cohort units. Eight eligible years are still not a
    # broad regional/geographic sampling frame.
    years=sorted({c["key"][1] for c in cohorts})
    byyear={year:[c for c in cohorts if c["key"][1]==year] for year in years}
    bootp,boots=[],[]
    for _ in range(bootstraps):
        draw=[rng.choice(years) for _ in years]
        cs=[c for y in draw for c in byyear[y]]
        if not cs:continue
        bootp.append(mean([c["normalized_coupling"] for c in cs]))
        cw=[c for c in cs if c["width"] is not None]
        if cw:
            boots.append(mean([c["width"]["coupling_delta_high_minus_low"]
                               for c in cw]))
    bootp.sort();boots.sort()
    looy={
        year:mean([c["normalized_coupling"] for c in cohorts if c["key"][1]!=year])
        for year in years
        if any(c["key"][1]!=year for c in cohorts)
    }
    site_summary={}
    for site in sorted({c["key"][0] for c in cohorts}):
        s=[c for c in cohorts if c["key"][0]==site]
        site_summary[site]={
            "n_site_year_type_cohorts":len(s),
            "n_matched_stage_rows":sum(c["n"] for c in s),
            "equal_cohort_mean_normalized_coupling":mean([c["normalized_coupling"] for c in s]),
            "site_is_not_an_independent_taxonomic_replicate":True,
        }
    stage_output=[]
    for c in cohorts:
        w=c["width"]
        stage_output.append({
            "site":c["key"][0],"year":int(c["key"][1]),"type":c["key"][2],
            "n_matched_stage_rows":c["n"],
            "normalized_stage_coupling":c["normalized_coupling"],
            "with_width_secondary":w is not None,
            "width_coupling_difference":(w["coupling_delta_high_minus_low"] if w else None),
            "width_proxy_stage_difference":(w["proxy_stage_response_high_minus_low"] if w else None),
            "width_independence_prediction_difference":(
                w["independent_marginal_stage_prediction_delta"] if w else None),
            "width_stage_sign_difference":(
                _sign(w["proxy_stage_response_high_minus_low"])!=
                _sign(w["independent_marginal_stage_prediction_delta"])
                if w else None),
            "measured_final_seeds_high_minus_low":(
                w["measured_final_seeds_high_minus_low"] if w else None),
            "proxy_and_measured_seed_sign_agree":(
                w["proxy_and_final_seed_sign_agree"] if w else None),
            "width_median_excluded_ties":(w["n_width_tied_dropped"] if w else None),
        })
    signs=[c["width"]["proxy_and_final_seed_sign_agree"]
           for c in secondary_cohorts
           if c["width"]["proxy_and_final_seed_sign_agree"] is not None]
    flip=[c for c in stage_output if c["width_stage_sign_difference"]]
    return {
        "analysis":"sch_ipomopsis_original_raw_within_cohort_fruit_escape_coupling_v1",
        "original_data_doi":SOURCE_DOI,
        "source_original_n_rows":len(original),
        "original_site_year_type_stratification":True,
        "registered_primary":(
            "equal_weight_mean_within_cohort_covariance_of_relative_seed_"
            "initiation_and_fruit_escape_fraction"
        ),
        "registered_secondary":(
            "equal_weight_high_minus_low_coupling_delta_within_corolla_"
            "width_median_strata_excluding_exact_width_ties"
        ),
        "n_cohorts_eligible":len(cohorts),
        "n_eligible_original_year_blocks":len(years),
        "n_cohorts_secondary":len(secondary_cohorts),
        "n_matched_rows_primary":sum(c["n"] for c in cohorts),
        "n_matched_rows_secondary":sum(
            len(c["width"]["low"])+len(c["width"]["high"])
            for c in secondary_cohorts),
        "excluded_rows":excluded,
        "n_independent_study_programmes":1,
        "primary_normalized_mean_coupling":primary,
        "primary_normalized_mean_coupling_direction":_sign(primary),
        "primary_within_cohort_shuffle_p_two_sided":p_primary,
        "primary_familywise_two_test_adjusted_p":min(1,2*p_primary),
        "secondary_width_coupling_delta":secondary,
        "secondary_width_coupling_delta_direction":_sign(secondary),
        "secondary_shuffle_p_two_sided":p_secondary,
        "secondary_familywise_two_test_adjusted_p":min(1,2*p_secondary),
        "n_permutations":permutations,
        "fixed_random_seed":seed,
        "original_year_block_resampling_ci_95pct_primary":(
            [_quantile(bootp,.025),_quantile(bootp,.975)]),
        "original_year_block_resampling_ci_95pct_secondary":(
            [_quantile(boots,.025),_quantile(boots,.975)]),
        "leave_one_year_out_primary":looy,
        "per_source_site_summary":site_summary,
        "n_width_cohorts_where_stage_proxy_sign_differs_from_marginal_prediction":len(flip),
        "n_width_cohorts_with_observed_final_seed_direction_check":len(signs),
        "n_width_cohorts_proxy_and_measured_final_seed_sign_agree":sum(signs),
        "cohort_effects":stage_output,
        "interpretive_limits":[
            "original_archived_individual_rows_not_author_generated_new_fieldwork",
            "observational_floral_width_not_randomized",
            "site_year_type_groups_are_not_independent_species_or_experiments",
            "year_bootstrap_only_eight_eligible_year_blocks_in_one_original_study",
            "primary_permutation_conditions_on_within_cohort_exchangeability",
            "fruit_escape_is_proportion_of_fruits_not_seed_survival",
            "initiated_times_escape_is_a_labelled_proxy_not_real_final_seeds",
            "original_seed_count_can_exceed_reported_initiated_estimate",
            "stage_covariance_not_a_proof_of_causal_phenotype_selection",
            "no_crossed_trait_by_pollinator_by_predator_intervention",
            "no_empirically_estimated_SCH_L_or_pure_function_optima",
        ],
        "status":"ORIGINAL_RAW_ARCHIVAL_REANALYSIS_CONDITIONAL_COUPLING_TESTED",
    }


def main()->None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--output",type=Path)
    ap.add_argument("--permutations",type=int,default=4999)
    ap.add_argument("--bootstraps",type=int,default=3000)
    args=ap.parse_args()
    receipt=analyze(read(args.source),permutations=args.permutations,
                    bootstraps=args.bootstraps)
    payload=json.dumps(receipt,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    print("BEGIN_SCH_ORIGINAL_IPOMOPSIS_COUPLING_RESULT")
    print(payload)
    print("END_SCH_ORIGINAL_IPOMOPSIS_COUPLING_RESULT")


if __name__=="__main__":
    main()

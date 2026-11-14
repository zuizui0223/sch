"""Source-backed inferential-resolution audit for 2020 plant functional-trait meta.

All biological numeric inputs come from the 137-line ORIGINAL MASTER PAIR
ledger already source-hash checked and CI tested in PR239 (Dryad DOI
10.5061/dryad.sn02v6x0q). This pass does not add species or count the
author's intentionally duplicated workbook as additional data.

Primary scientific question:
Among observed beta sign changes in the same original study/trait/
fitness year/population, how many are both-slope supported by source
marginal SEs, and how much additional precision would be needed for
the SAME SOURCE POINT ESTIMATES to meet a per-arm 95% threshold?

A sample size "multiplier" is a purely arithmetic information HEURISTIC,
not a credible field sample-size forecast, causal power calculation,
confidence interval, or posterior probability of a true reversal.
Assumes both beta point estimates unchanged and SE proportional to n^-1/2,
which cannot be guaranteed when original study context/variance changes.

No inferential significance is assigned to n=137 case fractions: original
paper n=26 is the independent publication unit, 15 with ≥1 point crossing.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data/SCH_2020_FUNCTIONAL_META_MATCHED_ORIGINAL_PAIRS_V1.csv"
PARENT=ROOT/"data/SCH_2020_FUNCTIONAL_META_EXPERIMENTAL_READOUT_V1.json"
Z95=1.96
LEVELS=(2,4,8,16,25,100)
FIELDS=("paper_id","source_row_id_1","source_row_id_2","trait_class",
        "agent_category","point_sign_flip","beta1","beta2","se1","se2")


def read(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8",newline="") as f:
        return list(csv.DictReader(f))


def quantile(vals:list[float],p:float)->float:
    if not vals or p<0 or p>1:raise ValueError("invalid quantile")
    vs=sorted(vals)
    x=p*(len(vs)-1)
    lo,hi=math.floor(x),math.ceil(x)
    return vs[lo]+(vs[hi]-vs[lo])*(x-lo)


def inspect(rows:list[dict[str,str]],receipt:dict)->dict:
    if len(rows)!=137 or receipt["eligible_matched_pair_total"]!=137:
        raise ValueError("PR239 137-row original master pairing receipt required")
    if {x["paper_id"] for x in rows}.__len__()!=26:
        raise ValueError("26 original independent publications required")
    paper_groups=defaultdict(list)
    seen_ids=set()
    flipped=[]
    classified=[]
    for row in rows:
        if any(k not in row for k in FIELDS):
            raise ValueError("original matched-source schema missing")
        paper=row["paper_id"]
        pair=(row["source_row_id_1"],row["source_row_id_2"])
        if any(x in seen_ids for x in pair) or pair[0]==pair[1]:
            raise ValueError("same source gradient row used in two comparisons")
        seen_ids.update(pair)
        first,second,se1,se2=[float(row[k]) for k in ("beta1","beta2","se1","se2")]
        if any(not math.isfinite(x) for x in (first,second,se1,se2)) or min(se1,se2)<=0:
            raise ValueError("original published source coefficient or SE invalid")
        sign_first=(first>0)-(first<0)
        sign_second=(second>0)-(second<0)
        source_flip=(sign_first*sign_second)<0
        if source_flip != (row["point_sign_flip"].lower()=="true"):
            raise ValueError("registered published-master sign flip classification drift")
        z1,z2=abs(first/se1),abs(second/se2)
        positive95=z1>Z95
        negative95=z2>Z95
        status=("BOTH_OPPOSITE_SOURCE_SUPPORTED" if positive95 and negative95 else
                "ONE_ARM_SOURCE_SUPPORTED" if positive95 or negative95 else
                "NEITHER_ARM_SOURCE_SUPPORTED") if source_flip else "NOT_A_SIGN_CROSSING"
        item={
            "paper_id":paper,"authors":row.get("authors"),
            "species":row.get("species"),"trait":row.get("trait"),
            "trait_class":row["trait_class"],"agent_category":row["agent_category"],
            "source_original_row_ids":[*pair],
            "source_point_sign_crossing":source_flip,
            "abs_z_1":z1,"abs_z_2":z2,
            "precision_class":status,
        }
        if source_flip:
            if min(z1,z2)<=0:raise ValueError("source sign crossing with zero gradient")
            # Information multiplier if BOTH SOURCE POINT estimates remain
            # unchanged and only their Gaussian SEs shrink by sqrt(nfactor).
            hypothetical_n_factor=(Z95/min(z1,z2))**2
            item["hypothetical_sample_information_multiplier_to_two_source_signs"]=hypothetical_n_factor
            item["min_source_arm_abs_z"]=min(z1,z2)
            flipped.append(item)
        paper_groups[paper].append(item)
        classified.append(item)
    if len(seen_ids)!=274:
        raise ValueError("274 unique original paired source coefficient rows required")
    if len(flipped)!=receipt["all_source_point_sign_flips"]:
        raise ValueError("source 2020 original 41 crossings changed")
    counts=Counter(x["precision_class"] for x in flipped)
    required_n=[v["hypothetical_sample_information_multiplier_to_two_source_signs"]
                for v in flipped]
    bytrait={}
    for trait in sorted({x["trait_class"] for x in classified}):
        group=[x for x in classified if x["trait_class"]==trait]
        bytrait[trait]={
            "n_source_pairs":len(group),
            "n_original_papers":len({x["paper_id"] for x in group}),
            "n_point_crossings":sum(x["source_point_sign_crossing"] for x in group),
            "n_both_arm_source_supported_crossings":sum(
                x["precision_class"]=="BOTH_OPPOSITE_SOURCE_SUPPORTED" for x in group),
        }
    byagent={}
    for agent in sorted({x["agent_category"] for x in classified}):
        group=[x for x in classified if x["agent_category"]==agent]
        byagent[agent]={
            "n_source_pairs":len(group),
            "n_original_papers":len({x["paper_id"] for x in group}),
            "n_point_crossings":sum(x["source_point_sign_crossing"] for x in group),
            "n_neither_arm_supported":sum(
                x["precision_class"]=="NEITHER_ARM_SOURCE_SUPPORTED" for x in group),
            "n_one_arm_supported":sum(
                x["precision_class"]=="ONE_ARM_SOURCE_SUPPORTED" for x in group),
        }
    papers_with_flips=[p for p,v in paper_groups.items() if any(
        x["source_point_sign_crossing"] for x in v)]
    # Only the count across 26 independent published SOURCE papers is a
    # study-grain denominator; case fraction is not world-flora prevalence.
    paper_records=[{
        "paper_id":key,"authors":values[0]["authors"],
        "n_original_trait_context_pairs":len(values),
        "n_point_crossings":sum(v["source_point_sign_crossing"] for v in values),
        "n_neither_arm_supported_crossings":sum(
            v["precision_class"]=="NEITHER_ARM_SOURCE_SUPPORTED" for v in values),
        "n_one_arm_supported_crossings":sum(
            v["precision_class"]=="ONE_ARM_SOURCE_SUPPORTED" for v in values),
        "n_both_arm_supported_crossings":sum(
            v["precision_class"]=="BOTH_OPPOSITE_SOURCE_SUPPORTED" for v in values),
    } for key,values in sorted(paper_groups.items(),key=lambda v:int(v[0]))]
    out={
        "analysis":"sch_2020_original_source_meta_point_sign_resolution_v1",
        "original_source_DOI":"10.5061/dryad.sn02v6x0q",
        "original_experimental_master_MD5":"7f680c344c0a418a3d8742649de24d52",
        "n_complete_paired_source_gradients":len(rows),
        "n_original_independent_papers":len(paper_groups),
        "n_original_independent_papers_with_one_or_more_point_flips":len(papers_with_flips),
        "n_source_point_crossings":len(flipped),
        "n_crossings_with_two_nominally_supported_opposite_slopes":counts[
            "BOTH_OPPOSITE_SOURCE_SUPPORTED"],
        "n_crossings_with_one_nominally_supported_slope":counts[
            "ONE_ARM_SOURCE_SUPPORTED"],
        "n_crossings_with_neither_slope_nominally_supported":counts[
            "NEITHER_ARM_SOURCE_SUPPORTED"],
        "source_95pct_two_sided_abs_z_threshold":Z95,
        "hypothetical_sample_information_multiplier_IF_source_betas_remain_fixed":{
            "median":quantile(required_n,.5),
            "q25":quantile(required_n,.25),
            "q75":quantile(required_n,.75),
            "min":min(required_n),
            "max":max(required_n),
            "n_below_or_equal_threshold":{str(k):sum(v<=k for v in required_n)
                                          for k in LEVELS},
            "n_exceed_100_fold_sample_information":sum(v>100 for v in required_n),
            "NOT_AN_EMPIRICAL_POWER_CALCULATION":True,
            "ASSUMES_SOURCE_POINT_BETAS_FIXED_AND_GAUSSIAN_SE_SQRT_N":True,
        },
        "trait_class_source_diagnostics":bytrait,
        "environmental_agent_source_diagnostics":byagent,
        "source_paper_diagnostics":paper_records,
        "point_crossing_source_record_diagnostics":flipped,
        "interpretive_boundaries":[
            "source_original_137_pairs_nonnumeric_diversity_has_no_world_pop_sampling_frame",
            "published_point_sign_crossing_not_a_detected_two_direction_reversal",
            "one_or_zero_significant_source_cells_do_not_prove_same_true_sign",
            "n_multiplies_only_math_SE_with_source_beta_unchanged_no_power_or_sample_size_plan",
            "original_26_studies_rather_than_137_gradients_are_independent_units",
            "study_and_year_fitness_and_trait_context_dependence_not_resolved",
            "original_Pvalues_may_disagree_with_normal_Wald_source_SEs",
            "none_identifies_causal_shared_trait_L_or_pure_function_optima",
        ],
        "status":"ORIGINAL_SOURCE_META_NO_INFERENTIALLY_SUPPORTED_SIGN_REVERSALS",
    }
    if counts["BOTH_OPPOSITE_SOURCE_SUPPORTED"]!=0:
        raise ValueError("prior original 2020 source result claiming zero supported reversals drifted")
    return out


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source-pairs",type=Path,default=SOURCE)
    p.add_argument("--source-receipt",type=Path,default=PARENT)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    j=inspect(read(args.source_pairs),
              json.loads(args.source_receipt.read_text(encoding="utf-8")))
    text=json.dumps(j,indent=2,sort_keys=True)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text,encoding="utf-8")
    else:
        print(text,end="")


if __name__=="__main__":
    main()

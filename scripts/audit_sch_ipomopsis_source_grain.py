"""Adjudicate ORIGINAL Ipomopsis individual-row grouping before inference.

No new biological effect estimated; checks exact group replication, missingness,
the relationship of the two distinct reproductive-stage endpoints, and
whether one plant-like source row can validly be used as a matched sample.

The stage variable flyescape is proportion of FRUITS escaping predation,
not seed survival. Consequently seedsinit*flyescape is only a labelled proxy
and must never be promoted to observed mature viable seeds.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

ORIGINAL_COLUMNS=(
    "Site","Year","Type","width","color","nectar","sepal",
    "totpinene","indoleN","seeds","seedsinit","flyescape",
)
EXPECTED_N=437
MISSING={"",".","NA","NaN","nan","N/A","null"}


def _num(value: str) -> float|None:
    if value.strip() in MISSING:
        return None
    number=float(value)
    if not math.isfinite(number):
        raise ValueError("nonfinite original ecological observation")
    return number


def read(path:Path)->list[dict[str,str]]:
    with path.open(encoding="utf-8-sig",newline="") as fh:
        reader=csv.DictReader(fh)
        if tuple(reader.fieldnames or ())!=ORIGINAL_COLUMNS:
            raise ValueError("archived Ipomopsis source schema unexpectedly changed")
        rows=list(reader)
    if len(rows)!=EXPECTED_N:
        raise ValueError("archived original row count changed")
    return rows


def build(rows:list[dict[str,str]])->dict:
    if len(rows)!=EXPECTED_N:
        raise ValueError("original archival row count unexpectedly changed")
    keys=("Site","Year","Type")
    grouper=defaultdict(list)
    for row in rows:
        key=tuple(row.get(k,"") for k in keys)
        if any(not x for x in key):
            raise ValueError("missing biological stratification field")
        if key[0] not in {"agg","hyb","ten"} or key[2] not in {"A","H","T"}:
            raise ValueError("unrecognized original study site/type")
        year=int(key[1])
        if not 2010<=year<=2018:
            raise ValueError("outside source years")
        for col in ORIGINAL_COLUMNS[3:]:
            value=_num(row.get(col,""))
            if col in ("seeds","seedsinit","width","nectar","sepal","totpinene","indoleN") and value is not None and value<0:
                raise ValueError("negative impossible biological measurement")
            if col=="flyescape" and value is not None and not 0<=value<=1:
                raise ValueError("fruit escape proportion out of unit interval")
        grouper[key].append(row)
    groups=[]
    n_total_complete=0
    mismatch_count=0
    exact_product_matches=0
    stage_n=0
    product_to_seeds=[]
    for key,subset in sorted(grouper.items()):
        original_n=len(subset)
        complete_stage=[
            (_num(x["seedsinit"]),_num(x["flyescape"]))
            for x in subset
            if _num(x["seedsinit"]) is not None
            and _num(x["flyescape"]) is not None
        ]
        complete_early_late=[
            (_num(x["seeds"]),_num(x["seedsinit"]),_num(x["flyescape"]))
            for x in subset
            if _num(x["seeds"]) is not None
            and _num(x["seedsinit"]) is not None
            and _num(x["flyescape"]) is not None
        ]
        with_width=sum(
            _num(x["seedsinit"]) is not None
            and _num(x["flyescape"]) is not None
            and _num(x["width"]) is not None
            for x in subset
        )
        for y,i,e in complete_early_late:
            stage_n+=1
            if y>i+1e-6:
                mismatch_count+=1
            if abs(y-i*e)<1e-4:
                exact_product_matches+=1
            product_to_seeds.append((i*e,y))
        n_total_complete+=len(complete_stage)
        groups.append({
            "site":key[0],"year":int(key[1]),"plant_type":key[2],
            "n_original_plant_rows":original_n,
            "n_joint_initiation_fruit_escape":len(complete_stage),
            "n_joint_stages_and_final_seeds":len(complete_early_late),
            "n_joint_stage_proxy_and_corolla_width":with_width,
            "eligible_stage_group_n_ge_8":len(complete_stage)>=8,
            "eligible_width_stage_group_n_ge_8":with_width>=8,
        })
    diffs=[abs(a-b) for a,b in product_to_seeds]
    return {
        "analysis":"sch_ipomopsis_original_plant_grain_and_stage_fit_audit_v1",
        "doi":"10.7280/D1KM49",
        "original_archive_n":len(rows),
        "source_stage_fate_variable":"flyescape",
        "source_stage_fate_definition":"proportion_of_fruits_escaping_seed_predation",
        "original_source_site_levels":dict(Counter(r["Site"] for r in rows)),
        "original_source_type_levels":dict(Counter(r["Type"] for r in rows)),
        "n_site_year_type_cohorts":len(groups),
        "n_stage_complete_rows":n_total_complete,
        "n_triples_including_final_seeds":stage_n,
        "n_final_seed_gt_seedinit_in_matched_triples":mismatch_count,
        "n_exact_seedinit_times_fruit_escape_matches":exact_product_matches,
        "mean_absolute_difference_seeds_minus_proxy":statistics.mean(diffs) if diffs else None,
        "median_absolute_difference_seeds_minus_proxy":statistics.median(diffs) if diffs else None,
        "n_cohorts_stage_n_ge_8":sum(g["eligible_stage_group_n_ge_8"] for g in groups),
        "n_cohorts_width_stage_n_ge_8":sum(g["eligible_width_stage_group_n_ge_8"] for g in groups),
        "cohorts":groups,
        "source_dataset_is_primary_open_field_rows":True,
        "rows_are_not_automatically_independent_of_year_site_or_genotype":True,
        "fruit_escape_is_not_seed_survival":True,
        "seedinit_times_fruit_escape_is_only_an_ecological_proxy":True,
        "no_selection_fit_or_ecological_generalization_yet":True,
        "status":"REAL_PRIMARY_PLANT_GRAIN_ADJUDICATED_ANALYSIS_NOT_YET_EXECUTED",
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path)
    args=p.parse_args()
    report=build(read(args.source))
    result=json.dumps(report,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(result,encoding="utf-8")
    print("BEGIN_SCH_IPOMOPSIS_REAL_COHORT_QC")
    print(result)
    print("END_SCH_IPOMOPSIS_REAL_COHORT_QC")


if __name__=="__main__":
    main()

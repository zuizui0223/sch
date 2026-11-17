"""Audit repeated flower IDs across THREE original 2020 blueberry source CSVs.

This is a source data-quality audit, not an additional biological experiment.
All original 2020 Kendall et al. JAE source files were verified at Zenodo
record 3987488 (Dryad 10.5061/dryad.tmpg4f4wj). Importantly, file and
observation counts DO NOT certify independence across source CSVs.

The exact source flower identity is qualified by cultivar type, year, block,
original field crop row, original plant number, original RP plant label and
the individual tagged-flower ID. Corresponding fruit-set binary outcomes,
pick dates and nonmissing ripe weights are checked on any cross-file match.
A match across experimental files MUST NOT be treated as an independent
biological replication.
"""
from __future__ import annotations

import argparse
from collections import Counter,defaultdict
from pathlib import Path
import json
import math

from scripts.analyze_sch_blueberry_2020_matched_flower_gate import (
    DOI,SOURCE_RECORD_ID,SOURCE_TYPES,raw_source,fruit,_visit_count,plant_key,
)

SOURCE_EXPECTED={
  "multiple":2080,"single":1309,"pollination":2125
}
COMPOSITE_FIELDS=("Species","Year","Block","RP","Tag")
OBSERVED_ID_FIELD="Tag"
SOURCE_REGIMES={
 "multiple_zero":("multiple",lambda r:_visit_count(r)==0),
 "multiple_one":("multiple",lambda r:_visit_count(r)==1),
 "single_unvisited":("single",lambda r:r["SPEC.COM"].strip()=="UP"),
 "single_one_visited":("single",lambda r:r["SPEC.COM"].strip() in ("HB","Other")),
 "pollination_no":("pollination",lambda r:r["TREATMENT"].strip()=="No pollination"),
}

def flower_identity(row):
    if any(k not in row for k in COMPOSITE_FIELDS):
        raise ValueError("Original source flower identity columns missing")
    values=tuple(str(row[x]).strip() for x in COMPOSITE_FIELDS)
    incomplete=[name for name,value in zip(COMPOSITE_FIELDS,values)
                if not value or value.lower() in ("na","nan","null")]
    if incomplete:
        raise ValueError("Original flower source core identity incomplete: "+
             f"missing_fields={incomplete} values={values}")
    return values

def strict_original_rows(rows,source):
    """Link only authentic nonmissing flower tags; never invent an ID for NA."""
    found={}
    missing=Counter()
    categories=Counter()
    for row in rows:
        fruit(row)
        try:
            key=flower_identity(row)
        except ValueError:
            missing["TAG_OR_CORE_ID_MISSING"]+=1
            code=(row.get("SPEC.COM") or row.get("TREATMENT") or
                  str(row.get("sumvisits",""))).strip()
            categories[(row["Species"].strip(),code)]+=1
            continue
        if key in found:
            raise ValueError("Original source flower repeated with full qualified tag in "+source)
        found[key]=row
    receipt={
        "original_file":source,
        "n_original_rows":len(rows),
        "n_full_tag_ID_linkable_rows":len(found),
        "n_flower_rows_with_incomplete_tag_or_core_ID":sum(missing.values()),
        "source_missing_key_reasons":dict(missing),
        "source_missing_tags_by_type_and_protocol":{
            "|".join(k):v for k,v in sorted(categories.items())
        },
        "crossfile_nonmatch_cannot_certify_flower_independence":bool(missing),
    }
    return found,receipt


def pair_overlap(a,b):
    aid=set(a)
    bid=set(b)
    joint=sorted(aid&bid)
    disagreement=[]
    uncertain=[]
    for identity in joint:
        x=a[identity];y=b[identity]
        if x["FS"].strip()!=y["FS"].strip():
            disagreement.append({"identity":identity,"field":"FS",
                                "source_a":x["FS"],"source_b":y["FS"]})
        # Compare only source columns shared by the two tables. Fruit
        # pick and fresh weight describe the same tagged flower if matched.
        for name in ("Row","Plant.number","Pick.date","Fresh.wgt","Date"):
            if name not in x or name not in y:
                continue
            vx=str(x[name]).strip()
            vy=str(y[name]).strip()
            if vx==vy or vx in ("","NA","NaN") or vy in ("","NA","NaN"):
                continue
            if name=="Fresh.wgt":
                try:
                    if math.isclose(float(vx),float(vy),rel_tol=1e-6,abs_tol=1e-7):
                        continue
                except ValueError:pass
            uncertain.append({"identity":identity,"field":name,
                              "source_a":vx,"source_b":vy})
    per=Counter(x[0] for x in joint)
    return {
      "original_source_a_rows":len(a),"original_source_b_rows":len(b),
      "source_flower_identity_matches":len(joint),
      "source_match_by_original_cultivar":dict(per),
      "n_identity_matched_FS_disagreements":len(disagreement),
      "n_identity_matched_date_or_weight_disagreements":len(uncertain),
      "examples_outcome_disagreement":disagreement[:10],
      "examples_nonoutcome_disagreement":uncertain[:10],
      "source_a_flower_keys_not_in_b":len(aid-bid),
      "source_b_flower_keys_not_in_a":len(bid-aid),
      "all_matched_fruit_outcomes_agree":len(disagreement)==0,
      "source_matched_data_not_independent":len(joint)>0,
    }

def run(folder):
    raw={}
    origins={}
    for name in SOURCE_EXPECTED:
        rows,schema,sha=raw_source(folder,name)
        if len(rows)!=SOURCE_EXPECTED[name]:
            raise ValueError("Original source file records changed "+name)
        raw[name],coverage=strict_original_rows(rows,name)
        origins[name]={
          **coverage,
          "source_file":name,"original_n_rows":len(rows),
          "source_original_SHA256":sha,
          "source_unique_tagged_flower_IDs":len(raw[name]),
          "source_original_plant_label_clusters":len(set(plant_key(r) for r in rows)),
        }
    subsets={}
    for regime,(file,predicate) in SOURCE_REGIMES.items():
        selected={k:r for k,r in raw[file].items() if predicate(r)}
        subsets[regime]=selected
    analyses={}
    for a,b in (
        ("multiple_zero","single_unvisited"),
        ("multiple_one","single_one_visited"),
        ("multiple_zero","pollination_no"),
        ("single_unvisited","pollination_no"),
        ("multiple_one","pollination_no"),
        ("multiple_zero","single_one_visited"),
    ):
        analyses[a+"__"+b]=pair_overlap(subsets[a],subsets[b])
    file_pairs={}
    names=list(SOURCE_EXPECTED)
    for i,a in enumerate(names):
        for b in names[i+1:]:
            file_pairs[a+"__"+b]=pair_overlap(raw[a],raw[b])
    global_ids=set().union(*(set(x) for x in raw.values()))
    common3=set.intersection(*(set(x) for x in raw.values()))
    many=defaultdict(list)
    for file,rows in raw.items():
        for key,r in rows.items():
            many[key].append(file)
    repeated=Counter(len(v) for v in many.values())
    by_source=Counter()
    for key,sources in many.items():
        if len(sources)>1:by_source[key[0]]+=1
    receipt={
      "analysis":"sch_2020_original_blueberry_three_csv_same_flower_identity_overlap_audit",
      "paper_DOI":DOI,
      "source_zenodo_record_id":SOURCE_RECORD_ID,
      "original_2020_published_programmes":1,
      "original_source_files":origins,
      "n_original_rows_summed_across_three_csvs":sum(SOURCE_EXPECTED.values()),
      "n_original_rows_with_full_original_tag_and_core_ID_across_three_files":
          sum(len(r) for r in raw.values()),
      "n_original_rows_not_linkable_across_three_files":
          sum(x["n_flower_rows_with_incomplete_tag_or_core_ID"] for x in origins.values()),
      "n_original_distinct_tagged_flower_composite_IDs_across_all_files":len(global_ids),
      "n_original_flower_IDs_present_in_all_three_files":len(common3),
      "number_of_original_CSVs_containing_each_distinct_flower_ID":dict(repeated),
      "n_distinct_reused_flower_IDs_by_source_cultivar":dict(by_source),
      "file_pair_ID_comparisons":file_pairs,
      "treatment_role_flower_identity_comparisons":analyses,
      "single_visit_is_an_independent_raw_flower_sample_from_multiple_visits":
           (False if set(raw["single"])&set(raw["multiple"])
            else "UNRESOLVED_SOURCE_TAG_MISSING_CANNOT_PROVE_INDEPENDENCE"),
      "all_independence_and_replication_claims_require_crossfile_qa":True,
      "source_raw_flower_rows_cannot_be_added_as_independent_biological_replicates":True,
      "no_new_independent_experiment_claim_without_nonoverlap":True,
      "stage_specific_causal_optimum_or_SCH_loss_L":False,
      "source_ID_linkage_is_partial_if_original_Tag_is_NA":True,
      "status":"CROSS_FILE_PARTIAL_ORIGINAL_TAG_ID_LINKAGE_NO_INDEPENDENCE_ASSUMPTION",
    }
    return receipt

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source",type=Path,default=Path("artifacts/sch_blueberry_single_visit_source"))
    p.add_argument("--out",type=Path,default=Path("artifacts/sch_blueberry_single_visit_source/crossfile_identity_overlap.json"))
    args=p.parse_args()
    r=run(args.source)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("BEGIN_SCH_BLUEBERRY_CROSSFILE_FLOWER_SOURCE")
    print(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False))
    print("END_SCH_BLUEBERRY_CROSSFILE_FLOWER_SOURCE")

if __name__=="__main__":
    main()

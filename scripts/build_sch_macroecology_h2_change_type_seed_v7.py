from __future__ import annotations
import argparse, csv, json
from collections import Counter
from pathlib import Path
ALLOWED={
 "GEOMETRY_CLASS_SWITCH","GEOMETRY_DISAPPEARANCE","COMPONENT_WEIGHT_SHIFT",
 "COMPONENT_WEIGHT_SHIFT_WITH_EVOLUTIONARY_RESPONSE","CONSUMER_ROLE_BEHAVIOR_SHIFT",
 "NET_SELECTION_CONTEXT_SHIFT","REPRODUCTIVE_COMPONENT_CONTEXT_SHIFT",
}
def _read(path):
    with path.open(encoding="utf-8",newline="") as h:
        rows=[]
        for r in csv.DictReader(h):
            if None in r: raise ValueError(f"malformed CSV {path}: {r[None]}")
            rows.append({k:(v or "").strip() for k,v in r.items()})
        return rows
def build(path):
    rows=_read(path); ids=[r["change_record_id"] for r in rows]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate change_record_id")
    bad=sorted({r["change_type"] for r in rows if r["change_type"] not in ALLOWED})
    if bad: raise ValueError("invalid change types: "+", ".join(bad))
    c=Counter(r["change_type"] for r in rows)
    return {
      "analysis":"sch_macroecology_h2_change_type_seed_v7",
      "n_change_records":len(rows),
      "n_canonical_axes":len({r["canonical_trait_axis_id"] for r in rows}),
      "change_type_counts":dict(sorted(c.items())),
      "n_change_records_with_materialized_local_cases":sum(int(r["local_cases_materialized"])>0 for r in rows),
      "n_change_records_with_two_or_more_materialized_cases":sum(int(r["local_cases_materialized"])>=2 for r in rows),
      "n_materialized_local_cases_represented":sum(int(r["local_cases_materialized"]) for r in rows),
      "n_change_records_without_materialized_local_cases":sum(int(r["local_cases_materialized"])==0 for r in rows),
      "status":"H2_CHANGE_TYPE_SEED_V7_POLYGALA_COMPONENT_SHIFT_ADDED",
      "claim_ceiling":[
        "change_types_are_mechanistic_descriptive_classes_not_frequencies",
        "reproductive_component_context_shift_is_not_final_fitness_selection_shift",
        "tanacetum_single_performance_snapshots_are_not_change_records",
        "H2_change_type_model_not_ready",
      ],
    }
def main():
    p=argparse.ArgumentParser(); p.add_argument("seed",type=Path); p.add_argument("--output",type=Path); a=p.parse_args()
    r=build(a.seed); t=json.dumps(r,indent=2,sort_keys=True)+"\n"; a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

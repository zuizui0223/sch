from __future__ import annotations
import argparse, csv, importlib.util, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"build_sch_macroecology_h2_context_cases_cumulative_v5.py"
def _base():
    spec=importlib.util.spec_from_file_location("h2v5",BASE); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def _read(paths):
    out=[]
    for p in paths:
        with p.open(encoding="utf-8",newline="") as h: out.extend({k:(v or "").strip() for k,v in r.items()} for r in csv.DictReader(h))
    return out
def _class(r):
    if r["combined_or_net_response"]=="LOCAL_ANTAGONIST_PRESSURE_ONLY" or r["effect_metric"]=="SEED_PREDATION_PERCENT": return "LOCAL_ANTAGONIST_PRESSURE"
    if r["effect_metric"] in {"PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA","STANDARDIZED_LINEAR_SELECTION_GRADIENT_BETA","SEM_TOTAL_DIRECT_SELECTION_PATH_COEFFICIENT"}: return "LOCAL_NET_SELECTION"
    if r["function_2_direction_or_optimum"]=="REMOVED_BY_EXCLUSION": return "LOCAL_NET_SELECTION"
    if any(r[k]=="YES" for k in ["conflict_detected","alignment_detected","one_sided_or_null_detected"]): return "LOCAL_GEOMETRY"
    if r["antagonist_role_status"]!="NET_ANTAGONISTIC": return "ROLE_BEHAVIOR_CONTEXT"
    return "UNRESOLVED"
def build(evidence_paths,case_paths):
    res=_base().build(evidence_paths,case_paths); cases=_read(case_paths)
    ery=[r for r in cases if r["source_id"]=="SCHPRISMA-000008"]
    if len(ery)!=18: raise ValueError(f"expected 18 Erysimum cases, found {len(ery)}")
    res["analysis"]="sch_macroecology_h2_context_cases_cumulative_v6"
    res["local_measurement_class_counts"]=dict(sorted(Counter(_class(r) for r in cases).items()))
    res["n_erysimum_local_net_selection_cases"]=18
    res["erysimum_axes_materialized"]=sorted({r["canonical_trait_axis_id"] for r in ery})
    res["status"]="H2_ERYSIMUM_NET_SELECTION_EXPANDED_INFERENCE_FAIL_CLOSED"
    marker="erysimum_table5_paths_are_local_net_selection_not_local_agent_geometry"
    if marker not in res["claim_ceiling"]: res["claim_ceiling"].insert(-1,marker)
    return res
def main():
    p=argparse.ArgumentParser(); p.add_argument("--evidence",type=Path,nargs="+",required=True); p.add_argument("--cases",type=Path,nargs="+",required=True); p.add_argument("--output",type=Path); a=p.parse_args()
    r=build(a.evidence,a.cases); t=json.dumps(r,indent=2,sort_keys=True)+"\n"; a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

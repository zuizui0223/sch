from __future__ import annotations
import argparse, csv, importlib.util, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"build_sch_macroecology_h2_context_cases_cumulative_v6.py"

def _base():
    spec=importlib.util.spec_from_file_location("h2v6",BASE)
    mod=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(mod); return mod

def _read(paths):
    out=[]
    for p in paths:
        with p.open(encoding="utf-8",newline="") as h:
            for r in csv.DictReader(h):
                if None in r: raise ValueError(f"malformed CSV {p}: {r[None]}")
                out.append({k:(v or "").strip() for k,v in r.items()})
    return out

def _class(r):
    if r["combined_or_net_response"]=="LOCAL_ANTAGONIST_PRESSURE_ONLY" or r["effect_metric"]=="SEED_PREDATION_PERCENT":
        return "LOCAL_ANTAGONIST_PRESSURE"
    if r["effect_metric"] in {"PHENOTYPIC_LINEAR_SELECTION_GRADIENT_BETA","STANDARDIZED_LINEAR_SELECTION_GRADIENT_BETA","SEM_TOTAL_DIRECT_SELECTION_PATH_COEFFICIENT"}:
        return "LOCAL_NET_SELECTION"
    if r["effect_metric"]=="STANDARDIZED_REGRESSION_B_SUCCESSFUL_POLLINATION":
        return "LOCAL_REPRODUCTIVE_COMPONENT_EFFECT"
    if r["effect_metric"]=="LME_WALD_CHISQ_REPRODUCTIVE_PERFORMANCE_PROXY":
        return "LOCAL_REPRODUCTIVE_PERFORMANCE_PROXY"
    if r["function_2_direction_or_optimum"]=="REMOVED_BY_EXCLUSION":
        return "LOCAL_NET_SELECTION"
    if any(r[k]=="YES" for k in ["conflict_detected","alignment_detected","one_sided_or_null_detected"]):
        return "LOCAL_GEOMETRY"
    if r["antagonist_role_status"]!="NET_ANTAGONISTIC":
        return "ROLE_BEHAVIOR_CONTEXT"
    return "UNRESOLVED"

def build(evidence_paths,case_paths):
    r=_base().build(evidence_paths,case_paths)
    cases=_read(case_paths)
    pol=[x for x in cases if x["source_id"]=="SCHPRISMA-000334"]
    tan=[x for x in cases if x["source_id"]=="SCHPRISMA-000352"]
    if len(pol)!=3: raise ValueError(f"expected 3 Polygala cases, found {len(pol)}")
    if len(tan)!=2: raise ValueError(f"expected 2 Tanacetum cases, found {len(tan)}")
    r["analysis"]="sch_macroecology_h2_context_cases_cumulative_v7"
    r["local_measurement_class_counts"]=dict(sorted(Counter(_class(x) for x in cases).items()))
    r["n_polygala_reproductive_component_cases"]=3
    r["n_tanacetum_reproductive_performance_proxy_cases"]=2
    r["status"]="H2_BREADTH_EXPANDED_ESTIMAND_FAMILIES_SEPARATE"
    for marker in [
        "polygala_successful_pollination_effect_is_reproductive_component_not_final_fitness",
        "tanacetum_germination_is_reproductive_performance_proxy_not_seed_set",
    ]:
        if marker not in r["claim_ceiling"]: r["claim_ceiling"].insert(-1,marker)
    return r

def main():
    p=argparse.ArgumentParser(); p.add_argument("--evidence",type=Path,nargs="+",required=True); p.add_argument("--cases",type=Path,nargs="+",required=True); p.add_argument("--output",type=Path)
    a=p.parse_args(); r=build(a.evidence,a.cases); t=json.dumps(r,indent=2,sort_keys=True)+"\n"
    a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

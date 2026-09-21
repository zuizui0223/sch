from __future__ import annotations
import argparse, csv, importlib.util, json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"diagnose_sch_macroecology_h2_modelability_v5.py"

def _base():
    spec=importlib.util.spec_from_file_location("g5",BASE)
    mod=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(mod); return mod

def _read(path):
    with path.open(encoding="utf-8",newline="") as h:
        return [{k:(v or "").strip() for k,v in r.items()} for r in csv.DictReader(h)]

def _case_ids(r):
    return [x for x in r["case_ids"].split(";") if x]

def _families(rows,field,gates):
    out=defaultdict(lambda:{"cases":0,"axes":set(),"clusters":set(),"repeated_axes":set()})
    for r in rows:
        ids=_case_ids(r)
        if not ids: continue
        key=r[field]; out[key]["cases"]+=len(ids); out[key]["axes"].add(r["canonical_trait_axis_id"]); out[key]["clusters"].add(r["cluster_id"])
        if len(ids)>=2: out[key]["repeated_axes"].add(r["canonical_trait_axis_id"])
    result={}
    for k,v in sorted(out.items()):
        result[k]={
          "n_cases":v["cases"],"n_axes":len(v["axes"]),"n_clusters":len(v["clusters"]),
          "n_repeated_axes":len(v["repeated_axes"]),
          "model_ready":(
            v["cases"]>=gates["min_cases_per_layer"] and len(v["axes"])>=gates["min_canonical_axes_per_layer"]
            and len(v["clusters"])>=gates["min_independent_clusters_per_layer"] and len(v["repeated_axes"])>=gates["min_repeated_axes_per_layer"]
          )
        }
    return result

def build(measurement_path,change_seed_path,case_paths):
    r=_base().build(measurement_path,change_seed_path,case_paths)
    rows=_read(measurement_path); g=r["project_gates"]; p=r["plant_performance_layer"]
    broad=(p["n_cases"]>=g["min_cases_per_layer"] and p["n_canonical_axes"]>=g["min_canonical_axes_per_layer"] and p["n_clusters"]>=g["min_independent_clusters_per_layer"] and p["n_axes_with_two_or_more_cases"]>=g["min_repeated_axes_per_layer"])
    estimands=_families(rows,"estimand_family",g); pools=_families(rows,"numeric_pooling_family",g)
    estimand_ready=any(x["model_ready"] for x in estimands.values())
    numeric_ready=any(x["model_ready"] for x in pools.values())
    r["analysis"]="sch_macroecology_h2_modelability_gate_v6"
    r["broad_plant_performance_structural_gate_pass"]=broad
    r["estimand_family_modelability"]=estimands
    r["numeric_pooling_family_modelability"]=pools
    r["commensurate_estimand_family_model_ready"]=estimand_ready
    r["commensurate_numeric_pooling_model_ready"]=numeric_ready
    r["plant_performance_model_ready"]=False
    r["primary_h2_status"]="BREADTH_GATE_PASS_ESTIMAND_HARMONIZATION_FAIL" if broad and not estimand_ready else r["primary_h2_status"]
    r["structural_gate_blockers"]=[] if broad else r.get("structural_gate_blockers",[])
    r["estimand_gate_blockers"]=[
      "no_single_estimand_family_meets_registered_case_axis_cluster_repeat_gates",
      "effect_metrics_are_not_numerically_commensurate_across_estimand_families",
      "antagonist_pressure_and_reproductive_proxy_rows_cannot_be_treated_as_selection_gradients",
    ] if not estimand_ready else []
    r["status"]="H2_BREADTH_GATE_PASS_ESTIMAND_FAMILY_FAIL_CLOSED" if broad and not estimand_ready else "H2_MODELABILITY_V6_FAIL_CLOSED"
    r["reasons"]=[
      f"broad_plant_performance_layer_has_{p['n_cases']}_cases_across_{p['n_canonical_axes']}_axes_and_{p['n_clusters']}_clusters",
      "legacy_breadth_thresholds_pass_but_commensurate_estimand_family_thresholds_fail",
      "largest_estimand_family_is_total_selection_effect_but_has_only_3_independent_clusters",
      "Polygala_adds_reproductive_component_effect_not_final_fitness_selection",
      "Tanacetum_adds_germination_proxy_performance_not_seed_set_or_selection_gradient",
    ]
    return r

def main():
    p=argparse.ArgumentParser(); p.add_argument("measurement",type=Path); p.add_argument("change_seed",type=Path); p.add_argument("--cases",type=Path,nargs="+",required=True); p.add_argument("--output",type=Path)
    a=p.parse_args(); r=build(a.measurement,a.change_seed,a.cases); t=json.dumps(r,indent=2,sort_keys=True)+"\n"
    a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

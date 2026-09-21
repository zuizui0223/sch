from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"diagnose_sch_macroecology_h2_modelability_v4.py"
def _base():
    spec=importlib.util.spec_from_file_location("mod4",BASE); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def build(measurement_path,change_seed_path,case_paths):
    r=_base().build(measurement_path,change_seed_path,case_paths)
    r["analysis"]="sch_macroecology_h2_modelability_gate_v5"; r["status"]="H2_MODELABILITY_GATE_V5_ERYSIMUM_ADDED_FAIL_CLOSED"
    p=r["plant_performance_layer"]; g=r["project_gates"]; blockers=[]
    if p["n_cases"]<g["min_cases_per_layer"]: blockers.append("case_count_below_gate")
    if p["n_canonical_axes"]<g["min_canonical_axes_per_layer"]: blockers.append("canonical_axes_below_gate")
    if p["n_clusters"]<g["min_independent_clusters_per_layer"]: blockers.append("independent_clusters_below_gate")
    if p["n_axes_with_two_or_more_cases"]<g["min_repeated_axes_per_layer"]: blockers.append("repeated_axes_below_gate")
    r["structural_gate_blockers"]=blockers
    r["raw_plant_performance_case_count_gate_pass"]=p["n_cases"]>=g["min_cases_per_layer"]
    r["plant_performance_axis_gate_pass"]=p["n_canonical_axes"]>=g["min_canonical_axes_per_layer"]
    r["plant_performance_repeated_axis_gate_pass"]=p["n_axes_with_two_or_more_cases"]>=g["min_repeated_axes_per_layer"]
    r["reasons"]=[
      f"only_{p['n_clusters']}_plant_performance_clusters_have_materialized_local_cases",
      f"plant_performance_layer_has_{p['n_cases']}_cases_across_{p['n_canonical_axes']}_axes_and_{p['n_clusters']}_clusters",
      "case_axis_and_repeated_axis_gates_pass_but_independent_cluster_gate_fails",
      f"role_behavior_layer_has_{r['role_behavior_layer']['n_cases']}_cases_across_{r['role_behavior_layer']['n_canonical_axes']}_axes_and_{r['role_behavior_layer']['n_clusters']}_clusters",
      "plant_performance_and_role_behavior_are_different_estimands",
      "Gentiana_and_Primula_exact_local_source_objects_remain_partly_unmaterialized",
    ]
    return r
def main():
    p=argparse.ArgumentParser(); p.add_argument("measurement",type=Path); p.add_argument("change_seed",type=Path); p.add_argument("--cases",type=Path,nargs="+",required=True); p.add_argument("--output",type=Path); a=p.parse_args()
    r=build(a.measurement,a.change_seed,a.cases); t=json.dumps(r,indent=2,sort_keys=True)+"\n"; a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

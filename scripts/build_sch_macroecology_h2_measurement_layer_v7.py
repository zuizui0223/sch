from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"build_sch_macroecology_h2_measurement_layer_v6.py"

def _base():
    spec=importlib.util.spec_from_file_location("m6",BASE)
    mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod

def build(measurement_path,source_registry_path,case_paths):
    r=_base().build(measurement_path,source_registry_path,case_paths)
    pol=sorted(x for x in r["plant_performance_case_ids"] if x.startswith("Polygala_nectar_reward_"))
    tan=sorted(x for x in r["plant_performance_case_ids"] if x=="Tanacetum_plot_chemodiversity_common_garden")
    if len(pol)!=3: raise ValueError(f"expected 3 Polygala cases, found {len(pol)}")
    if len(tan)!=1: raise ValueError(f"expected 1 Tanacetum case, found {len(tan)}")
    r["analysis"]="sch_macroecology_h2_measurement_layer_v7"
    r["n_polygala_local_net_selection_cases"]=3
    r["polygala_case_ids"]=pol
    r["n_tanacetum_local_geometry_cases"]=1
    r["tanacetum_case_ids"]=tan
    r["status"]="H2_MEASUREMENT_LAYER_V7_POLYGALA_TANACETUM_MATERIALIZED"
    for marker in [
        "polygala_reproductive_proxy_coefficients_are_not_trait_mediated_antagonist_components",
        "tanacetum_one_sided_geometry_does_not_imply_direct_plot_type_fitness_benefit",
    ]:
        if marker not in r["claim_ceiling"]: r["claim_ceiling"].insert(-1,marker)
    return r

def main():
    p=argparse.ArgumentParser(); p.add_argument("measurement",type=Path); p.add_argument("source_registry",type=Path); p.add_argument("--cases",type=Path,nargs="+",required=True); p.add_argument("--output",type=Path); a=p.parse_args()
    r=build(a.measurement,a.source_registry,a.cases); t=json.dumps(r,indent=2,sort_keys=True)+"\n"; a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"build_sch_macroecology_h2_measurement_layer_v5.py"
def _base():
    spec=importlib.util.spec_from_file_location("m5",BASE); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def build(measurement_path,source_registry_path,case_paths):
    r=_base().build(measurement_path,source_registry_path,case_paths)
    ids=sorted(x for x in r["plant_performance_case_ids"] if x.startswith("Erysimum_"))
    if len(ids)!=18: raise ValueError(f"expected 18 Erysimum cases, found {len(ids)}")
    r["analysis"]="sch_macroecology_h2_measurement_layer_v6"
    r["n_erysimum_local_net_selection_cases"]=18
    r["erysimum_case_ids"]=ids
    r["status"]="H2_MEASUREMENT_LAYER_V6_ERYSIMUM_NET_SELECTION_MATERIALIZED"
    marker="erysimum_total_direct_paths_are_not_local_pollinator_herbivore_components"
    if marker not in r["claim_ceiling"]: r["claim_ceiling"].insert(-1,marker)
    return r
def main():
    p=argparse.ArgumentParser(); p.add_argument("measurement",type=Path); p.add_argument("source_registry",type=Path); p.add_argument("--cases",type=Path,nargs="+",required=True); p.add_argument("--output",type=Path); a=p.parse_args()
    r=build(a.measurement,a.source_registry,a.cases); t=json.dumps(r,indent=2,sort_keys=True)+"\n"; a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

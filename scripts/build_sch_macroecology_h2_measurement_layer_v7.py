from __future__ import annotations
import argparse, csv, importlib.util, json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"build_sch_macroecology_h2_measurement_layer_v6.py"

def _base():
    spec=importlib.util.spec_from_file_location("m6",BASE)
    mod=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(mod); return mod

def _read(path):
    with path.open(encoding="utf-8",newline="") as h:
        rows=[]
        for r in csv.DictReader(h):
            if None in r: raise ValueError(f"malformed CSV {path}: {r[None]}")
            rows.append({k:(v or "").strip() for k,v in r.items()})
        return rows

def _case_n(r):
    return int(r["local_geometry_cases_materialized"])+int(r["local_net_selection_cases_materialized"])+int(r["local_antagonist_pressure_cases_materialized"])

def _summarize(rows,field):
    out=defaultdict(lambda: {"n_cases":0,"axes":set(),"clusters":set(),"records":0})
    for r in rows:
        n=_case_n(r)
        if n<=0: continue
        key=r[field]
        out[key]["n_cases"]+=n; out[key]["axes"].add(r["canonical_trait_axis_id"]); out[key]["clusters"].add(r["cluster_id"]); out[key]["records"]+=1
    return {k:{"n_cases":v["n_cases"],"n_axes":len(v["axes"]),"n_clusters":len(v["clusters"]),"n_measurement_records":v["records"]} for k,v in sorted(out.items())}

def build(measurement_path,source_registry_path,case_paths):
    r=_base().build(measurement_path,source_registry_path,case_paths)
    rows=_read(measurement_path)
    required={"estimand_family","numeric_pooling_family"}
    if not required <= set(rows[0]): raise ValueError("measurement V6 lacks estimand-family columns")
    r["analysis"]="sch_macroecology_h2_measurement_layer_v7"
    r["estimand_family_materialized_counts"]=_summarize(rows,"estimand_family")
    r["numeric_pooling_family_materialized_counts"]=_summarize(rows,"numeric_pooling_family")
    r["n_polygala_reproductive_component_cases"]=3
    r["n_tanacetum_reproductive_performance_proxy_cases"]=2
    r["status"]="H2_MEASUREMENT_LAYER_V7_ESTIMAND_FAMILIES_EXPLICIT"
    for marker in [
        "estimand_family_must_be_preserved_before_numeric_pooling",
        "reproductive_component_effect_is_not_final_fitness_selection",
        "germination_proxy_is_not_seed_set_or_selection_gradient",
    ]:
        if marker not in r["claim_ceiling"]: r["claim_ceiling"].insert(-1,marker)
    return r

def main():
    p=argparse.ArgumentParser(); p.add_argument("measurement",type=Path); p.add_argument("source_registry",type=Path); p.add_argument("--cases",type=Path,nargs="+",required=True); p.add_argument("--output",type=Path)
    a=p.parse_args(); r=build(a.measurement,a.source_registry,a.cases); t=json.dumps(r,indent=2,sort_keys=True)+"\n"
    a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

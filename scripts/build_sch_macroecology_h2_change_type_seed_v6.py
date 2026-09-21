from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"scripts"/"build_sch_macroecology_h2_change_type_seed_v5.py"
def _base():
    spec=importlib.util.spec_from_file_location("c5",BASE); mod=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(mod); return mod
def build(path):
    r=_base().build(path); r["analysis"]="sch_macroecology_h2_change_type_seed_v6"; r["status"]="H2_CHANGE_TYPE_SEED_V6_ERYSIMUM_GEOGRAPHIC_SELECTION_ADDED"; return r
def main():
    p=argparse.ArgumentParser(); p.add_argument("seed",type=Path); p.add_argument("--output",type=Path); a=p.parse_args()
    r=build(a.seed); t=json.dumps(r,indent=2,sort_keys=True)+"\n"; a.output.write_text(t,encoding="utf-8") if a.output else print(t,end="")
if __name__=="__main__": main()

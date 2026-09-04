from __future__ import annotations

import argparse
import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean


REQUIRED_FIELDS = (
    "population_id","season_id","plant_id","flower_id","predator_treatment","exclusion_method",
    "realized_exsertion","water_depth","pollen_grains","pollinator_visits","early_predator_attack_present",
    "ovule_count","undamaged_seed_count","damaged_seed_count","mechanical_damage",
)
TREATMENTS = ("EXPOSED", "EXCLUDED")
RECEIPT_SCHEMA = "SCH_PEDICULARIS_PREDATOR_WEIGHT_V2"


def _num(row: dict[str, str], field: str) -> float:
    try: value = float(row[field])
    except (KeyError, ValueError) as exc: raise ValueError(f"invalid numeric value for {field!r}: {row.get(field)!r}") from exc
    if not math.isfinite(value): raise ValueError(f"non-finite numeric value for {field!r}")
    return value


def _bin(row: dict[str, str], field: str) -> int:
    raw = row[field].strip()
    if raw not in {"0","1"}: raise ValueError(f"{field} must be coded 0/1")
    return int(raw)


def read_rows(path: Path) -> list[dict[str,str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None: raise ValueError("CSV has no header")
        missing = [f for f in REQUIRED_FIELDS if f not in reader.fieldnames]
        if missing: raise ValueError(f"missing required columns: {', '.join(missing)}")
        rows = list(reader)
    if not rows: raise ValueError("CSV has no data rows")
    seen=set()
    for i,row in enumerate(rows,start=2):
        for f in REQUIRED_FIELDS:
            if row.get(f,"").strip()=="": raise ValueError(f"blank required field {f!r} on CSV line {i}")
        if row["flower_id"] in seen: raise ValueError(f"duplicate flower_id {row['flower_id']!r}")
        seen.add(row["flower_id"])
        if row["predator_treatment"] not in TREATMENTS: raise ValueError("predator_treatment must be EXPOSED or EXCLUDED")
        for f in ("realized_exsertion","water_depth","pollen_grains","pollinator_visits","ovule_count","undamaged_seed_count","damaged_seed_count"):
            _num(row,f)
        _bin(row,"early_predator_attack_present"); _bin(row,"mechanical_damage")
        ov=_num(row,"ovule_count"); u=_num(row,"undamaged_seed_count"); d=_num(row,"damaged_seed_count")
        if ov<=0 or u<0 or d<0 or u+d>ov: raise ValueError("invalid ovule/seed counts")
    return rows


def _initial(row): return (_num(row,"undamaged_seed_count")+_num(row,"damaged_seed_count"))/_num(row,"ovule_count")
def _final(row): return _num(row,"undamaged_seed_count")/_num(row,"ovule_count")
def _pred(row):
    total=_num(row,"undamaged_seed_count")+_num(row,"damaged_seed_count")
    return 0.0 if total<=0 else _num(row,"damaged_seed_count")/total


def _context(rows):
    pops={r["population_id"] for r in rows}; seasons={r["season_id"] for r in rows}
    if len(pops)!=1 or len(seasons)!=1: raise ValueError("one predator-weight package must contain one population and season")
    return next(iter(pops)),next(iter(seasons))


def _plant_pairs(rows):
    by=defaultdict(lambda: defaultdict(list))
    for r in rows: by[r["plant_id"]][r["predator_treatment"]].append(r)
    pairs=[]
    for plant,treatments in sorted(by.items()):
        if set(treatments)!=set(TREATMENTS): continue
        def m(t,fn): return mean(fn(r) for r in treatments[t])
        exposed=treatments["EXPOSED"]; excluded=treatments["EXCLUDED"]
        def rel(field):
            a=m("EXPOSED",lambda r,f=field:_num(r,f)); b=m("EXCLUDED",lambda r,f=field:_num(r,f))
            return abs(b-a)/max(abs(a),1e-12)
        pairs.append({
            "plant_id":plant,
            "attack_reduction":m("EXPOSED",lambda r:_bin(r,"early_predator_attack_present"))-m("EXCLUDED",lambda r:_bin(r,"early_predator_attack_present")),
            "predation_reduction":m("EXPOSED",_pred)-m("EXCLUDED",_pred),
            "final_seed_gain":m("EXCLUDED",_final)-m("EXPOSED",_final),
            "initial_seed_abs_difference":abs(m("EXCLUDED",_initial)-m("EXPOSED",_initial)),
            "pollen_relative_change":rel("pollen_grains"),
            "pollinator_visit_relative_change":rel("pollinator_visits"),
            "z_relative_change":rel("realized_exsertion"),
            "water_depth_abs_difference":abs(m("EXCLUDED",lambda r:_num(r,"water_depth"))-m("EXPOSED",lambda r:_num(r,"water_depth"))),
            "damage_rate_abs_difference":abs(m("EXCLUDED",lambda r:_bin(r,"mechanical_damage"))-m("EXPOSED",lambda r:_bin(r,"mechanical_damage"))),
        })
    return pairs


def _quantile(values,q):
    values=sorted(values); pos=(len(values)-1)*q; lo=math.floor(pos); hi=math.ceil(pos)
    if lo==hi:return values[lo]
    w=pos-lo; return values[lo]*(1-w)+values[hi]*w


def _bootstrap(pairs,field,reps,rng):
    vals=[]
    for _ in range(reps): vals.append(mean(p[field] for p in rng.choices(pairs,k=len(pairs))))
    return [_quantile(vals,0.025),_quantile(vals,0.975)]


def evaluate(rows,config):
    population,season=_context(rows); pairs=_plant_pairs(rows); cfg=config["predator_weight"]
    reps=int(config["bootstrap_reps"])
    if reps<200: raise ValueError("bootstrap_reps must be >= 200")
    if len(pairs)<2: raise ValueError("at least two paired plants are required")
    rng=random.Random(int(config.get("random_seed",20260904)))
    fields=("attack_reduction","predation_reduction","final_seed_gain","initial_seed_abs_difference","pollen_relative_change","pollinator_visit_relative_change","z_relative_change","water_depth_abs_difference","damage_rate_abs_difference")
    obs={f:mean(p[f] for p in pairs) for f in fields}
    cis={f:_bootstrap(pairs,f,reps,rng) for f in fields}
    counts={t:sum(r["predator_treatment"]==t for r in rows) for t in TREATMENTS}
    gates={
        "minimum_paired_plants":len(pairs)>=int(cfg["min_paired_plants"]),
        "minimum_flowers_per_treatment":all(counts[t]>=int(cfg["min_flowers_per_treatment"]) for t in TREATMENTS),
        "early_attack_reduced":cis["attack_reduction"][0]>=float(cfg["min_early_attack_reduction"]),
        "seed_predation_reduced":cis["predation_reduction"][0]>=float(cfg["min_predation_fraction_reduction"]),
        "final_seed_set_improves":cis["final_seed_gain"][0]>=float(cfg["min_final_seed_set_gain"]),
        "initial_seed_set_stable":cis["initial_seed_abs_difference"][1]<=float(cfg["max_initial_seed_set_difference"]),
        "pollen_receipt_stable":cis["pollen_relative_change"][1]<=float(cfg["max_pollen_grain_relative_change"]),
        "pollinator_visitation_stable":cis["pollinator_visit_relative_change"][1]<=float(cfg["max_pollinator_visit_relative_change"]),
        "realized_z_stable":cis["z_relative_change"][1]<=float(cfg["max_z_relative_change"]),
        "water_state_stable":cis["water_depth_abs_difference"][1]<=float(cfg["max_water_depth_change"]),
        "handling_damage_stable":cis["damage_rate_abs_difference"][1]<=float(cfg["max_damage_rate_difference"]),
    }
    status="PEDICULARIS_PREDATOR_WEIGHT_VALIDATED" if all(gates.values()) else "PEDICULARIS_PREDATOR_WEIGHT_NOT_VALIDATED"
    return {"receipt_schema_version":RECEIPT_SCHEMA,"analysis":"pedicularis_independent_seed_predator_weight_pilot","population_id":population,"season_id":season,"n_rows":len(rows),"n_paired_plants":len(pairs),"n_by_treatment":counts,"observed_estimands":obs,"bootstrap_95_ci":cis,"gates":gates,"status":status,"claim_ceiling":"independent_antagonist_weight_intervention_only_not_causal_compromise_not_water_y_release"}


def main():
    p=argparse.ArgumentParser(); p.add_argument("csv_path",type=Path); p.add_argument("config_path",type=Path); p.add_argument("--output",type=Path); a=p.parse_args()
    result=evaluate(read_rows(a.csv_path),json.loads(a.config_path.read_text(encoding="utf-8")))
    payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output:a.output.write_text(payload,encoding="utf-8")
    else:print(payload,end="")

if __name__=="__main__":main()

from __future__ import annotations

import argparse
import json
from pathlib import Path


EXPECTED = {
    "z": {"schema": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1", "status": "PEDICULARIS_Z_MANIPULATION_VALIDATED"},
    "p": {"schema": "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1", "status": "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED"},
    "g": {"schema": "SCH_PEDICULARIS_PREDATOR_WEIGHT_V2", "status": "PEDICULARIS_PREDATOR_WEIGHT_VALIDATED"},
}
READINESS_SCHEMA = "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V2"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict): raise ValueError(f"receipt {path} is not a JSON object")
    return payload


def assemble(z_receipt: dict, p_receipt: dict, g_receipt: dict) -> dict:
    receipts={"z":z_receipt,"p":p_receipt,"g":g_receipt}; checks={}; contexts=[]
    for lane,receipt in receipts.items():
        expected=EXPECTED[lane]
        checks[f"{lane}_schema"]=receipt.get("receipt_schema_version")==expected["schema"]
        checks[f"{lane}_status"]=receipt.get("status")==expected["status"]
        population=receipt.get("population_id"); season=receipt.get("season_id")
        checks[f"{lane}_context_present"]=isinstance(population,str) and bool(population) and isinstance(season,str) and bool(season)
        contexts.append((population,season))
    same_context=len(set(contexts))==1; checks["same_population_and_season"]=same_context
    ready=all(checks.values()); population,season=contexts[0] if same_context else (None,None)
    return {
        "receipt_schema_version":READINESS_SCHEMA,
        "analysis":"pedicularis_pre_surface_readiness_independent_predator_G",
        "population_id":population,"season_id":season,"checks":checks,
        "source_receipts":{lane:{"schema":receipt.get("receipt_schema_version"),"status":receipt.get("status")} for lane,receipt in receipts.items()},
        "status":"PEDICULARIS_FULL_SURFACE_READY" if ready else "PEDICULARIS_FULL_SURFACE_NOT_READY",
        "unlocked_next_step":">=5 realized z levels x pollination-weight P0/P1 x independent predator G0/G1 with water-y held fixed" if ready else None,
        "water_y_requirement":"HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "claim_ceiling":"execution_readiness_only_not_causal_compromise_not_dimensional_release",
    }


def main() -> None:
    p=argparse.ArgumentParser(description="Assemble fail-closed Pedicularis z/P/independent-predator-G readiness receipt")
    p.add_argument("z_receipt",type=Path); p.add_argument("p_receipt",type=Path); p.add_argument("g_receipt",type=Path); p.add_argument("--output",type=Path); a=p.parse_args()
    result=assemble(_load(a.z_receipt),_load(a.p_receipt),_load(a.g_receipt)); payload=json.dumps(result,indent=2,sort_keys=True)+"\n"
    if a.output:a.output.write_text(payload,encoding="utf-8")
    else:print(payload,end="")

if __name__=="__main__":main()

from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.evaluate_pedicularis_predator_weight import REQUIRED_FIELDS, evaluate

ROOT=Path(__file__).resolve().parents[1]
TEMPLATE=ROOT/"empirical"/"architecture"/"PEDICULARIS_PREDATOR_WEIGHT_TEMPLATE_V2.csv"
CONFIG=ROOT/"empirical"/"architecture"/"PEDICULARIS_PREDATOR_WEIGHT_CONFIG_TEMPLATE_V2.json"


def _config():
    return {"bootstrap_reps":300,"random_seed":61,"predator_weight":{"min_paired_plants":12,"min_flowers_per_treatment":12,"min_early_attack_reduction":0.5,"min_predation_fraction_reduction":0.15,"min_final_seed_set_gain":0.1,"max_initial_seed_set_difference":0.03,"max_pollen_grain_relative_change":0.05,"max_pollinator_visit_relative_change":0.05,"max_z_relative_change":0.05,"max_water_depth_change":0.5,"max_damage_rate_difference":0.05}}


def _rows(contaminate=False):
    rows=[]
    for plant in range(16):
        for treatment in ("EXPOSED","EXCLUDED"):
            exposed=treatment=="EXPOSED"
            pollen=100 if not contaminate or exposed else 80
            rows.append({"population_id":"P_REX_TEST","season_id":"S1","plant_id":f"P{plant:02d}","flower_id":f"P{plant:02d}_{treatment}","predator_treatment":treatment,"exclusion_method":"OPEN_CONTROL" if exposed else "TARGETED_OVIPOSITION_BARRIER","realized_exsertion":"0.50","water_depth":"10.0","pollen_grains":str(pollen),"pollinator_visits":"10","early_predator_attack_present":"1" if exposed else "0","ovule_count":"100","undamaged_seed_count":"50" if exposed else "68","damaged_seed_count":"20" if exposed else "2","mechanical_damage":"0"})
    return rows


def test_template_and_config_are_fail_closed():
    with TEMPLATE.open(encoding="utf-8",newline="") as h: assert tuple(next(csv.reader(h)))==REQUIRED_FIELDS
    cfg=json.loads(CONFIG.read_text(encoding="utf-8")); assert cfg["predator_weight"]["min_paired_plants"]=="REQUIRED_BEFORE_USE"; assert "DO_NOT_RUN" in cfg["status"]


def test_independent_predator_intervention_passes_when_pollination_and_water_stay_stable():
    result=evaluate(_rows(False),_config())
    assert result["status"]=="PEDICULARIS_PREDATOR_WEIGHT_VALIDATED"
    assert all(result["gates"].values())
    assert result["observed_estimands"]["predation_reduction"]>0.2
    assert result["observed_estimands"]["final_seed_gain"]>0.15
    assert result["observed_estimands"]["pollen_relative_change"]==0
    assert result["observed_estimands"]["water_depth_abs_difference"]==0


def test_pollination_contamination_blocks_predator_weight_validation():
    result=evaluate(_rows(True),_config())
    assert result["gates"]["pollen_receipt_stable"] is False
    assert result["status"]=="PEDICULARIS_PREDATOR_WEIGHT_NOT_VALIDATED"

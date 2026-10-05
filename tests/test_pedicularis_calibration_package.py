from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts import evaluate_pedicularis_pollination_weight as p1mod
from scripts import evaluate_pedicularis_predator_method as gmod
from scripts import evaluate_pedicularis_stage_p0 as p0mod
from scripts import summarize_pedicularis_cal_a_repeatability as repmod
from scripts.build_pedicularis_calibration_package import build_package
from scripts.validate_pedicularis_cohort_registry import REQUIRED_FIELDS as REG_FIELDS


def _write(path: Path, fields: list[str] | tuple[str, ...], rows: list[dict[str, str]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)
    return path


def _p0_rows(season: str = "S1") -> list[dict[str, str]]:
    rows = []
    for plant in range(4):
        for rank in range(5):
            rows.append({
                "population_id":"P_REX_TEST","season_id":season,
                "plant_id":f"A{plant:02d}","flower_id":f"A{plant:02d}_Z{rank}",
                "assigned_z_level":f"Z{rank}","assigned_z_rank":str(rank),
                "sham_control":"1" if rank==4 else "0",
                "realized_exsertion":str(0.2+0.15*rank+plant*0.001),
                "corolla_opening_width":"8.0","lower_lip_angle_deg":"25.0",
                "tube_diameter":"4.0","bract_height":"20.0","water_depth":"5.0",
                "flower_orientation_deg":"15.0","mechanical_damage":"0",
                "pollinator_visits":str(2+rank),"pollen_grains":str(10+rank),
            })
    return rows


def _repeatability_rows(season: str = "S1") -> list[dict[str, str]]:
    rows = []
    for plant in range(4):
        flower_id=f"A{plant:02d}_Z0"
        base=0.2+plant*0.001
        for rep,shift in ((1,-0.002),(2,0.002)):
            rows.append({
                "population_id":"P_REX_TEST","season_id":season,
                "plant_id":f"A{plant:02d}","flower_id":flower_id,
                "measurement_replicate":str(rep),"observer_id":f"O{rep}",
                "realized_exsertion":str(base+shift),
                "corolla_opening_width":str(8.0+shift),
                "lower_lip_angle_deg":str(25.0+shift),
                "tube_diameter":str(4.0+shift),
                "bract_height":str(20.0+shift),
                "water_depth":str(5.0+shift),
                "flower_orientation_deg":str(15.0+shift),
            })
    return rows


def _p1_rows(season: str = "S1") -> list[dict[str, str]]:
    rows=[]
    for plant in range(4):
        for treatment in ("NATURAL","SUPPLEMENTED"):
            sup=treatment=="SUPPLEMENTED"
            rows.append({
                "population_id":"P_REX_TEST","season_id":season,
                "plant_id":f"B{plant:02d}","flower_id":f"B{plant:02d}_{treatment}",
                "pollination_treatment":treatment,"realized_exsertion":"0.55",
                "water_depth":"5.0","bract_height":"20.0","corolla_opening_width":"8.0",
                "mechanical_damage":"0","pollen_grains_post_treatment":"24" if sup else "10",
                "early_predator_attack_present":"0","ovule_count":"20",
                "undamaged_seed_count":"10" if sup else "6","damaged_seed_count":"2",
            })
    return rows


def _g_rows(season: str = "S1") -> list[dict[str, str]]:
    rows=[]
    for plant in range(4):
        for treatment in ("EXPOSED","EXCLUDED"):
            exp=treatment=="EXPOSED"
            rows.append({
                "population_id":"P_REX_TEST","season_id":season,
                "plant_id":f"C{plant:02d}","flower_id":f"C{plant:02d}_{treatment}",
                "predator_treatment":treatment,
                "exclusion_method":"SHAM_SLEEVE" if exp else "POST_POLLINATION_LOWER_FLOWER_SLEEVE",
                "sham_device_applied":"1" if exp else "0",
                "anthesis_time_hours":"0","barrier_application_time_hours":"12",
                "pollination_window_complete_before_barrier":"1",
                "ovary_swollen_at_barrier":"0","barrier_covers_pollinator_entry":"0",
                "pre_barrier_attack_present":"0","barrier_integrity_failure_present":"0",
                "realized_exsertion":"0.50","water_depth":"10.0","pollen_grains":"100",
                "pollinator_visits":"10","early_predator_attack_present":"1" if exp else "0",
                "ovule_count":"100","undamaged_seed_count":"50" if exp else "68",
                "damaged_seed_count":"20" if exp else "2","mechanical_damage":"0",
            })
    return rows


def _g_timing_config(season: str = "S1") -> dict:
    return {
        "schema": "SCH_PEDICULARIS_G_EVENT_TIME_PILOT_CONFIG_V1",
        "status": "PEDICULARIS_G_EVENT_TIME_PILOT_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": season,
        "pollination_completion_definition": "unit-test pollen criterion",
        "pollination_completion_measurement": "destructive stigma pollen count",
        "attack_event_definition": "visible egg or puncture",
        "ovary_swelling_definition": "unit-test visible swelling",
        "sampling_schedule_basis_note": "fixed unit-test schedule",
        "frozen_before_event_time_data": True,
        "frozen_at_utc": "2026-10-05T00:00:00Z",
    }


def _g_timing_rows(season: str = "S1") -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(4):
        for hours, pollen, complete in (
            (4, 10 + plant, 0),
            (8, 30 + plant, 1 if plant < 2 else 0),
            (12, 50 + plant, 1),
        ):
            rows.append({
                "population_id": "P_REX_TEST",
                "season_id": season,
                "plant_id": f"D{plant:02d}",
                "flower_id": f"D{plant:02d}_P{hours}",
                "flower_role": "POLLINATION_SENTINEL",
                "anthesis_time_hours": "0",
                "observation_time_hours": str(hours),
                "pollen_grains": str(pollen),
                "pollination_complete": str(complete),
                "attack_present": "",
                "ovary_swollen": "",
            })
        for hours, attack, swollen in (
            (4, 0, 0),
            (8, 0, 0),
            (12, 1 if plant < 2 else 0, 1 if plant >= 2 else 0),
        ):
            rows.append({
                "population_id": "P_REX_TEST",
                "season_id": season,
                "plant_id": f"D{plant:02d}",
                "flower_id": f"D{plant:02d}_N",
                "flower_role": "ATTACK_SWELL_SENTINEL",
                "anthesis_time_hours": "0",
                "observation_time_hours": str(hours),
                "pollen_grains": "",
                "pollination_complete": "",
                "attack_present": str(attack),
                "ovary_swollen": str(swollen),
            })
    return rows


def _write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _registry_rows(
    p0_rows: list[dict[str,str]],
    p1_rows: list[dict[str,str]],
    g_rows: list[dict[str,str]],
    g_timing_rows: list[dict[str,str]],
) -> list[dict[str,str]]:
    rows=[]
    def add(data,role,lane):
        seen: set[str] = set()
        for r in data:
            if r["flower_id"] in seen:
                continue
            seen.add(r["flower_id"])
            rows.append({
                "record_id":f"R{len(rows)+1:03d}","population_id":r["population_id"],
                "season_id":r["season_id"],"plant_id":r["plant_id"],
                "flower_id":r["flower_id"],"cohort_role":role,"lane":lane,
                "threshold_basis_eligible":"YES","confirmatory_eligible":"NO","notes":"",
            })
    add(p0_rows,"CAL_A","MULTI")
    add(p1_rows,"CAL_B_P1","P1")
    add(g_rows,"CAL_B_G","G")
    add(g_timing_rows,"CAL_B_G_TIMING","G")
    return rows


def _paths(
    tmp_path: Path,
    *,
    g_season: str="S1",
    g_timing_season: str="S1",
):
    p0=_p0_rows(); p1=_p1_rows(); g=_g_rows(g_season); rep=_repeatability_rows()
    gt=_g_timing_rows(g_timing_season)
    registry=_registry_rows(p0,p1,g,gt)
    return {
        "registry":_write(tmp_path/"registry.csv",REG_FIELDS,registry),
        "repeatability":_write(tmp_path/"repeat.csv",repmod.REQUIRED_FIELDS,rep),
        "p0":_write(tmp_path/"p0.csv",p0mod.REQUIRED_FIELDS,p0),
        "p1":_write(tmp_path/"p1.csv",p1mod.REQUIRED_FIELDS,p1),
        "g":_write(tmp_path/"g.csv",gmod.REQUIRED_FIELDS,g),
        "g_timing":_write(tmp_path/"g_timing.csv",list(gt[0]),gt),
        "g_timing_config":_write_json(
            tmp_path/"g_timing_config.json",
            _g_timing_config(g_timing_season),
        ),
    }


def test_complete_calibration_package_builds_two_summaries_and_receipt(tmp_path: Path) -> None:
    p=_paths(tmp_path)
    rep,cal,receipt=build_package(
        registry_path=p["registry"],repeatability_path=p["repeatability"],
        p0_path=p["p0"],p1_path=p["p1"],g_path=p["g"],
        g_timing_config_path=p["g_timing_config"],
        g_timing_path=p["g_timing"],
    )
    assert receipt["status"]=="PEDICULARIS_CALIBRATION_PACKAGE_READY_FOR_TARGET_FREEZE"
    assert receipt["allowed_repeatability_p0_overlap_n_flowers"]==4
    assert receipt["cross_lane_flower_overlap_detected"] is False
    assert receipt["dataset_registration"]["P0"]["role"]=="CAL_A"
    assert receipt["dataset_registration"]["P1"]["role"]=="CAL_B_P1"
    assert receipt["dataset_registration"]["G"]["role"]=="CAL_B_G"
    assert receipt["dataset_registration"]["G_TIMING"]["role"]=="CAL_B_G_TIMING"
    assert receipt["g_event_time_summary_status"] == (
        "G_EVENT_TIME_DESCRIPTORS_READY_NO_WINDOW_SELECTED"
    )
    assert receipt["g_effect_and_timing_flower_overlap_detected"] is False
    assert "G_TIMING" in cal["available_pilot_lanes"]
    assert rep["status"]=="CAL_A_REPEATABILITY_SUMMARY_ONLY_NO_MARGIN_DECISION"
    assert cal["status"]=="CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION"


def test_missing_registry_flower_fails_closed(tmp_path: Path) -> None:
    p0=_p0_rows(); p1=_p1_rows(); g=_g_rows(); rep=_repeatability_rows()
    gt=_g_timing_rows(); registry=_registry_rows(p0,p1,g,gt)
    registry=[r for r in registry if r["flower_id"]!=p1[0]["flower_id"]]
    paths={
        "registry":_write(tmp_path/"registry.csv",REG_FIELDS,registry),
        "repeatability":_write(tmp_path/"repeat.csv",repmod.REQUIRED_FIELDS,rep),
        "p0":_write(tmp_path/"p0.csv",p0mod.REQUIRED_FIELDS,p0),
        "p1":_write(tmp_path/"p1.csv",p1mod.REQUIRED_FIELDS,p1),
        "g":_write(tmp_path/"g.csv",gmod.REQUIRED_FIELDS,g),
        "g_timing":_write(tmp_path/"g_timing.csv",list(gt[0]),gt),
        "g_timing_config":_write_json(
            tmp_path/"g_timing_config.json",
            _g_timing_config(),
        ),
    }
    with pytest.raises(ValueError,match="missing from cohort registry"):
        build_package(registry_path=paths["registry"],repeatability_path=paths["repeatability"],
                      p0_path=paths["p0"],p1_path=paths["p1"],g_path=paths["g"],
                      g_timing_config_path=paths["g_timing_config"],
                      g_timing_path=paths["g_timing"])


def test_wrong_calibration_role_fails_closed(tmp_path: Path) -> None:
    p0=_p0_rows(); p1=_p1_rows(); g=_g_rows(); rep=_repeatability_rows()
    gt=_g_timing_rows(); registry=_registry_rows(p0,p1,g,gt)
    target=next(r for r in registry if r["flower_id"]==p1[0]["flower_id"])
    target["cohort_role"]="CAL_A"; target["lane"]="MULTI"
    paths={
        "registry":_write(tmp_path/"registry.csv",REG_FIELDS,registry),
        "repeatability":_write(tmp_path/"repeat.csv",repmod.REQUIRED_FIELDS,rep),
        "p0":_write(tmp_path/"p0.csv",p0mod.REQUIRED_FIELDS,p0),
        "p1":_write(tmp_path/"p1.csv",p1mod.REQUIRED_FIELDS,p1),
        "g":_write(tmp_path/"g.csv",gmod.REQUIRED_FIELDS,g),
        "g_timing":_write(tmp_path/"g_timing.csv",list(gt[0]),gt),
        "g_timing_config":_write_json(
            tmp_path/"g_timing_config.json",
            _g_timing_config(),
        ),
    }
    with pytest.raises(ValueError,match="wrong cohort_role"):
        build_package(registry_path=paths["registry"],repeatability_path=paths["repeatability"],
                      p0_path=paths["p0"],p1_path=paths["p1"],g_path=paths["g"],
                      g_timing_config_path=paths["g_timing_config"],
                      g_timing_path=paths["g_timing"])


def test_repeatability_flowers_must_be_subset_of_p0_cal_a(tmp_path: Path) -> None:
    p0=_p0_rows(); p1=_p1_rows(); g=_g_rows(); rep=_repeatability_rows()
    extra=dict(rep[0]); extra["flower_id"]="A_EXTRA"; extra["measurement_replicate"]="1"
    extra2=dict(extra); extra2["measurement_replicate"]="2"
    rep.extend([extra,extra2])
    gt=_g_timing_rows(); registry=_registry_rows(p0,p1,g,gt)
    registry.append({
        "record_id":"R999","population_id":"P_REX_TEST","season_id":"S1",
        "plant_id":extra["plant_id"],"flower_id":"A_EXTRA","cohort_role":"CAL_A",
        "lane":"MULTI","threshold_basis_eligible":"YES","confirmatory_eligible":"NO","notes":"",
    })
    paths={
        "registry":_write(tmp_path/"registry.csv",REG_FIELDS,registry),
        "repeatability":_write(tmp_path/"repeat.csv",repmod.REQUIRED_FIELDS,rep),
        "p0":_write(tmp_path/"p0.csv",p0mod.REQUIRED_FIELDS,p0),
        "p1":_write(tmp_path/"p1.csv",p1mod.REQUIRED_FIELDS,p1),
        "g":_write(tmp_path/"g.csv",gmod.REQUIRED_FIELDS,g),
        "g_timing":_write(tmp_path/"g_timing.csv",list(gt[0]),gt),
        "g_timing_config":_write_json(
            tmp_path/"g_timing_config.json",
            _g_timing_config(),
        ),
    }
    with pytest.raises(ValueError,match="must be a subset"):
        build_package(registry_path=paths["registry"],repeatability_path=paths["repeatability"],
                      p0_path=paths["p0"],p1_path=paths["p1"],g_path=paths["g"],
                      g_timing_config_path=paths["g_timing_config"],
                      g_timing_path=paths["g_timing"])


def test_all_calibration_inputs_must_share_context(tmp_path: Path) -> None:
    p=_paths(tmp_path,g_season="S2")
    with pytest.raises(
        ValueError,
        match="population and season|contexts must match exactly",
    ):
        build_package(
            registry_path=p["registry"],
            repeatability_path=p["repeatability"],
            p0_path=p["p0"],
            p1_path=p["p1"],
            g_path=p["g"],
            g_timing_config_path=p["g_timing_config"],
            g_timing_path=p["g_timing"],
        )


def test_g_event_time_context_mismatch_fails_package(tmp_path: Path) -> None:
    p=_paths(tmp_path,g_timing_season="S2")
    with pytest.raises(
        ValueError,
        match="population and season|contexts must match exactly",
    ):
        build_package(
            registry_path=p["registry"],
            repeatability_path=p["repeatability"],
            p0_path=p["p0"],
            p1_path=p["p1"],
            g_path=p["g"],
            g_timing_config_path=p["g_timing_config"],
            g_timing_path=p["g_timing"],
        )


def test_g_effect_and_event_time_cannot_reuse_a_flower(tmp_path: Path) -> None:
    p0=_p0_rows(); p1=_p1_rows(); g=_g_rows(); rep=_repeatability_rows()
    gt=_g_timing_rows()
    gt[0]["flower_id"] = g[0]["flower_id"]
    registry=_registry_rows(p0,p1,g,gt)
    paths={
        "registry":_write(tmp_path/"registry.csv",REG_FIELDS,registry),
        "repeatability":_write(tmp_path/"repeat.csv",repmod.REQUIRED_FIELDS,rep),
        "p0":_write(tmp_path/"p0.csv",p0mod.REQUIRED_FIELDS,p0),
        "p1":_write(tmp_path/"p1.csv",p1mod.REQUIRED_FIELDS,p1),
        "g":_write(tmp_path/"g.csv",gmod.REQUIRED_FIELDS,g),
        "g_timing":_write(tmp_path/"g_timing.csv",list(gt[0]),gt),
        "g_timing_config":_write_json(
            tmp_path/"g_timing_config.json",
            _g_timing_config(),
        ),
    }
    with pytest.raises(
        ValueError,
        match="flower_id must be globally unique|flower reuse",
    ):
        build_package(
            registry_path=paths["registry"],
            repeatability_path=paths["repeatability"],
            p0_path=paths["p0"],
            p1_path=paths["p1"],
            g_path=paths["g"],
            g_timing_config_path=paths["g_timing_config"],
            g_timing_path=paths["g_timing"],
        )

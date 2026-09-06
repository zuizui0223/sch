from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from scripts.analyze_pedicularis_full_surface_v2 import analyze as analyze_surface, to_sch_rows
from scripts.estimate_sch_conflict_budget import estimate as estimate_conflict_budget


REQUIRED_GENERATING_FIELDS = (
    "z_levels",
    "baseline_fitness",
    "pollination_peak",
    "pollination_optimum",
    "pollination_curvature",
    "antagonist_peak",
    "antagonist_optimum",
    "antagonist_curvature",
    "between_plant_sd",
    "residual_sd",
    "ovule_count",
    "water_depth_mean",
    "water_depth_sd",
    "mechanical_damage_rate",
    "predator_attack_rate_exposed",
    "predator_attack_rate_excluded",
)


def _require_frozen(value: object, name: str) -> object:
    if value == "REQUIRED_BEFORE_USE" or value is None:
        raise ValueError(f"{name} must be prospectively frozen before power simulation")
    return value


def _number(value: object, name: str, *, nonnegative: bool = False) -> float:
    _require_frozen(value, name)
    out = float(value)
    if not math.isfinite(out):
        raise ValueError(f"{name} must be finite")
    if nonnegative and out < 0:
        raise ValueError(f"{name} must be non-negative")
    return out


def _prob(value: object, name: str) -> float:
    out = _number(value, name, nonnegative=True)
    if out > 1:
        raise ValueError(f"{name} must lie in [0,1]")
    return out


def _read_config(config: dict) -> tuple[list[int], int, float, dict, dict, dict]:
    if "DO_NOT_RUN" in str(config.get("status", "")):
        raise ValueError("power template must be copied and fully frozen before use")
    raw_candidates = _require_frozen(config.get("candidate_plants_per_cell"), "candidate_plants_per_cell")
    if not isinstance(raw_candidates, list) or not raw_candidates:
        raise ValueError("candidate_plants_per_cell must be a non-empty list")
    candidates = sorted({int(value) for value in raw_candidates})
    if candidates[0] < 2:
        raise ValueError("candidate plants per cell must be >=2")
    reps = int(_require_frozen(config.get("simulation_reps"), "simulation_reps"))
    if reps < 1:
        raise ValueError("simulation_reps must be >=1")
    target = _number(config.get("target_joint_power"), "target_joint_power", nonnegative=True)
    if target > 1:
        raise ValueError("target_joint_power must lie in [0,1]")

    model = config.get("generating_model")
    if not isinstance(model, dict):
        raise ValueError("generating_model must be an object")
    for field in REQUIRED_GENERATING_FIELDS:
        _require_frozen(model.get(field), f"generating_model.{field}")
    z_levels = model["z_levels"]
    if not isinstance(z_levels, list) or len(z_levels) < 5:
        raise ValueError("generating_model.z_levels must contain at least five levels")
    if len({float(value) for value in z_levels}) != len(z_levels):
        raise ValueError("z levels must be distinct")

    surface_config = config.get("production_surface_config")
    budget_config = config.get("production_conflict_budget_config")
    if not isinstance(surface_config, dict) or not isinstance(budget_config, dict):
        raise ValueError("production analyzer configs are required")
    return candidates, reps, target, model, surface_config, budget_config


def _readiness(population: str, season: str) -> dict:
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3",
        "status": "PEDICULARIS_FULL_SURFACE_READY",
        "population_id": population,
        "season_id": season,
        "water_y_requirement": "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "predator_method_requirement": "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED",
        "source_receipts": {"g": {"schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V3"}},
    }


def _component(z: float, peak: float, optimum: float, curvature: float) -> float:
    return peak - curvature * (z - optimum) ** 2


def generate_rows(model: dict, plants_per_cell: int, rng: random.Random) -> list[dict[str, str]]:
    z_levels = [float(value) for value in model["z_levels"]]
    baseline = _number(model["baseline_fitness"], "baseline_fitness")
    p_peak = _number(model["pollination_peak"], "pollination_peak")
    p_opt = _number(model["pollination_optimum"], "pollination_optimum")
    p_curv = _number(model["pollination_curvature"], "pollination_curvature", nonnegative=True)
    g_peak = _number(model["antagonist_peak"], "antagonist_peak")
    g_opt = _number(model["antagonist_optimum"], "antagonist_optimum")
    g_curv = _number(model["antagonist_curvature"], "antagonist_curvature", nonnegative=True)
    plant_sd = _number(model["between_plant_sd"], "between_plant_sd", nonnegative=True)
    residual_sd = _number(model["residual_sd"], "residual_sd", nonnegative=True)
    ovules = _number(model["ovule_count"], "ovule_count", nonnegative=True)
    water_mean = _number(model["water_depth_mean"], "water_depth_mean")
    water_sd = _number(model["water_depth_sd"], "water_depth_sd", nonnegative=True)
    damage_rate = _prob(model["mechanical_damage_rate"], "mechanical_damage_rate")
    attack_exposed = _prob(model["predator_attack_rate_exposed"], "predator_attack_rate_exposed")
    attack_excluded = _prob(model["predator_attack_rate_excluded"], "predator_attack_rate_excluded")
    if ovules <= 0 or p_curv <= 0 or g_curv <= 0:
        raise ValueError("ovule_count and both curvatures must be >0")

    rows: list[dict[str, str]] = []
    # Complete-block planning model: every independent plant contributes one focal
    # flower to every treatment cell. If the field design is incomplete-block,
    # extend the generator rather than treating flowers as independent plants.
    plant_effects = [rng.gauss(0.0, plant_sd) for _ in range(plants_per_cell)]
    for plant, plant_effect in enumerate(plant_effects):
        for zi, z in enumerate(z_levels):
            f1 = _component(z, p_peak, p_opt, p_curv)
            f2 = _component(z, g_peak, g_opt, g_curv)
            for p_name, p in (("SUPPLEMENTED", 0), ("NATURAL", 1)):
                for g_name, g in (("EXCLUDED", 0), ("EXPOSED", 1)):
                    mu = baseline + plant_effect + p * f1 + g * f2
                    undamaged = max(0.0, min(ovules, rng.gauss(mu, residual_sd)))
                    attack_rate = attack_exposed if g else attack_excluded
                    attacked = 1 if rng.random() < attack_rate else 0
                    damaged = min(max(0.0, ovules - undamaged), (0.08 * ovules if attacked else 0.0))
                    undamaged = min(undamaged, ovules - damaged)
                    pollen = max(0.0, 100.0 + 4.0 * z + (8.0 if p else 0.0) + rng.gauss(0, 2.0))
                    water = water_mean + rng.gauss(0.0, water_sd)
                    rows.append(
                        {
                            "population_id": "PEDICULARIS_POWER_SIM",
                            "season_id": "SIM_SEASON",
                            "plant_id": f"P{plant:04d}",
                            "flower_id": f"P{plant:04d}_Z{zi}_P{p}G{g}",
                            "assigned_z_level": f"Z{zi}",
                            "realized_exsertion": f"{z:.8f}",
                            "pollination_treatment": p_name,
                            "predator_treatment": g_name,
                            "exclusion_method": "SIMULATED_METHOD_QUALIFIED",
                            "water_depth": f"{water:.8f}",
                            "ovule_count": f"{ovules:.8f}",
                            "undamaged_seed_count": f"{undamaged:.8f}",
                            "damaged_seed_count": f"{damaged:.8f}",
                            "pollen_grains": f"{pollen:.8f}",
                            "early_predator_attack_present": str(attacked),
                            "mechanical_damage": str(1 if rng.random() < damage_rate else 0),
                        }
                    )
    return rows


def _truth_upgrade(model: dict) -> dict:
    return {
        "receipt_schema_version": "SIMULATION_TRUTH_ONLY",
        "pure_function_upgrade": {
            "schema_version": "SIMULATION_CONTEXT_STABLE_COMPONENT_OPTIMA_V1",
            "status": "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED",
        },
        "identified_pure_function_optima": {
            "z_F1": float(model["pollination_optimum"]),
            "z_F2": float(model["antagonist_optimum"]),
        },
    }


def simulate_power(config: dict) -> dict:
    candidates, reps, target, model, surface_config, budget_config = _read_config(config)
    master = random.Random(int(config.get("simulation_seed", 20260906)))
    results = []
    for n in candidates:
        surface_success = 0
        budget_success = 0
        joint_success = 0
        failures = 0
        for _ in range(reps):
            rng = random.Random(master.randrange(1, 2**31 - 1))
            rows = generate_rows(model, n, rng)
            try:
                surface = analyze_surface(rows, _readiness("PEDICULARIS_POWER_SIM", "SIM_SEASON"), surface_config)
                surface_ok = surface.get("status") == "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
                budget = estimate_conflict_budget(
                    to_sch_rows(rows),
                    _truth_upgrade(model),
                    budget_config,
                )
                budget_lo = float(budget["criticality_export"]["L_S_component_95_ci"][0])
                budget_ok = budget_lo > 0.0
            except (ValueError, KeyError, TypeError):
                failures += 1
                surface_ok = False
                budget_ok = False
            surface_success += int(surface_ok)
            budget_success += int(budget_ok)
            joint_success += int(surface_ok and budget_ok)
        row = {
            "plants_per_cell": n,
            "simulation_reps": reps,
            "surface_gate_power": surface_success / reps,
            "positive_conflict_budget_power": budget_success / reps,
            "joint_primary_gate_power": joint_success / reps,
            "analysis_failure_fraction": failures / reps,
        }
        results.append(row)

    eligible = [row["plants_per_cell"] for row in results if row["joint_primary_gate_power"] >= target]
    return {
        "analysis": "pedicularis_experiment_a_full_pipeline_power",
        "design_assumption": "balanced complete-block planning model; one focal flower per treatment cell per independent plant cluster",
        "target_joint_power": target,
        "candidate_results": results,
        "minimum_candidate_meeting_target": min(eligible) if eligible else None,
        "claim_ceiling": (
            "planning simulation conditional on prospectively frozen pilot parameters and generating model; "
            "not empirical evidence and not a substitute for field manipulation checks"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    result = simulate_power(config)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path

from scripts import analyze_pedicularis_full_surface as full_surface
from scripts import analyze_pedicularis_antagonist_constrained_pollination as secondary
from scripts.classify_pedicularis_empirical_outcome import (
    DEFAULT_WORLDS,
    _read_worlds,
    build as classify_world,
)
from scripts.pedicularis_config_freeze import FREEZE_STATUS


SCHEMA = "PEDICULARIS_W1_W2_POWER_CONFIG_V1"
FROZEN_STATUS = "PEDICULARIS_W1_W2_POWER_INPUTS_PROSPECTIVELY_FROZEN"
POSITIVE_SURFACE = "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
STATES = ("P0G0", "P1G0", "P0G1", "P1G1")
STATE_TREATMENTS = {
    "P0G0": ("SUPPLEMENTED", "EXCLUDED"),
    "P1G0": ("NATURAL", "EXCLUDED"),
    "P0G1": ("SUPPLEMENTED", "EXPOSED"),
    "P1G1": ("NATURAL", "EXPOSED"),
}
PLACEHOLDER = "REQUIRED_BEFORE_USE"


def _number(value: object, label: str) -> float:
    if value in (None, "", PLACEHOLDER):
        raise ValueError(f"{label} must be prospectively frozen")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{label} must be finite")
    return out


def _probability(value: object, label: str) -> float:
    out = _number(value, label)
    if not 0.0 <= out <= 1.0:
        raise ValueError(f"{label} must lie in [0, 1]")
    return out


def _positive_int(value: object, label: str) -> int:
    out = _number(value, label)
    if out < 1 or not float(out).is_integer():
        raise ValueError(f"{label} must be a positive integer")
    return int(out)


def _nonempty_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or value == PLACEHOLDER:
        raise ValueError(f"{label} must be prospectively frozen")
    return value.strip()


def _surface_model(payload: object, label: str) -> dict[str, float]:
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be an object")
    peak = _number(payload.get("peak"), f"{label}.peak")
    optimum = _number(payload.get("optimum"), f"{label}.optimum")
    curvature = _number(payload.get("curvature"), f"{label}.curvature")
    if curvature <= 0:
        raise ValueError(f"{label}.curvature must be > 0")
    return {"peak": peak, "optimum": optimum, "curvature": curvature}


def _linear_model(
    payload: object,
    label: str,
    *,
    fraction: bool,
) -> dict[str, float]:
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be an object")
    if fraction:
        intercept_key = "intercept_fraction"
        slope_key = "z_slope_fraction"
    else:
        intercept_key = "intercept"
        slope_key = "z_slope"
    return {
        intercept_key: _number(
            payload.get(intercept_key),
            f"{label}.{intercept_key}",
        ),
        slope_key: _number(
            payload.get(slope_key),
            f"{label}.{slope_key}",
        ),
    }


def _validate_config(config: dict) -> dict:
    if config.get("schema") != SCHEMA:
        raise ValueError("W1/W2 power config schema mismatch")
    if config.get("status") != FROZEN_STATUS:
        raise ValueError("W1/W2 power inputs are not prospectively frozen")

    provenance = config.get("planning_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("planning_provenance is required")
    population_id = _nonempty_text(
        provenance.get("population_id"),
        "planning_provenance.population_id",
    )
    season_id = _nonempty_text(
        provenance.get("season_id"),
        "planning_provenance.season_id",
    )
    _nonempty_text(
        provenance.get("basis_document"),
        "planning_provenance.basis_document",
    )
    if provenance.get("frozen_before_full_surface_data") is not True:
        raise ValueError(
            "power inputs must be frozen before full-surface outcome data"
        )

    raw_candidates = config.get("candidate_complete_block_plants")
    if not isinstance(raw_candidates, list) or not raw_candidates:
        raise ValueError(
            "candidate_complete_block_plants must be a non-empty list"
        )
    candidates = sorted(
        {
            _positive_int(value, "candidate_complete_block_plants")
            for value in raw_candidates
        }
    )
    if candidates[0] < 3:
        raise ValueError(
            "candidate_complete_block_plants must be >=3 for the secondary bootstrap"
        )

    reps = _positive_int(config.get("simulation_reps"), "simulation_reps")
    target_primary = _probability(
        config.get("target_primary_surface_power"),
        "target_primary_surface_power",
    )
    target_headline = _probability(
        config.get("target_headline_w1_or_w2_power"),
        "target_headline_w1_or_w2_power",
    )

    model = config.get("generating_model")
    if not isinstance(model, dict):
        raise ValueError("generating_model is required")

    z_raw = model.get("z_levels")
    if not isinstance(z_raw, list) or len(z_raw) < 5:
        raise ValueError("generating_model.z_levels must contain >=5 values")
    z_levels = [float(_number(value, "generating_model.z_levels")) for value in z_raw]
    if len(set(z_levels)) != len(z_levels):
        raise ValueError("generating_model.z_levels must be distinct")
    z_levels = sorted(z_levels)

    ovules = _number(model.get("ovule_count"), "generating_model.ovule_count")
    if ovules <= 0:
        raise ValueError("generating_model.ovule_count must be > 0")

    fitness_between = _number(
        model.get("fitness_between_plant_sd"),
        "generating_model.fitness_between_plant_sd",
    )
    fitness_residual = _number(
        model.get("fitness_residual_sd"),
        "generating_model.fitness_residual_sd",
    )
    pollen_between = _number(
        model.get("pollen_between_plant_sd"),
        "generating_model.pollen_between_plant_sd",
    )
    pollen_residual = _number(
        model.get("pollen_residual_sd"),
        "generating_model.pollen_residual_sd",
    )
    seed_between = _number(
        model.get("initial_seed_between_plant_sd_fraction"),
        "generating_model.initial_seed_between_plant_sd_fraction",
    )
    seed_residual = _number(
        model.get("initial_seed_residual_sd_fraction"),
        "generating_model.initial_seed_residual_sd_fraction",
    )
    for label, value in (
        ("fitness_between_plant_sd", fitness_between),
        ("fitness_residual_sd", fitness_residual),
        ("pollen_between_plant_sd", pollen_between),
        ("pollen_residual_sd", pollen_residual),
        ("initial_seed_between_plant_sd_fraction", seed_between),
        ("initial_seed_residual_sd_fraction", seed_residual),
    ):
        if value < 0:
            raise ValueError(f"generating_model.{label} must be >=0")

    surface_payload = model.get("state_fitness_surfaces")
    pollen_payload = model.get("pollen_state_models")
    seed_payload = model.get("initial_seed_state_models")
    if not all(isinstance(value, dict) for value in (
        surface_payload,
        pollen_payload,
        seed_payload,
    )):
        raise ValueError("all generating state-model objects are required")

    surfaces = {
        state: _surface_model(
            surface_payload.get(state),
            f"state_fitness_surfaces.{state}",
        )
        for state in STATES
    }
    pollen_models = {
        state: _linear_model(
            pollen_payload.get(state),
            f"pollen_state_models.{state}",
            fraction=False,
        )
        for state in STATES
    }
    seed_models = {
        state: _linear_model(
            seed_payload.get(state),
            f"initial_seed_state_models.{state}",
            fraction=True,
        )
        for state in STATES
    }

    # Fail before simulation when the mean model itself requires impossible
    # negative damaged-seed counts. Random noise can still create rare clipping,
    # which is tracked explicitly in the simulation output.
    min_expected_seed_margin = math.inf
    for state in STATES:
        for z in z_levels:
            surface = surfaces[state]
            final_mean = (
                surface["peak"]
                - surface["curvature"] * (z - surface["optimum"]) ** 2
            )
            seed = seed_models[state]
            initial_fraction = (
                seed["intercept_fraction"]
                + seed["z_slope_fraction"] * z
            )
            if not 0.0 <= initial_fraction <= 1.0:
                raise ValueError(
                    f"expected initial-seed fraction for {state} at z={z} "
                    "falls outside [0,1]"
                )
            initial_mean = ovules * initial_fraction
            if final_mean < 0 or final_mean > ovules:
                raise ValueError(
                    f"expected undamaged-seed fitness for {state} at z={z} "
                    "falls outside [0, ovule_count]"
                )
            min_expected_seed_margin = min(
                min_expected_seed_margin,
                initial_mean - final_mean,
            )
    if min_expected_seed_margin < 0:
        raise ValueError(
            "expected initial seed count must be >= expected undamaged mature "
            "seed count in every generated cell"
        )

    attack_excluded = _probability(
        model.get("early_attack_rate_excluded"),
        "generating_model.early_attack_rate_excluded",
    )
    attack_exposed = _probability(
        model.get("early_attack_rate_exposed"),
        "generating_model.early_attack_rate_exposed",
    )
    water_depth = _number(
        model.get("water_depth"),
        "generating_model.water_depth",
    )

    surface_config = config.get("production_surface_config")
    secondary_config = config.get("secondary_diagnostic_config")
    if not isinstance(surface_config, dict):
        raise ValueError("production_surface_config is required")
    if not isinstance(secondary_config, dict):
        raise ValueError("secondary_diagnostic_config is required")

    # Validate the minimum requirements of the production analyzers now, rather
    # than discovering an unfrozen setting during the simulation.
    sch = surface_config.get("sch_surface")
    checks = surface_config.get("system_checks")
    if not isinstance(sch, dict) or not isinstance(checks, dict):
        raise ValueError(
            "production_surface_config must contain sch_surface and system_checks"
        )
    if _positive_int(sch.get("bootstrap_reps"), "sch_surface.bootstrap_reps") < 200:
        raise ValueError("sch_surface.bootstrap_reps must be >=200")
    if _positive_int(
        secondary_config.get("bootstrap_reps"),
        "secondary_diagnostic_config.bootstrap_reps",
    ) < 200:
        raise ValueError("secondary_diagnostic_config.bootstrap_reps must be >=200")

    return {
        "planning_provenance": {
            **provenance,
            "population_id": population_id,
            "season_id": season_id,
        },
        "candidate_complete_block_plants": candidates,
        "simulation_reps": reps,
        "simulation_seed": int(config.get("simulation_seed", 20261005)),
        "target_primary_surface_power": target_primary,
        "target_headline_w1_or_w2_power": target_headline,
        "generating_model": {
            "z_levels": z_levels,
            "ovule_count": ovules,
            "fitness_between_plant_sd": fitness_between,
            "fitness_residual_sd": fitness_residual,
            "state_fitness_surfaces": surfaces,
            "pollen_between_plant_sd": pollen_between,
            "pollen_residual_sd": pollen_residual,
            "pollen_state_models": pollen_models,
            "initial_seed_between_plant_sd_fraction": seed_between,
            "initial_seed_residual_sd_fraction": seed_residual,
            "initial_seed_state_models": seed_models,
            "early_attack_rate_excluded": attack_excluded,
            "early_attack_rate_exposed": attack_exposed,
            "water_depth": water_depth,
            "minimum_expected_initial_minus_final_seed_count": (
                min_expected_seed_margin
            ),
        },
        "production_surface_config": surface_config,
        "secondary_diagnostic_config": secondary_config,
    }


def _readiness(population_id: str, season_id: str) -> dict:
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3",
        "status": "PEDICULARIS_FULL_SURFACE_READY",
        "population_id": population_id,
        "season_id": season_id,
        "water_y_requirement": "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "predator_method_requirement": (
            "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_"
            "WITH_POLLINATOR_ACCESS_PRESERVED"
        ),
        "source_receipts": {
            "z": {
                "schema": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1",
                "threshold_freeze_status": FREEZE_STATUS,
            },
            "p": {
                "schema": "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1",
                "threshold_freeze_status": FREEZE_STATUS,
            },
            "g": {
                "schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V4",
                "threshold_freeze_status": FREEZE_STATUS,
            },
        },
    }


def _state_mean(surface: dict[str, float], z: float) -> float:
    return (
        surface["peak"]
        - surface["curvature"] * (z - surface["optimum"]) ** 2
    )


def generate_rows(
    model: dict,
    n_plants: int,
    rng: random.Random,
    *,
    population_id: str = "PEDICULARIS_W1W2_POWER",
    season_id: str = "SIMULATION",
) -> tuple[list[dict[str, str]], dict]:
    z_levels = model["z_levels"]
    ovules = float(model["ovule_count"])
    surfaces = model["state_fitness_surfaces"]
    pollen_models = model["pollen_state_models"]
    seed_models = model["initial_seed_state_models"]

    rows: list[dict[str, str]] = []
    final_clip_count = 0
    initial_clip_count = 0
    initial_floor_count = 0

    for plant_index in range(n_plants):
        plant_id = f"P{plant_index:04d}"
        fitness_plant = rng.gauss(
            0.0,
            float(model["fitness_between_plant_sd"]),
        )
        pollen_plant = rng.gauss(
            0.0,
            float(model["pollen_between_plant_sd"]),
        )
        initial_plant = rng.gauss(
            0.0,
            float(model["initial_seed_between_plant_sd_fraction"]),
        )

        for z_index, z in enumerate(z_levels):
            for state in STATES:
                pollination, predator = STATE_TREATMENTS[state]

                final_value = (
                    _state_mean(surfaces[state], z)
                    + fitness_plant
                    + rng.gauss(0.0, float(model["fitness_residual_sd"]))
                )
                clipped_final = min(ovules, max(0.0, final_value))
                final_clip_count += int(clipped_final != final_value)

                pollen_model = pollen_models[state]
                pollen_value = (
                    pollen_model["intercept"]
                    + pollen_model["z_slope"] * z
                    + pollen_plant
                    + rng.gauss(0.0, float(model["pollen_residual_sd"]))
                )
                pollen_value = max(0.0, pollen_value)

                seed_model = seed_models[state]
                initial_fraction = (
                    seed_model["intercept_fraction"]
                    + seed_model["z_slope_fraction"] * z
                    + initial_plant
                    + rng.gauss(
                        0.0,
                        float(model["initial_seed_residual_sd_fraction"]),
                    )
                )
                clipped_fraction = min(1.0, max(0.0, initial_fraction))
                initial_clip_count += int(clipped_fraction != initial_fraction)
                initial_count = ovules * clipped_fraction

                if initial_count < clipped_final:
                    initial_count = clipped_final
                    initial_floor_count += 1

                damaged = initial_count - clipped_final
                attack_rate = (
                    float(model["early_attack_rate_exposed"])
                    if predator == "EXPOSED"
                    else float(model["early_attack_rate_excluded"])
                )
                attacked = int(rng.random() < attack_rate)

                rows.append(
                    {
                        "population_id": population_id,
                        "season_id": season_id,
                        "plant_id": plant_id,
                        "flower_id": (
                            f"{plant_id}_Z{z_index}_{state}"
                        ),
                        "assigned_z_level": f"Z{z_index:02d}",
                        "realized_exsertion": repr(float(z)),
                        "pollination_treatment": pollination,
                        "predator_treatment": predator,
                        "exclusion_method": (
                            "SIMULATED_QUALIFIED_PREDATOR_EXCLUSION"
                            if predator == "EXCLUDED"
                            else "SIMULATED_MATCHED_EXPOSED_SHAM"
                        ),
                        "water_depth": repr(float(model["water_depth"])),
                        "ovule_count": repr(ovules),
                        "undamaged_seed_count": repr(clipped_final),
                        "damaged_seed_count": repr(damaged),
                        "pollen_grains": repr(pollen_value),
                        "early_predator_attack_present": str(attacked),
                        "mechanical_damage": "0",
                    }
                )

    n_rows = len(rows)
    return rows, {
        "n_rows": n_rows,
        "n_plants": n_plants,
        "flowers_per_plant": len(z_levels) * len(STATES),
        "final_seed_boundary_clip_fraction": final_clip_count / n_rows,
        "initial_seed_fraction_clip_fraction": initial_clip_count / n_rows,
        "initial_seed_floored_at_final_seed_fraction": (
            initial_floor_count / n_rows
        ),
    }


def _truth_descriptor(model: dict) -> dict:
    surfaces = model["state_fitness_surfaces"]
    pollen = model["pollen_state_models"]
    seed = model["initial_seed_state_models"]
    shift = (
        surfaces["P1G0"]["optimum"] - surfaces["P1G1"]["optimum"]
    )
    pollen_positive = (
        pollen["P1G0"]["z_slope"] > 0
        and pollen["P1G1"]["z_slope"] > 0
    )
    seed_positive = (
        seed["P1G0"]["z_slope_fraction"] > 0
        and seed["P1G1"]["z_slope_fraction"] > 0
    )
    if shift > 0 and pollen_positive and seed_positive:
        intended_world = "W1"
    elif shift > 0 and pollen_positive:
        intended_world = "W2"
    elif shift > 0:
        intended_world = "W3"
    elif pollen_positive:
        intended_world = "W4"
    else:
        intended_world = "W5"
    return {
        "generating_z_predator_free_natural_optimum": surfaces["P1G0"][
            "optimum"
        ],
        "generating_z_predator_exposed_natural_optimum": surfaces["P1G1"][
            "optimum"
        ],
        "generating_shift_remove_antagonist": shift,
        "generating_pollen_slopes_positive_in_both_G_states": pollen_positive,
        "generating_initial_seed_slopes_positive_in_both_G_states": seed_positive,
        "intended_secondary_world_if_primary_surface_passes": intended_world,
    }


def simulate_power(
    config: dict,
    *,
    world_rows: list[dict[str, str]] | None = None,
) -> dict:
    frozen = _validate_config(config)
    worlds = _read_worlds(DEFAULT_WORLDS) if world_rows is None else world_rows
    provenance = frozen["planning_provenance"]
    population_id = provenance["population_id"]
    season_id = provenance["season_id"]
    reps = frozen["simulation_reps"]
    master = random.Random(frozen["simulation_seed"])

    candidate_results = []
    for n_plants in frozen["candidate_complete_block_plants"]:
        primary_success = 0
        shift_success = 0
        pollen_success = 0
        initial_seed_success = 0
        headline_success = 0
        w1_success = 0
        analysis_failures = 0
        world_counts = {f"W{i}": 0 for i in range(6)}
        clip_sums = {
            "final_seed_boundary_clip_fraction": 0.0,
            "initial_seed_fraction_clip_fraction": 0.0,
            "initial_seed_floored_at_final_seed_fraction": 0.0,
        }

        for _ in range(reps):
            rng = random.Random(master.randrange(1, 2**31 - 1))
            rows, generation = generate_rows(
                frozen["generating_model"],
                n_plants,
                rng,
                population_id=population_id,
                season_id=season_id,
            )
            for key in clip_sums:
                clip_sums[key] += float(generation[key])

            try:
                surface_receipt = full_surface.analyze(
                    rows,
                    _readiness(population_id, season_id),
                    frozen["production_surface_config"],
                )
                is_primary = surface_receipt.get("status") == POSITIVE_SURFACE
                primary_success += int(is_primary)

                if is_primary:
                    secondary_receipt = secondary.build(
                        rows,
                        surface_receipt,
                        frozen["secondary_diagnostic_config"],
                    )
                    shift = bool(
                        secondary_receipt[
                            "predator_removal_shifts_optimum_upward"
                        ]
                    )
                    pollen = bool(
                        secondary_receipt[
                            "higher_z_increases_pollen_receipt_in_both_G_states"
                        ]
                    )
                    seed = bool(
                        secondary_receipt[
                            "higher_z_increases_initial_seed_set_in_both_G_states"
                        ]
                    )
                    shift_success += int(shift)
                    pollen_success += int(pollen)
                    initial_seed_success += int(seed)
                    outcome = classify_world(
                        surface_receipt,
                        secondary_receipt,
                        worlds,
                    )
                else:
                    outcome = classify_world(
                        surface_receipt,
                        None,
                        worlds,
                    )

                world_id = outcome.get("world_id")
                if world_id not in world_counts:
                    raise ValueError(
                        "production outcome classifier did not return W0-W5"
                    )
                world_counts[world_id] += 1
                headline_success += int(world_id in {"W1", "W2"})
                w1_success += int(world_id == "W1")
            except (ValueError, KeyError, TypeError, ZeroDivisionError):
                analysis_failures += 1

        candidate_results.append(
            {
                "complete_block_plants": n_plants,
                "flowers_per_treatment_cell": n_plants,
                "flowers_per_plant": (
                    len(frozen["generating_model"]["z_levels"]) * len(STATES)
                ),
                "total_full_surface_flowers": (
                    n_plants
                    * len(frozen["generating_model"]["z_levels"])
                    * len(STATES)
                ),
                "simulation_reps": reps,
                "primary_surface_power": primary_success / reps,
                "enemy_optimum_shift_power": shift_success / reps,
                "positive_pollen_gradient_both_G_states_power": (
                    pollen_success / reps
                ),
                "positive_initial_seed_gradient_both_G_states_power": (
                    initial_seed_success / reps
                ),
                "headline_W1_or_W2_power": headline_success / reps,
                "strongest_W1_power": w1_success / reps,
                "world_probabilities": {
                    world: count / reps
                    for world, count in world_counts.items()
                },
                "analysis_failure_fraction": analysis_failures / reps,
                "mean_generation_clip_diagnostics": {
                    key: value / reps
                    for key, value in clip_sums.items()
                },
            }
        )

    eligible = [
        row["complete_block_plants"]
        for row in candidate_results
        if row["primary_surface_power"]
        >= frozen["target_primary_surface_power"]
        and row["headline_W1_or_W2_power"]
        >= frozen["target_headline_w1_or_w2_power"]
    ]

    return {
        "analysis": "pedicularis_W1_W2_full_surface_power_v1",
        "planning_provenance": provenance,
        "design_assumption": (
            "balanced complete-block planning model: each independent plant "
            "contributes one focal flower to every z x P x G cell"
        ),
        "conditioning_statement": (
            "power is conditional on P0/P1/G having already passed their "
            "separate CAL-C qualification and full-surface readiness gates"
        ),
        "target_primary_surface_power": frozen["target_primary_surface_power"],
        "target_headline_w1_or_w2_power": frozen[
            "target_headline_w1_or_w2_power"
        ],
        "generating_truth_descriptor": _truth_descriptor(
            frozen["generating_model"]
        ),
        "candidate_results": candidate_results,
        "minimum_complete_block_plants_meeting_both_targets": (
            min(eligible) if eligible else None
        ),
        "minimum_total_full_surface_flowers_meeting_both_targets": (
            min(eligible)
            * len(frozen["generating_model"]["z_levels"])
            * len(STATES)
            if eligible
            else None
        ),
        "status": "PEDICULARIS_W1_W2_POWER_SIMULATION_COMPLETE",
        "claim_ceiling": [
            "prospective_design_planning_only",
            "conditional_on_qualified_P0_P1_G_interventions",
            "uses_current_production_surface_secondary_and_W0_W5_classifiers",
            "does_not_choose_generating_effects_from_confirmatory_data",
            "complete_block_assumption_must_match_field_design_before_using_n",
            "Monte_Carlo_power_is_conditional_on_frozen_generating_scenario",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Power the biology-first P. rex full-surface W1/W2 headline using "
            "the current production surface, secondary and W0-W5 classifiers"
        )
    )
    parser.add_argument("config_json", type=Path)
    parser.add_argument("--worlds", type=Path, default=DEFAULT_WORLDS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    config = json.loads(args.config_json.read_text(encoding="utf-8"))
    result = simulate_power(
        config,
        world_rows=_read_worlds(args.worlds),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

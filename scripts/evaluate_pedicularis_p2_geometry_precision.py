from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts import analyze_pedicularis_full_surface as surface
from scripts import analyze_sch_compromise_surface as core
from scripts import summarize_pedicularis_p2_geometry_pilot as geom
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.build_pedicularis_p2_geometry_pilot import _validate_config as validate_pilot_config


SCHEMA = "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_V1"
READY_STATUS = "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_READY_FOR_BASIS"
INSUFFICIENT_STATUS = "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_INSUFFICIENT_FOR_BASIS"
POINT_READY_STATUS = (
    "PEDICULARIS_P2_GEOMETRY_PILOT_POINT_ESTIMATES_READY_NOT_YET_PRECISION_QUALIFIED"
)
STATE_KEYS = ("P0G0", "P1G0", "P0G1", "P1G1")


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _read_rows(path: Path) -> list[dict[str, str]]:
    return geom._read_csv(path)


def _number(value: object, label: str) -> float:
    if value in (None, "", "REQUIRED_BEFORE_USE"):
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
    if not 0 < out <= 1:
        raise ValueError(f"{label} must lie in (0,1]")
    return out


def _sample_sd(values: list[float]) -> float:
    if len(values) < 2:
        raise ValueError("sample SD requires >=2 values")
    center = mean(values)
    variance = sum((value - center) ** 2 for value in values) / (len(values) - 1)
    return math.sqrt(max(0.0, variance))


def _quantile(values: list[float], q: float) -> float:
    return core._quantile(values, q)


def _ci(values: list[float]) -> list[float]:
    return [_quantile(values, 0.025), _quantile(values, 0.975)]


def _width(values: list[float]) -> float:
    interval = _ci(values)
    return interval[1] - interval[0]


def _cluster_bootstrap(
    rows: list[dict[str, str]],
    rng: random.Random,
) -> list[dict[str, str]]:
    by_plant: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_plant[row["plant_id"]].append(row)
    ids = sorted(by_plant)
    if len(ids) < 2:
        raise ValueError("geometry precision bootstrap requires >=2 plants")

    sampled: list[dict[str, str]] = []
    for draw_index, plant_id in enumerate(rng.choices(ids, k=len(ids))):
        for row_index, row in enumerate(by_plant[plant_id]):
            clone = dict(row)
            clone["plant_id"] = f"BOOT{draw_index:04d}_{plant_id}"
            clone["flower_id"] = (
                f"BOOT{draw_index:04d}_{plant_id}_{row_index:03d}_{row['flower_id']}"
            )
            sampled.append(clone)
    return sampled


def _estimate(rows: list[dict[str, str]], min_levels: int) -> dict:
    sch_rows = surface.to_sch_rows(rows)
    fits = core._fit_states(sch_rows, min_levels=min_levels)
    surface_specs, surfaces_usable = geom._surface_specs(fits)

    pollen_models = geom._linear_models(rows, "pollen")
    seed_raw = geom._linear_models(rows, "initial_seed")
    seed_models = {
        state: {
            "intercept_fraction": model["intercept"],
            "z_slope_fraction": model["z_slope"],
        }
        for state, model in seed_raw.items()
    }

    if not surfaces_usable:
        return {
            "surface_specs": surface_specs,
            "all_surfaces_usable": False,
        }

    fitness_variance = geom._variance_components(
        rows,
        lambda row: (
            float(row["undamaged_seed_count"])
            - geom._predict_quadratic(
                surface_specs[geom._state_id(row)],
                float(row["realized_exsertion"]),
            )
        ),
    )
    pollen_variance = geom._variance_components(
        rows,
        lambda row: (
            float(row["pollen_grains"])
            - geom._predict_linear(
                pollen_models[geom._state_id(row)],
                float(row["realized_exsertion"]),
            )
        ),
    )
    seed_variance = geom._variance_components(
        rows,
        lambda row: (
            geom._initial_seed_fraction(row)
            - geom._predict_linear(
                seed_raw[geom._state_id(row)],
                float(row["realized_exsertion"]),
            )
        ),
    )

    values: dict[str, object] = {
        "generating_model.fitness_between_plant_sd": fitness_variance[
            "between_plant_sd"
        ],
        "generating_model.fitness_residual_sd": fitness_variance["residual_sd"],
        "generating_model.pollen_between_plant_sd": pollen_variance[
            "between_plant_sd"
        ],
        "generating_model.pollen_residual_sd": pollen_variance["residual_sd"],
        "generating_model.initial_seed_between_plant_sd_fraction": seed_variance[
            "between_plant_sd"
        ],
        "generating_model.initial_seed_residual_sd_fraction": seed_variance[
            "residual_sd"
        ],
    }
    for state in STATE_KEYS:
        values[f"generating_model.state_fitness_surfaces.{state}"] = {
            "peak": surface_specs[state]["peak"],
            "optimum": surface_specs[state]["optimum"],
            "curvature": surface_specs[state]["curvature"],
        }
        values[f"generating_model.pollen_state_models.{state}"] = pollen_models[
            state
        ]
        values[
            f"generating_model.initial_seed_state_models.{state}"
        ] = seed_models[state]

    return {
        "surface_specs": surface_specs,
        "all_surfaces_usable": True,
        "resolved_power_basis_values": values,
    }


def _validate_precision_gate(config: dict) -> dict:
    validate_pilot_config(config)
    gate = config.get("precision_gate")
    if not isinstance(gate, dict):
        raise ValueError("geometry-pilot precision_gate is required")

    reps = int(_number(gate.get("bootstrap_reps"), "precision_gate.bootstrap_reps"))
    if reps < 200:
        raise ValueError("precision_gate.bootstrap_reps must be >=200")

    return {
        "bootstrap_reps": reps,
        "random_seed": int(gate.get("random_seed", 20261006)),
        "min_valid_bootstrap_fraction": _probability(
            gate.get("min_valid_bootstrap_fraction"),
            "precision_gate.min_valid_bootstrap_fraction",
        ),
        "min_interior_concave_fraction_per_state": _probability(
            gate.get("min_interior_concave_fraction_per_state"),
            "precision_gate.min_interior_concave_fraction_per_state",
        ),
        "max_normalized_95ci_width_per_power_basis_path": _number(
            gate.get("max_normalized_95ci_width_per_power_basis_path"),
            "precision_gate.max_normalized_95ci_width_per_power_basis_path",
        ),
    }


def _bind_inputs(
    rows: list[dict[str, str]],
    summary: dict,
    config: dict,
) -> None:
    if summary.get("receipt_schema") != "PEDICULARIS_P2_GEOMETRY_PILOT_SUMMARY_V1":
        raise ValueError("geometry summary schema mismatch")
    if summary.get("status") != POINT_READY_STATUS:
        raise ValueError("geometry point estimates are not ready for precision evaluation")
    if summary.get("geometry_and_variance_point_estimates_complete") is not True:
        raise ValueError("geometry summary lacks complete point estimates")
    if summary.get("precision_qualification_required") is not True:
        raise ValueError("geometry summary does not require precision qualification")

    if summary.get("pilot_data_sha256") != surface.surface_data_sha256(rows):
        raise ValueError("geometry precision rows do not match summary data fingerprint")

    pilot = validate_pilot_config(config)
    if summary.get("population_id") != pilot["population_id"]:
        raise ValueError("geometry config and summary population_id do not match")
    if summary.get("season_id") != pilot["season_id"]:
        raise ValueError("geometry config and summary season_id do not match")
    if int(summary.get("n_plants", -1)) != pilot["planned_n_plants"]:
        raise ValueError("geometry config and summary plant count do not match")
    if int(summary.get("n_z_levels", -1)) != len(pilot["z_levels"]):
        raise ValueError("geometry config and summary z-level count do not match")


def _normalization_scales(rows: list[dict[str, str]]) -> dict[str, float]:
    z = [float(row["realized_exsertion"]) for row in rows]
    z_span = max(z) - min(z)
    if z_span <= 0:
        raise ValueError("geometry precision requires positive realized-z span")

    fitness = [float(row["undamaged_seed_count"]) for row in rows]
    pollen = [float(row["pollen_grains"]) for row in rows]
    initial = [geom._initial_seed_fraction(row) for row in rows]
    ovules = [float(row["ovule_count"]) for row in rows]

    scales = {
        "z_span": z_span,
        "z_center": mean(z),
        "ovule_mean": mean(ovules),
        "fitness_sd": _sample_sd(fitness),
        "pollen_sd": _sample_sd(pollen),
        "initial_seed_sd": _sample_sd(initial),
    }
    for key in ("ovule_mean", "fitness_sd", "pollen_sd", "initial_seed_sd"):
        if scales[key] <= 0:
            raise ValueError(f"geometry precision normalization scale {key} must be >0")
    return scales


def _collect_path_widths(
    bootstrap_values: list[dict[str, object]],
    scales: dict[str, float],
) -> tuple[dict[str, float], dict[str, dict]]:
    widths: dict[str, float] = {}
    details: dict[str, dict] = {}

    scalar_scale = {
        "generating_model.fitness_between_plant_sd": scales["fitness_sd"],
        "generating_model.fitness_residual_sd": scales["fitness_sd"],
        "generating_model.pollen_between_plant_sd": scales["pollen_sd"],
        "generating_model.pollen_residual_sd": scales["pollen_sd"],
        "generating_model.initial_seed_between_plant_sd_fraction": scales[
            "initial_seed_sd"
        ],
        "generating_model.initial_seed_residual_sd_fraction": scales[
            "initial_seed_sd"
        ],
    }
    for path, denominator in scalar_scale.items():
        values = [float(item[path]) for item in bootstrap_values]
        interval = _ci(values)
        normalized = (interval[1] - interval[0]) / denominator
        widths[path] = normalized
        details[path] = {
            "components": {
                "sd": {
                    "ci95": interval,
                    "normalization": denominator,
                    "normalized_width": normalized,
                }
            },
            "path_normalized_width": normalized,
        }

    for state in STATE_KEYS:
        path = f"generating_model.state_fitness_surfaces.{state}"
        peaks = [float(item[path]["peak"]) for item in bootstrap_values]  # type: ignore[index]
        optima = [float(item[path]["optimum"]) for item in bootstrap_values]  # type: ignore[index]
        curvatures = [float(item[path]["curvature"]) for item in bootstrap_values]  # type: ignore[index]

        peak_ci = _ci(peaks)
        optimum_ci = _ci(optima)
        curvature_ci = _ci(curvatures)
        components = {
            "peak": {
                "ci95": peak_ci,
                "normalized_width": (
                    peak_ci[1] - peak_ci[0]
                ) / scales["ovule_mean"],
            },
            "optimum": {
                "ci95": optimum_ci,
                "normalized_width": (
                    optimum_ci[1] - optimum_ci[0]
                ) / scales["z_span"],
            },
            "curvature": {
                "ci95": curvature_ci,
                "normalized_width": (
                    (curvature_ci[1] - curvature_ci[0])
                    * scales["z_span"] ** 2
                    / scales["ovule_mean"]
                ),
            },
        }
        path_width = max(
            component["normalized_width"]
            for component in components.values()
        )
        widths[path] = path_width
        details[path] = {
            "components": components,
            "path_normalized_width": path_width,
        }

    for state in STATE_KEYS:
        path = f"generating_model.pollen_state_models.{state}"
        centers = []
        effects = []
        for item in bootstrap_values:
            model = item[path]  # type: ignore[index]
            intercept = float(model["intercept"])
            slope = float(model["z_slope"])
            centers.append(intercept + slope * scales["z_center"])
            effects.append(slope * scales["z_span"])
        center_ci = _ci(centers)
        effect_ci = _ci(effects)
        components = {
            "predicted_mean_at_z_center": {
                "ci95": center_ci,
                "normalized_width": (
                    center_ci[1] - center_ci[0]
                ) / scales["pollen_sd"],
            },
            "predicted_change_across_z_span": {
                "ci95": effect_ci,
                "normalized_width": (
                    effect_ci[1] - effect_ci[0]
                ) / scales["pollen_sd"],
            },
        }
        path_width = max(
            component["normalized_width"]
            for component in components.values()
        )
        widths[path] = path_width
        details[path] = {
            "components": components,
            "path_normalized_width": path_width,
        }

    for state in STATE_KEYS:
        path = f"generating_model.initial_seed_state_models.{state}"
        centers = []
        effects = []
        for item in bootstrap_values:
            model = item[path]  # type: ignore[index]
            intercept = float(model["intercept_fraction"])
            slope = float(model["z_slope_fraction"])
            centers.append(intercept + slope * scales["z_center"])
            effects.append(slope * scales["z_span"])
        center_ci = _ci(centers)
        effect_ci = _ci(effects)
        components = {
            "predicted_mean_at_z_center": {
                "ci95": center_ci,
                "normalized_width": (
                    center_ci[1] - center_ci[0]
                ) / scales["initial_seed_sd"],
            },
            "predicted_change_across_z_span": {
                "ci95": effect_ci,
                "normalized_width": (
                    effect_ci[1] - effect_ci[0]
                ) / scales["initial_seed_sd"],
            },
        }
        path_width = max(
            component["normalized_width"]
            for component in components.values()
        )
        widths[path] = path_width
        details[path] = {
            "components": components,
            "path_normalized_width": path_width,
        }

    if len(widths) != 18:
        raise ValueError(f"precision audit expected 18 power-basis paths, got {len(widths)}")
    return widths, details


def build(
    rows: list[dict[str, str]],
    summary: dict,
    config: dict,
) -> dict:
    _bind_inputs(rows, summary, config)
    gate = _validate_precision_gate(config)
    scales = _normalization_scales(rows)
    min_levels = int(summary["n_z_levels"])

    rng = random.Random(gate["random_seed"])
    state_interior_counts = {state: 0 for state in STATE_KEYS}
    valid_values: list[dict[str, object]] = []

    for _ in range(gate["bootstrap_reps"]):
        sampled = _cluster_bootstrap(rows, rng)
        try:
            estimate = _estimate(sampled, min_levels=min_levels)
        except (ValueError, ZeroDivisionError):
            continue

        for state in STATE_KEYS:
            if estimate["surface_specs"][state][
                "usable_for_registered_power_basis"
            ]:
                state_interior_counts[state] += 1

        if not estimate["all_surfaces_usable"]:
            continue
        valid_values.append(estimate["resolved_power_basis_values"])

    valid_fraction = len(valid_values) / gate["bootstrap_reps"]
    interior_fractions = {
        state: state_interior_counts[state] / gate["bootstrap_reps"]
        for state in STATE_KEYS
    }

    enough_valid = (
        valid_fraction >= gate["min_valid_bootstrap_fraction"]
        and len(valid_values) >= 50
    )

    if enough_valid:
        widths, details = _collect_path_widths(valid_values, scales)
    else:
        widths = {}
        details = {}

    all_states_stable = all(
        value >= gate["min_interior_concave_fraction_per_state"]
        for value in interior_fractions.values()
    )
    all_paths_precise = (
        enough_valid
        and len(widths) == 18
        and all(
            value <= gate["max_normalized_95ci_width_per_power_basis_path"]
            for value in widths.values()
        )
    )
    ready = enough_valid and all_states_stable and all_paths_precise

    failing_paths = sorted(
        path
        for path, value in widths.items()
        if value > gate["max_normalized_95ci_width_per_power_basis_path"]
    )
    unstable_states = sorted(
        state
        for state, value in interior_fractions.items()
        if value < gate["min_interior_concave_fraction_per_state"]
    )

    return {
        "analysis": "pedicularis_p2_geometry_pilot_precision_v1",
        "receipt_schema": SCHEMA,
        "population_id": summary["population_id"],
        "season_id": summary["season_id"],
        "geometry_summary_sha256": _semantic_sha256(summary),
        "pilot_data_sha256": summary["pilot_data_sha256"],
        "n_plants": summary["n_plants"],
        "n_rows": summary["n_rows"],
        "normalization_scales": scales,
        "precision_gate": gate,
        "bootstrap_requested_reps": gate["bootstrap_reps"],
        "bootstrap_valid_all_18_path_reps": len(valid_values),
        "bootstrap_valid_all_18_path_fraction": valid_fraction,
        "surface_interior_concave_fraction_by_state": interior_fractions,
        "normalized_95ci_width_by_power_basis_path": widths,
        "precision_detail_by_power_basis_path": details,
        "n_power_basis_paths_precision_evaluated": len(widths),
        "failing_precision_paths": failing_paths,
        "unstable_surface_states": unstable_states,
        "valid_bootstrap_gate_passed": enough_valid,
        "surface_stability_gate_passed": all_states_stable,
        "all_18_path_precision_gate_passed": all_paths_precise,
        "basis_materialization_authorized": ready,
        "status": READY_STATUS if ready else INSUFFICIENT_STATUS,
        "claim_ceiling": [
            "plant_cluster_bootstrap_precision_audit_only",
            "precision_thresholds_must_be_frozen_before_geometry_outcomes",
            "normalized_widths_are_scale_free_planning_diagnostics",
            "does_not_assign_W0_W5",
            "does_not_use_geometry_pilot_rows_in_confirmatory_P2_inference",
            "does_not_resolve_remaining_P0_or_primary_threshold_basis_rows",
            "point_estimability_alone_cannot_authorize_basis_materialization",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Qualify whether the independent P. rex geometry pilot estimates "
            "the 18 W1/W2 power-basis paths precisely enough for materialization"
        )
    )
    parser.add_argument("completed_geometry_pilot_csv", type=Path)
    parser.add_argument("geometry_summary_json", type=Path)
    parser.add_argument("geometry_pilot_config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        _read_rows(args.completed_geometry_pilot_csv),
        _load(args.geometry_summary_json),
        _load(args.geometry_pilot_config_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

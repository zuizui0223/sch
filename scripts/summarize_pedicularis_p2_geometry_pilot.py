from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean

from scripts import analyze_pedicularis_full_surface as surface
from scripts import analyze_sch_compromise_surface as core
from scripts import validate_pedicularis_cohort_registry as cohort
from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.build_pedicularis_p2_geometry_pilot import (
    PROVENANCE_FIELDS,
    RECEIPT_SCHEMA,
)


PILOT_ROLE = "POWER_BASIS_ONLY_NEVER_CONFIRMATORY"
COHORT_ROLE = "POWER_GEOMETRY_PILOT"
READY_STATUS = "PEDICULARIS_P2_GEOMETRY_PILOT_POINT_ESTIMATES_READY_NOT_YET_PRECISION_QUALIFIED"
INCOMPLETE_STATUS = "PEDICULARIS_P2_GEOMETRY_PILOT_POINT_ESTIMATES_INCOMPLETE"
STATE_KEYS = ("P0G0", "P1G0", "P0G1", "P1G1")
FROZEN_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "assigned_z_level",
    "manipulation_setting_id",
    "pollination_treatment",
    "predator_treatment",
    "exclusion_method",
    *PROVENANCE_FIELDS,
)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError(f"{path} has no data rows")
    return rows


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _state_id(row: dict[str, str]) -> str:
    p = 1 if row["pollination_treatment"] == "NATURAL" else 0
    g = 1 if row["predator_treatment"] == "EXPOSED" else 0
    return f"P{p}G{g}"


def _initial_seed_fraction(row: dict[str, str]) -> float:
    ovules = float(row["ovule_count"])
    if ovules <= 0:
        raise ValueError("ovule_count must be >0 in geometry pilot")
    initial = float(row["undamaged_seed_count"]) + float(
        row["damaged_seed_count"]
    )
    return initial / ovules


def _fit_linear(points: list[tuple[float, float]]) -> dict[str, float]:
    if len(points) < 3:
        raise ValueError("state linear model requires >=3 rows")
    xbar = mean(x for x, _ in points)
    ybar = mean(y for _, y in points)
    denom = sum((x - xbar) ** 2 for x, _ in points)
    if denom <= 0:
        raise ValueError("state linear model requires realized-z variation")
    slope = sum((x - xbar) * (y - ybar) for x, y in points) / denom
    intercept = ybar - slope * xbar
    return {"intercept": intercept, "z_slope": slope}


def _linear_models(
    rows: list[dict[str, str]],
    metric: str,
) -> dict[str, dict[str, float]]:
    by_state: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for row in rows:
        z = float(row["realized_exsertion"])
        if metric == "pollen":
            y = float(row["pollen_grains"])
        elif metric == "initial_seed":
            y = _initial_seed_fraction(row)
        else:
            raise ValueError(f"unknown metric {metric}")
        by_state[_state_id(row)].append((z, y))

    if set(by_state) != set(STATE_KEYS):
        raise ValueError(f"{metric} models require all four P/G states")

    return {
        state: _fit_linear(by_state[state])
        for state in STATE_KEYS
    }


def _surface_specs(
    fits: dict[str, dict],
) -> tuple[dict[str, dict], bool]:
    specs = {}
    all_usable = True
    for state in STATE_KEYS:
        fit = fits[state]
        vertex = fit["quadratic_vertex"]
        c = float(fit["c"])
        usable = (
            vertex is not None
            and c < 0
            and fit["optimum_class"] == "INTERIOR_CONCAVE"
        )
        if usable:
            optimum = float(vertex)
            curvature = -c
            peak = (
                float(fit["a"])
                + float(fit["b"]) * optimum
                + c * optimum * optimum
            )
        else:
            optimum = None
            curvature = None
            peak = None
            all_usable = False

        specs[state] = {
            "usable_for_registered_power_basis": usable,
            "peak": peak,
            "optimum": optimum,
            "curvature": curvature,
            "quadratic_coefficients": {
                "a": float(fit["a"]),
                "b": float(fit["b"]),
                "c": c,
            },
            "z_min": float(fit["z_min"]),
            "z_max": float(fit["z_max"]),
            "optimum_class": fit["optimum_class"],
        }
    return specs, all_usable


def _predict_quadratic(spec: dict, z: float) -> float:
    coeffs = spec["quadratic_coefficients"]
    return (
        float(coeffs["a"])
        + float(coeffs["b"]) * z
        + float(coeffs["c"]) * z * z
    )


def _predict_linear(model: dict[str, float], z: float) -> float:
    return float(model["intercept"]) + float(model["z_slope"]) * z


def _variance_components(
    rows: list[dict[str, str]],
    residual_getter,
) -> dict:
    by_plant: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        by_plant[row["plant_id"]].append(float(residual_getter(row)))

    if len(by_plant) < 2:
        raise ValueError("geometry pilot variance requires >=2 plants")
    sizes = {len(values) for values in by_plant.values()}
    if len(sizes) != 1:
        raise ValueError(
            "geometry pilot variance decomposition requires equal flowers per plant"
        )
    k = next(iter(sizes))
    if k < 2:
        raise ValueError("variance decomposition requires >=2 flowers per plant")

    plant_means = {
        plant: mean(values)
        for plant, values in by_plant.items()
    }
    grand = mean(plant_means.values())
    n = len(by_plant)
    ss_between = k * sum(
        (value - grand) ** 2
        for value in plant_means.values()
    )
    ms_between = ss_between / (n - 1)
    ss_within = sum(
        sum(
            (value - plant_means[plant]) ** 2
            for value in values
        )
        for plant, values in by_plant.items()
    )
    ms_within = ss_within / (n * (k - 1))
    between = max(0.0, (ms_between - ms_within) / k)
    denominator = ms_between + (k - 1) * ms_within
    icc = (
        (ms_between - ms_within) / denominator
        if denominator > 0
        else 0.0
    )
    return {
        "n_plants": n,
        "rows_per_plant": k,
        "between_plant_variance": between,
        "between_plant_sd": math.sqrt(between),
        "residual_variance": ms_within,
        "residual_sd": math.sqrt(max(0.0, ms_within)),
        "residualized_icc": icc,
    }


def _validate_execution(
    rows: list[dict[str, str]],
    allocation_receipt: dict,
    registry_rows: list[dict[str, str]],
) -> dict:
    if allocation_receipt.get("receipt_schema") != RECEIPT_SCHEMA:
        raise ValueError("geometry-pilot allocation receipt schema mismatch")
    if allocation_receipt.get("status") != (
        "P2_GEOMETRY_PILOT_ALLOCATED_NOT_YET_MEASURED"
    ):
        raise ValueError("geometry-pilot allocation receipt is not valid")
    if allocation_receipt.get("pilot_role") != PILOT_ROLE:
        raise ValueError("geometry-pilot allocation role mismatch")
    binding_sha = allocation_receipt.get("intervention_plan_binding_sha256")
    if not isinstance(binding_sha, str) or len(binding_sha) != 64:
        raise ValueError(
            "geometry-pilot allocation lacks preoutcome intervention-plan binding"
        )
    bound_plan = allocation_receipt.get("bound_intervention_plan")
    if not isinstance(bound_plan, dict):
        raise ValueError(
            "geometry-pilot allocation lacks bound intervention-plan provenance"
        )

    cohort_receipt = cohort.validate(registry_rows)
    registry = {row["flower_id"]: row for row in registry_rows}
    flower_ids = {row["flower_id"] for row in rows}
    missing = sorted(flower_ids - set(registry))
    if missing:
        raise ValueError(
            "geometry-pilot flower IDs are missing from cohort registry: "
            + ", ".join(missing)
        )
    wrong = sorted(
        flower_id
        for flower_id in flower_ids
        if registry[flower_id]["cohort_role"] != COHORT_ROLE
    )
    if wrong:
        raise ValueError(
            "geometry-pilot flowers must use POWER_GEOMETRY_PILOT cohort role: "
            + ", ".join(wrong)
        )

    for row in rows:
        if row.get("pilot_role") != PILOT_ROLE:
            raise ValueError("completed geometry-pilot rows lost pilot_role")
        for field in surface.RAW_FIELDS:
            if row.get(field, "").strip() == "":
                raise ValueError(
                    f"geometry-pilot canonical outcome field is blank: {field}"
                )

    expected = allocation_receipt.get("expected_frozen_rows")
    if not isinstance(expected, list):
        raise ValueError("geometry-pilot allocation receipt lacks frozen identity")

    frozen = sorted(
        [
            {field: row[field].strip() for field in FROZEN_FIELDS}
            for row in rows
        ],
        key=lambda row: (row["plant_id"], row["flower_id"]),
    )
    if frozen != expected:
        raise ValueError(
            "completed geometry-pilot rows drifted from randomized allocation"
        )
    if _semantic_sha256(frozen) != allocation_receipt.get(
        "frozen_identity_sha256"
    ):
        raise ValueError("geometry-pilot frozen identity digest mismatch")

    contexts = {
        (row["population_id"], row["season_id"])
        for row in rows
    }
    if contexts != {
        (
            allocation_receipt["population_id"],
            allocation_receipt["season_id"],
        )
    }:
        raise ValueError("geometry-pilot context drifted from allocation")

    return cohort_receipt


def build(
    rows: list[dict[str, str]],
    allocation_receipt: dict,
    registry_rows: list[dict[str, str]],
    readiness_receipt: dict,
) -> dict:
    cohort_receipt = _validate_execution(
        rows,
        allocation_receipt,
        registry_rows,
    )

    surface._validate_readiness(
        readiness_receipt,
        allocation_receipt["population_id"],
        allocation_receipt["season_id"],
    )
    bound_plan = allocation_receipt["bound_intervention_plan"]
    validated = readiness_receipt.get("validated_execution")
    if not isinstance(validated, dict):
        raise ValueError("readiness V3 lacks validated execution provenance")

    exact_matches = {
        "z_levels": validated.get("z_levels") == bound_plan.get("z_levels"),
        "z_manipulation_settings": (
            validated.get("z_manipulation_settings")
            == bound_plan.get("z_manipulation_settings")
        ),
        "p1_experimental_unit": (
            validated.get("p_experimental_unit")
            == bound_plan.get("p1_experimental_unit")
        ),
        "g_exclusion_method": (
            validated.get("g_exclusion_method")
            == bound_plan.get("g_exclusion_method")
        ),
        "p0_level_plan_sha256": (
            validated.get("p0_level_plan_sha256")
            == bound_plan.get("p0_level_plan_sha256")
        ),
        "p0_field_config_sha256": (
            validated.get("p0_field_config_sha256")
            == bound_plan.get("p0_field_config_sha256")
        ),
        "p1_field_config_sha256": (
            validated.get("p1_field_config_sha256")
            == bound_plan.get("p1_field_config_sha256")
        ),
        "g_field_config_sha256": (
            validated.get("g_field_config_sha256")
            == bound_plan.get("g_field_config_sha256")
        ),
        "g_method_selection_sha256": (
            validated.get("g_method_selection_sha256")
            == bound_plan.get("g_method_selection_sha256")
        ),
    }
    failed_matches = [
        name for name, passed in exact_matches.items() if not passed
    ]
    if failed_matches:
        raise ValueError(
            "later readiness V3 does not match the preoutcome geometry "
            "intervention plan: " + ", ".join(failed_matches)
        )

    sch_rows = surface.to_sch_rows(rows)
    fits = core._fit_states(
        sch_rows,
        min_levels=len(allocation_receipt["z_levels"]),
    )
    surface_specs, surfaces_usable = _surface_specs(fits)
    pollen_models = _linear_models(rows, "pollen")
    seed_models_raw = _linear_models(rows, "initial_seed")
    seed_models = {
        state: {
            "intercept_fraction": model["intercept"],
            "z_slope_fraction": model["z_slope"],
        }
        for state, model in seed_models_raw.items()
    }

    fitness_variance = _variance_components(
        rows,
        lambda row: (
            float(row["undamaged_seed_count"])
            - _predict_quadratic(
                surface_specs[_state_id(row)],
                float(row["realized_exsertion"]),
            )
        ),
    )
    pollen_variance = _variance_components(
        rows,
        lambda row: (
            float(row["pollen_grains"])
            - _predict_linear(
                pollen_models[_state_id(row)],
                float(row["realized_exsertion"]),
            )
        ),
    )
    initial_seed_variance = _variance_components(
        rows,
        lambda row: (
            _initial_seed_fraction(row)
            - _predict_linear(
                seed_models_raw[_state_id(row)],
                float(row["realized_exsertion"]),
            )
        ),
    )

    target_by_level = {
        row["assigned_z_level"]: float(row["target_exsertion"])
        for row in rows
    }
    z_errors = [
        float(row["realized_exsertion"])
        - target_by_level[row["assigned_z_level"]]
        for row in rows
    ]
    z_error_mean = mean(z_errors)
    realized_z_error_sd = math.sqrt(
        sum((value - z_error_mean) ** 2 for value in z_errors)
        / (len(z_errors) - 1)
    ) if len(z_errors) > 1 else 0.0

    ovules = [float(row["ovule_count"]) for row in rows]
    resolved_paths = {
        "generating_model.fitness_between_plant_sd": fitness_variance[
            "between_plant_sd"
        ],
        "generating_model.fitness_residual_sd": fitness_variance["residual_sd"],
        "generating_model.pollen_between_plant_sd": pollen_variance[
            "between_plant_sd"
        ],
        "generating_model.pollen_residual_sd": pollen_variance["residual_sd"],
        "generating_model.initial_seed_between_plant_sd_fraction": (
            initial_seed_variance["between_plant_sd"]
        ),
        "generating_model.initial_seed_residual_sd_fraction": (
            initial_seed_variance["residual_sd"]
        ),
    }
    for state in STATE_KEYS:
        resolved_paths[
            f"generating_model.state_fitness_surfaces.{state}"
        ] = {
            "peak": surface_specs[state]["peak"],
            "optimum": surface_specs[state]["optimum"],
            "curvature": surface_specs[state]["curvature"],
        }
        resolved_paths[
            f"generating_model.pollen_state_models.{state}"
        ] = pollen_models[state]
        resolved_paths[
            f"generating_model.initial_seed_state_models.{state}"
        ] = seed_models[state]

    n_resolved = len(resolved_paths) if surfaces_usable else (
        len(resolved_paths) - 4
    )

    return {
        "analysis": "pedicularis_p2_geometry_pilot_summary_v1",
        "receipt_schema": "PEDICULARIS_P2_GEOMETRY_PILOT_SUMMARY_V1",
        "population_id": allocation_receipt["population_id"],
        "season_id": allocation_receipt["season_id"],
        "pilot_role": PILOT_ROLE,
        "cohort_registry_status": cohort_receipt["status"],
        "cohort_independence_status": cohort_receipt["independence_status"],
        "n_rows": len(rows),
        "n_plants": len({row["plant_id"] for row in rows}),
        "candidate_cumulative_plants": allocation_receipt.get(
            "candidate_cumulative_plants"
        ),
        "current_precision_look_n": int(
            allocation_receipt.get(
                "current_precision_look_n",
                allocation_receipt["n_plants"],
            )
        ),
        "allocation_scope": allocation_receipt.get(
            "allocation_scope",
            "MAXIMUM_PILOT_ALLOCATION",
        ),
        "parent_allocation_sha256": allocation_receipt.get(
            "parent_allocation_sha256"
        ),
        "n_z_levels": len({row["assigned_z_level"] for row in rows}),
        "n_surface_cells": allocation_receipt["n_surface_cells"],
        "replicates_per_cell": allocation_receipt["replicates_per_cell"],
        "pilot_data_sha256": surface.surface_data_sha256(rows),
        "allocation_frozen_identity_sha256": allocation_receipt.get(
            "frozen_identity_sha256"
        ),
        "pilot_config_sha256": allocation_receipt.get("config_sha256"),
        "intervention_plan_binding_sha256": allocation_receipt.get(
            "intervention_plan_binding_sha256"
        ),
        "readiness_receipt_sha256": _semantic_sha256(readiness_receipt),
        "readiness_intervention_plan_match": exact_matches,
        "validated_execution": validated,
        "precision_gate_frozen_at_allocation": allocation_receipt.get(
            "precision_gate"
        ),
        "surface_specs": surface_specs,
        "all_four_fitness_surfaces_usable_for_power_basis": surfaces_usable,
        "pollen_state_models": pollen_models,
        "initial_seed_state_models": seed_models,
        "fitness_variance_components": fitness_variance,
        "pollen_variance_components": pollen_variance,
        "initial_seed_variance_components": initial_seed_variance,
        "pilot_realized_z_error_sd": realized_z_error_sd,
        "pilot_ovule_count_mean": mean(ovules),
        "resolved_power_basis_values": resolved_paths,
        "n_power_basis_paths_resolved": n_resolved,
        "expected_geometry_and_variance_paths": 18,
        "geometry_and_variance_point_estimates_complete": (
            surfaces_usable and n_resolved == 18
        ),
        "geometry_and_variance_basis_complete": False,
        "precision_qualification_required": True,
        "status": (
            READY_STATUS
            if surfaces_usable and n_resolved == 18
            else INCOMPLETE_STATUS
        ),
        "claim_ceiling": [
            "nonconfirmatory_power_basis_only",
            "geometry_collection_may_precede_lane_validation_but_basis_use_cannot",
            "geometry_basis_conditioned_on_later_positive_randomized_P0_P1_G_readiness",
            "later_readiness_must_match_exact_preoutcome_intervention_plan",
            "pilot_rows_never_enter_confirmatory_P2_inference",
            "does_not_assign_W0_W5",
            "does_not_test_causal_compromise",
            "pilot_realized_z_error_is_descriptive_not_a_replacement_for_registered_P0_basis",
            "pilot_ovule_mean_is_descriptive_context",
            "point_estimability_does_not_imply_precision_sufficiency",
            "precision_qualification_required_before_basis_materialization",
            "registered_power_still_requires_remaining_P0_and_threshold_basis_rows",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Summarize a separate randomized P. rex mini-surface into the "
            "same-context geometry and variance quantities needed for W1/W2 power"
        )
    )
    parser.add_argument("completed_geometry_pilot_csv", type=Path)
    parser.add_argument("allocation_receipt_json", type=Path)
    parser.add_argument("cohort_registry_csv", type=Path)
    parser.add_argument("readiness_v3_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = _read_csv(args.completed_geometry_pilot_csv)
    result = build(
        rows,
        _load_json(args.allocation_receipt_json),
        cohort._read(args.cohort_registry_csv),
        _load_json(args.readiness_v3_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

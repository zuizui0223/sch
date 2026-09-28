from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from statistics import NormalDist


PLACEHOLDER = "REQUIRED_BEFORE_USE"
NOT_APPLICABLE = "NOT_APPLICABLE"
PLANNING_STATUS = "PEDICULARIS_CAL_C_INPUTS_PROSPECTIVELY_FROZEN"
MAX_N = 10000

EXPECTED_GATE_PATHS = {
    "P0": {
        "stage_p0.min_adjacent_exsertion_gap",
        "stage_p0.max_opening_width_relative_change",
        "stage_p0.max_tube_diameter_relative_change",
        "stage_p0.max_bract_height_relative_change",
        "stage_p0.max_lower_lip_angle_change_deg",
        "stage_p0.max_water_depth_change",
        "stage_p0.max_flower_orientation_change_deg",
        "stage_p0.max_mechanical_damage_rate",
    },
    "P1": {
        "pollination_weight.min_pollen_grain_delta",
        "pollination_weight.min_initial_seed_set_delta",
        "pollination_weight.max_early_predator_attack_difference",
        "pollination_weight.max_z_relative_change",
        "pollination_weight.max_bract_height_relative_change",
        "pollination_weight.max_opening_width_relative_change",
        "pollination_weight.max_water_depth_change",
        "pollination_weight.max_mechanical_damage_rate",
    },
    "G": {
        "predator_weight.min_early_attack_reduction",
        "predator_weight.min_predation_fraction_reduction",
        "predator_weight.min_final_seed_set_gain",
        "predator_weight.max_initial_seed_set_difference",
        "predator_weight.max_pollen_grain_relative_change",
        "predator_weight.max_pollinator_visit_relative_change",
        "predator_weight.max_z_relative_change",
        "predator_weight.max_water_depth_change",
        "predator_weight.max_damage_rate_difference",
    },
}


def _number(value: object, label: str) -> float:
    if value == PLACEHOLDER or value in (None, ""):
        raise ValueError(f"{label} is not prospectively specified")
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{label} must be finite")
    return out


def _positive_int(value: object, label: str) -> int:
    numeric = _number(value, label)
    if numeric < 1 or not float(numeric).is_integer():
        raise ValueError(f"{label} must be a positive integer")
    return int(numeric)


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _read_criteria(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("CAL-C criteria table is empty")
    return rows


def _validate_planning_config(config: dict) -> dict:
    confidence = _number(config.get("confidence_level"), "confidence_level")
    if not math.isclose(confidence, 0.95, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(
            "CAL-C confidence_level must be 0.95 to match the registered "
            "confirmatory 95% interval gates"
        )

    familywise_power = _number(
        config.get("familywise_target_power"),
        "familywise_target_power",
    )
    if not 0.0 < familywise_power < 1.0:
        raise ValueError("familywise_target_power must lie in (0, 1)")
    familywise_basis = config.get("familywise_target_power_basis")
    if (
        not isinstance(familywise_basis, str)
        or not familywise_basis.strip()
        or familywise_basis == PLACEHOLDER
    ):
        raise ValueError("familywise_target_power_basis is not prospectively specified")

    provenance = config.get("planning_provenance")
    if not isinstance(provenance, dict):
        raise ValueError("planning_provenance is required")
    if provenance.get("status") != PLANNING_STATUS:
        raise ValueError("CAL-C planning inputs are not prospectively frozen")
    for field in ("population_id", "season_id", "basis_document"):
        value = provenance.get(field)
        if (
            not isinstance(value, str)
            or not value.strip()
            or value == PLACEHOLDER
        ):
            raise ValueError(f"planning_provenance.{field} is not frozen")
    if provenance.get("frozen_before_confirmatory_data") is not True:
        raise ValueError(
            "CAL-C planning assumptions must be frozen before confirmatory data"
        )

    lane_design = config.get("lane_design")
    if not isinstance(lane_design, dict):
        raise ValueError("lane_design is required")

    normalized_design = {}
    for lane in ("P0", "P1", "G"):
        design = lane_design.get(lane)
        if not isinstance(design, dict):
            raise ValueError(f"lane_design.{lane} is required")
        design_effect = _number(
            design.get("design_effect"),
            f"lane_design.{lane}.design_effect",
        )
        if design_effect < 1.0:
            raise ValueError(
                f"lane_design.{lane}.design_effect must be >= 1"
            )
        flowers = _positive_int(
            design.get("flowers_per_plant_per_cell"),
            f"lane_design.{lane}.flowers_per_plant_per_cell",
        )
        design_effect_basis = design.get("design_effect_basis")
        flowers_basis = design.get("flowers_per_plant_per_cell_basis")
        if (
            not isinstance(design_effect_basis, str)
            or not design_effect_basis.strip()
            or design_effect_basis == PLACEHOLDER
        ):
            raise ValueError(
                f"lane_design.{lane}.design_effect_basis is not prospectively specified"
            )
        if (
            not isinstance(flowers_basis, str)
            or not flowers_basis.strip()
            or flowers_basis == PLACEHOLDER
        ):
            raise ValueError(
                f"lane_design.{lane}.flowers_per_plant_per_cell_basis is not prospectively specified"
            )
        normalized_design[lane] = {
            "design_effect": design_effect,
            "design_effect_basis": design_effect_basis,
            "flowers_per_plant_per_cell": flowers,
            "flowers_per_plant_per_cell_basis": flowers_basis,
        }

    return {
        "confidence_level": confidence,
        "familywise_target_power": familywise_power,
        "familywise_target_power_basis": familywise_basis,
        "planning_provenance": provenance,
        "lane_design": normalized_design,
    }


def _validate_criteria(
    rows: list[dict[str, str]],
    config: dict,
) -> list[dict[str, object]]:
    criterion_ids = [row.get("criterion_id", "") for row in rows]
    if any(not value for value in criterion_ids):
        raise ValueError("criterion_id is required")
    if len(criterion_ids) != len(set(criterion_ids)):
        raise ValueError("criterion_id must be unique")

    expected_total = sum(len(values) for values in EXPECTED_GATE_PATHS.values())
    if len(rows) != expected_total:
        raise ValueError(
            f"expected {expected_total} CAL-C criteria, found {len(rows)}"
        )

    by_lane = Counter(row.get("lane", "") for row in rows)
    for lane, expected in EXPECTED_GATE_PATHS.items():
        actual_paths = {
            row.get("gate_path", "")
            for row in rows
            if row.get("lane") == lane
        }
        if actual_paths != expected:
            raise ValueError(
                f"{lane} CAL-C gate coverage mismatch: "
                f"missing={sorted(expected - actual_paths)}, "
                f"extra={sorted(actual_paths - expected)}"
            )

    provenance = config["planning_provenance"]
    normalized: list[dict[str, object]] = []

    for row in rows:
        lane = row["lane"]
        if lane not in EXPECTED_GATE_PATHS:
            raise ValueError(f"unregistered CAL-C lane: {lane}")

        if row.get("population_id") != provenance["population_id"]:
            raise ValueError(
                f"{row['criterion_id']} population_id does not match planning provenance"
            )
        if row.get("season_id") != provenance["season_id"]:
            raise ValueError(
                f"{row['criterion_id']} season_id does not match planning provenance"
            )

        criterion_type = row.get("criterion_type")
        direction = row.get("direction")
        unit_type = row.get("unit_type")
        if criterion_type not in {"NORMAL_BOUND", "BINOMIAL_UPPER"}:
            raise ValueError(
                f"invalid criterion_type for {row['criterion_id']}: {criterion_type}"
            )
        if direction not in {"LOWER", "UPPER"}:
            raise ValueError(
                f"invalid direction for {row['criterion_id']}: {direction}"
            )
        if unit_type not in {"PLANT", "FLOWER"}:
            raise ValueError(
                f"invalid unit_type for {row['criterion_id']}: {unit_type}"
            )
        if criterion_type == "BINOMIAL_UPPER" and direction != "UPPER":
            raise ValueError("BINOMIAL_UPPER criteria must use UPPER direction")

        boundary = _number(
            row.get("boundary"),
            f"{row['criterion_id']}.boundary",
        )
        assumed_true = _number(
            row.get("assumed_true_value"),
            f"{row['criterion_id']}.assumed_true_value",
        )
        basis_note = row.get("basis_note", "")
        if not basis_note or basis_note == PLACEHOLDER:
            raise ValueError(
                f"{row['criterion_id']}.basis_note is not prospectively specified"
            )

        pilot_sd = None
        pilot_sd_source = row.get("pilot_sd_source", "")
        if criterion_type == "NORMAL_BOUND":
            pilot_sd = _number(
                row.get("pilot_sd"),
                f"{row['criterion_id']}.pilot_sd",
            )
            if pilot_sd <= 0:
                raise ValueError(
                    f"{row['criterion_id']}.pilot_sd must be > 0"
                )
            if (
                not pilot_sd_source
                or pilot_sd_source == PLACEHOLDER
                or pilot_sd_source == NOT_APPLICABLE
            ):
                raise ValueError(
                    f"{row['criterion_id']}.pilot_sd_source is not specified"
                )
        else:
            if row.get("pilot_sd") != NOT_APPLICABLE:
                raise ValueError(
                    f"{row['criterion_id']}.pilot_sd must be {NOT_APPLICABLE}"
                )
            if pilot_sd_source != NOT_APPLICABLE:
                raise ValueError(
                    f"{row['criterion_id']}.pilot_sd_source must be {NOT_APPLICABLE}"
                )

        if direction == "LOWER":
            distance = assumed_true - boundary
        else:
            distance = boundary - assumed_true
        if distance <= 0:
            raise ValueError(
                f"{row['criterion_id']} assumed true value does not lie on the "
                "success side of its boundary"
            )

        if criterion_type == "BINOMIAL_UPPER":
            if not 0.0 < boundary < 1.0:
                raise ValueError(
                    f"{row['criterion_id']} binomial boundary must lie in (0, 1)"
                )
            if not 0.0 <= assumed_true < boundary:
                raise ValueError(
                    f"{row['criterion_id']} binomial assumed true rate must lie "
                    "in [0, boundary)"
                )

        normalized.append(
            {
                **row,
                "boundary": boundary,
                "assumed_true_value": assumed_true,
                "pilot_sd": pilot_sd,
                "pilot_sd_source": pilot_sd_source,
                "distance_to_boundary": distance,
            }
        )

    return normalized


def wilson_interval(
    k: int,
    n: int,
    confidence: float,
) -> tuple[float, float]:
    if not 0 <= k <= n or n <= 0:
        raise ValueError("require 0 <= k <= n and n > 0")
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    p = k / n
    denominator = 1.0 + z * z / n
    center = (p + z * z / (2.0 * n)) / denominator
    half = (
        z
        * math.sqrt(
            p * (1.0 - p) / n
            + z * z / (4.0 * n * n)
        )
        / denominator
    )
    return center - half, center + half


def _binomial_cdf(k_max: int, n: int, p: float) -> float:
    if k_max < 0:
        return 0.0
    if k_max >= n:
        return 1.0
    if p == 0.0:
        return 1.0
    if p == 1.0:
        return 0.0

    pmf = (1.0 - p) ** n
    total = pmf
    ratio = p / (1.0 - p)
    for k in range(0, k_max):
        pmf *= (n - k) / (k + 1) * ratio
        total += pmf
    return min(1.0, max(0.0, total))


def binomial_upper_success_probability(
    n: int,
    *,
    true_p: float,
    boundary: float,
    confidence: float,
) -> float:
    k_max = -1
    for k in range(n + 1):
        _, upper = wilson_interval(k, n, confidence)
        if upper <= boundary:
            k_max = k
        else:
            break
    return _binomial_cdf(k_max, n, true_p)


def minimum_binomial_n(
    *,
    true_p: float,
    boundary: float,
    confidence: float,
    target_power: float,
    max_n: int = MAX_N,
) -> tuple[int, float]:
    for n in range(2, max_n + 1):
        achieved = binomial_upper_success_probability(
            n,
            true_p=true_p,
            boundary=boundary,
            confidence=confidence,
        )
        if achieved >= target_power:
            return n, achieved
    raise RuntimeError(
        "binomial target power not reached before CAL-C max_n"
    )


def normal_boundary_required_n(
    *,
    pilot_sd: float,
    distance_to_boundary: float,
    confidence: float,
    target_power: float,
) -> int:
    if pilot_sd <= 0 or distance_to_boundary <= 0:
        raise ValueError("pilot_sd and distance_to_boundary must be > 0")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    if not 0.0 < target_power < 1.0:
        raise ValueError("target_power must lie in (0, 1)")

    z_conf = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    z_power = NormalDist().inv_cdf(target_power)
    n = math.ceil(
        ((z_conf + z_power) * pilot_sd / distance_to_boundary) ** 2
    )
    return max(2, n)


def _criterion_plan(
    row: dict[str, object],
    *,
    confidence: float,
    target_power: float,
    design_effect: float,
    flowers_per_plant_per_cell: int,
) -> dict[str, object]:
    if row["criterion_type"] == "NORMAL_BOUND":
        raw_units = normal_boundary_required_n(
            pilot_sd=float(row["pilot_sd"]),
            distance_to_boundary=float(row["distance_to_boundary"]),
            confidence=confidence,
            target_power=target_power,
        )
        achieved_probability = None
    else:
        raw_units, achieved_probability = minimum_binomial_n(
            true_p=float(row["assumed_true_value"]),
            boundary=float(row["boundary"]),
            confidence=confidence,
            target_power=target_power,
        )

    inflated_units = max(2, math.ceil(raw_units * design_effect))

    if row["unit_type"] == "PLANT":
        required_plants = inflated_units
    else:
        required_plants = max(
            2,
            math.ceil(inflated_units / flowers_per_plant_per_cell),
        )

    required_flowers_per_cell = (
        required_plants * flowers_per_plant_per_cell
    )

    return {
        "criterion_id": row["criterion_id"],
        "gate_path": row["gate_path"],
        "criterion_type": row["criterion_type"],
        "direction": row["direction"],
        "unit_type": row["unit_type"],
        "metric_source": row["metric_source"],
        "boundary": row["boundary"],
        "assumed_true_value": row["assumed_true_value"],
        "pilot_sd": row["pilot_sd"],
        "pilot_sd_source": row["pilot_sd_source"],
        "distance_to_boundary": row["distance_to_boundary"],
        "per_criterion_target_power": target_power,
        "raw_required_units": raw_units,
        "design_effect": design_effect,
        "inflated_required_units": inflated_units,
        "required_plants": required_plants,
        "required_flowers_per_cell": required_flowers_per_cell,
        "exact_binomial_achieved_probability": achieved_probability,
        "basis_note": row["basis_note"],
    }


def build_plan(
    criteria_rows: list[dict[str, str]],
    planning_config: dict,
) -> dict:
    config = _validate_planning_config(planning_config)
    rows = _validate_criteria(criteria_rows, config)

    lane_results = {}
    all_criterion_rows = []

    for lane in ("P0", "P1", "G"):
        lane_rows = [row for row in rows if row["lane"] == lane]
        k = len(lane_rows)
        familywise = config["familywise_target_power"]
        per_criterion_power = 1.0 - (1.0 - familywise) / k

        design = config["lane_design"][lane]
        planned = [
            _criterion_plan(
                row,
                confidence=config["confidence_level"],
                target_power=per_criterion_power,
                design_effect=design["design_effect"],
                flowers_per_plant_per_cell=design[
                    "flowers_per_plant_per_cell"
                ],
            )
            for row in lane_rows
        ]

        required_plants = max(
            int(row["required_plants"]) for row in planned
        )
        flowers_per_cell = (
            required_plants * design["flowers_per_plant_per_cell"]
        )
        driving = sorted(
            row["criterion_id"]
            for row in planned
            if int(row["required_plants"]) == required_plants
        )

        lane_results[lane] = {
            "n_criteria": k,
            "familywise_target_power": familywise,
            "union_bound_per_criterion_target_power": per_criterion_power,
            "design_effect": design["design_effect"],
            "design_effect_basis": design["design_effect_basis"],
            "flowers_per_plant_per_cell": design[
                "flowers_per_plant_per_cell"
            ],
            "flowers_per_plant_per_cell_basis": design[
                "flowers_per_plant_per_cell_basis"
            ],
            "required_plants": required_plants,
            "required_flowers_per_cell": flowers_per_cell,
            "driving_criteria": driving,
        }
        all_criterion_rows.extend(planned)

    p0 = lane_results["P0"]
    p1 = lane_results["P1"]
    g = lane_results["G"]

    sample_size_gate_values = {
        "stage_p0.min_plants": p0["required_plants"],
        "stage_p0.min_flowers_per_level": p0[
            "required_flowers_per_cell"
        ],
        "pollination_weight.min_plant_units_per_treatment": p1[
            "required_plants"
        ],
        "pollination_weight.min_flowers_per_treatment": p1[
            "required_flowers_per_cell"
        ],
        "method_gate.min_paired_plants": g["required_plants"],
        "method_gate.min_flowers_per_treatment": g[
            "required_flowers_per_cell"
        ],
        "predator_weight.min_paired_plants": g[
            "required_plants"
        ],
        "predator_weight.min_flowers_per_treatment": g[
            "required_flowers_per_cell"
        ],
    }

    return {
        "analysis": "pedicularis_cal_c_sample_size_plan_v1",
        "planning_provenance": config["planning_provenance"],
        "confidence_level": config["confidence_level"],
        "familywise_target_power": config[
            "familywise_target_power"
        ],
        "familywise_target_power_basis": config[
            "familywise_target_power_basis"
        ],
        "familywise_method": (
            "union_bound_failure_allocation_no_independence_assumption"
        ),
        "lane_plans": lane_results,
        "criterion_plans": sorted(
            all_criterion_rows,
            key=lambda row: (str(row["gate_path"]), str(row["criterion_id"])),
        ),
        "sample_size_gate_values": sample_size_gate_values,
        "status": "PEDICULARIS_CAL_C_SAMPLE_SIZE_PLAN_READY",
        "claim_ceiling": [
            "prospective_planning_only",
            "normal_bound_rows_use_normal_approximation_to_registered_95pct_CI_gate",
            "current_registered_criteria_are_plant_level_normal_bound_planning_approximations",
            "optional_BINOMIAL_UPPER_rows_if_registered_use_exact_Wilson_upper_bound_success_probability",
            "design_effect_is_explicit_planning_inflation_not_estimated_by_this_script",
            "familywise_target_uses_union_bound_not_independence_assumption",
            "pilot_sd_and_assumed_true_values_are_planning_inputs_not_guarantees",
            "sample_size_values_require_transfer_into_final_F0_configs_with_provenance",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Plan Pedicularis CAL-C confirmatory sample sizes from prospectively "
            "frozen gate boundaries, assumed true values and pilot variability"
        )
    )
    parser.add_argument("criteria_csv", type=Path)
    parser.add_argument("planning_config_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build_plan(
        _read_criteria(args.criteria_csv),
        _load_json(args.planning_config_json),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

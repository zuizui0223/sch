from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_EXPLORATORY_CANDIDATES_V1.csv"
)

SCHEMA = "SCH_PEDICULARIS_G_HARD_VALIDITY_PILOT_PLAN_V1"
FREEZE_STATUS = "PEDICULARIS_G_HARD_VALIDITY_PILOT_PLAN_PROSPECTIVELY_FROZEN"
PLAN_STATUS = "PEDICULARIS_G_HARD_VALIDITY_PILOT_SAMPLE_SIZE_READY"


def _read_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _read_candidates(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("G candidate matrix has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("G candidate matrix is empty")
    return rows


def _timestamp(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("frozen_at_utc is required")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("frozen_at_utc must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError("frozen_at_utc must be timezone-aware")
    return value


def zero_failure_upper_bound(n: int, confidence_level: float) -> float:
    if n < 1:
        raise ValueError("n must be >= 1")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must lie in (0, 1)")
    alpha = 1.0 - confidence_level
    return 1.0 - alpha ** (1.0 / n)


def minimum_zero_failure_n(
    *,
    max_failure_probability: float,
    confidence_level: float,
) -> int:
    if not 0.0 < max_failure_probability < 1.0:
        raise ValueError("max_failure_probability must lie in (0, 1)")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must lie in (0, 1)")

    alpha = 1.0 - confidence_level
    raw = math.log(alpha) / math.log(1.0 - max_failure_probability)
    n = math.ceil(raw)
    while zero_failure_upper_bound(n, confidence_level) > max_failure_probability:
        n += 1
    while (
        n > 1
        and zero_failure_upper_bound(n - 1, confidence_level)
        <= max_failure_probability
    ):
        n -= 1
    return n


def build(config: dict, candidate_rows: list[dict[str, str]]) -> dict:
    if config.get("schema") != SCHEMA:
        raise ValueError("G hard-validity planning schema mismatch")
    if config.get("status") != FREEZE_STATUS:
        raise ValueError("G hard-validity planning inputs are not prospectively frozen")
    if config.get("frozen_before_exploratory_G_data") is not True:
        raise ValueError("G hard-validity plan must be frozen before exploratory G data")
    frozen_at = _timestamp(config.get("frozen_at_utc"))

    population_id = config.get("population_id")
    season_id = config.get("season_id")
    if not isinstance(population_id, str) or not population_id:
        raise ValueError("population_id is required")
    if not isinstance(season_id, str) or not season_id:
        raise ValueError("season_id is required")

    basis = config.get("planning_basis_note")
    if not isinstance(basis, str) or not basis.strip() or basis == "REQUIRED_BEFORE_USE":
        raise ValueError("planning_basis_note is required")

    try:
        confidence = float(config["confidence_level"])
        max_failure = float(
            config["max_acceptable_per_plant_hard_failure_probability"]
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("confidence/failure planning values must be numeric") from exc

    n = minimum_zero_failure_n(
        max_failure_probability=max_failure,
        confidence_level=confidence,
    )
    achieved = zero_failure_upper_bound(n, confidence)

    candidates = []
    seen_ids = set()
    seen_methods = set()
    for row in candidate_rows:
        candidate_id = row["candidate_id"]
        method = row["field_exclusion_method"]
        if candidate_id in seen_ids or method in seen_methods:
            raise ValueError("candidate IDs and field method codes must be unique")
        seen_ids.add(candidate_id)
        seen_methods.add(method)
        priority = int(row["exploratory_priority"])
        candidates.append(
            {
                "candidate_id": candidate_id,
                "field_exclusion_method": method,
                "exploratory_priority": priority,
                "minimum_paired_plants_for_zero_failure_screen": n,
                "required_exposed_flowers_minimum": n,
                "required_excluded_flowers_minimum": n,
                "zero_failure_one_sided_upper_bound": achieved,
                "advance_condition": (
                    f">={n} paired plants and zero registered hard-validity "
                    "failures; effect/selectivity targets remain separate"
                ),
            }
        )

    first_tier = [
        row for row in candidates
        if row["exploratory_priority"] == 1
    ]
    initial_total = sum(
        row["minimum_paired_plants_for_zero_failure_screen"]
        for row in first_tier
    )
    first_tier_ids = sorted(row["candidate_id"] for row in first_tier)
    current_three_arm_manifest_ids = [
        "G_A1_FINE_MESH",
        "G_A2_POROUS_TUBING",
    ]
    current_three_arm_manifest_compatible = (
        first_tier_ids == current_three_arm_manifest_ids
    )
    current_distinct_plants = (
        n if current_three_arm_manifest_compatible else None
    )
    current_total_flowers = (
        n * 3 if current_three_arm_manifest_compatible else None
    )

    return {
        "analysis": "pedicularis_g_hard_validity_pilot_planner_v1",
        "population_id": population_id,
        "season_id": season_id,
        "confidence_level": confidence,
        "max_acceptable_per_plant_hard_failure_probability": max_failure,
        "planning_basis_note": basis,
        "frozen_at_utc": frozen_at,
        "hard_failure_unit": (
            "paired-plant candidate application fails if any registered "
            "hard-validity condition fails"
        ),
        "zero_failure_rule": (
            "one-sided exact binomial upper bound on the composite per-plant "
            "hard-failure probability: 1 - (1-confidence)^(1/n)"
        ),
        "minimum_paired_plants_per_tested_candidate": n,
        "achieved_zero_failure_upper_bound": achieved,
        "candidate_plans": sorted(
            candidates,
            key=lambda row: (
                row["exploratory_priority"],
                row["candidate_id"],
            ),
        ),
        "first_tier_candidate_ids": first_tier_ids,
        "initial_first_tier_total_paired_plant_assignments": initial_total,
        "current_three_arm_manifest_compatible": (
            current_three_arm_manifest_compatible
        ),
        "minimum_distinct_plants_for_current_three_arm_manifest": (
            current_distinct_plants
        ),
        "minimum_total_flowers_for_current_three_arm_manifest": (
            current_total_flowers
        ),
        "candidate_selected": False,
        "effect_thresholds_selected": False,
        "selectivity_thresholds_selected": False,
        "status": PLAN_STATUS,
        "claim_ceiling": [
            "hard_validity_failure_rate_planning_only",
            "failure_probability_is_composite_any_registered_hard_failure_not_six_separate_error_rates",
            "zero_observed_hard_failures_required_for_this_plan",
            "does_not_establish_predator_exclusion_effectiveness",
            "does_not_establish_selectivity",
            "does_not_rank_first_tier_candidates_by_expected_effect",
            "current_three_arm_manifest_uses_one_shared_sham_plus_both_first_tier_candidates_per_plant",
            "paired_plants_can_host_multiple_candidate_flowers_only_if_assignment_and_interference_are_prospectively_controlled",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Plan focal P. rex exploratory G candidate sample size from a "
            "prospectively frozen maximum hard-validity failure probability"
        )
    )
    parser.add_argument("planning_config", type=Path)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        _read_json(args.planning_config),
        _read_candidates(args.candidates),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

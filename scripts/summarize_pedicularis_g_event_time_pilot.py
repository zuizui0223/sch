from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean, median, stdev


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_EVENT_TIME_PILOT_CONFIG_TEMPLATE_V1.json"
)
DEFAULT_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_EVENT_TIME_PILOT_TEMPLATE_V1.csv"
)

SCHEMA = "SCH_PEDICULARIS_G_EVENT_TIME_PILOT_CONFIG_V1"
FREEZE_STATUS = "PEDICULARIS_G_EVENT_TIME_PILOT_PROSPECTIVELY_FROZEN"
PLACEHOLDER = "REQUIRED_BEFORE_USE"
POLLEN_ROLE = "POLLINATION_SENTINEL"
NATURAL_ROLE = "ATTACK_SWELL_SENTINEL"
ROLES = {POLLEN_ROLE, NATURAL_ROLE}

REQUIRED_FIELDS = (
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "flower_role",
    "anthesis_time_hours",
    "observation_time_hours",
    "pollen_grains",
    "pollination_complete",
    "attack_present",
    "ovary_swollen",
)


def _read_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("event-time config must be a JSON object")
    return payload


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("event-time pilot table has no header")
        missing = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing:
            raise ValueError(
                "event-time pilot table lacks columns: " + ", ".join(missing)
            )
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("event-time pilot table is empty")
    return rows


def _number(value: str, label: str) -> float:
    try:
        out = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{label} must be finite")
    return out


def _binary(value: str, label: str) -> int:
    if value not in {"0", "1"}:
        raise ValueError(f"{label} must be 0 or 1")
    return int(value)


def _summary(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        raise ValueError("cannot summarize an empty value set")
    ordered = sorted(values)

    def quantile(q: float) -> float:
        pos = (len(ordered) - 1) * q
        lo = math.floor(pos)
        hi = math.ceil(pos)
        if lo == hi:
            return ordered[lo]
        w = pos - lo
        return ordered[lo] * (1 - w) + ordered[hi] * w

    return {
        "n": len(values),
        "mean": mean(values),
        "sd": stdev(values) if len(values) >= 2 else None,
        "min": min(values),
        "q05": quantile(0.05),
        "median": median(values),
        "q95": quantile(0.95),
        "max": max(values),
    }


def _stable_half_crossing_interval(
    profiles: list[dict[str, object]],
    rate_field: str,
) -> dict[str, float | bool | None]:
    """Bracket the stable 50% crossing on the prospectively sampled time grid.

    This is a descriptive schedule-grid interval, not an exact latent event-time
    estimate. A crossing is accepted only when the observed rate is >=0.5 at
    that time and at every later sampled time, so one noisy early crossing does
    not define the median event time by itself.
    """
    if not profiles:
        raise ValueError("cannot bracket a median crossing from no profiles")
    ordered = sorted(profiles, key=lambda row: float(row["elapsed_hours"]))
    for i, row in enumerate(ordered):
        if (
            float(row[rate_field]) >= 0.5
            and all(float(later[rate_field]) >= 0.5 for later in ordered[i:])
        ):
            lower = 0.0 if i == 0 else float(ordered[i - 1]["elapsed_hours"])
            return {
                "lower_bound_hours": lower,
                "lower_bound_open": i > 0,
                "upper_bound_hours": float(row["elapsed_hours"]),
                "upper_bound_closed": True,
                "right_censored": False,
            }
    return {
        "lower_bound_hours": float(ordered[-1]["elapsed_hours"]),
        "lower_bound_open": True,
        "upper_bound_hours": None,
        "upper_bound_closed": False,
        "right_censored": True,
    }


def _median_gap_descriptor(
    pollination: dict[str, float | bool | None],
    constraint: dict[str, float | bool | None],
) -> dict[str, object]:
    p_lower = float(pollination["lower_bound_hours"])
    p_upper_raw = pollination["upper_bound_hours"]
    c_lower = float(constraint["lower_bound_hours"])
    c_upper_raw = constraint["upper_bound_hours"]
    p_upper = float(p_upper_raw) if p_upper_raw is not None else None
    c_upper = float(c_upper_raw) if c_upper_raw is not None else None

    lower_gap = c_lower - p_upper if p_upper is not None else None
    upper_gap = c_upper - p_lower if c_upper is not None else None

    positive = (
        p_upper is not None
        and (
            c_lower > p_upper
            or (
                c_lower == p_upper
                and bool(constraint["lower_bound_open"])
            )
        )
    )
    negative = (
        c_upper is not None
        and (
            p_lower > c_upper
            or (
                p_lower == c_upper
                and bool(pollination["lower_bound_open"])
            )
        )
    )

    if positive:
        state = "MEDIAN_TEMPORAL_SEPARATION_SUPPORTED_ON_SAMPLED_GRID"
    elif negative:
        state = "MEDIAN_TEMPORAL_ENTANGLEMENT_SUPPORTED_ON_SAMPLED_GRID"
    else:
        state = "MEDIAN_TEMPORAL_ORDERING_UNRESOLVED_ON_SAMPLED_GRID"

    return {
        "delta_t50_lower_bound_hours": lower_gap,
        "delta_t50_upper_bound_hours": upper_gap,
        "ordering_state": state,
        "definition": (
            "Delta_T50 = median onset of first attack-or-swelling constraint "
            "minus median pollination-completion time, each bracketed on the "
            "prospectively sampled time grid"
        ),
        "exact_individual_delta_t_estimated": False,
    }


def _validate_config(config: dict) -> tuple[str, str]:
    if config.get("schema") != SCHEMA:
        raise ValueError("event-time pilot schema mismatch")
    if config.get("status") != FREEZE_STATUS:
        raise ValueError("event-time pilot config is not prospectively frozen")
    if config.get("frozen_before_event_time_data") is not True:
        raise ValueError("event-time definitions must be frozen before data")

    population_id = config.get("population_id")
    season_id = config.get("season_id")
    if (
        not isinstance(population_id, str)
        or not population_id
        or population_id == PLACEHOLDER
    ):
        raise ValueError("event-time population_id must be resolved")
    if (
        not isinstance(season_id, str)
        or not season_id
        or season_id == PLACEHOLDER
    ):
        raise ValueError("event-time season_id must be resolved")

    for field in (
        "pollination_completion_definition",
        "pollination_completion_measurement",
        "attack_event_definition",
        "ovary_swelling_definition",
        "sampling_schedule_basis_note",
    ):
        value = config.get(field)
        if (
            not isinstance(value, str)
            or not value.strip()
            or value == PLACEHOLDER
        ):
            raise ValueError(f"{field} must be prospectively resolved")

    frozen_at = config.get("frozen_at_utc")
    if not isinstance(frozen_at, str) or not frozen_at:
        raise ValueError("frozen_at_utc is required")
    try:
        parsed = datetime.fromisoformat(frozen_at.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("frozen_at_utc must be ISO-8601") from exc
    if parsed.tzinfo is None:
        raise ValueError("frozen_at_utc must be timezone-aware")

    return population_id, season_id


def _validate_rows(
    rows: list[dict[str, str]],
    *,
    population_id: str,
    season_id: str,
) -> list[dict[str, object]]:
    normalized: list[dict[str, object]] = []

    for i, row in enumerate(rows, start=1):
        if row["population_id"] != population_id or row["season_id"] != season_id:
            raise ValueError(
                f"row {i} does not match frozen population/season"
            )
        for field in ("plant_id", "flower_id"):
            if not row[field] or row[field] == PLACEHOLDER:
                raise ValueError(f"row {i} has unresolved {field}")
        role = row["flower_role"]
        if role not in ROLES:
            raise ValueError(f"row {i} has unregistered flower_role {role!r}")

        anthesis = _number(row["anthesis_time_hours"], f"row {i}.anthesis_time_hours")
        observation = _number(
            row["observation_time_hours"],
            f"row {i}.observation_time_hours",
        )
        elapsed = observation - anthesis
        if elapsed < 0:
            raise ValueError(f"row {i} observation precedes anthesis")

        base: dict[str, object] = {
            "population_id": population_id,
            "season_id": season_id,
            "plant_id": row["plant_id"],
            "flower_id": row["flower_id"],
            "flower_role": role,
            "anthesis_time_hours": anthesis,
            "observation_time_hours": observation,
            "elapsed_hours": elapsed,
        }

        if role == POLLEN_ROLE:
            pollen = _number(row["pollen_grains"], f"row {i}.pollen_grains")
            if pollen < 0:
                raise ValueError(f"row {i}.pollen_grains must be >= 0")
            complete = _binary(
                row["pollination_complete"],
                f"row {i}.pollination_complete",
            )
            if row["attack_present"] or row["ovary_swollen"]:
                raise ValueError(
                    "POLLINATION_SENTINEL rows must leave attack/swelling blank"
                )
            base.update(
                {
                    "pollen_grains": pollen,
                    "pollination_complete": complete,
                    "attack_present": None,
                    "ovary_swollen": None,
                }
            )
        else:
            if row["pollen_grains"] or row["pollination_complete"]:
                raise ValueError(
                    "ATTACK_SWELL_SENTINEL rows must leave pollen fields blank"
                )
            base.update(
                {
                    "pollen_grains": None,
                    "pollination_complete": None,
                    "attack_present": _binary(
                        row["attack_present"],
                        f"row {i}.attack_present",
                    ),
                    "ovary_swollen": _binary(
                        row["ovary_swollen"],
                        f"row {i}.ovary_swollen",
                    ),
                }
            )

        normalized.append(base)

    by_flower: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in normalized:
        by_flower[str(row["flower_id"])].append(row)

    for flower_id, group in by_flower.items():
        roles = {str(row["flower_role"]) for row in group}
        plants = {str(row["plant_id"]) for row in group}
        anthesis_values = {float(row["anthesis_time_hours"]) for row in group}
        if len(roles) != 1 or len(plants) != 1 or len(anthesis_values) != 1:
            raise ValueError(
                f"flower {flower_id} changes role, plant, or anthesis time"
            )
        role = next(iter(roles))
        if role == POLLEN_ROLE:
            if len(group) != 1:
                raise ValueError(
                    f"pollination sentinel {flower_id} must be sampled once"
                )
            continue

        if len(group) < 2:
            raise ValueError(
                f"attack/swelling sentinel {flower_id} needs >=2 observations"
            )
        ordered = sorted(group, key=lambda row: float(row["elapsed_hours"]))
        times = [float(row["elapsed_hours"]) for row in ordered]
        if len(times) != len(set(times)):
            raise ValueError(
                f"attack/swelling sentinel {flower_id} repeats an observation time"
            )
        for field in ("attack_present", "ovary_swollen"):
            values = [int(row[field]) for row in ordered]
            if any(left > right for left, right in zip(values, values[1:])):
                raise ValueError(
                    f"{field} must be absorbing once observed for {flower_id}"
                )

    pollen_times = {
        float(row["elapsed_hours"])
        for row in normalized
        if row["flower_role"] == POLLEN_ROLE
    }
    natural_times = {
        float(row["elapsed_hours"])
        for row in normalized
        if row["flower_role"] == NATURAL_ROLE
    }
    if len(pollen_times) < 2:
        raise ValueError(
            "event-time pilot needs >=2 pollination sentinel time points"
        )
    if len(natural_times) < 2:
        raise ValueError(
            "event-time pilot needs >=2 attack/swelling observation time points"
        )

    return normalized


def _event_interval(
    rows: list[dict[str, object]],
    field: str,
) -> dict[str, float | bool | None]:
    ordered = sorted(rows, key=lambda row: float(row["elapsed_hours"]))
    negatives = [
        float(row["elapsed_hours"])
        for row in ordered
        if int(row[field]) == 0
    ]
    positives = [
        float(row["elapsed_hours"])
        for row in ordered
        if int(row[field]) == 1
    ]
    if not positives:
        return {
            "last_negative_hours": max(negatives),
            "first_positive_hours": None,
            "right_censored": True,
        }
    first_positive = min(positives)
    prior_negatives = [value for value in negatives if value < first_positive]
    return {
        "last_negative_hours": max(prior_negatives) if prior_negatives else 0.0,
        "first_positive_hours": first_positive,
        "right_censored": False,
    }


def build(config: dict, rows: list[dict[str, str]]) -> dict:
    population_id, season_id = _validate_config(config)
    normalized = _validate_rows(
        rows,
        population_id=population_id,
        season_id=season_id,
    )

    pollen_rows = [
        row for row in normalized
        if row["flower_role"] == POLLEN_ROLE
    ]
    natural_rows = [
        row for row in normalized
        if row["flower_role"] == NATURAL_ROLE
    ]

    pollen_by_time: dict[float, list[dict[str, object]]] = defaultdict(list)
    natural_by_time: dict[float, list[dict[str, object]]] = defaultdict(list)
    for row in pollen_rows:
        pollen_by_time[float(row["elapsed_hours"])].append(row)
    for row in natural_rows:
        natural_by_time[float(row["elapsed_hours"])].append(row)

    pollen_profiles = []
    for hours, group in sorted(pollen_by_time.items()):
        pollen_profiles.append(
            {
                "elapsed_hours": hours,
                "n_flowers": len(group),
                "n_plants": len({str(row["plant_id"]) for row in group}),
                "pollination_complete_rate": mean(
                    int(row["pollination_complete"]) for row in group
                ),
                "pollen_grains": _summary(
                    [float(row["pollen_grains"]) for row in group]
                ),
            }
        )

    natural_profiles = []
    for hours, group in sorted(natural_by_time.items()):
        natural_profiles.append(
            {
                "elapsed_hours": hours,
                "n_observations": len(group),
                "n_flowers": len({str(row["flower_id"]) for row in group}),
                "attack_free_rate": mean(
                    1 - int(row["attack_present"]) for row in group
                ),
                "ovary_not_swollen_rate": mean(
                    1 - int(row["ovary_swollen"]) for row in group
                ),
                "constraint_free_rate": mean(
                    int(row["attack_present"]) == 0
                    and int(row["ovary_swollen"]) == 0
                    for row in group
                ),
                "constraint_present_rate": mean(
                    int(row["attack_present"]) == 1
                    or int(row["ovary_swollen"]) == 1
                    for row in group
                ),
            }
        )

    natural_by_flower: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in natural_rows:
        natural_by_flower[str(row["flower_id"])].append(row)

    event_intervals = []
    constraint_first_positive: list[float] = []
    for flower_id, group in sorted(natural_by_flower.items()):
        attack = _event_interval(group, "attack_present")
        swelling = _event_interval(group, "ovary_swollen")
        positive_bounds = [
            value
            for value in (
                attack["first_positive_hours"],
                swelling["first_positive_hours"],
            )
            if value is not None
        ]
        first_constraint = min(positive_bounds) if positive_bounds else None
        if first_constraint is not None:
            constraint_first_positive.append(float(first_constraint))
        event_intervals.append(
            {
                "flower_id": flower_id,
                "plant_id": str(group[0]["plant_id"]),
                "attack_interval": attack,
                "swelling_interval": swelling,
                "first_constraint_positive_hours": first_constraint,
                "constraint_right_censored": first_constraint is None,
            }
        )

    complete_hours = [
        float(row["elapsed_hours"])
        for row in pollen_rows
        if int(row["pollination_complete"]) == 1
    ]

    common_times = sorted(set(pollen_by_time) & set(natural_by_time))
    joint_profiles = []
    pollen_profile_by_time = {
        row["elapsed_hours"]: row for row in pollen_profiles
    }
    natural_profile_by_time = {
        row["elapsed_hours"]: row for row in natural_profiles
    }
    for hours in common_times:
        p = pollen_profile_by_time[hours]
        n = natural_profile_by_time[hours]
        joint_profiles.append(
            {
                "elapsed_hours": hours,
                "pollination_complete_rate": p["pollination_complete_rate"],
                "attack_free_rate": n["attack_free_rate"],
                "ovary_not_swollen_rate": n["ovary_not_swollen_rate"],
                "constraint_free_rate": n["constraint_free_rate"],
                "constraint_present_rate": n["constraint_present_rate"],
                "n_pollination_sentinels": p["n_flowers"],
                "n_natural_history_flowers": n["n_flowers"],
            }
        )

    pollination_median_interval = _stable_half_crossing_interval(
        pollen_profiles,
        "pollination_complete_rate",
    )
    constraint_median_interval = _stable_half_crossing_interval(
        natural_profiles,
        "constraint_present_rate",
    )
    median_gap = _median_gap_descriptor(
        pollination_median_interval,
        constraint_median_interval,
    )

    return {
        "analysis": "pedicularis_g_event_time_pilot_v1",
        "population_id": population_id,
        "season_id": season_id,
        "config_status": FREEZE_STATUS,
        "pollination_completion_definition": config[
            "pollination_completion_definition"
        ],
        "pollination_completion_measurement": config[
            "pollination_completion_measurement"
        ],
        "attack_event_definition": config["attack_event_definition"],
        "ovary_swelling_definition": config["ovary_swelling_definition"],
        "n_rows": len(normalized),
        "n_pollination_sentinel_flowers": len(pollen_rows),
        "n_attack_swelling_sentinel_flowers": len(natural_by_flower),
        "n_plants": len({str(row["plant_id"]) for row in normalized}),
        "pollination_time_profiles": pollen_profiles,
        "attack_swelling_time_profiles": natural_profiles,
        "joint_time_profiles": joint_profiles,
        "pollination_complete_observation_hours": (
            _summary(complete_hours) if complete_hours else None
        ),
        "first_constraint_positive_observation_hours": (
            _summary(constraint_first_positive)
            if constraint_first_positive
            else None
        ),
        "event_intervals_by_flower": event_intervals,
        "median_pollination_completion_interval_hours": (
            pollination_median_interval
        ),
        "median_constraint_onset_interval_hours": constraint_median_interval,
        "median_temporal_separability_descriptor": median_gap,
        "timing_window_selected": False,
        "temporal_separability_inferred": False,
        "status": "G_EVENT_TIME_DESCRIPTORS_READY_NO_WINDOW_SELECTED",
        "interpretation": (
            "The pilot describes when prospectively defined pollination "
            "completion is observed and interval-censored onset of predator "
            "attack or ovary swelling. It also brackets the median pollination "
            "completion and median first-constraint onset on the sampled time grid "
            "and reports their interval difference (Delta_T50) without converting "
            "that exploratory descriptor into a barrier timing gate."
        ),
        "claim_ceiling": [
            "natural_history_event_time_calibration_only",
            "pollination_completion_hours_are_cross_sectional_observation_times",
            "attack_and_swelling_onsets_are_interval_censored",
            "delta_t50_is_a_schedule_grid_median_descriptor_not_an_exact_individual_gap",
            "does_not_use_barrier_application_time_as_natural_window",
            "does_not_select_minimum_or_maximum_barrier_hour",
            "does_not_validate_G",
            "does_not_support_cross_system_timing_generalization",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Summarize focal P. rex natural event times relevant to a selective "
            "post-pollination predator-exclusion window"
        )
    )
    parser.add_argument("config_json", type=Path)
    parser.add_argument("event_time_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(_read_json(args.config_json), _read_csv(args.event_time_csv))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

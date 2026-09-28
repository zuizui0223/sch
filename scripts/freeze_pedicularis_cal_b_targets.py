from __future__ import annotations

import argparse
import csv
import json
import math
from datetime import datetime
from pathlib import Path


PLACEHOLDER = "REQUIRED_BEFORE_USE"
FREEZE_STATUS = "PEDICULARIS_CAL_B_TARGET_PROSPECTIVELY_FROZEN"
RECEIPT_SCHEMA = "SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1"

EXPECTED = {
    "pollination_weight.min_pollen_grain_delta": ("P1", "MINIMUM_EFFECT"),
    "pollination_weight.min_initial_seed_set_delta": ("P1", "MINIMUM_EFFECT"),
    "predator_weight.min_early_attack_reduction": ("G", "MINIMUM_EFFECT"),
    "predator_weight.min_predation_fraction_reduction": ("G", "MINIMUM_EFFECT"),
    "predator_weight.min_final_seed_set_gain": ("G", "MINIMUM_EFFECT"),
    "method_gate.min_hours_after_anthesis_before_barrier": ("G", "TIMING_LOWER_BOUND"),
    "method_gate.max_hours_after_anthesis_before_barrier": ("G", "TIMING_UPPER_BOUND"),
}

REQUIRED_OBSERVED = (
    "observed_n",
    "observed_mean",
    "observed_q05",
    "observed_median",
    "observed_q95",
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CAL-B target table has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("CAL-B target table is empty")
    return rows


def _number(value: str, label: str) -> float:
    if not value or value == PLACEHOLDER:
        raise ValueError(f"{label} is not specified")
    try:
        out = float(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be numeric") from exc
    if not math.isfinite(out):
        raise ValueError(f"{label} must be finite")
    return out


def _positive_int(value: str, label: str) -> int:
    number = _number(value, label)
    if number < 1 or not number.is_integer():
        raise ValueError(f"{label} must be a positive integer")
    return int(number)


def _timestamp(value: str, label: str) -> str:
    if not value or value == PLACEHOLDER:
        raise ValueError(f"{label} is not specified")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} is not a valid ISO timestamp") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must be timezone-aware")
    return value


def validate(rows: list[dict[str, str]]) -> dict:
    if len(rows) != len(EXPECTED):
        raise ValueError(
            f"expected {len(EXPECTED)} CAL-B decisions, found {len(rows)}"
        )

    gate_paths = [row.get("gate_path", "") for row in rows]
    if len(gate_paths) != len(set(gate_paths)):
        raise ValueError("CAL-B gate_path must be unique")
    if set(gate_paths) != set(EXPECTED):
        raise ValueError(
            "CAL-B target coverage mismatch: "
            f"missing={sorted(set(EXPECTED) - set(gate_paths))}, "
            f"extra={sorted(set(gate_paths) - set(EXPECTED))}"
        )

    decision_ids = [row.get("decision_id", "") for row in rows]
    if any(not value for value in decision_ids):
        raise ValueError("decision_id is required")
    if len(decision_ids) != len(set(decision_ids)):
        raise ValueError("decision_id must be unique")

    contexts = {
        (row.get("population_id"), row.get("season_id"))
        for row in rows
    }
    if len(contexts) != 1:
        raise ValueError("all CAL-B decisions must share one population and season")
    population_id, season_id = next(iter(contexts))
    if not population_id or population_id == PLACEHOLDER:
        raise ValueError("CAL-B population_id is not frozen")
    if not season_id or season_id == PLACEHOLDER:
        raise ValueError("CAL-B season_id is not frozen")

    targets: dict[str, float] = {}
    decision_rows = []

    for row in rows:
        gate_path = row["gate_path"]
        expected_lane, expected_kind = EXPECTED[gate_path]
        if row.get("lane") != expected_lane:
            raise ValueError(f"{gate_path} lane mismatch")
        if row.get("decision_kind") != expected_kind:
            raise ValueError(f"{gate_path} decision_kind mismatch")
        if not row.get("calibration_source_path"):
            raise ValueError(f"{gate_path} calibration_source_path is required")

        observed = {
            "n": _positive_int(row["observed_n"], f"{gate_path}.observed_n"),
            "mean": _number(row["observed_mean"], f"{gate_path}.observed_mean"),
            "q05": _number(row["observed_q05"], f"{gate_path}.observed_q05"),
            "median": _number(row["observed_median"], f"{gate_path}.observed_median"),
            "q95": _number(row["observed_q95"], f"{gate_path}.observed_q95"),
        }
        if not (
            observed["q05"]
            <= observed["median"]
            <= observed["q95"]
        ):
            raise ValueError(f"{gate_path} observed quantiles are not ordered")

        target = _number(row["target_value"], f"{gate_path}.target_value")
        if expected_kind == "MINIMUM_EFFECT" and target <= 0:
            raise ValueError(f"{gate_path} minimum effect must be > 0")
        if expected_kind.startswith("TIMING_") and target < 0:
            raise ValueError(f"{gate_path} timing bound must be >= 0")

        basis_note = row.get("target_basis_note", "")
        if not basis_note or basis_note == PLACEHOLDER:
            raise ValueError(f"{gate_path}.target_basis_note is not specified")
        if row.get("frozen_before_confirmatory_data") != "YES":
            raise ValueError(
                f"{gate_path} must be frozen before confirmatory data"
            )
        frozen_at = _timestamp(
            row.get("frozen_at_utc", ""),
            f"{gate_path}.frozen_at_utc",
        )
        if row.get("status") != FREEZE_STATUS:
            raise ValueError(f"{gate_path} CAL-B target status is not positive")

        targets[gate_path] = target
        decision_rows.append(
            {
                "decision_id": row["decision_id"],
                "gate_path": gate_path,
                "lane": expected_lane,
                "decision_kind": expected_kind,
                "target_value": target,
                "target_basis_note": basis_note,
                "calibration_source_path": row["calibration_source_path"],
                "observed_pilot_summary": observed,
                "frozen_at_utc": frozen_at,
            }
        )

    lower = targets["method_gate.min_hours_after_anthesis_before_barrier"]
    upper = targets["method_gate.max_hours_after_anthesis_before_barrier"]
    if lower >= upper:
        raise ValueError(
            "CAL-B G timing lower bound must be strictly below upper bound"
        )

    return {
        "receipt_schema_version": RECEIPT_SCHEMA,
        "analysis": "pedicularis_cal_b_target_freeze",
        "population_id": population_id,
        "season_id": season_id,
        "n_decisions": len(decision_rows),
        "targets": dict(sorted(targets.items())),
        "decision_rows": sorted(
            decision_rows,
            key=lambda row: row["gate_path"],
        ),
        "status": "PEDICULARIS_CAL_B_TARGETS_FROZEN",
        "claim_ceiling": [
            "prospective_target_definition_only",
            "pilot_descriptors_are_context_not_automatic_cutoffs",
            "does_not_validate_P1_or_G",
            "does_not_set_CAL_C_assumed_true_effects",
            "does_not_set_sample_size",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and freeze the seven Pedicularis CAL-B target decisions"
    )
    parser.add_argument("cal_b_target_csv", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = validate(_read(args.cal_b_target_csv))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

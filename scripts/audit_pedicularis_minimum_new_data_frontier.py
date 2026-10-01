from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FRONTIER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_MINIMUM_NEW_DATA_FRONTIER_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("minimum-new-data frontier has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("minimum-new-data frontier is empty")
    return rows


def build(path: Path = DEFAULT_FRONTIER) -> dict:
    rows = _read(path)
    by_id = {row["stage_id"]: row for row in rows}
    if len(by_id) != len(rows):
        raise ValueError("stage_id must be unique")

    expected = [
        "REGISTERED_5",
        "CAL_P0",
        "CAL_P1",
        "CAL_G",
        "CAL_C",
        "F0_ASSEMBLY",
    ]
    if [row["stage_id"] for row in rows] != expected:
        raise ValueError("minimum-new-data stage order drift")

    field = [
        row for row in rows
        if row["new_field_data_required"] == "YES"
    ]
    if [row["stage_id"] for row in field] != [
        "CAL_P0", "CAL_P1", "CAL_G"
    ]:
        raise ValueError(
            "new field calibration must remain exactly P0/P1/G"
        )

    empirical_gate_counts = {
        "CAL_P0": 8,
        "CAL_P1": 8,
        "CAL_G": 11,
    }
    cal_c_variance_counts = {
        "CAL_P0": 8,
        "CAL_P1": 8,
        "CAL_G": 9,
    }

    if sum(empirical_gate_counts.values()) != 27:
        raise AssertionError("empirical target count drift")
    if sum(cal_c_variance_counts.values()) != 25:
        raise AssertionError("CAL-C criterion count drift")

    return {
        "analysis": "pedicularis_minimum_new_data_frontier_v1",
        "n_total_f0_gates": 40,
        "n_registered_without_new_data": 5,
        "n_empirical_target_gates_requiring_new_field_calibration": 27,
        "n_sample_size_gates_computed_after_calibration": 8,
        "n_independent_field_calibration_cohorts": 3,
        "field_calibration_cohorts": [
            "CAL_P0", "CAL_P1", "CAL_G"
        ],
        "empirical_target_gates_by_cohort": empirical_gate_counts,
        "cal_c_variance_criteria_by_cohort": cal_c_variance_counts,
        "n_cal_c_variance_criteria": 25,
        "repeatability_is_additional_independent_cohort": False,
        "repeatability_nesting_rule": (
            "same-flower repeatability flowers are a subset of "
            "the CAL_P0 calibration flowers"
        ),
        "p0_p1_g_flower_sets_must_be_disjoint": True,
        "plant_level_overlap_can_be_reported_but_not_silently_used_as_independence": True,
        "published_data_role": (
            "external target/variance/feasibility priors only; "
            "published evidence reduces design invention but does not replace "
            "the three focal calibration cohorts"
        ),
        "status": "THREE_FIELD_CALIBRATION_COHORTS_ARE_THE_MINIMUM_DIRECT_DATA_FRONTIER",
        "claim_ceiling": [
            "27_empirical_gate_targets_do_not_mean_27_separate_experiments",
            "CAL_C_is_computation_not_a_fourth_field_cohort",
            "same_flower_repeatability_is_nested_within_CAL_P0",
            "published_priors_do_not_create_missing_focal_interventions",
            "confirmatory_rows_remain_separate_from_calibration_rows",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the minimum new Pedicularis field-data burden after "
            "published-data recovery and calibration-module consolidation"
        )
    )
    parser.add_argument("--frontier", type=Path, default=DEFAULT_FRONTIER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.frontier)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

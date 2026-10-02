from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from scripts.audit_pedicularis_focal_direct_evidence_search import (
    build as build_focal_search,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_YIELD = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CALIBRATION_COLLECTION_YIELD_V1.csv"
)
CAL_A_TARGETS = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_A_TARGET_TEMPLATE_V1.csv"
)
CAL_B_TARGETS = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_B_TARGET_TEMPLATE_V1.csv"
)
CAL_C_CRITERIA = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_C_CRITERIA_TEMPLATE_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError(f"{path} is empty")
    return rows


def _int(row: dict[str, str], field: str) -> int:
    try:
        value = int(row[field])
    except (KeyError, ValueError) as exc:
        raise ValueError(
            f"{row.get('bundle_id', '<row>')}.{field} must be an integer"
        ) from exc
    if value < 0:
        raise ValueError(f"{field} must be >= 0")
    return value


def build(path: Path = DEFAULT_YIELD) -> dict:
    rows = _read(path)
    bundle_ids = [row["bundle_id"] for row in rows]
    if len(bundle_ids) != len(set(bundle_ids)):
        raise ValueError("bundle_id must be unique")

    expected_bundles = {
        "COHORT_REGISTRY",
        "G_EXPLORATORY",
        "P0_EXPLORATORY",
        "CAL_A_REPEATABILITY",
        "P1_EXPLORATORY",
    }
    if set(bundle_ids) != expected_bundles:
        raise ValueError(
            "collection-yield bundle coverage mismatch: "
            f"missing={sorted(expected_bundles - set(bundle_ids))}, "
            f"extra={sorted(set(bundle_ids) - expected_bundles)}"
        )

    cal_a = _read(CAL_A_TARGETS)
    cal_b = _read(CAL_B_TARGETS)
    cal_c = _read(CAL_C_CRITERIA)

    cal_a_by_lane = Counter(row["lane"] for row in cal_a)
    cal_b_by_lane = Counter(row["lane"] for row in cal_b)
    cal_c_by_lane = Counter(row["lane"] for row in cal_c)
    repeatability_floors = sum(
        row["repeatability_source_path"] != "NOT_APPLICABLE"
        for row in cal_a
    )

    expected_counts = {
        "G_EXPLORATORY": {
            "cal_a_observed_decisions": cal_a_by_lane["G"],
            "cal_b_effect_or_timing_decisions": cal_b_by_lane["G"],
            "cal_c_pilot_sd_criteria": cal_c_by_lane["G"],
        },
        "P0_EXPLORATORY": {
            "cal_a_observed_decisions": cal_a_by_lane["P0"],
            "cal_b_effect_or_timing_decisions": cal_b_by_lane["P0"],
            "cal_c_pilot_sd_criteria": cal_c_by_lane["P0"],
        },
        "P1_EXPLORATORY": {
            "cal_a_observed_decisions": cal_a_by_lane["P1"],
            "cal_b_effect_or_timing_decisions": cal_b_by_lane["P1"],
            "cal_c_pilot_sd_criteria": cal_c_by_lane["P1"],
        },
    }

    for row in rows:
        template_path = ROOT / row["template_path"]
        if not template_path.exists():
            raise ValueError(
                f"registered collection template does not exist: {row['template_path']}"
            )

    by_id = {row["bundle_id"]: row for row in rows}
    for bundle_id, fields in expected_counts.items():
        row = by_id[bundle_id]
        for field, expected in fields.items():
            if _int(row, field) != expected:
                raise ValueError(
                    f"{bundle_id}.{field} expected {expected}, "
                    f"found {row[field]}"
                )

    repeatability_row = by_id["CAL_A_REPEATABILITY"]
    if (
        _int(repeatability_row, "cal_a_measurement_noise_floors")
        != repeatability_floors
    ):
        raise ValueError(
            "CAL_A_REPEATABILITY measurement-noise floor count drifted"
        )

    for row in rows:
        if _int(row, "direct_f0_values") != 0:
            raise ValueError(
                "field calibration bundles must not directly create F0 values"
            )

    direct_target_sum = sum(
        _int(row, "cal_a_observed_decisions")
        for row in rows
    )
    cal_b_sum = sum(
        _int(row, "cal_b_effect_or_timing_decisions")
        for row in rows
    )
    cal_c_sum = sum(
        _int(row, "cal_c_pilot_sd_criteria")
        for row in rows
    )

    if direct_target_sum != len(cal_a):
        raise ValueError(
            f"CAL-A observed target yield {direct_target_sum} != {len(cal_a)}"
        )
    if cal_b_sum != len(cal_b):
        raise ValueError(
            f"CAL-B target yield {cal_b_sum} != {len(cal_b)}"
        )
    if cal_c_sum != len(cal_c):
        raise ValueError(
            f"CAL-C SD criterion yield {cal_c_sum} != {len(cal_c)}"
        )

    focal = build_focal_search()
    if focal["direct_registered_g_recovered"]:
        raise ValueError(
            "collection priority must be re-audited if focal independent G "
            "becomes recovered"
        )
    if focal["direct_multi_level_p0_recovered"]:
        raise ValueError(
            "collection priority must be re-audited if focal multi-level P0 "
            "becomes recovered"
        )
    if focal["direct_registered_p1_recovered"]:
        raise ValueError(
            "collection priority must be re-audited if focal P1 becomes recovered"
        )

    priorities = {
        row["bundle_id"]: int(row["risk_priority"])
        for row in rows
        if row["bundle_id"] != "COHORT_REGISTRY"
    }
    if priorities != {
        "G_EXPLORATORY": 1,
        "P0_EXPLORATORY": 2,
        "CAL_A_REPEATABILITY": 2,
        "P1_EXPLORATORY": 3,
    }:
        raise ValueError("risk-priority ordering drifted")

    yield_rows = {}
    for row in rows:
        bundle_id = row["bundle_id"]
        if bundle_id == "COHORT_REGISTRY":
            continue
        decision_distributions = (
            _int(row, "cal_a_observed_decisions")
            + _int(row, "cal_b_effect_or_timing_decisions")
        )
        support_outputs = (
            decision_distributions
            + _int(row, "cal_a_measurement_noise_floors")
            + _int(row, "cal_c_pilot_sd_criteria")
        )
        yield_rows[bundle_id] = {
            "cal_a_observed_decisions": _int(
                row, "cal_a_observed_decisions"
            ),
            "cal_a_measurement_noise_floors": _int(
                row, "cal_a_measurement_noise_floors"
            ),
            "cal_b_effect_or_timing_decisions": _int(
                row, "cal_b_effect_or_timing_decisions"
            ),
            "cal_c_pilot_sd_criteria": _int(
                row, "cal_c_pilot_sd_criteria"
            ),
            "decision_distributions": decision_distributions,
            "total_calibration_support_outputs": support_outputs,
            "structural_risk": row["structural_risk"],
            "risk_priority": int(row["risk_priority"]),
            "execution_mode": row["execution_mode"],
        }

    return {
        "analysis": "pedicularis_calibration_collection_yield_v1",
        "n_collection_rows": len(rows),
        "same_context_requirement": (
            "all calibration bundles and registry must share one population "
            "and season before package assembly"
        ),
        "derived_gate_yield": {
            "cal_a_observed_decisions": direct_target_sum,
            "cal_a_measurement_noise_floors": repeatability_floors,
            "cal_b_effect_or_timing_decisions": cal_b_sum,
            "cal_c_pilot_sd_criteria": cal_c_sum,
            "direct_f0_values": 0,
        },
        "bundle_yield": yield_rows,
        "risk_priority_order": [
            "G_EXPLORATORY",
            "P0_EXPLORATORY+CAL_A_REPEATABILITY",
            "P1_EXPLORATORY",
        ],
        "priority_interpretation": (
            "risk priority, not mandatory chronological order; lanes may run "
            "in parallel as phenology requires, but scarce effort should first "
            "retire focal G method risk, then focal P0 manipulation risk"
        ),
        "package_completion_requirement": [
            "COHORT_REGISTRY",
            "CAL_A_REPEATABILITY",
            "P0_EXPLORATORY",
            "P1_EXPLORATORY",
            "G_EXPLORATORY",
        ],
        "status": "CALIBRATION_COLLECTION_YIELD_MAPPED_NO_SAMPLE_SIZE_INVENTED",
        "claim_ceiling": [
            "yield_counts_are_derived_from_existing_registered_templates",
            "risk_priority_is_not_a_sample_size",
            "priority_is_not_a_confirmatory_stop_rule",
            "repeatability_should_be_nested_with_P0_when_feasible",
            "all_four_data_bundles_are_still_required_for_full_package",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit the information yield and fail-fast priority of the four "
            "Pedicularis calibration data bundles without inventing sample sizes"
        )
    )
    parser.add_argument("--yield-ledger", type=Path, default=DEFAULT_YIELD)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.yield_ledger)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

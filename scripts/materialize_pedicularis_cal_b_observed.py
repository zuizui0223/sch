from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


PLACEHOLDER = "REQUIRED_BEFORE_USE"
SUMMARY_STATUS = "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION"
OBSERVED_FIELDS = ("n", "mean", "q05", "median", "q95")


def _load_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("CAL-B target template has no header")
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]


def _resolve_path(payload: dict, dotted_path: str) -> dict:
    current: object = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ValueError(
                f"calibration summary lacks source path {dotted_path!r}"
            )
        current = current[part]
    if not isinstance(current, dict):
        raise ValueError(
            f"calibration source {dotted_path!r} is not a summary object"
        )
    return current


def build(
    calibration_summary: dict,
    target_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], dict]:
    if calibration_summary.get("status") != SUMMARY_STATUS:
        raise ValueError(
            "CAL-B materialization requires the threshold-free calibration summary"
        )
    if calibration_summary.get("thresholds_selected") is not False:
        raise ValueError("calibration summary must not have selected thresholds")
    if calibration_summary.get("confirmatory_receipt_generated") is not False:
        raise ValueError("calibration summary must not be confirmatory evidence")

    population_id = calibration_summary.get("population_id")
    season_id = calibration_summary.get("season_id")
    if not isinstance(population_id, str) or not population_id:
        raise ValueError("calibration summary population_id is missing")
    if not isinstance(season_id, str) or not season_id:
        raise ValueError("calibration summary season_id is missing")

    available = set(calibration_summary.get("available_pilot_lanes") or [])
    if not {"P1", "G"} <= available:
        raise ValueError("CAL-B materialization requires both P1 and G pilot summaries")

    out: list[dict[str, str]] = []
    seen_decisions: set[str] = set()

    for source_row in target_rows:
        row = dict(source_row)
        decision_id = row.get("decision_id", "")
        if not decision_id:
            raise ValueError("decision_id is required")
        if decision_id in seen_decisions:
            raise ValueError("decision_id must be unique")
        seen_decisions.add(decision_id)

        for field in (
            "target_value",
            "target_basis_note",
            "frozen_before_confirmatory_data",
            "frozen_at_utc",
            "status",
        ):
            if row.get(field) != PLACEHOLDER:
                raise ValueError(
                    f"{decision_id}.{field} must remain unresolved during materialization"
                )

        observed = _resolve_path(
            calibration_summary,
            row["calibration_source_path"],
        )
        for field in OBSERVED_FIELDS:
            if field not in observed or observed[field] is None:
                raise ValueError(
                    f"{decision_id} calibration source lacks observed {field}"
                )

        row["population_id"] = population_id
        row["season_id"] = season_id
        row["observed_n"] = str(observed["n"])
        row["observed_mean"] = repr(float(observed["mean"]))
        row["observed_q05"] = repr(float(observed["q05"]))
        row["observed_median"] = repr(float(observed["median"]))
        row["observed_q95"] = repr(float(observed["q95"]))
        out.append(row)

    receipt = {
        "analysis": "pedicularis_cal_b_observed_materialization_v1",
        "population_id": population_id,
        "season_id": season_id,
        "n_target_decisions": len(out),
        "n_observed_summaries_materialized": len(out),
        "targets_selected": 0,
        "status": "CAL_B_OBSERVED_SUMMARIES_MATERIALIZED_TARGETS_UNFROZEN",
        "claim_ceiling": [
            "observed_pilot_summary_provenance_only",
            "does_not_choose_minimum_effect",
            "does_not_choose_G_timing_window",
            "does_not_generate_confirmatory_receipt",
        ],
    }
    return out, receipt


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError("cannot write empty CAL-B target table")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Copy P1/G pilot descriptors into the Pedicularis CAL-B target "
            "decision table without selecting targets"
        )
    )
    parser.add_argument("calibration_summary_json", type=Path)
    parser.add_argument("target_template_csv", type=Path)
    parser.add_argument("out_csv", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    rows, receipt = build(
        _load_json(args.calibration_summary_json),
        _read_csv(args.target_template_csv),
    )
    _write_csv(args.out_csv, rows)
    payload = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()

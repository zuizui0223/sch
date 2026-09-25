from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as h:
        return [
            {k: (v or "").strip() for k, v in row.items()}
            for row in csv.DictReader(h)
        ]


def _support(beta: float, se: float) -> str:
    if se <= 0:
        raise ValueError("SE must be positive")
    z = beta / se
    if z > 1.96:
        return "SUPPORTED_POSITIVE"
    if z < -1.96:
        return "SUPPORTED_NEGATIVE"
    return "NOT_SUPPORTED"


def build(source_path: Path) -> dict[str, object]:
    rows = _read(source_path)
    if not rows:
        raise ValueError("empty V27 source freeze")

    eligible = [row for row in rows if row["axis_eligible"] == "YES"]
    ineligible = [row for row in rows if row["axis_eligible"] == "NO"]

    adjudicated_rows = []
    by_programme_axis: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)

    for row in eligible:
        if not row["beta"] or not row["se"]:
            raise ValueError(
                f"eligible row missing beta/SE: {row['programme_id']} {row['canonical_axis']}"
            )
        beta = float(row["beta"])
        se = float(row["se"])
        item = {
            **row,
            "beta": beta,
            "se": se,
            "z": beta / se,
            "support_status": _support(beta, se),
        }
        adjudicated_rows.append(item)
        by_programme_axis[(row["programme_id"], row["canonical_axis"])].append(item)

    axis_rows = []
    for (programme, axis), axis_contexts in sorted(by_programme_axis.items()):
        if len(axis_contexts) < 2:
            raise ValueError(f"eligible axis lacks >=2 source-defined contexts: {axis}")
        supported_positive = any(
            row["support_status"] == "SUPPORTED_POSITIVE" for row in axis_contexts
        )
        supported_negative = any(
            row["support_status"] == "SUPPORTED_NEGATIVE" for row in axis_contexts
        )
        by_year: dict[str, list[dict[str, object]]] = defaultdict(list)
        for context_row in axis_contexts:
            by_year[str(context_row["year"])].append(context_row)
        within_year_reversal = any(
            any(r["support_status"] == "SUPPORTED_POSITIVE" for r in year_rows)
            and any(r["support_status"] == "SUPPORTED_NEGATIVE" for r in year_rows)
            for year_rows in by_year.values()
        )
        axis_rows.append(
            {
                "programme_id": programme,
                "canonical_axis": axis,
                "n_source_defined_contexts": len(axis_contexts),
                "supported_positive": supported_positive,
                "supported_negative": supported_negative,
                "bidirectionally_supported_reversal": (
                    supported_positive and supported_negative
                ),
                "within_year_bidirectionally_supported_reversal": within_year_reversal,
                "support_statuses": sorted(
                    {row["support_status"] for row in axis_contexts}
                ),
            }
        )

    programmes = []
    programme_ids = sorted({row["programme_id"] for row in axis_rows})
    for programme in programme_ids:
        axes = [row for row in axis_rows if row["programme_id"] == programme]
        n_axes = len(axes)
        n_reversal = sum(row["bidirectionally_supported_reversal"] for row in axes)
        n_within_year = sum(
            row["within_year_bidirectionally_supported_reversal"]
            for row in axes
        )
        programmes.append(
            {
                "programme_id": programme,
                "n_eligible_repeated_axes": n_axes,
                "n_bidirectionally_supported_reversal_axes": n_reversal,
                "q_j": n_reversal / n_axes,
                "n_within_year_supported_reversal_axes": n_within_year,
                "n_cross_year_or_cross_stratum_only_reversal_axes": (
                    n_reversal - n_within_year
                ),
                "reversal_axis_ids": sorted(
                    row["canonical_axis"]
                    for row in axes
                    if row["bidirectionally_supported_reversal"]
                ),
            }
        )

    return {
        "analysis": "sch_h2_holdout_v27_outcomes",
        "source_row_count": len(rows),
        "eligible_numeric_row_count": len(eligible),
        "ineligible_source_row_count": len(ineligible),
        "n_programmes_adjudicated": len(programmes),
        "n_eligible_axes": len(axis_rows),
        "n_supported_reversal_axes": sum(
            row["bidirectionally_supported_reversal"] for row in axis_rows
        ),
        "programme_rows": programmes,
        "axis_rows": axis_rows,
        "status": "THREE_HELDOUT_PROGRAMMES_OUTCOME_ADJUDICATED_ONE_REMAINS_PENDING",
        "claim_ceiling": [
            "uses_all_uncertainty_resolved_source_defined_contexts",
            "no_posthoc_context_pair_selection",
            "support_requires_abs_beta_over_se_gt_1_96",
            "categorical_or_nonfloral_rows_do_not_enter_denominator",
            "programme_is_primary_inference_unit",
            "impatiens_remains_pending_without_numeric_uncertainty_table",
            "primary_q_uses_all_registered_source_defined_contexts_including_year",
            "within_year_reversal_diagnostic_is_secondary_not_primary",
            "trillium_primary_reversals_are_not_attributed_to_pollination_modifier_alone",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    result = build(a.source)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if a.output:
        a.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

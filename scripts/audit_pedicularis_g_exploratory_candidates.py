from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT / "empirical" / "architecture"
    / "PEDICULARIS_G_EXPLORATORY_CANDIDATES_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
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


def build(path: Path = DEFAULT_LEDGER) -> dict:
    rows = _read(path)
    ids = [row["candidate_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("G candidate_id must be unique")

    if {row["automatic_selection_allowed"] for row in rows} != {"NO"}:
        raise ValueError("no exploratory G candidate may be auto-selected")

    priorities = {}
    for row in rows:
        try:
            priority = int(row["exploratory_priority"])
        except ValueError as exc:
            raise ValueError("exploratory_priority must be integer") from exc
        if priority < 1:
            raise ValueError("exploratory_priority must be >=1")
        priorities[row["candidate_id"]] = priority

    first = sorted(
        candidate
        for candidate, priority in priorities.items()
        if priority == 1
    )
    if first != ["G_A1_FINE_MESH", "G_A2_POROUS_TUBING"]:
        raise ValueError(
            "first exploratory tier must remain fine mesh + porous tubing"
        )

    whole = next(
        row for row in rows
        if row["candidate_id"] == "G_C_WHOLE_FLOWER_MESH"
    )
    if whole["pollinator_entry_expected"] != (
        "NOT_PRESERVED_DURING_OPEN_FLOWER_PHASE"
    ):
        raise ValueError(
            "whole-flower mesh must remain disqualified during open pollination"
        )

    chemical = next(
        row for row in rows if row["candidate_id"] == "G_D_CHEMICAL"
    )
    if chemical["exploratory_priority"] != "4":
        raise ValueError("chemical route must remain last-priority")

    return {
        "analysis": "pedicularis_g_exploratory_candidate_matrix_v1",
        "n_candidates": len(rows),
        "priority_counts": dict(
            sorted(Counter(priorities.values()).items())
        ),
        "first_tier_candidates": first,
        "second_tier_candidates": sorted(
            candidate for candidate, p in priorities.items() if p == 2
        ),
        "fallback_candidates": sorted(
            candidate for candidate, p in priorities.items() if p >= 3
        ),
        "automatic_method_selection": False,
        "screen_with": "screen_pedicularis_g_exploratory_methods.py",
        "status": "G_EXPLORATORY_CANDIDATES_DEFINED_EFFECT_TARGETS_UNFROZEN",
        "claim_ceiling": [
            "candidate_class_priority_only",
            "no_effect_thresholds_selected",
            "no_equivalence_margins_selected",
            "no_candidate_declared_valid_without_focal_V4_rows",
            "hard_validity_screen_must_precede_method_selection",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.ledger)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

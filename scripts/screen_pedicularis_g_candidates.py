from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from scripts import evaluate_pedicularis_predator_method as gmethod
from scripts import screen_pedicularis_g_exploratory_methods as screen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CANDIDATES = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_EXPLORATORY_CANDIDATES_V1.csv"
)


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


def build(
    field_rows: list[dict[str, str]],
    candidate_rows: list[dict[str, str]],
) -> dict:
    candidate_ids = [row["candidate_id"] for row in candidate_rows]
    method_codes = [row["field_exclusion_method"] for row in candidate_rows]
    if len(candidate_ids) != len(set(candidate_ids)):
        raise ValueError("candidate_id must be unique")
    if len(method_codes) != len(set(method_codes)):
        raise ValueError("field_exclusion_method must be unique")
    if any(not value for value in method_codes):
        raise ValueError("every G candidate needs a canonical field method code")

    by_method = {
        row["field_exclusion_method"]: row
        for row in candidate_rows
    }

    observed_methods = sorted({
        row["exclusion_method"]
        for row in field_rows
        if row["predator_treatment"] == "EXCLUDED"
    })
    unknown = sorted(set(observed_methods) - set(by_method))
    if unknown:
        raise ValueError(
            "V4 EXCLUDED rows use unregistered G field method codes: "
            + ", ".join(unknown)
        )

    if not observed_methods:
        raise ValueError("V4 candidate screen requires EXCLUDED rows")

    base = screen.build(field_rows)

    candidate_screens = {}
    for method in observed_methods:
        candidate = by_method[method]
        method_screen = base["method_screens"][method]
        candidate_screens[candidate["candidate_id"]] = {
            "candidate_id": candidate["candidate_id"],
            "field_exclusion_method": method,
            "device_class": candidate["device_class"],
            "exploratory_priority": int(candidate["exploratory_priority"]),
            "precedent_basis": candidate["precedent_basis"],
            "known_failure_mode": candidate["known_failure_mode"],
            "advance_rule": candidate["advance_rule"],
            "hard_validity_all_pass": method_screen[
                "hard_validity_all_pass"
            ],
            "screen_state": method_screen["screen_state"],
            "n_paired_plants": method_screen["n_paired_plants"],
            "barrier_delay_hours": method_screen["barrier_delay_hours"],
            "effect_distributions": method_screen[
                "effect_distributions"
            ],
            "contamination_distributions": method_screen[
                "contamination_distributions"
            ],
            "hard_validity_failure_counts": method_screen[
                "hard_validity_failure_counts"
            ],
        }

    hard_pass_candidates = sorted(
        candidate_id
        for candidate_id, result in candidate_screens.items()
        if result["hard_validity_all_pass"]
    )
    retired_candidates = sorted(
        candidate_id
        for candidate_id, result in candidate_screens.items()
        if not result["hard_validity_all_pass"]
    )

    if not hard_pass_candidates:
        frontier = "ALL_TESTED_CANDIDATES_FAIL_HARD_VALIDITY"
    elif len(hard_pass_candidates) == 1:
        frontier = (
            "ONE_TESTED_CANDIDATE_PASSES_HARD_VALIDITY_"
            "EFFECT_SELECTIVITY_TARGETS_STILL_UNFROZEN"
        )
    else:
        frontier = (
            "MULTIPLE_TESTED_CANDIDATES_PASS_HARD_VALIDITY_"
            "NO_AUTOMATIC_SELECTION"
        )

    return {
        "analysis": "pedicularis_g_candidate_linked_screen_v1",
        "population_id": base["population_id"],
        "season_id": base["season_id"],
        "n_registered_candidates": len(candidate_rows),
        "n_tested_candidates": len(candidate_screens),
        "tested_candidate_ids": sorted(candidate_screens),
        "hard_validity_pass_candidate_ids": hard_pass_candidates,
        "retired_candidate_ids": retired_candidates,
        "candidate_screens": candidate_screens,
        "current_frontier": frontier,
        "candidate_selected": False,
        "effect_thresholds_applied": False,
        "selectivity_thresholds_applied": False,
        "confirmatory_receipt_generated": False,
        "status": "G_CANDIDATE_LINKED_EXPLORATORY_SCREEN_ONLY",
        "claim_ceiling": [
            "candidate_identity_and_hard_validity_only",
            "hard_failure_can_retire_tested_candidate_as_is",
            "hard_pass_does_not_establish_effectiveness",
            "hard_pass_does_not_establish_selectivity",
            "multiple_pass_candidates_are_not_ranked_by_posthoc_effect_size",
            "does_not_generate_registered_G_receipt",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Link focal P. rex V4 G rows to the registered exploratory "
            "candidate matrix and run fail-fast hard-validity screening"
        )
    )
    parser.add_argument("g_v4_csv", type=Path)
    parser.add_argument(
        "--candidates",
        type=Path,
        default=DEFAULT_CANDIDATES,
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        gmethod.read_rows(args.g_v4_csv),
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

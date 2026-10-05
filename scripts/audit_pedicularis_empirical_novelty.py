from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MATRIX = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_EMPIRICAL_NOVELTY_MATRIX_V1.csv"
)
TARGET_ID = "PEDICULARIS_REGISTERED"
BINARY_FIELDS = (
    "opposing_functional_selection",
    "trait_manipulated_multilevel",
    "pollination_manipulated",
    "antagonist_manipulated",
    "factorial_P_x_G",
    "natural_trait_selection_analysis",
    "state_specific_reproductive_optima",
    "optimum_displacement_test",
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Pedicularis empirical novelty matrix has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("Pedicularis empirical novelty matrix is empty")
    ids = [row["precedent_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("precedent_id must be unique")
    return rows


def build(rows: list[dict[str, str]]) -> dict:
    targets = [row for row in rows if row["precedent_id"] == TARGET_ID]
    if len(targets) != 1:
        raise ValueError("novelty matrix must contain exactly one registered P. rex target")
    target = targets[0]
    precedents = [row for row in rows if row["precedent_id"] != TARGET_ID]

    for row in rows:
        for field in BINARY_FIELDS:
            if row[field] not in {"YES", "NO"}:
                raise ValueError(f"{row['precedent_id']}.{field} must be YES or NO")

    if not all(target[field] == "YES" for field in BINARY_FIELDS):
        raise ValueError("registered P. rex target must declare the full intended design")

    counts = {
        field: sum(row[field] == "YES" for row in precedents)
        for field in BINARY_FIELDS
    }
    factorial_ids = sorted(
        row["precedent_id"]
        for row in precedents
        if row["factorial_P_x_G"] == "YES"
    )
    full_joint_ids = sorted(
        row["precedent_id"]
        for row in precedents
        if (
            row["trait_manipulated_multilevel"] == "YES"
            and row["factorial_P_x_G"] == "YES"
            and row["state_specific_reproductive_optima"] == "YES"
            and row["optimum_displacement_test"] == "YES"
        )
    )

    return {
        "analysis": "pedicularis_empirical_novelty_boundary_v1",
        "n_close_precedents_audited": len(precedents),
        "precedent_feature_counts": counts,
        "factorial_consumer_manipulation_precedent_ids": factorial_ids,
        "n_factorial_consumer_manipulation_precedents": len(factorial_ids),
        "n_precedents_with_multilevel_trait_manipulation": counts[
            "trait_manipulated_multilevel"
        ],
        "n_precedents_with_state_specific_reproductive_optima": counts[
            "state_specific_reproductive_optima"
        ],
        "n_precedents_with_optimum_displacement_test": counts[
            "optimum_displacement_test"
        ],
        "close_precedents_with_full_joint_design": full_joint_ids,
        "bounded_design_gap_present": len(full_joint_ids) == 0,
        "allowed_novelty_statement": (
            "Among the audited close floral mutualist-antagonist precedents, "
            "factorial consumer manipulations, a multi-level floral-display optimum "
            "precedent, and an antagonist-associated floral optimum-displacement "
            "precedent exist, but none combines a randomized multi-level shared-trait "
            "manipulation with crossed selective consumer "
            "states to recover state-specific reproductive optima and test "
            "antagonist-induced optimum displacement."
        ),
        "forbidden_novelty_statements": [
            "first_study_to_manipulate_pollinators_and_antagonists",
            "first_factorial_pollinator_antagonist_experiment",
            "first_demonstration_of_conflicting_selection_on_floral_traits",
            "global_first_optimum_displacement_claim_without_systematic_review",
        ],
        "status": "BOUNDED_CLOSE_PRECEDENT_GAP_NOT_GLOBAL_FIRST_CLAIM",
        "claim_ceiling": [
            "close_precedent_audit_not_systematic_global_review",
            "novelty_attaches_to_joint_design_and_estimand_combination",
            "consumer_factorial_manipulation_itself_is_not_novel",
            "conflicting_selection_itself_is_not_novel",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(_read(args.matrix))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

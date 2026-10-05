from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAUSAL_DESIGN_COMPARATOR_V1.csv"
)

REQUIRED_COMPARATORS = {
    "HERRERA2000",
    "AGREN2013",
    "SLETVOLD2015",
    "SUN2016",
    "FITCH2021",
    "PEREZBARRALES2013",
}
PROSPECTIVE_ID = "SCH_PREX_PROSPECTIVE"

TARGET_FEATURES = (
    "trait_multilevel_randomized",
    "p_x_g_factorial",
    "common_reproductive_fitness",
    "state_specific_nonlinear_optima",
    "causal_optimum_shift_test",
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("causal-design comparator ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("causal-design comparator ledger is empty")
    return rows


def _yes(row: dict[str, str], field: str) -> bool:
    value = row[field]
    if value not in {"YES", "NO"}:
        raise ValueError(f"{field} must be YES/NO for {row['comparator_id']}")
    return value == "YES"


def build(rows: list[dict[str, str]]) -> dict:
    ids = [row["comparator_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("comparator_id must be unique")

    by_id = {row["comparator_id"]: row for row in rows}
    missing = sorted(REQUIRED_COMPARATORS - set(by_id))
    if missing:
        raise ValueError(
            "targeted comparator set missing required studies: "
            + ", ".join(missing)
        )
    if PROSPECTIVE_ID not in by_id:
        raise ValueError("prospective SCH P. rex design row is required")

    prior_rows = [by_id[key] for key in sorted(REQUIRED_COMPARATORS)]
    prospective = by_id[PROSPECTIVE_ID]

    for row in rows:
        for field in (
            "pollination_state_manipulated",
            "antagonist_state_manipulated",
            "p_x_g_factorial",
            "common_reproductive_fitness",
            "trait_multilevel_randomized",
            "state_specific_nonlinear_optima",
            "causal_optimum_shift_test",
            "evolutionary_response_measured",
            "adaptive_pollen_limitation_target",
        ):
            _yes(row, field)

    if not all(_yes(prospective, field) for field in TARGET_FEATURES):
        raise ValueError(
            "prospective P. rex design must contain the full registered "
            "multi-level z x P x G optimum-identification feature set"
        )

    prior_feature_counts = {
        row["comparator_id"]: sum(
            _yes(row, field) for field in TARGET_FEATURES
        )
        for row in prior_rows
    }
    full_matches = [
        row["comparator_id"]
        for row in prior_rows
        if all(_yes(row, field) for field in TARGET_FEATURES)
    ]

    pxg_precedents = sorted(
        row["comparator_id"]
        for row in prior_rows
        if _yes(row, "p_x_g_factorial")
    )
    trait_randomization_precedents = sorted(
        row["comparator_id"]
        for row in prior_rows
        if _yes(row, "trait_multilevel_randomized")
    )
    evolutionary_response_precedents = sorted(
        row["comparator_id"]
        for row in prior_rows
        if _yes(row, "evolutionary_response_measured")
    )
    adaptive_pollen_limitation_precedents = sorted(
        row["comparator_id"]
        for row in prior_rows
        if _yes(row, "adaptive_pollen_limitation_target")
    )

    return {
        "analysis": "pedicularis_causal_design_novelty_audit_v1",
        "targeted_comparator_ids": sorted(REQUIRED_COMPARATORS),
        "n_targeted_prior_comparators": len(prior_rows),
        "target_features": list(TARGET_FEATURES),
        "prior_target_feature_counts": dict(sorted(prior_feature_counts.items())),
        "prior_full_matching_design_ids": sorted(full_matches),
        "n_prior_full_matching_designs": len(full_matches),
        "prior_p_x_g_factorial_precedents": pxg_precedents,
        "prior_multilevel_trait_randomization_precedents": (
            trait_randomization_precedents
        ),
        "prior_evolutionary_response_precedents": (
            evolutionary_response_precedents
        ),
        "prior_adaptive_pollen_limitation_precedents": (
            adaptive_pollen_limitation_precedents
        ),
        "prospective_design_has_all_target_features": True,
        "targeted_set_design_gap": (
            "NO_MATCHING_FULL_CROSSED_OPTIMUM_DESIGN_IN_TARGETED_COMPARATOR_SET"
            if not full_matches
            else "MATCHING_DESIGN_PRESENT_IN_TARGETED_COMPARATOR_SET"
        ),
        "global_first_claim_licensed": False,
        "novelty_statement": (
            "The targeted comparator set contains precedents for P x G "
            "factorials, manipulated floral display, conflict on standing trait "
            "variation, inferred optima and evolutionary response, but no "
            "recovered prior study combines randomized multi-level focal trait "
            "variation with an independently crossed P x G design to reconstruct "
            "state-specific nonlinear optima and directly test optimum shifts on "
            "one reproductive fitness scale."
        ),
        "claim_ceiling": [
            "targeted_comparator_set_only",
            "no_global_first_claim",
            "design_combination_novelty_not_component_method_novelty",
            "prospective_design_novelty_is_not_empirical_result",
            "existing_PxG_and_evolutionary_precedents_must_be_acknowledged",
        ],
        "status": "TARGETED_DESIGN_NOVELTY_AUDIT_COMPLETE",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit whether the prospective P. rex SCH experiment combines "
            "design elements not recovered together in a fixed comparator set"
        )
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(_read(args.ledger))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

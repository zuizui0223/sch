from __future__ import annotations

"""Recover one-factor vs two-factor selection-direction reversals from the
actual 2015 Gymnadenia 2x2 treatment-cell gradients (Appendix A Table A2).

A significant signed beta in each context is NOT a covariance-aware
test of the contrast between treatment betas. Never report the
difference-in-differences as a statistically supported interaction.
"""

import argparse
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "SCH_H2_GYMNADENIA_A2_SELECTION_GRADIENTS_V1.csv"
TREATMENTS = ("C+H", "C+E", "HP+H", "HP+E")
TRAITS = (
    "plant_height",
    "number_of_flowers",
    "corolla_size",
    "spur_length",
    "flowering_start",
)
EDGES = (
    # Hold herbivory fixed, alter only open vs hand-supplemented pollination.
    ("P_ONLY_HERBIVORES_EXCLUDED", "C+E", "HP+E", "POLLINATION_SUPPLEMENTATION"),
    ("P_ONLY_NATURAL_HERBIVORY", "C+H", "HP+H", "POLLINATION_SUPPLEMENTATION"),
    # Hold pollination fixed, change only herbivore access.
    ("H_ONLY_OPEN_POLLINATION", "C+H", "C+E", "HERBIVORE_EXCLUSION"),
    ("H_ONLY_HAND_POLLINATION", "HP+H", "HP+E", "HERBIVORE_EXCLUSION"),
)
SIG = {"P_LT_0.05", "P_LT_0.01", "P_LT_0.001"}


def read(path: Path = SOURCE) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("Gymnadenia source Table A2 empty")
    return rows


def _direction(x: float) -> str:
    return "POSITIVE" if x > 0 else "NEGATIVE" if x < 0 else "ZERO"


def build(rows: list[dict[str, str]]) -> dict:
    lookup: dict[tuple[str, str], dict] = {}
    for row in rows:
        trait, treatment = row["trait"], row["treatment"]
        if trait not in TRAITS or treatment not in TREATMENTS:
            raise ValueError("unknown frozen Gymnadenia trait or treatment")
        if (trait, treatment) in lookup:
            raise ValueError("duplicate Gymnadenia treatment cell")
        if row.get("source_table") != "Table_A2":
            raise ValueError("Gymnadenia value not linked to published A2 table")
        if row["significance"] not in SIG | {"NS", "P_EQ_0.057"}:
            raise ValueError("unknown original statistical support code")
        try:
            beta, se, n = float(row["beta"]), float(row["se"]), int(row["treatment_n"])
        except (TypeError, ValueError) as exc:
            raise ValueError("Gymnadenia effect/SE/n malformed") from exc
        if not math.isfinite(beta) or not math.isfinite(se) or se <= 0 or n <= 0:
            raise ValueError("Gymnadenia requires finite beta and positive SE/n")
        lookup[(trait, treatment)] = {
            "beta": beta,
            "se": se,
            "n": n,
            "supported_nonzero_original": row["significance"] in SIG,
            "original_significance": row["significance"],
            "direction": _direction(beta),
        }
    if set(lookup) != {(t, s) for t in TRAITS for s in TREATMENTS}:
        raise ValueError("Gymnadenia Appendix A2 must contain 5 traits x 4 treatments")
    # Factorial assignment sizes are shared across trait axes.
    reference_n = {"C+H": 146, "C+E": 112, "HP+H": 117, "HP+E": 110}
    for (trait, treatment), cell in lookup.items():
        if cell["n"] != reference_n[treatment]:
            raise ValueError("Gymnadenia A2 treatment sample-size provenance drift")

    result: dict[str, dict] = {}
    for trait in TRAITS:
        cells = {t: lookup[(trait, t)] for t in TREATMENTS}
        edges = []
        for name, a, b, manipulated_axis in EDGES:
            left, right = cells[a], cells[b]
            opposed = (
                left["direction"] != right["direction"]
                and "ZERO" not in {left["direction"], right["direction"]}
            )
            both_supported = (
                opposed
                and left["supported_nonzero_original"]
                and right["supported_nonzero_original"]
            )
            edges.append({
                "edge": name,
                "single_manipulation_axis": manipulated_axis,
                "held_other_axis_fixed": True,
                "treatment_A": a,
                "treatment_B": b,
                "beta_A": left["beta"],
                "beta_B": right["beta"],
                "delta_beta_B_minus_A": right["beta"] - left["beta"],
                "point_sign_reversal": opposed,
                "both_endpoints_supported_opposite_signs": both_supported,
                "uncertainty_of_between_group_contrast_identified": False,
            })
        b = {key: cell["beta"] for key, cell in cells.items()}
        # Same 2x2 factorial double difference expressed two equivalent ways.
        did = b["C+H"] - b["C+E"] - b["HP+H"] + b["HP+E"]
        predicted_ch_additive = b["C+E"] + b["HP+H"] - b["HP+E"]
        assert math.isclose(did, b["C+H"] - predicted_ch_additive, abs_tol=1e-12)
        # Without covariance, even approximate SE of the contrast is unknown.
        result[trait] = {
            "treatment_gradients": cells,
            "single_axis_edges": edges,
            "n_single_axis_supported_opposite_sign_edges": sum(
                e["both_endpoints_supported_opposite_signs"] for e in edges
            ),
            "natural_reference_net_beta": b["C+H"],
            "additive_prediction_for_CplusH": predicted_ch_additive,
            "factorial_difference_in_differences_point": did,
            "factorial_interaction_standard_error_identified": False,
            "factorial_additivity_confirmed_statistically": False,
            "strong_sign_reversal_implies_nonadditive_selection": False,
            "trait_axis_reversal_is_not_function_optimum": True,
        }
    all_edges = [
        {"trait": trait, **e}
        for trait, item in result.items()
        for e in item["single_axis_edges"]
        if e["both_endpoints_supported_opposite_signs"]
    ]
    return {
        "analysis": "gymnadenia_2015_five_trait_factorial_selection_edge_audit_v1",
        "source_doi": "10.1890/14-0119.1",
        "source_table": "Ecological_Archives_E096_022_Appendix_A_Table_A2",
        "n_source_traits": len(TRAITS),
        "n_source_treatment_cells": len(lookup),
        "n_single_manipulation_edges_tested": len(TRAITS) * len(EDGES),
        "n_both_endpoint_supported_opposite_sign_edges": len(all_edges),
        "source_supported_single_factor_reversal_edges": all_edges,
        "trait_results": result,
        "ecological_correction": (
            "A directionally supported net-selection reversal can occur when "
            "pollination is changed alone while herbivory is held excluded; "
            "multifactor context turnover is not necessary."
        ),
        "claim_ceiling": [
            "phenotypic_selection_on_naturally_varying_traits_not_randomized_trait",
            "original_individual_cell_significance_not_multiple_test_adjusted",
            "different_cell_betas_not_a_covariance_aware_difference_test",
            "no_variance_or_p_value_for_factorial_difference_in_differences",
            "near_zero_factorial_residual_is_not_an_equivalence_test",
            "factorial_selective_gradient_not_a_function_specific_optimum",
            "single_programme_no_cross_species_reversal_rate_inference",
        ],
        "status": "REAL_SINGLE_FACTOR_SUPPORTED_SIGN_REVERSAL_RECLASSIFIED",
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, default=SOURCE)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    result = build(read(args.source))
    s = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(s, encoding="utf-8")
    else:
        print(s, end="")


if __name__ == "__main__":
    main()

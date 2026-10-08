"""Covariance-agnostic *upper* SE bounds for published Gymnadenia contrasts.

For any two coefficient estimates with reported standard errors s1, s2,
SE(beta2 - beta1) <= s1+s2 by Cauchy-Schwarz. An interval using this
worst-case SE is conservative under a joint-normal Wald approximation
even when their covariance is unavailable. It is NOT the source paper's
formal interaction test, and multiplicity remains an independent issue.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from scripts.audit_sch_gymnadenia_factorial_reversal import read, build as source_audit

NORMAL_Z_95 = 1.959963984540054
NORMAL_Z_99 = 2.5758293035489004
SOURCE_DOI = "10.1890/14-0119.1"
EXPECTED_FAMILY_SIZE = 20


def worst_case_wald(
    beta_a: float, se_a: float, beta_b: float, se_b: float
) -> dict:
    """B minus A contrast with arbitrary correlation rho in [-1, 1]."""
    vals = (beta_a, se_a, beta_b, se_b)
    if not all(math.isfinite(x) for x in vals) or se_a <= 0 or se_b <= 0:
        raise ValueError("all estimates must be finite and SE positive")
    diff = beta_b - beta_a
    se_upper = se_a + se_b
    se_lower = abs(se_a - se_b)
    z_floor = abs(diff) / se_upper
    # 2*(1-Phi(z_floor)); only an *upper* bound on the nominal Wald p.
    p_upper = math.erfc(z_floor / math.sqrt(2))
    return {
        "beta_B_minus_A": diff,
        "SE_lower_possible_arbitrary_covariance": se_lower,
        "SE_upper_Cauchy_Schwarz_sharp": se_upper,
        "worst_case_absolute_z_floor": z_floor,
        "two_sided_normal_wald_p_upper": p_upper,
        "conservative_normal_wald_95_interval": [
            diff - NORMAL_Z_95 * se_upper,
            diff + NORMAL_Z_95 * se_upper,
        ],
        "conservative_normal_wald_99_interval": [
            diff - NORMAL_Z_99 * se_upper,
            diff + NORMAL_Z_99 * se_upper,
        ],
        "95pct_sign_certified_given_joint_normality_and_valid_SEs": (
            abs(diff) > NORMAL_Z_95 * se_upper
        ),
        "99pct_sign_certified_given_joint_normality_and_valid_SEs": (
            abs(diff) > NORMAL_Z_99 * se_upper
        ),
        "actual_covariance_and_exact_p_value_identified": False,
        "uncertainty_reference": (
            "Sharp maximal contrast SE over correlations [-1,1]; "
            "normal Wald approximation, no source-level covariance recovered."
        ),
    }


def build(rows: list[dict[str, str]]) -> dict:
    prior = source_audit(rows)
    if prior["source_doi"] != SOURCE_DOI or prior["n_source_treatment_cells"] != 20:
        raise ValueError("needs original Gymnadenia 5x4 published source table")
    edge_items: list[dict] = []
    for trait, item in prior["trait_results"].items():
        for edge in item["single_axis_edges"]:
            a = item["treatment_gradients"][edge["treatment_A"]]
            b = item["treatment_gradients"][edge["treatment_B"]]
            stats = worst_case_wald(a["beta"], a["se"], b["beta"], b["se"])
            edge_items.append({
                "trait": trait,
                "edge": edge["edge"],
                "treatment_A": edge["treatment_A"],
                "treatment_B": edge["treatment_B"],
                "single_manipulation_axis": edge["single_manipulation_axis"],
                "cell_A_original_significance": a["original_significance"],
                "cell_B_original_significance": b["original_significance"],
                "both_cells_originally_supported_opposite_signs": (
                    edge["both_endpoints_supported_opposite_signs"]
                ),
                **stats,
                # Correct multiplicity only as conditional bounds; no
                # individual significance declaration for selected edges.
                "p_upper_Bonferroni_4_edges_within_trait": min(
                    1., stats["two_sided_normal_wald_p_upper"] * 4
                ),
                "p_upper_Bonferroni_all_20_exploratory_edges": min(
                    1., stats["two_sided_normal_wald_p_upper"] *
                    EXPECTED_FAMILY_SIZE
                ),
            })
    if len(edge_items) != EXPECTED_FAMILY_SIZE:
        raise ValueError("source factorial does not have 20 single-factor edges")
    nominal = [
        edge for edge in edge_items
        if edge["95pct_sign_certified_given_joint_normality_and_valid_SEs"]
    ]
    within_family = [
        edge for edge in edge_items
        if edge["p_upper_Bonferroni_4_edges_within_trait"] < 0.05
    ]
    across_family = [
        edge for edge in edge_items
        if edge["p_upper_Bonferroni_all_20_exploratory_edges"] < 0.05
    ]

    # Four signed-cell SEs bound even the factorial interaction's SE,
    # but that wide bound is not evidence for near-zero interaction.
    factorial = {}
    for trait, item in prior["trait_results"].items():
        cell_se_sum = sum(
            entry["se"] for entry in item["treatment_gradients"].values()
        )
        did = item["factorial_difference_in_differences_point"]
        factorial[trait] = {
            "DID_point": did,
            "DID_SE_upper_arbitrary_four_cell_covariance": cell_se_sum,
            "conservative_normal_wald_95_interval": [
                did - NORMAL_Z_95 * cell_se_sum,
                did + NORMAL_Z_95 * cell_se_sum,
            ],
            "factorial_interaction_certified_nonzero_from_source_SEs": (
                abs(did) > NORMAL_Z_95 * cell_se_sum
            ),
            "additivity_equivalence_certified": False,
        }
    return {
        "analysis": "gymnadenia_2015_covariance_robust_single_factor_gradient_contrasts_v1",
        "source_doi": SOURCE_DOI,
        "source_table": "E096-022_A2_FROZEN_20_CELLS",
        "n_traits": 5,
        "n_single_factor_edges": len(edge_items),
        "method": "Cauchy-Schwarz sharp covariance worst-case SE plus normal Wald sensitivity",
        "edges": edge_items,
        "n_unadjusted_covariance_robust_95pct_sign_edges": len(nominal),
        "unadjusted_covariance_robust_95pct_sign_edges": [
            {"trait": x["trait"], "edge": x["edge"]}
            for x in nominal
        ],
        "n_covariance_robust_sign_edges_Bonferroni_within_trait_four": len(within_family),
        "n_covariance_robust_sign_edges_Bonferroni_exploratory_family_twenty": len(across_family),
        "factorial_interaction_bounds_by_trait": factorial,
        "revised_boundary": (
            "Unknown contrast covariance does not automatically prevent "
            "a conservative sign test; for flowering-start C+E vs HP+E, "
            "a covariance-worst-case normal-Wald bound stays nonzero at 95% "
            "and 99%, but the all-20 exploratory family-wise threshold is "
            "not passed."
        ),
        "claim_ceiling": [
            "nominal_normal_Wald_bounds_are_conditional_on_valid_comparable_SEs",
            "not_an_exact_joint_covariance_or_the_original_authors_ANCOVA_p",
            "20_edges_examined_post_outcome_so_family_wide_adjustment_matters",
            "4_within_trait_adjustment_not_preregistered_before_source_exposure",
            "significant_beta_contrast_does_not_equal_identified_causal_trait_optimum",
            "no_four_cell_additivity_equivalence_or_interaction_test_without_more_data",
            "one_biological_programme_not_20_independent_systems",
        ],
        "status": "CONSERVATIVE_CONTRAST_BOUND_RECOVERED_LIMITED_INFERENCE",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = build(read())
    content = json.dumps(output, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

from copy import deepcopy
import math

import pytest

from scripts.audit_sch_gymnadenia_covariance_robust_contrasts import (
    NORMAL_Z_95, build, worst_case_wald,
)
from scripts.audit_sch_gymnadenia_factorial_reversal import read


def test_unknown_covariance_still_certifies_one_nominal_single_factor_sign_change():
    result = build(read())
    assert result["n_traits"] == 5
    assert result["n_single_factor_edges"] == 20
    assert result["n_unadjusted_covariance_robust_95pct_sign_edges"] == 1
    assert result["unadjusted_covariance_robust_95pct_sign_edges"] == [
        {"trait": "flowering_start", "edge": "P_ONLY_HERBIVORES_EXCLUDED"}
    ]
    edge = next(
        x for x in result["edges"]
        if (x["trait"], x["edge"]) == (
            "flowering_start", "P_ONLY_HERBIVORES_EXCLUDED"
        )
    )
    assert edge["treatment_A"] == "C+E"
    assert edge["treatment_B"] == "HP+E"
    assert edge["beta_B_minus_A"] == pytest.approx(-0.16)
    assert edge["SE_upper_Cauchy_Schwarz_sharp"] == pytest.approx(.059)
    assert edge["worst_case_absolute_z_floor"] == pytest.approx(.16 / .059)
    assert edge["conservative_normal_wald_95_interval"] == pytest.approx([
        -.16 - NORMAL_Z_95 * .059,
        -.16 + NORMAL_Z_95 * .059,
    ])
    assert edge["95pct_sign_certified_given_joint_normality_and_valid_SEs"]
    assert edge["99pct_sign_certified_given_joint_normality_and_valid_SEs"]
    assert .006 < edge["two_sided_normal_wald_p_upper"] < .007
    assert edge["actual_covariance_and_exact_p_value_identified"] is False
    assert edge["both_cells_originally_supported_opposite_signs"]


def test_multiple_comparison_caveat_changes_family_wide_claim():
    result = build(read())
    assert result["n_covariance_robust_sign_edges_Bonferroni_within_trait_four"] == 1
    assert result["n_covariance_robust_sign_edges_Bonferroni_exploratory_family_twenty"] == 0
    edge = next(
        x for x in result["edges"]
        if x["trait"] == "flowering_start"
        and x["edge"] == "P_ONLY_HERBIVORES_EXCLUDED"
    )
    assert edge["p_upper_Bonferroni_4_edges_within_trait"] < .05
    assert edge["p_upper_Bonferroni_all_20_exploratory_edges"] > .05
    assert "20_edges_examined_post_outcome_so_family_wide_adjustment_matters" in (
        result["claim_ceiling"]
    )


def test_an_unsupported_spur_switch_is_not_certified_by_se_inequality():
    result = build(read())
    edge = next(x for x in result["edges"]
                if x["trait"] == "spur_length"
                and x["edge"] == "P_ONLY_HERBIVORES_EXCLUDED")
    assert edge["beta_B_minus_A"] == pytest.approx(-.119)
    assert edge["SE_upper_Cauchy_Schwarz_sharp"] == pytest.approx(.064)
    assert edge["conservative_normal_wald_95_interval"][0] < 0
    assert edge["conservative_normal_wald_95_interval"][1] > 0
    assert edge["95pct_sign_certified_given_joint_normality_and_valid_SEs"] is False


def test_factorial_additivity_still_unresolved_even_with_covariance_bound():
    r = build(read())["factorial_interaction_bounds_by_trait"]
    phen = r["flowering_start"]
    assert phen["DID_point"] == pytest.approx(-.0042)
    assert phen["DID_SE_upper_arbitrary_four_cell_covariance"] == pytest.approx(
        .054 + .031 + .056 + .028
    )
    assert phen["conservative_normal_wald_95_interval"][0] < 0
    assert phen["conservative_normal_wald_95_interval"][1] > 0
    assert phen["factorial_interaction_certified_nonzero_from_source_SEs"] is False
    assert phen["additivity_equivalence_certified"] is False
    assert all(
        not cell["factorial_interaction_certified_nonzero_from_source_SEs"]
        for cell in r.values()
    )


def test_se_sum_bound_is_sharp_at_perfect_negative_correlation():
    s_a, s_b = .031, .028
    bound = worst_case_wald(.094, s_a, -.066, s_b)
    variance_at_rho_minus_one = s_a ** 2 + s_b ** 2 + 2 * s_a * s_b
    assert math.sqrt(variance_at_rho_minus_one) == pytest.approx(
        bound["SE_upper_Cauchy_Schwarz_sharp"]
    )
    variance_at_rho_plus_one = (s_a-s_b)**2
    assert math.sqrt(variance_at_rho_plus_one) == pytest.approx(
        bound["SE_lower_possible_arbitrary_covariance"]
    )
    assert bound["two_sided_normal_wald_p_upper"] < 0.01


@pytest.mark.parametrize(
    ("beta_a", "se_a", "beta_b", "se_b"),
    [
        (0, 0, 1, .02),
        (0, .02, 1, 0),
        (float("nan"), .02, 1, .02),
        (0, float("inf"), 1, .02),
    ],
)
def test_covariance_bound_rejects_invalid_source_uncertainty(
    beta_a, se_a, beta_b, se_b
):
    with pytest.raises(ValueError, match="finite and SE positive"):
        worst_case_wald(beta_a, se_a, beta_b, se_b)


def test_missing_source_cell_and_mutated_sample_size_still_fail_closed():
    rows = read()
    with pytest.raises(ValueError, match="5 traits x 4"):
        build(rows[:-1])
    altered = deepcopy(rows)
    altered[0]["treatment_n"] = "44"
    with pytest.raises(ValueError, match="sample-size provenance"):
        build(altered)

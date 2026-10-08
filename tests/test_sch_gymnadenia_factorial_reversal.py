from __future__ import annotations

from copy import deepcopy
import math

import pytest

from scripts.audit_sch_gymnadenia_factorial_reversal import (
    TRAITS, EDGES, read, build,
)


def test_source_a2_recovers_single_pollination_factor_supported_direction_reversal():
    result = build(read())
    assert result["n_source_traits"] == 5
    assert result["n_source_treatment_cells"] == 20
    assert result["n_single_manipulation_edges_tested"] == 20
    assert result["n_both_endpoint_supported_opposite_sign_edges"] == 1
    edge = result["source_supported_single_factor_reversal_edges"][0]
    assert edge["trait"] == "flowering_start"
    assert edge["edge"] == "P_ONLY_HERBIVORES_EXCLUDED"
    assert edge["treatment_A"] == "C+E"
    assert edge["treatment_B"] == "HP+E"
    assert edge["beta_A"] == pytest.approx(0.094)
    assert edge["beta_B"] == pytest.approx(-0.066)
    assert edge["delta_beta_B_minus_A"] == pytest.approx(-0.160)
    assert edge["uncertainty_of_between_group_contrast_identified"] is False


def test_factorial_cancellation_and_additivity_residuals_are_point_only():
    r = build(read())["trait_results"]
    phen = r["flowering_start"]
    assert phen["treatment_gradients"]["C+H"]["beta"] == pytest.approx(-0.0042)
    assert phen["additive_prediction_for_CplusH"] == pytest.approx(0)
    assert phen["factorial_difference_in_differences_point"] == pytest.approx(-0.0042)
    assert phen["factorial_interaction_standard_error_identified"] is False
    assert phen["factorial_additivity_confirmed_statistically"] is False
    assert phen["strong_sign_reversal_implies_nonadditive_selection"] is False
    spur = r["spur_length"]
    assert spur["additive_prediction_for_CplusH"] == pytest.approx(0.202)
    assert spur["factorial_difference_in_differences_point"] == pytest.approx(-0.022)
    assert spur["natural_reference_net_beta"] == pytest.approx(0.18)
    assert spur["n_single_axis_supported_opposite_sign_edges"] == 0


def test_all_factorial_paths_reconcile_exactly_and_other_traits_are_retained():
    r = build(read())["trait_results"]
    expected = {
        "plant_height": 0.011,
        "number_of_flowers": 0.06,
        "corolla_size": 0.043,
        "spur_length": -0.022,
        "flowering_start": -0.0042,
    }
    assert set(r) == set(TRAITS)
    for trait, expected_did in expected.items():
        assert r[trait]["factorial_difference_in_differences_point"] == pytest.approx(
            expected_did, abs=1e-12
        )
        assert math.isclose(
            r[trait]["natural_reference_net_beta"],
            r[trait]["additive_prediction_for_CplusH"] + expected_did,
            abs_tol=1e-12,
        )
        assert len(r[trait]["single_axis_edges"]) == len(EDGES)


def test_one_sided_spur_switch_cannot_be_upgraded_to_supported_reversal():
    r = build(read())["trait_results"]["spur_length"]
    edge = next(e for e in r["single_axis_edges"]
                if e["edge"] == "P_ONLY_HERBIVORES_EXCLUDED")
    assert edge["point_sign_reversal"] is True
    assert edge["both_endpoints_supported_opposite_signs"] is False
    assert r["treatment_gradients"]["HP+E"]["original_significance"] == "NS"


def test_ranking_does_not_assert_trait_optimum_or_factorial_interaction_p_value():
    r = build(read())
    assert r["status"] == "REAL_SINGLE_FACTOR_SUPPORTED_SIGN_REVERSAL_RECLASSIFIED"
    assert "no_variance_or_p_value_for_factorial_difference_in_differences" in (
        r["claim_ceiling"]
    )
    assert all(
        q["trait_axis_reversal_is_not_function_optimum"]
        for q in r["trait_results"].values()
    )


@pytest.mark.parametrize(("key","value","expected_error"),[
    ("beta","nan","finite beta"),
    ("se","0","positive SE"),
    ("source_table","Synthetic_A2","source"),
    ("treatment_n","12","sample-size provenance"),
    ("significance","MADE_UP","statistical support code"),
])
def test_raw_source_table_corruption_cannot_change_status(
    key: str, value: str, expected_error: str
):
    rows=deepcopy(read())
    rows[0][key]=value
    with pytest.raises(ValueError,match=expected_error):
        build(rows)


def test_missing_or_duplicate_source_cell_fails_closed():
    rows=read()
    with pytest.raises(ValueError,match="must contain"):
        build(rows[:-1])
    with pytest.raises(ValueError,match="duplicate"):
        build(rows+[deepcopy(rows[0])])


def test_single_factor_reverse_requires_both_original_cell_signs_supported():
    rows=deepcopy(read())
    cell=next(row for row in rows
              if row["trait"]=="flowering_start" and row["treatment"]=="HP+E")
    cell["significance"]="NS"
    r=build(rows)
    assert r["n_both_endpoint_supported_opposite_sign_edges"]==0
    assert not r["source_supported_single_factor_reversal_edges"]

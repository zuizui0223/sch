from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_2015_site_heterogeneity import (
    SOURCE, _read, build,
)
from scripts.audit_pedicularis_2016_censored_predation_bounds import (
    build as missingness_build, envelope,
)


def test_six_published_site_coefficients_show_substantial_heterogeneity() -> None:
    r = build(_read(SOURCE))
    hetero = r["heterogeneity"]
    assert r["source_doi"] == "10.1093/aobpla/plv019"
    assert hetero["n_population_estimates"] == 6
    assert r["n_site_beta_negative"] == 6
    assert r["site_beta_span"] == pytest.approx(0.109)
    assert r["original_reported_site_by_treatment_chi2"] == pytest.approx(36.782)
    assert hetero["Cochran_Q_source_estimates"] == pytest.approx(30.28203777)
    assert hetero["Cochran_Q_df"] == 5
    assert hetero["I2_descriptive"] == pytest.approx(0.8348856164)
    assert hetero["DerSimonian_Laird_tau"] == pytest.approx(0.0399548994)
    assert hetero["approx_random_effect_mean_model_scale"] == pytest.approx(
        -0.0838597297
    )
    assert r["water_only_effect_identified"] is False
    assert "GLM_beta_is_not_an_absolute_predation_probability_difference" in (
        r["claim_ceiling"]
    )


def test_extreme_zhongdian_se_does_not_determine_global_site_variation() -> None:
    r = build(_read(SOURCE))
    h = r["heterogeneity"]
    no_zhong = r["leave_one_site_out_descriptive"]["Zhongdian"]
    assert r["source_Zhongdian_se_over_other_five_median"] == pytest.approx(
        0.348 / 0.017
    )
    assert no_zhong["approx_random_effect_mean_model_scale"] == pytest.approx(
        -0.0838108532
    )
    assert abs(
        no_zhong["approx_random_effect_mean_model_scale"]
        - h["approx_random_effect_mean_model_scale"]
    ) < 0.0001
    assert no_zhong["I2_descriptive"] > h["I2_descriptive"]


@pytest.mark.parametrize(
    ("site", "field", "bad_value", "expected_error"),
    [
        ("Sanba", "estimate", "-0.140", "drifted"),
        ("Zhongdian", "uncertainty_value", "0.0348", "drifted"),
        ("Deqin", "uncertainty_type", "SD", "identity changed"),
        ("Shama", "direct_freeze_eligible", "YES", "identity changed"),
    ],
)
def test_site_audit_rejects_corrupted_published_inputs(
    site: str, field: str, bad_value: str, expected_error: str
) -> None:
    rows = deepcopy(_read(SOURCE))
    match = next(
        row for row in rows
        if row.get("measurement_id", "").startswith("PRX2015_PRED_")
        and row["population_scope"] == site
    )
    match[field] = bad_value
    with pytest.raises(ValueError, match=expected_error):
        build(rows)


def test_missing_2015_site_record_cannot_be_silently_ignored() -> None:
    rows = [
        row for row in _read(SOURCE)
        if row["measurement_id"] != "PRX2015_PRED_SANBA"
    ]
    with pytest.raises(ValueError, match="incomplete"):
        build(rows)


def test_2016_missing_capsule_extremes_are_only_conditional_bounds() -> None:
    result = missingness_build(115)
    assert result["source_doi"] == "10.1093/aob/mcw097"
    low = result["scenario_bounds_for_low"][
        "bounds_if_unscorable_unit_risks_can_be_anywhere_0_to_1"
    ]
    high = result["scenario_bounds_for_high"][
        "bounds_if_unscorable_unit_risks_can_be_anywhere_0_to_1"
    ]
    assert low == pytest.approx([0.0076666667, 0.0493333333])
    assert high == pytest.approx([0.262775, 0.3044416667])
    assert result["worst_case_high_minus_low_fraction"] == pytest.approx(
        0.2134416667
    )
    assert result[
        "minimum_assessable_n_per_population_to_preserve_ranking_under_model"
    ] == 19
    assert result["worst_case_high_still_greater_than_low_under_model"] is True
    assert "hypothetical_n_not_verified_per_population" in result["assumptions"]


def test_at_the_sharp_model_limit_five_uncertain_fruits_can_mask_the_contrast() -> None:
    r18 = missingness_build(18)
    r19 = missingness_build(19)
    assert r18["worst_case_high_still_greater_than_low_under_model"] is False
    assert r19["worst_case_high_still_greater_than_low_under_model"] is True


def test_source_missing_bounds_respect_unit_interval_and_reported_limit() -> None:
    assert envelope(0.1, 20, 0)[
        "bounds_if_unscorable_unit_risks_can_be_anywhere_0_to_1"
    ] == pytest.approx([0.1, 0.1])
    with pytest.raises(ValueError, match="range"):
        envelope(0.1, 20, 6)
    with pytest.raises(ValueError, match="fraction"):
        envelope(1.5, 20, 5)
    with pytest.raises(ValueError, match="positive integer"):
        envelope(0.1, 0, 5)
    with pytest.raises(ValueError, match="must remain five"):
        missingness_build(115, 4)

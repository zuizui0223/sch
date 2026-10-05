from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_causal_design_novelty import (
    DEFAULT_LEDGER,
    PROSPECTIVE_ID,
    REQUIRED_COMPARATORS,
    _read,
    build,
)


def test_targeted_comparator_set_contains_close_precedents_without_full_match() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["n_targeted_prior_comparators"] == 6
    assert set(result["targeted_comparator_ids"]) == REQUIRED_COMPARATORS
    assert result["prior_full_matching_design_ids"] == []
    assert result["n_prior_full_matching_designs"] == 0
    assert result["targeted_set_design_gap"] == (
        "NO_MATCHING_FULL_CROSSED_OPTIMUM_DESIGN_IN_TARGETED_COMPARATOR_SET"
    )


def test_prior_art_explicitly_contains_pxg_trait_and_evolutionary_precedents() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert set(result["prior_p_x_g_factorial_precedents"]) == {
        "AGREN2013",
        "HERRERA2000",
        "SLETVOLD2015",
    }
    assert result["prior_multilevel_trait_randomization_precedents"] == [
        "FITCH2021"
    ]
    assert result["prior_evolutionary_response_precedents"] == ["AGREN2013"]
    assert result["prior_adaptive_pollen_limitation_precedents"] == [
        "FITCH2021"
    ]


def test_prospective_design_combines_all_registered_target_features() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["prospective_design_has_all_target_features"] is True
    assert set(result["target_features"]) == {
        "trait_multilevel_randomized",
        "p_x_g_factorial",
        "common_reproductive_fitness",
        "state_specific_nonlinear_optima",
        "causal_optimum_shift_test",
    }


def test_audit_never_licenses_global_first_claim() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["global_first_claim_licensed"] is False
    assert "no_global_first_claim" in result["claim_ceiling"]
    assert "design_combination_novelty_not_component_method_novelty" in (
        result["claim_ceiling"]
    )


def test_a_prior_full_match_changes_targeted_set_result() -> None:
    rows = _read(DEFAULT_LEDGER)
    prospective = next(
        row for row in rows
        if row["comparator_id"] == PROSPECTIVE_ID
    )
    edited = deepcopy(rows)
    prior = next(
        row for row in edited
        if row["comparator_id"] == "SUN2016"
    )
    for field in (
        "trait_multilevel_randomized",
        "p_x_g_factorial",
        "common_reproductive_fitness",
        "state_specific_nonlinear_optima",
        "causal_optimum_shift_test",
    ):
        prior[field] = prospective[field]

    result = build(edited)
    assert result["prior_full_matching_design_ids"] == ["SUN2016"]
    assert result["targeted_set_design_gap"] == (
        "MATCHING_DESIGN_PRESENT_IN_TARGETED_COMPARATOR_SET"
    )


def test_missing_required_comparator_fails_closed() -> None:
    rows = [
        row for row in _read(DEFAULT_LEDGER)
        if row["comparator_id"] != "AGREN2013"
    ]

    with pytest.raises(ValueError, match="missing required studies"):
        build(rows)

from __future__ import annotations

from scripts.audit_pedicularis_empirical_novelty import (
    DEFAULT_MATRIX,
    _read,
    build,
)


def test_close_precedents_include_existing_factorial_consumer_experiments() -> None:
    result = build(_read(DEFAULT_MATRIX))

    assert result["n_close_precedents_audited"] == 8
    assert result["n_factorial_consumer_manipulation_precedents"] == 2
    assert result["factorial_consumer_manipulation_precedent_ids"] == [
        "FRAGARIA_2021",
        "GYMNADENIA_2015",
    ]


def test_bounded_gap_is_multilevel_trait_by_consumer_state_optimum_design() -> None:
    result = build(_read(DEFAULT_MATRIX))

    assert result["n_precedents_with_multilevel_trait_manipulation"] == 1
    assert result["n_precedents_with_state_specific_reproductive_optima"] == 0
    assert result["n_precedents_with_optimum_displacement_test"] == 0
    assert result["close_precedents_with_full_joint_design"] == []
    assert result["bounded_design_gap_present"] is True


def test_novelty_statement_is_bounded_not_global_first() -> None:
    result = build(_read(DEFAULT_MATRIX))

    assert result["status"] == (
        "BOUNDED_CLOSE_PRECEDENT_GAP_NOT_GLOBAL_FIRST_CLAIM"
    )
    assert result["allowed_novelty_statement"].startswith(
        "Among the audited close floral mutualist-antagonist precedents"
    )
    assert "first_factorial_pollinator_antagonist_experiment" in (
        result["forbidden_novelty_statements"]
    )
    assert "consumer_factorial_manipulation_itself_is_not_novel" in (
        result["claim_ceiling"]
    )


def test_matrix_keeps_classic_conflict_and_trait_manipulation_precedents() -> None:
    rows = {row["precedent_id"]: row for row in _read(DEFAULT_MATRIX)}

    assert rows["POLEMONIUM_2001"]["opposing_functional_selection"] == "YES"
    assert rows["POLEMONIUM_2001"]["trait_manipulated_multilevel"] == "NO"
    assert rows["DALECHAMPIA_2013"]["natural_trait_selection_analysis"] == "YES"
    assert rows["CASTILLEJA_2004"]["opposing_functional_selection"] == "YES"
    assert rows["EURYA_2018"]["pollination_manipulated"] == "YES"
    assert rows["EURYA_2018"]["antagonist_manipulated"] == "YES"
    assert rows["EURYA_2018"]["state_specific_reproductive_optima"] == "NO"
    assert rows["ODONTONEMA_2021"]["trait_manipulated_multilevel"] == "YES"
    assert rows["ODONTONEMA_2021"]["pollination_manipulated"] == "NO"
    assert rows["ODONTONEMA_2021"]["antagonist_manipulated"] == "NO"
    assert rows["ODONTONEMA_2021"]["state_specific_reproductive_optima"] == "NO"
    assert rows["ODONTONEMA_2021"]["optimum_displacement_test"] == "NO"


def test_registered_target_declares_full_intended_design_only() -> None:
    rows = {row["precedent_id"]: row for row in _read(DEFAULT_MATRIX)}
    target = rows["PEDICULARIS_REGISTERED"]

    for field in (
        "opposing_functional_selection",
        "trait_manipulated_multilevel",
        "pollination_manipulated",
        "antagonist_manipulated",
        "factorial_P_x_G",
        "natural_trait_selection_analysis",
        "state_specific_reproductive_optima",
        "optimum_displacement_test",
    ):
        assert target[field] == "YES"

    assert "do not claim global first" in target["claim_boundary"].lower()

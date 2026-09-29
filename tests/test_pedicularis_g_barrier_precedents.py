from scripts.audit_pedicularis_g_barrier_precedents import build


def test_g_barrier_precedent_ledger_has_three_distinct_evidence_axes() -> None:
    result = build()

    assert result["n_precedents"] == 3
    assert result["n_species"] == 3
    assert result["evidence_axis_counts"] == {
        "POSTPOLLINATION_FRUIT_BARRIER_COMPATIBILITY": 1,
        "POSTPOLLINATION_FRUIT_LOCAL_BARRIER_EFFICACY": 1,
        "WITHIN_GENUS_POSTPOLLINATION_ATTACK_TIMING": 1,
    }


def test_timing_compatibility_and_efficacy_are_all_recovered_but_external() -> None:
    result = build()

    assert result["within_genus_postpollination_attack_timing_recovered"] is True
    assert (
        result["external_postpollination_fruit_barrier_compatibility_recovered"]
        is True
    )
    assert (
        result["external_fruit_local_barrier_efficacy_class_recovered"]
        is True
    )

    assert result["focal_P_rex_barrier_effectiveness_recovered"] is False
    assert result["focal_P_rex_barrier_selectivity_recovered"] is False
    assert result["focal_P_rex_timing_bounds_recovered"] is False


def test_cypripedium_is_compatibility_not_same_year_efficacy() -> None:
    result = build()
    assert result["cypripedium_same_year_unshielded_control_available"] is False
    assert (
        "fruit_development_compatibility_is_not_predator_reduction_effect"
        in result["claim_ceiling"]
    )


def test_chamaecrista_preserves_barrier_failure_modes() -> None:
    result = build()
    assert set(result["chamaecrista_failure_modes"]) == {
        "attack_before_fruits_large_enough_to_bag",
        "sucking_attack_through_mesh_holes",
        "efficacy_context_dependent",
    }


def test_current_g_bottleneck_is_focal_barrier_validation() -> None:
    result = build()
    assert result["current_G_method_bottleneck"] == (
        "FOCAL_P_REX_POSTPOLLINATION_BARRIER_EFFECTIVENESS_SELECTIVITY_AND_TIMING_QUALIFICATION"
    )
    assert result["status"] == (
        "G_BARRIER_CLASS_TIMING_COMPATIBILITY_EFFICACY_PRECEDENTS_RECOVERED_"
        "FOCAL_VALIDATION_STILL_REQUIRED"
    )
    assert "external_barrier_efficacy_is_not_P_rex_efficacy" in (
        result["claim_ceiling"]
    )

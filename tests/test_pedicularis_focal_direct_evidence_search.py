from scripts.audit_pedicularis_focal_direct_evidence_search import build


def test_focal_direct_search_audit_keeps_registered_gaps_open() -> None:
    result = build()

    assert result["n_search_rows"] == 12
    assert result["direct_registered_p1_recovered"] is False
    assert result["direct_registered_g_recovered"] is False
    assert result["direct_same_flower_repeatability_recovered"] is False
    assert result["direct_multi_level_p0_recovered"] is False
    assert result["status"] == (
        "FOCAL_DIRECT_EVIDENCE_SEARCHED_REGISTERED_CALIBRATION_STILL_REQUIRED"
    )


def test_jing2013_hand_pollination_is_not_promoted_without_primary_methods() -> None:
    result = build()
    assert result["p1_hand_pollination_treatment_identity_status"] == (
        "FOCAL_HAND_VS_NATURAL_REPORTED_TREATMENT_IDENTITY_UNRESOLVED"
    )
    assert "hand_pollination_is_not_relabelled_as_supplementation_without_primary_methods" in (
        result["claim_ceiling"]
    )


def test_direct_gap_set_matches_registered_focal_work() -> None:
    result = build()
    assert set(result["remaining_focal_direct_gaps"]) == {
        "P_rex_multi_level_realized_exsertion_manipulation",
        "P_rex_same_flower_repeatability",
        "P_rex_registered_pollination_supplementation_effect",
        "P_rex_independent_seed_predator_exclusion",
        "P_rex_postpollination_barrier_effectiveness_under_natural_pollination",
        "P_rex_independent_G_timing_qualification",
    }


def test_search_audit_distinguishes_recovery_from_absence_claim() -> None:
    result = build()
    assert "absence_of_recovery_is_not_proof_of_absence" in result["claim_ceiling"]


def test_g_timing_is_recovered_but_barrier_effectiveness_is_not() -> None:
    result = build()
    assert result["n_independent_g_sources_checked"] == 6
    assert result["pedicularis_postpollination_attack_timing_recovered"] is True
    assert result["pedicularis_within_genus_barrier_efficacy_recovered"] is True
    assert (
        result["pedicularis_within_genus_barrier_preserved_natural_pollination"]
        is False
    )
    assert result["focal_p_rex_barrier_effectiveness_recovered"] is False
    assert result["focal_p_rex_natural_pollination_selectivity_recovered"] is False
    assert result["focal_p_rex_g_timing_qualification_recovered"] is False
    assert (
        "within_genus_postpollination_attack_timing_is_not_barrier_effectiveness"
        in result["claim_ceiling"]
    )


def test_lapponica_closes_barrier_efficacy_class_but_not_natural_pollination_selectivity() -> None:
    result = build()
    assert result["pedicularis_within_genus_barrier_efficacy_recovered"] is True
    assert (
        "within_genus_barrier_efficacy_with_hand_pollination_is_not_natural_pollination_selectivity"
        in result["claim_ceiling"]
    )


def test_tang2011_abstract_strengthens_natural_history_but_not_direct_g() -> None:
    result = build()
    assert result["direct_registered_g_recovered"] is False
    assert "absence_of_recovery_is_not_proof_of_absence" in result["claim_ceiling"]

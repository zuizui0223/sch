from scripts.audit_pedicularis_focal_direct_evidence_search import build


def test_focal_direct_search_audit_keeps_registered_gaps_open() -> None:
    result = build()

    assert result["n_search_rows"] == 10
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
        "P_rex_independent_G_timing_window",
    }


def test_search_audit_distinguishes_recovery_from_absence_claim() -> None:
    result = build()
    assert "absence_of_recovery_is_not_proof_of_absence" in result["claim_ceiling"]

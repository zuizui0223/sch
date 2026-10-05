from scripts.audit_pedicularis_g_exploratory_candidates import build


def test_g_candidate_matrix_has_five_bounded_device_classes() -> None:
    result = build()
    assert result["n_candidates"] == 5
    assert result["priority_counts"] == {1: 2, 2: 1, 3: 1, 4: 1}


def test_first_tier_is_mesh_and_porous_tubing_without_auto_selection() -> None:
    result = build()
    assert result["first_tier_candidates"] == [
        "G_A1_FINE_MESH",
        "G_A2_POROUS_TUBING",
    ]
    assert result["automatic_method_selection"] is False


def test_local_sleeve_is_second_tier_for_timing_overlap() -> None:
    result = build()
    assert result["second_tier_candidates"] == ["G_B_LOCAL_SLEEVE"]


def test_whole_flower_mesh_and_chemical_are_fallbacks() -> None:
    result = build()
    assert result["fallback_candidates"] == [
        "G_C_WHOLE_FLOWER_MESH",
        "G_D_CHEMICAL",
    ]


def test_candidate_matrix_still_requires_focal_v4_rows() -> None:
    result = build()
    assert result["status"] == (
        "G_EXPLORATORY_CANDIDATES_DEFINED_EFFECT_TARGETS_UNFROZEN"
    )
    assert "no_candidate_declared_valid_without_focal_V4_rows" in (
        result["claim_ceiling"]
    )

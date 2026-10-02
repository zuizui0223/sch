from scripts.audit_pedicularis_primary_binary_retrieval_attempts import build


def test_retrieval_attempt_audit_covers_all_five_primary_assets() -> None:
    result = build()
    assert result["n_attempts"] == 10
    assert result["n_primary_assets_with_attempts"] == 5
    assert set(result["attempt_counts_by_asset"]) == {
        "PRIMARY_JING2013_METHODS",
        "PRIMARY_TANG2011_THESIS",
        "PRIMARY_WANG1998_PDF",
        "RAW_XIA2013_DRYAD",
        "SUPP_SUN2016_MCW097",
    }


def test_direct_gap_assets_remain_unresolved_after_current_attempts() -> None:
    result = build()
    assert result["direct_registered_p1_recovered_from_binary_attempts"] is False
    assert result["direct_registered_g_recovered_from_binary_attempts"] is False
    assert result["broad_screening_should_resume"] is False
    assert result["status"] == (
        "PRIMARY_BINARY_RETRIEVAL_ATTEMPTS_RECORDED_DIRECT_GAPS_STILL_OPEN"
    )


def test_dryad_blocker_is_authentication_not_missing_file() -> None:
    result = build()
    assert result["dryad_file_stream_id"] == 46101
    assert result["dryad_anonymous_download_state"] == (
        "PUBLIC_FILE_IDENTITY_VERIFIED_BYTES_REQUIRE_AUTHENTICATED_ROUTE"
    )
    assert "authenticated_public_data_retrieval_is_distinct_from_literature_discovery" in (
        result["claim_ceiling"]
    )


def test_jing_treatment_identity_is_still_primary_methods_dependent() -> None:
    result = build()
    jing = result["direct_gap_asset_states"]["PRIMARY_JING2013_METHODS"]
    assert jing["gap"] == "P1"
    assert "P1_UNRESOLVED" in jing["states"]
    assert "primary" in jing["latest_allowed_action"].lower()


def test_tang_thesis_is_natural_history_stronger_not_direct_g() -> None:
    result = build()
    tang = result["direct_gap_asset_states"]["PRIMARY_TANG2011_THESIS"]
    assert tang["gap"] == "G"
    assert any("NATURAL_HISTORY" in state for state in tang["states"])
    assert all("G_RECOVERED" != state for state in tang["states"])


def test_external_prior_assets_never_change_direct_gap_state() -> None:
    result = build()
    for states in result["external_prior_only_asset_states"].values():
        assert all(
            state in {"NO_DIRECT_G_CHANGE", "NO_DIRECT_GAP_CHANGE"}
            for state in states
        )

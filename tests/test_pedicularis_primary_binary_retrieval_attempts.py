from scripts.audit_pedicularis_primary_binary_retrieval_attempts import build


def test_retrieval_attempt_audit_covers_all_five_primary_assets() -> None:
    result = build()
    assert result["n_attempts"] == 14
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
    assert "legitimate primary binary" in tang["latest_allowed_action"].lower()


def test_external_prior_assets_never_change_direct_gap_state() -> None:
    result = build()
    for states in result["external_prior_only_asset_states"].values():
        assert all(
            state in {"NO_DIRECT_G_CHANGE", "NO_DIRECT_GAP_CHANGE"}
            for state in states
        )


def test_tang_full_abstract_reduces_direct_g_expectation_without_closing_gap() -> None:
    result = build()
    tang = result["direct_gap_asset_states"]["PRIMARY_TANG2011_THESIS"]
    assert tang["n_attempts"] == 4
    assert tang["states"] == [
        "G_UNRESOLVED",
        "G_UNRESOLVED_NATURAL_HISTORY_STRONGER",
    ]


def test_wang_exact_pdf_url_is_known_even_though_binary_get_is_blocked() -> None:
    result = build()
    assert result["wang1998_exact_pdf_url"] == (
        "https://www.jipb.net/EN/article/downloadArticleFile.do"
        "?attachType=PDF&id=25287"
    )
    assert result["wang1998_direct_pdf_state"] == (
        "EXACT_URL_KNOWN_DIRECT_GET_HTTP_403"
    )
    assert result["primary_route_search_stop"]["PRIMARY_WANG1998_PDF"].startswith(
        "STOP_URL_DISCOVERY"
    )


def test_jing_primary_publisher_page_does_not_resolve_methods() -> None:
    result = build()
    assert result["jing2013_primary_page_state"] == (
        "LIVE_PUBLISHER_PREVIEW_METHODS_NOT_PUBLICLY_EXPOSED"
    )
    jing = result["direct_gap_asset_states"]["PRIMARY_JING2013_METHODS"]
    assert jing["n_attempts"] == 4
    assert "P1_UNRESOLVED" in jing["states"]
    assert result["primary_route_search_stop"]["PRIMARY_JING2013_METHODS"].startswith(
        "STOP_ABSTRACT_AND_INDEX_SEARCH"
    )


def test_tang_live_host_is_concretely_suspended() -> None:
    result = build()
    assert result["tang2011_live_host_state"] == (
        "GLOBETHESIS_REDIRECTS_TO_SUSPENDED_PAGE_NO_BINARY_LINKS"
    )
    assert result["primary_route_search_stop"]["PRIMARY_TANG2011_THESIS"].startswith(
        "STOP_GLOBETHESIS_RETRIES"
    )

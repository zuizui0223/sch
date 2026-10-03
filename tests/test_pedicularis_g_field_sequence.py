from scripts.audit_pedicularis_g_field_sequence import build


def test_g_field_sequence_covers_all_23_v4_fields() -> None:
    result = build()

    assert result["status"] == "G_FIELD_SEQUENCE_COVERS_ALL_V4_FIELDS"
    assert result["n_v4_fields"] == 23
    assert result["v4_field_coverage_complete"] is True
    assert result["phase_labels"] == {
        0: "REGISTRY_ASSIGNMENT",
        1: "ANTHESIS_BASELINE",
        2: "POLLINATION_WINDOW",
        3: "BARRIER_APPLICATION",
        4: "POST_BARRIER_INTEGRITY",
        5: "EARLY_POST_TREATMENT",
        6: "HARVEST",
    }


def test_hard_method_validity_is_detectable_before_harvest() -> None:
    result = build()

    assert set(result["hard_method_validity_fields"]) == {
        "sham_device_applied",
        "pollination_window_complete_before_barrier",
        "ovary_swollen_at_barrier",
        "barrier_covers_pollinator_entry",
        "pre_barrier_attack_present",
        "barrier_integrity_failure_present",
    }
    assert result["earliest_hard_method_validity_phase"] == 3
    assert set(result["hard_method_validity_by_phase"]) == {3, 4}
    assert "HARVEST_ENDPOINTS" in result["field_stop_priority"]


def test_pollen_grains_remain_explicit_destructive_proxy() -> None:
    result = build()
    assert result["pollen_proxy_semantics"] == {
        "collection_source": "PROXY_MATERIALIZED",
        "phase": "POLLEN_PROXY_COLLECTION",
        "destructive_or_endpoint": "DESTRUCTIVE_PROXY",
    }
    assert "pollen_proxy_provenance_must_remain_explicit" in (
        result["claim_ceiling"]
    )


def test_harvest_is_not_needed_for_early_method_invalidity() -> None:
    result = build()
    assert (
        "harvest_endpoints_are_not_needed_to_detect_early_method-invalid_flowers"
        in result["claim_ceiling"]
    )

from __future__ import annotations

from scripts.assemble_pedicularis_full_surface_readiness import assemble


def _freeze(lane: str, population: str = "P_REX_TEST", season: str = "S1") -> dict:
    return {
        "schema": "SCH_PEDICULARIS_THRESHOLD_FREEZE_V1",
        "status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
        "lane": lane,
        "population_id": population,
        "season_id": season,
    }


def _receipt(schema: str, status: str, lane: str, population: str = "P_REX_TEST", season: str = "S1") -> dict:
    return {
        "receipt_schema_version": schema,
        "status": status,
        "population_id": population,
        "season_id": season,
        "config_freeze": _freeze(lane, population, season),
    }


def _z() -> dict:
    receipt = _receipt(
        "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1",
        "PEDICULARIS_Z_MANIPULATION_VALIDATED",
        "P0",
    )
    receipt["z_levels"] = ["Z0", "Z1", "Z2", "Z3", "Z4"]
    receipt["field_allocation_verification"] = {
        "receipt_schema": "PEDICULARIS_P0_RANDOMIZED_ALLOCATION_V1",
        "allocation_identity_sha256": "a" * 64,
        "assignment_method": "SHA256_RANK_V1",
        "identity_z_assignment_match": True,
    }
    return receipt


def _p() -> dict:
    receipt = _receipt(
        "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1",
        "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED",
        "P1",
    )
    receipt["field_allocation_verification"] = {
        "receipt_schema": "PEDICULARIS_P1_RANDOMIZED_ALLOCATION_V1",
        "allocation_identity_sha256": "b" * 64,
        "identity_treatment_handling_match": True,
        "experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
    }
    return receipt


def _g() -> dict:
    receipt = _receipt(
        "SCH_PEDICULARIS_PREDATOR_METHOD_V4",
        "PEDICULARIS_PREDATOR_METHOD_VALIDATED",
        "G",
    )
    receipt["method_summary"] = {
        "exclusion_method": "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
    }
    receipt["field_allocation_verification"] = {
        "receipt_schema": "PEDICULARIS_G_CONFIRMATORY_RANDOMIZED_ALLOCATION_V1",
        "allocation_identity_sha256": "c" * 64,
        "identity_treatment_method_sham_match": True,
        "selected_candidate_id": "G_TEST",
        "selected_exclusion_method": "POST_POLLINATION_LOWER_FLOWER_SLEEVE",
    }
    receipt["gates"] = {
        "method_single_exclusion_method": True,
        "method_minimum_paired_plants": True,
        "method_minimum_flowers_per_treatment": True,
        "method_barrier_after_minimum_pollination_window": True,
        "method_barrier_before_maximum_registered_delay": True,
        "method_pollination_window_complete": True,
        "method_ovary_not_swollen_at_barrier": True,
        "method_pollinator_entry_not_covered": True,
        "method_exposed_has_sham_handling": True,
        "predator_weight_selectivity": True,
    }
    return receipt


def test_three_valid_same_context_receipts_unlock_full_surface() -> None:
    result = assemble(_z(), _p(), _g())
    assert result["receipt_schema_version"] == "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3"
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_READY"
    assert all(result["checks"].values())
    assert result["population_id"] == "P_REX_TEST"
    assert "timed independent predator" in result["unlocked_next_step"]
    assert result["water_y_requirement"] == "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE"
    assert "POLLINATOR_ACCESS_PRESERVED" in result["predator_method_requirement"]
    assert result["validated_execution"]["z_levels"] == [
        "Z0", "Z1", "Z2", "Z3", "Z4"
    ]
    assert result["validated_execution"]["p_experimental_unit"] == (
        "WITHIN_PLANT_PAIRED_FLOWERS"
    )
    assert result["validated_execution"]["g_exclusion_method"] == (
        "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
    )
    assert all(
        len(result["source_receipts"][lane]["receipt_sha256"]) == 64
        for lane in ("z", "p", "g")
    )


def test_valid_receipts_from_different_contexts_do_not_unlock_surface() -> None:
    p = _p()
    p["season_id"] = "S2"
    result = assemble(_z(), p, _g())
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["same_population_and_season"] is False
    assert result["unlocked_next_step"] is None


def test_failed_method_gate_blocks_surface() -> None:
    g = _g()
    g["gates"]["method_pollinator_entry_not_covered"] = False
    g["status"] = "PEDICULARIS_PREDATOR_METHOD_NOT_VALIDATED"
    result = assemble(_z(), _p(), g)
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["g_status"] is False


def test_predator_weight_v2_without_timing_qualification_cannot_unlock_surface() -> None:
    old_g = _receipt("SCH_PEDICULARIS_PREDATOR_WEIGHT_V2", "PEDICULARIS_PREDATOR_WEIGHT_VALIDATED", "G")
    result = assemble(_z(), _p(), old_g)
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["g_schema"] is False


def test_old_water_defence_receipt_cannot_unlock_sch_surface() -> None:
    old_g = _receipt("SCH_PEDICULARIS_ANTAGONIST_WEIGHT_V1", "PEDICULARIS_ANTAGONIST_WEIGHT_VALIDATED", "G")
    result = assemble(_z(), _p(), old_g)
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["g_schema"] is False


def test_missing_threshold_freeze_provenance_blocks_surface() -> None:
    z = _z()
    z.pop("config_freeze")
    result = assemble(z, _p(), _g())
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["z_threshold_freeze"] is False


def test_threshold_freeze_context_must_match_lane_receipt() -> None:
    p = _p()
    p["config_freeze"]["season_id"] = "S2"
    result = assemble(_z(), p, _g())
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["p_threshold_freeze"] is False


def test_missing_randomized_p0_verification_blocks_readiness() -> None:
    z = _z()
    z.pop("field_allocation_verification")
    result = assemble(z, _p(), _g())

    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["z_randomized_allocation_verified"] is False


def test_missing_randomized_p1_verification_blocks_readiness() -> None:
    p = _p()
    p.pop("field_allocation_verification")
    result = assemble(_z(), p, _g())

    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["p_randomized_allocation_verified"] is False


def test_missing_randomized_g_verification_blocks_readiness() -> None:
    g = _g()
    g.pop("field_allocation_verification")
    result = assemble(_z(), _p(), g)

    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["g_randomized_allocation_verified"] is False


def test_g_method_identity_must_match_randomized_allocation() -> None:
    g = _g()
    g["field_allocation_verification"]["selected_exclusion_method"] = (
        "DIFFERENT_METHOD"
    )
    result = assemble(_z(), _p(), g)

    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["g_randomized_allocation_verified"] is False

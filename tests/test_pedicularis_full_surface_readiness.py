from __future__ import annotations

from scripts.assemble_pedicularis_full_surface_readiness import assemble


def _receipt(schema: str, status: str, population: str = "P_REX_TEST", season: str = "S1") -> dict:
    return {"receipt_schema_version": schema, "status": status, "population_id": population, "season_id": season}


def _z() -> dict:
    return _receipt("SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1", "PEDICULARIS_Z_MANIPULATION_VALIDATED")


def _p() -> dict:
    return _receipt("SCH_PEDICULARIS_POLLINATION_WEIGHT_V1", "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED")


def _g() -> dict:
    receipt = _receipt("SCH_PEDICULARIS_PREDATOR_METHOD_V3", "PEDICULARIS_PREDATOR_METHOD_VALIDATED")
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
    old_g = _receipt("SCH_PEDICULARIS_PREDATOR_WEIGHT_V2", "PEDICULARIS_PREDATOR_WEIGHT_VALIDATED")
    result = assemble(_z(), _p(), old_g)
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["g_schema"] is False


def test_old_water_defence_receipt_cannot_unlock_sch_surface() -> None:
    old_g = _receipt("SCH_PEDICULARIS_ANTAGONIST_WEIGHT_V1", "PEDICULARIS_ANTAGONIST_WEIGHT_VALIDATED")
    result = assemble(_z(), _p(), old_g)
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["g_schema"] is False

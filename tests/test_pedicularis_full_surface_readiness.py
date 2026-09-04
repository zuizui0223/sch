from __future__ import annotations

from scripts.assemble_pedicularis_full_surface_readiness import assemble


def _receipt(schema: str, status: str, population: str = "P_REX_TEST", season: str = "S1") -> dict:
    return {
        "receipt_schema_version": schema,
        "status": status,
        "population_id": population,
        "season_id": season,
    }


def _z() -> dict:
    return _receipt("SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1", "PEDICULARIS_Z_MANIPULATION_VALIDATED")


def _p() -> dict:
    return _receipt("SCH_PEDICULARIS_POLLINATION_WEIGHT_V1", "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED")


def _g() -> dict:
    return _receipt("SCH_PEDICULARIS_ANTAGONIST_WEIGHT_V1", "PEDICULARIS_ANTAGONIST_WEIGHT_VALIDATED")


def test_three_valid_same_context_receipts_unlock_full_surface() -> None:
    result = assemble(_z(), _p(), _g())
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_READY"
    assert all(result["checks"].values())
    assert result["population_id"] == "P_REX_TEST"
    assert ">=5 realized z levels" in result["unlocked_next_step"]


def test_valid_receipts_from_different_contexts_do_not_unlock_surface() -> None:
    p = _p()
    p["season_id"] = "S2"
    result = assemble(_z(), p, _g())
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["same_population_and_season"] is False
    assert result["unlocked_next_step"] is None


def test_failed_lane_blocks_surface() -> None:
    g = _g()
    g["status"] = "PEDICULARIS_ANTAGONIST_WEIGHT_NOT_VALIDATED"
    result = assemble(_z(), _p(), g)
    assert result["status"] == "PEDICULARIS_FULL_SURFACE_NOT_READY"
    assert result["checks"]["g_status"] is False

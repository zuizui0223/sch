from __future__ import annotations

from scripts.audit_pedicularis_w1_w2_power_basis import (
    DEFAULT_LEDGER,
    _read,
    build,
)


def test_registered_w1_w2_n_is_currently_basis_blocked() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["n_basis_rows"] == 30
    assert result["n_blocking_rows"] == 21
    assert result["registered_single_scenario_n_basis_ready"] is False
    assert result["registered_power_status"] == (
        "PEDICULARIS_W1_W2_POWER_BASIS_BLOCKED"
    )


def test_no_causal_geometry_row_is_ready_for_registered_n() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["n_geometry_rows"] == 12
    assert result["n_geometry_rows_ready_for_registered_n"] == 0

    blockers = set(result["blocking_config_paths"])
    assert "generating_model.state_fitness_surfaces.P0G0" in blockers
    assert "generating_model.state_fitness_surfaces.P1G0" in blockers
    assert "generating_model.state_fitness_surfaces.P0G1" in blockers
    assert "generating_model.state_fitness_surfaces.P1G1" in blockers
    assert "generating_model.pollen_state_models.P1G0" in blockers
    assert "generating_model.pollen_state_models.P1G1" in blockers


def test_external_focal_data_remain_sensitivity_context_only() -> None:
    result = build(_read(DEFAULT_LEDGER))
    rows = {
        row["config_path"]: row
        for row in _read(DEFAULT_LEDGER)
    }

    assert result["n_external_or_direction_only_rows"] == 8
    assert rows["generating_model.ovule_count"][
        "current_status"
    ] == "EXTERNAL_SENSITIVITY_ONLY"
    assert rows["generating_model.state_fitness_surfaces.P1G1"][
        "current_status"
    ] == "DIRECTION_ONLY_NOT_QUADRATIC_SURFACE"
    assert rows["generating_model.pollen_state_models.P1G1"][
        "current_status"
    ] == "DIRECTION_ONLY_NO_CAUSAL_MAGNITUDE"


def test_same_context_execution_inputs_are_recoverable_but_not_yet_ready() -> None:
    rows = {
        row["config_path"]: row
        for row in _read(DEFAULT_LEDGER)
    }

    assert rows["generating_model.z_levels"]["current_status"] == (
        "RECOVERABLE_AFTER_P0_FREEZE"
    )
    assert rows["generating_model.realized_z_sd"]["current_status"] == (
        "RECOVERABLE_AFTER_P0"
    )
    assert rows["generating_model.early_attack_rate_excluded"][
        "current_status"
    ] == "RECOVERABLE_AFTER_G"
    assert rows["generating_model.early_attack_rate_exposed"][
        "current_status"
    ] == "RECOVERABLE_AFTER_G"


def test_only_two_registered_resolution_routes_are_admissible() -> None:
    result = build(_read(DEFAULT_LEDGER))
    routes = {
        item["route"] for item in result["admissible_resolution_routes"]
    }

    assert routes == {
        "SEPARATE_NONCONFIRMATORY_P2_GEOMETRY_PILOT",
        "PROSPECTIVELY_FROZEN_ROBUST_MULTI_SCENARIO_ENVELOPE",
    }
    assert "single_convenient_generating_scenario_without_basis" in (
        result["inadmissible_routes"]
    )
    assert (
        "promote_observational_exsertion_selection_to_randomized_state_surface"
        in result["inadmissible_routes"]
    )


def test_zero_blocker_basis_receipt_does_not_claim_it_is_still_blocked() -> None:
    rows = _read(DEFAULT_LEDGER)
    promoted = []
    for row in rows:
        out = dict(row)
        if out["blocking_for_registered_n"] == "YES":
            out["current_status"] = "DIRECT_SAME_CONTEXT_READY"
            out["direct_registered_n_eligible"] = "YES"
        promoted.append(out)

    result = build(promoted)

    assert result["n_blocking_rows"] == 0
    assert result["registered_single_scenario_n_basis_ready"] is True
    assert result["registered_power_status"] == (
        "PEDICULARIS_W1_W2_POWER_BASIS_READY_FOR_REGISTERED_N"
    )
    assert "support a registered single-scenario" in result["interpretation"]
    assert "no_registered_W1_W2_n_yet" not in result["claim_ceiling"]
    assert "basis_ready_does_not_itself_choose_or_register_n" in (
        result["claim_ceiling"]
    )

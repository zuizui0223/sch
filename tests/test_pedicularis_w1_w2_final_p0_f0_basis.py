from __future__ import annotations

from copy import deepcopy

import pytest

from scripts import audit_pedicularis_w1_w2_power_basis as basis
from scripts.bind_pedicularis_w1_w2_p0_f0_config import build as bind_final
from scripts.build_pedicularis_p0_randomized_assignment import build as allocate_p0
from scripts.evaluate_pedicularis_stage_p0 import evaluate_locked
from scripts.freeze_pedicularis_full_surface_thresholds import build as freeze_surface
from scripts.materialize_pedicularis_w1_w2_final_p0_f0_basis import materialize
from scripts.pedicularis_config_freeze import (
    FREEZE_SCHEMA,
    FREEZE_STATUS,
    required_gate_paths,
)


GEOMETRY_GROUPS = {
    "FITNESS_VARIANCE",
    "FITNESS_GEOMETRY",
    "POLLEN_VARIANCE",
    "POLLEN_GEOMETRY",
    "INITIAL_SEED_VARIANCE",
    "INITIAL_SEED_GEOMETRY",
}


def _p0_config() -> dict:
    return {
        "prospective_freeze": {
            "schema": FREEZE_SCHEMA,
            "status": FREEZE_STATUS,
            "lane": "P0",
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "frozen_before_confirmatory_data": True,
            "frozen_at_utc": "2026-10-07T00:00:00+00:00",
            "basis_document": "SYNTHETIC_TEST_ONLY",
            "threshold_basis": {
                path: "SYNTHETIC_TEST_ONLY"
                for path in required_gate_paths("P0")
            },
        },
        "bootstrap_reps": 300,
        "random_seed": 23,
        "stage_p0": {
            "min_z_levels": 5,
            "min_flowers_per_level": 15,
            "min_plants": 15,
            "min_adjacent_exsertion_gap": 0.10,
            "max_opening_width_relative_change": 0.03,
            "max_tube_diameter_relative_change": 0.03,
            "max_bract_height_relative_change": 0.03,
            "max_lower_lip_angle_change_deg": 2.0,
            "max_water_depth_change": 0.15,
            "max_flower_orientation_change_deg": 2.0,
            "max_mechanical_damage_rate": 0.05,
        },
    }


def _p0_packet() -> tuple[list[dict[str, str]], dict]:
    manifest = [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower}",
        }
        for plant in range(20)
        for flower in range(5)
    ]
    levels = [
        {
            "assigned_z_level": f"Z{rank}",
            "assigned_z_rank": str(rank),
            "manipulation_setting_id": f"SETTING_Z{rank}",
            "manipulation_setting_spec": f"BEND_FIX_SPEC_Z{rank}",
            "sham_control": "1" if rank == 4 else "0",
        }
        for rank in range(5)
    ]
    allocations, allocation_receipt = allocate_p0(
        manifest,
        levels,
        "FINAL-THREE-P0-SEED",
    )

    rows = []
    for alloc in allocations:
        rank = int(alloc["assigned_z_rank"])
        plant = int(alloc["plant_id"][1:])
        plant_shift = (plant % 4) * 0.001
        z = 0.20 + 0.15 * rank + plant_shift
        rows.append(
            {
                "population_id": alloc["population_id"],
                "season_id": alloc["season_id"],
                "plant_id": alloc["plant_id"],
                "flower_id": alloc["flower_id"],
                "assigned_z_level": alloc["assigned_z_level"],
                "assigned_z_rank": alloc["assigned_z_rank"],
                "manipulation_setting_id": alloc["manipulation_setting_id"],
                "sham_control": alloc["sham_control"],
                "realized_exsertion": f"{z:.4f}",
                "corolla_opening_width": f"{8.0 + plant_shift:.4f}",
                "lower_lip_angle_deg": f"{25.0 + plant_shift:.4f}",
                "tube_diameter": f"{4.0 + plant_shift:.4f}",
                "bract_height": f"{20.0 + plant_shift:.4f}",
                "water_depth": f"{5.0 + plant_shift:.4f}",
                "flower_orientation_deg": f"{15.0 + plant_shift:.4f}",
                "mechanical_damage": "0",
                "pollinator_visits": f"{2.0 + 0.5 * rank:.4f}",
                "pollen_grains": f"{8.0 + 2.0 * rank:.4f}",
            }
        )

    receipt = evaluate_locked(rows, _p0_config(), allocation_receipt)
    assert receipt["status"] == "PEDICULARIS_Z_MANIPULATION_VALIDATED"
    return rows, receipt


def _surface_config() -> dict:
    return {
        "sch_surface": {
            "bootstrap_reps": 300,
            "random_seed": 41,
            "min_z_levels": 5,
            "min_valid_bootstrap_fraction": 0.8,
            "min_interior_bootstrap_fraction": 0.9,
            "min_optimum_separation": 0.10,
            "min_optimum_shift": 0.05,
            "min_abs_component_gradient": 0.05,
        },
        "system_checks": {
            "max_water_depth_range": 0.1,
            "max_mechanical_damage_rate": 0.05,
        },
        "status": "PEDICULARIS_FULL_SURFACE_CONFIG_PROSPECTIVELY_FROZEN",
    }


def _surface_freeze(config: dict | None = None) -> dict:
    config = _surface_config() if config is None else config
    freeze = {
        "schema": "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_V1",
        "status": "PEDICULARIS_FULL_SURFACE_THRESHOLDS_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_at_utc": "2026-10-07T00:00:00+00:00",
        "basis_document": "SYNTHETIC_TEST_ONLY",
        "frozen_before_geometry_outcomes": True,
        "frozen_before_full_surface_outcomes": True,
        "threshold_basis": {
            "sch_surface.min_z_levels": "registered minimum five-level design",
            "sch_surface.min_valid_bootstrap_fraction": "registered bootstrap quality rule",
            "sch_surface.min_interior_bootstrap_fraction": "prospective stability rule",
            "sch_surface.min_optimum_separation": "prospective biological effect threshold",
            "sch_surface.min_optimum_shift": "prospective biological effect threshold",
            "sch_surface.min_abs_component_gradient": "prospective biological effect threshold",
        },
    }
    return freeze_surface(config, freeze)


def _geometry_ready_ledger() -> list[dict[str, str]]:
    rows = basis._read(basis.DEFAULT_LEDGER)
    updated = []
    for row in rows:
        out = dict(row)
        if row["field_group"] in GEOMETRY_GROUPS:
            out["current_status"] = "DIRECT_SAME_CONTEXT_READY"
            out["direct_registered_n_eligible"] = "YES"
            out["current_source"] = "SYNTHETIC_PRECISION_QUALIFIED_GEOMETRY"
        updated.append(out)
    audit = basis.build(updated)
    assert set(audit["blocking_config_paths"]) == {
        "generating_model.z_levels",
        "generating_model.realized_z_sd",
        "production_surface_config.sch_surface.*",
    }
    return updated


def _materialized():
    p0_rows, p0_receipt = _p0_packet()
    config = _surface_config()
    freeze = _surface_freeze(config)
    ledger, receipt = materialize(
        _geometry_ready_ledger(),
        p0_rows,
        p0_receipt,
        config,
        freeze,
    )
    return p0_rows, p0_receipt, config, freeze, ledger, receipt


def test_final_three_materialization_closes_three_to_zero_blockers() -> None:
    _, _, _, _, ledger, receipt = _materialized()
    audit = basis.build(ledger)

    assert receipt["n_paths_promoted"] == 3
    assert receipt["remaining_blockers"] == []
    assert audit["n_blocking_rows"] == 0
    assert audit["registered_single_scenario_n_basis_ready"] is True
    assert receipt["registered_single_scenario_n_basis_ready"] is True

    values = receipt["resolved_power_inputs"]
    assert values["generating_model.z_levels"] == pytest.approx(
        [0.2015, 0.3515, 0.5015, 0.6515, 0.8015]
    )
    assert values["generating_model.realized_z_sd"] > 0
    assert values["production_surface_config.sch_surface"] == (
        _surface_config()["sch_surface"]
    )


def test_materialization_rejects_p0_raw_data_changed_after_validation() -> None:
    p0_rows, p0_receipt = _p0_packet()
    changed = deepcopy(p0_rows)
    changed[0]["realized_exsertion"] = str(
        float(changed[0]["realized_exsertion"]) + 0.01
    )
    config = _surface_config()

    with pytest.raises(ValueError, match="validated P0 data fingerprint"):
        materialize(
            _geometry_ready_ledger(),
            changed,
            p0_receipt,
            config,
            _surface_freeze(config),
        )


def test_surface_threshold_freeze_must_precede_geometry_outcomes() -> None:
    config = _surface_config()
    freeze = {
        "schema": "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_V1",
        "status": "PEDICULARIS_FULL_SURFACE_THRESHOLDS_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_at_utc": "2026-10-07T00:00:00+00:00",
        "basis_document": "SYNTHETIC_TEST_ONLY",
        "frozen_before_geometry_outcomes": False,
        "frozen_before_full_surface_outcomes": True,
        "threshold_basis": {
            "sch_surface.min_z_levels": "x",
            "sch_surface.min_valid_bootstrap_fraction": "x",
            "sch_surface.min_interior_bootstrap_fraction": "x",
            "sch_surface.min_optimum_separation": "x",
            "sch_surface.min_optimum_shift": "x",
            "sch_surface.min_abs_component_gradient": "x",
        },
    }

    with pytest.raises(ValueError, match="before geometry outcomes"):
        freeze_surface(config, freeze)


def test_surface_threshold_freeze_rejects_unresolved_config() -> None:
    config = _surface_config()
    config["sch_surface"]["min_optimum_shift"] = "REQUIRED_BEFORE_USE"

    with pytest.raises(ValueError, match="must be numeric"):
        _surface_freeze(config)


def test_exact_p0_f0_power_binding_accepts_materialized_values() -> None:
    _, _, config, freeze, _, materialization = _materialized()
    basis_receipt = materialization["basis_audit_after_materialization"]
    values = materialization["resolved_power_inputs"]
    power_config = {
        "schema": "PEDICULARIS_W1_W2_POWER_CONFIG_V1",
        "status": "PEDICULARIS_W1_W2_POWER_INPUTS_PROSPECTIVELY_FROZEN",
        "planning_provenance": {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
        },
        "generating_model": {
            "z_levels": values["generating_model.z_levels"],
            "realized_z_sd": values["generating_model.realized_z_sd"],
        },
        "production_surface_config": {
            "sch_surface": values["production_surface_config.sch_surface"],
            "system_checks": config["system_checks"],
        },
    }

    binding = bind_final(
        power_config,
        materialization,
        basis_receipt,
        freeze,
    )

    assert binding["status"] == "PEDICULARIS_W1_W2_P0_F0_CONFIG_EXACTLY_BOUND"
    assert binding["all_final_three_paths_match"] is True
    assert all(binding["path_checks"].values())
    assert len(binding["analysis_config_sha256"]) == 64


def test_p0_f0_power_binding_rejects_z_grid_drift() -> None:
    _, _, config, freeze, _, materialization = _materialized()
    basis_receipt = materialization["basis_audit_after_materialization"]
    values = materialization["resolved_power_inputs"]
    changed_z = list(values["generating_model.z_levels"])
    changed_z[-1] += 0.01
    power_config = {
        "schema": "PEDICULARIS_W1_W2_POWER_CONFIG_V1",
        "status": "PEDICULARIS_W1_W2_POWER_INPUTS_PROSPECTIVELY_FROZEN",
        "planning_provenance": {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
        },
        "generating_model": {
            "z_levels": changed_z,
            "realized_z_sd": values["generating_model.realized_z_sd"],
        },
        "production_surface_config": {
            "sch_surface": values["production_surface_config.sch_surface"],
            "system_checks": config["system_checks"],
        },
    }

    with pytest.raises(ValueError, match="generating_model.z_levels"):
        bind_final(
            power_config,
            materialization,
            basis_receipt,
            freeze,
        )


def test_p0_f0_power_binding_rejects_threshold_drift() -> None:
    _, _, config, freeze, _, materialization = _materialized()
    basis_receipt = materialization["basis_audit_after_materialization"]
    values = materialization["resolved_power_inputs"]
    changed_surface = deepcopy(
        values["production_surface_config.sch_surface"]
    )
    changed_surface["min_optimum_shift"] += 0.01
    power_config = {
        "schema": "PEDICULARIS_W1_W2_POWER_CONFIG_V1",
        "status": "PEDICULARIS_W1_W2_POWER_INPUTS_PROSPECTIVELY_FROZEN",
        "planning_provenance": {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
        },
        "generating_model": {
            "z_levels": values["generating_model.z_levels"],
            "realized_z_sd": values["generating_model.realized_z_sd"],
        },
        "production_surface_config": {
            "sch_surface": changed_surface,
            "system_checks": config["system_checks"],
        },
    }

    with pytest.raises(ValueError, match="production_surface_config.sch_surface"):
        bind_final(
            power_config,
            materialization,
            basis_receipt,
            freeze,
        )

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import pytest

from scripts.assemble_pedicularis_f0_configs import (
    ASSEMBLY_INPUT_STATUS,
    ASSEMBLY_SCHEMA,
    ASSEMBLY_STATUS,
    DEFAULT_TEMPLATES,
    assemble,
)
from scripts.freeze_pedicularis_cal_a_targets import EXPECTED as CAL_A_EXPECTED
from scripts.freeze_pedicularis_cal_b_targets import EXPECTED as CAL_B_EXPECTED
from scripts.pedicularis_config_freeze import (
    FREEZE_STATUS,
    required_gate_paths,
    validate_prospective_freeze,
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _cal_a_receipt(
    population: str = "P_REX_TEST",
    season: str = "S1",
) -> dict:
    targets = {gate: 0.20 for gate in CAL_A_EXPECTED}
    decisions = [
        {
            "gate_path": gate,
            "target_value": value,
            "target_basis_note": f"UNIT_TEST_CAL_A_{gate}",
        }
        for gate, value in sorted(targets.items())
    ]
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_CAL_A_TARGET_FREEZE_V1",
        "population_id": population,
        "season_id": season,
        "targets": targets,
        "decision_rows": decisions,
        "status": "PEDICULARIS_CAL_A_TARGETS_FROZEN",
    }


def _cal_b_receipt(
    population: str = "P_REX_TEST",
    season: str = "S1",
) -> dict:
    targets = {}
    for gate, (_, kind) in CAL_B_EXPECTED.items():
        if kind == "TIMING_LOWER_BOUND":
            targets[gate] = 8.0
        elif kind == "TIMING_UPPER_BOUND":
            targets[gate] = 24.0
        else:
            targets[gate] = 0.10
    decisions = [
        {
            "gate_path": gate,
            "target_value": value,
            "target_basis_note": f"UNIT_TEST_CAL_B_{gate}",
        }
        for gate, value in sorted(targets.items())
    ]
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_CAL_B_TARGET_FREEZE_V1",
        "population_id": population,
        "season_id": season,
        "targets": targets,
        "decision_rows": decisions,
        "status": "PEDICULARIS_CAL_B_TARGETS_FROZEN",
    }


def _cal_c_plan(
    population: str = "P_REX_TEST",
    season: str = "S1",
) -> dict:
    lane_plans = {}
    for lane, plants, flowers, driver in (
        ("P0", 24, 120, "P0_Z_GAP"),
        ("P1", 30, 60, "P1_INITIAL_SEED"),
        ("G", 36, 72, "G_PREDATION"),
    ):
        lane_plans[lane] = {
            "required_plants": plants,
            "required_flowers_per_cell": flowers,
            "driving_criteria": [driver],
            "design_effect": 1.25,
            "design_effect_basis": "UNIT_TEST_DESIGN_EFFECT_BASIS",
            "flowers_per_plant_per_cell": 2 if lane != "P0" else 5,
            "flowers_per_plant_per_cell_basis": "UNIT_TEST_FLOWER_COUNT_BASIS",
        }
        if lane == "P1":
            lane_plans[lane]["design_unit"] = (
                "WITHIN_PLANT_PAIRED_FLOWERS"
            )
            lane_plans[lane]["design_unit_basis"] = (
                "UNIT_TEST_P1_DESIGN_BASIS"
            )

    return {
        "analysis": "pedicularis_cal_c_sample_size_plan_v1",
        "planning_provenance": {
            "status": "PEDICULARIS_CAL_C_INPUTS_PROSPECTIVELY_FROZEN",
            "population_id": population,
            "season_id": season,
            "frozen_before_confirmatory_data": True,
            "basis_document": "UNIT_TEST_CAL_C_BASIS_DOCUMENT",
        },
        "familywise_target_power": 0.80,
        "familywise_target_power_basis": "UNIT_TEST_FAMILYWISE_POWER_BASIS",
        "p1_design_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
        "p1_design_unit_basis": "UNIT_TEST_P1_DESIGN_BASIS",
        "lane_plans": lane_plans,
        "sample_size_gate_values": {
            "stage_p0.min_plants": 24,
            "stage_p0.min_flowers_per_level": 120,
            "pollination_weight.min_plant_units_per_treatment": 30,
            "pollination_weight.min_flowers_per_treatment": 60,
            "method_gate.min_paired_plants": 36,
            "method_gate.min_flowers_per_treatment": 72,
            "predator_weight.min_paired_plants": 36,
            "predator_weight.min_flowers_per_treatment": 72,
        },
        "status": "PEDICULARIS_CAL_C_SAMPLE_SIZE_PLAN_READY",
    }


def _p1_design_receipt(
    population: str = "P_REX_TEST",
    season: str = "S1",
    design_unit: str = "WITHIN_PLANT_PAIRED_FLOWERS",
) -> dict:
    paired = design_unit == "WITHIN_PLANT_PAIRED_FLOWERS"
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_P1_DESIGN_FREEZE_V1",
        "status": "PEDICULARIS_P1_DESIGN_PROSPECTIVELY_FROZEN",
        "population_id": population,
        "season_id": season,
        "design_unit": design_unit,
        "treatment_assignment": (
            "PAIRED_WITHIN_PLANT"
            if paired
            else "RANDOMIZED_BETWEEN_PLANTS"
        ),
        "resource_reallocation_strategy": (
            "paired flowers retain individual blocking while acknowledging "
            "within-plant resource reallocation"
            if paired
            else "whole-plant supplementation treats the whole flowering plant "
            "to reduce within-plant resource-reallocation bias"
        ),
        "donor_protocol": "UNIT_TEST_DONOR_PROTOCOL",
        "randomization_or_matching_protocol": (
            "paired within-plant treatment assignment"
            if paired
            else "randomized between-plant treatment assignment"
        ),
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-09-28T00:00:00Z",
        "basis_document": "UNIT_TEST_P1_DESIGN_BASIS",
    }


def _assembly_config(
    population: str = "P_REX_TEST",
    season: str = "S1",
) -> dict:
    return {
        "receipt_schema_version": ASSEMBLY_SCHEMA,
        "status": ASSEMBLY_INPUT_STATUS,
        "population_id": population,
        "season_id": season,
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-09-28T00:00:00Z",
        "basis_document": "UNIT_TEST_F0_ASSEMBLY_BASIS",
    }


def _templates() -> dict[str, dict]:
    return {
        lane: _load(path)
        for lane, path in DEFAULT_TEMPLATES.items()
    }


def test_f0_assembler_closes_exactly_40_gate_fields() -> None:
    outputs, receipt = assemble(
        cal_a_receipt=_cal_a_receipt(),
        cal_b_receipt=_cal_b_receipt(),
        cal_c_plan=_cal_c_plan(),
        p1_design_receipt=_p1_design_receipt(),
        assembly_config=_assembly_config(),
        templates=_templates(),
    )

    assert receipt["status"] == ASSEMBLY_STATUS
    assert receipt["n_gate_values"] == 40
    assert receipt["source_counts"] == {
        "REGISTERED_CONTRACT": 5,
        "CAL_A": 20,
        "CAL_B": 7,
        "CAL_C": 8,
    }
    assert receipt["lane_gate_counts"] == {"P0": 11, "P1": 10, "G": 19}
    assert len(receipt["gate_sources"]) == 40
    assert receipt["p1_design_unit"] == "WITHIN_PLANT_PAIRED_FLOWERS"
    assert outputs["P1"]["pollination_design"]["design_unit"] == (
        "WITHIN_PLANT_PAIRED_FLOWERS"
    )

    for lane in ("P0", "P1", "G"):
        freeze = validate_prospective_freeze(outputs[lane], lane)
        assert freeze["status"] == FREEZE_STATUS
        assert freeze["issues"] == []
        assert freeze["population_id"] == "P_REX_TEST"
        assert freeze["season_id"] == "S1"
        assert len(outputs[lane]["prospective_freeze"]["threshold_basis"]) == len(
            required_gate_paths(lane)
        )


def test_registered_contract_values_are_not_overwritten_by_calibration() -> None:
    outputs, receipt = assemble(
        cal_a_receipt=_cal_a_receipt(),
        cal_b_receipt=_cal_b_receipt(),
        cal_c_plan=_cal_c_plan(),
        p1_design_receipt=_p1_design_receipt(),
        assembly_config=_assembly_config(),
        templates=_templates(),
    )

    assert outputs["P0"]["stage_p0"]["min_z_levels"] == 5
    assert outputs["G"]["method_gate"]["require_pollination_window_complete"] is True
    assert outputs["G"]["method_gate"]["require_ovary_not_swollen"] is True
    assert outputs["G"]["method_gate"]["require_barrier_not_cover_pollinator_entry"] is True
    assert outputs["G"]["method_gate"]["require_sham_on_exposed"] is True

    for gate in (
        "stage_p0.min_z_levels",
        "method_gate.require_pollination_window_complete",
        "method_gate.require_ovary_not_swollen",
        "method_gate.require_barrier_not_cover_pollinator_entry",
        "method_gate.require_sham_on_exposed",
    ):
        assert receipt["gate_sources"][gate] == "REGISTERED_CONTRACT"


def test_cal_a_cal_b_and_cal_c_values_land_in_correct_lane_configs() -> None:
    outputs, _ = assemble(
        cal_a_receipt=_cal_a_receipt(),
        cal_b_receipt=_cal_b_receipt(),
        cal_c_plan=_cal_c_plan(),
        p1_design_receipt=_p1_design_receipt(),
        assembly_config=_assembly_config(),
        templates=_templates(),
    )

    assert outputs["P0"]["stage_p0"]["min_adjacent_exsertion_gap"] == pytest.approx(0.20)
    assert outputs["P1"]["pollination_weight"]["min_pollen_grain_delta"] == pytest.approx(0.10)
    assert outputs["G"]["method_gate"]["min_hours_after_anthesis_before_barrier"] == pytest.approx(8.0)
    assert outputs["G"]["method_gate"]["max_hours_after_anthesis_before_barrier"] == pytest.approx(24.0)

    assert outputs["P0"]["stage_p0"]["min_plants"] == 24
    assert outputs["P1"]["pollination_weight"]["min_plant_units_per_treatment"] == 30
    assert outputs["G"]["method_gate"]["min_paired_plants"] == 36
    assert outputs["G"]["predator_weight"]["min_paired_plants"] == 36


def test_every_threshold_basis_records_its_source_layer() -> None:
    outputs, _ = assemble(
        cal_a_receipt=_cal_a_receipt(),
        cal_b_receipt=_cal_b_receipt(),
        cal_c_plan=_cal_c_plan(),
        p1_design_receipt=_p1_design_receipt(),
        assembly_config=_assembly_config(),
        templates=_templates(),
    )

    p0_basis = outputs["P0"]["prospective_freeze"]["threshold_basis"]
    p1_basis = outputs["P1"]["prospective_freeze"]["threshold_basis"]
    g_basis = outputs["G"]["prospective_freeze"]["threshold_basis"]

    assert p0_basis["stage_p0.min_z_levels"].startswith("REGISTERED_CONTRACT:")
    assert p0_basis["stage_p0.min_adjacent_exsertion_gap"].startswith("CAL_A:")
    assert p1_basis["pollination_weight.min_pollen_grain_delta"].startswith("CAL_B:")
    assert p1_basis["pollination_weight.min_plant_units_per_treatment"].startswith("CAL_C:")
    assert "driving_criteria=" in g_basis["predator_weight.min_paired_plants"]
    assert "familywise_basis=" in g_basis["predator_weight.min_paired_plants"]


def test_context_mismatch_between_sources_fails_closed() -> None:
    with pytest.raises(ValueError, match="contexts must match"):
        assemble(
            cal_a_receipt=_cal_a_receipt(),
            cal_b_receipt=_cal_b_receipt(season="S2"),
            cal_c_plan=_cal_c_plan(),
            p1_design_receipt=_p1_design_receipt(),
            assembly_config=_assembly_config(),
            templates=_templates(),
        )


def test_missing_cal_a_gate_fails_40_gate_coverage() -> None:
    receipt = _cal_a_receipt()
    gate = next(iter(receipt["targets"]))
    receipt["targets"].pop(gate)
    receipt["decision_rows"] = [
        row for row in receipt["decision_rows"] if row["gate_path"] != gate
    ]

    with pytest.raises(ValueError, match="40-gate coverage mismatch"):
        assemble(
            cal_a_receipt=receipt,
            cal_b_receipt=_cal_b_receipt(),
            cal_c_plan=_cal_c_plan(),
            p1_design_receipt=_p1_design_receipt(),
            assembly_config=_assembly_config(),
            templates=_templates(),
        )


def test_cal_c_must_supply_exactly_eight_sample_size_gates() -> None:
    plan = _cal_c_plan()
    plan["sample_size_gate_values"].pop("stage_p0.min_plants")
    with pytest.raises(ValueError, match="sample-size gate coverage mismatch"):
        assemble(
            cal_a_receipt=_cal_a_receipt(),
            cal_b_receipt=_cal_b_receipt(),
            cal_c_plan=plan,
            p1_design_receipt=_p1_design_receipt(),
            assembly_config=_assembly_config(),
            templates=_templates(),
        )


def test_assembly_freeze_timestamp_must_be_timezone_aware() -> None:
    config = _assembly_config()
    config["frozen_at_utc"] = "2026-09-28T00:00:00"
    with pytest.raises(ValueError, match="timezone-aware"):
        assemble(
            cal_a_receipt=_cal_a_receipt(),
            cal_b_receipt=_cal_b_receipt(),
            cal_c_plan=_cal_c_plan(),
            p1_design_receipt=_p1_design_receipt(),
            assembly_config=config,
            templates=_templates(),
        )


def test_f0_rejects_cal_c_and_p1_design_unit_mismatch() -> None:
    with pytest.raises(ValueError, match="design_unit does not match"):
        assemble(
            cal_a_receipt=_cal_a_receipt(),
            cal_b_receipt=_cal_b_receipt(),
            cal_c_plan=_cal_c_plan(),
            p1_design_receipt=_p1_design_receipt(
                design_unit="WHOLE_PLANT_RANDOMIZED"
            ),
            assembly_config=_assembly_config(),
            templates=_templates(),
        )


def test_f0_accepts_whole_plant_design_when_cal_c_matches() -> None:
    plan = _cal_c_plan()
    plan["p1_design_unit"] = "WHOLE_PLANT_RANDOMIZED"
    plan["lane_plans"]["P1"]["design_unit"] = (
        "WHOLE_PLANT_RANDOMIZED"
    )

    outputs, receipt = assemble(
        cal_a_receipt=_cal_a_receipt(),
        cal_b_receipt=_cal_b_receipt(),
        cal_c_plan=plan,
        p1_design_receipt=_p1_design_receipt(
            design_unit="WHOLE_PLANT_RANDOMIZED"
        ),
        assembly_config=_assembly_config(),
        templates=_templates(),
    )

    assert receipt["p1_design_unit"] == "WHOLE_PLANT_RANDOMIZED"
    assert outputs["P1"]["pollination_design"]["design_unit"] == (
        "WHOLE_PLANT_RANDOMIZED"
    )

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.analyze_pedicularis_full_surface import (
    RAW_FIELDS,
    _semantic_sha256,
    analyze,
    analyze_locked,
    surface_data_sha256,
    to_sch_rows,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_FULL_SURFACE_TEMPLATE_V2.csv"
CONFIG_TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_FULL_SURFACE_CONFIG_TEMPLATE_V2.json"
CONTRACT = ROOT / "docs" / "SCH_PEDICULARIS_FULL_SURFACE_CONTRACT_V2.md"


def _readiness(population: str = "P_REX_TEST", season: str = "S1") -> dict:
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3",
        "analysis": "pedicularis_pre_surface_readiness_timed_independent_predator_G",
        "population_id": population,
        "season_id": season,
        "status": "PEDICULARIS_FULL_SURFACE_READY",
        "checks": {
            "same_population_and_season": True,
            "z_randomized_allocation_verified": True,
            "z_levels_validated": True,
            "z_manipulation_settings_validated": True,
            "p_randomized_allocation_verified": True,
            "g_randomized_allocation_verified": True,
            "g_method_timing_validated": True,
        },
        "validated_execution": {
            "z_levels": ["Z-2", "Z-1", "Z+0", "Z+1", "Z+2"],
            "z_manipulation_settings": [
                {
                    "assigned_z_level": f"Z{z:+d}",
                    "assigned_z_rank": i,
                    "manipulation_setting_id": f"SETTING_Z{z:+d}",
                }
                for i, z in enumerate((-2, -1, 0, 1, 2))
            ],
            "p0_level_plan_sha256": "1" * 64,
            "p_experimental_unit": "WITHIN_PLANT_PAIRED_FLOWERS",
            "g_exclusion_method": "POST_POLLINATION_LOWER_FLOWER_SLEEVE",
            "g_exposed_sham_method": "SHAM_SLEEVE",
            "z_allocation_identity_sha256": "a" * 64,
            "p_allocation_identity_sha256": "b" * 64,
            "g_allocation_identity_sha256": "c" * 64,
        },
        "source_receipts": {
            "z": {
                "schema": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1",
                "status": "PEDICULARIS_Z_MANIPULATION_VALIDATED",
                "threshold_freeze_status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
                "receipt_sha256": "d" * 64,
            },
            "p": {
                "schema": "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1",
                "status": "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED",
                "threshold_freeze_status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
                "receipt_sha256": "e" * 64,
            },
            "g": {
                "schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V4",
                "status": "PEDICULARIS_PREDATOR_METHOD_VALIDATED",
                "threshold_freeze_status": "PEDICULARIS_THRESHOLDS_PROSPECTIVELY_FROZEN",
                "receipt_sha256": "f" * 64,
            },
        },
        "water_y_requirement": "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "predator_method_requirement": "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED",
    }


def _field_verification(
    rows: list[dict[str, str]],
    readiness: dict | None = None,
) -> dict:
    readiness = _readiness() if readiness is None else readiness
    return {
        "receipt_schema": "PEDICULARIS_FULL_SURFACE_FIELD_VERIFICATION_V1",
        "status": "P2_FULL_SURFACE_FIELD_PACKET_VERIFIED_COMPLETE",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "n_rows": len(rows),
        "allocation_identity_sha256": "a" * 64,
        "field_identity_sha256": "b" * 64,
        "p0_level_plan_sha256": "1" * 64,
        "readiness_receipt_sha256": _semantic_sha256(readiness),
        "surface_data_sha256": surface_data_sha256(rows),
        "identity_and_treatment_match": True,
        "canonical_outcomes_complete": True,
    }


def _config() -> dict:
    return {
        "sch_surface": {
            "bootstrap_reps": 300,
            "random_seed": 41,
            "min_z_levels": 5,
            "min_valid_bootstrap_fraction": 0.8,
            "min_interior_bootstrap_fraction": 0.9,
            "min_optimum_separation": 1.0,
            "min_optimum_shift": 0.5,
            "min_abs_component_gradient": 0.5,
        },
        "system_checks": {
            "max_water_depth_range": 0.1,
            "max_mechanical_damage_rate": 0.05,
        },
    }


def _rows(water_contaminated: bool = False) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(18):
        plant_effect = (plant % 3) * 0.02
        for z in (-2, -1, 0, 1, 2):
            for p, g in ((0, 0), (1, 0), (0, 1), (1, 1)):
                if (p, g) == (0, 0):
                    undamaged = 70.0
                elif (p, g) == (1, 0):
                    undamaged = 70.0 - (z - 2) ** 2
                elif (p, g) == (0, 1):
                    undamaged = 70.0 - (z + 2) ** 2
                else:
                    undamaged = 70.0 - (z - 2) ** 2 - (z + 2) ** 2
                undamaged += plant_effect
                damaged = float((z + 2) ** 2) if g else 0.0
                pollination = "NATURAL" if p else "SUPPLEMENTED"
                predator = "EXPOSED" if g else "EXCLUDED"
                water = 10.0 + (2.0 if (water_contaminated and g) else 0.0)
                rows.append(
                    {
                        "population_id": "P_REX_TEST",
                        "season_id": "S1",
                        "plant_id": f"P{plant:02d}",
                        "flower_id": f"P{plant:02d}_Z{z:+d}_P{p}G{g}",
                        "assigned_z_level": f"Z{z:+d}",
                        "manipulation_setting_id": f"SETTING_Z{z:+d}",
                        "realized_exsertion": str(float(z)),
                        "pollination_treatment": pollination,
                        "predator_treatment": predator,
                        "exclusion_method": "SHAM_SLEEVE" if g else "POST_POLLINATION_LOWER_FLOWER_SLEEVE",
                        "water_depth": f"{water:.3f}",
                        "ovule_count": "100",
                        "undamaged_seed_count": f"{undamaged:.5f}",
                        "damaged_seed_count": f"{damaged:.5f}",
                        "pollen_grains": str(80 + 5 * z if p else 120),
                        "early_predator_attack_present": str(g),
                        "mechanical_damage": "0",
                    }
                )
    return rows


def test_v2_template_and_config_are_registered_fail_closed_inputs() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == RAW_FIELDS
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["sch_surface"]["min_optimum_shift"] == "REQUIRED_BEFORE_USE"
    assert config["system_checks"]["max_water_depth_range"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_v2_mapping_recovers_non_circular_pedicularis_compromise_surface() -> None:
    result = analyze(_rows(), _readiness(), _config())
    assert result["status"] == "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
    assert result["system_wrapper_schema_version"] == "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2"
    assert result["surface_data_sha256"] == surface_data_sha256(_rows())
    assert result["surface_data_n_rows"] == len(_rows())
    mapping = result["pedicularis_state_mapping"]
    assert mapping["G0"] == "SEED_PREDATOR_INDEPENDENTLY_EXCLUDED"
    assert mapping["G1"] == "SEED_PREDATOR_EXPOSED"
    assert mapping["water_y"] == "HELD_FIXED_ACROSS_ALL_SCH_CELLS"
    assert result["readiness_reference"]["g_schema"] == "SCH_PEDICULARIS_PREDATOR_METHOD_V4"
    assert "POLLINATOR_ACCESS_PRESERVED" in result["readiness_reference"]["predator_method_requirement"]
    est = result["observed_estimands"]
    assert abs(est["z_pollinator_context"] - 2.0) < 1e-8
    assert abs(est["z_antagonist_context"] + 2.0) < 1e-8
    assert abs(est["z_combined"]) < 1e-8
    assert all(result["decisions"].values())
    assert result["pedicularis_system_checks"]["decisions"]["water_y_held_fixed"] is True
    secondary = result["pedicularis_secondary_outcomes"]
    assert secondary["P0G0"]["mean_predation_fraction"] == 0.0
    assert secondary["P0G1"]["mean_predation_fraction"] > 0.0


def test_v2_conversion_uses_independent_predator_G_semantics() -> None:
    converted = to_sch_rows(_rows()[:4])
    states = {(row["pollinator_state"], row["antagonist_state"]) for row in converted}
    assert states == {("0", "0"), ("1", "0"), ("0", "1"), ("1", "1")}


def test_v2_rejects_legacy_readiness_schema() -> None:
    receipt = _readiness()
    receipt["receipt_schema_version"] = "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V2"
    with pytest.raises(ValueError, match="READINESS_V3"):
        analyze(_rows(), receipt, _config())


def test_v2_rejects_predator_weight_without_method_qualification() -> None:
    receipt = _readiness()
    receipt["source_receipts"]["g"] = {
        "schema": "SCH_PEDICULARIS_PREDATOR_WEIGHT_V2",
        "status": "PEDICULARIS_PREDATOR_WEIGHT_VALIDATED",
    }
    with pytest.raises(ValueError, match="predator-method V4"):
        analyze(_rows(), receipt, _config())


def test_v2_rejects_water_y_contamination() -> None:
    with pytest.raises(ValueError, match="water-y or handling"):
        analyze(_rows(water_contaminated=True), _readiness(), _config())


def test_v2_readiness_context_mismatch_fails_closed() -> None:
    with pytest.raises(ValueError, match="match the readiness population and season"):
        analyze(_rows(), _readiness(season="S2"), _config())


def test_v2_contract_separates_independent_G_from_bita_y() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "G0 = PREDATOR_EXCLUDED" in text
    assert "water defence is held fixed" in text
    assert "non-circular" in text
    assert "R_state = |x0* - z_P*| - |x1* - z_P*|" in text


def test_v2_rejects_readiness_without_threshold_freeze_provenance() -> None:
    receipt = _readiness()
    receipt["source_receipts"]["p"].pop("threshold_freeze_status")
    with pytest.raises(ValueError, match="threshold-freeze provenance"):
        analyze(_rows(), receipt, _config())


def test_production_locked_analysis_accepts_exact_verified_surface() -> None:
    rows = _rows()
    result = analyze_locked(
        rows,
        _readiness(),
        _config(),
        _field_verification(rows),
    )

    assert result["field_execution_verification"]["identity_and_treatment_match"] is True
    assert result["field_execution_verification"]["canonical_outcomes_complete"] is True
    assert result["field_execution_verification"]["surface_data_sha256"] == (
        result["surface_data_sha256"]
    )


def test_production_locked_analysis_rejects_surface_changed_after_verify() -> None:
    rows = _rows()
    verification = _field_verification(rows)
    changed = [dict(row) for row in rows]
    changed[0]["pollen_grains"] = str(float(changed[0]["pollen_grains"]) + 1.0)

    with pytest.raises(ValueError, match="verified field-packet fingerprint"):
        analyze_locked(changed, _readiness(), _config(), verification)


def test_production_locked_analysis_rejects_identity_only_verification() -> None:
    rows = _rows()
    verification = _field_verification(rows)
    verification["status"] = "P2_FULL_SURFACE_FIELD_IDENTITY_VERIFIED"
    verification["canonical_outcomes_complete"] = False
    verification["surface_data_sha256"] = None

    with pytest.raises(ValueError, match="identity-verified and complete"):
        analyze_locked(rows, _readiness(), _config(), verification)


def test_v2_rejects_raw_z_grid_not_matching_validated_p0() -> None:
    rows = _rows()
    rows[0]["assigned_z_level"] = "UNVALIDATED_Z"

    with pytest.raises(ValueError, match="z-level labels do not match"):
        analyze(rows, _readiness(), _config())


def test_v2_rejects_raw_excluded_method_not_matching_validated_g() -> None:
    rows = _rows()
    for row in rows:
        if row["predator_treatment"] == "EXCLUDED":
            row["exclusion_method"] = "UNVALIDATED_G_METHOD"

    with pytest.raises(ValueError, match="EXCLUDED method does not match"):
        analyze(rows, _readiness(), _config())


def test_v2_rejects_readiness_without_randomized_execution_checks() -> None:
    receipt = _readiness()
    receipt["checks"]["p_randomized_allocation_verified"] = False

    with pytest.raises(ValueError, match="randomized execution checks"):
        analyze(_rows(), receipt, _config())


def test_v2_rejects_raw_physical_z_setting_not_matching_validated_p0() -> None:
    rows = _rows()
    rows[0]["manipulation_setting_id"] = "UNVALIDATED_SETTING"

    with pytest.raises(ValueError, match="physical z-manipulation settings"):
        analyze(rows, _readiness(), _config())


def test_production_locked_analysis_rejects_wrong_p0_plan_digest() -> None:
    rows = _rows()
    verification = _field_verification(rows)
    verification["p0_level_plan_sha256"] = "9" * 64

    with pytest.raises(ValueError, match="validated P0 level-plan SHA-256"):
        analyze_locked(rows, _readiness(), _config(), verification)


def test_v2_rejects_raw_exposed_sham_not_matching_validated_g() -> None:
    rows = _rows()
    for row in rows:
        if row["predator_treatment"] == "EXPOSED":
            row["exclusion_method"] = "UNVALIDATED_SHAM_METHOD"

    with pytest.raises(ValueError, match="EXPOSED sham method does not match"):
        analyze(rows, _readiness(), _config())


def test_production_locked_analysis_rejects_different_readiness_after_allocation() -> None:
    rows = _rows()
    allocated_readiness = _readiness()
    verification = _field_verification(rows, allocated_readiness)
    changed_readiness = _readiness()
    changed_readiness["validated_execution"]["p_allocation_identity_sha256"] = (
        "9" * 64
    )

    with pytest.raises(ValueError, match="exact readiness V3 receipt"):
        analyze_locked(rows, changed_readiness, _config(), verification)

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.analyze_pedicularis_full_surface_v2 import RAW_FIELDS, analyze, to_sch_rows


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
        "source_receipts": {
            "z": {"schema": "SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1", "status": "PEDICULARIS_Z_MANIPULATION_VALIDATED"},
            "p": {"schema": "SCH_PEDICULARIS_POLLINATION_WEIGHT_V1", "status": "PEDICULARIS_POLLINATION_WEIGHT_VALIDATED"},
            "g": {"schema": "SCH_PEDICULARIS_PREDATOR_METHOD_V3", "status": "PEDICULARIS_PREDATOR_METHOD_VALIDATED"},
        },
        "water_y_requirement": "HOLD_WATER_DEFENCE_FIXED_DURING_SCH_FULL_SURFACE",
        "predator_method_requirement": "TIMED_POST_POLLINATION_OR_LOCAL_BARRIER_QUALIFIED_WITH_POLLINATOR_ACCESS_PRESERVED",
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
    mapping = result["pedicularis_state_mapping"]
    assert mapping["G0"] == "SEED_PREDATOR_INDEPENDENTLY_EXCLUDED"
    assert mapping["G1"] == "SEED_PREDATOR_EXPOSED"
    assert mapping["water_y"] == "HELD_FIXED_ACROSS_ALL_SCH_CELLS"
    assert result["readiness_reference"]["g_schema"] == "SCH_PEDICULARIS_PREDATOR_METHOD_V3"
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
    with pytest.raises(ValueError, match="predator-method V3"):
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

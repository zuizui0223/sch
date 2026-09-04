from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from scripts.analyze_pedicularis_full_surface import RAW_FIELDS, analyze, to_sch_rows


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_FULL_SURFACE_TEMPLATE_V1.csv"
CONFIG_TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_FULL_SURFACE_CONFIG_TEMPLATE_V1.json"
CONTRACT = ROOT / "docs" / "SCH_PEDICULARIS_FULL_SURFACE_CONTRACT_V1.md"


def _readiness(population: str = "P_REX_TEST", season: str = "S1") -> dict:
    return {
        "receipt_schema_version": "SCH_PEDICULARIS_FULL_SURFACE_READINESS_V1",
        "analysis": "pedicularis_pre_surface_readiness",
        "population_id": population,
        "season_id": season,
        "status": "PEDICULARIS_FULL_SURFACE_READY",
    }


def _config() -> dict:
    return {
        "sch_surface": {
            "bootstrap_reps": 300,
            "random_seed": 37,
            "min_z_levels": 5,
            "min_valid_bootstrap_fraction": 0.8,
            "min_interior_bootstrap_fraction": 0.9,
            "min_optimum_separation": 1.0,
            "min_optimum_shift": 0.5,
            "min_abs_component_gradient": 0.5,
        }
    }


def _rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(16):
        for z in (-2, -1, 0, 1, 2):
            for p, g in ((0, 0), (1, 0), (0, 1), (1, 1)):
                if (p, g) == (0, 0):
                    undamaged = 70
                elif (p, g) == (1, 0):
                    undamaged = 70 - (z - 2) ** 2
                elif (p, g) == (0, 1):
                    undamaged = 70 - (z + 2) ** 2
                else:
                    undamaged = 70 - (z - 2) ** 2 - (z + 2) ** 2
                damaged = (z + 2) ** 2 if g else 0
                pollination = "NATURAL" if p else "SUPPLEMENTED"
                water = "DRAINED" if g else "PROTECTED"
                rows.append(
                    {
                        "population_id": "P_REX_TEST",
                        "season_id": "S1",
                        "plant_id": f"P{plant:02d}",
                        "flower_id": f"P{plant:02d}_Z{z:+d}_P{p}G{g}",
                        "assigned_z_level": f"Z{z:+d}",
                        "realized_exsertion": str(float(z)),
                        "pollination_treatment": pollination,
                        "water_treatment": water,
                        "ovule_count": "100",
                        "undamaged_seed_count": str(undamaged),
                        "damaged_seed_count": str(damaged),
                        "pollen_grains": str(80 + 5 * z if p else 120),
                        "early_predator_attack_present": str(g),
                        "water_depth": "0" if g else "10",
                        "mechanical_damage": "0",
                    }
                )
    return rows


def test_template_and_config_are_registered_fail_closed_inputs() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == RAW_FIELDS
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["sch_surface"]["min_optimum_shift"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_registered_mapping_recovers_positive_pedicularis_compromise_surface() -> None:
    result = analyze(_rows(), _readiness(), _config())
    assert result["status"] == "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
    assert result["system"] == "Pedicularis rex"
    assert result["system_wrapper_schema_version"] == "SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V1"
    assert result["pedicularis_state_mapping"]["P0"].startswith("SUPPLEMENTED_OPEN")
    assert result["pedicularis_state_mapping"]["G0"].startswith("PROTECTED_WATER")
    est = result["observed_estimands"]
    assert abs(est["z_pollinator_context"] - 2.0) < 1e-8
    assert abs(est["z_antagonist_context"] + 2.0) < 1e-8
    assert abs(est["z_combined"]) < 1e-8
    assert est["shift_remove_antagonist"] > 0
    assert est["shift_remove_pollinator"] < 0
    assert all(result["decisions"].values())
    secondary = result["pedicularis_secondary_outcomes"]
    assert secondary["P0G0"]["mean_predation_fraction"] == 0.0
    assert secondary["P0G1"]["mean_predation_fraction"] > 0.0


def test_conversion_keeps_functional_weight_state_semantics() -> None:
    converted = to_sch_rows(_rows()[:4])
    states = {(row["pollinator_state"], row["antagonist_state"]) for row in converted}
    assert states == {("0", "0"), ("1", "0"), ("0", "1"), ("1", "1")}


def test_readiness_context_mismatch_fails_closed() -> None:
    with pytest.raises(ValueError, match="match the population and season"):
        analyze(_rows(), _readiness(season="S2"), _config())


def test_contract_preserves_p0_neutralization_and_primary_fitness_semantics() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "`P0` is **not** pollinator absence" in text
    assert "undamaged mature seed count per focal flower" in text
    assert "R_state = |x0* - z_P*| - |x1* - z_P*|" in text

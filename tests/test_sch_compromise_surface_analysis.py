from __future__ import annotations

import csv
import json
from pathlib import Path

from scripts.analyze_sch_compromise_surface import REQUIRED_FIELDS, analyze


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "SCH_CAUSAL_COMPROMISE_SURFACE_TEMPLATE_V1.csv"
CONFIG_TEMPLATE = ROOT / "empirical" / "architecture" / "SCH_CAUSAL_COMPROMISE_SURFACE_CONFIG_TEMPLATE_V1.json"
CONTRACT = ROOT / "docs" / "SCH_CAUSAL_COMPROMISE_SURFACE_ANALYSIS_V1.md"
MULTILEVEL = ROOT / "docs" / "SCH_MULTI_LEVEL_COMPROMISE_IDENTIFICATION_V1.md"
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_SHARED_TRAIT_COMPROMISE.md"


def _config() -> dict:
    return {
        "bootstrap_reps": 300,
        "random_seed": 11,
        "min_z_levels": 5,
        "min_valid_bootstrap_fraction": 0.8,
        "min_interior_bootstrap_fraction": 0.9,
        "min_optimum_separation": 1.0,
        "min_optimum_shift": 0.5,
        "min_abs_component_gradient": 0.5,
    }


def _positive_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(18):
        plant_effect = (plant % 3) * 0.1
        for z in (-2, -1, 0, 1, 2):
            for p, g in ((0, 0), (1, 0), (0, 1), (1, 1)):
                if (p, g) == (0, 0):
                    fitness = 30.0
                elif (p, g) == (1, 0):
                    fitness = 40.0 - (z - 2.0) ** 2
                elif (p, g) == (0, 1):
                    fitness = 40.0 - (z + 2.0) ** 2
                else:
                    fitness = 45.0 - z**2
                fitness += plant_effect
                rows.append(
                    {
                        "plant_id": f"P{plant:02d}",
                        "blossom_id": f"P{plant:02d}_Z{z:+d}_P{p}G{g}",
                        "z_level": f"Z{z:+d}",
                        "z_measured": str(float(z)),
                        "pollinator_state": str(p),
                        "antagonist_state": str(g),
                        "fitness_value": f"{fitness:.4f}",
                    }
                )
    return rows


def _boundary_rows() -> list[dict[str, str]]:
    rows = _positive_rows()
    for row in rows:
        if row["pollinator_state"] == "1" and row["antagonist_state"] == "1":
            z = float(row["z_measured"])
            plant = int(row["plant_id"][1:])
            row["fitness_value"] = f"{35.0 + 2.0 * z + (plant % 3) * 0.1:.4f}"
    return rows


def test_registered_template_and_fail_closed_config_exist() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["min_optimum_shift"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_positive_surface_recovers_interior_compromise_and_opposing_shifts() -> None:
    result = analyze(_positive_rows(), _config())
    assert result["status"] == "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
    assert all(result["decisions"].values())
    est = result["observed_estimands"]
    assert abs(est["z_combined"]) < 1e-8
    assert abs(est["z_pollinator_context"] - 2.0) < 1e-8
    assert abs(est["z_antagonist_context"] + 2.0) < 1e-8
    assert est["shift_remove_antagonist"] > 0
    assert est["shift_remove_pollinator"] < 0
    gradients = est["gradients_at_combined_optimum"]
    assert gradients["pollinator_component_G0"] > 0
    assert gradients["antagonist_component_P1"] < 0
    assert result["bootstrap"]["combined_interior_fraction"] == 1.0


def test_boundary_combined_surface_does_not_get_promoted_to_compromise() -> None:
    result = analyze(_boundary_rows(), _config())
    assert result["decisions"]["combined_interior_optimum"] is False
    assert result["status"] == "COMPROMISE_CRITERIA_NOT_ALL_RECOVERED"


def test_contract_rejects_vertex_zero_slope_as_independent_proof() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "not** counted as an independent test of gradient cancellation" in text
    assert "opposing functional-component gradients" in text
    assert "construction / physiological cost by subtraction" in text
    assert "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE" in text


def test_state_specific_optima_are_not_relabelled_as_pure_function_optima() -> None:
    contract = CONTRACT.read_text(encoding="utf-8")
    multilevel = MULTILEVEL.read_text(encoding="utf-8")
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    for text in (contract, multilevel, manuscript):
        assert "z_P* != automatically z_F1*" in text
        assert "z_G* != automatically z_F2*" in text
    assert "state-specific reproductive optima" in manuscript
    assert "pure function optima require an additional identifying assay" in contract

import json
import math
from pathlib import Path

import pytest

from scripts.estimate_sch_conflict_budget import estimate


ROOT = Path(__file__).resolve().parents[1]
CONFIG_TEMPLATE = ROOT / "empirical" / "architecture" / "SCH_CONFLICT_BUDGET_CONFIG_TEMPLATE_V1.json"


def _rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    z_values = (-3.0, -1.5, 0.0, 1.5, 3.0)
    for plant in range(18):
        plant_effect = (plant % 3) * 0.02
        for zi, z in enumerate(z_values):
            f1 = 10.0 - (z - 2.0) ** 2
            f2 = 10.0 - (z + 2.0) ** 2
            for p, g in ((0, 0), (1, 0), (0, 1), (1, 1)):
                value = 30.0 + plant_effect
                if p:
                    value += f1
                if g:
                    value += f2
                rows.append(
                    {
                        "plant_id": f"P{plant:02d}",
                        "blossom_id": f"P{plant:02d}_Z{zi}_P{p}G{g}",
                        "z_level": f"Z{zi}",
                        "z_measured": str(z),
                        "pollinator_state": str(p),
                        "antagonist_state": str(g),
                        "fitness_value": f"{value:.8f}",
                    }
                )
    return rows


def _receipt() -> dict:
    return {
        "receipt_schema_version": "SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1",
        "pure_function_upgrade": {
            "schema_version": "SCH_CONTEXT_STABLE_COMPONENT_OPTIMA_V1",
            "status": "CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED",
        },
        "identified_pure_function_optima": {
            "z_F1": 2.0,
            "z_F2": -2.0,
        },
    }


def _config() -> dict:
    return {
        "fitness_scale_id": "INTACT_SEEDS_COMPONENT_SCALE",
        "min_z_levels": 5,
        "bootstrap_reps": 200,
        "random_seed": 17,
        "min_valid_bootstrap_fraction": 0.8,
    }


def test_fail_closed_template_requires_scale_identity() -> None:
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    assert config["fitness_scale_id"] == "REQUIRED_BEFORE_USE"
    assert "DO_NOT_RUN" in config["status"]


def test_known_quadratic_components_recover_conflict_budget_eight() -> None:
    result = estimate(_rows(), _receipt(), _config())
    observed = result["observed_estimands"]
    assert result["status"] == "FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED"
    assert result["fitness_scale_id"] == "INTACT_SEEDS_COMPONENT_SCALE"
    assert math.isclose(observed["F1_separate_optimum"]["z_optimum"], 2.0, abs_tol=1e-10)
    assert math.isclose(observed["F2_separate_optimum"]["z_optimum"], -2.0, abs_tol=1e-10)
    assert math.isclose(observed["shared_component_optimum"]["z_optimum"], 0.0, abs_tol=1e-10)
    assert math.isclose(observed["component_conflict_load"], 8.0, rel_tol=1e-10)
    assert observed["component_identity_max_abs_error"] < 1e-10
    lo, hi = result["bootstrap"]["component_conflict_load_95_ci"]
    assert math.isclose(lo, 8.0, rel_tol=1e-9)
    assert math.isclose(hi, 8.0, rel_tol=1e-9)


def test_conflict_budget_fails_without_pure_component_gate() -> None:
    receipt = _receipt()
    receipt["pure_function_upgrade"]["status"] = "PURE_FUNCTION_OPTIMA_NOT_IDENTIFIED"
    with pytest.raises(ValueError, match="context-stable component optima"):
        estimate(_rows(), receipt, _config())


def test_conflict_budget_fails_without_frozen_fitness_scale() -> None:
    config = _config()
    config["fitness_scale_id"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="fitness_scale_id"):
        estimate(_rows(), _receipt(), config)

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_sch_compromise_surface.py"
spec = importlib.util.spec_from_file_location("sch_surface_units", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def _surface(scale: float):
    return [
        (z * scale, 10.0 - (z - 2.0) ** 2)
        for z in (0.0, 1.0, 2.0, 3.0, 4.0)
    ]


def _predict(fit: dict, z: float) -> float:
    return fit["a"] + fit["b"] * z + fit["c"] * z * z


def test_quadratic_fit_is_invariant_to_z_units():
    for scale in (1e-13, 1e-3, 1.0, 1e6):
        fit = module._fit_quadratic(_surface(scale))
        assert fit["optimum_class"] == "INTERIOR_CONCAVE"
        assert math.isclose(
            fit["primary_optimum"],
            2.0 * scale,
            rel_tol=2e-13,
            abs_tol=1e-30,
        )
        for z in (0.0, 1.0, 2.0, 3.0, 4.0):
            observed = _predict(fit, z * scale)
            expected = 10.0 - (z - 2.0) ** 2
            assert math.isclose(observed, expected, rel_tol=1e-12, abs_tol=1e-10)


def test_three_distinct_tiny_z_values_are_not_collapsed_by_decimal_rounding():
    fit = module._fit_quadratic(
        [(0.0, 0.0), (1e-13, 1.0), (2e-13, 0.0)]
    )
    assert fit["optimum_class"] == "INTERIOR_CONCAVE"
    assert math.isclose(fit["primary_optimum"], 1e-13, rel_tol=1e-12)


def test_genuinely_degenerate_z_design_still_fails_closed():
    with pytest.raises(ValueError, match="three distinct measured z values"):
        module._fit_quadratic([(1.0, 1.0), (1.0, 2.0), (2.0, 3.0)])

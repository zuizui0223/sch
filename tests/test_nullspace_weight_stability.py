import pytest

from scripts.curvature_weight_nullspace import (
    nullspace_angle_bound_from_true_gap,
    nullspace_stability_from_estimated_gap,
)


def test_true_gap_davis_kahan_bound():
    bound = nullspace_angle_bound_from_true_gap(true_gap=1.0, operator_error=0.1)
    assert bound == pytest.approx(1.0 / 9.0)


def test_estimated_gap_yields_conservative_stable_direction():
    out = nullspace_stability_from_estimated_gap(
        estimated_second_eigenvalue=1.0,
        operator_error=0.1,
    )
    assert out.stable_one_dimensional_nullspace
    assert out.conservative_gap_lower == pytest.approx(0.9)
    assert out.sin_angle_upper == pytest.approx(0.125)


def test_small_gap_is_fail_closed():
    out = nullspace_stability_from_estimated_gap(
        estimated_second_eigenvalue=0.25,
        operator_error=0.1,
    )
    assert not out.stable_one_dimensional_nullspace
    assert out.sin_angle_upper is None


def test_zero_error_has_zero_angle_bound_when_gap_positive():
    out = nullspace_stability_from_estimated_gap(
        estimated_second_eigenvalue=0.5,
        operator_error=0.0,
    )
    assert out.stable_one_dimensional_nullspace
    assert out.sin_angle_upper == pytest.approx(0.0)


def test_invalid_true_gap_regime_fails_closed():
    with pytest.raises(ValueError):
        nullspace_angle_bound_from_true_gap(true_gap=0.2, operator_error=0.1)

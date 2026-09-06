import pytest

from scripts.weight_chord_curvature import (
    audit_concave_chord_gap,
    concave_chord_gap_bounds,
)


def test_midpoint_gap_bounds_use_one_eighth_rule():
    lower, upper = concave_chord_gap_bounds(
        curvature_lower=2.0,
        curvature_upper=6.0,
        t=0.5,
    )
    assert lower == pytest.approx(0.25)
    assert upper == pytest.approx(0.75)


def test_quadratic_concave_example_hits_exact_gap():
    # g(t)=1-2(t-0.5)^2 has -g''=4 and endpoint values 0.5, midpoint 1.
    out = audit_concave_chord_gap(
        endpoint0=0.5,
        endpoint1=0.5,
        observed=1.0,
        curvature_lower=4.0,
        curvature_upper=4.0,
        t=0.5,
    )
    assert out.observed_gap == pytest.approx(0.5)
    assert out.lower == pytest.approx(0.5)
    assert out.upper == pytest.approx(0.5)
    assert not out.violates_lower
    assert not out.violates_upper


def test_negative_gap_rejects_concavity_floor():
    out = audit_concave_chord_gap(
        endpoint0=1.0,
        endpoint1=1.0,
        observed=0.9,
        curvature_lower=0.0,
        curvature_upper=10.0,
        t=0.5,
    )
    assert out.violates_lower


def test_metric_scaling_enters_directional_gap():
    lower, upper = concave_chord_gap_bounds(
        curvature_lower=1.0,
        curvature_upper=2.0,
        t=0.25,
        direction_metric_norm_sq=4.0,
    )
    assert lower == pytest.approx(0.375)
    assert upper == pytest.approx(0.75)


def test_invalid_curvature_bounds_fail_closed():
    with pytest.raises(ValueError):
        concave_chord_gap_bounds(curvature_lower=2.0, curvature_upper=1.0, t=0.5)

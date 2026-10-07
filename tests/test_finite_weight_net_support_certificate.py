import math

import pytest


def support_value(points, weight):
    return min(sum(w * y for w, y in zip(weight, point)) for point in points)


def support_slack_bound(attainable_radius, candidate_radius, covering_radius):
    if attainable_radius < 0 or candidate_radius < 0 or covering_radius < 0:
        raise ValueError("radii must be nonnegative")
    return (attainable_radius + candidate_radius) * covering_radius


def test_support_value_is_lipschitz_in_weight_direction():
    points = [(0.0, 2.0), (1.0, 0.5), (2.0, 0.0)]
    radius = max(math.hypot(*p) for p in points)
    w = (1.0, 0.0)
    v_raw = (0.98, 0.2)
    norm = math.hypot(*v_raw)
    v = tuple(x / norm for x in v_raw)
    lhs = abs(support_value(points, w) - support_value(points, v))
    delta = math.dist(w, v)
    assert lhs <= radius * delta + 1e-12


def test_sampled_support_candidate_obeys_unsampled_slack_bound():
    points = [(0.0, 2.0), (2.0, 0.0)]
    registered = [(1.0, 0.0), (0.0, 1.0)]
    candidate = (0.5, 0.5)
    assert all(
        sum(a * b for a, b in zip(v, candidate)) >= support_value(points, v)
        for v in registered
    )

    w_raw = (1.0, 1.0)
    w_norm = math.hypot(*w_raw)
    w = tuple(x / w_norm for x in w_raw)
    nearest_delta = min(math.dist(w, v) for v in registered)
    r_y = max(math.hypot(*p) for p in points)
    r_b = math.hypot(*candidate)
    epsilon = support_slack_bound(r_y, r_b, nearest_delta)
    violation = max(0.0, support_value(points, w) - sum(a * b for a, b in zip(w, candidate)))
    assert violation <= epsilon + 1e-12


def test_refining_covering_radius_tightens_certificate():
    coarse = support_slack_bound(2.0, 1.5, 0.2)
    fine = support_slack_bound(2.0, 1.5, 0.05)
    assert fine < coarse
    assert fine == pytest.approx(coarse / 4.0)


def test_common_radius_special_case_is_two_r_delta():
    assert support_slack_bound(3.0, 3.0, 0.1) == pytest.approx(0.6)


def test_negative_radius_fails_closed():
    with pytest.raises(ValueError):
        support_slack_bound(-1.0, 1.0, 0.1)

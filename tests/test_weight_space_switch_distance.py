import math

import pytest


def euclidean_simplex_switch_distance(weight, loss_a, loss_b):
    delta = [b - a for a, b in zip(loss_a, loss_b)]
    margin = sum(w * d for w, d in zip(weight, delta))
    mean = sum(delta) / len(delta)
    centered = [d - mean for d in delta]
    s2 = sum(d * d for d in centered)
    if s2 == 0.0:
        return math.inf, tuple(0.0 for _ in delta)
    distance = margin / math.sqrt(s2)
    perturbation = tuple(-margin * d / s2 for d in centered)
    return distance, perturbation


def test_simplex_projection_reaches_pairwise_tie_and_preserves_total_weight():
    weight = (0.6, 0.2, 0.2)
    loss_a = (1.0, 3.0, 2.0)
    loss_b = (3.0, 1.0, 2.0)
    distance, perturbation = euclidean_simplex_switch_distance(weight, loss_a, loss_b)

    assert distance == pytest.approx(0.8 / math.sqrt(8.0))
    assert sum(perturbation) == pytest.approx(0.0)
    new_weight = tuple(w + dw for w, dw in zip(weight, perturbation))
    va = sum(w * y for w, y in zip(new_weight, loss_a))
    vb = sum(w * y for w, y in zip(new_weight, loss_b))
    assert va == pytest.approx(vb)
    assert new_weight == pytest.approx((0.4, 0.4, 0.2))


def test_common_loss_shift_is_invisible_to_relative_weight_switching():
    weight = (0.5, 0.3, 0.2)
    loss_a = (1.0, 2.0, 3.0)
    loss_b = (2.0, 3.0, 4.0)  # delta is proportional to all-ones
    distance, perturbation = euclidean_simplex_switch_distance(weight, loss_a, loss_b)
    assert math.isinf(distance)
    assert perturbation == (0.0, 0.0, 0.0)


def test_nearest_competitor_is_minimum_pairwise_switch_distance():
    weight = (0.55, 0.30, 0.15)
    a = (1.0, 2.0, 2.0)
    competitors = [
        (2.0, 1.0, 2.0),
        (2.5, 1.8, 1.0),
    ]
    distances = [euclidean_simplex_switch_distance(weight, a, b)[0] for b in competitors]
    assert min(distances) == pytest.approx(sorted(distances)[0])

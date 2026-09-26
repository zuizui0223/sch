import pytest


def value(loss, weight):
    return sum(y * w for y, w in zip(loss, weight))


def is_optimal(target, candidates, weight, tol=1e-12):
    target_value = value(target, weight)
    return target_value <= min(value(c, weight) for c in candidates) + tol


def test_state_supported_at_two_weights_is_supported_on_entire_chord():
    a = (1.0, 1.0)
    candidates = [a, (0.0, 3.0), (3.0, 0.0)]
    w0 = (0.35, 0.65)
    w1 = (0.65, 0.35)
    assert is_optimal(a, candidates, w0)
    assert is_optimal(a, candidates, w1)

    for k in range(21):
        t = k / 20.0
        wt = ((1.0 - t) * w0[0] + t * w1[0], (1.0 - t) * w0[1] + t * w1[1])
        assert is_optimal(a, candidates, wt)


def test_pairwise_switch_weight_ratio_matches_loss_difference_formula():
    a = (1.0, 3.0)
    b = (4.0, 1.0)
    # r = w1/w2 = -(a2-b2)/(a1-b1) = -2/-3 = 2/3.
    r = -(a[1] - b[1]) / (a[0] - b[0])
    weight = (r, 1.0)
    assert r == pytest.approx(2.0 / 3.0)
    assert value(a, weight) == pytest.approx(value(b, weight))


def test_support_region_is_closed_under_positive_scaling():
    a = (1.0, 1.0)
    candidates = [a, (0.0, 3.0), (3.0, 0.0)]
    w = (0.4, 0.6)
    assert is_optimal(a, candidates, w)
    assert is_optimal(a, candidates, (7.0 * w[0], 7.0 * w[1]))

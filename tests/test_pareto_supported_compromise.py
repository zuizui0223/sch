import pytest


def weighted_value(point, weight):
    return sum(x * w for x, w in zip(point, weight))


def test_positive_weight_minimizer_is_not_dominated_in_finite_example():
    points = [(0.0, 4.0), (1.0, 2.0), (4.0, 0.0)]
    weight = (0.7, 0.3)
    best = min(points, key=lambda p: weighted_value(p, weight))

    for candidate in points:
        dominates = all(c <= b for c, b in zip(candidate, best)) and any(
            c < b for c, b in zip(candidate, best)
        )
        assert not dominates


def test_value_function_is_concave_in_weights_for_finite_loss_set():
    points = [(0.0, 4.0), (1.5, 1.5), (4.0, 0.0)]

    def value(weight):
        return min(weighted_value(p, weight) for p in points)

    w = (0.8, 0.2)
    v = (0.2, 0.8)
    theta = 0.35
    mix = tuple(theta * a + (1.0 - theta) * b for a, b in zip(w, v))
    assert value(mix) + 1e-12 >= theta * value(w) + (1.0 - theta) * value(v)


def test_pareto_point_can_be_unsupported_when_loss_image_is_nonconvex():
    a = (0.0, 4.0)
    b = (2.0, 3.0)
    c = (4.0, 0.0)

    # B is nondominated by A or C.
    for other in (a, c):
        assert not (
            all(o <= x for o, x in zip(other, b))
            and any(o < x for o, x in zip(other, b))
        )

    # No positive normalized weight on a dense deterministic grid supports B.
    for k in range(1, 1000):
        w1 = k / 1000.0
        w2 = 1.0 - w1
        vb = weighted_value(b, (w1, w2))
        assert vb > min(weighted_value(a, (w1, w2)), weighted_value(c, (w1, w2)))


def test_common_weight_scaling_preserves_minimizer():
    points = [(0.0, 4.0), (1.0, 1.5), (4.0, 0.0)]
    w = (0.6, 0.4)
    scaled = (3.0 * w[0], 3.0 * w[1])
    best_w = min(range(len(points)), key=lambda i: weighted_value(points[i], w))
    best_scaled = min(range(len(points)), key=lambda i: weighted_value(points[i], scaled))
    assert best_w == best_scaled

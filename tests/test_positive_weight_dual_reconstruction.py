from __future__ import annotations


def support_value(points, weight):
    return min(sum(w * y for w, y in zip(weight, point)) for point in points)


def satisfies_registered_halfspaces(point, weights, values, tol=1e-12):
    for weight, value in zip(weights, values):
        lhs = sum(w * y for w, y in zip(weight, point))
        if lhs + tol < value:
            return False
    return True


def test_unsupported_nonconvex_point_is_invisible_to_positive_weights():
    endpoints = [(0.0, 2.0), (2.0, 0.0)]
    with_unsupported = endpoints + [(1.2, 1.2)]
    weights = [
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
        (2.0, 1.0),
        (1.0, 2.0),
        (4.0, 1.0),
        (1.0, 4.0),
    ]
    assert [support_value(endpoints, w) for w in weights] == [
        support_value(with_unsupported, w) for w in weights
    ]


def test_adding_weight_constraints_can_only_shrink_outer_approximation():
    points = [(0.0, 2.0), (2.0, 0.0)]
    weights_small = [(1.0, 0.0), (0.0, 1.0)]
    weights_large = weights_small + [(1.0, 1.0)]
    values_small = [support_value(points, w) for w in weights_small]
    values_large = [support_value(points, w) for w in weights_large]

    grid = [
        (x / 2.0, y / 2.0)
        for x in range(0, 7)
        for y in range(0, 7)
    ]
    accepted_small = {
        p for p in grid if satisfies_registered_halfspaces(p, weights_small, values_small)
    }
    accepted_large = {
        p for p in grid if satisfies_registered_halfspaces(p, weights_large, values_large)
    }
    assert accepted_large <= accepted_small
    assert (0.5, 0.5) in accepted_small
    assert (0.5, 0.5) not in accepted_large


def test_attainable_points_satisfy_every_registered_support_halfspace():
    points = [(0.2, 1.8), (0.8, 0.9), (1.7, 0.2)]
    weights = [(1.0, 0.0), (0.0, 1.0), (1.0, 1.0), (3.0, 2.0)]
    values = [support_value(points, w) for w in weights]
    for point in points:
        assert satisfies_registered_halfspaces(point, weights, values)

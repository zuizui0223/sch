import math


def _optimized_quadratic_loss(weights, thetas):
    z = sum(w * theta for w, theta in zip(weights, thetas)) / sum(weights)
    loss = sum(w * (z - theta) ** 2 for w, theta in zip(weights, thetas))
    return z, loss


def test_extreme_pair_certifies_worst_conflict_for_ordered_equal_curvature_quadratics():
    thetas = (-2.0, -0.5, 0.5, 2.0)
    weights = (0.5, 0.0, 0.0, 0.5)
    z, loss = _optimized_quadratic_loss(weights, thetas)

    assert math.isclose(z, 0.0, abs_tol=1e-12)
    assert math.isclose(loss, 4.0, abs_tol=1e-12)
    assert math.isclose(loss, (max(thetas) - min(thetas)) ** 2 / 4.0, abs_tol=1e-12)


def test_intermediate_functions_are_nonbinding_at_extreme_pair_minimax_point():
    thetas = (-2.0, -0.5, 0.5, 2.0)
    z = 0.0
    residuals = tuple((z - theta) ** 2 for theta in thetas)
    assert residuals[0] == residuals[3] == 4.0
    assert residuals[1] < 4.0
    assert residuals[2] < 4.0

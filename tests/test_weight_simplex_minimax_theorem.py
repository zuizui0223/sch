import math


def _quad_loss(z, theta):
    return (z - theta) ** 2


def _optimized_weighted_loss(weights, thetas):
    total = sum(weights)
    z_star = sum(w * t for w, t in zip(weights, thetas)) / total
    loss = sum(w * _quad_loss(z_star, t) for w, t in zip(weights, thetas))
    return z_star, loss


def test_two_function_simplex_max_matches_minimax_residual():
    thetas = (-1.0, 1.0)
    best = (-1.0, None, None)
    for k in range(1001):
        w1 = k / 1000.0
        weights = (w1, 1.0 - w1)
        z_star, loss = _optimized_weighted_loss(weights, thetas)
        if loss > best[0]:
            best = (loss, weights, z_star)

    loss, weights, z_star = best
    assert math.isclose(weights[0], 0.5, abs_tol=1e-3)
    assert math.isclose(z_star, 0.0, abs_tol=1e-3)
    assert math.isclose(loss, 1.0, abs_tol=1e-6)
    assert math.isclose(max(_quad_loss(z_star, t) for t in thetas), 1.0, abs_tol=1e-6)


def test_three_function_max_can_drop_nonbinding_middle_function():
    thetas = (-1.0, 0.0, 1.0)
    weights = (0.5, 0.0, 0.5)
    z_star, loss = _optimized_weighted_loss(weights, thetas)
    residuals = tuple(_quad_loss(z_star, t) for t in thetas)

    assert math.isclose(z_star, 0.0, abs_tol=1e-12)
    assert math.isclose(loss, 1.0, abs_tol=1e-12)
    assert residuals == (1.0, 0.0, 1.0)
    assert residuals[1] <= residuals[0]

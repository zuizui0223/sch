import math


def _weighted_quadratic_optimum(weights, points):
    dim = len(points[0])
    z = tuple(
        sum(w * point[j] for w, point in zip(weights, points)) / sum(weights)
        for j in range(dim)
    )
    loss = sum(
        w * sum((zj - pj) ** 2 for zj, pj in zip(z, point))
        for w, point in zip(weights, points)
    )
    return z, loss


def test_equilateral_triangle_requires_three_binding_functions_for_global_worst_case():
    root3 = math.sqrt(3.0)
    points = (
        (1.0, 0.0),
        (-0.5, root3 / 2.0),
        (-0.5, -root3 / 2.0),
    )

    z3, loss3 = _weighted_quadratic_optimum((1 / 3, 1 / 3, 1 / 3), points)
    assert math.isclose(z3[0], 0.0, abs_tol=1e-12)
    assert math.isclose(z3[1], 0.0, abs_tol=1e-12)
    assert math.isclose(loss3, 1.0, rel_tol=1e-12)

    # Any pair is distance sqrt(3) apart; the maximum pairwise compromise
    # under simplex weights occurs at 1/2,1/2 and equals d^2/4=3/4.
    for i, j in ((0, 1), (0, 2), (1, 2)):
        pair = (points[i], points[j])
        _, pair_loss = _weighted_quadratic_optimum((0.5, 0.5), pair)
        assert math.isclose(pair_loss, 0.75, rel_tol=1e-12)
        assert pair_loss < loss3

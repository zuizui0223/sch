import math


def pairwise_quadratic_min(effective_weights, thetas):
    total = sum(effective_weights)
    numerator = 0.0
    for i in range(len(thetas)):
        for j in range(i + 1, len(thetas)):
            numerator += effective_weights[i] * effective_weights[j] * (thetas[i] - thetas[j]) ** 2
    return numerator / (2.0 * total)


def test_bounds_collapse_to_exact_value_for_quadratic_losses():
    weights = [1.0, 2.0, 0.7]
    curvature = [0.8, 1.3, 2.0]
    thetas = [-2.0, 0.5, 3.0]
    effective = [w * q for w, q in zip(weights, curvature)]
    exact_from_pairwise = pairwise_quadratic_min(effective, thetas)

    total = sum(effective)
    z = sum(a * t for a, t in zip(effective, thetas)) / total
    direct = 0.5 * sum(a * (z - t) ** 2 for a, t in zip(effective, thetas))
    assert math.isclose(direct, exact_from_pairwise, rel_tol=1e-12, abs_tol=1e-12)


def test_nonquadratic_quartic_example_stays_above_strong_convex_lower_bound():
    weights = [1.0, 1.5]
    thetas = [-1.0, 2.0]
    base_curvature = [0.6, 1.0]
    quartic = [0.08, 0.05]

    lower_effective = [w * m for w, m in zip(weights, base_curvature)]
    lower = pairwise_quadratic_min(lower_effective, thetas)

    def loss(z):
        total = 0.0
        for w, theta, m, q in zip(weights, thetas, base_curvature, quartic):
            x = z - theta
            total += w * (0.5 * m * x * x + q * x ** 4)
        return total

    # Dense deterministic grid is sufficient for a regression check of the inequality.
    grid = [-2.0 + 0.0005 * i for i in range(10001)]
    approx_min = min(loss(z) for z in grid)
    assert approx_min + 1e-8 >= lower

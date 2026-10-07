import math


def loss_prime(z: float, theta: float, curvature: float) -> float:
    d = z - theta
    return curvature * d + 0.2 * d**3


def loss_second(z: float, theta: float, curvature: float) -> float:
    d = z - theta
    return curvature + 0.6 * d * d


def solve_optimum(thetas, curvatures, weights):
    lo = min(thetas) - 2.0
    hi = max(thetas) + 2.0

    def score(z):
        return sum(w * loss_prime(z, t, c) for t, c, w in zip(thetas, curvatures, weights))

    assert score(lo) < 0
    assert score(hi) > 0
    for _ in range(120):
        mid = 0.5 * (lo + hi)
        if score(mid) < 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def test_optimum_lies_strictly_inside_function_optimum_hull():
    theta = [-2.0, 0.5, 3.0]
    curvature = [1.0, 1.7, 0.8]
    weights = [0.7, 2.0, 1.2]
    z = solve_optimum(theta, curvature, weights)
    assert min(theta) < z < max(theta)


def test_log_weight_sensitivity_matches_implicit_formula_and_points_toward_theta_j():
    theta = [-2.0, 0.5, 3.0]
    curvature = [1.0, 1.7, 0.8]
    weights = [0.7, 2.0, 1.2]
    z = solve_optimum(theta, curvature, weights)
    H = sum(w * loss_second(z, t, c) for t, c, w in zip(theta, curvature, weights))

    eps = 1e-5
    for j in range(len(theta)):
        predicted = -weights[j] * loss_prime(z, theta[j], curvature[j]) / H
        plus = weights[:]
        minus = weights[:]
        plus[j] *= math.exp(eps)
        minus[j] *= math.exp(-eps)
        finite_difference = (
            solve_optimum(theta, curvature, plus) - solve_optimum(theta, curvature, minus)
        ) / (2 * eps)
        assert abs(predicted - finite_difference) < 2e-5
        if abs(theta[j] - z) > 1e-9:
            assert math.copysign(1.0, predicted) == math.copysign(1.0, theta[j] - z)


def test_common_weight_rescaling_leaves_optimum_unchanged_and_sensitivities_sum_to_zero():
    theta = [-2.0, 0.5, 3.0]
    curvature = [1.0, 1.7, 0.8]
    weights = [0.7, 2.0, 1.2]
    z = solve_optimum(theta, curvature, weights)
    z_scaled = solve_optimum(theta, curvature, [11.0 * w for w in weights])
    assert abs(z - z_scaled) < 1e-10

    H = sum(w * loss_second(z, t, c) for t, c, w in zip(theta, curvature, weights))
    sensitivities = [
        -w * loss_prime(z, t, c) / H
        for t, c, w in zip(theta, curvature, weights)
    ]
    assert abs(sum(sensitivities)) < 1e-10

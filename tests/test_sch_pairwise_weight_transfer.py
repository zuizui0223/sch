import math


def optimized_loss_two(w1: float, w2: float, theta1: float = -1.0, theta2: float = 2.0) -> float:
    W = w1 + w2
    return 0.5 * (w1 * w2 / W) * (theta1 - theta2) ** 2


def test_fixed_total_transfer_is_concave_and_maximized_at_equal_weights():
    W = 4.0
    values = []
    for t in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5):
        w1 = W / 2 + t
        w2 = W / 2 - t
        values.append(optimized_loss_two(w1, w2))

    center = len(values) // 2
    assert values[center] == max(values)

    # Discrete second differences are non-positive for the quadratic special case.
    for i in range(1, len(values) - 1):
        second_difference = values[i + 1] - 2 * values[i] + values[i - 1]
        assert second_difference <= 1e-12


def test_first_derivative_matches_residual_loss_contrast():
    theta1, theta2 = -1.0, 2.0
    w1, w2 = 1.2, 2.8
    W = w1 + w2
    z = (w1 * theta1 + w2 * theta2) / W
    residual_contrast = 0.5 * (z - theta1) ** 2 - 0.5 * (z - theta2) ** 2

    eps = 1e-6
    plus = optimized_loss_two(w1 + eps, w2 - eps, theta1, theta2)
    minus = optimized_loss_two(w1 - eps, w2 + eps, theta1, theta2)
    finite = (plus - minus) / (2 * eps)
    assert math.isclose(finite, residual_contrast, rel_tol=2e-6, abs_tol=2e-8)

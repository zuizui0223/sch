import math


def _quadratic_load(w1: float, w2: float, theta1: float = -1.0, theta2: float = 1.0) -> float:
    # ell_i(z)=0.5*(z-theta_i)^2
    z = (w1 * theta1 + w2 * theta2) / (w1 + w2)
    return 0.5 * w1 * (z - theta1) ** 2 + 0.5 * w2 * (z - theta2) ** 2


def test_finite_weight_reoptimization_relief_is_positive_and_exact():
    # w0=(1,1), w1=(2,1). Baseline optimum z0=0 and each residual loss=0.5.
    l0 = _quadratic_load(1.0, 1.0)
    l1 = _quadratic_load(2.0, 1.0)
    no_reopt = l0 + 0.5 * (2.0 - 1.0)
    relief = no_reopt - l1
    assert math.isclose(l0, 1.0)
    assert math.isclose(l1, 4.0 / 3.0)
    assert math.isclose(relief, 1.0 / 6.0)
    assert relief > 0.0


def test_relief_equals_integrated_weight_curvature_for_quadratic_example():
    # Along w1=1+t, w2=1, L(t)=2(1+t)/(2+t), hence -L''=4/(2+t)^3.
    # Integral_0^1 (1-t)*4/(2+t)^3 dt = 1/6.
    n = 20000
    h = 1.0 / n
    integral = 0.0
    for k in range(n):
        t = (k + 0.5) * h
        integral += (1.0 - t) * 4.0 / (2.0 + t) ** 3 * h
    assert abs(integral - 1.0 / 6.0) < 1e-8


def test_no_relief_when_all_function_optima_are_aligned():
    # If both functions have the same optimum, reweighting never moves the shared optimum.
    def load(w1: float, w2: float) -> float:
        theta = 0.3
        z = theta
        return 0.5 * w1 * (z - theta) ** 2 + 0.5 * w2 * (z - theta) ** 2

    l0 = load(1.0, 1.0)
    l1 = load(3.0, 0.5)
    assert l0 == 0.0
    assert l1 == 0.0
    assert l0 - l1 == 0.0

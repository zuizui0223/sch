import math


def dloss1(z):
    u = z + 1.0
    return 4.0 * u**3 + 2.0 * u


def dloss2(z):
    u = z - 2.0
    return 4.0 * u**3 + 2.0 * u


def loss1(z):
    u = z + 1.0
    return u**4 + u**2


def loss2(z):
    u = z - 2.0
    return u**4 + u**2


def optimum(w1, w2):
    lo, hi = -1.0, 2.0
    for _ in range(100):
        mid = (lo + hi) / 2.0
        grad = w1 * dloss1(mid) + w2 * dloss2(mid)
        if grad < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def test_nonquadratic_shared_optimum_is_strictly_between_function_optima():
    z = optimum(1.0, 1.0)
    assert -1.0 < z < 2.0


def test_increasing_function1_weight_moves_optimum_toward_theta1():
    z_low = optimum(0.5, 1.0)
    z_mid = optimum(1.0, 1.0)
    z_high = optimum(2.0, 1.0)
    assert z_high < z_mid < z_low


def test_nonquadratic_compromise_load_is_positive_when_optima_differ():
    z = optimum(1.0, 1.0)
    combined = loss1(z) + loss2(z)
    separate = loss1(-1.0) + loss2(2.0)
    assert combined - separate > 0
    assert math.isclose(separate, 0.0, abs_tol=1e-12)

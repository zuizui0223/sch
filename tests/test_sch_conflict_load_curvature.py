import math


def optimum(weights, thetas):
    # Quadratic special case ell_i=(z-theta_i)^2 / 2.
    total = sum(weights)
    return sum(w * t for w, t in zip(weights, thetas)) / total


def gradients(z, thetas):
    return [z - t for t in thetas]


def hessian(weights, thetas):
    z = optimum(weights, thetas)
    g = gradients(z, thetas)
    H = sum(weights)  # ell_i''=1
    return [[-(gj * gk) / H for gk in g] for gj in g]


def optimized_loss(weights, thetas):
    z = optimum(weights, thetas)
    return sum(w * 0.5 * (z - t) ** 2 for w, t in zip(weights, thetas))


def test_hessian_is_negative_semidefinite_and_cross_signs_match_pulls():
    weights = [1.0, 2.0, 1.5]
    thetas = [-2.0, 0.5, 3.0]
    z = optimum(weights, thetas)
    g = gradients(z, thetas)
    H = hessian(weights, thetas)

    v = [0.7, -1.2, 0.4]
    quad = sum(v[i] * H[i][j] * v[j] for i in range(3) for j in range(3))
    assert quad <= 1e-12

    # Functions on opposite sides of z* have positive cross-curvature.
    assert g[0] * g[2] < 0
    assert H[0][2] > 0


def test_envelope_shadow_price_matches_finite_difference():
    weights = [1.3, 0.8, 2.1]
    thetas = [-1.0, 0.7, 2.5]
    z = optimum(weights, thetas)
    j = 1
    expected = 0.5 * (z - thetas[j]) ** 2

    eps = 1e-6
    w2 = list(weights)
    w2[j] += eps
    finite = (optimized_loss(w2, thetas) - optimized_loss(weights, thetas)) / eps
    assert math.isclose(finite, expected, rel_tol=2e-5, abs_tol=2e-7)


def test_common_weight_scaling_keeps_optimum_and_scales_load():
    weights = [0.6, 1.4, 2.0]
    thetas = [-3.0, 0.0, 1.2]
    factor = 4.7
    scaled = [factor * w for w in weights]
    assert math.isclose(optimum(weights, thetas), optimum(scaled, thetas), rel_tol=0, abs_tol=1e-12)
    assert math.isclose(
        optimized_loss(scaled, thetas),
        factor * optimized_loss(weights, thetas),
        rel_tol=1e-12,
        abs_tol=1e-12,
    )

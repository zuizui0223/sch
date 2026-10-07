import math


def _mat_vec(matrix, vector):
    return tuple(sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix)


def _quad_form(matrix, vector):
    mv = _mat_vec(matrix, vector)
    return sum(v * m for v, m in zip(vector, mv))


def test_equilateral_three_function_weight_hessian_has_rank_two_and_is_negative_semidefinite():
    root3 = math.sqrt(3.0)
    # At equal weights for equal-curvature quadratics centered at these points,
    # z*=0 and H=I. Function gradients are -theta_i.
    gradients = (
        (-1.0, 0.0),
        (0.5, -root3 / 2.0),
        (0.5, root3 / 2.0),
    )

    # Weight Hessian is minus the Gram matrix G^T G.
    hessian = tuple(
        tuple(-sum(gi[k] * gj[k] for k in range(2)) for gj in gradients)
        for gi in gradients
    )

    # 3x3 determinant is zero, so rank is at most two.
    a, b, c = hessian[0]
    d, e, f = hessian[1]
    g, h, i = hessian[2]
    determinant = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
    assert math.isclose(determinant, 0.0, abs_tol=1e-12)

    for vector in ((1.0, 0.0, 0.0), (1.0, -1.0, 0.0), (1.0, 2.0, -3.0)):
        assert _quad_form(hessian, vector) <= 1e-12


def test_common_weight_scaling_is_curvature_flat():
    root3 = math.sqrt(3.0)
    gradients = (
        (-1.0, 0.0),
        (0.5, -root3 / 2.0),
        (0.5, root3 / 2.0),
    )
    hessian = tuple(
        tuple(-sum(gi[k] * gj[k] for k in range(2)) for gj in gradients)
        for gi in gradients
    )
    equal_weight_direction = (1.0, 1.0, 1.0)
    assert math.isclose(_quad_form(hessian, equal_weight_direction), 0.0, abs_tol=1e-12)

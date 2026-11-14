import pytest


def inv2(m):
    a, b = m[0]
    c, d = m[1]
    det = a * d - b * c
    return [[d / det, -b / det], [-c / det, a / det]]


def transpose(m):
    return [list(row) for row in zip(*m)]


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col)) for col in zip(*b)] for row in a]


def weight_curvature(g, h):
    return mm(transpose(g), mm(inv2(h), g))


def test_weight_curvature_is_invariant_under_linear_trait_change():
    # Columns are function gradients in R^2.
    g = [[1.0, -2.0, 1.0], [2.0, 1.0, -3.0]]
    h = [[4.0, 1.0], [1.0, 3.0]]
    a = [[2.0, 1.0], [0.5, 1.5]]

    a_inv = inv2(a)
    a_inv_t = transpose(a_inv)
    g_tilde = mm(a_inv_t, g)
    h_tilde = mm(a_inv_t, mm(h, a_inv))

    original = weight_curvature(g, h)
    transformed = weight_curvature(g_tilde, h_tilde)

    for row_o, row_t in zip(original, transformed):
        assert row_t == pytest.approx(row_o)


def test_isotropic_rescaling_does_not_change_weight_curvature():
    g = [[1.0, -1.0], [2.0, -2.0]]
    h = [[5.0, 0.0], [0.0, 2.0]]
    scale = [[10.0, 0.0], [0.0, 0.1]]
    scale_inv = inv2(scale)
    g_tilde = mm(transpose(scale_inv), g)
    h_tilde = mm(transpose(scale_inv), mm(h, scale_inv))

    original = weight_curvature(g, h)
    transformed = weight_curvature(g_tilde, h_tilde)
    for row_o, row_t in zip(original, transformed):
        assert row_t == pytest.approx(row_o)

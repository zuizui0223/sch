import pytest


def effective_dimension(matrix):
    trace = sum(matrix[i][i] for i in range(len(matrix)))
    frob_sq = sum(x * x for row in matrix for x in row)
    return 0.0 if frob_sq == 0.0 else trace * trace / frob_sq


def test_rank_one_curvature_has_effective_dimension_one():
    m = [[1.0, 2.0], [2.0, 4.0]]
    assert effective_dimension(m) == pytest.approx(1.0)


def test_two_equal_curvature_modes_have_effective_dimension_two():
    m = [[3.0, 0.0], [0.0, 3.0]]
    assert effective_dimension(m) == pytest.approx(2.0)


def test_unequal_two_mode_spectrum_lies_between_one_and_two():
    m = [[4.0, 0.0], [0.0, 1.0]]
    d_eff = effective_dimension(m)
    assert 1.0 < d_eff < 2.0
    assert d_eff == pytest.approx(25.0 / 17.0)


def test_zero_curvature_has_zero_effective_dimension():
    assert effective_dimension([[0.0, 0.0], [0.0, 0.0]]) == 0.0

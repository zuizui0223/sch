import pytest

from scripts.curvature_weight_nullspace import (
    curvature_weight_residual,
    infer_relative_weights_from_curvature,
)


def test_two_function_scalar_curvature_recovers_relative_weights():
    # Whitened gradients g1=1, g2=-2 -> C = g^T g.
    curvature = [[1.0, -2.0], [-2.0, 4.0]]
    out = infer_relative_weights_from_curvature(curvature)
    assert out.relative_weights == pytest.approx((2.0 / 3.0, 1.0 / 3.0))
    assert out.residual_max_abs == pytest.approx(0.0, abs=1e-12)


def test_three_function_two_dimensional_full_balance_recovers_equal_weights():
    # g1=(1,0), g2=(0,1), g3=(-1,-1), H=I.
    curvature = [
        [1.0, 0.0, -1.0],
        [0.0, 1.0, -1.0],
        [-1.0, -1.0, 2.0],
    ]
    out = infer_relative_weights_from_curvature(curvature)
    assert out.relative_weights == pytest.approx((1.0 / 3.0,) * 3)


def test_independent_weight_vector_must_annihilate_curvature():
    curvature = [[1.0, -2.0], [-2.0, 4.0]]
    assert curvature_weight_residual(curvature, [2.0, 1.0]) == pytest.approx((0.0, 0.0))
    bad = curvature_weight_residual(curvature, [1.0, 1.0])
    assert max(abs(x) for x in bad) > 0.0


def test_larger_nullspace_is_fail_closed_for_weight_identification():
    with pytest.raises(ValueError, match="one-dimensional nullspace"):
        infer_relative_weights_from_curvature(
            [
                [1.0, -1.0, 0.0],
                [-1.0, 1.0, 0.0],
                [0.0, 0.0, 0.0],
            ]
        )


def test_nonpositive_unique_null_direction_is_rejected():
    with pytest.raises(ValueError, match="not strictly positive"):
        infer_relative_weights_from_curvature([[1.0, 0.0], [0.0, 0.0]])

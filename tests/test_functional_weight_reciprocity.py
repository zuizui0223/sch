import math


def _gram(vectors):
    return tuple(
        tuple(sum(a * b for a, b in zip(vi, vj)) for vj in vectors)
        for vi in vectors
    )


def test_equilateral_quadratic_cross_weight_responses_are_reciprocal():
    root3 = math.sqrt(3.0)
    # H=I in this normalized quadratic example, so whitened gradients equal gradients.
    gradients = (
        (-1.0, 0.0),
        (0.5, -root3 / 2.0),
        (0.5, root3 / 2.0),
    )
    c = _gram(gradients)
    # residual-loss response matrix M = -C must be symmetric.
    for i in range(3):
        for j in range(3):
            assert math.isclose(-c[i][j], -c[j][i], abs_tol=1e-12)


def test_curvature_gram_recovers_pairwise_angles_and_distances():
    gradients = (
        (1.0, 0.0),
        (0.0, 2.0),
        (-1.0, 0.0),
    )
    c = _gram(gradients)

    def cosine(i, j):
        return c[i][j] / math.sqrt(c[i][i] * c[j][j])

    assert math.isclose(cosine(0, 1), 0.0, abs_tol=1e-12)
    assert math.isclose(cosine(0, 2), -1.0, abs_tol=1e-12)

    dist_sq_01 = c[0][0] + c[1][1] - 2.0 * c[0][1]
    assert math.isclose(dist_sq_01, 5.0, abs_tol=1e-12)


def test_scalar_rank_one_minor_identity():
    # Scalar shared phenotype: whitened gradients are scalar values.
    gradients = ((2.0,), (-3.0,), (5.0,))
    c = _gram(gradients)
    for i in range(3):
        for j in range(3):
            assert math.isclose(
                c[i][j] ** 2,
                c[i][i] * c[j][j],
                rel_tol=1e-12,
                abs_tol=1e-12,
            )

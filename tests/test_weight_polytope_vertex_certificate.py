import pytest


def optimized_value(weight, loss_vectors):
    return min(sum(w * y for w, y in zip(weight, loss)) for loss in loss_vectors)


def test_concave_value_on_triangle_is_bounded_below_by_vertex_minimum():
    # Finite attainable loss vectors make L*(w)=min_z w·ell(z) exactly concave.
    losses = [
        (0.0, 4.0, 3.0),
        (3.0, 0.0, 4.0),
        (4.0, 3.0, 0.0),
        (1.5, 1.5, 1.5),
    ]
    vertices = [
        (0.7, 0.2, 0.1),
        (0.1, 0.7, 0.2),
        (0.2, 0.1, 0.7),
    ]
    vertex_min = min(optimized_value(v, losses) for v in vertices)

    # Convex combinations of the three vertices cannot fall below vertex_min.
    for i in range(11):
        for j in range(11 - i):
            a = i / 10.0
            b = j / 10.0
            c = 1.0 - a - b
            w = tuple(
                a * vertices[0][k] + b * vertices[1][k] + c * vertices[2][k]
                for k in range(3)
            )
            assert optimized_value(w, losses) + 1e-12 >= vertex_min


def test_interior_value_obeys_concave_chord_lower_bound():
    losses = [(0.0, 4.0), (1.5, 1.5), (4.0, 0.0)]
    v1 = (0.8, 0.2)
    v2 = (0.2, 0.8)
    theta = 0.35
    w = (
        theta * v1[0] + (1.0 - theta) * v2[0],
        theta * v1[1] + (1.0 - theta) * v2[1],
    )
    lhs = optimized_value(w, losses)
    rhs = theta * optimized_value(v1, losses) + (1.0 - theta) * optimized_value(v2, losses)
    assert lhs + 1e-12 >= rhs


def test_common_scaling_changes_value_linearly():
    losses = [(0.0, 4.0), (1.5, 1.5), (4.0, 0.0)]
    w = (0.6, 0.4)
    scale = 2.5
    assert optimized_value((scale * w[0], scale * w[1]), losses) == pytest.approx(
        scale * optimized_value(w, losses)
    )

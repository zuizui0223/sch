from __future__ import annotations


def satisfies(point, normal, bound, tol=1e-12):
    return sum(a * y for a, y in zip(normal, point)) + tol >= bound


def test_three_facet_two_function_example_is_exact():
    # U = {y1>=0, y2>=0, y1+y2>=1}
    facets = [
        ((1.0, 0.0), 0.0),
        ((0.0, 1.0), 0.0),
        ((1.0, 1.0), 1.0),
    ]
    inside = [(0.0, 1.0), (1.0, 0.0), (0.4, 0.6), (2.0, 2.0)]
    outside = [(-0.1, 1.2), (1.2, -0.1), (0.2, 0.2)]
    for point in inside:
        assert all(satisfies(point, normal, bound) for normal, bound in facets)
    for point in outside:
        assert not all(satisfies(point, normal, bound) for normal, bound in facets)


def test_omitting_each_irredundant_facet_strictly_enlarges_region():
    facets = [
        ((1.0, 0.0), 0.0),
        ((0.0, 1.0), 0.0),
        ((1.0, 1.0), 1.0),
    ]
    witnesses = [
        (-0.5, 1.5),
        (1.5, -0.5),
        (0.0, 0.0),
    ]
    for omitted, witness in enumerate(witnesses):
        retained = [facet for i, facet in enumerate(facets) if i != omitted]
        assert all(satisfies(witness, normal, bound) for normal, bound in retained)
        normal, bound = facets[omitted]
        assert not satisfies(witness, normal, bound)


def test_redundant_support_direction_does_not_change_exact_polyhedron_on_grid():
    base = [
        ((1.0, 0.0), 0.0),
        ((0.0, 1.0), 0.0),
        ((1.0, 1.0), 1.0),
    ]
    # Valid redundant support inequality for U: 2*y1+y2 >= 1.
    augmented = base + [((2.0, 1.0), 1.0)]
    grid = [(i / 4.0, j / 4.0) for i in range(-2, 9) for j in range(-2, 9)]
    base_accept = {
        p for p in grid if all(satisfies(p, normal, bound) for normal, bound in base)
    }
    aug_accept = {
        p for p in grid if all(satisfies(p, normal, bound) for normal, bound in augmented)
    }
    assert aug_accept == base_accept

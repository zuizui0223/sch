def value(points, weight):
    return min(sum(w * y for w, y in zip(weight, point)) for point in points)


def test_raw_attainable_sets_can_differ_but_all_positive_weight_values_match():
    # (1,1) is already in the convex hull of the two endpoint loss vectors.
    # Adding it changes the raw attainable set but not the positive-weight value function.
    y = [(0.0, 2.0), (2.0, 0.0)]
    z = y + [(1.0, 1.0)]

    weights = [
        (0.1, 1.0),
        (0.5, 1.0),
        (1.0, 1.0),
        (2.0, 1.0),
        (10.0, 1.0),
    ]
    assert [value(y, w) for w in weights] == [value(z, w) for w in weights]


def test_finite_weight_design_can_miss_a_real_difference_elsewhere():
    y = [(0.0, 2.0), (2.0, 0.0)]
    # This unsupported-by-the-design point changes the global positive-weight
    # value function near equal weights, but not at the two extreme treatments.
    z = y + [(0.9, 0.9)]

    registered_design = [(10.0, 1.0), (1.0, 10.0)]
    assert [value(y, w) for w in registered_design] == [
        value(z, w) for w in registered_design
    ]

    held_out_weight = (1.0, 1.0)
    assert value(y, held_out_weight) == 2.0
    assert value(z, held_out_weight) == 1.8


def test_dominated_latent_loss_state_is_observationally_silent():
    y = [(0.0, 2.0), (2.0, 0.0)]
    z = y + [(3.0, 3.0)]

    weights = [(a, b) for a in (0.2, 1.0, 5.0) for b in (0.2, 1.0, 5.0)]
    assert all(value(y, w) == value(z, w) for w in weights)

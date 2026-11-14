import pytest

from scripts.weight_design_capacity import assess_weight_design_capacity


def test_d_dimensions_require_at_least_d_relative_directions():
    out = assess_weight_design_capacity(
        number_of_functions=4,
        independent_relative_directions=2,
        target_dimension=3,
    )
    assert not out.capacity_sufficient
    assert out.maximum_detectable_dimension == 2
    assert out.classification == "INSUFFICIENT_WEIGHT_DIRECTION_CAPACITY_FOR_DIMENSION_3"


def test_d_plus_one_functions_and_d_directions_have_capacity():
    out = assess_weight_design_capacity(
        number_of_functions=4,
        independent_relative_directions=3,
        target_dimension=3,
    )
    assert out.capacity_sufficient
    assert out.maximum_detectable_dimension == 3


def test_two_function_focal_design_cannot_identify_two_dimensional_curvature():
    out = assess_weight_design_capacity(
        number_of_functions=2,
        independent_relative_directions=1,
        target_dimension=2,
    )
    assert not out.capacity_sufficient
    assert out.maximum_detectable_dimension == 1


def test_invalid_relative_direction_count_fails_closed():
    with pytest.raises(ValueError):
        assess_weight_design_capacity(
            number_of_functions=3,
            independent_relative_directions=3,
            target_dimension=2,
        )

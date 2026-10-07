from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WeightDesignCapacity:
    number_of_functions: int
    independent_relative_directions: int
    target_dimension: int
    maximum_detectable_dimension: int
    capacity_sufficient: bool
    classification: str


def assess_weight_design_capacity(
    *,
    number_of_functions: int,
    independent_relative_directions: int,
    target_dimension: int,
) -> WeightDesignCapacity:
    if number_of_functions < 1:
        raise ValueError("number_of_functions must be positive")
    if independent_relative_directions < 0:
        raise ValueError("independent_relative_directions must be nonnegative")
    if target_dimension < 0:
        raise ValueError("target_dimension must be nonnegative")
    if independent_relative_directions > number_of_functions - 1:
        raise ValueError(
            "fixed-total relative-weight directions cannot exceed number_of_functions - 1"
        )

    capacity = min(number_of_functions - 1, independent_relative_directions)
    sufficient = capacity >= target_dimension
    classification = (
        "WEIGHT_DIRECTION_CAPACITY_SUFFICIENT"
        if sufficient
        else f"INSUFFICIENT_WEIGHT_DIRECTION_CAPACITY_FOR_DIMENSION_{target_dimension}"
    )
    return WeightDesignCapacity(
        number_of_functions=number_of_functions,
        independent_relative_directions=independent_relative_directions,
        target_dimension=target_dimension,
        maximum_detectable_dimension=capacity,
        capacity_sufficient=sufficient,
        classification=classification,
    )

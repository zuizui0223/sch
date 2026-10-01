from scripts.audit_pedicularis_minimum_new_data_frontier import build


def test_minimum_new_data_frontier_is_three_field_cohorts() -> None:
    result = build()

    assert result["n_total_f0_gates"] == 40
    assert result["n_registered_without_new_data"] == 5
    assert result["n_empirical_target_gates_requiring_new_field_calibration"] == 27
    assert result["n_sample_size_gates_computed_after_calibration"] == 8
    assert result["n_independent_field_calibration_cohorts"] == 3
    assert result["field_calibration_cohorts"] == [
        "CAL_P0", "CAL_P1", "CAL_G"
    ]


def test_empirical_targets_partition_as_8_8_11() -> None:
    result = build()
    assert result["empirical_target_gates_by_cohort"] == {
        "CAL_P0": 8,
        "CAL_P1": 8,
        "CAL_G": 11,
    }
    assert sum(result["empirical_target_gates_by_cohort"].values()) == 27


def test_cal_c_variance_inputs_partition_as_8_8_9() -> None:
    result = build()
    assert result["cal_c_variance_criteria_by_cohort"] == {
        "CAL_P0": 8,
        "CAL_P1": 8,
        "CAL_G": 9,
    }
    assert result["n_cal_c_variance_criteria"] == 25


def test_repeatability_is_nested_not_a_fourth_field_cohort() -> None:
    result = build()
    assert result["repeatability_is_additional_independent_cohort"] is False
    assert "subset" in result["repeatability_nesting_rule"]
    assert result["p0_p1_g_flower_sets_must_be_disjoint"] is True


def test_published_data_reduce_design_invention_but_not_direct_cohort_count() -> None:
    result = build()
    assert "external" in result["published_data_role"]
    assert "does not replace" in result["published_data_role"]
    assert result["status"] == (
        "THREE_FIELD_CALIBRATION_COHORTS_ARE_THE_MINIMUM_DIRECT_DATA_FRONTIER"
    )

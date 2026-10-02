from scripts.audit_pedicularis_calibration_collection_yield import build


def test_collection_yield_matches_registered_calibration_templates() -> None:
    result = build()

    assert result["status"] == (
        "CALIBRATION_COLLECTION_YIELD_MAPPED_NO_SAMPLE_SIZE_INVENTED"
    )
    assert result["n_collection_rows"] == 5
    assert result["derived_gate_yield"] == {
        "cal_a_observed_decisions": 20,
        "cal_a_measurement_noise_floors": 13,
        "cal_b_effect_or_timing_decisions": 7,
        "cal_c_pilot_sd_criteria": 25,
        "direct_f0_values": 0,
    }


def test_g_exploratory_has_highest_risk_and_largest_direct_support_yield() -> None:
    result = build()
    bundles = result["bundle_yield"]

    g = bundles["G_EXPLORATORY"]
    assert g["structural_risk"] == "HIGHEST"
    assert g["risk_priority"] == 1
    assert g["cal_a_observed_decisions"] == 6
    assert g["cal_b_effect_or_timing_decisions"] == 5
    assert g["cal_c_pilot_sd_criteria"] == 9
    assert g["decision_distributions"] == 11
    assert g["total_calibration_support_outputs"] == 20

    assert g["total_calibration_support_outputs"] > bundles[
        "P0_EXPLORATORY"
    ]["total_calibration_support_outputs"]
    assert g["total_calibration_support_outputs"] > bundles[
        "P1_EXPLORATORY"
    ]["total_calibration_support_outputs"]


def test_p0_and_repeatability_are_same_priority_and_should_be_nested() -> None:
    result = build()
    bundles = result["bundle_yield"]

    p0 = bundles["P0_EXPLORATORY"]
    rep = bundles["CAL_A_REPEATABILITY"]

    assert p0["risk_priority"] == 2
    assert rep["risk_priority"] == 2
    assert rep["cal_a_measurement_noise_floors"] == 13
    assert rep["execution_mode"] == "NEST_WITHIN_P0_CAL_A_FLOWERS"
    assert p0["cal_a_observed_decisions"] == 8
    assert p0["cal_c_pilot_sd_criteria"] == 8


def test_p1_is_required_but_lower_method_risk_than_g_or_p0() -> None:
    result = build()
    p1 = result["bundle_yield"]["P1_EXPLORATORY"]

    assert p1["risk_priority"] == 3
    assert p1["structural_risk"] == "MEDIUM"
    assert p1["cal_a_observed_decisions"] == 6
    assert p1["cal_b_effect_or_timing_decisions"] == 2
    assert p1["cal_c_pilot_sd_criteria"] == 8
    assert p1["total_calibration_support_outputs"] == 16


def test_risk_priority_is_not_mistaken_for_strict_chronology() -> None:
    result = build()
    assert result["risk_priority_order"] == [
        "G_EXPLORATORY",
        "P0_EXPLORATORY+CAL_A_REPEATABILITY",
        "P1_EXPLORATORY",
    ]
    assert "not mandatory chronological order" in result[
        "priority_interpretation"
    ]
    assert "phenology" in result["priority_interpretation"]


def test_full_package_still_requires_all_four_data_bundles_and_registry() -> None:
    result = build()
    assert result["package_completion_requirement"] == [
        "COHORT_REGISTRY",
        "CAL_A_REPEATABILITY",
        "P0_EXPLORATORY",
        "P1_EXPLORATORY",
        "G_EXPLORATORY",
    ]
    assert "all_four_data_bundles_are_still_required_for_full_package" in (
        result["claim_ceiling"]
    )

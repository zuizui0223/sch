from scripts.audit_pedicularis_method_precedents import build


def test_method_precedent_ledger_has_five_bounded_precedents() -> None:
    result = build()
    assert result["n_method_precedents"] == 5
    assert result["n_unique_dois"] == 5
    assert result["n_direct_f0_values"] == 0
    assert result["status"] == (
        "PEDICULARIS_METHOD_PRECEDENTS_RECOVERED_FOCAL_VALIDATION_STILL_REQUIRED"
    )


def test_p0_has_direct_congeneric_manipulation_precedent() -> None:
    result = build()
    assert "PEDMETH_P0_HUANG2016" in result["p0_method_precedents"]
    assert "PEDMETH_HANDLING_HUANG2013" in result["cal_a_method_precedents"]


def test_p1_has_two_independent_congeneric_supplementation_precedents() -> None:
    result = build()
    assert set(result["p1_supplementation_precedents"]) == {
        "PEDMETH_P1_DAI2017",
        "PEDMETH_P1_YANG2005",
    }
    assert "PEDMETH_HANDLING_HUANG2013" in result["p1_method_precedents"]


def test_same_species_water_experiment_is_not_promoted_to_independent_g() -> None:
    result = build()
    assert result["same_species_precedents"] == ["PEDMETH_G_WATER2015"]
    assert "same_species_water_drainage_is_not_independent_G" in (
        result["claim_ceiling"]
    )


def test_method_precedents_leave_focal_direct_empirical_gaps_open() -> None:
    result = build()
    assert set(result["registered_method_gaps_after_recovery"]) == {
        "P_rex_multi_level_realized_exsertion_manipulation",
        "P_rex_same_flower_repeatability",
        "P_rex_pollen_supplementation_effect",
        "P_rex_independent_seed_predator_exclusion",
        "P_rex_independent_G_timing_window",
    }

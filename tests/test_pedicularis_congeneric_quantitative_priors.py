from scripts.audit_pedicularis_congeneric_quantitative_priors import build


def test_congeneric_quantitative_ledger_has_27_rows_across_six_species() -> None:
    result = build()
    assert result["n_quantitative_prior_rows"] == 27
    assert result["n_species"] == 6
    assert result["species_counts"] == {
        "Pedicularis densispica": 3,
        "Pedicularis dunniana": 4,
        "Pedicularis monbeigiana": 10,
        "Pedicularis palustris": 4,
        "Pedicularis siphonantha": 1,
        "Pedicularis tricolor": 5,
    }


def test_congeneric_quantitative_priors_never_become_direct_p_rex_or_f0() -> None:
    result = build()
    assert result["n_direct_P_rex_effect_rows"] == 0
    assert result["n_direct_F0_values"] == 0
    assert result["status"] == (
        "CONGENERIC_QUANTITATIVE_PRIORS_RECOVERED_P_REX_EFFECT_STILL_REQUIRED"
    )


def test_p1_contains_null_and_large_positive_effect_precedents() -> None:
    result = build()
    assert "PCQ_P1_MONB2005_SUPP_TEST" in result["near_zero_effect_precedents"]
    assert {
        "PCQ_P1_MONB2011_PURE_SPARSE",
        "PCQ_P1_MONB2011_PURE_DENSE",
        "PCQ_P1_MONB2011_MIXED_SPARSE",
        "PCQ_P1_MONB2011_MIXED_DENSE",
    } <= set(result["relative_effect_rows"])
    assert "null responses" in result["p1_effect_range_statement"]
    assert "2.1x" in result["p1_effect_range_statement"]


def test_p1_design_families_keep_whole_plant_separate_from_paired_designs() -> None:
    result = build()
    families = result["p1_design_families"]
    assert "PCQ_P1_MONB2011_SEED_F" in families["whole_plant_supplementation"]
    assert "PCQ_P1_MONB2005_SUPP_TEST" in (
        families["within_plant_or_flower_level_supplementation"]
    )
    assert "PCQ_P1_DENSISPICA_PL_S" in (
        families["patch_context_supplementation"]
    )


def test_p0_mean_se_rows_are_directly_reported_congeneric_handling_data() -> None:
    result = build()
    assert {
        "PCQ_P0_TRICOLOR_VISIT_SHORT",
        "PCQ_P0_TRICOLOR_VISIT_CTRL",
        "PCQ_P0_TRICOLOR_SEED_SHORT",
        "PCQ_P0_TRICOLOR_SEED_CTRL",
        "PCQ_P0_TRICOLOR_COROLLA",
    } >= set(result["exact_mean_se_rows"])
    assert len(result["exact_mean_se_rows"]) >= 4


def test_dunniana_adds_quantitative_hand_pollination_pollen_limitation() -> None:
    result = build()
    family = result["p1_design_families"][
        "bagged_or_hand_pollination_pollen_limitation"
    ]
    assert set(family) == {
        "PCQ_P1_DUNN2005_NATURAL",
        "PCQ_P1_DUNN2005_HAND_SELF",
        "PCQ_P1_DUNN2005_HAND_CROSS",
        "PCQ_P1_DUNN2005_POLLEN_LIMIT_F",
    }
    assert "PCQ_P1_DUNN2005_HAND_CROSS" in result["p1_prior_rows"]
    assert (
        "hand_pollination_pollen_limitation_is_not_identical_to_open_supplementation"
        in result["claim_ceiling"]
    )


def test_palustris_adds_whole_plant_pollinator_dependence_and_context_prior() -> None:
    result = build()
    family = result["p1_design_families"][
        "whole_plant_exclosure_hand_natural_context"
    ]
    assert set(family) == {
        "PCQ_P1_PALUSTRIS_EXCLOSURE",
        "PCQ_P1_PALUSTRIS_SELF_COMPAT_LOW",
        "PCQ_P1_PALUSTRIS_SELF_COMPAT_HIGH",
        "PCQ_P1_PALUSTRIS_DISPLAY",
    }
    assert "PCQ_P1_PALUSTRIS_EXCLOSURE" in result["p1_prior_rows"]
    assert (
        "whole_plant_seed_production_and_capsule_level_pollen_limitation_can_diverge"
        in result["claim_ceiling"]
    )

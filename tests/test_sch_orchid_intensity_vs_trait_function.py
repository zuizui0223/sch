from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_sch_orchid_intensity_vs_trait_function import (
    read, build, read_guild, audit_guild,
)
from scripts.audit_sch_gymnadenia_factorial_reversal import read as read_2015


def test_2014_real_multiyear_pl_dissociation_is_recorded_without_inventing_rows():
    result = build(read(), read_2015())
    assert result["status"] == (
        "PUBLISHED_MULTISEASON_INTENSITY_FUNCTION_DISSOCIATION_RECORDED"
    )
    sources = result["sources"]
    assert sources[0]["Gymnadenia_population_years"] == 9
    assert sources[0]["Dactylorhiza_population_years"] == 5
    assert sources[0]["independent_populations_per_species"] == 2
    assert sources[0]["raw_spreadsheet_retrieved"] is False
    facts = result["2014_published_results"]
    assert facts["Gymnadenia_abs_net_selection_associated_with_PL"] is True
    assert facts["Gymnadenia_abs_pollinator_mediated_selection_associated_with_PL_detected"] is False
    assert facts["Dactylorhiza_abs_pollinator_mediated_selection_associated_with_PL_detected"] is False
    assert facts["Gymnadenia_spur_pollinator_mediation_stronger_than_attraction_traits"] is True
    assert facts["Gymnadenia_multiyear_flowering_phenology_analyzed"] is False
    assert facts["pollen_limitation_alone_sufficient_to_explain_selected_trait"] == "NOT_ESTABLISHED"
    assert "no_detected_association_does_not_imply_zero_population_PL_effect" in result["claim_ceiling"]


def test_cross_source_functional_mappings_preserve_original_2015_point_estimates():
    result = build(read(), read_2015())
    a = result["2015_same_experiment_point_component_contrasts"]["flowering_start"]
    b = result["2015_same_experiment_point_component_contrasts"]["spur_length"]
    assert a["2015_pollinator_selection_delta_with_natural_herbivory"] == pytest.approx(.1558)
    assert a["2015_pollinator_selection_delta_with_herbivores_excluded"] == pytest.approx(.160)
    assert a["2015_herbivore_selection_delta_with_open_pollination"] == pytest.approx(-.0982)
    assert a["2015_herbivore_selection_delta_with_hand_pollination"] == pytest.approx(-.094)
    assert b["2015_pollinator_selection_delta_with_natural_herbivory"] == pytest.approx(.097)
    assert b["2015_pollinator_selection_delta_with_herbivores_excluded"] == pytest.approx(.119)
    assert b["2015_herbivore_selection_delta_with_open_pollination"] == pytest.approx(.103)
    assert b["2015_herbivore_selection_delta_with_hand_pollination"] == pytest.approx(.125)
    assert a["original_cell_fitness_standardization_matched_verified"] is False
    assert b["treatment_cell_point_contrast_not_pure_function_optimum"] is True


@pytest.mark.parametrize(
    ("species", "outcome", "field", "alteration", "match"),
    [
        ("Gymnadenia conopsea", "delta_beta_pollinator_time_series",
         "source_result", "SIGNIFICANT_REVERSAL", "published direction"),
        ("Gymnadenia conopsea", "delta_beta_pollinator_time_series",
         "trait_set", "spur_length", "trait eligibility"),
        ("Gymnadenia conopsea", "delta_beta_pollinator_trait_comparison",
         "population_year_units", "14", "population-year"),
        ("Dactylorhiza lapponica", "abs_pollinator_mediated_selection_vs_PL",
         "independent_populations", "5", "population-year"),
        ("Gymnadenia conopsea", "abs_open_pollinated_net_selection_vs_PL",
         "raw_data_access", "DRYAD_WORKBOOK_INGESTED", "must not be reported ingested"),
        ("Gymnadenia conopsea", "abs_open_pollinated_net_selection_vs_PL",
         "observation_unit", "plant", "population-year"),
    ],
)
def test_source_receipt_rejects_false_temporal_replication_or_data_claims(
    species, outcome, field, alteration, match
):
    rows = deepcopy(read())
    row = next(r for r in rows
               if (r["species"], r["selected_outcome"]) == (species, outcome))
    row[field] = alteration
    with pytest.raises(ValueError, match=match):
        build(rows, read_2015())


def test_source_ledger_must_be_complete_and_no_duplicate_traits_as_studies():
    rows = read()
    with pytest.raises(ValueError, match="incomplete"):
        build(rows[1:], read_2015())
    with pytest.raises(ValueError, match="duplicate"):
        build(rows+[deepcopy(rows[0])], read_2015())


def test_no_causal_functional_mapping_or_multiyear_phenology_replication_claim():
    result = build(read(), read_2015())
    assert result["2014_published_results"][
        "functional_trait_response_causally_identified_from_PL_regression"
    ] is False
    assert "2014_multiyear_Gymnadenia_did_not_include_flowering_start" in (
        result["claim_ceiling"]
    )
    assert "response_curve_mapping_is_mechanistic_hypothesis_not_measured_cause" in (
        result["claim_ceiling"]
    )
    assert result["sources"][1]["same_site_year_match_to_2014_series_verified"] is False



def test_real_guild_exclusion_mean_service_and_trait_selection_are_distinct() -> None:
    r = build(read(), read_2015())
    guild = r["independent_published_guild_exclusion_evidence"]
    assert [q["doi"] for q in guild["source_programmes"]] == [
        "10.1890/11-2044.1", "10.1111/nph.13555"
    ]
    assert guild["2012_diurnal_removal_mean_seed_production_decreased_both_pops"]
    assert guild["2012_nocturnal_removal_mean_seed_production_decrease_detected"] is False
    assert guild["2012_both_guilds_contributed_to_flower_trait_selection"] is True
    assert guild["2012_direction_of_selection_consistent_across_guild_treatments"] is True
    assert guild["2015_nocturnal_guild_selected_longer_spur_in_guild_subset"] is True
    assert guild["2015_guild_specific_correlational_trait_combinations"] is True
    assert guild["guild_specific_selection_coefficients_recovered"] is False
    assert "non_detected_nocturnal_seed_loss_is_not_zero_nocturnal_service" in guild["claim_ceiling"]


@pytest.mark.parametrize(
    ("outcome", "field", "replacement", "match"),
    [
        ("diurnal_exclusion_effect_on_mean_seed_production", "reported_result",
         "NOT_SIGNIFICANT", "published result"),
        ("nocturnal_exclusion_effect_on_mean_seed_production", "raw_estimates_recovered",
         "YES", "remain qualitative"),
        ("guild_effect_on_spur_length_selection", "populations_total",
         "2", "scope drift"),
        ("guild_effect_on_correlational_trait_selection", "source_doi",
         "10.1000/none", "unknown or duplicate"),
    ]
)
def test_guild_source_audit_rejects_invented_results_or_replicates(
    outcome, field, replacement, match
):
    rows = deepcopy(read_guild())
    cell = next(x for x in rows if x["outcome"] == outcome)
    cell[field] = replacement
    with pytest.raises(ValueError, match=match):
        audit_guild(rows)


def test_guild_source_row_loss_and_duplicate_are_not_independent_systems() -> None:
    rows = read_guild()
    with pytest.raises(ValueError, match="incomplete"):
        audit_guild(rows[:-1])
    with pytest.raises(ValueError, match="duplicate"):
        audit_guild(rows + [deepcopy(rows[0])])

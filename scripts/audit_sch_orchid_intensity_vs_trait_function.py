"""Audit the 2014 real multiyear PL-versus-selection contrast and its 2015
single-season factorial interpretation, without inventing Dryad rows.

Only reported primary-paper qualitative results are used for 2014. Source-
reported population-year n is not independent population or study replication.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from scripts.audit_sch_gymnadenia_factorial_reversal import (
    read as read_2015,
    build as build_2015,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/SCH_GYMNADENIA_INTERACTION_INTENSITY_FUNCTIONAL_RESPONSE_2014_V1.csv"
DOI = "10.1111/evo.12405"
GUILD_SOURCE = ROOT / "data/SCH_GYMNADENIA_GUILD_SERVICE_VS_SELECTION_V1.csv"
GUILD_EXPECTED = {
    ("10.1890/11-2044.1", "diurnal_exclusion_effect_on_mean_seed_production"):
        "SIGNIFICANT_DECREASE_IN_BOTH_POPULATIONS",
    ("10.1890/11-2044.1", "nocturnal_exclusion_effect_on_mean_seed_production"):
        "NO_DETECTED_DECREASE_IN_BOTH_POPULATIONS",
    ("10.1890/11-2044.1", "diurnal_and_nocturnal_trait_selection"):
        "BOTH_GUILDS_SELECTION_WITH_CONSISTENT_DIRECTION_AND_VARIABLE_STRENGTH",
    ("10.1111/nph.13555", "guild_effect_on_spur_length_selection"):
        "ONLY_NOCTURNAL_LONGER_SPUR_SELECTION_REPORTED_IN_SOURCE",
    ("10.1111/nph.13555", "guild_effect_on_correlational_trait_selection"):
        "GUILDS_SELECT_DIFFERENT_MULTITRAIT_COMBINATIONS",
}
G = "Gymnadenia conopsea"
D = "Dactylorhiza lapponica"
OUTCOMES = {
    (G, "abs_pollinator_mediated_selection_vs_PL"):
        "NO_DETECTED_RELATIONSHIP",
    (G, "abs_open_pollinated_net_selection_vs_PL"):
        "POSITIVE_RELATIONSHIP_REPORTED",
    (G, "delta_beta_pollinator_trait_comparison"):
        "STRONGER_THAN_OTHER_THREE_TRAITS_TUKEY_P_LT_0_01",
    (G, "delta_beta_pollinator_time_series"):
        "NOT_ANALYSED_FOR_DATA_QUALITY",
    (D, "abs_pollinator_mediated_selection_vs_PL"):
        "NO_DETECTED_RELATIONSHIP",
    (D, "abs_open_pollinated_net_selection_vs_PL"):
        "NO_DETECTED_RELATIONSHIP",
}
G_TRAITS = {"plant_height", "flower_number", "corolla_size", "spur_length"}
D_TRAITS = G_TRAITS | {"flowering_start"}


def read(path: Path = SOURCE) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        data = list(csv.DictReader(f))
    if not data:
        raise ValueError("2014 orchid source ledger empty")
    return data


def read_guild(path: Path = GUILD_SOURCE) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        out = list(csv.DictReader(f))
    if not out:
        raise ValueError("guild source table empty")
    return out


def audit_guild(rows: list[dict[str, str]]) -> dict:
    found = set()
    for row in rows:
        key = (row["source_doi"], row["outcome"])
        if key not in GUILD_EXPECTED or key in found:
            raise ValueError("unknown or duplicate guild-source result")
        found.add(key)
        year, n_pops, n_guild = (
            (2012, 2, 2) if key[0] == "10.1890/11-2044.1"
            else (2015, 4, 2)
        )
        if (
            int(row["year"]) != year
            or int(row["populations_total"]) != n_pops
            or int(row["populations_with_guild_manipulation"]) != n_guild
        ):
            raise ValueError("guild source population/manipulation scope drift")
        if row["reported_result"] != GUILD_EXPECTED[key]:
            raise ValueError("guild original published result identity drift")
        if (
            row["source_evidence"] != "PRIMARY_PUBLISHED_ABSTRACT"
            or row["raw_estimates_recovered"] != "NO"
        ):
            raise ValueError("guild effects remain qualitative until full tables")
    if found != set(GUILD_EXPECTED) or len(rows) != len(GUILD_EXPECTED):
        raise ValueError("guild source evidence set incomplete")
    return {
        "source_programmes": [
            {"doi": "10.1890/11-2044.1", "year": 2012,
             "population_count": 2, "guild_experiment_populations": 2},
            {"doi": "10.1111/nph.13555", "year": 2015,
             "population_count": 4, "guild_experiment_populations": 2},
        ],
        "2012_diurnal_removal_mean_seed_production_decreased_both_pops": True,
        "2012_nocturnal_removal_mean_seed_production_decrease_detected": False,
        "2012_both_guilds_contributed_to_flower_trait_selection": True,
        "2012_direction_of_selection_consistent_across_guild_treatments": True,
        "2015_nocturnal_guild_selected_longer_spur_in_guild_subset": True,
        "2015_guild_specific_correlational_trait_combinations": True,
        "guild_specific_selection_coefficients_recovered": False,
        "interpretation": (
            "The guild required for mean seed production need not be the "
            "only guild contributing to floral trait selection."
        ),
        "claim_ceiling": [
            "non_detected_nocturnal_seed_loss_is_not_zero_nocturnal_service",
            "2012_and_2015_source_programmes_may_share_sites_not_independent_field_replicates",
            "no_risk_or_absolute_visitor_effect_sizes_extracted",
            "not_proof_2012_to_2015_evolutionary_direction_changed",
            "does_not_identify_function_specific_optimum_or_trait_intervention",
        ],
    }


def build(
    rows: list[dict[str, str]],
    cells_2015: list[dict[str, str]],
    guild_rows: list[dict[str, str]] | None = None,
) -> dict:
    seen = set()
    for row in rows:
        species = row["species"]
        outcome = row["selected_outcome"]
        key = (species, outcome)
        if key not in OUTCOMES or key in seen:
            raise ValueError("2014 source has unknown or duplicate species/outcome")
        seen.add(key)
        if row["source_doi"] != DOI or row["study_year"] != "2014":
            raise ValueError("2014 source DOI/year drift")
        if row["observation_unit"] != "population_year":
            raise ValueError("2014 observation unit is population-year")
        n_pops = int(row["independent_populations"])
        n_py = int(row["population_year_units"])
        if n_pops != 2 or n_py != (9 if species == G else 5):
            raise ValueError("2014 source population-year or population count drift")
        traits = set(row["trait_set"].split("|"))
        expected_traits = (
            {"flowering_start"} if key == (G, "delta_beta_pollinator_time_series")
            else {"spur_length"} if key == (G, "delta_beta_pollinator_trait_comparison")
            else G_TRAITS if species == G else D_TRAITS
        )
        if traits != expected_traits:
            raise ValueError("2014 trait eligibility or phenology exclusion drift")
        if row["source_result"] != OUTCOMES[key]:
            raise ValueError("2014 published direction/non-detection changed")
        if row["raw_data_access"] != "DRYAD_WORKBOOK_NOT_INGESTED":
            raise ValueError("2014 raw data must not be reported ingested")
        if not row["source_evidence_level"].startswith(("ORIGINAL_PRIMARY_TEXT", "EXPLICIT_ORIGINAL_METHODS")):
            raise ValueError("2014 evidence level must remain primary-text bounded")
    if seen != set(OUTCOMES) or len(rows) != len(OUTCOMES):
        raise ValueError("2014 six-source-claim ledger incomplete")

    guild = audit_guild(read_guild() if guild_rows is None else guild_rows)
    prior = build_2015(cells_2015)
    if prior["n_source_treatment_cells"] != 20:
        raise ValueError("2015 factorial source lacks complete treatment cells")
    pairwise = {}
    for trait in ("flowering_start", "spur_length"):
        cell = prior["trait_results"][trait]["treatment_gradients"]
        # Flower-level natural selection contrasts with the other factor held
        # constant; these are 2015 point estimates, not 2014 source values.
        p_open_h = cell["C+H"]["beta"] - cell["HP+H"]["beta"]
        p_excl_h = cell["C+E"]["beta"] - cell["HP+E"]["beta"]
        h_open_p = cell["C+H"]["beta"] - cell["C+E"]["beta"]
        h_supp_p = cell["HP+H"]["beta"] - cell["HP+E"]["beta"]
        pairwise[trait] = {
            "2015_pollinator_selection_delta_with_natural_herbivory": p_open_h,
            "2015_pollinator_selection_delta_with_herbivores_excluded": p_excl_h,
            "2015_herbivore_selection_delta_with_open_pollination": h_open_p,
            "2015_herbivore_selection_delta_with_hand_pollination": h_supp_p,
            "original_cell_fitness_standardization_matched_verified": False,
            "treatment_cell_point_contrast_not_pure_function_optimum": True,
        }
    return {
        "analysis": "sch_orchid_pollen_limitation_vs_trait_functional_significance_v1",
        "sources": [
            {"doi": DOI, "publication": "Sletvold_Agren_2014_Evolution",
             "n_species": 2, "independent_populations_per_species": 2,
             "Gymnadenia_population_years": 9, "Dactylorhiza_population_years": 5,
             "raw_dataset": "10.5061/dryad.30dn3",
             "raw_spreadsheet_retrieved": False},
            {"doi": "10.1890/14-0119.1",
             "publication": "Sletvold_Moritz_Agren_2015_Ecology",
             "n_source_treatment_cells": 20,
             "same_site_year_match_to_2014_series_verified": False},
        ],
        "2014_published_results": {
            "Gymnadenia_abs_net_selection_associated_with_PL": True,
            "Gymnadenia_abs_pollinator_mediated_selection_associated_with_PL_detected": False,
            "Dactylorhiza_abs_pollinator_mediated_selection_associated_with_PL_detected": False,
            "Gymnadenia_spur_pollinator_mediation_stronger_than_attraction_traits": True,
            "Gymnadenia_multiyear_flowering_phenology_analyzed": False,
            "pollen_limitation_alone_sufficient_to_explain_selected_trait": "NOT_ESTABLISHED",
            "functional_trait_response_causally_identified_from_PL_regression": False,
        },
        "2015_same_experiment_point_component_contrasts": pairwise,
        "independent_published_guild_exclusion_evidence": guild,
        "ecological_discriminator": {
            "interaction_intensity": "population_year_mean_pollen_limitation",
            "functional_significance": "trait_specific_gradient_of_pollen_delivery_or_fitness",
            "causal_test_needed": (
                "At matched population-year pollen limitation, measure randomized "
                "trait-specific pollen-transfer responses and pollinator guilds; "
                "predict mediated selection from response-curve slopes, not PL alone."
            ),
            "source_claim": (
                "Within-species PL was not a detectable predictor of mediated "
                "selection in the 2014 source; the 2015 factorial source shows "
                "opposed phenology but reinforcing spur selection."
            ),
        },
        "claim_ceiling": [
            "n_population_years_not_independent_species_or_population_replicates",
            "no_detected_association_does_not_imply_zero_population_PL_effect",
            "2014_multiyear_Gymnadenia_did_not_include_flowering_start",
            "2015_phenology_sign_change_has_no_multiyear_replication_from_2014",
            "2014_and_2015_sampling_frames_cannot_be_merged_as_one_experiment",
            "response_curve_mapping_is_mechanistic_hypothesis_not_measured_cause",
            "2014_Dryad_xlsx_not_ingested_no_numeric_reanalysis_claim",
            "guild_exclusion_reports_not_raw_risk_or_selection_effect_sizes",
            "2012_and_2015_guild_studies_not_proof_of_longitudinal_selection_reversal",
            "trait_directional_selection_not_SCH_function_specific_optimum",
        ],
        "status": "PUBLISHED_MULTISEASON_INTENSITY_FUNCTION_DISSOCIATION_RECORDED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    receipt = build(read(args.source), read_2015())
    s = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(s, encoding="utf-8")
    else:
        print(s, end="")


if __name__ == "__main__":
    main()

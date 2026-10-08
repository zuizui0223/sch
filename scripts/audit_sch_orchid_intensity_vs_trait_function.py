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


def build(rows: list[dict[str, str]], cells_2015: list[dict[str, str]]) -> dict:
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

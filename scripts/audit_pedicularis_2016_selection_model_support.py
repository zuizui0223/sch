from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data" / "PEDICULARIS_2016_SELECTION_MODEL_AICC_V1.csv"
DOI = "10.1093/aob/mcw097"

# Exact two-decimal table AICc values, except the full final-seed model (3 decimals).
# These are source-printed values, not row-level refits or new measurements.
EXPECTED = {
    "pollen_receipt": {"full": 1728.99, "interaction": 1714.83, "best": 1700.10},
    "seed_predation": {"full": -128.48, "interaction": -151.03, "best": -156.11},
    "initial_seed_set": {"full": -452.54, "interaction": -480.30, "best": -493.44},
    "final_viable_seeds": {"full": -971.091, "best_interaction": -1000.03},
}
FULL_POPULATIONS = set(range(1, 15))
LINKED_POPULATIONS = {1, 3, 5, 8, 9, 10, 11}
PROSE_REPORTED_RELATIVE = {
    "pollen_receipt": 0.0068,
    "seed_predation": 0.3450,
    "initial_seed_set": 0.0120,
}


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError("Pedicularis source model ledger has no header")
        rows = [{k: (v or "").strip() for k, v in row.items()} for row in reader]
    if not rows:
        raise ValueError("Pedicularis source model ledger is empty")
    return rows


def _population_set(encoded: str) -> set[int]:
    if encoded == "1-14":
        return FULL_POPULATIONS
    try:
        values = {int(x) for x in encoded.split("|")}
    except ValueError as exc:
        raise ValueError("unparseable 2016 population subset") from exc
    return values


def build(rows: list[dict[str, str]]) -> dict:
    grouped: dict[str, dict[str, float]] = {}
    scopes: dict[str, set[int]] = {}
    for row in rows:
        endpoint, key = row["endpoint"], row["model_key"]
        if endpoint not in EXPECTED or key not in EXPECTED[endpoint]:
            raise ValueError("unexpected 2016 published model endpoint or candidate")
        if row["source_doi"] != DOI:
            raise ValueError("original 2016 source DOI mismatch")
        if key in grouped.get(endpoint, {}):
            raise ValueError("duplicate published model candidate")
        try:
            aicc = float(row["reported_aicc"])
            declared_n = int(row["n_populations"])
        except (ValueError, TypeError) as exc:
            raise ValueError("published AICc and population count must be numeric") from exc
        if not math.isfinite(aicc) or abs(aicc - EXPECTED[endpoint][key]) > 1e-6:
            raise ValueError("published Table 1 AICc value changed")
        population_set = _population_set(row["source_populations"])
        expected_population_set = (
            LINKED_POPULATIONS if endpoint in {"seed_predation", "final_viable_seeds"}
            else FULL_POPULATIONS
        )
        if population_set != expected_population_set or declared_n != len(population_set):
            raise ValueError("2016 endpoint-specific linked-population scope changed")
        if endpoint in scopes and scopes[endpoint] != population_set:
            raise ValueError("models within one endpoint use inconsistent populations")
        scopes[endpoint] = population_set
        grouped.setdefault(endpoint, {})[key] = aicc

    if len(rows) != 11 or set(grouped) != set(EXPECTED) or any(
        set(grouped[endpoint]) != set(EXPECTED[endpoint]) for endpoint in EXPECTED
    ):
        raise ValueError("2016 Table 1 candidate model inventory incomplete")

    model_support: dict[str, dict] = {}
    for endpoint, candidates in grouped.items():
        best_aicc = min(candidates.values())
        rel = {
            key: math.exp(-0.5 * (aicc - best_aicc))
            for key, aicc in candidates.items()
        }
        total = sum(rel.values())
        model_support[endpoint] = {
            "n_original_population_units": len(scopes[endpoint]),
            "population_ids": sorted(scopes[endpoint]),
            "aicc_comparison_is_within_endpoint_only": True,
            "best_aicc": best_aicc,
            "models": {
                key: {
                    "reported_table_aicc": aicc,
                    "delta_aicc": aicc - best_aicc,
                    "relative_likelihood_to_endpoint_best": rel[key],
                    "conditional_candidate_akaike_weight": rel[key] / total,
                }
                for key, aicc in sorted(candidates.items())
            },
        }

    comparison_notes = {}
    for endpoint, source_prose_number in PROSE_REPORTED_RELATIVE.items():
        calculated = model_support[endpoint]["models"]["interaction"][
            "relative_likelihood_to_endpoint_best"
        ]
        comparison_notes[endpoint] = {
            "published_prose_relative_likelihood": source_prose_number,
            "computed_from_published_table_aicc": calculated,
            "values_disagree_beyond_table_rounding": (
                not math.isclose(source_prose_number, calculated, rel_tol=0.01)
            ),
            "action": "USE_TABLE_BASED_SUPPORT_FOR_THIS_LEDGER; DO_NOT_EDIT_SOURCE",
        }

    return {
        "analysis": "pedicularis_rex_2016_original_AICc_evidence_v1",
        "source_doi": DOI,
        "n_original_published_model_candidates": len(rows),
        "model_support_by_endpoint": model_support,
        "prose_table_relative_likelihood_check": comparison_notes,
        "biological_discriminator": {
            "pollination_component_model_best_omits_population_by_z": True,
            "predation_component_model_best_omits_population_by_z": True,
            "initial_seed_model_best_omits_population_by_pollen": True,
            "final_viable_seed_best_retains_population_interactions": True,
            "support_statement": (
                "The source model shortlist supports simpler input-response models "
                "but a context-interactive final-fitness model."
            ),
            "candidate_hypothesis": (
                "A geographic mosaic in realized reproductive selection can emerge "
                "through context-dependent translation of pollen/attack into viable "
                "seeds even without demonstrated geographic shifts in consumer "
                "trait-response slopes."
            ),
            "hypothesis_directly_identified_by_table_only": False,
        },
        "method_limits": [
            "models_from_different_endpoints_have_incomparable_AICc_values",
            "7_linked_predation_fitness_populations_not_14_pollen_populations",
            "full_and_best_final_seed_models_both_contain_population_interactions",
            "no_reported_noninteraction_AICc_for_final_seeds",
            "absence_of_selected_interaction_does_not_prove_slope_equivalence",
            "published_model_selection_may_reflect_sample_size_and_model_search",
            "table_based_support_is_not_independent_raw_data_refitting",
            "covariance_and_causal_paths_not_identified_by_aggregate_AICc",
            "no_causal_randomized_z_P_G_or_pure_function_optimum",
        ],
        "status": "PUBLISHED_FITNESS_TRANSLATION_MOSAIC_MODEL_SUPPORT_RECOVERED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Recover published AICc evidence about P. rex context-dependent fitness translation"
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(read(args.source))
    payload = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

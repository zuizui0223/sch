from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_2016_selection_model_support import (
    DEFAULT_SOURCE,
    build,
    read,
)


def test_published_2016_model_table_has_original_11_candidates_and_grains() -> None:
    result = build(read(DEFAULT_SOURCE))
    assert result["n_original_published_model_candidates"] == 11
    models = result["model_support_by_endpoint"]
    assert models["pollen_receipt"]["n_population_labels_in_table_note"] == 14
    assert models["initial_seed_set"]["n_population_labels_in_table_note"] == 14
    assert models["seed_predation"]["population_ids"] == [1, 3, 5, 8, 9, 10, 11]
    assert models["final_viable_seeds"]["population_ids"] == [1, 3, 5, 8, 9, 10, 11]
    assert all(x["aicc_comparison_is_within_endpoint_only"] for x in models.values())
    assert models["initial_seed_set"]["underlying_n_population_units_independently_verified"] is False
    assert models["initial_seed_set"]["initial_seed_scope_ambiguous"] is True
    assert result["source_scope_discrepancies"][0]["resolved_from_raw_data"] is False
    assert "initial_seed_set_n_population_discrepancy_supplement_12_vs_table_note_14" in (
        result["method_limits"]
    )


def test_source_table_support_is_recomputed_not_copied_from_paper_prose() -> None:
    result = build(read(DEFAULT_SOURCE))
    models = result["model_support_by_endpoint"]
    expected = {
        "pollen_receipt": (14.73, 0.000633025),
        "seed_predation": (5.08, 0.0788664),
        "initial_seed_set": (13.14, 0.0014018),
    }
    for endpoint, (delta, likelihood) in expected.items():
        comparison = models[endpoint]["models"]["interaction"]
        assert comparison["delta_aicc"] == pytest.approx(delta)
        assert comparison["relative_likelihood_to_endpoint_best"] == pytest.approx(
            likelihood, rel=1e-5
        )
        assert result["prose_table_relative_likelihood_check"][endpoint][
            "values_disagree_beyond_table_rounding"
        ] is True
        weights = [v["conditional_candidate_akaike_weight"]
                   for v in models[endpoint]["models"].values()]
        assert sum(weights) == pytest.approx(1.0)

    # Do not misconstrue a final-seed full-vs-best model comparison as
    # evidence FOR including interactions: both listed candidates have them.
    best_final = models["final_viable_seeds"]["models"]["best_interaction"]
    alternative = models["final_viable_seeds"]["models"]["full"]
    assert best_final["reported_table_aicc"] == pytest.approx(-1000.03)
    assert alternative["delta_aicc"] == pytest.approx(28.939)
    assert "full_and_best_final_seed_models_both_contain_population_interactions" in (
        result["method_limits"]
    )
    assert "no_reported_noninteraction_AICc_for_final_seeds" in result["method_limits"]


def test_ecological_claim_does_not_promote_observational_tables_to_identified_cause() -> None:
    result = build(read(DEFAULT_SOURCE))
    bio = result["biological_discriminator"]
    assert bio["final_viable_seed_best_retains_population_interactions"] is True
    assert bio["predation_component_model_best_omits_population_by_z"] is True
    assert bio["hypothesis_directly_identified_by_table_only"] is False
    assert result["status"] == "PUBLISHED_FITNESS_TRANSLATION_MOSAIC_MODEL_SUPPORT_RECOVERED"
    assert "absence_of_selected_interaction_does_not_prove_slope_equivalence" in (
        result["method_limits"]
    )


@pytest.mark.parametrize(
    ("endpoint", "model_key", "column", "replacement", "message"),
    [
        ("seed_predation", "best", "reported_aicc", "-145.0", "AICc value changed"),
        ("pollen_receipt", "best", "source_populations", "1|3|5|8|9|10|11", "scope changed"),
        ("final_viable_seeds", "full", "source_doi", "10.1000/example", "DOI mismatch"),
        ("initial_seed_set", "interaction", "n_populations", "7", "scope changed"),
    ],
)
def test_original_source_contract_rejects_corruption(
    endpoint: str, model_key: str, column: str, replacement: str, message: str
) -> None:
    rows = deepcopy(read(DEFAULT_SOURCE))
    row = next(r for r in rows
               if r["endpoint"] == endpoint and r["model_key"] == model_key)
    row[column] = replacement
    with pytest.raises(ValueError, match=message):
        build(rows)


def test_duplicate_or_missing_published_model_is_rejected() -> None:
    rows = read(DEFAULT_SOURCE)
    with pytest.raises(ValueError, match="duplicate"):
        build(rows + [deepcopy(rows[0])])
    with pytest.raises(ValueError, match="inventory incomplete"):
        build(rows[1:])

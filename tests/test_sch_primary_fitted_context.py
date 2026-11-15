"""Fail-closed original-primary author tests and mismatched-estimand controls."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from scripts.audit_sch_primary_fitted_context import PAIRS, BEANS, STINCH, read_csv, run

ROOT = Path(__file__).resolve().parents[1]


def audited():
    return run(read_csv(PAIRS), read_csv(BEANS), read_csv(STINCH))


def test_original_author_interactions_not_marginal_wald_reconstruction():
    r = audited()
    assert r["compiled_matched_pair_denominator_unchanged"] == 137
    assert r["independent_2015_biological_papers_in_this_audit"] == 1
    assert r["author_fitted_2015_interaction_tests"] == 8
    assert r["n_nominal_direct_p_below_0_05"] == 4
    assert r["n_direct_p_below_0_05_over_eight"] == 2
    assert r["n_direct_p_below_0_05_over_137"] == 1
    passed = {(x["study"], x["trait"]) for x in r["direct_source_tests"]
              if x["source_eight_tests_bonferroni_0_05"]}
    assert passed == {("GREENHOUSE", "Number of internodes"),
                      ("GREENHOUSE", "Internode 1 length")}
    n = next(x for x in r["direct_source_tests"] if
             x["study"] == "GREENHOUSE" and x["trait"] == "Number of internodes")
    i = next(x for x in r["direct_source_tests"] if
             x["study"] == "GREENHOUSE" and x["trait"] == "Internode 1 length")
    assert n["delta_beta_present_minus_absent"] == pytest.approx(+0.22)
    assert i["delta_beta_present_minus_absent"] == pytest.approx(-0.11)


def test_field_nominal_interaction_does_not_certify_opposite_signs():
    r = audited()
    f = next(x for x in r["direct_source_tests"] if
             x["study"] == "FIELD" and x["trait"] == "Early growth rate")
    assert f["original_author_p"] == "0.049"
    assert f["nominal_p_lt_0_05"]
    assert f["point_sign_flip"]
    assert not f["both_arm_opposite_nonzero_supported"]
    assert not f["source_eight_tests_bonferroni_0_05"]


def test_2002_source_table_does_not_test_insect_by_trait():
    r = audited()
    assert r["stinchcombe_table2_p_values_test_bias_within_regimes_not_trait_by_insect"]
    assert r["stinchcombe_source_table2_direct_trait_by_insect_p_recovered"] is False
    assert "NO_META_GENERALITY" in r["status"]


@pytest.mark.parametrize("change", ["author_p", "source_beta", "source_id"])
def test_mutation_fails_closed(change):
    a, b, s = read_csv(PAIRS), deepcopy(read_csv(BEANS)), deepcopy(read_csv(STINCH))
    if change == "author_p":
        b[2]["original_p"] = "0.000001"
    elif change == "source_beta":
        b[3]["beta_present"] = "3.6"
    else:
        s[0]["source_row_id"] = "9999"
    with pytest.raises(ValueError):
        run(a, b, s)


def test_document_preserves_claim_ceiling():
    doc = (ROOT/"docs/SCH_2020_PRIMARY_AUTHOR_CONTEXT_AUDIT_V2.md").read_text(encoding="utf-8")
    for phrase in ["8比較", "2形質", "0.005", "0.049", "Stinchcombe",
                   "同一論文", "機能別最適値", "137"]:
        assert phrase in doc

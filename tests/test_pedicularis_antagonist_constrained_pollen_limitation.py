from __future__ import annotations

from copy import deepcopy

import pytest

from scripts.audit_pedicularis_antagonist_constrained_pollen_limitation import (
    DEFAULT_LEDGER,
    _read,
    build,
)


def test_p_rex_is_only_a_partial_match_to_adaptive_pollen_limitation() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["aipl_criteria"] == {
        "AIPL_C1": "SUPPORTED_OBSERVATIONAL",
        "AIPL_C2": "UNRESOLVED",
        "AIPL_C3": "COMPONENTS_PRESENT_CAUSAL_CHAIN_UNRESOLVED",
        "AIPL_C4": "UNRESOLVED",
    }
    assert result["n_aipl_criteria_fully_supported"] == 1
    assert result["aipl_full_mechanism_supported"] is False
    assert result["status"] == "P_REX_AIPL_PARTIAL_MATCH_CAUSAL_TEST_REQUIRED"


def test_success_risk_coupling_is_recovered_but_not_causal() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert result["p_rex_pollen_limited_state_recovered"] is True
    assert result["p_rex_success_risk_coupling_recovered"] is True
    assert result["success_risk_coupling_causal"] is False
    assert result["predictive_cue_identity_resolved"] is False
    assert "do_not_claim_pollen_is_the_predator_cue" in result["claim_ceiling"]


def test_causal_surface_has_directional_predictions_and_falsifiers() -> None:
    result = build(_read(DEFAULT_LEDGER))

    assert any(
        "predator removal shifts" in prediction
        for prediction in result["causal_surface_predictions"]
    )
    assert any(
        "does not shift" in falsifier
        for falsifier in result["falsifiers"]
    )


def test_c2_c3_c4_cannot_be_silently_promoted() -> None:
    rows = _read(DEFAULT_LEDGER)

    for criterion_id in ("AIPL_C2", "AIPL_C4"):
        edited = deepcopy(rows)
        row = next(r for r in edited if r["criterion_id"] == criterion_id)
        row["status"] = "SUPPORTED"
        with pytest.raises(ValueError, match="must remain unresolved"):
            build(edited)

    edited = deepcopy(rows)
    row = next(r for r in edited if r["criterion_id"] == "AIPL_C3")
    row["status"] = "SUPPORTED"
    with pytest.raises(ValueError, match="partial/unresolved"):
        build(edited)


def test_current_rows_cannot_claim_causal_support() -> None:
    rows = _read(DEFAULT_LEDGER)
    edited = deepcopy(rows)
    edited[0]["causal_support"] = "YES"

    with pytest.raises(ValueError, match="promoted to causal support"):
        build(edited)


def test_source_model_details_are_locked() -> None:
    rows = _read(DEFAULT_LEDGER)
    coupling = next(
        row for row in rows
        if row["criterion_id"] == "PRX_COUPLING_1"
    )

    assert "exsertion***" in coupling["focal_evidence"]
    assert "lip width*" in coupling["focal_evidence"]
    assert "pollen*" in coupling["focal_evidence"]
    assert "population***" in coupling["focal_evidence"]
    assert "AICc -156.11" in coupling["focal_evidence"]

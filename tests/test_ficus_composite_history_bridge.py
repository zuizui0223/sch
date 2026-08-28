from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "empirical" / "one_trait_shared_cue" / "FICUS_COMPOSITE_HISTORY_BRIDGE_V1.csv"
AUDIT = ROOT / "docs" / "SCH_FICUS_COMPOSITE_HISTORY_BRIDGE_AUDIT_V1.md"
HISTORY = ROOT / "docs" / "SCH_HISTORICAL_CUE_TRANSITION_PRIMARY_SOURCE_AUDIT_V1.md"
READOUT = ROOT / "empirical" / "one_trait_shared_cue" / "EVOLUTIONARY_OUTCOME_READOUT_V1.md"


def _rows() -> list[dict[str, str]]:
    with LEDGER.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_ficus_composite_contains_history_private_and_dual_audience_pieces() -> None:
    rows = _rows()
    assert len(rows) == 4
    roles = {row["evidence_role"] for row in rows}
    assert "phylogenetic_scent_divergence" in roles
    assert "extant_private_pollinator_channel" in roles
    assert "shared_signal_exploitation" in roles
    assert "developmental_signal_switch_and_receiver_molecular_specificity" in roles


def test_ficus_composite_is_not_promoted_to_direct_l4() -> None:
    rows = _rows()
    assert all(row["within_same_comparative_transition"] == "NO" for row in rows)
    assert all(row["status"] != "DIRECT_L4" for row in rows)
    text = AUDIT.read_text(encoding="utf-8")
    assert "COMPOSITE_NEAR_L4" in text
    assert "not DIRECT_L4" in text
    assert "ancestral shared state | **UNRESOLVED**" in text
    assert "replicated transition + alternatives | **UNRESOLVED**" in text


def test_ficus_audit_preserves_fail_closed_next_step() -> None:
    text = AUDIT.read_text(encoding="utf-8")
    assert "same phylogeny" in text
    assert "conditioning on phylogeny and alternatives" in text
    assert "NOT_EVALUABLE" in text


def test_ficus_composite_is_integrated_without_changing_direct_l4_count() -> None:
    history = HISTORY.read_text(encoding="utf-8")
    readout = READOUT.read_text(encoding="utf-8")
    for text in (history, readout):
        assert "COMPOSITE_NEAR_L4" in text
        assert "DIRECT_L4" in text
        assert "FICUS_COMPOSITE_HISTORY_BRIDGE_V1.csv" in text
    assert "private-cue evolution from a shared cue:     0 direct sources" in readout
    assert "lineage branching/specialization:            0 direct sources" in readout

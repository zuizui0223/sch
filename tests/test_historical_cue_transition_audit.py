from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "empirical" / "one_trait_shared_cue" / "HISTORICAL_CUE_TRANSITION_AUDIT_V1.csv"
READOUT = ROOT / "docs" / "SCH_HISTORICAL_CUE_TRANSITION_PRIMARY_SOURCE_AUDIT_V1.md"


def _rows() -> dict[str, dict[str, str]]:
    with AUDIT.open(encoding="utf-8", newline="") as handle:
        return {row["study"]: row for row in csv.DictReader(handle)}


def test_history_audit_keeps_direct_transition_fail_closed() -> None:
    rows = _rows()
    assert len(rows) == 8
    assert all(row["status"] != "DIRECT_SHARED_TO_PRIVATE_TRANSITION" for row in rows.values())
    assert all(row["claim_ceiling"] for row in rows.values())
    assert all(row["ancestral_shared_state"] != "DIRECT_RECONSTRUCTED_SHARED_ANCESTOR" for row in rows.values())


def test_history_audit_distinguishes_complementary_near_misses() -> None:
    rows = _rows()
    assert rows["Joffard_et_al_2020"]["status"] == "PHYLOGENETIC_POLLINATOR_ONLY"
    assert rows["Muhlemann_et_al_2006"]["status"] == "CONTEMPORARY_TEMPORAL_GATING_ONLY"
    assert rows["Campbell_et_al_2022"]["status"] == "DUAL_SELECTION_NO_HISTORY"
    assert rows["Opedal_et_al_2019"]["status"] == "NEGATIVE_CONTROL_WEAK_CONFLICT"


def test_history_readout_requires_both_history_and_dual_audience_channels() -> None:
    text = READOUT.read_text(encoding="utf-8")
    assert "ancestral state" in text
    assert "pollinator channel" in text
    assert "antagonist channel" in text
    assert "replicated transition and alternatives" in text
    assert "L4  reconstructed shared-cue -> private-cue transition under both audiences" in text
    assert "lineage branching` remains `NOT_EVALUABLE" in text

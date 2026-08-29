from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "MANUSCRIPT_SHARED_CUE_FRAMEWORK.md"


def test_manuscript_contains_bounded_ficus_historical_bridge() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "Historical bridge: Ficus is near L4 but not L4" in text
    assert "COMPOSITE_NEAR_L4" in text
    assert "not `DIRECT_L4`" in text
    assert "resolved pollinator attractive chemical codes" in text
    assert "resolved code + direct same-code NPFW behavioural response" in text
    assert "0" in text


def test_manuscript_separates_temporal_from_chemical_privacy() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "Platyneura cunia" in text
    assert "Sycoscapter trifemmensis" in text
    assert "Temporal separation does not prove chemical privatization" in text
    assert "NPFW host association does not prove interception" in text
    assert "whole-odour response does not identify response to an unresolved key code" in text


def test_manuscript_requires_equivalence_not_nonsignificance_for_privacy() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "206 decisive choices for 80% power" in text
    assert "260 for 90%" in text
    assert "412 and 520 introduced wasps" in text
    assert "nonsignificance at a legacy attraction sample size cannot be reinterpreted as evidence for a private channel" in text
    assert "working NPFW host/stage positive control" in text
    assert "BEHAVIORAL_NONRESPONSE_EQUIVALENT" in text


def test_historical_research_fork_stays_fixed_to_same_code_cells() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "For the historical L4 endpoint, the strategy is no longer a broad literature search" in text
    assert "4-methylanisole" in text
    assert "four-VOC ratio" in text
    assert "minimal *F. hispida* pollinator code" in text
    assert "NOT_EVALUABLE" in text

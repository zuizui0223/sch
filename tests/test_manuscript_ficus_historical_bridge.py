from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs" / "SCH_FICUS_32_SPECIES_L4_MATRIX_READOUT_V1.md"
PROTOCOL = ROOT / "docs" / "SCH_FICUS_SAME_CODE_EXPERIMENT_PROTOCOL_V1.md"
CONTRACT = ROOT / "docs" / "SCH_FICUS_SAME_CODE_TRIAL_DATA_CONTRACT_V1.md"


def test_ficus_module_contains_bounded_historical_bridge() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    assert "resolved pollinator attractive chemical codes" in text
    assert "resolved pollinator code + direct same-code NPFW behaviour" in text
    assert "DIRECT_L4 species/transitions" in text
    assert "historical shared -> private transition" in text
    assert "NOT_EVALUABLE" in text


def test_ficus_module_separates_temporal_from_chemical_privacy() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    assert "Platyneura cunia" in text
    assert "Sycoscapter trifemmensis" in text
    assert "temporal separation is not chemical privatization" in text
    assert "host association does not show that it intercepts" in text
    assert "whole-odour response" in text


def test_ficus_protocol_requires_equivalence_not_nonsignificance_for_privacy() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    assert "80% power: 206 decisive choices" in text
    assert "90% power: 260 decisive choices" in text
    assert "80% power: 412 introduced" in text
    assert "90% power: 520 introduced" in text
    assert "A failed attraction test is not converted into privacy by rhetoric." in text
    assert "NPFW responsiveness positive control" in text
    assert "BEHAVIORAL_NONRESPONSE_EQUIVALENT" in text


def test_ficus_contract_separates_directional_and_equivalence_intervals_and_preserves_clusters() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "NPFW same-code direction        -> 95% cluster-bootstrap interval" in text
    assert "NPFW same-code equivalence      -> 90% cluster-bootstrap interval" in text
    assert "cluster_id" in text
    assert "rather than treating introduced wasps as exchangeable" in text
    assert "scripts/analyze_ficus_same_code_trials.py" in text


def test_historical_research_fork_stays_fixed_to_same_code_cells() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    assert "The next pass should remain inside the fixed *Ficus* system" in text
    assert "4-methylanisole" in text
    assert "four-VOC ratio" in text
    assert "resolve the pollinator-attractive blend to a synthetic code" in text
    assert "NOT_EVALUABLE" in text

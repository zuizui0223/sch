from __future__ import annotations

import csv
from pathlib import Path

from scripts.analyze_ficus_same_code_trials import REQUIRED_FIELDS


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "one_trait_shared_cue" / "FICUS_SAME_CODE_TRIAL_TEMPLATE_V1.csv"
CONTRACT = ROOT / "docs" / "SCH_FICUS_SAME_CODE_TRIAL_DATA_CONTRACT_V1.md"
PROTOCOL = ROOT / "docs" / "SCH_FICUS_SAME_CODE_EXPERIMENT_PROTOCOL_V1.md"


def test_trial_csv_template_exactly_matches_analyzer_contract() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        header = next(reader)
        assert list(header) == list(REQUIRED_FIELDS)
        assert list(reader) == []


def test_data_contract_separates_directional_and_equivalence_inference() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "NPFW same-code direction        -> 95% cluster-bootstrap interval" in text
    assert "NPFW same-code equivalence      -> 90% cluster-bootstrap interval" in text
    assert "The two NPFW intervals are intentionally separate" in text
    assert "NO_CHOICE" in text
    assert "code_id" in text
    assert "cluster_id" in text
    assert "None of those states alone is `DIRECT_L4`" in text


def test_historical_gap_points_to_executable_trial_contract() -> None:
    contract = CONTRACT.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    assert "95% cluster-bootstrap interval" in contract
    assert "90% cluster-bootstrap interval" in contract
    assert "cluster_id" in contract
    assert "scripts/analyze_ficus_same_code_trials.py" in contract
    assert "a nonsignificant NPFW response is not called a private channel" in protocol
    assert "BEHAVIORAL_NONRESPONSE_EQUIVALENT" in protocol

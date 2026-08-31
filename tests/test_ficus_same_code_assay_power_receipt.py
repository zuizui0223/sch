from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "empirical" / "one_trait_shared_cue" / "FICUS_SAME_CODE_ASSAY_POWER_V1.json"
PROTOCOL = ROOT / "docs" / "SCH_FICUS_SAME_CODE_EXPERIMENT_PROTOCOL_V1.md"


def test_equivalence_receipt_matches_registered_actions_result() -> None:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    rows = {row["target_power"]: row for row in data["equivalence_rows"]}
    assert rows[0.8]["decisive_choices"] == 206
    assert rows[0.8]["planned_introductions"] == 412
    assert rows[0.9]["decisive_choices"] == 260
    assert rows[0.9]["planned_introductions"] == 520
    assert data["provenance"]["workflow_run_id"] == 33224872756
    assert data["provenance"]["artifact_id"] == 9706487884


def test_strong_attraction_and_privacy_have_distinct_information_requirements() -> None:
    data = json.loads(RECEIPT.read_text(encoding="utf-8"))
    attraction = {
        (row["true_choice_probability"], row["target_power"]): row
        for row in data["attraction_rows"]
    }
    assert attraction[(0.65, 0.8)]["decisive_choices"] == 82
    assert attraction[(0.70, 0.8)]["decisive_choices"] == 43
    assert attraction[(0.65, 0.8)]["decisive_choices"] < 206
    assert "nonsignificant attraction test is not equivalence" in data["claim_boundary"]


def test_protocol_uses_powered_equivalence_not_expected_width_as_promotion_rule() -> None:
    text = PROTOCOL.read_text(encoding="utf-8")
    assert "only an expected-width benchmark, not a powered equivalence design" in text
    assert "80% power: 206 decisive choices" in text
    assert "90% power: 260 decisive choices" in text
    assert "80% power: 412 introduced" in text
    assert "90% power: 520 introduced" in text

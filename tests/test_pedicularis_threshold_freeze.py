from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.pedicularis_config_freeze import (
    FREEZE_SCHEMA,
    FREEZE_STATUS,
    inspect_prospective_freeze,
    required_gate_paths,
    validate_freeze_context,
    validate_prospective_freeze,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIGS = {
    "P0": ROOT / "empirical" / "architecture" / "PEDICULARIS_STAGE_P0_CONFIG_TEMPLATE_V1.json",
    "P1": ROOT / "empirical" / "architecture" / "PEDICULARIS_POLLINATION_WEIGHT_CONFIG_TEMPLATE_V1.json",
    "G": ROOT / "empirical" / "architecture" / "PEDICULARIS_PREDATOR_METHOD_CONFIG_V4.json",
}


def _frozen_config(lane: str) -> dict:
    config = json.loads(CONFIGS[lane].read_text(encoding="utf-8"))
    for path in required_gate_paths(lane):
        section, field = path.split(".", 1)
        if isinstance(config[section][field], bool):
            continue
        config[section][field] = 1.0
    config["prospective_freeze"] = {
        "schema": FREEZE_SCHEMA,
        "status": FREEZE_STATUS,
        "lane": lane,
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-09-27T00:00:00Z",
        "basis_document": "UNIT_TEST_SYNTHETIC_FIXTURE_ONLY",
        "threshold_basis": {
            path: "UNIT_TEST_SYNTHETIC_FIXTURE_ONLY"
            for path in required_gate_paths(lane)
        },
    }
    return config


def test_committed_field_templates_are_intentionally_not_frozen() -> None:
    for lane, path in CONFIGS.items():
        config = json.loads(path.read_text(encoding="utf-8"))
        receipt = inspect_prospective_freeze(config, lane)
        assert receipt["status"] == "PEDICULARIS_THRESHOLDS_NOT_FROZEN"
        assert receipt["issues"]
        assert any(issue.startswith("gate_not_frozen:") for issue in receipt["issues"])


def test_each_lane_has_explicit_basis_for_every_gate_field() -> None:
    assert len(required_gate_paths("P0")) == 11
    assert len(required_gate_paths("P1")) == 10
    assert len(required_gate_paths("G")) == 19

    for lane in CONFIGS:
        receipt = validate_prospective_freeze(_frozen_config(lane), lane)
        assert receipt["status"] == FREEZE_STATUS
        assert receipt["n_required_gate_fields"] == len(required_gate_paths(lane))
        assert receipt["issues"] == []


def test_missing_threshold_basis_fails_closed() -> None:
    config = _frozen_config("P0")
    missing = required_gate_paths("P0")[0]
    config["prospective_freeze"]["threshold_basis"].pop(missing)

    with pytest.raises(ValueError, match="basis_missing"):
        validate_prospective_freeze(config, "P0")


def test_config_lane_cannot_be_relabelled_after_freeze() -> None:
    config = _frozen_config("P1")
    config["prospective_freeze"]["lane"] = "G"

    with pytest.raises(ValueError, match="freeze_lane_mismatch"):
        validate_prospective_freeze(config, "P1")


def test_data_context_must_match_frozen_population_and_season() -> None:
    receipt = validate_prospective_freeze(_frozen_config("G"), "G")
    validate_freeze_context(receipt, "P_REX_TEST", "S1")

    with pytest.raises(ValueError, match="do not match"):
        validate_freeze_context(receipt, "P_REX_TEST", "S2")


def test_freeze_must_precede_confirmatory_data() -> None:
    config = _frozen_config("P0")
    config["prospective_freeze"]["frozen_before_confirmatory_data"] = False

    with pytest.raises(ValueError, match="not_declared_frozen_before_confirmatory_data"):
        validate_prospective_freeze(config, "P0")

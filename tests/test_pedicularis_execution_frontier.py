from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_pedicularis_execution_frontier import DEFAULT_CONFIGS, build
from scripts.pedicularis_config_freeze import FREEZE_SCHEMA, FREEZE_STATUS, required_gate_paths


def _write_frozen(path: Path, source: Path, lane: str, population: str = "P_REX_TEST", season: str = "S1") -> Path:
    config = json.loads(source.read_text(encoding="utf-8"))
    for gate_path in required_gate_paths(lane):
        section, field = gate_path.split(".", 1)
        if not isinstance(config[section][field], bool):
            config[section][field] = 1.0
    config["prospective_freeze"] = {
        "schema": FREEZE_SCHEMA,
        "status": FREEZE_STATUS,
        "lane": lane,
        "population_id": population,
        "season_id": season,
        "frozen_before_confirmatory_data": True,
        "frozen_at_utc": "2026-09-27T00:00:00Z",
        "basis_document": "UNIT_TEST_SYNTHETIC_FIXTURE_ONLY",
        "threshold_basis": {
            gate_path: "UNIT_TEST_SYNTHETIC_FIXTURE_ONLY"
            for gate_path in required_gate_paths(lane)
        },
    }
    path.write_text(json.dumps(config), encoding="utf-8")
    return path


def test_committed_repository_frontier_stops_before_data_collection() -> None:
    result = build(DEFAULT_CONFIGS)
    assert result["n_lanes_frozen"] == 0
    assert result["all_three_lane_configs_frozen"] is False
    assert result["current_blocker"] == "PROSPECTIVE_THRESHOLD_FREEZE_REQUIRED"
    assert "before reading confirmatory outcomes" in result["next_action"]


def test_three_same_context_frozen_configs_advance_to_receipt_collection(tmp_path: Path) -> None:
    configs = {
        lane: _write_frozen(
            tmp_path / f"{lane}.json",
            DEFAULT_CONFIGS[lane],
            lane,
        )
        for lane in ("P0", "P1", "G")
    }
    result = build(configs)
    assert result["n_lanes_frozen"] == 3
    assert result["same_population_and_season_after_freeze"] is True
    assert result["current_blocker"] == "CONFIRMATORY_P0_P1_G_RECEIPTS_REQUIRED"


def test_frozen_configs_from_different_seasons_fail_closed(tmp_path: Path) -> None:
    configs = {
        "P0": _write_frozen(tmp_path / "P0.json", DEFAULT_CONFIGS["P0"], "P0"),
        "P1": _write_frozen(tmp_path / "P1.json", DEFAULT_CONFIGS["P1"], "P1"),
        "G": _write_frozen(tmp_path / "G.json", DEFAULT_CONFIGS["G"], "G", season="S2"),
    }
    result = build(configs)
    assert result["all_three_lane_configs_frozen"] is True
    assert result["same_population_and_season_after_freeze"] is False
    assert result["current_blocker"] == "FROZEN_CONFIG_CONTEXT_MISMATCH"

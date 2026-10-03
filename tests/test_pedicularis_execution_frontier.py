from __future__ import annotations

import json
from pathlib import Path

from scripts.audit_pedicularis_execution_frontier import DEFAULT_CONFIGS, build
from scripts.pedicularis_config_freeze import FREEZE_SCHEMA, FREEZE_STATUS, required_gate_paths


def _write_frozen(
    path: Path,
    source: Path,
    lane: str,
    population: str = "P_REX_TEST",
    season: str = "S1",
    *,
    selected_g_device: str | None = None,
) -> Path:
    config = json.loads(source.read_text(encoding="utf-8"))
    for gate_path in required_gate_paths(lane):
        section, field = gate_path.split(".", 1)
        if not isinstance(config[section][field], bool):
            config[section][field] = 1.0
    if lane == "G" and selected_g_device is not None:
        config["method_gate"]["selected_exclusion_method"] = selected_g_device
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
    assert result["threshold_gate_module_counts"] == {
        "CAL_A": 20,
        "CAL_B": 7,
        "CAL_C": 8,
        "REGISTERED_CONTRACT": 5,
    }
    assert result["unresolved_calibration_gate_count"] == 35
    assert result["calibration_program_sequence"] == ["CAL_A", "CAL_B", "CAL_C"]
    assert "CAL-A" in result["next_action"]
    assert "CAL-B" in result["next_action"]
    assert "CAL-C" in result["next_action"]
    assert "before reading confirmatory outcomes" in result["next_action"]


def test_thresholds_frozen_without_g_device_selection_stop_before_confirmatory(tmp_path: Path) -> None:
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
    assert result["g_device_selected"] is False
    assert result["selected_g_device"] is None
    assert result["current_blocker"] == "G_DEVICE_SELECTION_REQUIRED"
    assert "device screen" in result["next_action"]


def test_three_same_context_frozen_configs_with_selected_g_device_advance_to_receipts(tmp_path: Path) -> None:
    configs = {
        "P0": _write_frozen(
            tmp_path / "P0.json",
            DEFAULT_CONFIGS["P0"],
            "P0",
        ),
        "P1": _write_frozen(
            tmp_path / "P1.json",
            DEFAULT_CONFIGS["P1"],
            "P1",
        ),
        "G": _write_frozen(
            tmp_path / "G.json",
            DEFAULT_CONFIGS["G"],
            "G",
            selected_g_device="POST_POLLINATION_LOWER_FLOWER_SLEEVE",
        ),
    }
    result = build(configs)
    assert result["n_lanes_frozen"] == 3
    assert result["same_population_and_season_after_freeze"] is True
    assert result["g_device_selected"] is True
    assert result["selected_g_device"] == "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
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

from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.freeze_pedicularis_full_surface_thresholds import build


ROOT = Path(__file__).resolve().parents[1]
CONFIG_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_FULL_SURFACE_CONFIG_TEMPLATE_V2.json"
)
FREEZE_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_TEMPLATE_V1.json"
)


def test_committed_surface_and_freeze_templates_fail_closed() -> None:
    config = json.loads(CONFIG_TEMPLATE.read_text(encoding="utf-8"))
    freeze = json.loads(FREEZE_TEMPLATE.read_text(encoding="utf-8"))

    with pytest.raises(ValueError):
        build(config, freeze)


def test_surface_threshold_freeze_requires_pregeometry_and_preP2_flags() -> None:
    config = {
        "sch_surface": {
            "bootstrap_reps": 300,
            "random_seed": 41,
            "min_z_levels": 5,
            "min_valid_bootstrap_fraction": 0.8,
            "min_interior_bootstrap_fraction": 0.9,
            "min_optimum_separation": 0.1,
            "min_optimum_shift": 0.05,
            "min_abs_component_gradient": 0.05,
        },
        "system_checks": {
            "max_water_depth_range": 0.1,
            "max_mechanical_damage_rate": 0.05,
        },
        "status": "PEDICULARIS_FULL_SURFACE_CONFIG_PROSPECTIVELY_FROZEN",
    }
    freeze = {
        "schema": "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_V1",
        "status": "PEDICULARIS_FULL_SURFACE_THRESHOLDS_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_at_utc": "2026-10-07T00:00:00+00:00",
        "basis_document": "SYNTHETIC_TEST_ONLY",
        "frozen_before_geometry_outcomes": True,
        "frozen_before_full_surface_outcomes": True,
        "threshold_basis": {
            "sch_surface.min_z_levels": "x",
            "sch_surface.min_valid_bootstrap_fraction": "x",
            "sch_surface.min_interior_bootstrap_fraction": "x",
            "sch_surface.min_optimum_separation": "x",
            "sch_surface.min_optimum_shift": "x",
            "sch_surface.min_abs_component_gradient": "x",
            "system_checks.max_water_depth_range": "x",
            "system_checks.max_mechanical_damage_rate": "x",
        },
    }

    receipt = build(config, freeze)
    assert receipt["status"] == (
        "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_VALIDATED"
    )
    assert len(receipt["analysis_config_sha256"]) == 64
    assert receipt["threshold_basis"]["system_checks.max_water_depth_range"] == "x"
    assert receipt["threshold_basis"]["system_checks.max_mechanical_damage_rate"] == "x"

    changed = dict(freeze)
    changed["frozen_before_geometry_outcomes"] = False
    with pytest.raises(ValueError, match="before geometry outcomes"):
        build(config, changed)

    changed = dict(freeze)
    changed["frozen_before_full_surface_outcomes"] = False
    with pytest.raises(ValueError, match="before P2 outcomes"):
        build(config, changed)


def test_surface_threshold_freeze_requires_system_check_basis_notes() -> None:
    config = {
        "sch_surface": {
            "bootstrap_reps": 300,
            "random_seed": 41,
            "min_z_levels": 5,
            "min_valid_bootstrap_fraction": 0.8,
            "min_interior_bootstrap_fraction": 0.9,
            "min_optimum_separation": 0.1,
            "min_optimum_shift": 0.05,
            "min_abs_component_gradient": 0.05,
        },
        "system_checks": {
            "max_water_depth_range": 0.1,
            "max_mechanical_damage_rate": 0.05,
        },
        "status": "PEDICULARIS_FULL_SURFACE_CONFIG_PROSPECTIVELY_FROZEN",
    }
    freeze = {
        "schema": "PEDICULARIS_FULL_SURFACE_THRESHOLD_FREEZE_V1",
        "status": "PEDICULARIS_FULL_SURFACE_THRESHOLDS_PROSPECTIVELY_FROZEN",
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "frozen_at_utc": "2026-10-07T00:00:00+00:00",
        "basis_document": "SYNTHETIC_TEST_ONLY",
        "frozen_before_geometry_outcomes": True,
        "frozen_before_full_surface_outcomes": True,
        "threshold_basis": {
            "sch_surface.min_z_levels": "x",
            "sch_surface.min_valid_bootstrap_fraction": "x",
            "sch_surface.min_interior_bootstrap_fraction": "x",
            "sch_surface.min_optimum_separation": "x",
            "sch_surface.min_optimum_shift": "x",
            "sch_surface.min_abs_component_gradient": "x",
        },
    }

    with pytest.raises(ValueError, match="registered full-surface decision paths"):
        build(config, freeze)

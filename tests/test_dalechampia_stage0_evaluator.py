from __future__ import annotations

import csv
import random
from pathlib import Path

import pytest

from scripts.evaluate_dalechampia_stage0 import (
    EXPOSURE_REQUIRED,
    POPULATION_REQUIRED,
    _predated_fraction,
    evaluate_exposure,
    evaluate_population,
)


ROOT = Path(__file__).resolve().parents[1]
POP_TEMPLATE = ROOT / "empirical" / "architecture" / "DALECHAMPIA_STAGE0_POPULATION_TEMPLATE_V1.csv"
EXP_TEMPLATE = ROOT / "empirical" / "architecture" / "DALECHAMPIA_STAGE0_EXPOSURE_TEMPLATE_V1.csv"
CONTRACT = ROOT / "docs" / "SCH_DALECHAMPIA_STAGE0_DATA_CONTRACT_V1.md"


def _config() -> dict:
    return {
        "bootstrap_reps": 300,
        "random_seed": 7,
        "population": {
            "min_blossoms": 30,
            "min_plants": 10,
            "min_predator_incidence": 0.2,
            "min_positive_correlation": 0.15,
        },
        "exposure": {
            "min_complete_plants": 15,
            "min_damage_fraction_delta": 0.2,
            "max_pollen_relative_change": 0.1,
            "max_z_relative_change": 0.05,
            "max_resin_relative_change": 0.1,
        },
    }


def _population_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(20):
        for blossom in range(3):
            z = 0.7 + plant * 0.035 + blossom * 0.01
            pollen = 40 + 80 * z
            predated = min(9, max(1, round(1 + 5 * z)))
            rows.append(
                {
                    "population_id": "MX_TEST",
                    "season_id": "S1",
                    "plant_id": f"P{plant:02d}",
                    "blossom_id": f"P{plant:02d}_B{blossom}",
                    "bract_area": f"{z:.4f}",
                    "pollen_grains": f"{pollen:.4f}",
                    "seed_predator_present": "1",
                    "predated_seed_count": str(predated),
                    "initiated_seed_count": "10",
                }
            )
    return rows


def _exposure_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(24):
        base_pollen = 100 + (plant % 3)
        base_z = 1.0 + (plant % 4) * 0.002
        base_resin = 2.0 + (plant % 2) * 0.01
        for window, pred, pollen_multiplier in (
            ("E0", 1, 1.0),
            ("E1", 5, 1.35),
            ("E2", 5, 1.0),
        ):
            rows.append(
                {
                    "population_id": "MX_TEST",
                    "season_id": "S1",
                    "plant_id": f"P{plant:02d}",
                    "blossom_id": f"P{plant:02d}_{window}",
                    "exposure_window": window,
                    "bract_area": f"{base_z:.4f}",
                    "pollen_grains": f"{base_pollen * pollen_multiplier:.4f}",
                    "resin_amount": f"{base_resin:.4f}",
                    "predated_seed_count": str(pred),
                    "initiated_seed_count": "10",
                }
            )
    return rows


def test_templates_match_registered_required_fields() -> None:
    with POP_TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == POPULATION_REQUIRED
    with EXP_TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == EXPOSURE_REQUIRED


def test_population_screen_qualifies_strong_dual_tracking_only_as_stage0_candidate() -> None:
    result = evaluate_population(_population_rows(), _config(), random.Random(7))
    assert result["status"] == "QUALIFIED_CONFLICT_ACTIVE_CANDIDATE"
    assert all(result["gates"].values())
    assert result["bract_pollen_bootstrap_95_ci"][0] > 0
    assert result["bract_predation_bootstrap_95_ci"][0] > 0
    assert result["claim_ceiling"] == "stage0_screen_only_not_causal_compromise_or_optimum_identification"


def test_exposure_screen_selects_damage_window_that_preserves_pollination_and_trait_state() -> None:
    result = evaluate_exposure(_exposure_rows(), _config(), random.Random(7))
    assert result["status"] == "SELECTIVE_G_WINDOW_CANDIDATE"
    assert result["selected_g1_window"] == "E2"
    assert result["design"] == "within_plant_E0_vs_window_paired_contrasts"
    by_window = {item["window"]: item for item in result["candidate_windows"]}
    assert by_window["E2"]["n_complete_plants"] == 24
    assert by_window["E2"]["passes"] is True
    assert by_window["E1"]["passes"] is False
    assert by_window["E1"]["gates"]["pollination_selectivity"] is False
    assert "not_direct_oviposition" in result["claim_ceiling"]


def test_exposure_screen_requires_enough_complete_within_plant_pairs() -> None:
    rows = [
        row
        for row in _exposure_rows()
        if not (row["exposure_window"] == "E0" and int(row["plant_id"][1:]) >= 10)
    ]
    result = evaluate_exposure(rows, _config(), random.Random(7))
    by_window = {item["window"]: item for item in result["candidate_windows"]}
    assert by_window["E2"]["n_complete_plants"] == 10
    assert by_window["E2"]["gates"]["minimum_complete_plants"] is False
    assert result["status"] == "NO_SELECTIVE_G_WINDOW_RECOVERED"


def test_invalid_seed_denominator_fails_closed() -> None:
    row = _population_rows()[0]
    row["initiated_seed_count"] = "0"
    with pytest.raises(ValueError, match="initiated_seed_count must be > 0"):
        _predated_fraction(row)


def test_contract_does_not_promote_stage0_to_compromise() -> None:
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Neither mode estimates `z1*`, `z2*`, or `zc*`." in text
    assert "population screen\n!= causal multifunctionality" in text
    assert "controlled exposure screen\n!= direct observation of oviposition" in text
    assert "Thresholds are **not hard-coded**" in text
    assert "within-plant" in text.lower()

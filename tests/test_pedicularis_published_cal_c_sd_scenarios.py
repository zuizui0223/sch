from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from scripts.build_pedicularis_published_cal_c_sd_scenarios import (
    build,
    paired_difference_sd,
)


ROOT = Path(__file__).resolve().parents[1]
READOUT = ROOT / "empirical" / "architecture" / "PEDICULARIS_PUBLISHED_CAL_C_SD_SCENARIOS_V1.json"


def test_paired_difference_sd_formula_known_cases() -> None:
    assert paired_difference_sd(5.30, 0.50) == pytest.approx(5.30)
    assert paired_difference_sd(5.30, 0.00) == pytest.approx(
        5.30 * math.sqrt(2.0)
    )
    assert paired_difference_sd(0.12, 0.75) == pytest.approx(
        0.12 * math.sqrt(0.5)
    )


def test_published_scenarios_cover_p1_pollen_and_g_predation_only() -> None:
    result = build()

    assert result["status"] == "PUBLISHED_SD_SENSITIVITY_SCENARIOS_READY"
    assert result["n_criteria_with_external_sd_scenarios"] == 2
    assert result["n_scenarios"] == 8
    assert set(result["criterion_summary"]) == {
        "P1_POLLEN",
        "G_PREDATION",
    }
    assert result["direct_cal_c_pilot_sd_values_materialized"] == 0
    assert result["direct_f0_values_materialized"] == 0


def test_pollen_difference_sd_envelope_is_explicitly_correlation_sensitive() -> None:
    result = build()
    pollen = result["criterion_summary"]["P1_POLLEN"]

    assert pollen["published_measurement_id"] == "PRX2016_POLLEN_GLM_POOL"
    assert pollen["published_marginal_sd"] == pytest.approx(5.30)
    assert pollen["max_implied_paired_difference_sd"] == pytest.approx(
        5.30 * math.sqrt(2.0)
    )
    assert pollen["min_implied_paired_difference_sd"] == pytest.approx(
        5.30 * math.sqrt(0.5)
    )


def test_seed_predation_difference_sd_envelope_uses_direct_reported_sd() -> None:
    result = build()
    predation = result["criterion_summary"]["G_PREDATION"]

    assert predation["published_measurement_id"] == (
        "PRX2016_PREDATION_GLM_POOL"
    )
    assert predation["published_marginal_sd"] == pytest.approx(0.120)
    assert predation["max_implied_paired_difference_sd"] == pytest.approx(
        0.120 * math.sqrt(2.0)
    )
    assert predation["min_implied_paired_difference_sd"] == pytest.approx(
        0.120 * math.sqrt(0.5)
    )


def test_external_scenarios_are_never_labelled_as_observed_cal_c_pilot_sd() -> None:
    result = build()
    assert {
        row["scenario_role"]
        for row in result["scenarios"]
    } == {"EXTERNAL_CAL_C_SENSITIVITY_ONLY_NOT_PILOT_SD"}
    assert "do_not_write_scenario_sd_into_CAL_C_as_observed_pilot_sd" in (
        result["claim_ceiling"]
    )


def test_invalid_correlation_grid_fails_closed() -> None:
    with pytest.raises(ValueError, match="at least two"):
        build(correlations=(0.5,))
    with pytest.raises(ValueError, match="unique"):
        build(correlations=(0.5, 0.5))
    with pytest.raises(ValueError, match="\(-1, 1\)"):
        build(correlations=(0.0, 1.0))


def test_frozen_published_sd_scenario_readout_is_reproducible() -> None:
    assert build() == json.loads(READOUT.read_text(encoding="utf-8"))

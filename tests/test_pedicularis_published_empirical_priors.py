from __future__ import annotations

import csv
from pathlib import Path

from scripts.audit_pedicularis_published_empirical_priors import (
    DEFAULT_DATASETS,
    DEFAULT_PRIORS,
    build,
)


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_published_empirical_recovery_has_five_sources_and_32_measurements() -> None:
    result = build()
    assert result["n_published_sources"] == 5
    assert result["n_published_measurement_rows"] == 32
    assert result["measurement_rows_by_source"] == {
        "PRX2007_POLLINATION": 1,
        "PRX2013_ALLEE": 8,
        "PRX2015_WATER": 15,
        "PRX2016_SELECTION": 8,
    }


def test_dryad_raw_data_is_the_highest_priority_recovery_target() -> None:
    result = build()
    raw = result["highest_priority_raw_recovery"]
    assert raw["source_id"] == "PRX2013_ALLEE"
    assert raw["dataset_doi"] == "10.5061/dryad.6cv06"
    assert raw["file"] == "raw data.xlsx"
    assert result["public_raw_data_sources"] == ["PRX2013_ALLEE"]


def test_2016_supplement_files_are_explicitly_tracked() -> None:
    result = build()
    second = result["second_priority_recovery"]
    assert second["source_id"] == "PRX2016_SELECTION"
    assert set(second["files"]) == {
        "supp_mcw097_aob-16074-s01.doc",
        "supp_mcw097_aob-16074-s02.xls",
    }
    assert result["public_supplement_sources"] == [
        "PRX2015_WATER",
        "PRX2016_SELECTION",
    ]


def test_reported_uncertainty_is_preserved_without_inventing_raw_variance() -> None:
    result = build()
    assert result["n_rows_with_reported_sd"] == 3
    assert set(result["rows_with_reported_sd"]) == {
        "PRX2016_CAPSULES_PER_PLANT",
        "PRX2016_OVULES_MEAN",
        "PRX2016_POLLEN_MEAN",
    }
    assert result["n_rows_with_reported_se"] == 12


def test_historical_measurements_do_not_directly_freeze_f0() -> None:
    result = build()
    assert result["n_direct_F0_freeze_values_recovered"] == 0
    assert result["published_data_can_replace_same_context_calibration_package"] is False
    assert result["status"] == (
        "PUBLISHED_EMPIRICAL_PRIORS_RECOVERED_CALIBRATION_STILL_REQUIRED"
    )

    priors = _rows(DEFAULT_PRIORS)
    assert {row["direct_freeze_eligible"] for row in priors} == {"NO"}

    datasets = _rows(DEFAULT_DATASETS)
    assert {row["direct_F0_freeze_eligible"] for row in datasets} == {"NO"}


def test_water_drain_experiment_remains_external_prior_not_independent_G() -> None:
    datasets = {
        row["source_id"]: row
        for row in _rows(DEFAULT_DATASETS)
    }
    water = datasets["PRX2015_WATER"]
    assert water["current_independent_G_evidence"].startswith("NO;")
    assert "DEPRECATED_SCH_G" in water["current_independent_G_evidence"]
    assert water["direct_F0_freeze_eligible"] == "NO"


def test_published_data_leave_the_registered_direct_empirical_gaps_open() -> None:
    result = build()
    assert set(result["remaining_direct_empirical_gaps"]) == {
        "same_flower_repeatability_for_registered_P0_metrics",
        "multi_level_P_rex_z_manipulation_with_off_target_checks",
        "P_rex_pollination_supplementation_effect_on_pollen_and_initial_seed_set",
        "independent_seed_predator_exclusion_effect_with_water_y_fixed",
        "independent_G_timing_window_qualified_in_P_rex",
    }

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


def test_published_empirical_recovery_has_nine_sources_and_69_measurements() -> None:
    result = build()
    assert result["n_published_sources"] == 9
    assert result["n_published_measurement_rows"] == 69
    assert result["measurement_rows_by_source"] == {
        "PRX2007_GAMETE": 1,
        "PRX2007_POLLINATION": 1,
        "PRX2013_ALLEE": 8,
        "PRX2014_BUZZ_MORPHOLOGY": 3,
        "PRX2013_OUTCROSSING": 3,
        "PRX2015_WATER": 15,
        "PRX2016_NECTAR_DYNAMICS": 28,
        "PRX2016_SELECTION": 10,
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
    assert result["n_rows_with_reported_sd"] == 8
    assert set(result["rows_with_reported_sd"]) == {
        "PRX2007_PO_RATIO_REX",
        "PRX2016_CAPSULES_PER_PLANT",
        "PRX2016_NECTAR_POOL_SUGAR",
        "PRX2016_NECTAR_POOL_VOL",
        "PRX2016_OVULES_MEAN",
        "PRX2016_POLLEN_GLM_POOL",
        "PRX2016_POLLEN_MEAN",
        "PRX2016_PREDATION_GLM_POOL",
    }
    assert result["n_rows_with_reported_se"] == 12
    assert result["n_rows_with_reported_sem"] == 3
    assert set(result["rows_with_reported_sem"]) == {
        "PRX2014_COROLLA_TUBE",
        "PRX2014_LOWER_LIP_WIDTH",
        "PRX2014_POLLEN_GRAIN_VOL",
    }


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


def test_focal_p_rex_nectar_dynamics_are_multisite_and_stage_resolved() -> None:
    priors = _rows(DEFAULT_PRIORS)
    nectar = [
        row for row in priors
        if row["source_id"] == "PRX2016_NECTAR_DYNAMICS"
    ]
    assert len(nectar) == 28
    stage_rows = [
        row for row in nectar
        if row["measurement_id"] not in {
            "PRX2016_NECTAR_POOL_VOL",
            "PRX2016_NECTAR_POOL_SUGAR",
        }
    ]
    assert len(stage_rows) == 26
    assert {row["population_scope"] for row in stage_rows} == {
        "Kunming, Yunnan",
        "Lijiang, Yunnan",
        "Daocheng, Sichuan",
    }

    pooled = {row["measurement_id"]: row for row in nectar}
    assert pooled["PRX2016_NECTAR_POOL_VOL"]["estimate"] == "1.13"
    assert pooled["PRX2016_NECTAR_POOL_VOL"]["uncertainty_value"] == "0.68"
    assert pooled["PRX2016_NECTAR_POOL_SUGAR"]["estimate"] == "33"
    assert pooled["PRX2016_NECTAR_POOL_SUGAR"]["uncertainty_value"] == "5"


def test_focal_p_rex_pollen_ovule_ratio_is_external_context_not_p1_effect() -> None:
    priors = {
        row["measurement_id"]: row
        for row in _rows(DEFAULT_PRIORS)
    }
    po = priors["PRX2007_PO_RATIO_REX"]
    assert po["estimate"] == "11222.04"
    assert po["uncertainty_type"] == "SD"
    assert po["uncertainty_value"] == "4887.18"
    assert po["direct_freeze_eligible"] == "NO"


def test_focal_p_rex_outcrossing_is_high_in_both_density_contexts() -> None:
    priors = {
        row["measurement_id"]: row
        for row in _rows(DEFAULT_PRIORS)
    }
    sparse = priors["PRX2013_OUTCROSS_SPARSE"]
    dense = priors["PRX2013_OUTCROSS_DENSE"]

    assert sparse["estimate"] == "1.151"
    assert dense["estimate"] == "0.924"
    assert sparse["uncertainty_value"] == "0.108"
    assert dense["uncertainty_value"] == "0.042"
    assert sparse["uncertainty_type"] == (
        "SECONDARY_REPORTED_UNCERTAINTY_TYPE_UNVERIFIED"
    )
    assert dense["uncertainty_type"] == (
        "SECONDARY_REPORTED_UNCERTAINTY_TYPE_UNVERIFIED"
    )
    assert sparse["direct_freeze_eligible"] == "NO"
    assert dense["direct_freeze_eligible"] == "NO"


def test_focal_outcrossing_source_does_not_become_supplementation_effect() -> None:
    datasets = {
        row["source_id"]: row
        for row in _rows(DEFAULT_DATASETS)
    }
    source = datasets["PRX2013_OUTCROSSING"]
    assert source["direct_F0_freeze_eligible"] == "NO"
    assert "NO_MANIPULATED_REGISTERED_P1_OR_G" in (
        source["current_independent_G_evidence"]
    )


def test_focal_p_rex_buzz_pollination_morphology_keeps_sem_separate() -> None:
    priors = {
        row["measurement_id"]: row
        for row in _rows(DEFAULT_PRIORS)
    }
    tube = priors["PRX2014_COROLLA_TUBE"]
    lip = priors["PRX2014_LOWER_LIP_WIDTH"]
    pollen = priors["PRX2014_POLLEN_GRAIN_VOL"]

    assert tube["estimate"] == "23.43"
    assert tube["uncertainty_type"] == "SEM"
    assert tube["uncertainty_value"] == "0.498"
    assert tube["sample_n"] == "20 specimens"

    assert lip["estimate"] == "12.71"
    assert lip["uncertainty_type"] == "SEM"
    assert lip["uncertainty_value"] == "0.382"

    assert pollen["estimate"] == "4448"
    assert pollen["uncertainty_type"] == "SEM"
    assert pollen["uncertainty_value"] == "89.28"
    assert pollen["sample_n"] == "20 plants"

    assert {tube["direct_freeze_eligible"], lip["direct_freeze_eligible"], pollen["direct_freeze_eligible"]} == {"NO"}

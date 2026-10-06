from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.validate_pedicularis_cohort_registry import REQUIRED_FIELDS, validate


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "empirical" / "architecture" / "PEDICULARIS_CALIBRATION_COHORT_TEMPLATE_V1.csv"


def _row(
    record_id: str,
    plant_id: str,
    flower_id: str,
    role: str,
    lane: str,
    basis: str,
    confirmatory: str,
) -> dict[str, str]:
    return {
        "record_id": record_id,
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "plant_id": plant_id,
        "flower_id": flower_id,
        "cohort_role": role,
        "lane": lane,
        "threshold_basis_eligible": basis,
        "confirmatory_eligible": confirmatory,
        "notes": "",
    }


def test_cohort_template_header_is_frozen() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS


def test_disjoint_calibration_and_confirmatory_cohorts_validate() -> None:
    rows = [
        _row("R1", "C01", "C01_F1", "CAL_A", "MULTI", "YES", "NO"),
        _row("R2", "C02", "C02_F1", "CAL_B_P1", "P1", "YES", "NO"),
        _row("R3", "C03", "C03_F1", "CAL_B_G", "G", "YES", "NO"),
        _row("R3T", "C04", "C04_F1", "CAL_B_G_TIMING", "G", "YES", "NO"),
        _row("R4", "V01", "V01_F1", "CONFIRMATORY_P0", "P0", "NO", "YES"),
        _row("R5", "V02", "V02_F1", "CONFIRMATORY_P1", "P1", "NO", "YES"),
        _row("R6", "V03", "V03_F1", "CONFIRMATORY_G", "G", "NO", "YES"),
        _row("R7", "S01", "S01_F1", "FULL_SURFACE", "P0_P1_G", "NO", "YES"),
    ]
    result = validate(rows)
    assert result["status"] == "PEDICULARIS_COHORT_REGISTRY_VALID"
    assert result["independence_status"] == "PLANT_AND_FLOWER_LEVEL_DISJOINT"
    assert result["n_shared_plants_across_calibration_and_confirmatory"] == 0


def test_flower_reuse_between_calibration_and_confirmatory_is_blocked() -> None:
    rows = [
        _row("R1", "P01", "F1", "CAL_A", "MULTI", "YES", "NO"),
        _row("R2", "P01", "F1", "CONFIRMATORY_P0", "P0", "NO", "YES"),
    ]
    with pytest.raises(ValueError, match="flower_id must be globally unique"):
        validate(rows)


def test_plant_overlap_is_reported_but_not_mislabelled_as_data_reuse() -> None:
    rows = [
        _row("R1", "P01", "F1", "CAL_A", "MULTI", "YES", "NO"),
        _row("R2", "P01", "F2", "CONFIRMATORY_P0", "P0", "NO", "YES"),
    ]
    result = validate(rows)
    assert result["independence_status"] == "FLOWER_LEVEL_DISJOINT_PLANT_OVERLAP_PRESENT"
    assert result["shared_plant_ids"] == ["P01"]
    assert result["flower_level_reuse_detected"] is False


def test_threshold_basis_record_cannot_be_confirmatory() -> None:
    row = _row("R1", "P01", "F1", "CAL_A", "MULTI", "YES", "YES")
    with pytest.raises(ValueError, match="confirmatory_eligible mismatch"):
        validate([row])


def test_registry_is_single_population_and_season() -> None:
    rows = [
        _row("R1", "P01", "F1", "CAL_A", "MULTI", "YES", "NO"),
        _row("R2", "P02", "F2", "CONFIRMATORY_P0", "P0", "NO", "YES"),
    ]
    rows[1]["season_id"] = "S2"
    with pytest.raises(ValueError, match="exactly one population and season"):
        validate(rows)


def test_g_event_time_role_is_threshold_basis_only() -> None:
    row = _row(
        "RT",
        "T01",
        "T01_F1",
        "CAL_B_G_TIMING",
        "G",
        "YES",
        "NO",
    )
    result = validate([row])
    assert result["role_counts"]["CAL_B_G_TIMING"] == 1

    row["confirmatory_eligible"] = "YES"
    with pytest.raises(ValueError, match="confirmatory_eligible mismatch"):
        validate([row])


def test_power_geometry_pilot_role_is_nonconfirmatory_and_nonthreshold() -> None:
    row = _row(
        "PG1",
        "GP01",
        "GP01_F1",
        "POWER_GEOMETRY_PILOT",
        "P0_P1_G",
        "NO",
        "NO",
    )
    result = validate([row])

    assert result["role_counts"]["POWER_GEOMETRY_PILOT"] == 1
    assert result["n_power_geometry_pilot_plants"] == 1
    assert result["power_geometry_pilot_plant_overlap_detected"] is False


def test_power_geometry_pilot_plant_cannot_reappear_in_full_surface() -> None:
    rows = [
        _row(
            "PG1",
            "P01",
            "P01_GP",
            "POWER_GEOMETRY_PILOT",
            "P0_P1_G",
            "NO",
            "NO",
        ),
        _row(
            "FS1",
            "P01",
            "P01_FS",
            "FULL_SURFACE",
            "P0_P1_G",
            "NO",
            "YES",
        ),
    ]

    with pytest.raises(ValueError, match="POWER_GEOMETRY_PILOT plants must be disjoint"):
        validate(rows)


def test_power_geometry_pilot_plant_cannot_reappear_in_calibration() -> None:
    rows = [
        _row(
            "PG1",
            "P01",
            "P01_GP",
            "POWER_GEOMETRY_PILOT",
            "P0_P1_G",
            "NO",
            "NO",
        ),
        _row(
            "CA1",
            "P01",
            "P01_CA",
            "CAL_A",
            "MULTI",
            "YES",
            "NO",
        ),
    ]

    with pytest.raises(ValueError, match="POWER_GEOMETRY_PILOT plants must be disjoint"):
        validate(rows)

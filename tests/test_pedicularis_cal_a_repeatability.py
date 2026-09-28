from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.summarize_pedicularis_cal_a_repeatability import (
    REQUIRED_FIELDS,
    build,
    read_rows,
)


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_CAL_A_REPEATABILITY_TEMPLATE_V1.csv"
)


def _rows(season: str = "S1") -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for plant in range(4):
        for flower in range(2):
            base = 0.40 + 0.04 * plant + 0.01 * flower
            flower_id = f"P{plant:02d}_F{flower:02d}"
            for rep, shift in ((1, -0.005), (2, 0.005)):
                rows.append(
                    {
                        "population_id": "P_REX_TEST",
                        "season_id": season,
                        "plant_id": f"P{plant:02d}",
                        "flower_id": flower_id,
                        "measurement_replicate": str(rep),
                        "observer_id": "OBS_A" if rep == 1 else "OBS_B",
                        "realized_exsertion": f"{base + shift:.5f}",
                        "corolla_opening_width": f"{8.0 + 0.02 * flower + shift:.5f}",
                        "lower_lip_angle_deg": f"{25.0 + 0.10 * flower + shift:.5f}",
                        "tube_diameter": f"{4.0 + 0.01 * flower + shift:.5f}",
                        "bract_height": f"{20.0 + 0.03 * flower + shift:.5f}",
                        "water_depth": f"{5.0 + 0.02 * flower + shift:.5f}",
                        "flower_orientation_deg": f"{15.0 + 0.10 * flower + shift:.5f}",
                    }
                )
    return rows


def _write(path: Path, rows: list[dict[str, str]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(REQUIRED_FIELDS))
        writer.writeheader()
        writer.writerows(rows)
    return path


def test_repeatability_template_header_is_frozen() -> None:
    with TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == REQUIRED_FIELDS


def test_repeatability_summary_reports_measurement_noise_without_margin_decision(tmp_path: Path) -> None:
    path = _write(tmp_path / "repeat.csv", _rows())
    result = build(read_rows(path))

    assert result["status"] == "CAL_A_REPEATABILITY_SUMMARY_ONLY_NO_MARGIN_DECISION"
    assert result["thresholds_selected"] is False
    assert result["confirmatory_receipt_generated"] is False
    assert result["n_plants"] == 4
    assert result["n_flowers"] == 8
    assert result["observer_counts"] == {"OBS_A": 8, "OBS_B": 8}

    exsertion = result["metric_repeatability"]["realized_exsertion"]
    assert exsertion["pooled_within_flower_sd"] > 0
    assert exsertion["max_absolute_deviation_from_flower_mean"]["q95"] == pytest.approx(0.005)
    assert exsertion["max_relative_deviation_from_flower_mean"]["q95"] > 0

    water = result["metric_repeatability"]["water_depth"]
    assert "max_relative_deviation_from_flower_mean" not in water
    assert water["max_absolute_deviation_from_flower_mean"]["q95"] == pytest.approx(0.005)


def test_every_flower_requires_two_measurement_replicates(tmp_path: Path) -> None:
    rows = _rows()
    rows = [row for row in rows if not (
        row["flower_id"] == "P00_F00"
        and row["measurement_replicate"] == "2"
    )]
    path = _write(tmp_path / "repeat.csv", rows)
    with pytest.raises(ValueError, match="requires >=2"):
        read_rows(path)


def test_repeatability_package_is_single_population_and_season(tmp_path: Path) -> None:
    rows = _rows()
    rows[-1]["season_id"] = "S2"
    path = _write(tmp_path / "repeat.csv", rows)
    with pytest.raises(ValueError, match="exactly one population and season"):
        read_rows(path)


def test_duplicate_flower_replicate_is_rejected(tmp_path: Path) -> None:
    rows = _rows()
    rows.append(dict(rows[0]))
    path = _write(tmp_path / "repeat.csv", rows)
    with pytest.raises(ValueError, match="must be unique"):
        read_rows(path)

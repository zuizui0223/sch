from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts import evaluate_pedicularis_predator_method as gmethod
from scripts.materialize_pedicularis_g_field_rows import (
    FOCAL_REQUIRED_FIELDS,
    PROXY_REQUIRED_FIELDS,
    build,
    _write_csv,
)


ROOT = Path(__file__).resolve().parents[1]
FOCAL_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_FOCAL_FIELD_TEMPLATE_V1.csv"
)
PROXY_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_POLLEN_PROXY_TEMPLATE_V1.csv"
)


def _write(
    path: Path,
    fields: tuple[str, ...],
    rows: list[dict[str, str]],
) -> Path:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields))
        writer.writeheader()
        writer.writerows(rows)
    return path


def _focal_rows(
    *,
    season: str = "S1",
) -> list[dict[str, str]]:
    rows = []
    for plant in ("P01", "P02"):
        for treatment in ("EXPOSED", "EXCLUDED"):
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": season,
                    "plant_id": plant,
                    "flower_id": f"{plant}_{treatment}_END",
                    "predator_treatment": treatment,
                    "exclusion_method": (
                        "SHAM_SLEEVE"
                        if treatment == "EXPOSED"
                        else "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
                    ),
                    "sham_device_applied": (
                        "1" if treatment == "EXPOSED" else "0"
                    ),
                    "anthesis_time_hours": "0",
                    "barrier_application_time_hours": "12",
                    "pollination_window_complete_before_barrier": "1",
                    "ovary_swollen_at_barrier": "0",
                    "barrier_covers_pollinator_entry": "0",
                    "pre_barrier_attack_present": "0",
                    "barrier_integrity_failure_present": "0",
                    "realized_exsertion": "0.50",
                    "water_depth": "10.0",
                    "pollinator_visits": "4",
                    "early_predator_attack_present": (
                        "1" if treatment == "EXPOSED" else "0"
                    ),
                    "ovule_count": "100",
                    "undamaged_seed_count": (
                        "50" if treatment == "EXPOSED" else "70"
                    ),
                    "damaged_seed_count": (
                        "20" if treatment == "EXPOSED" else "2"
                    ),
                    "mechanical_damage": "0",
                }
            )
    return rows


def _proxy_rows(
    *,
    season: str = "S1",
    two_proxies: bool = False,
) -> list[dict[str, str]]:
    rows = []
    for plant_index, plant in enumerate(("P01", "P02"), start=1):
        for treatment in ("EXPOSED", "EXCLUDED"):
            base = 100 + 10 * plant_index
            if treatment == "EXCLUDED":
                base += 5
            values = [base]
            if two_proxies:
                values.append(base + 10)
            for index, pollen in enumerate(values, start=1):
                rows.append(
                    {
                        "population_id": "P_REX_TEST",
                        "season_id": season,
                        "plant_id": plant,
                        "predator_treatment": treatment,
                        "proxy_flower_id": (
                            f"{plant}_{treatment}_POLLEN_{index}"
                        ),
                        "proxy_anthesis_time_hours": "0",
                        "proxy_collection_time_hours": "10",
                        "pollination_window_complete_before_collection": "1",
                        "pollen_grains": str(pollen),
                        "notes": "synthetic unit-test proxy",
                    }
                )
    return rows


def test_g_field_templates_match_registered_materializer_contract() -> None:
    with FOCAL_TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == FOCAL_REQUIRED_FIELDS

    with PROXY_TEMPLATE.open(encoding="utf-8", newline="") as handle:
        assert tuple(next(csv.reader(handle))) == PROXY_REQUIRED_FIELDS


def test_materializer_assigns_matched_proxy_means_to_canonical_v4_rows(
    tmp_path: Path,
) -> None:
    focal = _write(
        tmp_path / "focal.csv",
        FOCAL_REQUIRED_FIELDS,
        _focal_rows(),
    )
    proxy = _write(
        tmp_path / "proxy.csv",
        PROXY_REQUIRED_FIELDS,
        _proxy_rows(two_proxies=True),
    )

    rows, receipt = build(focal, proxy)

    assert receipt["status"] == (
        "PEDICULARIS_G_FIELD_ROWS_READY_FOR_"
        "THRESHOLD_FREE_CALIBRATION_SUMMARY"
    )
    assert receipt["n_focal_endpoint_rows"] == 4
    assert receipt["n_pollen_proxy_rows"] == 8
    assert receipt["n_plant_treatment_pairs"] == 4
    assert receipt["all_focal_pairs_have_pollen_proxy"] is True
    assert receipt["proxy_flowers_disjoint_from_endpoint_flowers"] is True

    by_pair = {
        (row["plant_id"], row["predator_treatment"]): row
        for row in rows
    }
    assert float(by_pair[("P01", "EXPOSED")]["pollen_grains"]) == pytest.approx(
        115.0
    )
    assert float(by_pair[("P01", "EXCLUDED")]["pollen_grains"]) == pytest.approx(
        120.0
    )
    assert float(by_pair[("P02", "EXPOSED")]["pollen_grains"]) == pytest.approx(
        125.0
    )
    assert float(by_pair[("P02", "EXCLUDED")]["pollen_grains"]) == pytest.approx(
        130.0
    )

    out = tmp_path / "v4.csv"
    _write_csv(out, rows)
    canonical = gmethod.read_rows(out)
    assert len(canonical) == 4
    assert set(canonical[0]) >= set(gmethod.REQUIRED_FIELDS)


def test_missing_pollen_proxy_for_one_plant_treatment_pair_fails_closed(
    tmp_path: Path,
) -> None:
    focal = _write(
        tmp_path / "focal.csv",
        FOCAL_REQUIRED_FIELDS,
        _focal_rows(),
    )
    proxies = [
        row
        for row in _proxy_rows()
        if not (
            row["plant_id"] == "P02"
            and row["predator_treatment"] == "EXCLUDED"
        )
    ]
    proxy = _write(
        tmp_path / "proxy.csv",
        PROXY_REQUIRED_FIELDS,
        proxies,
    )

    with pytest.raises(ValueError, match="missing pollen proxy rows"):
        build(focal, proxy)


def test_proxy_flower_cannot_be_a_focal_endpoint_flower(
    tmp_path: Path,
) -> None:
    focal_rows = _focal_rows()
    proxy_rows = _proxy_rows()
    proxy_rows[0]["proxy_flower_id"] = focal_rows[0]["flower_id"]

    focal = _write(
        tmp_path / "focal.csv",
        FOCAL_REQUIRED_FIELDS,
        focal_rows,
    )
    proxy = _write(
        tmp_path / "proxy.csv",
        PROXY_REQUIRED_FIELDS,
        proxy_rows,
    )

    with pytest.raises(ValueError, match="must be disjoint"):
        build(focal, proxy)


def test_proxy_must_be_collected_after_pollination_window_complete(
    tmp_path: Path,
) -> None:
    proxy_rows = _proxy_rows()
    proxy_rows[0]["pollination_window_complete_before_collection"] = "0"

    focal = _write(
        tmp_path / "focal.csv",
        FOCAL_REQUIRED_FIELDS,
        _focal_rows(),
    )
    proxy = _write(
        tmp_path / "proxy.csv",
        PROXY_REQUIRED_FIELDS,
        proxy_rows,
    )

    with pytest.raises(ValueError, match="pollination window is complete"):
        build(focal, proxy)


def test_proxy_collection_cannot_precede_proxy_anthesis(
    tmp_path: Path,
) -> None:
    proxy_rows = _proxy_rows()
    proxy_rows[0]["proxy_collection_time_hours"] = "-1"

    focal = _write(
        tmp_path / "focal.csv",
        FOCAL_REQUIRED_FIELDS,
        _focal_rows(),
    )
    proxy = _write(
        tmp_path / "proxy.csv",
        PROXY_REQUIRED_FIELDS,
        proxy_rows,
    )

    with pytest.raises(ValueError, match="cannot precede"):
        build(focal, proxy)


def test_proxy_and_focal_contexts_must_match(
    tmp_path: Path,
) -> None:
    focal = _write(
        tmp_path / "focal.csv",
        FOCAL_REQUIRED_FIELDS,
        _focal_rows(season="S1"),
    )
    proxy = _write(
        tmp_path / "proxy.csv",
        PROXY_REQUIRED_FIELDS,
        _proxy_rows(season="S2"),
    )

    with pytest.raises(ValueError, match="share exactly one"):
        build(focal, proxy)

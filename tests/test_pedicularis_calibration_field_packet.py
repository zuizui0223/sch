from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts import evaluate_pedicularis_pollination_weight as p1mod
from scripts import evaluate_pedicularis_stage_p0 as p0mod
from scripts import summarize_pedicularis_cal_a_repeatability as repmod
from scripts.build_pedicularis_calibration_field_packet import build_field_packet
from scripts.materialize_pedicularis_g_field_rows import (
    FOCAL_REQUIRED_FIELDS,
    PROXY_REQUIRED_FIELDS,
)
from scripts.validate_pedicularis_cohort_registry import (
    REQUIRED_FIELDS as REG_FIELDS,
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


def _p0_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(2):
        for rank in range(5):
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"A{plant}",
                    "flower_id": f"A{plant}_Z{rank}",
                    "assigned_z_level": f"Z{rank}",
                    "assigned_z_rank": str(rank),
                    "sham_control": "1" if rank == 4 else "0",
                    "realized_exsertion": str(0.2 + 0.15 * rank),
                    "corolla_opening_width": "8",
                    "lower_lip_angle_deg": "25",
                    "tube_diameter": "4",
                    "bract_height": "20",
                    "water_depth": "5",
                    "flower_orientation_deg": "15",
                    "mechanical_damage": "0",
                    "pollinator_visits": "3",
                    "pollen_grains": str(10 + rank),
                }
            )
    return rows


def _repeatability_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(2):
        flower_id = f"A{plant}_Z0"
        for rep, shift in ((1, -0.002), (2, 0.002)):
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"A{plant}",
                    "flower_id": flower_id,
                    "measurement_replicate": str(rep),
                    "observer_id": f"O{rep}",
                    "realized_exsertion": str(0.2 + shift),
                    "corolla_opening_width": str(8 + shift),
                    "lower_lip_angle_deg": str(25 + shift),
                    "tube_diameter": str(4 + shift),
                    "bract_height": str(20 + shift),
                    "water_depth": str(5 + shift),
                    "flower_orientation_deg": str(15 + shift),
                }
            )
    return rows


def _p1_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(2):
        for treatment in ("NATURAL", "SUPPLEMENTED"):
            sup = treatment == "SUPPLEMENTED"
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"B{plant}",
                    "flower_id": f"B{plant}_{treatment}",
                    "pollination_treatment": treatment,
                    "realized_exsertion": "0.5",
                    "water_depth": "5",
                    "bract_height": "20",
                    "corolla_opening_width": "8",
                    "mechanical_damage": "0",
                    "pollen_grains_post_treatment": "25" if sup else "10",
                    "early_predator_attack_present": "0",
                    "ovule_count": "20",
                    "undamaged_seed_count": "10" if sup else "6",
                    "damaged_seed_count": "2",
                }
            )
    return rows


def _g_focal_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(2):
        for treatment in ("EXPOSED", "EXCLUDED"):
            exp = treatment == "EXPOSED"
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"C{plant}",
                    "flower_id": f"C{plant}_{treatment}_END",
                    "predator_treatment": treatment,
                    "exclusion_method": (
                        "SHAM_SLEEVE"
                        if exp
                        else "POST_POLLINATION_LOWER_FLOWER_SLEEVE"
                    ),
                    "sham_device_applied": "1" if exp else "0",
                    "anthesis_time_hours": "0",
                    "barrier_application_time_hours": "12",
                    "pollination_window_complete_before_barrier": "1",
                    "ovary_swollen_at_barrier": "0",
                    "barrier_covers_pollinator_entry": "0",
                    "pre_barrier_attack_present": "0",
                    "barrier_integrity_failure_present": "0",
                    "realized_exsertion": "0.5",
                    "water_depth": "10",
                    "pollinator_visits": "4",
                    "early_predator_attack_present": "1" if exp else "0",
                    "ovule_count": "100",
                    "undamaged_seed_count": "50" if exp else "70",
                    "damaged_seed_count": "20" if exp else "2",
                    "mechanical_damage": "0",
                }
            )
    return rows


def _g_proxy_rows() -> list[dict[str, str]]:
    rows = []
    for plant in range(2):
        for treatment in ("EXPOSED", "EXCLUDED"):
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"C{plant}",
                    "predator_treatment": treatment,
                    "proxy_flower_id": f"C{plant}_{treatment}_POLLEN",
                    "proxy_anthesis_time_hours": "0",
                    "proxy_collection_time_hours": "10",
                    "pollination_window_complete_before_collection": "1",
                    "pollen_grains": "100",
                    "notes": "synthetic",
                }
            )
    return rows


def _registry(
    p0_rows: list[dict[str, str]],
    p1_rows: list[dict[str, str]],
    g_focal_rows: list[dict[str, str]],
    g_proxy_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(
        *,
        plant_id: str,
        flower_id: str,
        role: str,
        lane: str,
    ) -> None:
        rows.append(
            {
                "record_id": f"R{len(rows)+1:03d}",
                "population_id": "P_REX_TEST",
                "season_id": "S1",
                "plant_id": plant_id,
                "flower_id": flower_id,
                "cohort_role": role,
                "lane": lane,
                "threshold_basis_eligible": "YES",
                "confirmatory_eligible": "NO",
                "notes": "",
            }
        )

    for row in p0_rows:
        add(
            plant_id=row["plant_id"],
            flower_id=row["flower_id"],
            role="CAL_A",
            lane="MULTI",
        )

    for row in p1_rows:
        add(
            plant_id=row["plant_id"],
            flower_id=row["flower_id"],
            role="CAL_B_P1",
            lane="P1",
        )

    for row in g_focal_rows:
        add(
            plant_id=row["plant_id"],
            flower_id=row["flower_id"],
            role="CAL_B_G",
            lane="G",
        )

    for row in g_proxy_rows:
        add(
            plant_id=row["plant_id"],
            flower_id=row["proxy_flower_id"],
            role="CAL_B_G",
            lane="G",
        )

    return rows


def _paths(tmp_path: Path) -> dict[str, Path]:
    p0 = _p0_rows()
    rep = _repeatability_rows()
    p1 = _p1_rows()
    g_focal = _g_focal_rows()
    g_proxy = _g_proxy_rows()
    registry = _registry(p0, p1, g_focal, g_proxy)

    return {
        "registry": _write(
            tmp_path / "registry.csv",
            REG_FIELDS,
            registry,
        ),
        "repeatability": _write(
            tmp_path / "repeatability.csv",
            repmod.REQUIRED_FIELDS,
            rep,
        ),
        "p0": _write(
            tmp_path / "p0.csv",
            p0mod.REQUIRED_FIELDS,
            p0,
        ),
        "p1": _write(
            tmp_path / "p1.csv",
            p1mod.REQUIRED_FIELDS,
            p1,
        ),
        "g_focal": _write(
            tmp_path / "g_focal.csv",
            FOCAL_REQUIRED_FIELDS,
            g_focal,
        ),
        "g_proxy": _write(
            tmp_path / "g_proxy.csv",
            PROXY_REQUIRED_FIELDS,
            g_proxy,
        ),
        "g_materialized": tmp_path / "g_v4.csv",
    }


def test_complete_field_packet_builds_existing_calibration_summaries(
    tmp_path: Path,
) -> None:
    p = _paths(tmp_path)

    rep, cal, g_receipt, field_receipt = build_field_packet(
        registry_path=p["registry"],
        repeatability_path=p["repeatability"],
        p0_path=p["p0"],
        p1_path=p["p1"],
        g_focal_path=p["g_focal"],
        g_proxy_path=p["g_proxy"],
        g_materialized_out=p["g_materialized"],
    )

    assert field_receipt["status"] == (
        "PEDICULARIS_CALIBRATION_FIELD_PACKET_"
        "READY_FOR_TARGET_FREEZE"
    )
    assert field_receipt["g_proxy_registration"][
        "all_proxy_flowers_registered_as_CAL_B_G"
    ] is True
    assert field_receipt["n_g_endpoint_rows"] == 4
    assert field_receipt["n_g_pollen_proxy_rows"] == 4
    assert rep["status"] == (
        "CAL_A_REPEATABILITY_SUMMARY_ONLY_NO_MARGIN_DECISION"
    )
    assert cal["status"] == (
        "CALIBRATION_SUMMARY_ONLY_NO_THRESHOLD_DECISION"
    )
    assert g_receipt["all_focal_pairs_have_pollen_proxy"] is True
    assert p["g_materialized"].exists()


def test_unregistered_g_proxy_flower_fails_before_package_build(
    tmp_path: Path,
) -> None:
    p = _paths(tmp_path)

    with p["registry"].open(encoding="utf-8", newline="") as handle:
        registry = list(csv.DictReader(handle))

    with p["g_proxy"].open(encoding="utf-8", newline="") as handle:
        proxies = list(csv.DictReader(handle))

    missing_id = proxies[0]["proxy_flower_id"]
    registry = [
        row
        for row in registry
        if row["flower_id"] != missing_id
    ]
    _write(p["registry"], REG_FIELDS, registry)

    with pytest.raises(ValueError, match="missing from cohort registry"):
        build_field_packet(
            registry_path=p["registry"],
            repeatability_path=p["repeatability"],
            p0_path=p["p0"],
            p1_path=p["p1"],
            g_focal_path=p["g_focal"],
            g_proxy_path=p["g_proxy"],
            g_materialized_out=p["g_materialized"],
        )


def test_g_proxy_must_be_registered_as_cal_b_g(
    tmp_path: Path,
) -> None:
    p = _paths(tmp_path)

    with p["registry"].open(encoding="utf-8", newline="") as handle:
        registry = list(csv.DictReader(handle))
    with p["g_proxy"].open(encoding="utf-8", newline="") as handle:
        proxies = list(csv.DictReader(handle))

    target = next(
        row
        for row in registry
        if row["flower_id"] == proxies[0]["proxy_flower_id"]
    )
    target["cohort_role"] = "CAL_A"
    target["lane"] = "MULTI"
    _write(p["registry"], REG_FIELDS, registry)

    with pytest.raises(ValueError, match="registered as CAL_B_G"):
        build_field_packet(
            registry_path=p["registry"],
            repeatability_path=p["repeatability"],
            p0_path=p["p0"],
            p1_path=p["p1"],
            g_focal_path=p["g_focal"],
            g_proxy_path=p["g_proxy"],
            g_materialized_out=p["g_materialized"],
        )


def test_g_proxy_registry_plant_identity_must_match_data(
    tmp_path: Path,
) -> None:
    p = _paths(tmp_path)

    with p["registry"].open(encoding="utf-8", newline="") as handle:
        registry = list(csv.DictReader(handle))
    with p["g_proxy"].open(encoding="utf-8", newline="") as handle:
        proxies = list(csv.DictReader(handle))

    target = next(
        row
        for row in registry
        if row["flower_id"] == proxies[0]["proxy_flower_id"]
    )
    target["plant_id"] = "WRONG_PLANT"
    _write(p["registry"], REG_FIELDS, registry)

    with pytest.raises(ValueError, match="identity mismatch"):
        build_field_packet(
            registry_path=p["registry"],
            repeatability_path=p["repeatability"],
            p0_path=p["p0"],
            p1_path=p["p1"],
            g_focal_path=p["g_focal"],
            g_proxy_path=p["g_proxy"],
            g_materialized_out=p["g_materialized"],
        )

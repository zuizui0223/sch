from __future__ import annotations

import csv
from pathlib import Path

import pytest

from scripts.build_pedicularis_p0_randomized_assignment import (
    ASSIGNMENT_METHOD,
    _read_level_plan,
    build,
)


ROOT = Path(__file__).resolve().parents[1]
LEVEL_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_P0_LEVEL_PLAN_TEMPLATE_V1.csv"
)
FLOWER_TEMPLATE = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_P0_FLOWER_MANIFEST_TEMPLATE_V1.csv"
)


def _levels(n: int = 5) -> list[dict[str, str]]:
    return [
        {
            "assigned_z_level": f"Z{i}",
            "assigned_z_rank": str(i),
            "sham_control": "1" if i == n - 1 else "0",
        }
        for i in range(n)
    ]


def _flowers(n_plants: int = 4, n_levels: int = 5) -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{plant:02d}",
            "flower_id": f"P{plant:02d}_F{flower:02d}",
        }
        for plant in range(n_plants)
        for flower in range(n_levels)
    ]


def _assignment_map(
    rows: list[dict[str, str]],
) -> dict[tuple[str, str], str]:
    return {
        (row["plant_id"], row["assigned_z_level"]): row["flower_id"]
        for row in rows
    }


def test_templates_are_treatment_blind_before_allocation() -> None:
    with FLOWER_TEMPLATE.open(encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle))
    assert header == [
        "population_id",
        "season_id",
        "plant_id",
        "flower_id",
    ]

    with LEVEL_TEMPLATE.open(encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle))
        assert list(csv.reader(handle)) == []
    assert header == [
        "assigned_z_level",
        "assigned_z_rank",
        "sham_control",
    ]


def test_complete_block_randomizes_each_plant_across_all_levels() -> None:
    allocations, receipt = build(
        _flowers(),
        _levels(),
        allocation_seed="p0-seed-a",
    )

    assert receipt["n_plants"] == 4
    assert receipt["n_z_levels"] == 5
    assert receipt["n_allocated_flowers"] == 20
    assert receipt["assignment_randomized_within_plant"] is True
    assert receipt["allocation_algorithm"] == ASSIGNMENT_METHOD
    assert receipt["sample_size_chosen_by_script"] is False
    assert receipt["z_level_values_chosen_by_script"] is False

    for plant in {row["plant_id"] for row in allocations}:
        subset = [row for row in allocations if row["plant_id"] == plant]
        assert {row["assigned_z_rank"] for row in subset} == {
            "0",
            "1",
            "2",
            "3",
            "4",
        }
        assert sum(int(row["sham_control"]) for row in subset) == 1
        assert {row["assignment_method"] for row in subset} == {
            ASSIGNMENT_METHOD
        }


def test_assignment_is_reproducible_and_seed_sensitive() -> None:
    first, first_receipt = build(
        _flowers(),
        _levels(),
        allocation_seed="p0-seed-a",
    )
    repeat, repeat_receipt = build(
        _flowers(),
        _levels(),
        allocation_seed="p0-seed-a",
    )
    alternate, alternate_receipt = build(
        _flowers(),
        _levels(),
        allocation_seed="p0-seed-b",
    )

    assert _assignment_map(first) == _assignment_map(repeat)
    assert _assignment_map(first) != _assignment_map(alternate)
    assert (
        first_receipt["allocation_seed_sha256"]
        == repeat_receipt["allocation_seed_sha256"]
    )
    assert (
        first_receipt["allocation_seed_sha256"]
        != alternate_receipt["allocation_seed_sha256"]
    )


def test_wrong_flower_count_per_plant_fails_closed() -> None:
    flowers = _flowers()
    flowers.pop()
    with pytest.raises(ValueError, match="exactly one flower per planned z level"):
        build(flowers, _levels(), allocation_seed="p0-seed-a")


def test_level_plan_requires_five_levels_unique_ranks_and_one_sham() -> None:
    with pytest.raises(ValueError, match="at least five"):
        build(_flowers(n_levels=4), _levels(4), allocation_seed="p0-seed-a")

    levels = _levels()
    levels[1]["assigned_z_rank"] = levels[0]["assigned_z_rank"]
    with pytest.raises(ValueError):
        build(_flowers(), levels, allocation_seed="p0-seed-a")

    levels = _levels()
    levels[0]["sham_control"] = "1"
    with pytest.raises(ValueError, match="exactly one sham"):
        build(_flowers(), levels, allocation_seed="p0-seed-a")


def test_unresolved_seed_and_duplicate_flowers_fail_closed() -> None:
    with pytest.raises(ValueError, match="allocation_seed"):
        build(_flowers(), _levels(), allocation_seed="REQUIRED_BEFORE_USE")

    flowers = _flowers()
    flowers[1]["flower_id"] = flowers[0]["flower_id"]
    with pytest.raises(ValueError, match="flower_id must be unique"):
        build(flowers, _levels(), allocation_seed="p0-seed-a")


def test_level_plan_parser_rejects_empty_template() -> None:
    with pytest.raises(ValueError, match="no data rows"):
        _read_level_plan(LEVEL_TEMPLATE)

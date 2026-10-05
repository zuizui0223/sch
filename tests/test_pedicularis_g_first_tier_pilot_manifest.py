import pytest

from scripts.build_pedicularis_g_first_tier_pilot_manifest import build


def _rows(n: int = 4) -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{i:02d}",
            "flower_id_1": f"P{i:02d}_1",
            "flower_id_2": f"P{i:02d}_2",
            "flower_id_3": f"P{i:02d}_3",
        }
        for i in range(n)
    ]


def _assignment_map(
    allocations: list[dict[str, str]],
) -> dict[tuple[str, str], str]:
    return {
        (row["plant_id"], row["pilot_arm_id"]): row["flower_id"]
        for row in allocations
    }


def test_first_tier_manifest_allocates_three_arms_per_input_plant() -> None:
    allocations, receipt = build(_rows(), allocation_seed="seed-a")

    assert receipt["n_plants"] == 4
    assert receipt["n_allocated_flowers"] == 12
    assert receipt["arms_per_plant"] == 3
    assert receipt["candidate_ids_tested"] == [
        "G_A1_FINE_MESH",
        "G_A2_POROUS_TUBING",
    ]
    assert receipt["candidate_selected"] is False
    assert receipt["sample_size_chosen_by_script"] is False
    assert receipt["assignment_randomized_within_plant"] is True
    assert receipt["allocation_algorithm"] == "SHA256_RANK_V1"
    assert receipt["allocation_seed"] == "seed-a"

    for plant in {row["plant_id"] for row in allocations}:
        subset = [row for row in allocations if row["plant_id"] == plant]
        assert {row["pilot_arm_id"] for row in subset} == {
            "EXPOSED_SHAM",
            "G_A1_FINE_MESH",
            "G_A2_POROUS_TUBING",
        }
        assert {row["assignment_method"] for row in subset} == {
            "SHA256_RANK_V1"
        }


def test_manifest_uses_exact_canonical_field_method_codes() -> None:
    allocations, _ = build(_rows(2), allocation_seed="seed-a")
    excluded = {
        row["pilot_arm_id"]: row["exclusion_method"]
        for row in allocations
        if row["predator_treatment"] == "EXCLUDED"
    }

    assert excluded == {
        "G_A1_FINE_MESH": "FINE_MESH_LOWER_FRUIT_SLEEVE",
        "G_A2_POROUS_TUBING": "POROUS_TUBING_LOWER_FRUIT_SLEEVE",
    }


def test_exposed_arm_has_sham_and_candidates_do_not() -> None:
    allocations, _ = build(_rows(2), allocation_seed="seed-a")
    for row in allocations:
        if row["pilot_arm_id"] == "EXPOSED_SHAM":
            assert row["predator_treatment"] == "EXPOSED"
            assert row["sham_device_applied"] == "1"
            assert row["exclusion_method"] == "SHAM_SLEEVE"
        else:
            assert row["predator_treatment"] == "EXCLUDED"
            assert row["sham_device_applied"] == "0"


def test_assignment_is_reproducible_and_seed_sensitive() -> None:
    first, first_receipt = build(_rows(), allocation_seed="seed-a")
    repeat, repeat_receipt = build(_rows(), allocation_seed="seed-a")
    alternate, alternate_receipt = build(_rows(), allocation_seed="seed-b")

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


def test_script_does_not_invent_a_sample_size() -> None:
    _, small = build(_rows(2), allocation_seed="seed-a")
    _, large = build(_rows(7), allocation_seed="seed-a")

    assert small["n_plants"] == 2
    assert large["n_plants"] == 7
    assert small["sample_size_chosen_by_script"] is False
    assert large["sample_size_chosen_by_script"] is False


def test_flower_reuse_within_or_across_plants_fails_closed() -> None:
    rows = _rows(2)
    rows[0]["flower_id_2"] = rows[0]["flower_id_1"]
    with pytest.raises(ValueError, match="reuses a flower"):
        build(rows, allocation_seed="seed-a")

    rows = _rows(2)
    rows[1]["flower_id_2"] = rows[0]["flower_id_2"]
    with pytest.raises(ValueError, match="unique across"):
        build(rows, allocation_seed="seed-a")


def test_context_plant_ids_and_seed_must_be_resolved() -> None:
    rows = _rows(2)
    rows[1]["season_id"] = "S2"
    with pytest.raises(ValueError, match="one population and season"):
        build(rows, allocation_seed="seed-a")

    rows = _rows(2)
    rows[0]["plant_id"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="resolved plant_id"):
        build(rows, allocation_seed="seed-a")

    with pytest.raises(ValueError, match="allocation_seed must be resolved"):
        build(_rows(2), allocation_seed="REQUIRED_BEFORE_USE")

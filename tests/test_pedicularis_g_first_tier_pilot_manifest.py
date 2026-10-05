import pytest

from scripts.build_pedicularis_g_first_tier_pilot_manifest import build


def _rows(n: int = 4) -> list[dict[str, str]]:
    return [
        {
            "population_id": "P_REX_TEST",
            "season_id": "S1",
            "plant_id": f"P{i:02d}",
            "exposed_flower_id": f"P{i:02d}_E",
            "fine_mesh_flower_id": f"P{i:02d}_M",
            "porous_tubing_flower_id": f"P{i:02d}_P",
        }
        for i in range(n)
    ]


def test_first_tier_manifest_allocates_three_arms_per_input_plant() -> None:
    allocations, receipt = build(_rows())

    assert receipt["n_plants"] == 4
    assert receipt["n_allocated_flowers"] == 12
    assert receipt["arms_per_plant"] == 3
    assert receipt["candidate_ids_tested"] == [
        "G_A1_FINE_MESH",
        "G_A2_POROUS_TUBING",
    ]
    assert receipt["candidate_selected"] is False
    assert receipt["sample_size_chosen_by_script"] is False

    for plant in {row["plant_id"] for row in allocations}:
        subset = [row for row in allocations if row["plant_id"] == plant]
        assert {row["pilot_arm_id"] for row in subset} == {
            "EXPOSED_SHAM",
            "G_A1_FINE_MESH",
            "G_A2_POROUS_TUBING",
        }


def test_manifest_uses_exact_canonical_field_method_codes() -> None:
    allocations, _ = build(_rows(2))
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
    allocations, _ = build(_rows(2))
    for row in allocations:
        if row["pilot_arm_id"] == "EXPOSED_SHAM":
            assert row["predator_treatment"] == "EXPOSED"
            assert row["sham_device_applied"] == "1"
            assert row["exclusion_method"] == "SHAM_SLEEVE"
        else:
            assert row["predator_treatment"] == "EXCLUDED"
            assert row["sham_device_applied"] == "0"


def test_script_does_not_invent_a_sample_size() -> None:
    _, small = build(_rows(2))
    _, large = build(_rows(7))

    assert small["n_plants"] == 2
    assert large["n_plants"] == 7
    assert small["sample_size_chosen_by_script"] is False
    assert large["sample_size_chosen_by_script"] is False


def test_flower_reuse_within_or_across_plants_fails_closed() -> None:
    rows = _rows(2)
    rows[0]["fine_mesh_flower_id"] = rows[0]["exposed_flower_id"]
    with pytest.raises(ValueError, match="reuses a flower"):
        build(rows)

    rows = _rows(2)
    rows[1]["fine_mesh_flower_id"] = rows[0]["fine_mesh_flower_id"]
    with pytest.raises(ValueError, match="unique across"):
        build(rows)


def test_context_and_plant_ids_must_be_resolved() -> None:
    rows = _rows(2)
    rows[1]["season_id"] = "S2"
    with pytest.raises(ValueError, match="one population and season"):
        build(rows)

    rows = _rows(2)
    rows[0]["plant_id"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="resolved plant_id"):
        build(rows)

import hashlib

import pytest

from scripts.prepare_pedicularis_g_v4_field_sheet import (
    V4_IDENTITY_FIELDS,
    prepare,
    verify,
)


V4_FIELDS = [
    "population_id",
    "season_id",
    "plant_id",
    "flower_id",
    "predator_treatment",
    "exclusion_method",
    "sham_device_applied",
    "anthesis_time_hours",
    "barrier_application_time_hours",
    "pollination_window_complete_before_barrier",
    "ovary_swollen_at_barrier",
    "barrier_covers_pollinator_entry",
    "pre_barrier_attack_present",
    "barrier_integrity_failure_present",
    "realized_exsertion",
    "water_depth",
    "pollen_grains",
    "pollinator_visits",
    "early_predator_attack_present",
    "ovule_count",
    "undamaged_seed_count",
    "damaged_seed_count",
    "mechanical_damage",
]


def _allocation_rows(n_plants: int = 2) -> list[dict[str, str]]:
    rows = []
    arms = [
        (
            "EXPOSED_SHAM",
            "EXPOSED",
            "SHAM_SLEEVE",
            "1",
        ),
        (
            "G_A1_FINE_MESH",
            "EXCLUDED",
            "FINE_MESH_LOWER_FRUIT_SLEEVE",
            "0",
        ),
        (
            "G_A2_POROUS_TUBING",
            "EXCLUDED",
            "POROUS_TUBING_LOWER_FRUIT_SLEEVE",
            "0",
        ),
    ]
    for i in range(n_plants):
        for j, (arm, treatment, method, sham) in enumerate(arms, start=1):
            rows.append(
                {
                    "population_id": "P_REX_TEST",
                    "season_id": "S1",
                    "plant_id": f"P{i:02d}",
                    "flower_id": f"P{i:02d}_F{j}",
                    "pilot_arm_id": arm,
                    "predator_treatment": treatment,
                    "exclusion_method": method,
                    "sham_device_applied": sham,
                    "candidate_selected": "NO",
                    "assignment_method": "SHA256_RANK_V1",
                    "field_status": "ALLOCATED_NOT_YET_MEASURED",
                }
            )
    return rows


def _receipt(n_plants: int = 2) -> dict:
    seed = "seed-a"
    return {
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "n_plants": n_plants,
        "n_allocated_flowers": n_plants * 3,
        "allocation_algorithm": "SHA256_RANK_V1",
        "assignment_randomized_within_plant": True,
        "allocation_seed": seed,
        "allocation_seed_sha256": hashlib.sha256(
            seed.encode("utf-8")
        ).hexdigest(),
        "status": "G_FIRST_TIER_PILOT_ALLOCATED_NOT_YET_MEASURED",
    }


def test_prepare_prefills_only_locked_v4_identity() -> None:
    field_rows, lock = prepare(
        _allocation_rows(),
        _receipt(),
        V4_FIELDS,
        allocation_receipt_sha256="receipt-digest",
    )

    assert len(field_rows) == 6
    assert lock["n_plants"] == 2
    assert lock["n_rows"] == 6
    assert lock["allocation_receipt_sha256"] == "receipt-digest"
    assert lock["status"] == "G_V4_FIELD_SHEET_PREPARED_NOT_YET_MEASURED"

    for row in field_rows:
        assert all(row[field] for field in V4_IDENTITY_FIELDS)
        for field in V4_FIELDS:
            if field not in V4_IDENTITY_FIELDS:
                assert row[field] == ""


def test_prepare_rejects_allocation_or_receipt_drift() -> None:
    rows = _allocation_rows()
    rows[0]["exclusion_method"] = "FINE_MESH_LOWER_FRUIT_SLEEVE"
    with pytest.raises(ValueError, match="expected"):
        prepare(rows, _receipt(), V4_FIELDS)

    bad_receipt = _receipt()
    bad_receipt["n_allocated_flowers"] = 999
    with pytest.raises(ValueError, match="receipt mismatch"):
        prepare(_allocation_rows(), bad_receipt, V4_FIELDS)


def test_verify_accepts_same_frozen_units_in_any_row_order() -> None:
    field_rows, lock = prepare(_allocation_rows(), _receipt(), V4_FIELDS)
    result = verify(list(reversed(field_rows)), lock)

    assert result["identity_lock_match"] is True
    assert result["ready_for_candidate_screen"] is False
    assert (
        result["status"]
        == "G_V4_IDENTITY_VERIFIED_PARTIAL_COLLECTION_ALLOWED"
    )


def test_verify_rejects_flower_substitution_and_method_drift() -> None:
    field_rows, lock = prepare(_allocation_rows(), _receipt(), V4_FIELDS)

    changed = [dict(row) for row in field_rows]
    changed[0]["flower_id"] = "POSTHOC_REPLACEMENT"
    with pytest.raises(ValueError, match="frozen allocation lock"):
        verify(changed, lock)

    changed = [dict(row) for row in field_rows]
    changed[0]["exclusion_method"] = "FINE_MESH_LOWER_FRUIT_SLEEVE"
    with pytest.raises(ValueError, match="exactly one frozen"):
        verify(changed, lock)


def test_verify_complete_gate_is_explicit() -> None:
    field_rows, lock = prepare(_allocation_rows(), _receipt(), V4_FIELDS)

    with pytest.raises(ValueError, match="blank outcome/timing"):
        verify(field_rows, lock, require_complete=True)

    completed = [dict(row) for row in field_rows]
    for row in completed:
        for field in V4_FIELDS:
            if field not in V4_IDENTITY_FIELDS:
                row[field] = "0"

    result = verify(completed, lock, require_complete=True)
    assert result["identity_lock_match"] is True
    assert result["all_locked_v4_cells_complete"] is True
    assert result["ready_for_candidate_screen"] is True

import hashlib
import json

import pytest

from scripts.audit_pedicularis_g_pilot_preflight import (
    PREFLIGHT_INSUFFICIENT,
    PREFLIGHT_READY,
    build,
)
from scripts.plan_pedicularis_g_hard_validity_pilot import PLAN_STATUS
from scripts.prepare_pedicularis_g_v4_field_sheet import prepare


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


def _allocation_rows(n_plants: int) -> list[dict[str, str]]:
    arms = [
        ("EXPOSED_SHAM", "EXPOSED", "SHAM_SLEEVE", "1"),
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
    rows = []
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


def _receipt(n_plants: int) -> dict:
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


def _receipt_digest(receipt: dict) -> str:
    raw = (json.dumps(receipt, sort_keys=True) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _lock(rows: list[dict[str, str]], receipt: dict) -> dict:
    _, lock = prepare(
        rows,
        receipt,
        V4_FIELDS,
        allocation_receipt_sha256=_receipt_digest(receipt),
    )
    return lock


def _plan(required_n: int) -> dict:
    return {
        "status": PLAN_STATUS,
        "population_id": "P_REX_TEST",
        "season_id": "S1",
        "current_three_arm_manifest_compatible": True,
        "first_tier_candidate_ids": [
            "G_A1_FINE_MESH",
            "G_A2_POROUS_TUBING",
        ],
        "minimum_distinct_plants_for_current_three_arm_manifest": required_n,
        "confidence_level": 0.95,
        "max_acceptable_per_plant_hard_failure_probability": 0.10,
    }


def test_preflight_ready_when_packet_matches_and_n_is_sufficient() -> None:
    rows = _allocation_rows(4)
    receipt = _receipt(4)
    result = build(
        _plan(3),
        rows,
        receipt,
        _lock(rows, receipt),
        allocation_receipt_sha256=_receipt_digest(receipt),
    )

    assert result["status"] == PREFLIGHT_READY
    assert result["observed_distinct_plants"] == 4
    assert result["required_distinct_plants"] == 3
    assert result["plant_deficit"] == 0
    assert result["v4_identity_lock_match"] is True
    assert result["same_population_and_season"] is True
    assert result["ready_to_start_locked_g_exploratory_pilot"] is True


def test_preflight_reports_exact_plant_deficit_without_relaxing_plan() -> None:
    rows = _allocation_rows(2)
    receipt = _receipt(2)
    result = build(
        _plan(5),
        rows,
        receipt,
        _lock(rows, receipt),
        allocation_receipt_sha256=_receipt_digest(receipt),
    )

    assert result["status"] == PREFLIGHT_INSUFFICIENT
    assert result["plant_deficit"] == 3
    assert result["sample_size_meets_hard_validity_plan"] is False
    assert result["ready_to_start_locked_g_exploratory_pilot"] is False


def test_preflight_rejects_context_or_lock_drift() -> None:
    rows = _allocation_rows(3)
    receipt = _receipt(3)
    lock = _lock(rows, receipt)

    plan = _plan(3)
    plan["season_id"] = "S2"
    with pytest.raises(ValueError, match="context do not match"):
        build(
            plan,
            rows,
            receipt,
            lock,
            allocation_receipt_sha256=_receipt_digest(receipt),
        )

    bad_lock = dict(lock)
    bad_lock["allocation_identity_sha256"] = "wrong"
    with pytest.raises(ValueError, match="allocation identity"):
        build(
            _plan(3),
            rows,
            receipt,
            bad_lock,
            allocation_receipt_sha256=_receipt_digest(receipt),
        )


def test_preflight_rejects_receipt_digest_or_unready_plan() -> None:
    rows = _allocation_rows(3)
    receipt = _receipt(3)
    lock = _lock(rows, receipt)

    with pytest.raises(ValueError, match="allocation receipt"):
        build(
            _plan(3),
            rows,
            receipt,
            lock,
            allocation_receipt_sha256="different",
        )

    plan = _plan(3)
    plan["status"] = "NOT_READY"
    with pytest.raises(ValueError, match="not ready"):
        build(
            plan,
            rows,
            receipt,
            lock,
            allocation_receipt_sha256=_receipt_digest(receipt),
        )


def test_preflight_rejects_unresolved_allocation_context() -> None:
    rows = _allocation_rows(3)
    receipt = _receipt(3)
    for row in rows:
        row["population_id"] = ""
    with pytest.raises(ValueError, match="population_id and season_id"):
        build(
            _plan(3),
            rows,
            receipt,
            {"status": "G_V4_FIELD_SHEET_PREPARED_NOT_YET_MEASURED"},
            allocation_receipt_sha256=_receipt_digest(receipt),
        )

    rows = _allocation_rows(3)
    rows[0]["plant_id"] = "REQUIRED_BEFORE_USE"
    with pytest.raises(ValueError, match="resolved plant_id"):
        build(
            _plan(3),
            rows,
            receipt,
            {"status": "G_V4_FIELD_SHEET_PREPARED_NOT_YET_MEASURED"},
            allocation_receipt_sha256=_receipt_digest(receipt),
        )

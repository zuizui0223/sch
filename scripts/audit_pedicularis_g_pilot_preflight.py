from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.plan_pedicularis_g_hard_validity_pilot import PLAN_STATUS
from scripts.prepare_pedicularis_g_v4_field_sheet import (
    _identity_digest,
    _read_csv,
    _sha256_bytes,
    _validate_allocation_receipt,
    _validate_allocation_rows,
)


PREFLIGHT_READY = "G_EXPLORATORY_PILOT_PREFLIGHT_READY"
PREFLIGHT_INSUFFICIENT = "G_EXPLORATORY_PILOT_PREFLIGHT_INSUFFICIENT_PLANTS"


def build(
    hard_validity_plan: dict,
    allocation_rows: list[dict[str, str]],
    allocation_receipt: dict,
    v4_lock: dict,
    *,
    allocation_receipt_sha256: str,
) -> dict:
    if hard_validity_plan.get("status") != PLAN_STATUS:
        raise ValueError("G hard-validity sample-size plan is not ready")
    if hard_validity_plan.get("current_three_arm_manifest_compatible") is not True:
        raise ValueError("hard-validity plan is not compatible with the three-arm manifest")

    population_id, season_id, n_plants = _validate_allocation_rows(
        allocation_rows
    )
    _validate_allocation_receipt(
        allocation_receipt,
        population_id=population_id,
        season_id=season_id,
        n_plants=n_plants,
        n_rows=len(allocation_rows),
    )

    plan_context = (
        hard_validity_plan.get("population_id"),
        hard_validity_plan.get("season_id"),
    )
    if plan_context != (population_id, season_id):
        raise ValueError("hard-validity plan and allocation context do not match")

    if v4_lock.get("status") != "G_V4_FIELD_SHEET_PREPARED_NOT_YET_MEASURED":
        raise ValueError("V4 identity lock is not in prepared pre-outcome state")
    if (
        v4_lock.get("population_id"),
        v4_lock.get("season_id"),
    ) != (population_id, season_id):
        raise ValueError("V4 lock and allocation context do not match")
    if v4_lock.get("n_plants") != n_plants:
        raise ValueError("V4 lock plant count does not match allocation")
    if v4_lock.get("n_rows") != len(allocation_rows):
        raise ValueError("V4 lock row count does not match allocation")

    identity_digest = _identity_digest(allocation_rows)
    if v4_lock.get("allocation_identity_sha256") != identity_digest:
        raise ValueError("V4 lock is not bound to this allocation identity")
    if v4_lock.get("allocation_receipt_sha256") != allocation_receipt_sha256:
        raise ValueError("V4 lock is not bound to this allocation receipt")
    if (
        v4_lock.get("allocation_seed_sha256")
        != allocation_receipt.get("allocation_seed_sha256")
    ):
        raise ValueError("V4 lock seed digest does not match allocation receipt")

    expected_candidates = sorted(
        ["G_A1_FINE_MESH", "G_A2_POROUS_TUBING"]
    )
    if sorted(hard_validity_plan.get("first_tier_candidate_ids", [])) != expected_candidates:
        raise ValueError("hard-validity plan first-tier candidates do not match")

    required_n = hard_validity_plan.get(
        "minimum_distinct_plants_for_current_three_arm_manifest"
    )
    if not isinstance(required_n, int) or required_n < 1:
        raise ValueError("hard-validity plan lacks a valid required plant count")

    deficit = max(0, required_n - n_plants)
    ready = deficit == 0

    return {
        "analysis": "pedicularis_g_exploratory_pilot_preflight_v1",
        "population_id": population_id,
        "season_id": season_id,
        "observed_distinct_plants": n_plants,
        "required_distinct_plants": required_n,
        "plant_deficit": deficit,
        "hard_validity_confidence_level": hard_validity_plan[
            "confidence_level"
        ],
        "max_acceptable_per_plant_hard_failure_probability": (
            hard_validity_plan[
                "max_acceptable_per_plant_hard_failure_probability"
            ]
        ),
        "allocation_algorithm": allocation_receipt["allocation_algorithm"],
        "allocation_seed_sha256": allocation_receipt[
            "allocation_seed_sha256"
        ],
        "allocation_identity_sha256": identity_digest,
        "v4_identity_lock_match": True,
        "same_population_and_season": True,
        "sample_size_meets_hard_validity_plan": ready,
        "ready_to_start_locked_g_exploratory_pilot": ready,
        "status": PREFLIGHT_READY if ready else PREFLIGHT_INSUFFICIENT,
        "next_step": (
            "start locked V4 field collection; verify the completed V4 sheet "
            "before candidate screening"
            if ready
            else f"add at least {deficit} distinct plants before field collection"
        ),
        "claim_ceiling": [
            "pre_outcome_execution_readiness_only",
            "does_not_observe_hard_validity_failures",
            "does_not_establish_predator_exclusion_effectiveness",
            "does_not_establish_selectivity",
            "does_not_select_a_candidate",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit whether the frozen P. rex G hard-validity plan, randomized "
            "allocation and V4 identity lock form one same-context field-ready packet"
        )
    )
    parser.add_argument("hard_validity_plan_json", type=Path)
    parser.add_argument("allocation_csv", type=Path)
    parser.add_argument("allocation_receipt_json", type=Path)
    parser.add_argument("v4_identity_lock_json", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    hard_plan = json.loads(
        args.hard_validity_plan_json.read_text(encoding="utf-8")
    )
    _, allocation_rows = _read_csv(args.allocation_csv)
    receipt_bytes = args.allocation_receipt_json.read_bytes()
    allocation_receipt = json.loads(receipt_bytes.decode("utf-8"))
    v4_lock = json.loads(
        args.v4_identity_lock_json.read_text(encoding="utf-8")
    )

    result = build(
        hard_plan,
        allocation_rows,
        allocation_receipt,
        v4_lock,
        allocation_receipt_sha256=_sha256_bytes(receipt_bytes),
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

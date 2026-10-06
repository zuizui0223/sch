from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.build_pedicularis_full_surface_allocation import _semantic_sha256
from scripts.build_pedicularis_p2_geometry_pilot import _validate_config


SCHEMA = "PEDICULARIS_P2_GEOMETRY_PILOT_ACCRUAL_DECISION_V1"
PRECISION_SCHEMA = "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_V1"
READY = "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_READY_FOR_BASIS"
INSUFFICIENT = "PEDICULARIS_P2_GEOMETRY_PILOT_PRECISION_INSUFFICIENT_FOR_BASIS"
STOP_READY = "STOP_GEOMETRY_PILOT_AND_MATERIALIZE_BASIS"
CONTINUE = "CONTINUE_TO_NEXT_REGISTERED_GEOMETRY_STAGE"
STOP_MAX = "STOP_MAXIMUM_GEOMETRY_PILOT_BASIS_NOT_QUALIFIED"


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _validate_precision(
    receipt: dict,
    *,
    config_sha: str,
    candidates: list[int],
) -> int:
    if receipt.get("receipt_schema") != PRECISION_SCHEMA:
        raise ValueError("geometry precision receipt schema mismatch")
    if receipt.get("status") not in {READY, INSUFFICIENT}:
        raise ValueError("unrecognized geometry precision status")
    if receipt.get("pilot_config_sha256") != config_sha:
        raise ValueError(
            "geometry precision receipt does not match frozen staged pilot config"
        )
    if [int(value) for value in receipt.get(
        "candidate_cumulative_plants", []
    )] != candidates:
        raise ValueError(
            "geometry precision receipt cumulative looks drift from frozen config"
        )
    stage_n = int(receipt.get("current_precision_look_n", -1))
    if stage_n not in candidates:
        raise ValueError(
            "geometry precision receipt is not from a registered cumulative look"
        )
    if int(receipt.get("n_plants", -1)) != stage_n:
        raise ValueError("geometry precision receipt plant count and look n differ")
    return stage_n


def build(
    config: dict,
    current_summary: dict,
    current_precision: dict,
    prior_precisions: list[dict],
) -> dict:
    frozen = _validate_config(config)
    candidates = list(frozen["candidate_cumulative_plants"])
    config_sha = _semantic_sha256(config)

    current_n = _validate_precision(
        current_precision,
        config_sha=config_sha,
        candidates=candidates,
    )
    if current_summary.get("pilot_config_sha256") != config_sha:
        raise ValueError(
            "current geometry summary does not match frozen staged pilot config"
        )
    if int(current_summary.get("current_precision_look_n", -1)) != current_n:
        raise ValueError(
            "current geometry summary and precision receipt refer to different looks"
        )
    summary_sha = _semantic_sha256(current_summary)
    if current_precision.get("geometry_summary_sha256") != summary_sha:
        raise ValueError(
            "current precision receipt is not bound to current geometry summary"
        )

    current_index = candidates.index(current_n)
    expected_prior = candidates[:current_index]
    by_n: dict[int, dict] = {}
    for receipt in prior_precisions:
        stage_n = _validate_precision(
            receipt,
            config_sha=config_sha,
            candidates=candidates,
        )
        if stage_n in by_n:
            raise ValueError("duplicate prior precision receipt for one staged look")
        by_n[stage_n] = receipt

    if sorted(by_n) != expected_prior:
        raise ValueError(
            "staged geometry decision requires every earlier registered look "
            "exactly once before evaluating the current look"
        )

    prior_status = {}
    for stage_n in expected_prior:
        receipt = by_n[stage_n]
        prior_status[str(stage_n)] = receipt["status"]
        if receipt["status"] == READY or receipt.get(
            "basis_materialization_authorized"
        ) is True:
            raise ValueError(
                "geometry pilot cannot continue after an earlier precision look passed"
            )
        if receipt["status"] != INSUFFICIENT:
            raise ValueError(
                "every earlier geometry look must have a formal insufficient-precision receipt"
            )

    current_ready = (
        current_precision["status"] == READY
        and current_precision.get("basis_materialization_authorized") is True
    )
    if current_ready:
        decision = STOP_READY
        next_n = None
        materialize = True
    elif current_n == candidates[-1]:
        decision = STOP_MAX
        next_n = None
        materialize = False
    else:
        if current_precision["status"] != INSUFFICIENT:
            raise ValueError(
                "nonpassing current geometry look lacks insufficient-precision status"
            )
        decision = CONTINUE
        next_n = candidates[current_index + 1]
        materialize = False

    return {
        "analysis": "pedicularis_p2_geometry_pilot_staged_accrual_v1",
        "receipt_schema": SCHEMA,
        "population_id": frozen["population_id"],
        "season_id": frozen["season_id"],
        "pilot_config_sha256": config_sha,
        "candidate_cumulative_plants": candidates,
        "current_precision_look_n": current_n,
        "current_geometry_summary_sha256": summary_sha,
        "current_precision_sha256": _semantic_sha256(current_precision),
        "prior_precision_status_by_n": prior_status,
        "decision": decision,
        "next_registered_precision_look_n": next_n,
        "basis_materialization_authorized": materialize,
        "additional_geometry_collection_authorized": decision == CONTINUE,
        "maximum_registered_pilot_reached": current_n == candidates[-1],
        "status": "PEDICULARIS_P2_GEOMETRY_STAGED_ACCRUAL_DECISION_READY",
        "claim_ceiling": [
            "prospective_precision_stopping_only",
            "cannot_skip_registered_precision_looks",
            "cannot_continue_after_first_precision_pass",
            "does_not_choose_new_unregistered_sample_size",
            "does_not_assign_W0_W5",
            "does_not_make_geometry_pilot_confirmatory",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Adjudicate a prospectively frozen staged P. rex geometry pilot: "
            "stop at first precision pass or proceed only to the next registered look"
        )
    )
    parser.add_argument("geometry_pilot_config_json", type=Path)
    parser.add_argument("current_geometry_summary_json", type=Path)
    parser.add_argument("current_geometry_precision_json", type=Path)
    parser.add_argument(
        "--prior-precision",
        type=Path,
        action="append",
        default=[],
        help="Earlier cumulative precision receipt; repeat once for every prior look",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        _load(args.geometry_pilot_config_json),
        _load(args.current_geometry_summary_json),
        _load(args.current_geometry_precision_json),
        [_load(path) for path in args.prior_precision],
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

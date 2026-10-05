from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORLDS = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_EMPIRICAL_OUTCOME_WORLDS_V1.csv"
)

POSITIVE_SURFACE = "MODEL_SUPPORTED_CAUSAL_COMPROMISE_CANDIDATE"
NEGATIVE_SURFACE = "COMPROMISE_CRITERIA_NOT_ALL_RECOVERED"


def _read_worlds(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("Pedicularis empirical outcome-world ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("Pedicularis empirical outcome-world ledger is empty")
    ids = [row["world_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("world_id must be unique")
    if set(ids) != {"W0", "W1", "W2", "W3", "W4", "W5"}:
        raise ValueError("outcome-world ledger must contain exactly W0-W5")
    return rows


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} is not a JSON object")
    return payload


def _validate_secondary(surface: dict, secondary: dict) -> None:
    for field in ("population_id", "season_id", "surface_data_sha256"):
        if secondary.get(field) != surface.get(field):
            raise ValueError(
                f"secondary diagnostic does not match surface receipt for {field}"
            )
    if secondary.get("surface_data_fingerprint_match") is not True:
        raise ValueError("secondary diagnostic lacks positive surface-data fingerprint match")
    if secondary.get("pollinator_favored_optimum_identified") is not False:
        raise ValueError("secondary diagnostic must not promote a pure pollinator optimum")
    if (
        secondary.get("antagonist_contribution_to_pollen_limitation_identified")
        is not False
    ):
        raise ValueError(
            "secondary diagnostic must not promote antagonist maintenance of pollen limitation"
        )


def _classify_positive(secondary: dict) -> str:
    shift = secondary.get("predator_removal_shifts_optimum_upward")
    pollen = secondary.get("higher_z_increases_pollen_receipt_in_both_G_states")
    seed = secondary.get("higher_z_increases_initial_seed_set_in_both_G_states")
    if not all(isinstance(value, bool) for value in (shift, pollen, seed)):
        raise ValueError("secondary diagnostic lacks boolean shift/pollen/seed results")

    if shift and pollen and seed:
        return "W1"
    if shift and pollen and not seed:
        return "W2"
    if shift and not pollen:
        return "W3"
    if not shift and pollen:
        return "W4"
    return "W5"


def build(
    surface_receipt: dict,
    secondary_receipt: dict | None,
    world_rows: list[dict[str, str]],
) -> dict:
    worlds = {row["world_id"]: row for row in world_rows}
    status = surface_receipt.get("status")
    if status not in {POSITIVE_SURFACE, NEGATIVE_SURFACE}:
        raise ValueError("unrecognized SCH causal-compromise surface status")

    if status == NEGATIVE_SURFACE:
        if secondary_receipt is not None:
            raise ValueError(
                "secondary antagonist diagnostic is not admissible after a negative primary surface"
            )
        world_id = "W0"
    else:
        if secondary_receipt is None:
            return {
                "analysis": "pedicularis_empirical_outcome_world_v1",
                "population_id": surface_receipt.get("population_id"),
                "season_id": surface_receipt.get("season_id"),
                "primary_surface_status": status,
                "world_id": None,
                "status": "POSITIVE_PRIMARY_SURFACE_SECONDARY_DIAGNOSTIC_PENDING",
                "next_step": (
                    "run the preregistered antagonist state-optimum/pollination-performance "
                    "diagnostic on the exact same fingerprinted surface data"
                ),
                "claim_ceiling": [
                    "primary_causal_compromise_only",
                    "no_enemy_induced_optimum_displacement_world_assigned_yet",
                ],
            }
        _validate_secondary(surface_receipt, secondary_receipt)
        world_id = _classify_positive(secondary_receipt)

    world = worlds[world_id]
    return {
        "analysis": "pedicularis_empirical_outcome_world_v1",
        "population_id": surface_receipt.get("population_id"),
        "season_id": surface_receipt.get("season_id"),
        "primary_surface_status": status,
        "world_id": world_id,
        "biological_state": world["biological_state"],
        "allowed_headline": world["allowed_headline"],
        "claim_ceiling": world["claim_ceiling"],
        "next_interpretive_step": world["next_interpretive_step"],
        "pure_pollinator_optimum_identified_by_world_map": False,
        "antagonist_maintenance_of_pollen_limitation_identified_by_world_map": False,
        "historical_adaptation_identified_by_world_map": False,
        "status": f"PEDICULARIS_EMPIRICAL_OUTCOME_{world_id}_ASSIGNED",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Assign a predeclared biological outcome world to the P. rex full-surface "
            "and downstream antagonist diagnostic results"
        )
    )
    parser.add_argument("surface_receipt_json", type=Path)
    parser.add_argument("--secondary-receipt", type=Path)
    parser.add_argument("--worlds", type=Path, default=DEFAULT_WORLDS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    surface = _load(args.surface_receipt_json)
    secondary = (
        _load(args.secondary_receipt)
        if args.secondary_receipt is not None
        else None
    )
    result = build(surface, secondary, _read_worlds(args.worlds))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

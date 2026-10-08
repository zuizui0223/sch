"""Finite-sample SCH fruit-fate bounds with zero/unknown reproductive outcomes.

Separate three biological questions:
1. How many viable mature seeds are left? This can be exactly zero even
   when the mechanism of failure (no fertilization vs full predation) is unknown.
2. How many seeds were initiated/damaged? A verified zero mature yield does
   NOT imply that predation q is known (0/0 is undefined).
3. Was viable output observed at all? A missing fruit is NOT assigned 0:
   before-dispersal ovule counts or defensible frozen caps bound [0,U].

For each frozen randomized assignment, retain all assigned flower IDs.
The results are finite-sample deterministic identification bounds, not
confidence intervals, causal G selectivity qualification or SCH P2 release.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

from scripts.build_pedicularis_p0_randomized_assignment import _semantic_sha256
from scripts.build_pedicularis_two_cohort_fruit_allocation import (
    FROZEN_FIELDS,
    RECEIPT_SCHEMA as ASSIGNMENT_SCHEMA,
    RECEIPT_STATUS as ASSIGNMENT_STATUS,
)

OUTPUT_SCHEMA = "PEDICULARIS_FRUIT_FATE_PRIMARY_SEED_COUNT_BOUNDS_V1"
STATUSES = {
    "MATURE_COUNTED", "ZERO_VIABLE_VERIFIED", "PARTIALLY_CENSORED",
    "FATE_UNOBSERVED",
}
VALID_ZERO = {
    "RECOVERED_EMPTY_PRE_DISPERSAL",
    "VERIFIED_NO_FRUIT_BEFORE_SEED_MATURITY",
    "DOCUMENTED_ALL_SEEDS_DESTROYED_PRE_DISPERSAL",
}
VALID_CAP_BASIS = {
    "MEASURED_PRE_EVENT_OVULES", "PROSPECTIVELY_FROZEN_UPPER_BOUND",
}
VALID_PARTIAL_BASIS = "DOCUMENTED_INTACT_LOWER_AND_POTENTIAL_SEED_UPPER"

REQUIRED_FIELDS = set(FROZEN_FIELDS) | {
    "fate_status", "intact_seeds", "damaged_seeds", "seed_stage_proof",
    "viable_lower", "viable_upper", "seed_potential_upper",
    "seed_potential_upper_basis", "zero_fate_proof",
    "partial_interval_proof",
}


def _integer(value: object, label: str, *, required: bool) -> int | None:
    if value is None or str(value).strip() == "":
        if required:
            raise ValueError(f"{label}: missing required seed count")
        return None
    raw = str(value).strip()
    if not raw.isascii() or not raw.isdecimal():
        raise ValueError(f"{label}: must be a nonnegative integer count")
    return int(raw)


def read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        rd = csv.DictReader(f)
        if not rd.fieldnames or not REQUIRED_FIELDS.issubset(rd.fieldnames):
            raise ValueError("fruit fate CSV missing source or fate columns")
        rows = [
            {k: (v or "").strip() for k, v in row.items()}
            for row in rd
        ]
    if not rows:
        raise ValueError("fruit fate CSV has no source flowers")
    return rows


def _interpret(row: dict[str, str]) -> dict:
    status = row["fate_status"]
    if status not in STATUSES:
        raise ValueError(f"unrecognized fruit fate status: {status}")
    cap = _integer(row["seed_potential_upper"], "seed_potential_upper", required=True)
    if cap < 1 or row["seed_potential_upper_basis"] not in VALID_CAP_BASIS:
        raise ValueError("seed potential upper bound needs positive prospective provenance")
    intact = _integer(row["intact_seeds"], "intact_seeds", required=False)
    damaged = _integer(row["damaged_seeds"], "damaged_seeds", required=False)
    low = _integer(row["viable_lower"], "viable_lower", required=False)
    high = _integer(row["viable_upper"], "viable_upper", required=False)
    proof = row["zero_fate_proof"]
    partial = row["partial_interval_proof"]
    stage_proof = row["seed_stage_proof"]
    if status == "MATURE_COUNTED":
        if intact is None or intact > cap:
            raise ValueError("counted mature fruit needs integer intact<=potential")
        if low is not None or high is not None or proof or partial:
            raise ValueError("counted fruit cannot also declare zero/interval censoring")
        if damaged is not None and intact + damaged > cap:
            raise ValueError("counted damaged+intact cannot exceed potential seed cap")
        if stage_proof not in ("", "COMPLETE_COUNTED_SEED_FATES"):
            raise ValueError("unknown stage fate proof")
        if stage_proof == "COMPLETE_COUNTED_SEED_FATES" and damaged is None:
            raise ValueError("complete stage fate needs damaged-seed count")
        stage_known = (
            stage_proof == "COMPLETE_COUNTED_SEED_FATES"
            and damaged is not None
            and intact + damaged > 0
        )
        bounds = (intact, intact)
    elif status == "ZERO_VIABLE_VERIFIED":
        if intact not in (None, 0) or damaged is not None or low is not None or high is not None:
            raise ValueError("verified zero has no inferred initiation/predation counts")
        if proof not in VALID_ZERO or partial or stage_proof:
            raise ValueError("verified zero requires pre-dispersal outcome proof")
        bounds = (0, 0)
        stage_known = False
    elif status == "PARTIALLY_CENSORED":
        if (intact is not None or damaged is not None or proof or stage_proof
            or low is None or high is None or not (0 <= low <= high <= cap)
            or partial != VALID_PARTIAL_BASIS):
            raise ValueError("partial censoring needs independently documented bounds")
        bounds = (low, high)
        stage_known = False
    else:  # allocated flower, reproductive output not observed
        if any((v is not None for v in (intact, damaged, low, high))) or proof or partial or stage_proof:
            raise ValueError("unobserved fate cannot be recoded as zero or counted")
        bounds = (0, cap)
        stage_known = False
    return {
        "flower_id": row["flower_id"],
        "plant_id": row["plant_id"],
        "assigned_z_rank": int(row["assigned_z_rank"]),
        "predator_treatment": row["predator_treatment"],
        "fate_status": status,
        "seed_fitness_lower": bounds[0],
        "seed_fitness_upper": bounds[1],
        "predation_q_identified_from_stage_counts": stage_known,
        "verified_zero_seed_yield": status == "ZERO_VIABLE_VERIFIED",
        "unknown_viable_output": status in {"PARTIALLY_CENSORED", "FATE_UNOBSERVED"},
    }


def _as_stat(x: Fraction) -> dict:
    return {"exact": str(x), "value": float(x)}


def _sign(lower: Fraction, upper: Fraction) -> str:
    if lower > 0:
        return "POSITIVE_IN_EVERY_FATE_COMPLETION"
    if upper < 0:
        return "NEGATIVE_IN_EVERY_FATE_COMPLETION"
    return "SIGN_UNRESOLVED_UNDER_FATE_CENSORING"


def build(rows: list[dict[str, str]], allocation_receipt: dict) -> dict:
    if (
        allocation_receipt.get("receipt_schema") != ASSIGNMENT_SCHEMA
        or allocation_receipt.get("status") != ASSIGNMENT_STATUS
        or allocation_receipt.get("cohort_role") != "TWO_COHORT_FRUIT"
        or allocation_receipt.get("pollination_treatment") != "NATURAL"
    ):
        raise ValueError("requires separate frozen nonconfirmatory fruit allocation receipt")
    if not rows or any(not REQUIRED_FIELDS.issubset(row) for row in rows):
        raise ValueError("fruit outcomes require every frozen source and fate field")
    ids = [row["flower_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate allocated flower ID in fruit fate observations")
    frozen = sorted(
        [{key: row[key] for key in FROZEN_FIELDS} for row in rows],
        key=lambda r: (r["plant_id"], r["flower_id"]),
    )
    if (
        frozen != allocation_receipt.get("expected_frozen_rows")
        or _semantic_sha256(frozen) != allocation_receipt.get("allocation_identity_sha256")
        or len(rows) != allocation_receipt.get("n_allocated_flowers")
    ):
        raise ValueError("fruit fate audit must retain exact allocated z/G/flower rows")

    population = allocation_receipt.get("population_id")
    season = allocation_receipt.get("season_id")
    if not isinstance(population, str) or not population or not isinstance(season, str) or not season:
        raise ValueError("allocation population and season missing")
    if any((r["population_id"],r["season_id"])!=(population,season) for r in rows):
        raise ValueError("source population/season changed")
    ranks = list(range(allocation_receipt.get("n_z_levels", 0)))
    if len(ranks) < 5:
        raise ValueError("source z grid requires >=5 assigned levels")
    if any(
        row["assigned_z_rank"] not in {str(rank) for rank in ranks}
        or row["predator_treatment"] not in {"EXPOSED","EXCLUDED"}
        for row in rows
    ):
        raise ValueError("unregistered z-rank or predator treatment")
    source_by_plant = defaultdict(set)
    for row in rows:
        unit = (int(row["assigned_z_rank"]), row["predator_treatment"])
        if unit in source_by_plant[row["plant_id"]]:
            raise ValueError("fate audit expected one z×G flower per plant")
        source_by_plant[row["plant_id"]].add(unit)
    required_cells = {(rank,g) for rank in ranks for g in ("EXCLUDED","EXPOSED")}
    if any(cells != required_cells for cells in source_by_plant.values()):
        raise ValueError("fate audit cannot ignore any allocated plant-by-z×G cell")

    interpreted = [_interpret(row) for row in rows]
    cells: dict[tuple[int,str],list[dict]] = defaultdict(list)
    for x in interpreted:
        cells[x["assigned_z_rank"],x["predator_treatment"]].append(x)
    means: dict[str,dict[int,tuple[Fraction,Fraction]]] = {
        "EXCLUDED": {}, "EXPOSED": {}
    }
    per_cell: dict[str,dict[str,dict]] = {"EXCLUDED": {}, "EXPOSED": {}}
    for g in ("EXCLUDED","EXPOSED"):
        for z in ranks:
            data = cells[z,g]
            n = len(data)
            lo = Fraction(sum(x["seed_fitness_lower"] for x in data),n)
            hi = Fraction(sum(x["seed_fitness_upper"] for x in data),n)
            means[g][z] = lo,hi
            per_cell[g][str(z)] = {
                "n_all_allocated_flowers": n,
                "mean_viable_seeds_per_flower_bounds": [_as_stat(lo),_as_stat(hi)],
                "n_exact_mature_fitness": sum(
                    x["seed_fitness_lower"]==x["seed_fitness_upper"] for x in data
                ),
                "n_verified_zero_mature_yield": sum(x["verified_zero_seed_yield"] for x in data),
                "n_stage_predation_q_known": sum(x["predation_q_identified_from_stage_counts"] for x in data),
                "n_stage_predation_q_unknown": sum(not x["predation_q_identified_from_stage_counts"] for x in data),
                "n_censored_or_unobserved_viable_yield": sum(x["unknown_viable_output"] for x in data),
            }
    contrasts: dict[str,dict] = {}
    optima: dict[str,dict] = {}
    for g in ("EXCLUDED","EXPOSED"):
        high,low = means[g][ranks[-1]],means[g][ranks[0]]
        d0,d1 = high[0]-low[1],high[1]-low[0]
        contrasts[g] = {
            "high_minus_low_viable_seed_count_per_flower_bounds": [
                _as_stat(d0), _as_stat(d1)
            ],
            "direction": _sign(d0,d1),
        }
        benchmark = max(low_bound for low_bound,_ in means[g].values())
        possible = [
            z for z,(lower,upper) in means[g].items() if upper>=benchmark
        ]
        strict_unique = [
            z for z,(lower,upper) in means[g].items()
            if all(lower>other_upper for k,(_,other_upper) in means[g].items() if k!=z)
        ]
        optima[g] = {
            "possible_discrete_optimum_ranks": possible,
            "guaranteed_unique_discrete_optimum_rank": (
                strict_unique[0] if len(strict_unique)==1 else None
            ),
            "rank_optimum_claim_only_conditional_on_independently_feasible_cell_bounds": True,
        }
    pred_effect:dict[str,dict] = {}
    for z in ranks:
        excl,expo = means["EXCLUDED"][z],means["EXPOSED"][z]
        d0,d1 = excl[0]-expo[1],excl[1]-expo[0]
        pred_effect[str(z)] = {
            "excluded_minus_exposed_viable_seed_count_bounds": [
                _as_stat(d0),_as_stat(d1)
            ],
            "direction": _sign(d0,d1),
        }
    excluded_possible = optima["EXCLUDED"]["possible_discrete_optimum_ranks"]
    exposed_possible = optima["EXPOSED"]["possible_discrete_optimum_ranks"]
    optimum_rank_shift_outer = [
        min(excluded_possible)-max(exposed_possible),
        max(excluded_possible)-min(exposed_possible),
    ]
    return {
        "receipt_schema": OUTPUT_SCHEMA,
        "analysis": "pedicularis_fruit_fate_conditional_fitness_selection_bounds",
        "population_id": population,
        "season_id": season,
        "allocation_receipt_sha256": _semantic_sha256(allocation_receipt),
        "source_outcome_rows_sha256": _semantic_sha256(sorted(rows,key=lambda r:(r["plant_id"],r["flower_id"]))),
        "n_all_allocated_flowers": len(rows),
        "n_independent_plant_blocks": len(source_by_plant),
        "fate_status_counts": {
            status: sum(x["fate_status"]==status for x in interpreted)
            for status in sorted(STATUSES)
        },
        "mean_fitness_by_predator_treatment_and_z": per_cell,
        "extreme_z_fitness_selection_contrasts": contrasts,
        "predator_exclusion_fitness_differences_by_z": pred_effect,
        "predator_state_possible_optimum_ranks": optima,
        "excluded_minus_exposed_optimum_rank_shift_outer_bound": optimum_rank_shift_outer,
        "optimum_shift_guaranteed_positive_given_bounds": optimum_rank_shift_outer[0]>0,
        "status": "NON_GATING_FINITE_ASSIGNED_FRUIT_FATE_BOUNDS",
        "claim_ceiling": [
            "source_allocation_hash_checks_identity_not_authenticity_of_field_randomization",
            "separate_two_cohort_exploratory_lane_not_primary_W1_W2",
            "verified_zero_viable_seed_fitness_does_not_identify_cause_or_predation_q",
            "missing_frustation_not_imputed_as_0_and_full_seed_count_potential_cap_required",
            "ovule_cap_basis_provenance_user_declared_not_independently_verified",
            "finite_allocated_sample_identification_not_superpopulation_confidence_interval",
            "individual_flower_outcomes_within_plant_may_interfere",
            "independent_latent_cell_completion_assumption_for_joint_sharpness",
            "mean_viable_seed_count_per_flower_not_fraction",
            "no_causal_pollinator_specific_optima_or_SCH_architecture_value",
        ],
    }


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("complete_allocated_fruit_fate_csv", type=Path)
    p.add_argument("frozen_fruit_allocation_json", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    out = build(
        read(args.complete_allocated_fruit_fate_csv),
        json.loads(args.frozen_fruit_allocation_json.read_text(encoding="utf-8")),
    )
    payload = json.dumps(out,sort_keys=True,indent=2)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload,encoding="utf-8")
    else:
        print(payload,end="")


if __name__ == "__main__":
    main()

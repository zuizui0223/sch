from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PRIORS = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_P2_HISTORICAL_CONTEXT_PRIORS_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("historical context prior ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("historical context prior ledger is empty")
    return rows


def build(rows: list[dict[str, str]]) -> dict:
    codes = [row["historical_population_code"] for row in rows]
    if len(codes) != len(set(codes)):
        raise ValueError("historical_population_code must be unique")
    if set(codes) != {f"POP{i}" for i in range(1, 13)}:
        raise ValueError("historical context ledger must contain exactly POP1-POP12")

    linked = {
        row["historical_population_code"]
        for row in rows
        if row["individual_linkage_retained"] == "YES"
    }
    if linked != {"POP1", "POP3", "POP5", "POP8", "POP9", "POP10", "POP11"}:
        raise ValueError("historical individual-linkage set changed unexpectedly")

    exact = {}
    for row in rows:
        raw = row["exact_main_text_seed_predation_percent"]
        rank = row["exact_pressure_rank_among_four"]
        if raw:
            if not rank:
                raise ValueError("exact pressure rows require exact-pressure rank")
            exact[row["historical_population_code"]] = {
                "seed_predation_percent": float(raw),
                "rank": int(rank),
                "linked": row["individual_linkage_retained"] == "YES",
                "history_class": row["history_class"],
            }
        elif rank:
            raise ValueError("pressure rank cannot exist without exact pressure")

    expected = {
        "POP5": (27.42, 1),
        "POP12": (18.50, 2),
        "POP3": (1.36, 3),
        "POP11": (0.80, 4),
    }
    for code, (pressure, rank) in expected.items():
        observed = exact.get(code)
        if observed is None:
            raise ValueError(f"missing exact main-text pressure for {code}")
        if observed["seed_predation_percent"] != pressure:
            raise ValueError(f"historical pressure for {code} changed unexpectedly")
        if observed["rank"] != rank:
            raise ValueError(f"historical pressure rank for {code} changed unexpectedly")

    if exact["POP5"]["history_class"] != "HIGHEST_EXACT_PRESSURE_LINKED":
        raise ValueError("POP5 must remain the highest exact linked pressure prior")
    if exact["POP12"]["linked"]:
        raise ValueError("POP12 historical individual linkage must remain lost")

    return {
        "analysis": "pedicularis_p2_historical_context_prior_audit_v1",
        "n_historical_populations": len(rows),
        "linked_historical_populations": sorted(linked),
        "n_linked_historical_populations": len(linked),
        "exact_main_text_pressure_cases": exact,
        "highest_exact_pressure_linked_population": "POP5",
        "highest_exact_pressure_linked_percent": 27.42,
        "lowest_exact_pressure_linked_populations": ["POP11", "POP3"],
        "historical_prior_can_select_p2_context_automatically": False,
        "current_season_validation_required": True,
        "status": "HISTORICAL_CONTEXT_PRIORS_READY_NOT_CURRENT_SEASON_QUALIFICATION",
        "claim_ceiling": [
            "historical_antagonist_pressure_is_recruitment_prior_only",
            "do_not_infer_current_season_predation_from_2016_values",
            "do_not_treat_four_exact_pressures_as_population_prevalence",
            "do_not_call_POP5_current_conflict_active_without_same_season_P1_G_validation",
            "population_12_pressure_is_not_linked_individual_geometry",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--priors", type=Path, default=DEFAULT_PRIORS)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(_read(args.priors))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

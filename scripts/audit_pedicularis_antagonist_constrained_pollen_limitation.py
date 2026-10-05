from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_ANTAGONIST_CONSTRAINED_POLLEN_LIMITATION_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("antagonist-constrained pollen-limitation ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("antagonist-constrained pollen-limitation ledger is empty")
    return rows


def build(rows: list[dict[str, str]]) -> dict:
    ids = [row["criterion_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("criterion_id must be unique")

    criteria = {
        row["criterion_id"]: row
        for row in rows
        if row["criterion_id"].startswith("AIPL_C")
    }
    expected = {"AIPL_C1", "AIPL_C2", "AIPL_C3", "AIPL_C4"}
    if set(criteria) != expected:
        raise ValueError("AIPL criterion map must contain exactly C1-C4")

    if criteria["AIPL_C1"]["status"] != "SUPPORTED_OBSERVATIONAL":
        raise ValueError("AIPL C1 must remain observationally supported")
    if criteria["AIPL_C2"]["status"] != "UNRESOLVED":
        raise ValueError("AIPL C2 must remain unresolved")
    if criteria["AIPL_C3"]["status"] != "COMPONENTS_PRESENT_CAUSAL_CHAIN_UNRESOLVED":
        raise ValueError("AIPL C3 must remain partial/unresolved")
    if criteria["AIPL_C4"]["status"] != "UNRESOLVED":
        raise ValueError("AIPL C4 must remain unresolved")

    if any(row["causal_support"] == "YES" for row in rows):
        raise ValueError(
            "current P. rex success-risk evidence must not be promoted to causal support"
        )

    coupling = next(
        (
            row
            for row in rows
            if row["criterion_id"] == "PRX_COUPLING_1"
        ),
        None,
    )
    if coupling is None:
        raise ValueError("P. rex success-risk coupling row is required")
    if "pollen*" not in coupling["focal_evidence"]:
        raise ValueError("coupling row must retain the positive pollen term")
    if "AICc -156.11" not in coupling["focal_evidence"]:
        raise ValueError("coupling row must retain the source best-model AICc")

    hypothesis = next(
        (
            row
            for row in rows
            if row["criterion_id"] == "PRX_COUPLING_2"
        ),
        None,
    )
    if hypothesis is None or hypothesis["status"] != "SOURCE_HYPOTHESIS_UNTESTED":
        raise ValueError("predictive-cue mechanism must remain an untested source hypothesis")

    status_counts = Counter(row["status"] for row in rows)

    return {
        "analysis": "pedicularis_antagonist_constrained_pollen_limitation_v1",
        "n_rows": len(rows),
        "status_counts": dict(sorted(status_counts.items())),
        "aipl_criteria": {
            key: criteria[key]["status"]
            for key in sorted(criteria)
        },
        "n_aipl_criteria_fully_supported": 1,
        "aipl_full_mechanism_supported": False,
        "p_rex_pollen_limited_state_recovered": True,
        "p_rex_success_risk_coupling_recovered": True,
        "success_risk_coupling_causal": False,
        "predictive_cue_identity_resolved": False,
        "focal_hypothesis": (
            "seed predators constrain floral exsertion below the pollinator-favored "
            "state, thereby contributing to maintenance of pollen limitation"
        ),
        "causal_surface_predictions": [
            "predator removal shifts the reproductive optimum toward greater exsertion",
            "the predator-removed higher-exsertion state increases pollen receipt and/or initial seed set",
            "with predators present, the combined optimum lies below the pollinator-favored optimum",
        ],
        "falsifiers": [
            "predator removal does not shift the exsertion optimum upward",
            "greater exsertion under predator removal does not improve pollen receipt or initial seed set",
            "pollinator and antagonist response surfaces do not support opposing z effects",
        ],
        "status": "P_REX_AIPL_PARTIAL_MATCH_CAUSAL_TEST_REQUIRED",
        "claim_ceiling": [
            "criterion_1_observationally_supported",
            "pollen_limitation_and_conflicting_selection_cooccur",
            "pollen_predation_coupling_is_observational",
            "do_not_claim_pollen_is_the_predator_cue",
            "do_not_claim_antagonists_caused_pollen_limitation",
            "do_not_claim_adaptive_pollen_limitation_without_causal_surface_and_optimum_evidence",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit how far focal P. rex evidence satisfies the four criteria "
            "for antagonist-induced adaptive pollen limitation"
        )
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(_read(args.ledger))
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

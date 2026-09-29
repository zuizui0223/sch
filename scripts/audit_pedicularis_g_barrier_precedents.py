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
    / "PEDICULARIS_G_BARRIER_PRECEDENTS_V1.csv"
)

EXPECTED_AXES = {
    "WITHIN_GENUS_POSTPOLLINATION_ATTACK_TIMING",
    "POSTPOLLINATION_FRUIT_BARRIER_COMPATIBILITY",
    "POSTPOLLINATION_FRUIT_LOCAL_BARRIER_EFFICACY",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("G barrier precedent ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("G barrier precedent ledger is empty")
    return rows


def build(path: Path = DEFAULT_LEDGER) -> dict:
    rows = _read(path)

    ids = [row["precedent_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("G barrier precedent_id must be unique")

    axes = [row["evidence_axis"] for row in rows]
    if set(axes) != EXPECTED_AXES:
        raise ValueError(
            "G barrier evidence-axis coverage mismatch: "
            f"missing={sorted(EXPECTED_AXES - set(axes))}, "
            f"extra={sorted(set(axes) - EXPECTED_AXES)}"
        )
    if len(rows) != len(EXPECTED_AXES):
        raise ValueError(
            "G barrier V1 expects exactly one bounded precedent per evidence axis"
        )

    if {row["direct_P_rex_validation"] for row in rows} != {"NO"}:
        raise ValueError(
            "external G barrier precedents must not be labelled as focal P. rex validation"
        )
    if {row["direct_F0_freeze_eligible"] for row in rows} != {"NO"}:
        raise ValueError(
            "external G barrier precedents must not directly freeze F0"
        )

    by_axis = {row["evidence_axis"]: row for row in rows}
    timing = by_axis["WITHIN_GENUS_POSTPOLLINATION_ATTACK_TIMING"]
    compatibility = by_axis[
        "POSTPOLLINATION_FRUIT_BARRIER_COMPATIBILITY"
    ]
    efficacy = by_axis[
        "POSTPOLLINATION_FRUIT_LOCAL_BARRIER_EFFICACY"
    ]

    if timing["species"] != "Pedicularis furbishiae":
        raise ValueError("within-genus timing precedent must remain Pedicularis")
    if "removed before flowers opened" not in timing[
        "barrier_or_exclosure"
    ].lower():
        raise ValueError(
            "timing precedent must not be misread as a retained postpollination barrier"
        )

    if "no contemporaneous unshielded" not in compatibility["notes"].lower():
        raise ValueError(
            "Cypripedium compatibility precedent must preserve the missing same-year efficacy control"
        )

    if (
        "context-dependent and imperfect" not in efficacy["notes"].lower()
        or "before they were large enough to bag" not in efficacy["notes"].lower()
    ):
        raise ValueError(
            "Chamaecrista efficacy precedent must preserve timing and pore-size failure modes"
        )

    axis_counts = Counter(axes)

    return {
        "analysis": "pedicularis_g_barrier_precedent_audit_v1",
        "n_precedents": len(rows),
        "n_species": len({row["species"] for row in rows}),
        "evidence_axis_counts": dict(sorted(axis_counts.items())),
        "within_genus_postpollination_attack_timing_recovered": True,
        "external_postpollination_fruit_barrier_compatibility_recovered": True,
        "external_fruit_local_barrier_efficacy_class_recovered": True,
        "focal_P_rex_barrier_effectiveness_recovered": False,
        "focal_P_rex_barrier_selectivity_recovered": False,
        "focal_P_rex_timing_bounds_recovered": False,
        "cypripedium_same_year_unshielded_control_available": False,
        "chamaecrista_failure_modes": [
            "attack_before_fruits_large_enough_to_bag",
            "sucking_attack_through_mesh_holes",
            "efficacy_context_dependent",
        ],
        "current_G_method_bottleneck": (
            "FOCAL_P_REX_POSTPOLLINATION_BARRIER_EFFECTIVENESS_SELECTIVITY_AND_TIMING_QUALIFICATION"
        ),
        "status": (
            "G_BARRIER_CLASS_TIMING_COMPATIBILITY_EFFICACY_PRECEDENTS_RECOVERED_"
            "FOCAL_VALIDATION_STILL_REQUIRED"
        ),
        "claim_ceiling": [
            "timing_precedent_is_not_barrier_effectiveness",
            "fruit_development_compatibility_is_not_predator_reduction_effect",
            "external_barrier_efficacy_is_not_P_rex_efficacy",
            "mesh_pore_size_and_application_timing_are_candidate_specific",
            "no_precedent_directly_freezes_F0",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit timing, compatibility and efficacy precedents for the "
            "Pedicularis rex independent-G physical barrier"
        )
    )
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(args.ledger)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = (
    ROOT
    / "empirical"
    / "architecture"
    / "PEDICULARIS_G_BARRIER_MATERIAL_PRECEDENTS_V1.csv"
)


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("G barrier-material precedent ledger has no header")
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("G barrier-material precedent ledger is empty")
    return rows


def build(path: Path = DEFAULT_LEDGER) -> dict:
    rows = _read(path)

    ids = [row["precedent_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("barrier-material precedent_id must be unique")

    if {row["direct_P_rex_validation"] for row in rows} != {"NO"}:
        raise ValueError(
            "external/timing barrier precedents must not be labelled as direct P. rex validation"
        )
    if {row["direct_F0_freeze_eligible"] for row in rows} != {"NO"}:
        raise ValueError(
            "barrier-material precedents must not directly freeze F0"
        )

    dialysis = [
        row for row in rows
        if "dialysis tubing" in row["barrier_material"].lower()
    ]
    mesh = [
        row for row in rows
        if "mesh" in row["barrier_material"].lower()
    ]
    pedicularis = [
        row for row in rows
        if row["system"].startswith("Pedicularis ")
    ]

    if len(dialysis) != 1:
        raise ValueError("exactly one dialysis-tubing precedent is expected")
    if not any(
        "sucking insects could attack through mesh holes"
        in row["failure_mode_or_limit"]
        for row in mesh
    ):
        raise ValueError(
            "mesh failure-mode evidence must preserve aperture leakage"
        )
    if not any(
        "wet bag weight" in row["failure_mode_or_limit"]
        for row in mesh
    ):
        raise ValueError(
            "mesh failure-mode evidence must preserve mechanical-load risk"
        )

    return {
        "analysis": "pedicularis_g_barrier_material_precedent_audit_v1",
        "n_barrier_precedents": len(rows),
        "n_dialysis_tubing_precedents": len(dialysis),
        "n_mesh_related_precedents": len(mesh),
        "n_within_genus_timing_precedents": len(pedicularis),
        "porous_tubing_material_class_feasibility_recovered": True,
        "mesh_aperture_failure_mode_recovered": True,
        "mesh_mechanical_load_failure_mode_recovered": True,
        "pedicularis_postpollination_timing_recovered": True,
        "focal_p_rex_barrier_effectiveness_recovered": False,
        "focal_p_rex_barrier_selectivity_recovered": False,
        "pilot_material_classes": [
            "SOFT_POROUS_OR_DIALYSIS_LIKE_TUBING",
            "FINE_INERT_MESH",
        ],
        "required_focal_checks": [
            "predator_attack_reduction",
            "seed_predation_reduction",
            "final_intact_seed_gain",
            "initial_seed_set_stability",
            "pollen_receipt_stability",
            "pollinator_visitation_stability",
            "realized_exsertion_stability",
            "water_state_stability",
            "mechanical_damage_stability",
        ],
        "status": (
            "G_BARRIER_MATERIAL_PRECEDENTS_RECOVERED_"
            "P_REX_EFFECTIVENESS_SELECTIVITY_STILL_REQUIRED"
        ),
        "claim_ceiling": [
            "external_material_class_feasibility_only",
            "mesh_failure_modes_are_design_constraints_not_P_rex_effects",
            "within_genus_timing_is_not_material_effectiveness",
            "no_material_is_predeclared_successful_in_P_rex",
            "no_barrier_precedent_directly_freezes_F0",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit physical seed-predator barrier material precedents while "
            "keeping external feasibility separate from focal P. rex validation"
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

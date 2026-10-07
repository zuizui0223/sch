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
    / "PEDICULARIS_W1_W2_POWER_BASIS_LEDGER_V1.csv"
)

REQUIRED_COLUMNS = {
    "field_group",
    "config_path",
    "basis_type",
    "current_source",
    "current_status",
    "direct_registered_n_eligible",
    "blocking_for_registered_n",
    "notes",
}

READY_STATUSES = {
    "DIRECT_SAME_CONTEXT_READY",
    "REGISTERED_THRESHOLD_READY",
    "PROSPECTIVE_DESIGN_FROZEN",
    "ROBUST_ENVELOPE_READY",
}


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("W1/W2 power basis ledger has no header")
        missing = sorted(REQUIRED_COLUMNS - set(reader.fieldnames))
        if missing:
            raise ValueError(
                "W1/W2 power basis ledger lacks columns: "
                + ", ".join(missing)
            )
        rows = [
            {key: (value or "").strip() for key, value in row.items()}
            for row in reader
        ]
    if not rows:
        raise ValueError("W1/W2 power basis ledger is empty")
    return rows


def build(rows: list[dict[str, str]]) -> dict:
    paths = [row["config_path"] for row in rows]
    if any(not value for value in paths):
        raise ValueError("every power-basis row needs config_path")
    if len(paths) != len(set(paths)):
        raise ValueError("config_path must be unique in power-basis ledger")

    for row in rows:
        if row["direct_registered_n_eligible"] not in {"YES", "NO"}:
            raise ValueError(
                f"{row['config_path']}.direct_registered_n_eligible must be YES/NO"
            )
        if row["blocking_for_registered_n"] not in {"YES", "NO"}:
            raise ValueError(
                f"{row['config_path']}.blocking_for_registered_n must be YES/NO"
            )

    blockers = [
        row
        for row in rows
        if row["blocking_for_registered_n"] == "YES"
        and row["current_status"] not in READY_STATUSES
    ]
    direct_ready = [
        row
        for row in rows
        if row["current_status"] in READY_STATUSES
        and row["direct_registered_n_eligible"] == "YES"
    ]

    groups = Counter(row["field_group"] for row in rows)
    statuses = Counter(row["current_status"] for row in rows)

    geometry_groups = {
        "FITNESS_GEOMETRY",
        "POLLEN_GEOMETRY",
        "INITIAL_SEED_GEOMETRY",
    }
    geometry_rows = [
        row for row in rows if row["field_group"] in geometry_groups
    ]
    geometry_ready = [
        row for row in geometry_rows if row["current_status"] in READY_STATUSES
    ]

    external_only = [
        row
        for row in rows
        if (
            "EXTERNAL" in row["current_status"]
            or "DIRECTION_ONLY" in row["current_status"]
        )
    ]

    registered_ready = len(blockers) == 0

    if registered_ready:
        interpretation = (
            "All rows marked blocking_for_registered_n now have an admissible "
            "ready basis. The generating-input basis can support a registered "
            "single-scenario W1/W2 power calculation, subject to the separate "
            "exact geometry-config and P0/F0-config bindings."
        )
        claim_ceiling = [
            "basis_audit_only",
            "basis_ready_does_not_itself_choose_or_register_n",
            "exact_geometry_and_P0_F0_config_bindings_still_required",
            "power_targets_and_candidate_design_remain_prospective_inputs",
        ]
    else:
        interpretation = (
            "The production W1/W2 simulator is available, but a registered "
            "sample-size recommendation is not yet identified because one or "
            "more generating inputs still lack an admissible basis."
        )
        claim_ceiling = [
            "basis_audit_only",
            "no_registered_W1_W2_n_yet",
            "external_priors_are_sensitivity_context_not_direct_surface_truth",
            "do_not_use_single_arbitrary_scenario_for_field_allocation",
        ]

    return {
        "analysis": "pedicularis_w1_w2_power_basis_audit_v1",
        "n_basis_rows": len(rows),
        "field_group_counts": dict(sorted(groups.items())),
        "current_status_counts": dict(sorted(statuses.items())),
        "n_blocking_rows": len(blockers),
        "blocking_config_paths": sorted(
            row["config_path"] for row in blockers
        ),
        "n_direct_ready_rows": len(direct_ready),
        "n_geometry_rows": len(geometry_rows),
        "n_geometry_rows_ready_for_registered_n": len(geometry_ready),
        "n_external_or_direction_only_rows": len(external_only),
        "registered_single_scenario_n_basis_ready": registered_ready,
        "registered_power_status": (
            "PEDICULARIS_W1_W2_POWER_BASIS_READY_FOR_REGISTERED_N"
            if registered_ready
            else "PEDICULARIS_W1_W2_POWER_BASIS_BLOCKED"
        ),
        "admissible_resolution_routes": [
            {
                "route": "SEPARATE_NONCONFIRMATORY_P2_GEOMETRY_PILOT",
                "role": (
                    "estimate same-context randomized z x P x G geometry and "
                    "variance on flowers/plants excluded from confirmatory inference"
                ),
            },
            {
                "route": "PROSPECTIVELY_FROZEN_ROBUST_MULTI_SCENARIO_ENVELOPE",
                "role": (
                    "declare a biologically justified scenario set before P2 "
                    "outcomes and require the chosen n to meet power targets in "
                    "every scenario"
                ),
            },
        ],
        "inadmissible_routes": [
            "single_convenient_generating_scenario_without_basis",
            "use_confirmatory_P2_outcomes_to_choose_generating_geometry",
            "promote_observational_exsertion_selection_to_randomized_state_surface",
            "treat_pooled_pollen_SD_as_between_plant_plus_residual_variance_decomposition",
            "treat_population_initial_seed_range_as_randomized_z_slope_or_residual_SD",
        ],
        "interpretation": interpretation,
        "claim_ceiling": claim_ceiling,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Audit whether the P. rex W1/W2 production-power generating inputs "
            "have an admissible prospective evidence basis"
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

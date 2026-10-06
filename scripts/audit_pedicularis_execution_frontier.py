from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from scripts.pedicularis_config_freeze import (
    FREEZE_STATUS,
    inspect_prospective_freeze,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODULE_LEDGER = (
    ROOT / "empirical" / "architecture" / "PEDICULARIS_CALIBRATION_MODULE_LEDGER_V1.csv"
)
DEFAULT_CONFIGS = {
    "P0": ROOT / "empirical" / "architecture" / "PEDICULARIS_STAGE_P0_CONFIG_TEMPLATE_V1.json",
    "P1": ROOT / "empirical" / "architecture" / "PEDICULARIS_POLLINATION_WEIGHT_CONFIG_TEMPLATE_V1.json",
    "G": ROOT / "empirical" / "architecture" / "PEDICULARIS_PREDATOR_METHOD_CONFIG_V4.json",
}


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"config {path} is not a JSON object")
    return payload


def _module_counts(path: Path) -> dict[str, int]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return dict(sorted(Counter(row["calibration_module"] for row in rows).items()))


def build(
    config_paths: dict[str, Path],
    module_ledger_path: Path = DEFAULT_MODULE_LEDGER,
) -> dict:
    lane_receipts = {
        lane: inspect_prospective_freeze(_load(config_paths[lane]), lane)
        for lane in ("P0", "P1", "G")
    }
    frozen_lanes = [
        lane
        for lane, receipt in lane_receipts.items()
        if receipt["status"] == FREEZE_STATUS
    ]
    all_frozen = len(frozen_lanes) == 3

    if all_frozen:
        contexts = {
            (receipt["population_id"], receipt["season_id"])
            for receipt in lane_receipts.values()
        }
        same_context = len(contexts) == 1
        blocker = (
            "CONFIRMATORY_P0_P1_G_RECEIPTS_REQUIRED"
            if same_context
            else "FROZEN_CONFIG_CONTEXT_MISMATCH"
        )
    else:
        same_context = False
        blocker = "PROSPECTIVE_THRESHOLD_FREEZE_REQUIRED"

    module_counts = _module_counts(module_ledger_path)

    return {
        "analysis": "pedicularis_execution_frontier",
        "threshold_gate_module_counts": module_counts,
        "unresolved_calibration_gate_count": (
            module_counts.get("CAL_A", 0)
            + module_counts.get("CAL_B", 0)
            + module_counts.get("CAL_C", 0)
        ),
        "calibration_program_sequence": ["CAL_A", "CAL_B", "CAL_C"],
        "config_freeze_by_lane": lane_receipts,
        "n_lanes_frozen": len(frozen_lanes),
        "frozen_lanes": frozen_lanes,
        "all_three_lane_configs_frozen": all_frozen,
        "same_population_and_season_after_freeze": same_context,
        "confirmatory_execution_requirements": [
            "P0_treatment_blind_SHA256_z_sham_allocation",
            "P1_treatment_blind_SHA256_paired_NATURAL_vs_SUPPLEMENTED_allocation",
            "G_preoutcome_hard_pass_method_freeze",
            "G_treatment_blind_SHA256_paired_EXPOSED_vs_EXCLUDED_allocation",
            "locked_P0_P1_G_production_evaluators",
            "readiness_V3_requires_all_three_randomized_provenance_blocks",
            "geometry_intervention_plan_binding_frozen_before_confirmatory_outcomes",
            "POWER_GEOMETRY_PILOT_may_collect_in_parallel_on_disjoint_cohort",
            "geometry_summary_requires_later_positive_matching_readiness_V3",
        ],
        "current_blocker": blocker,
        "next_action": (
            "Complete nonconfirmatory CAL-A (measurement/equivalence), CAL-B (exploratory effects/G timing), and CAL-C (power/precision), then freeze P0/P1/G gate values with one basis note per gate before reading confirmatory outcomes."
            if blocker == "PROSPECTIVE_THRESHOLD_FREEZE_REQUIRED"
            else (
                "Re-freeze all three lane configs for one common population and season before collecting confirmatory data."
                if blocker == "FROZEN_CONFIG_CONTEXT_MISMATCH"
                else (
                    "Register treatment-blind P0/P1/G flower IDs and preselect "
                    "one hard-validity-pass G method. Before outcomes, bind the "
                    "frozen P0 z plan plus P0/P1/G configs and selected G method "
                    "to any planned POWER_GEOMETRY_PILOT. Then collect the "
                    "disjoint geometry cohort in parallel with randomized "
                    "confirmatory P0/P1/G. Use geometry only after the locked "
                    "lane evaluators produce a positive exact-plan-matching "
                    "readiness V3 receipt."
                )
            )
        ),
        "claim_ceiling": (
            "execution_frontier_only; no empirical receipt is inferred from config presence; "
            "unit-test fixture values are not field thresholds"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit the Pedicularis empirical execution frontier without reading outcome data"
    )
    parser.add_argument("--p0-config", type=Path, default=DEFAULT_CONFIGS["P0"])
    parser.add_argument("--p1-config", type=Path, default=DEFAULT_CONFIGS["P1"])
    parser.add_argument("--g-config", type=Path, default=DEFAULT_CONFIGS["G"])
    parser.add_argument("--module-ledger", type=Path, default=DEFAULT_MODULE_LEDGER)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build(
        {"P0": args.p0_config, "P1": args.p1_config, "G": args.g_config},
        module_ledger_path=args.module_ledger,
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

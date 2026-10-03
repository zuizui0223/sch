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
    configs = {
        lane: _load(config_paths[lane])
        for lane in ("P0", "P1", "G")
    }
    lane_receipts = {
        lane: inspect_prospective_freeze(configs[lane], lane)
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
        g_method = (
            configs["G"].get("method_gate", {}).get(
                "selected_exclusion_method"
            )
        )
        g_method_selected = (
            isinstance(g_method, str)
            and bool(g_method.strip())
            and g_method != "REQUIRED_BEFORE_USE"
        )
        if not same_context:
            blocker = "FROZEN_CONFIG_CONTEXT_MISMATCH"
        elif not g_method_selected:
            blocker = "G_DEVICE_SELECTION_REQUIRED"
        else:
            blocker = "CONFIRMATORY_P0_P1_G_RECEIPTS_REQUIRED"
    else:
        same_context = False
        g_method_selected = False
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
        "g_device_selected": g_method_selected,
        "selected_g_device": (
            configs["G"].get("method_gate", {}).get(
                "selected_exclusion_method"
            )
            if g_method_selected
            else None
        ),
        "current_blocker": blocker,
        "next_action": (
            "Complete nonconfirmatory CAL-A (measurement/equivalence), CAL-B (exploratory effects/G timing), and CAL-C (power/precision), then freeze P0/P1/G gate values with one basis note per gate before reading confirmatory outcomes."
            if blocker == "PROSPECTIVE_THRESHOLD_FREEZE_REQUIRED"
            else (
                "Re-freeze all three lane configs for one common population and season before collecting confirmatory data."
                if blocker == "FROZEN_CONFIG_CONTEXT_MISMATCH"
                else (
                    "Complete the threshold-free G device screen, prospectively freeze one hard-validity-admissible exclusion method, and propagate that method identity into the G config before confirmatory collection."
                    if blocker == "G_DEVICE_SELECTION_REQUIRED"
                    else "Collect same-context P0/P1/G confirmatory data and generate the three positive evaluator receipts."
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

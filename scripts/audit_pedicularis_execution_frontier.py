from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.pedicularis_config_freeze import (
    FREEZE_STATUS,
    inspect_prospective_freeze,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIGS = {
    "P0": ROOT / "empirical" / "architecture" / "PEDICULARIS_STAGE_P0_CONFIG_TEMPLATE_V1.json",
    "P1": ROOT / "empirical" / "architecture" / "PEDICULARIS_POLLINATION_WEIGHT_CONFIG_TEMPLATE_V1.json",
    "G": ROOT / "empirical" / "architecture" / "PEDICULARIS_PREDATOR_METHOD_CONFIG_V3.json",
}


def _load(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"config {path} is not a JSON object")
    return payload


def build(config_paths: dict[str, Path]) -> dict:
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

    return {
        "analysis": "pedicularis_execution_frontier",
        "config_freeze_by_lane": lane_receipts,
        "n_lanes_frozen": len(frozen_lanes),
        "frozen_lanes": frozen_lanes,
        "all_three_lane_configs_frozen": all_frozen,
        "same_population_and_season_after_freeze": same_context,
        "current_blocker": blocker,
        "next_action": (
            "Freeze P0/P1/G gate values, population, season, timing, and one basis note per gate before reading confirmatory outcomes."
            if blocker == "PROSPECTIVE_THRESHOLD_FREEZE_REQUIRED"
            else (
                "Re-freeze all three lane configs for one common population and season before collecting confirmatory data."
                if blocker == "FROZEN_CONFIG_CONTEXT_MISMATCH"
                else "Collect same-context P0/P1/G confirmatory data and generate the three positive evaluator receipts."
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
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = build({"P0": args.p0_config, "P1": args.p1_config, "G": args.g_config})
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "scripts" / "build_sch_h2_estimand_recovery_audit_cumulative.py"


def _load_v1():
    spec = importlib.util.spec_from_file_location("sch_h2_estimand_audit_cumulative_v1", V1)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(queue_path: Path, audit_paths: list[Path]) -> dict:
    result = _load_v1().build(queue_path, audit_paths)
    complete = result["n_unaudited_queue_records"] == 0
    result["analysis"] = "sch_h2_estimand_recovery_audit_cumulative_v2"
    result["fulltext_queue_audit_complete"] = complete
    result["next_screening_frontier"] = (
        "463_TITLE_ABSTRACT_UNSCREENED_RECORDS"
        if complete
        else "REMAINING_V20_FULLTEXT_PENDING"
    )
    result["status"] = (
        "ESTIMAND_RECOVERY_FULLTEXT_QUEUE_COMPLETE_ZERO_TOTAL_SELECTION_PROMOTIONS"
        if complete and result["n_total_selection_effect_promotions"] == 0
        else "ESTIMAND_RECOVERY_FULLTEXT_QUEUE_PARTIAL_OR_PROMOTED"
    )
    for marker in (
        "current_29_fulltext_pending_records_cannot_expand_TOTAL_SELECTION_EFFECT_under_current_audit",
        "next_expansion_must_return_to_frozen_unscreened_cohort_outcome_blind",
    ):
        if marker not in result["claim_ceiling"]:
            result["claim_ceiling"].append(marker)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("queue", type=Path)
    parser.add_argument("--audits", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.queue, args.audits)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V2_SCRIPT = ROOT / "scripts" / "evaluate_sch_h2_reversal_holdout_v2.py"


def _v2():
    spec = importlib.util.spec_from_file_location("sch_h2_holdout_v2", V2_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def validate_source_derivation(
    protocol_path: Path,
    active_source_path: Path,
    original_queue_path: Path,
) -> dict[str, object]:
    mod = _v2()
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    source = protocol["holdout_source"]

    if mod._git_blob_sha(original_queue_path) != source["derived_from_queue_git_blob_sha"]:
        raise ValueError("original 463-record queue blob SHA mismatch")
    if mod._git_blob_sha(active_source_path) != source["git_blob_sha"]:
        raise ValueError("active 456-record holdout roster blob SHA mismatch")

    original = mod._read_csv(original_queue_path)
    active = mod._read_csv(active_source_path)

    if len(original) != source["derived_from_queue_n_records"]:
        raise ValueError("original queue record count mismatch")
    if len(active) != source["n_records"]:
        raise ValueError("active holdout roster record count mismatch")

    original_ids = [row["record_id"] for row in original]
    active_ids = [row["record_id"] for row in active]
    excluded = source["pre_v3_formally_screened_record_ids"]

    if len(set(original_ids)) != len(original_ids):
        raise ValueError("original queue record IDs are not unique")
    if len(set(active_ids)) != len(active_ids):
        raise ValueError("active holdout record IDs are not unique")
    if len(set(excluded)) != len(excluded):
        raise ValueError("pre-V3 exclusion IDs are not unique")

    expected_active = [record_id for record_id in original_ids if record_id not in set(excluded)]
    if active_ids != expected_active:
        raise ValueError("active holdout roster is not original queue minus the seven pre-V3 screened records")

    missing_excluded = sorted(set(excluded) - set(original_ids))
    if missing_excluded:
        raise ValueError("pre-V3 screened ID absent from original queue: " + ", ".join(missing_excluded))

    if {row["current_title_abstract_decision"] for row in active} != {"UNSCREENED"}:
        raise ValueError("active holdout roster contains a pre-decided queue row")
    if {row["title_abstract_screening_status"] for row in active} != {"PENDING"}:
        raise ValueError("active holdout roster contains a non-pending queue row")
    if {row["outcome_blind_priority"] for row in active} != {"YES"}:
        raise ValueError("active holdout roster is not outcome blind")

    return {
        "original_queue_n": len(original),
        "pre_v3_formally_screened_n": len(excluded),
        "active_holdout_n": len(active),
        "review_order_preserved": True,
    }


def build(
    protocol_path: Path,
    registry_path: Path,
    active_source_path: Path,
    original_queue_path: Path,
) -> dict[str, object]:
    source_receipt = validate_source_derivation(
        protocol_path,
        active_source_path,
        original_queue_path,
    )
    mod = _v2()
    result = mod.build(protocol_path, registry_path, active_source_path)
    result["analysis"] = "sch_h2_reversal_holdout_v3"
    result["source_derivation"] = source_receipt
    result["status"] = "PROSPECTIVE_REVERSAL_HOLDOUT_V3_FROZEN"
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("protocol", type=Path)
    p.add_argument("registry", type=Path)
    p.add_argument("active_source", type=Path)
    p.add_argument("original_queue", type=Path)
    p.add_argument("--output", type=Path)
    a = p.parse_args()

    result = build(
        a.protocol,
        a.registry,
        a.active_source,
        a.original_queue,
    )
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if a.output:
        a.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()

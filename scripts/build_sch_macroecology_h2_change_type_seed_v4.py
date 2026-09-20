from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V3_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed_v3.py"


def _load_v3():
    spec = importlib.util.spec_from_file_location("sch_h2_change_v3", V3_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(path: Path) -> dict:
    result = _load_v3().build(path)
    result["analysis"] = "sch_macroecology_h2_change_type_seed_v4"
    result["status"] = "H2_CHANGE_TYPE_SEED_V4_PEDICULARIS_PRESSURE_ADDED"
    marker = "antagonist_pressure_cases_do_not_identify_local_geometry"
    if marker not in result["claim_ceiling"]:
        result["claim_ceiling"].insert(-1, marker)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build(args.seed)
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()

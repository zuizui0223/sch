from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V4_SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h2_change_type_seed_v4.py"


def _load_v4():
    spec = importlib.util.spec_from_file_location("sch_h2_change_v4", V4_SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def build(path):
    result = _load_v4().build(path)
    result["analysis"] = "sch_macroecology_h2_change_type_seed_v5"
    result["status"] = "H2_CHANGE_TYPE_SEED_V5_TRIFOLIUM_NET_SELECTION_ADDED"
    return result


def main():
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

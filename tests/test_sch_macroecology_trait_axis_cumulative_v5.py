import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCHES = [
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH2_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH3_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH4_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH5_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH6_V1.csv",
]
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_CUMULATIVE_V5.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_trait_axis_cumulative.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_trait_cumulative_v5", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(BATCHES)


def test_complete_source_axis_recode_structure():
    built = _build()
    assert built["n_trait_axes"] == 59
    assert built["n_source_records"] == 34
    assert built["n_biological_clusters"] == 31
    assert built["n_fixed_role_axes"] == 44


def test_complete_source_axis_fixed_role_geometry():
    built = _build()
    assert built["n_fixed_role_geometry_resolved_axes"] == 21
    assert built["n_fixed_role_geometry_resolved_clusters"] == 14
    assert built["resolved_fixed_role_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 3,
        "CONFLICT": 9,
        "ONE_SIDED_OR_NULL": 9,
    }
    assert built["n_resolved_fixed_role_axes_with_context_shift"] == 9
    assert built["n_resolved_fixed_role_axes_with_cancellation"] == 1


def test_complete_source_axis_readout_matches_builder():
    built = _build()
    assert built == json.loads(READOUT.read_text(encoding="utf-8"))

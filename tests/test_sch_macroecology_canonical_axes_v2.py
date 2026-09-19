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
OVERRIDES = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_OVERRIDES_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_READOUT_V2.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_canonical_axes.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_canonical_axes_v2", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(BATCHES, OVERRIDES)


def test_complete_canonical_axis_denominator():
    built = _build()
    assert built["n_source_axis_records"] == 57
    assert built["n_model_axis_source_records"] == 50
    assert built["n_source_records_excluded_before_canonical_axis"] == 7
    assert built["n_canonical_trait_axes"] == 48
    assert built["n_axes_with_multiple_source_records"] == 2


def test_complete_canonical_geometry():
    built = _build()
    assert built["n_fixed_role_canonical_axes"] == 35
    assert built["n_role_boundary_canonical_axes"] == 13
    assert built["n_fixed_role_resolved_canonical_axes"] == 20
    assert built["canonical_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 9,
        "CONTEXT_VARIABLE": 1,
        "ONE_SIDED_OR_NULL": 8,
        "ROLE_BOUNDARY": 13,
        "UNRESOLVED": 15,
    }


def test_complete_canonical_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

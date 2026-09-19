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
]
OVERRIDES = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_OVERRIDES_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_canonical_axes.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_canonical_axes", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(BATCHES, OVERRIDES)


def test_source_axis_records_collapse_to_canonical_axes():
    built = _build()
    assert built["n_source_axis_records"] == 48
    assert built["n_model_axis_source_records"] == 45
    assert built["n_source_records_excluded_before_canonical_axis"] == 3
    assert built["n_canonical_trait_axes"] == 44
    assert built["n_axes_with_multiple_source_records"] == 1
    assert built["multi_source_canonical_axes"] == ["Gentiana_lutea_color_axis"]


def test_cross_source_geometry_change_is_context_variable():
    built = _build()
    assert built["n_context_variable_canonical_axes"] == 1
    assert built["context_variable_canonical_axes"] == ["Gentiana_lutea_color_axis"]
    assert built["canonical_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 9,
        "CONTEXT_VARIABLE": 1,
        "ONE_SIDED_OR_NULL": 5,
        "ROLE_BOUNDARY": 13,
        "UNRESOLVED": 14,
    }


def test_canonical_fixed_role_denominator_is_not_source_record_count():
    built = _build()
    assert built["n_fixed_role_canonical_axes"] == 31
    assert built["n_fixed_role_resolved_canonical_axes"] == 17
    assert built["n_role_boundary_canonical_axes"] == 13
    assert built["excluded_source_axis_ids"] == [
        "CloudForest_000214_patch_display",
        "Haplopappus_000233_odor_blend",
        "Pulsatilla_000213_stalk_height",
    ]
    assert "source_axis_records_are_not_independent_trait_axes" in built["claim_ceiling"]


def test_canonical_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

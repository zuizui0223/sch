import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCHES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH{i}_V1.csv"
    for i in range(1, 7)
]
OVERRIDES = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_OVERRIDES_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_READOUT_V2.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_canonical_axes.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_canonical_v2", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(BATCHES, OVERRIDES)


def test_complete_p1_canonical_denominator():
    built = _build()
    assert built["n_source_axis_records"] == 56
    assert built["n_model_axis_source_records"] == 49
    assert built["n_source_records_excluded_before_canonical_axis"] == 7
    assert built["n_canonical_trait_axes"] == 47
    assert built["n_fixed_role_canonical_axes"] == 34
    assert built["n_role_boundary_canonical_axes"] == 13


def test_complete_p1_canonical_geometry():
    built = _build()
    assert built["n_fixed_role_resolved_canonical_axes"] == 20
    assert built["canonical_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 8,
        "CONTEXT_VARIABLE": 2,
        "ONE_SIDED_OR_NULL": 8,
        "ROLE_BOUNDARY": 13,
        "UNRESOLVED": 14,
    }


def test_cross_source_context_variable_axes_are_not_double_counted():
    built = _build()
    assert built["n_axes_with_multiple_source_records"] == 2
    assert built["multi_source_canonical_axes"] == [
        "Collaea_000312_flower_number",
        "Gentiana_lutea_color_axis",
    ]
    assert built["context_variable_canonical_axes"] == [
        "Collaea_000312_flower_number",
        "Gentiana_lutea_color_axis",
    ]


def test_complete_p1_canonical_readout_matches_builder():
    built = _build()
    frozen = json.loads(READOUT.read_text(encoding="utf-8"))
    for key in (
        "n_source_axis_records",
        "n_model_axis_source_records",
        "n_source_records_excluded_before_canonical_axis",
        "excluded_source_axis_ids",
        "n_canonical_trait_axes",
        "n_axes_with_multiple_source_records",
        "multi_source_canonical_axes",
        "n_fixed_role_canonical_axes",
        "n_role_boundary_canonical_axes",
        "n_fixed_role_resolved_canonical_axes",
        "canonical_geometry_counts",
        "n_context_variable_canonical_axes",
        "context_variable_canonical_axes",
    ):
        assert built[key] == frozen[key]

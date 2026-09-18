import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH1 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH1_V1.csv"
BATCH2 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH2_V1.csv"
BATCH3 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH3_V1.csv"
BATCH4 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH4_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_CUMULATIVE_V3.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_trait_axis_cumulative.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_trait_cumulative_v3", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build([BATCH1, BATCH2, BATCH3, BATCH4])


def test_cumulative_trait_axis_v3_structure():
    built = _build()
    assert built["n_trait_axes"] == 38
    assert built["n_source_records"] == 22
    assert built["n_biological_clusters"] == 20
    assert built["n_fixed_role_axes"] == 29


def test_cumulative_trait_axis_v3_fixed_role_geometry():
    built = _build()
    assert built["n_fixed_role_geometry_resolved_axes"] == 15
    assert built["n_fixed_role_geometry_resolved_clusters"] == 11
    assert built["resolved_fixed_role_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 3,
        "CONFLICT": 9,
        "ONE_SIDED_OR_NULL": 3,
    }


def test_cumulative_trait_axis_v3_keeps_boundary_and_context_structure():
    built = _build()
    assert built["n_consumer_role_boundary_axes"] == 9
    assert built["n_consumer_role_boundary_clusters"] == 6
    assert built["n_resolved_fixed_role_axes_with_context_shift"] == 5
    assert built["n_resolved_fixed_role_axes_with_cancellation"] == 1


def test_cumulative_trait_axis_v3_readout_matches_builder():
    built = _build()
    frozen = json.loads(READOUT.read_text(encoding="utf-8"))
    for key in (
        "n_batches",
        "batch_files",
        "n_trait_axes",
        "n_source_records",
        "n_biological_clusters",
        "conflict_detected_counts",
        "alignment_detected_counts",
        "one_sided_or_null_detected_counts",
        "context_shift_detected_counts",
        "antagonist_role_status_counts",
        "coding_status_counts",
        "n_fixed_role_axes",
        "n_fixed_role_geometry_resolved_axes",
        "n_fixed_role_geometry_resolved_clusters",
        "resolved_fixed_role_geometry_counts",
        "n_resolved_fixed_role_axes_with_context_shift",
        "n_resolved_fixed_role_axes_with_cancellation",
        "n_consumer_role_boundary_axes",
        "n_consumer_role_boundary_clusters",
        "consumer_role_boundary_axis_counts",
        "status",
        "claim_ceiling",
    ):
        assert built[key] == frozen[key]

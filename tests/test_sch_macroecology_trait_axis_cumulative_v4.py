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
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_CUMULATIVE_V4.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_trait_axis_cumulative.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_trait_cumulative_v4", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(BATCHES)


def test_cumulative_trait_axis_v4_structure():
    built = _build()
    assert built["n_trait_axes"] == 48
    assert built["n_source_records"] == 26
    assert built["n_biological_clusters"] == 24
    assert built["n_fixed_role_axes"] == 34
    assert built["n_consumer_role_boundary_axes"] == 14


def test_cumulative_trait_axis_v4_fixed_role_geometry():
    built = _build()
    assert built["n_fixed_role_geometry_resolved_axes"] == 17
    assert built["n_fixed_role_geometry_resolved_clusters"] == 12
    assert built["resolved_fixed_role_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 3,
        "CONFLICT": 9,
        "ONE_SIDED_OR_NULL": 5,
    }


def test_cumulative_trait_axis_v4_context_and_role_structure():
    built = _build()
    assert built["consumer_role_boundary_axis_counts"] == {
        "BENEFIT_COST_COUPLED": 5,
        "ROLE_DEPENDENT": 9,
    }
    assert built["n_resolved_fixed_role_axes_with_context_shift"] == 7
    assert built["n_resolved_fixed_role_axes_with_cancellation"] == 1


def test_cumulative_trait_axis_v4_readout_matches_builder():
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

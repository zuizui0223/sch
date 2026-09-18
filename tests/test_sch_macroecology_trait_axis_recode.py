import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH1_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH1_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_trait_axis_readout.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_trait_axis", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(LEDGER)


def test_trait_axis_batch_preserves_cluster_dependence():
    built = _build()
    assert built["n_trait_axes"] == 15
    assert built["n_source_records"] == 8
    assert built["n_biological_clusters"] == 7
    assert built["n_fixed_role_geometry_resolved_axes"] == 7
    assert built["n_fixed_role_geometry_resolved_clusters"] == 5


def test_resolved_fixed_role_axes_show_multiple_ecological_geometries():
    built = _build()
    assert built["resolved_fixed_role_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 3,
        "ONE_SIDED_OR_NULL": 2,
    }
    assert built["n_resolved_axes_with_context_shift"] == 4
    assert built["n_resolved_axes_with_cancellation"] == 1


def test_role_switching_is_not_forced_into_fixed_antagonist_geometry():
    built = _build()
    assert built["antagonist_role_status_counts"]["ROLE_DEPENDENT"] == 1
    assert built["n_role_dependent_boundary_axes"] == 1


def test_unresolved_axes_remain_visible():
    built = _build()
    assert built["conflict_detected_counts"]["UNRESOLVED"] == 8
    assert built["coding_status_counts"]["AXIS_FROZEN_OUTCOME_PENDING"] == 1
    assert "unresolved_axes_retained" in built["claim_ceiling"]


def test_trait_axis_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

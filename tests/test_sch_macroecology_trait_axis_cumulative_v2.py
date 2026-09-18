import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH1 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH1_V1.csv"
BATCH2 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH2_V1.csv"
BATCH3 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH3_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_CUMULATIVE_V2.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_trait_axis_cumulative.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_trait_cumulative_v2", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build([BATCH1, BATCH2, BATCH3])


def test_cumulative_trait_axis_v2_has_31_axes():
    built = _build()
    assert built["n_trait_axes"] == 31
    assert built["n_source_records"] == 19
    assert built["n_biological_clusters"] == 17
    assert built["n_fixed_role_geometry_resolved_axes"] == 10
    assert built["n_fixed_role_geometry_resolved_clusters"] == 8


def test_cumulative_trait_axis_v2_recovers_three_fixed_role_geometries():
    built = _build()
    assert built["resolved_fixed_role_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 3,
        "CONFLICT": 4,
        "ONE_SIDED_OR_NULL": 3,
    }


def test_cumulative_trait_axis_v2_keeps_role_boundaries_and_downgrades():
    built = _build()
    assert built["n_consumer_role_boundary_axes"] == 9
    assert built["consumer_role_boundary_axis_counts"] == {
        "BENEFIT_COST_COUPLED": 5,
        "ROLE_DEPENDENT": 4,
    }


def test_cumulative_trait_axis_v2_readout_matches_builder():
    built = _build()
    frozen = json.loads(READOUT.read_text(encoding="utf-8"))
    assert built["n_trait_axes"] == frozen["n_trait_axes"]
    assert built["n_source_records"] == frozen["n_source_records"]
    assert built["n_biological_clusters"] == frozen["n_biological_clusters"]
    assert built["n_fixed_role_geometry_resolved_axes"] == frozen["n_fixed_role_geometry_resolved_axes"]
    assert built["n_fixed_role_geometry_resolved_clusters"] == frozen["n_fixed_role_geometry_resolved_clusters"]
    assert built["resolved_fixed_role_geometry_counts"] == frozen["resolved_fixed_role_geometry_counts"]
    assert built["n_consumer_role_boundary_axes"] == frozen["n_consumer_role_boundary_axes"]

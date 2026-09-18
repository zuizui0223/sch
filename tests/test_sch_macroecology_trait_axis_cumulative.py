import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH1 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH1_V1.csv"
BATCH2 = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH2_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_CUMULATIVE_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_trait_axis_cumulative.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_trait_cumulative", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build([BATCH1, BATCH2])


def test_cumulative_trait_axis_structure():
    built = _build()
    assert built["n_trait_axes"] == 24
    assert built["n_source_records"] == 12
    assert built["n_biological_clusters"] == 10
    assert built["n_fixed_role_axes"] == 17


def test_fixed_role_geometry_result_remains_bounded():
    built = _build()
    assert built["n_fixed_role_geometry_resolved_axes"] == 7
    assert built["n_fixed_role_geometry_resolved_clusters"] == 5
    assert built["resolved_fixed_role_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 3,
        "ONE_SIDED_OR_NULL": 2,
    }


def test_consumer_role_boundary_is_explicit():
    built = _build()
    assert built["n_consumer_role_boundary_axes"] == 7
    assert built["n_consumer_role_boundary_clusters"] == 4
    assert built["consumer_role_boundary_axis_counts"] == {
        "BENEFIT_COST_COUPLED": 5,
        "ROLE_DEPENDENT": 2,
    }


def test_cumulative_trait_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

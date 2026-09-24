import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCHES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH{i}_V1.csv"
    for i in range(1, 7)
]
OVERRIDES = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_OVERRIDES_V2.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_LEDGER_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_canonical_ledger.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_canonical_ledger", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(BATCHES, OVERRIDES)


def test_canonical_ledger_materializes_independent_model_units():
    rows, receipt = _build()
    assert len(rows) == 52
    assert receipt["n_source_axis_records"] == 59
    assert receipt["n_excluded_source_axis_records"] == 7
    assert receipt["n_model_source_axis_records"] == 50
    assert receipt["n_canonical_trait_axes"] == 50


def test_canonical_ledger_static_h1_frontier():
    rows, receipt = _build()
    assert receipt["n_fixed_role_axes"] == 36
    assert receipt["n_static_resolved_fixed_role_axes"] == 19
    assert receipt["n_static_resolved_fixed_role_clusters"] == 13
    assert receipt["static_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 9,
        "ONE_SIDED_OR_NULL": 8,
    }
    assert sum(row["model_h1_status"] == "STATIC_RESOLVED_FIXED_ROLE" for row in rows) == 19


def test_canonical_ledger_keeps_context_variable_and_role_boundary_separate():
    rows, receipt = _build()
    assert receipt["canonical_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 9,
        "CONTEXT_VARIABLE": 1,
        "ONE_SIDED_OR_NULL": 8,
        "ROLE_BOUNDARY": 14,
        "UNRESOLVED": 16,
    }
    assert sum(row["canonical_geometry"] == "CONTEXT_VARIABLE" for row in rows) == 1
    assert sum(row["canonical_geometry"] == "ROLE_BOUNDARY" for row in rows) == 14


def test_canonical_ledger_readout_is_reproducible():
    _, receipt = _build()
    assert receipt == json.loads(READOUT.read_text(encoding="utf-8"))

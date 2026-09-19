import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCHES = [
    ROOT / "data" / f"SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH{i}_V1.csv"
    for i in range(1, 7)
]
OVERRIDES = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_OVERRIDES_V1.csv"
TABLE = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_TABLE_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_AXIS_TABLE_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_canonical_axis_table.py"


def _module():
    spec = importlib.util.spec_from_file_location("sch_macro_canonical_table", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def test_canonical_model_table_rebuilds_47_axes():
    mod = _module()
    rows, receipt = mod.build(BATCHES, OVERRIDES)
    assert len(rows) == 47
    assert receipt["n_canonical_trait_axes"] == 47
    assert receipt["n_axes_with_multiple_source_records"] == 2


def test_canonical_model_table_has_bounded_static_H1_set():
    _, receipt = _module().build(BATCHES, OVERRIDES)
    assert receipt["n_h1_static_eligible_axes"] == 18
    assert receipt["h1_static_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 8,
        "ONE_SIDED_OR_NULL": 8,
    }
    assert receipt["n_h2_context_priority_axes"] == 30


def test_trait_domain_normalization_is_closed():
    _, receipt = _module().build(BATCHES, OVERRIDES)
    assert receipt["trait_domain_counts"] == {
        "CHEMICAL_SIGNAL": 4,
        "DISPLAY_STATE": 4,
        "MORPHOLOGY": 30,
        "PHENOLOGY": 2,
        "REWARD": 4,
        "VISUAL_SIGNAL": 3,
    }


def test_committed_canonical_table_matches_builder(tmp_path):
    mod = _module()
    rows, receipt = mod.build(BATCHES, OVERRIDES)
    generated = tmp_path / "canonical.csv"
    mod._write_csv(generated, rows)
    assert generated.read_text(encoding="utf-8") == TABLE.read_text(encoding="utf-8")
    assert receipt == json.loads(READOUT.read_text(encoding="utf-8"))

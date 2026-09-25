import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = [
    ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH2_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_P1_REMAINDER_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_V26_HOLDOUT_V1.csv",
]
AXES = [
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH2_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH3_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH4_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH5_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH6_V1.csv",
]
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H1_SOURCE_AXIS_COVERAGE_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_h1_source_axis_coverage.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_h1_coverage", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(DESIGN, AXES)


def test_all_record_level_h1_candidates_are_source_axis_recoded():
    built = _build()
    assert built["n_record_level_h1_candidates"] == 38
    assert built["n_h1_candidates_with_source_axis_record"] == 34
    assert built["n_h1_candidates_missing_source_axis_record"] == 4
    assert built["missing_h1_record_ids"] == [
        "SCHPRISMA-000649",
        "SCHPRISMA-000651",
        "SCHPRISMA-000661",
        "SCHPRISMA-000723",
    ]
    assert built["status"] == "H1_SOURCE_AXIS_RECODE_INCOMPLETE"


def test_source_audit_separates_full_from_partial_downgrades():
    built = _build()
    assert built["n_h1_source_records_with_model_axis"] == 28
    assert built["n_h1_source_records_fully_downgraded_after_source_audit"] == 6
    assert built["fully_downgraded_h1_record_ids"] == [
        "SCHPRISMA-000202",
        "SCHPRISMA-000213",
        "SCHPRISMA-000214",
        "SCHPRISMA-000233",
        "SCHPRISMA-000253",
        "SCHPRISMA-000287",
    ]
    assert built["n_h1_source_records_partially_downgraded"] == 1
    assert built["partially_downgraded_h1_record_ids"] == ["SCHPRISMA-000353"]


def test_h1_coverage_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGN = [
    ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH1_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH2_V1.csv",
    ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_P1_REMAINDER_V1.csv",
]
TRAITS = [
    ROOT / "data" / f"SCH_MACROECOLOGY_TRAIT_AXIS_RECODE_BATCH{i}_V1.csv"
    for i in range(1, 7)
]
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_P1_SOURCE_AXIS_CLOSURE_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_p1_source_axis_closure.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_p1_source_closure", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(DESIGN, TRAITS)


def test_all_h1_candidates_are_source_axis_recoded():
    built = _build()
    assert built["n_h1_record_level_candidates"] == 32
    assert built["n_h1_candidates_source_axis_recoded"] == 32
    assert built["n_h1_candidates_missing_source_axis_recode"] == 0
    assert built["status"] == "ALL_H1_RECORD_CANDIDATES_SOURCE_AUDITED"


def test_source_audit_has_three_explicit_record_level_fates():
    built = _build()
    assert built["source_fate_counts"] == {
        "FULLY_DOWNGRADED": 6,
        "RETAINS_FIXED_ROLE_AXIS": 19,
        "ROLE_BOUNDARY_ONLY": 7,
    }
    assert len(built["fully_downgraded_source_ids"]) == 6
    assert len(built["role_boundary_only_source_ids"]) == 7


def test_source_axis_closure_preserves_design_evidence_after_downgrade():
    built = _build()
    assert "fully_downgraded_sources_remain_H4_evidence" in built["claim_ceiling"]
    assert built["n_source_axis_records"] == 56
    assert built["n_model_eligible_or_boundary_source_axes"] == 49


def test_source_axis_closure_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH1_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH1_READOUT_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_design_recode_readout.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_design_recode", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(CSV)


def test_first_design_recode_batch_is_outcome_blind():
    built = _build()
    assert built["n_records"] == 22
    assert built["n_outcomes_coded"] == 0
    assert built["status"] == "DESIGN_RECODE_FROZEN_OUTCOME_BLIND"
    assert built["design_audit_eligible_counts"] == {"YES": 22}


def test_first_design_recode_batch_separates_geometry_from_design_value():
    built = _build()
    assert built["n_geometry_eligible"] == 8
    assert built["geometry_eligibility_counts"] == {
        "ELIGIBLE_BOUNDED_COORDINATE": 3,
        "ELIGIBLE_SAME_COORDINATE": 5,
        "INELIGIBLE_NO_COMMON_FITNESS_LINK": 3,
        "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY": 9,
        "UNRESOLVED_SOURCE": 2,
    }
    assert built["context_switch_eligibility_counts"]["ELIGIBLE_MULTI_CONTEXT"] == 5


def test_design_recode_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

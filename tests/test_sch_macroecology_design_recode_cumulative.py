import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH1 = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH1_V1.csv"
BATCH2 = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_BATCH2_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_DESIGN_RECODE_CUMULATIVE_V1.json"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_design_recode_cumulative.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_design_cumulative", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build([BATCH1, BATCH2])


def test_cumulative_design_frontier_keeps_all_recoded_records():
    built = _build()
    assert built["n_batches"] == 2
    assert built["n_records"] == 44
    assert built["n_design_audit_eligible"] == 44
    assert built["n_outcomes_coded_in_design_batches"] == 0


def test_cumulative_design_frontier_localizes_major_gaps():
    built = _build()
    assert built["n_geometry_eligible"] == 12
    assert built["geometry_eligibility_counts"] == {
        "ELIGIBLE_BOUNDED_COORDINATE": 7,
        "ELIGIBLE_SAME_COORDINATE": 5,
        "INELIGIBLE_MULTIVARIATE_UNRESOLVED": 2,
        "INELIGIBLE_NO_COMMON_FITNESS_LINK": 6,
        "INELIGIBLE_NO_TWO_FUNCTION_GEOMETRY": 20,
        "UNRESOLVED_SOURCE": 4,
    }
    assert built["n_context_switch_eligible"] == 8


def test_cumulative_design_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

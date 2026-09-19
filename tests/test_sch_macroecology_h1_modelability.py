import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data" / "SCH_MACROECOLOGY_CANONICAL_TRAIT_AXIS_LEDGER_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_H1_MODELABILITY_V1.json"
SCRIPT = ROOT / "scripts" / "diagnose_sch_macroecology_h1_modelability.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_h1_modelability", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(LEDGER)


def test_h1_modelability_gate_fails_closed():
    built = _build()
    assert built["n_static_resolved_fixed_role_axes"] == 19
    assert built["n_static_resolved_fixed_role_clusters"] == 13
    assert built["static_geometry_counts"] == {
        "ALIGNMENT_REINFORCEMENT": 2,
        "CONFLICT": 9,
        "ONE_SIDED_OR_NULL": 8,
    }
    assert built["multinomial_geometry_model_ready"] is False
    assert built["binary_conflict_model_ready"] is False
    assert built["primary_h1_status"] == "REGRESSION_GATE_FAIL_DESCRIPTIVE_EXACT_ONLY"


def test_h1_modelability_gate_tracks_cluster_dependence_and_sparse_moderators():
    built = _build()
    assert built["n_multi_axis_static_clusters"] == 6
    assert built["trait_domain_counts"]["PHENOLOGY"] == 1
    assert built["antagonist_guild_family_counts"]["SEED_PREDATOR"] == 8
    assert built["trait_domain_moderator_ready_without_collapse"] is False
    assert built["antagonist_guild_moderator_ready_without_collapse"] is False


def test_h1_modelability_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))

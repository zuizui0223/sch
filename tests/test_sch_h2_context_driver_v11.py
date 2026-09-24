import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analyze_sch_h2_context_driver_v11.py"


def _build():
    spec = importlib.util.spec_from_file_location("h2ctxv11", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(ROOT)


def _families(result):
    return {r["context_family"]: r for r in result["context_family_summary"]}


def test_v11_preserves_v10_directional_denominator_and_programme_unit():
    result = _build()
    assert result["n_repeated_axes"] == 27
    assert result["n_repeated_programmes"] == 7
    assert result["n_point_switch_axes"] == 14
    assert result["n_supported_switch_axes"] == 3
    assert result["n_programmes_with_point_switch"] == 6
    assert result["n_programmes_with_supported_switch"] == 2


def test_v11_decomposes_context_drivers_without_pseudoreplication():
    result = _build()
    fam = _families(result)

    assert fam["BIOTIC_REGIME_MANIPULATION"] == {
        "context_family": "BIOTIC_REGIME_MANIPULATION",
        "n_programmes": 5,
        "n_programmes_with_point_switch": 4,
        "n_programmes_with_supported_switch": 1,
        "n_repeated_axes": 22,
        "n_point_switch_axes": 10,
        "n_supported_switch_axes": 1,
        "n_uncertainty_unresolved_switch_axes": 0,
    }
    assert fam["NATURAL_SPATIAL_MOSAIC"] == {
        "context_family": "NATURAL_SPATIAL_MOSAIC",
        "n_programmes": 1,
        "n_programmes_with_point_switch": 1,
        "n_programmes_with_supported_switch": 1,
        "n_repeated_axes": 4,
        "n_point_switch_axes": 3,
        "n_supported_switch_axes": 2,
        "n_uncertainty_unresolved_switch_axes": 0,
    }
    assert fam["ANTHROPOGENIC_PROXIMITY"] == {
        "context_family": "ANTHROPOGENIC_PROXIMITY",
        "n_programmes": 1,
        "n_programmes_with_point_switch": 1,
        "n_programmes_with_supported_switch": 0,
        "n_repeated_axes": 1,
        "n_point_switch_axes": 1,
        "n_supported_switch_axes": 0,
        "n_uncertainty_unresolved_switch_axes": 1,
    }


def test_v11_does_not_promote_family_differences_or_spatial_causality():
    result = _build()
    assert result["status"] == "CONTEXT_DRIVER_DECOMPOSITION_READY_NO_FAMILY_COMPARISON"
    assert "programme_is_the_independent_biological_unit" in result["claim_ceiling"]
    assert "no_statistical_test_of_context_family_differences" in result["claim_ceiling"]
    assert "spatial_mosaics_are_not_promoted_to_causal_driver_effects" in result["claim_ceiling"]
    assert "point_sign_switch_is_not_uncertainty_supported_reversal" in result["claim_ceiling"]


def test_v11_frozen_readout_matches_builder_summary():
    result = _build()
    frozen = json.loads(
        (ROOT / "data" / "SCH_H2_CONTEXT_DRIVER_READOUT_V11.json").read_text(
            encoding="utf-8"
        )
    )
    for key in frozen:
        assert result[key] == frozen[key]

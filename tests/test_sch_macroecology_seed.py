import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEED = ROOT / "data" / "SCH_MACROECOLOGY_CLUSTER_SEED_V1.csv"
READOUT = ROOT / "data" / "SCH_MACROECOLOGY_CLUSTER_SEED_READOUT_V1.json"
CASE_TEMPLATE = ROOT / "data" / "SCH_MACROECOLOGY_CONTEXT_CASE_TEMPLATE_V1.csv"
SCHEMA = ROOT / "docs" / "SCH_MACROECOLOGY_SCHEMA_V1.md"
SCRIPT = ROOT / "scripts" / "build_sch_macroecology_seed_readout.py"


def _build():
    spec = importlib.util.spec_from_file_location("sch_macro_seed", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod.build(SEED)


def test_macroecology_seed_preserves_16_independent_clusters():
    with SEED.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 16
    assert len({row["cluster_id"] for row in rows}) == 16
    assert {row["coding_generation"] for row in rows} == {"LEGACY_PATTERN_SEED"}


def test_macroecology_outcomes_are_nonexclusive_and_fail_closed():
    built = _build()
    assert built["conflict_detected_counts"] == {"NO": 2, "UNRESOLVED": 8, "YES": 6}
    assert built["alignment_detected_counts"] == {"NO": 6, "UNRESOLVED": 8, "YES": 2}
    assert built["context_shift_detected_counts"] == {"UNRESOLVED": 8, "YES": 8}
    assert built["compromise_detected_counts"] == {"UNRESOLVED": 15, "YES": 1}
    assert built["cancellation_detected_counts"] == {"UNRESOLVED": 15, "YES": 1}


def test_seed_exposes_crosscutting_ecological_structure_without_promoting_it():
    built = _build()
    assert built["antagonist_involved_counts"] == {"NO": 4, "YES": 12}
    assert built["conflict_by_antagonist_seed_crosstab"] == {
        "NO": {"NO": 2},
        "YES": {"NO": 1, "YES": 5},
    }
    assert built["context_shift_yes_antagonist_counts"] == {"NO": 1, "YES": 7}
    assert built["status"] == "SEED_SCHEMA_VALIDATED_NOT_INFERENTIAL_MACRO_SAMPLE"
    assert "not_sign_independent_macroecology_sample" in built["claim_ceiling"]
    assert "not_natural_prevalence" in built["claim_ceiling"]


def test_committed_macroecology_seed_readout_is_reproducible():
    assert _build() == json.loads(READOUT.read_text(encoding="utf-8"))


def test_context_case_template_preserves_nested_contexts():
    with CASE_TEMPLATE.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = set(reader.fieldnames or ())
    assert rows == []
    for required in (
        "case_id",
        "cluster_id",
        "population_or_site",
        "year_or_season",
        "treatment_or_consumer_regime",
        "conflict_detected",
        "context_shift_from_reference",
        "effect_covariance",
        "latitude",
        "longitude",
        "macro_design_eligible",
    ):
        assert required in fields


def test_schema_freezes_sign_independent_eligibility_and_four_hypotheses():
    text = SCHEMA.read_text(encoding="utf-8")
    assert "Sign-independent eligibility rule" in text
    assert "Positive-only inclusion is prohibited" in text
    assert "pollinator-antagonist macroecology" in text
    assert "matched comparator search" in text
    assert "H1 — ecological structure within pollinator-antagonist systems predicts opposition" in text
    assert "H2 — conflict geometry changes across ecological context" in text
    assert "H3 — opposing components can hide behind weak net selection" in text
    assert "H4 — design predicts identification ceiling" in text
    assert "FULL_MACRO_SAMPLE = NOT_YET_CONSTRUCTED" in text

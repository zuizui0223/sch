from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "empirical" / "one_trait_shared_cue" / "EVOLUTIONARY_OUTCOME_EVIDENCE_V1.csv"
PROTOCOL = ROOT / "empirical" / "one_trait_shared_cue" / "EVOLUTIONARY_OUTCOME_PROTOCOL_V1.md"
READOUT = ROOT / "empirical" / "one_trait_shared_cue" / "EVOLUTIONARY_OUTCOME_READOUT_V1.md"
CHAPTERS = ROOT / "docs" / "CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING.md"
FRAMEWORK = ROOT / "manuscript" / "MANUSCRIPT_SHARED_CUE_FRAMEWORK.md"
PUBLICATION_LEDGER = ROOT / "docs" / "PUBLICATION_MATERIAL_LEDGER.md"


def _rows() -> list[dict[str, str]]:
    with AUDIT.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_outcome_audit_preserves_eight_anchors_and_four_targeted_additions() -> None:
    rows = _rows()
    assert len(rows) == 12
    assert {row["study"] for row in rows}.issuperset({
        "Sasidharan_et_al_2023",
        "Theis_Adler_2012",
        "Page_et_al_2014",
        "Junker_Bluethgen_2010",
        "Knauer_Bakhtiari_Schiestl_2018",
        "Kessler_et_al_2015",
        "Perez_Barrales_2013",
        "Theis_et_al_2014",
    })
    assert {row["study"] for row in rows}.issuperset({
        "Kessler_et_al_2013",
        "Torang_Ehrlen_Agren_2008",
        "Agren_et_al_2013",
        "Ramos_Schiestl_2019",
    })
    assert all(row["positive_recovery"] for row in rows)
    assert all(row["claim_ceiling"] for row in rows)


def test_outcomes_are_recovered_without_promoting_lineage_branching() -> None:
    rows = _rows()
    assert sum(row["compromise_maintenance"] == "DIRECT_OBSERVATIONAL_STABILIZING" for row in rows) == 1
    assert sum(row["polymorphism_maintenance"].startswith("DIRECT") for row in rows) == 2
    assert sum(row["population_differentiation"].startswith("DIRECT") for row in rows) == 3
    assert all(row["lineage_branching"] == "NOT_EVALUABLE" for row in rows)
    assert sum(row["directional_specialization"] == "LOCAL_DIRECTION_ONLY" for row in rows) == 1
    assert sum(row["cue_modularization"].startswith("DIRECT") for row in rows) == 3


def test_protocol_and_readout_define_fail_closed_outcome_classes() -> None:
    protocol = PROTOCOL.read_text(encoding="utf-8")
    readout = READOUT.read_text(encoding="utf-8")
    framework = FRAMEWORK.read_text(encoding="utf-8")
    for token in (
        "Integrated compromise maintenance",
        "Directional specialization",
        "Polymorphism maintenance",
        "Population differentiation",
        "Lineage branching",
        "Cue modularization",
    ):
        assert token in protocol
    assert "observational interior compromise" in readout
    assert "lineage branching/specialization" in readout
    assert "An endpoint shift is directional specialization, not evolutionary branching." in framework


def test_chapter_sequence_keeps_estimands_and_positive_recovery_separate() -> None:
    text = CHAPTERS.read_text(encoding="utf-8")
    assert "Chapter 1 — SCH" in text
    assert "Chapter 2 — BITA" in text
    assert "Delta_AD W = rho_delta - iota_delta - kappa_delta" in text
    assert "share biological motivation but not estimands" in text
    assert "report positively how far current data recover" in text


def test_publication_ledger_admits_outcomes_without_changing_coverage_gate() -> None:
    text = PUBLICATION_LEDGER.read_text(encoding="utf-8")
    assert "12-source primary audit" in text
    assert "lineage branching untested" in text
    assert "Do not insert them into the frozen four-field coverage count" in text

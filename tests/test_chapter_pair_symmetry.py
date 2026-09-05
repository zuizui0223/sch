from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "SCH_BITA_SYMMETRY_CONTRACT_V1.md"
POSITIONING = ROOT / "docs" / "CHAPTER_1_TO_BITA_CHAPTER_2_POSITIONING_V2.md"
CH1 = ROOT / "manuscript" / "MANUSCRIPT_TRAIT_BALANCE_V1.md"
EVIDENCE_READOUT = ROOT / "empirical" / "one_trait_shared_cue" / "EVOLUTIONARY_OUTCOME_READOUT_V1.md"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_chapter_pair_uses_one_shared_architecture_interface() -> None:
    contract = _text(CONTRACT)
    for token in (
        "SCH / Chapter 1 — BALANCE",
        "BITA / Chapter 2 — DIFFERENTIATION",
        "z*     = argmin_z L_S(z)",
        "L_S*   = L_S(z*)",
        "Delta_arch = R - K",
        "R = s L_S*",
    ):
        assert token in contract, token


def test_chapter1_general_model_is_not_defined_by_pollination_defence() -> None:
    chapter = _text(CH1)
    assert "what is the best phenotype available while the functions are still forced to share one trait axis?" in chapter
    assert "Cue overlap is therefore a mechanism that shapes the one-axis fitness surface" in chapter
    assert "not the general definition of Chapter 1" in chapter
    assert "## 6. Handoff to BITA Chapter 2" in chapter


def test_quadratic_chapter1_output_matches_chapter2_input() -> None:
    positioning = _text(POSITIONING)
    assert "L_S* = [w1w2/(w1+w2)](theta1-theta2)^2" in positioning
    assert "R = s L_S*" in positioning
    assert "This makes the sister relationship substantive rather than rhetorical" in positioning


def test_existing_sch_evidence_ceiling_is_preserved() -> None:
    evidence = _text(EVIDENCE_READOUT)
    assert "Integrated compromise" in evidence
    assert "private-cue evolution from a shared cue:     0 direct sources" in evidence
    assert "lineage branching/specialization:            0 direct sources" in evidence
    chapter = _text(CH1)
    assert "does not yet support a cross-system quantitative distribution of `z*` or `L_S*`" in chapter
    assert "L4 therefore remains `NOT_EVALUABLE` rather than negative" in chapter


def test_symmetry_keeps_historical_claims_fail_closed() -> None:
    contract = _text(CONTRACT)
    for token in (
        "partial cue decoupling\n!= historical origin of a new module",
        "positive multi-trait interaction\n!= historical splitting",
        "structural differentiation\n!= functional independence",
        "route or case recurrence\n!= prevalence",
    ):
        assert token in contract, token

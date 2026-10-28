"""Keep the ecological flagship publishable without silently promoting causal claims."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.audit_sch_amnat_major_article_science import (
    PAPER, FIGURE_MAP, build, original_biological_numbers,
)

ROOT=Path(__file__).resolve().parents[1]


def _validated():
    return build(
        PAPER.read_text(encoding="utf-8"),
        FIGURE_MAP.read_text(encoding="utf-8"),
    )


def test_major_article_scope_and_words_are_now_within_official_guidelines():
    a=_validated()
    assert a["target_journal"]=="The American Naturalist"
    assert a["abstract_whitespace_word_proxy"]<=200
    assert a["full_markdown_whitespace_word_proxy"]<=7500
    assert a["manuscript_before_literature_cited_whitespace_word_proxy"]<7000
    assert a["references_are_excluded_from_soft_major_article_prose_gate"]
    assert a["abstract_whitespace_word_proxy"]<195
    assert a["figure_map_described_figures"]==5
    assert a["new_ecological_synthesis_tables_in_manuscript"]==1
    assert a["figure_map_described_figures"]+a["new_ecological_synthesis_tables_in_manuscript"]==6
    assert a["submission_ready"] is False
    assert a["status"].endswith("NOT_YET_SUBMISSION_READY")


def test_important_original_biological_effects_are_directly_source_anchored():
    n=original_biological_numbers()
    assert n["Gymnadenia_fixed_herbivory_open_hand_beta"]==[.094,-.066]
    assert n["Lythrum_control_clipped_inflorescence_mean"]==[5.4,8.0]
    assert n["Lythrum_control_clipped_inflorescence_selection_beta"]==[.47,.20]
    assert n["Brassica_butterfly_oviposition_corolla_beta"]==.45
    assert n["Brassica_corolla_seed_selection_all_regimes"]==[.22,.22,.26]
    assert n["Pedicularis_attack_site_interaction_chi2"]==36.782
    assert n["Pedicularis_final_seed_site_interaction_source_p"]=="0.4265"


def test_no_new_independent_fictitious_cluster_or_causal_optima():
    r=_validated()
    assert r["original_16_cluster_ledger_unchanged"]
    c=r["science_claim_boundary"]
    for token in (
        "sign_of_receiver_attraction_is_not_sign_of_final_seed_fitness_selection",
        "phenotype_change_not_identical_to_selection_gradient_change",
        "cross_endpoint_nondetection_not_effect_equality",
        "trait_and_consumer_z_x_P_x_G_factorial_outcome_absent",
        "no_empirical_SCH_L_or_Slk_architecture_value",
    ):
        assert token in c
    text=PAPER.read_text(encoding="utf-8")
    assert "These alternatives are hypotheses" in text
    assert "not replications of one mechanism" in text
    assert "not a pooled effect" in text
    assert "A shared oviposition cue need not produce negative net selection" not in text or "net selection" in text


@pytest.mark.parametrize(("bad","reason"),[
    ("## Abstract\n"+"too many words "*300,"abstract"),
    ("## 13. Filler\n"+"word "*1800,"word target"),
])
def test_journal_length_budget_fails_closed_for_unbounded_source_additions(bad,reason):
    m=PAPER.read_text(encoding="utf-8")
    fig=FIGURE_MAP.read_text(encoding="utf-8")
    if bad.startswith("## Abstract"):
        m=m.replace("## Abstract\n",bad+"\n",1)
    else:
        # The added material must enter article PROSE, not be appended to
        # bibliography after the current final Literature Cited heading.
        m=m.replace("## Literature Cited\n",bad+"\n## Literature Cited\n",1)
    with pytest.raises(ValueError,match=reason):
        build(m,fig)


def test_missing_falsifier_and_missing_table_are_not_submittable_as_science():
    m=PAPER.read_text(encoding="utf-8")
    f=FIGURE_MAP.read_text(encoding="utf-8")
    with pytest.raises(ValueError,match="ecological Table"):
        build(m.replace("Context-sensitive link","Unknown"),f)
    with pytest.raises(ValueError,match="missing ecological causal-ceiling"):
        build(m.replace("none can be promoted to a measured L","claim of L established"),f)


def test_camera_ready_figures_and_journal_bibliography_remain_explicitly_pending():
    remaining=_validated()["remaining_before_submission"]
    assert any("camera_ready" in s for s in remaining)
    assert any("literature_cited" in s for s in remaining)
    assert any("source-by-source" in s for s in remaining)

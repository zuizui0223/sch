from scripts.classify_ficus_same_code_receiver import Interval, classify_same_code_receiver


def test_interception_requires_direct_positive_npfw_code_response() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.62, 0.78),
        npfw_code_directional=Interval(0.58, 0.72),
        npfw_code_equivalence=Interval(0.59, 0.71),
        npfw_positive_control=Interval(0.64, 0.80),
    )
    assert decision.status == "SAME_CODE_INTERCEPTION"


def test_behavioral_nonresponse_requires_equivalence_and_working_positive_control() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code_directional=Interval(0.42, 0.59),
        npfw_code_equivalence=Interval(0.44, 0.57),
        npfw_positive_control=Interval(0.61, 0.77),
        equivalence_margin=0.10,
    )
    assert decision.status == "BEHAVIORAL_NONRESPONSE_EQUIVALENT"
    assert "not chemical imperceptibility" in decision.claim_ceiling
    assert decision.directional_interval_contract.startswith("95pct")
    assert decision.equivalence_interval_contract.startswith("90pct")


def test_nonsignificant_wide_interval_is_not_private() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code_directional=Interval(0.31, 0.69),
        npfw_code_equivalence=Interval(0.34, 0.66),
        npfw_positive_control=Interval(0.61, 0.77),
    )
    assert decision.status == "INCONCLUSIVE_SAME_CODE_RESPONSE"


def test_failed_npfw_positive_control_invalidates_nonresponse() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code_directional=Interval(0.43, 0.57),
        npfw_code_equivalence=Interval(0.45, 0.55),
        npfw_positive_control=Interval(0.42, 0.59),
    )
    assert decision.status == "NPFW_ASSAY_NOT_VALIDATED"


def test_direct_avoidance_is_separate_from_behavioral_privacy() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code_directional=Interval(0.22, 0.43),
        npfw_code_equivalence=Interval(0.24, 0.41),
        npfw_positive_control=Interval(0.61, 0.77),
    )
    assert decision.status == "SAME_CODE_AVOIDANCE"


def test_failed_pollinator_replication_blocks_same_code_promotion() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.45, 0.58),
        npfw_code_directional=Interval(0.62, 0.75),
        npfw_code_equivalence=Interval(0.64, 0.73),
        npfw_positive_control=Interval(0.65, 0.80),
    )
    assert decision.status == "POLLINATOR_CODE_NOT_REPLICATED"
    assert not decision.pollinator_code_validated


def test_95pct_directional_interval_controls_interception_not_narrower_equivalence_interval() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.62, 0.78),
        npfw_code_directional=Interval(0.49, 0.64),
        npfw_code_equivalence=Interval(0.52, 0.61),
        npfw_positive_control=Interval(0.64, 0.80),
    )
    # A narrower interval that happens to lie mostly above 0.5 cannot replace
    # the predeclared 95% directional interval, and it is not inside [0.4, 0.6].
    assert decision.status == "INCONCLUSIVE_SAME_CODE_RESPONSE"


def test_legacy_single_interval_path_remains_available_but_is_not_the_new_contract() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code=Interval(0.44, 0.57),
        npfw_positive_control=Interval(0.61, 0.77),
    )
    assert decision.status == "BEHAVIORAL_NONRESPONSE_EQUIVALENT"

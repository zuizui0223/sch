from scripts.classify_ficus_same_code_receiver import Interval, classify_same_code_receiver


def test_interception_requires_direct_positive_npfw_code_response() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.62, 0.78),
        npfw_code=Interval(0.58, 0.72),
        npfw_positive_control=Interval(0.64, 0.80),
    )
    assert decision.status == "SAME_CODE_INTERCEPTION"


def test_behavioral_nonresponse_requires_equivalence_and_working_positive_control() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code=Interval(0.44, 0.57),
        npfw_positive_control=Interval(0.61, 0.77),
        equivalence_margin=0.10,
    )
    assert decision.status == "BEHAVIORAL_NONRESPONSE_EQUIVALENT"
    assert "not chemical imperceptibility" in decision.claim_ceiling


def test_nonsignificant_wide_interval_is_not_private() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code=Interval(0.31, 0.69),
        npfw_positive_control=Interval(0.61, 0.77),
    )
    assert decision.status == "INCONCLUSIVE_SAME_CODE_RESPONSE"


def test_failed_npfw_positive_control_invalidates_nonresponse() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code=Interval(0.45, 0.55),
        npfw_positive_control=Interval(0.42, 0.59),
    )
    assert decision.status == "NPFW_ASSAY_NOT_VALIDATED"


def test_direct_avoidance_is_separate_from_behavioral_privacy() -> None:
    decision = classify_same_code_receiver(
        pollinator_code=Interval(0.63, 0.79),
        npfw_code=Interval(0.22, 0.43),
        npfw_positive_control=Interval(0.61, 0.77),
    )
    assert decision.status == "SAME_CODE_AVOIDANCE"

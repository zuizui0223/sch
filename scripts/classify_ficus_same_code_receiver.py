"""Fail-closed classifier for matched Ficus pollinator/NPFW chemical-code assays.

The classifier is intentionally behavioural. It never turns a nonsignificant
NPFW response into evidence that the cue is chemically imperceptible. A
behavioural nonresponse is supported only when (1) the pollinator code is
replicated, (2) the NPFW assay has a working host-odour positive control, and
(3) the NPFW *equivalence* interval lies wholly inside a predeclared zone around
no preference.

Directional response and equivalence are deliberately allowed to use different
intervals. The registered SCH planner uses a 95% interval for attraction or
avoidance and a 90% interval for equivalence. Reusing one interval for both
questions is supported only as a legacy compatibility path and should not be
used for new prospective assays.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import argparse
import json
from pathlib import Path


@dataclass(frozen=True)
class Interval:
    low: float
    high: float

    def validate(self, name: str) -> None:
        if not (0.0 <= self.low <= self.high <= 1.0):
            raise ValueError(f"{name} must satisfy 0 <= low <= high <= 1")


@dataclass(frozen=True)
class SameCodeDecision:
    status: str
    pollinator_code_validated: bool
    npfw_positive_control_validated: bool
    equivalence_zone: tuple[float, float]
    claim_ceiling: str
    directional_interval_contract: str = "95pct_interval_for_interception_or_avoidance"
    equivalence_interval_contract: str = "90pct_interval_for_behavioral_equivalence"


def _resolve_npfw_intervals(
    *,
    npfw_code: Interval | None,
    npfw_code_directional: Interval | None,
    npfw_code_equivalence: Interval | None,
) -> tuple[Interval, Interval]:
    """Resolve explicit prospective intervals, retaining a legacy fallback."""
    directional = npfw_code_directional or npfw_code
    equivalence = npfw_code_equivalence or npfw_code
    if directional is None or equivalence is None:
        raise ValueError(
            "provide npfw_code_directional and npfw_code_equivalence for new assays "
            "(or legacy npfw_code to reuse one interval for both questions)"
        )
    return directional, equivalence


def classify_same_code_receiver(
    *,
    pollinator_code: Interval,
    npfw_positive_control: Interval,
    npfw_code: Interval | None = None,
    npfw_code_directional: Interval | None = None,
    npfw_code_equivalence: Interval | None = None,
    null_preference: float = 0.5,
    equivalence_margin: float = 0.10,
) -> SameCodeDecision:
    """Classify one matched receiver assay from uncertainty intervals.

    ``pollinator_code`` and ``npfw_positive_control`` should be directional
    intervals on the declared choice-probability scale. For prospective assays,
    ``npfw_code_directional`` should be the directional interval used to test
    attraction/avoidance, while ``npfw_code_equivalence`` should be the interval
    used for the predeclared equivalence question. The registered planning
    contract is 95% directional and 90% equivalence.

    The function does not calculate intervals. The experimental analysis must
    propagate tree/day/batch dependence before calling it.
    """
    directional, equivalence = _resolve_npfw_intervals(
        npfw_code=npfw_code,
        npfw_code_directional=npfw_code_directional,
        npfw_code_equivalence=npfw_code_equivalence,
    )
    for name, interval in (
        ("pollinator_code", pollinator_code),
        ("npfw_code_directional", directional),
        ("npfw_code_equivalence", equivalence),
        ("npfw_positive_control", npfw_positive_control),
    ):
        interval.validate(name)
    if not (0.0 < null_preference < 1.0):
        raise ValueError("null_preference must lie strictly between 0 and 1")
    if not (0.0 < equivalence_margin < min(null_preference, 1.0 - null_preference)):
        raise ValueError("equivalence_margin is incompatible with the null preference")

    eq_low = null_preference - equivalence_margin
    eq_high = null_preference + equivalence_margin
    pollinator_ok = pollinator_code.low > null_preference
    npfw_control_ok = npfw_positive_control.low > null_preference

    if not pollinator_ok:
        return SameCodeDecision(
            status="POLLINATOR_CODE_NOT_REPLICATED",
            pollinator_code_validated=False,
            npfw_positive_control_validated=npfw_control_ok,
            equivalence_zone=(eq_low, eq_high),
            claim_ceiling="The declared chemical code was not validated in the current assay; no receiver-specific inference is allowed.",
        )
    if not npfw_control_ok:
        return SameCodeDecision(
            status="NPFW_ASSAY_NOT_VALIDATED",
            pollinator_code_validated=True,
            npfw_positive_control_validated=False,
            equivalence_zone=(eq_low, eq_high),
            claim_ceiling="NPFW nonresponse is uninterpretable because the positive-control host cue did not elicit a validated response.",
        )
    if directional.low > null_preference:
        return SameCodeDecision(
            status="SAME_CODE_INTERCEPTION",
            pollinator_code_validated=True,
            npfw_positive_control_validated=True,
            equivalence_zone=(eq_low, eq_high),
            claim_ceiling="Direct behavioural evidence that both receiver guilds are attracted to the same resolved chemical code; this is contemporary interception, not a historical transition.",
        )
    if directional.high < null_preference:
        return SameCodeDecision(
            status="SAME_CODE_AVOIDANCE",
            pollinator_code_validated=True,
            npfw_positive_control_validated=True,
            equivalence_zone=(eq_low, eq_high),
            claim_ceiling="Direct behavioural avoidance of the pollinator-attractive code by the NPFW; this supports receiver separation but does not by itself identify how the state evolved.",
        )
    if equivalence.low >= eq_low and equivalence.high <= eq_high:
        return SameCodeDecision(
            status="BEHAVIORAL_NONRESPONSE_EQUIVALENT",
            pollinator_code_validated=True,
            npfw_positive_control_validated=True,
            equivalence_zone=(eq_low, eq_high),
            claim_ceiling="NPFW behaviour is equivalent to no preference within the predeclared margin while its host-cue positive control works; this supports behavioural privacy at the assay scale, not chemical imperceptibility.",
        )
    return SameCodeDecision(
        status="INCONCLUSIVE_SAME_CODE_RESPONSE",
        pollinator_code_validated=True,
        npfw_positive_control_validated=True,
        equivalence_zone=(eq_low, eq_high),
        claim_ceiling="The NPFW directional interval does not establish attraction/avoidance and its equivalence interval does not lie wholly inside the no-preference zone; more information is required.",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args(argv)
    payload = json.loads(args.input_json.read_text(encoding="utf-8"))

    legacy = payload.get("npfw_code")
    directional_payload = payload.get("npfw_code_directional", legacy)
    equivalence_payload = payload.get("npfw_code_equivalence", legacy)
    if directional_payload is None or equivalence_payload is None:
        raise ValueError(
            "input requires npfw_code_directional and npfw_code_equivalence "
            "(legacy npfw_code is accepted only for compatibility)"
        )

    decision = classify_same_code_receiver(
        pollinator_code=Interval(**payload["pollinator_code"]),
        npfw_code_directional=Interval(**directional_payload),
        npfw_code_equivalence=Interval(**equivalence_payload),
        npfw_positive_control=Interval(**payload["npfw_positive_control"]),
        null_preference=float(payload.get("null_preference", 0.5)),
        equivalence_margin=float(payload.get("equivalence_margin", 0.10)),
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(asdict(decision), indent=2), encoding="utf-8")
    print(decision.status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

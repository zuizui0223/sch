from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_PRIOR_ANCHOR_FULLTEXT_MIGRATION_PREVIEW_V1.csv"
DECISIONS = ROOT / "empirical" / "prisma" / "SCH_PRISMA_V2_SCREENING_DECISIONS_V1.csv"
REGISTRY = ROOT / "evidence" / "EVIDENCE_ROLE_REGISTRY_V1.csv"


def _rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_preview_has_all_eight_prior_anchors_and_is_not_formal_adjudication() -> None:
    rows = _rows(PREVIEW)
    assert len(rows) == 8
    assert all(row["formal_systematic_status"] == "PREVIEW_ONLY_NOT_FULLTEXT_ADJUDICATION" for row in rows)
    assert len({row["record_id"] for row in rows}) == 8
    assert len({row["doi"] for row in rows}) == 8


def test_only_theis_adler_is_flagged_as_strict_four_field_candidate() -> None:
    rows = _rows(PREVIEW)
    strict = [row for row in rows if row["strict_four_field_candidate"] == "YES"]
    assert len(strict) == 1
    assert strict[0]["study"] == "Theis_Adler_2012"
    assert strict[0]["doi"] == "10.1890/11-0825.1"
    assert "STRICT_LINKED_EXPERIMENT" in strict[0]["suggested_systematic_lane"]
    assert all(
        row["suggested_systematic_lane"] == "DIRECTIONAL_OR_NEAR_PASS"
        for row in rows
        if row["study"] != "Theis_Adler_2012"
    )


def test_preview_dois_match_prior_registry_and_current_retain_overlay() -> None:
    preview = _rows(PREVIEW)
    registry = _rows(REGISTRY)
    decisions = _rows(DECISIONS)
    preview_dois = {row["doi"].lower() for row in preview}
    registry_dois = {row["doi"].lower() for row in registry}
    assert preview_dois == registry_dois
    decision_ids = {row["record_id"] for row in decisions}
    preview_ids = {row["record_id"] for row in preview}
    assert decision_ids == preview_ids
    assert all(row["screen_title_abstract"] == "RETAIN_FULLTEXT" for row in decisions)
    assert all(row["screen_fulltext"] == "" for row in decisions)


def test_claim_ceiling_preserves_each_prior_blocker() -> None:
    rows = _rows(PREVIEW)
    by_study = {row["study"]: row for row in rows}
    assert "raw table" in by_study["Theis_Adler_2012"]["prior_blocker_or_boundary"]
    assert "observational" in by_study["Theis_et_al_2014"]["prior_blocker_or_boundary"]
    assert "same-study pollination" in by_study["Page_et_al_2014"]["prior_blocker_or_boundary"]
    assert "common reproductive outcome" in by_study["Kessler_et_al_2015"]["prior_blocker_or_boundary"]
    assert "observational" in by_study["Perez_Barrales_2013"]["prior_blocker_or_boundary"]

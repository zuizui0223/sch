from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_one_trait_coverage_audit.py"
AUDIT = ROOT / "empirical" / "one_trait_shared_cue" / "ONE_TRAIT_COVERAGE_AUDIT_V1.csv"
READOUT = ROOT / "empirical" / "one_trait_shared_cue" / "ONE_TRAIT_COVERAGE_READOUT_V1.md"
FRAMEWORK = ROOT / "manuscript" / "MANUSCRIPT_SHARED_CUE_FRAMEWORK.md"
MANIFEST = ROOT / "data" / "source_exports" / "SOURCE_EXPORT_MANIFEST.json"
EVIDENCE = ROOT / "evidence" / "EVIDENCE_ROLE_REGISTRY_V1.csv"
PUBLICATION_LEDGER = ROOT / "docs" / "PUBLICATION_MATERIAL_LEDGER.md"


def _module():
    spec = importlib.util.spec_from_file_location("build_one_trait_coverage_audit", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _rows() -> list[dict[str, str]]:
    with AUDIT.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def test_one_trait_audit_rebuilds_declared_counts() -> None:
    summary = _module().run()
    assert summary["independent_cluster_count"] == 25
    assert summary["A_route_cluster_count"] == 8
    assert summary["dual_A_route_cluster_count"] == 5
    assert summary["strict_coverage_pass_count"] == 1
    assert summary["strict_coverage_pass_clusters"] == ["Theis_Adler_2012_Cucurbita"]
    assert summary["bita_source_commit"] == "20cd517b9b482e7e3e232a5088ae9c6422286418"


def test_high_information_matrix_is_not_misreported_as_complete_one_trait_universe() -> None:
    summary = _module().run()
    assert summary["high_information_system_count"] == 16
    assert summary["high_information_strict_pass_count"] == 0
    assert summary["theis_2012_present_in_high_information_matrix"] is False


def test_a_route_clusters_have_manual_fail_closed_adjudications() -> None:
    rows = _rows()
    candidates = [row for row in rows if row["audit_status"] != "NOT_EVALUABLE_NO_A_ROUTE"]
    assert len(candidates) == 8
    assert all(row["source_basis"] for row in candidates)
    assert all(row["audit_status"] in {"FAIL", "PASS_DIRECTIONAL_ONLY"} for row in candidates)


def test_readout_and_framework_keep_one_and_two_trait_estimands_separate() -> None:
    readout = READOUT.read_text(encoding="utf-8")
    framework = FRAMEWORK.read_text(encoding="utf-8")
    assert "Delta_A W = Delta_A M - Delta_A G - Delta_A C" in readout
    assert "coverage existence" in readout
    assert "S_A = M_A - G_A" in framework
    assert "requires neither a second trait `D` nor `Delta_AD W`" in framework
    assert "Selective consumer intervention is one route" in framework


def test_frozen_source_exports_match_declared_hashes() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for relative_path, declaration in manifest["artifacts"].items():
        observed = hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()
        assert observed == declaration["sha256"]


def test_evidence_spine_preserves_claim_ceilings() -> None:
    with EVIDENCE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert {row["study"] for row in rows} == {
        "Sasidharan_et_al_2023",
        "Theis_Adler_2012",
        "Page_et_al_2014",
        "Junker_Bluethgen_2010",
        "Knauer_Bakhtiari_Schiestl_2018",
        "Kessler_et_al_2015",
        "Perez_Barrales_2013",
        "Theis_et_al_2014",
    }
    theis = next(row for row in rows if row["study"] == "Theis_Adler_2012")
    assert theis["current_coverage_status"] == "PASS_DIRECTIONAL_ONLY"
    assert "unavailable focal raw data" in theis["prohibited_use"]


def test_publication_ledger_preserves_paper_fork_and_missing_gate() -> None:
    text = PUBLICATION_LEDGER.read_text(encoding="utf-8")
    lower = text.lower()
    assert "existing-study integration plus shared-cue framework" in lower
    assert "paired-channel measurement gap" in lower
    assert "No pooled effect is authorized" in text
    assert "A manipulated" in text
    assert "common reproductive outcome" in text

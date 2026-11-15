"""No fake source PDF, unchecked source filenames, or invented S5/S6."""
from scripts.probe_sch_trunschke2017_suppinfo import (
    PAPER_DOI,SUPPLEMENT,SOURCE_HOSTS,URLS,MAX_BYTES,
)

def test_official_pinned_paper_and_supplement_only():
    assert PAPER_DOI=="10.1111/nph.14479"
    assert SUPPLEMENT=="nph14479-sup-0001-SupInfo.pdf"
    assert len(URLS)==4
    assert all("nph.14479" in link and SUPPLEMENT in link for link in URLS)
    assert all(any(host in link for host in SOURCE_HOSTS) for link in URLS)
    assert MAX_BYTES<=2_000_000

def test_document_does_not_relabel_dryad_metadata_as_supplement():
    from pathlib import Path
    src=Path("scripts/probe_sch_trunschke2017_suppinfo.py").read_text()
    assert "S5_data_extracted\":False" in src
    assert "S6_data_extracted\":False" in src
    assert "independent_species_level_refit_executed\":False" in src

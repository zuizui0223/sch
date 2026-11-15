"""Source guards for original 2024 JPE milkweed Appendix II."""
from scripts.ingest_sch_milkweed_2024_original_appendix import (
 DOI,ARTICLE_ID,APPENDIX_II_GALLEY_ID,CANDIDATES,classify,MAX_BYTES,
)

def test_pinned_journal_article_and_appendix():
    assert DOI=="10.26786/1920-7603(2024)758"
    assert ARTICLE_ID==758
    assert APPENDIX_II_GALLEY_ID==478
    assert len(CANDIDATES)==4
    assert all("/article/" in link and "/758/478" in link
               and ("pollinationecology.org" in link) for link in CANDIDATES)
    assert MAX_BYTES<=4_000_000

def test_reject_login_html_pdfs_and_unknown_binary_as_individual_data():
    assert classify(b"<!DOCTYPE html><html><body>Login</body></html>")=="HTML_NOT_DATA"
    assert classify(b"%PDF-1.5"+b"0"*100)=="PDF_NOT_DIRECT_DATA"
    assert classify(b"\0"*400)=="BINARY_UNKNOWN"
    assert classify(bytes.fromhex("d0cf11e0a1b11ae1")+b"\x00"*500)=="XLS"
    assert classify(b"trait,plant_id,fruit\n1,2,3\n")=="TEXT_DELIMITED_CANDIDATE"

def test_standalone_ingress_does_not_report_unfitted_result():
    from pathlib import Path
    s=Path("scripts/ingest_sch_milkweed_2024_original_appendix.py").read_text()
    assert '"new_individual_plant_reanalysis_executed":False' in s
    assert '"selection_sign_or_stage_conversion_estimated":False' in s

"""Try official publisher routes for Trunschke et al. 2017 Supporting Information.

This is a *single source-access audit*, not an ecological result. No PDF bytes
are committed to git. A valid PDF allows page heading checks for Tables S5/S6.
Do not silently substitute the source DOI article PDF for the supplement.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import io
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path

PAPER_DOI="10.1111/nph.14479"
SUPPLEMENT="nph14479-sup-0001-SupInfo.pdf"
SOURCE_HOSTS=("nph.onlinelibrary.wiley.com","onlinelibrary.wiley.com")
URLS=(
    f"https://{SOURCE_HOSTS[0]}/doi/suppl/{PAPER_DOI}/supinfo/{SUPPLEMENT}",
    f"https://{SOURCE_HOSTS[1]}/doi/suppl/{PAPER_DOI}/supinfo/{SUPPLEMENT}",
    f"https://{SOURCE_HOSTS[0]}/action/downloadSupplement?doi=10.1111%2Fnph.14479&file={SUPPLEMENT}",
    f"https://{SOURCE_HOSTS[1]}/action/downloadSupplement?doi=10.1111%2Fnph.14479&file={SUPPLEMENT}",
)
SOURCE_INFO=f"https://{SOURCE_HOSTS[0]}/doi/supinfo/{PAPER_DOI}"
MAX_BYTES=2_000_000
MIN_PDF_BYTES=30_000
USER_AGENT="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/129.0.0.0 Safari/537.36"

def probe(url):
    request=Request(url,headers={"User-Agent":USER_AGENT,
          "Accept":"application/pdf,application/octet-stream;q=0.9,*/*;q=0.5",
          "Referer":f"https://{SOURCE_HOSTS[0]}/doi/full/{PAPER_DOI}"})
    try:
        with urlopen(request,timeout=18) as resp:
            raw=resp.read(MAX_BYTES+1)
            info={"url":url,"http":resp.status,"final_url":resp.geturl(),
                  "content_type":resp.headers.get("Content-Type",""),
                  "bytes":len(raw)}
        if len(raw)>MAX_BYTES:
            info["status"]="OVERSIZE_REJECTED"
            return info,None
        if not (raw[:16].lstrip().startswith(b"%PDF-") and len(raw)>=MIN_PDF_BYTES):
            info["status"]="NOT_PDF_REJECTED"
            info["first_bytes_hex"]=raw[:12].hex()
            return info,None
        info["status"]="VALID_PDF_BINARY"
        info["sha256"]=hashlib.sha256(raw).hexdigest()
        return info,raw
    except HTTPError as exc:
        return {"url":url,"http":exc.code,"status":"HTTP_ERROR"},None
    except (URLError,TimeoutError,ValueError,ConnectionError) as exc:
        return {"url":url,"status":"FETCH_ERROR_"+type(exc).__name__,
                "error":str(exc)[:120]},None

def pdf_inspect(raw:bytes):
    import fitz
    book=fitz.open(stream=raw,filetype="pdf")
    out={"n_pages":len(book),"pages_with_S5":[],"pages_with_S6":[]}
    for i,page in enumerate(book):
        txt=page.get_text("text",sort=True)
        for k in ("S5","S6"):
            # only true Table S5/S6 headings rather than in-text citations
            if re.search(r"\bTable\s+S\s*"+k[1:]+r"\b",txt,re.I):
                out["pages_with_"+k].append(i+1)
        if i==0:
            out["first_page_text_excerpt"]=txt[:300]
    return out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,default=Path("artifacts/trunschke2017_suppinfo_access.json"))
    a=p.parse_args(); a.out.parent.mkdir(parents=True,exist_ok=True)
    results=[];real_pdf=None;success_url=None
    for url in URLS:
        result,raw=probe(url)
        results.append(result)
        if raw is not None:
            real_pdf=raw;success_url=url;break
    # if direct links fail, test the official publisher's supinfo landing HTML,
    # but never treat it as a PDF.
    landing=None
    if real_pdf is None:
        landing,_=probe(SOURCE_INFO)
        results.append(landing)
    receipt={
      "paper_doi":PAPER_DOI,"expected_official_filename":SUPPLEMENT,
      "publisher_routes_checked":results,
      "source_pdf_verified":real_pdf is not None,
      "source_pdf_analyzed":False,
      "S5_data_extracted":False,"S6_data_extracted":False,
      "independent_species_level_refit_executed":False,
      "access_status":"PUBLISHER_SUPINFO_ACCESS_UNRESOLVED"}
    if real_pdf is not None:
        receipt["source_pdf_inspection"]=pdf_inspect(real_pdf)
        receipt["source_pdf_analyzed"]=True
        receipt["verified_source_url"]=success_url
        receipt["access_status"]="ORIGINAL_PUBLISHER_SUPINFO_VERIFIED_S5S6_PAGE_CHECK_ONLY"
    a.out.write_text(json.dumps(receipt,indent=2,ensure_ascii=False,sort_keys=True)+"\n",
                     encoding="utf-8")
    print(json.dumps(receipt,indent=2,ensure_ascii=False,sort_keys=True))

if __name__=="__main__":
    main()

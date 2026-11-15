"""Retrieve the 2024 Asclepias individual-plant appendix from its official OJS journal.

Source: García et al. (2024) Journal of Pollination Ecology, DOI
10.26786/1920-7603(2024)758; Appendix II galley 478.
Only exact journal-linked routes are allowed. This is a SOURCE probe, not
a source-independent biological analysis. Full data may be published under
original journal copyright; DO NOT commit raw publication tables to GitHub.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

DOI="10.26786/1920-7603(2024)758"
ORIGINS=["https://www.pollinationecology.org","https://pollinationecology.org"]
BASE_PATH="/index.php/jpe/article"
ARTICLE_ID=758
APPENDIX_II_GALLEY_ID=478
CANDIDATES=[
    f"{origin}{BASE_PATH}/download/{ARTICLE_ID}/{APPENDIX_II_GALLEY_ID}"
    for origin in ORIGINS
] + [
    f"{origin}{BASE_PATH}/view/{ARTICLE_ID}/{APPENDIX_II_GALLEY_ID}"
    for origin in ORIGINS
]
MAX_BYTES=4_000_000
AGENT="SCH-original-milkweed-2024-source-probe/1.0"
MISSING={"","NA","N/A","nan","NaN","NULL","."}

def get(url):
    request=Request(url,headers={"User-Agent":AGENT,
        "Accept":"text/csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel,application/octet-stream,*/*"})
    with urlopen(request,timeout=24) as response:
        raw=response.read(MAX_BYTES+1)
        result={"requested":url,"final_url":response.geturl(),
                "http":response.status,
                "content_type":response.headers.get("Content-Type",""),
                "bytes":len(raw)}
    if len(raw)>MAX_BYTES or not raw:
        result["status"]="INVALID_SIZE"
        return result,None
    return result,raw

def classify(raw):
    if raw.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
        return "XLS"
    if raw.startswith(b"PK\x03\x04"):
        try:
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                names=set(z.namelist())
            if "xl/workbook.xml" in names:return "XLSX"
            if "word/document.xml" in names:return "DOCX_NOT_DIRECT_DATA"
            return "ZIP_UNRESOLVED"
        except zipfile.BadZipFile:return "INVALID_ZIP"
    if raw.lstrip()[:10].lower().startswith((b"<!doctype",b"<html",b"<head",b"<?xml")):
        return "HTML_NOT_DATA"
    if raw.startswith(b"%PDF"):
        return "PDF_NOT_DIRECT_DATA"
    head=raw[:2048]
    if b"\x00" in head:return "BINARY_UNKNOWN"
    try:
        sample=head.decode("utf-8-sig")
        if ("," in sample or "\t" in sample or ";" in sample) and "\n" in sample:
            return "TEXT_DELIMITED_CANDIDATE"
    except UnicodeError:pass
    return "UNKNOWN"

def schema(raw,kind):
    if kind in ("XLSX","XLS"):
        if kind=="XLSX":
            import openpyxl
            wb=openpyxl.load_workbook(io.BytesIO(raw),read_only=True,data_only=True)
            out=[]
            for sh in wb.worksheets:
                vals=sh.iter_rows(values_only=True)
                start=list(next(vals,()))
                out.append({
                    "sheet":sh.title,"rows_including_header":sh.max_row,
                    "n_columns":sh.max_column,
                    "headings":[str(v) if v is not None else "" for v in start][:120],
                    "sample_second_row":[str(v)[:80] if v is not None else "" for v in next(vals,())][:120]})
            wb.close()
            return out
        import xlrd
        wb=xlrd.open_workbook(file_contents=raw)
        return [{
            "sheet":sh.name,"rows_including_header":sh.nrows,
            "n_columns":sh.ncols,
            "headings":[str(v) for v in sh.row_values(0)][:120] if sh.nrows else [],
            "sample_second_row":[str(v)[:80] for v in sh.row_values(1)][:120] if sh.nrows>1 else [],
        } for sh in wb.sheets()]
    if kind=="TEXT_DELIMITED_CANDIDATE":
        s=raw.decode("utf-8-sig",errors="strict")
        dialect=csv.Sniffer().sniff(s[:min(len(s),8192)],delimiters=",\t;")
        parsed=list(csv.reader(io.StringIO(s),dialect))
        if not parsed or len(parsed[0])<3 or len(parsed)>10000:
            raise ValueError("source CSV candidate invalid")
        return [{"sheet":"text_original","rows_including_header":len(parsed),
                 "n_columns":len(parsed[0]),
                 "headings":parsed[0][:120],
                 "sample_second_row":parsed[1][:120] if len(parsed)>1 else []}]
    return []

def run(outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    receipt={"paper_doi":DOI,"source":"Journal of Pollination Ecology",
      "article_id":ARTICLE_ID,"appendix_II_galley_id":APPENDIX_II_GALLEY_ID,
      "source_url":"https://www.pollinationecology.org/index.php/jpe/article/view/758",
      "attempts":[],"source_genuine_rows_recovered":False,
      "source_genuine_fitness_outcomes_jointly_available":"NOT_CHECKED",
      "new_individual_plant_reanalysis_executed":False,
      "selection_sign_or_stage_conversion_estimated":False}
    for url in CANDIDATES:
        try:
            state,raw=get(url)
            kind=classify(raw)
            state["file_kind"]=kind
            state["status"]="OK_SOURCE_BYTES" if kind in ("XLS","XLSX","TEXT_DELIMITED_CANDIDATE") else kind
            receipt["attempts"].append(state)
            if kind not in ("XLS","XLSX","TEXT_DELIMITED_CANDIDATE"):
                continue
            data_schema=schema(raw,kind)
            if not data_schema:
                raise ValueError("No data table from reported source")
            ext={"XLS":"xls","XLSX":"xlsx","TEXT_DELIMITED_CANDIDATE":"csv"}[kind]
            dest=outdir/("original_2024_jpe_appendix_ii."+ext)
            dest.write_bytes(raw)
            receipt["source_genuine_rows_recovered"]=True
            receipt["original_file_sha256"]=hashlib.sha256(raw).hexdigest()
            receipt["original_file_bytes"]=len(raw)
            receipt["original_official_url"]=url
            receipt["original_file_kind"]=kind
            receipt["original_schema"]=data_schema
            wanted=("fruit","pollin","insert")
            joined=" ".join(" ".join(z["headings"]).lower() for z in data_schema)
            receipt["source_genuine_fitness_outcomes_jointly_available"]=all(w in joined for w in wanted)
            receipt["status"]="OFFICIAL_JPE_ORIGINAL_APPENDIX_II_BYTES_RECOVERED_SCHEMA_ONLY"
            break
        except HTTPError as e:
            receipt["attempts"].append({"requested":url,"status":f"HTTP_{e.code}"})
        except (URLError,TimeoutError,ValueError,UnicodeError,RuntimeError) as e:
            receipt["attempts"].append({"requested":url,"status":type(e).__name__,
                                        "error":str(e)[:180]})
    if not receipt["source_genuine_rows_recovered"]:
        receipt["status"]="JPE_APPENDIX_II_ORIGINAL_BYTES_NOT_RECOVERED"
    dest=outdir/"source_ingress_receipt.json"
    dest.write_text(json.dumps(receipt,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    print("BEGIN_SCH_JPE2024_SOURCE_RECEIPT")
    print(dest.read_text(encoding="utf-8"))
    print("END_SCH_JPE2024_SOURCE_RECEIPT")
    return receipt

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--outdir",type=Path,default=Path("artifacts/sch_jpe2024_plant_raw"))
    args=p.parse_args()
    run(args.outdir)

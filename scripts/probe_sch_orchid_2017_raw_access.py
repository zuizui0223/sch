"""Non-gating, source-identity-first access probe for public orchid 2017 raw data.

This is a discovery-only instrument: no source observation is imputed,
and inability to fetch authentic Dryad bytes is a BLOCKER, not a null result.
Dryad DOI 10.5061/dryad.28n72; 2017 paper DOI 10.1111/nph.14479.

It does not change any registered SCH empirical denominator.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import re
import zipfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request,urlopen

DATA_DOI="10.5061/dryad.28n72"
DOI_ID=quote("doi:"+DATA_DOI,safe="")
BASE="https://datadryad.org"
UA="SCH-orchid-2017-real-raw-source-probe/1.0"
MAX_METADATA=1_000_000
MAX_DOWNLOAD=3_000_000

def get(url,max_size,accept="*/*"):
    req=Request(url,headers={"User-Agent":UA,"Accept":accept})
    with urlopen(req,timeout=22) as r:
        raw=r.read(max_size+1)
        code=r.status
    if not raw or len(raw)>max_size:
        raise ValueError("empty or unexpectedly large response")
    return code,raw

def record_error(e):
    if isinstance(e,HTTPError):
        return f"HTTP_{e.code}"
    if isinstance(e,URLError):
        return f"URL_{type(e.reason).__name__}"
    return f"{type(e).__name__}:{str(e)[:140]}"

def json_get(url):
    _,raw=get(url,MAX_METADATA,"application/json")
    return json.loads(raw.decode("utf-8"))

def values_any(record,token):
    # HAL _embedded keys vary by API version. Accept lists of typed objects only.
    out=[]
    def walk(node):
        if isinstance(node,dict):
            for k,v in node.items():
                if token in k.lower() and isinstance(v,list):
                    out.extend(x for x in v if isinstance(x,dict))
                elif k not in ("abstract","description"):
                    walk(v)
        elif isinstance(node,list):
            for item in node:walk(item)
    walk(record)
    ids={};result=[]
    for x in out:
        v=str(x.get("id",id(x)))
        if v not in ids:
            result.append(x); ids[v]=True
    return result

def file_names(file_info):
    return str(file_info.get("path") or file_info.get("filename") or
               file_info.get("name") or "")

def is_source_excel(raw):
    return raw.startswith(bytes.fromhex("d0cf11e0a1b11ae1")) or raw.startswith(b"PK\x03\x04")

def inspect_xls(raw,filename):
    import xlrd
    b=xlrd.open_workbook(file_contents=raw)
    r=[]
    for s in b.sheets():
        rows=[]
        for i in range(min(s.nrows,4)):
            rows.append([str(x)[:120] for x in s.row_values(i)[:60]])
        r.append({"sheet":s.name,"n_source_rows_including_header":s.nrows,
                  "n_source_columns":s.ncols,"first_four_rows":rows})
    return {"source_workbook_name":filename,"sheets":r}

def run(outdir):
    outdir.mkdir(parents=True,exist_ok=True)
    report={"paper_doi":"10.1111/nph.14479","data_doi":DATA_DOI,
            "downloaded_individual_plants":False,
            "independent_fitness_model_refit":False,
            "attempted_public_metadata":[],
            "attempted_public_file_download":[],"raw_files":[]}
    urls=[f"{BASE}/api/v2/datasets/{DOI_ID}",
          f"{BASE}/api/v2/datasets/{DOI_ID}/versions"]
    found={}
    for url in urls:
        try:
            item=json_get(url)
            report["attempted_public_metadata"].append({"url":url,"status":"HTTP_200_JSON"})
            found[url]=item
        except (HTTPError,URLError,ValueError,TimeoutError) as exc:
            report["attempted_public_metadata"].append({"url":url,"status":record_error(exc)})
    version_ids=set()
    for item in found.values():
        for version in values_any(item,"versions"):
            if "id" in version:version_ids.add(str(version["id"]))
        v=item.get("version")
        if isinstance(v,dict) and "id" in v:version_ids.add(str(v["id"]))
        for k in ("versionId","version_id"):
            if item.get(k): version_ids.add(str(item[k]))
    report["version_ids_discovered"]=sorted(version_ids)
    known_files=[]
    for version_id in sorted(version_ids):
        url=f"{BASE}/api/v2/versions/{version_id}/files"
        try:
            obj=json_get(url)
            rows=values_any(obj,"files")
            report["attempted_public_metadata"].append({
                "url":url,"status":"HTTP_200_JSON","n_file_records":len(rows)})
            known_files.extend(rows)
        except (HTTPError,URLError,ValueError,TimeoutError) as exc:
            report["attempted_public_metadata"].append({"url":url,"status":record_error(exc)})
    report["available_file_metadata"]=[
        {"id":r.get("id"),"name":file_names(r),"size":r.get("size"),"digest":r.get("digest")}
        for r in known_files]
    wanted=[r for r in known_files if file_names(r).lower().endswith((".xls",".xlsx",".docx"))]
    for record in wanted:
        fid=record.get("id")
        name=file_names(record)
        if not fid or not name or "/" in name or "\\" in name:
            continue
        exact=record.get("digest")
        candidates=[f"{BASE}/api/v2/files/{fid}/download",
                    f"{BASE}/downloads/file_stream/{fid}",
                    f"{BASE}/stash/downloads/file_stream/{fid}"]
        for url in candidates:
            try:
                code,raw=get(url,MAX_DOWNLOAD)
                valid=(is_source_excel(raw) if name.lower().endswith((".xls",".xlsx")) 
                       else raw.startswith(b"PK\x03\x04"))
                if not valid:
                    raise ValueError("NOT_EXPECTED_OFFICE_FILE_MAGIC")
                sha=hashlib.sha256(raw).hexdigest()
                md5=hashlib.md5(raw).hexdigest() # archival identity only
                if exact and isinstance(exact,str):
                    v=exact.replace("md5:","").replace("sha-256:","").lower()
                    if re.fullmatch("[0-9a-f]{32}",v) and v!=md5:
                        raise ValueError("DRYAD_METADATA_MD5_MISMATCH")
                    if re.fullmatch("[0-9a-f]{64}",v) and v!=sha:
                        raise ValueError("DRYAD_METADATA_SHA256_MISMATCH")
                path=outdir/name
                path.write_bytes(raw)
                row={"name":name,"file_id":fid,"bytes":len(raw),"sha256":sha,"md5":md5,
                     "verified_against_reported_digest":bool(exact),"source_url":url}
                if name.lower().endswith((".xls",".xlsx")):
                    row.update(inspect_xls(raw,name))
                    report["downloaded_individual_plants"]=True
                report["raw_files"].append(row)
                report["attempted_public_file_download"].append({
                   "file_id":fid,"source":url,"status":"HTTP_200_VALID_OFFICE_BYTES"})
                break
            except (HTTPError,URLError,ValueError,TimeoutError) as exc:
                report["attempted_public_file_download"].append({
                   "file_id":fid,"source":url,"status":record_error(exc)})
    report["status"]=("ORIGINAL_DRYAD_XLS_ACQUIRED_SCHEMA_ONLY_NO_ANALYSIS"
         if report["downloaded_individual_plants"] else
         "DRYAD_ORIGINAL_XLS_NOT_RETRIEVED_NO_INDIVIDUAL_INFERENCE")
    dest=outdir/"public_source_access_receipt.json"
    dest.write_text(json.dumps(report,ensure_ascii=False,indent=2,sort_keys=True)+"\n",
                    encoding="utf-8")
    print("BEGIN_SCH_ORCHID_2017_ACCESS_PROBE")
    print(dest.read_text(encoding="utf-8"))
    print("END_SCH_ORCHID_2017_ACCESS_PROBE")
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--outdir",type=Path,default=Path("artifacts/sch_orchid_2017_access"))
    args=p.parse_args()
    run(args.outdir)

if __name__=="__main__":
    main()

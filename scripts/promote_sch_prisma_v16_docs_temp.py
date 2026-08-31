from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected 1 occurrence, found {n}: {old[:100]!r}")
    return text.replace(old, new, 1)


def update_ledger() -> None:
    path = Path("docs/PUBLICATION_MATERIAL_LEDGER.md")
    text = path.read_text(encoding="utf-8")
    if "## Current screening state — Batch 3 title/abstract complete under V16" in text:
        return
    pairs = [
        ("## Current screening state — Batch 3 high-information full-text closure complete under V15", "## Current screening state — Batch 3 title/abstract complete under V16"),
        ("title/abstract screened:         241", "title/abstract screened:         307"),
        ("retained for full text:          158", "retained for full text:          202"),
        ("title/abstract excluded:          83", "title/abstract excluded:         105"),
        ("unscreened:                      627", "unscreened:                      561"),
        ("full-text eligible:              158", "full-text eligible:              202"),
        ("full-text undecided:               0", "full-text undecided:              44"),
        ("### Batch-3 high-information full-text closure under V15", "### Batch-3 title/abstract closure under V16"),
        ("Batch 2 remains closed. In Batch 3, V14 retained 28 high-information reports and V15 now resolves all 28 at full text: 20 are included and eight excluded. The high-information Batch-3 full-text backlog is therefore zero. The next work object is the remaining 66 genuinely new Batch-3 title/abstract records. This does not authorize pooled effects and does not mean the 868-record screen is complete.", "Batch 2 remains closed. V15 closed all 28 high-information Batch-3 full texts. V16 now adjudicates the remaining 66 genuinely new Batch-3 title/abstract records: 44 are retained for full text and 22 excluded. Batch 3 is therefore 100/100 complete at title/abstract stage, and the current Batch-3 full-text backlog is 44. This does not authorize pooled effects and does not mean the 868-record screen is complete."),
        ("| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 627 records remain title/abstract unscreened |", "| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 561 records remain title/abstract unscreened |"),
        ("| Batch 3 high-information | 33/33 prioritized TA decisions; V15 closes all 28 retained full texts (20 include / 8 exclude) | Third systematic batch | Closed; screen remaining 66 new Batch-3 records |", "| Batch 3 | 100/100 TA decisions; V15 closes the 28 high-information full texts; V16 retains 44 additional reports | Third systematic batch | Full-text adjudicate 44 newly retained reports |"),
        ("| Formal screening cumulative | 241 TA decisions; 73 primary includes; 84 assessed FT exclusions; 1 not retrieved; FT backlog 0 | Evidence lanes and blockers | Screen remaining 66 new Batch-3 records |", "| Formal screening cumulative | 307 TA decisions; 73 primary includes; 84 assessed FT exclusions; 1 not retrieved; FT backlog 44 | Evidence lanes and blockers | Close 44 newly retained Batch-3 full texts, then advance to Batch 4 |"),
        ("JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 627 records remain title/abstract unscreened and no common geography-by-cue-overlap estimand has passed independence/scale checks.", "JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 561 records remain title/abstract unscreened, 44 newly retained Batch-3 reports await full-text adjudication, and no common geography-by-cue-overlap estimand has passed independence/scale checks."),
    ]
    for old, new in pairs:
        text = replace_once(text, old, new, "ledger")
    path.write_text(text, encoding="utf-8")


def update_jbi() -> None:
    path = Path("docs/SCH_JBI_GEOGRAPHY_PREVIEW_READOUT_V1.md")
    text = path.read_text(encoding="utf-8")
    marker = "Batch 3 (`SCHPRISMA-000201`–`000300`) is now 100/100 complete at title/abstract stage under V16."
    if marker in text:
        return
    pairs = [
        ("Batch 1 (`SCHPRISMA-000001`–`000100`) and Batch 2 (`SCHPRISMA-000101`–`000200`) are now completely title/abstract screened. Batch 3 (`SCHPRISMA-000201`–`000300`) is in progress: one record (`000219`) was already adjudicated in V1, 33 high-information records are decided in V14, and 66 genuinely new Batch-3 records remain undecided.", "Batch 1 (`SCHPRISMA-000001`–`000100`) and Batch 2 (`SCHPRISMA-000101`–`000200`) are completely title/abstract screened. Batch 3 (`SCHPRISMA-000201`–`000300`) is now 100/100 complete at title/abstract stage under V16. One record (`000219`) was already adjudicated in V1; V14 decided 33 high-information records and V16 decides the remaining 66 genuinely new records."),
        ("title/abstract screened:               241", "title/abstract screened:               307"),
        ("retained for full text:                158", "retained for full text:                202"),
        ("title/abstract excluded:                83", "title/abstract excluded:               105"),
        ("unscreened:                            627", "unscreened:                            561"),
        ("full-text undecided among retained:      0", "full-text undecided among retained:     44"),
        ("current retained full-text backlog:      0", "current retained full-text backlog:     44"),
        ("full title/abstract screening:          NO (627 remaining)", "full title/abstract screening:          NO (561 remaining)"),
        ("The Batch-3 high-information queue is now closed through full text under V15. The next work object is the **remaining 66 genuinely new Batch-3 title/abstract records**.", "Batch 3 is now complete at title/abstract stage under V16. The next work object is **full-text adjudication of the 44 reports newly retained by V16**."),
    ]
    for old, new in pairs:
        text = replace_once(text, old, new, "JBI")
    path.write_text(text, encoding="utf-8")


def write_readout() -> None:
    Path("docs/SCH_PRISMA_V16_BATCH3_REMAINDER_TA_READOUT.md").write_text(
        """# SCH PRISMA V16 — Batch-3 remainder title/abstract closure

## Frozen Batch-3 accounting

```text
Batch-3 frozen records:                 100
prior source-adjudicated record:          1  (SCHPRISMA-000219)
V14 high-information TA decisions:       33
V16 remainder TA decisions:              66
V16 retain for full text:                 44
V16 TA exclude:                           22
Batch-3 TA completion:                  100/100
```

## Machine-audited cumulative state

```text
frozen denominator:                    868
title/abstract screened:               307
retained for full text:                202
title/abstract excluded:               105
TA unscreened:                         561

primary studies included:               73
formal full-text EXCLUDE decisions:     85
assessed full-text exclusions:          84
reports not retrieved:                   1
current full-text undecided:            44

STRICT_LINKED_EXPERIMENT:                2
DIRECTIONAL_OR_NEAR_PASS:               64
EVOLUTIONARY_OUTCOME:                   22
HISTORICAL_TRANSITION:                    1

positive geographic records:           13
positive receiver records:              12
joint geography + receiver records:     11
```

V16 is title/abstract screening progress only. The 44 retained records are not promoted into evidence lanes, geography counters or historical claims until source-level full-text adjudication. The strict positive dual-audience same-`A` chain remains unrecovered, and the single historical-transition record remains a receiver-role transition rather than shared-cue → private-cue L4.

The next work object is full-text adjudication of the 44 newly retained Batch-3 reports. Screening progress alone does not authorize pooling.
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    update_ledger()
    update_jbi()
    write_readout()

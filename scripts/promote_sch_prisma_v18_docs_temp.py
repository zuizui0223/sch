from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise RuntimeError(f"{label}: expected 1 anchor, found {n}")
    return text.replace(old, new, 1)

# Publication ledger
p = ROOT / 'docs' / 'PUBLICATION_MATERIAL_LEDGER.md'
text = p.read_text(encoding='utf-8')
for old, new, label in [
    ('## Current screening state — Batch 3 full-text closure complete under V17', '## Current screening state — Batch 4 high-information title/abstract screening under V18', 'ledger heading'),
    ('title/abstract screened:         307', 'title/abstract screened:         364', 'ledger TA screened'),
    ('retained for full text:          202', 'retained for full text:          248', 'ledger retained'),
    ('title/abstract excluded:         105', 'title/abstract excluded:         116', 'ledger TA excluded'),
    ('unscreened:                      561', 'unscreened:                      504', 'ledger unscreened'),
    ('full-text eligible:              202', 'full-text eligible:              248', 'ledger FT eligible'),
    ('full-text undecided:               0', 'full-text undecided:              46', 'ledger FT backlog'),
    ('JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 561 records remain title/abstract unscreened and no common geography-by-cue-overlap estimand has passed independence/scale checks.', 'JBI remains **UNRESOLVED, NOW EMPIRICALLY PLAUSIBLE**, not submission-ready: 504 records remain title/abstract unscreened, 46 Batch-4 high-information reports await full-text adjudication, and no common geography-by-cue-overlap estimand has passed independence/scale checks.', 'ledger JBI state'),
    ('| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 561 records |', '| Framing question | shared versus private cues | Cue overlap determines whether pollinator gain can be separated from antagonist exposure | Preserve operational cue-overlap coding through remaining 504 records |', 'ledger framing row'),
    ('| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 561 records remain title/abstract unscreened |', '| PRISMA V2 | frozen 868 cohort | Immutable systematic denominator | 504 records remain title/abstract unscreened |', 'ledger PRISMA row'),
    ('| Formal screening cumulative | 307 TA decisions; 89 primary includes; 112 assessed FT exclusions; 1 not retrieved; FT backlog 0 | Evidence lanes and blockers | Advance to Batch 4 title/abstract screening |', '| Formal screening cumulative | 364 TA decisions; 89 primary includes; 112 assessed FT exclusions; 1 not retrieved; FT backlog 46 | Evidence lanes and blockers | Full-text adjudicate 46 V18 reports and screen the remaining 41 new Batch-4 TA records |', 'ledger formal row'),
    ('| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 307 TA decisions; 89 includes; 112 assessed FT exclusions; 1 not retrieved; FT backlog 0 |', '| Figure 2 | PRISMA flow + strict/near-pass/evolutionary lanes | Frozen denominator; 364 TA decisions; 89 includes; 112 assessed FT exclusions; 1 not retrieved; FT backlog 46 |', 'ledger fig2 row'),
    ('| Table 1 | Systematic study decisions/blockers | 307 TA screened; 89 primary includes; FT backlog 0 |', '| Table 1 | Systematic study decisions/blockers | 364 TA screened; 89 primary includes; FT backlog 46 |', 'ledger table1 row'),
]:
    text = replace_once(text, old, new, label)

batch3 = 'Batch 2 remains closed. V16 completed Batch-3 title/abstract screening, and V17 now resolves all 44 reports retained by V16 at full text: 16 are included and 28 excluded. Batch 3 is therefore closed at both title/abstract and current full-text stages. The next work object is Batch-4 title/abstract screening. This does not authorize pooled effects and does not mean the 868-record screen is complete.'
addition = batch3 + '\n\n### Batch-4 high-information title/abstract screening under V18\n\nBatch 4 contains 100 frozen records. Two (`SCHPRISMA-000329`, `SCHPRISMA-000339`) were already source-adjudicated before V18, leaving 98 genuinely new title/abstract targets. Machine triage identified 57 high-information records; V18 formally retains 46 for full text and excludes 11. The remaining 41 new Batch-4 records are still title/abstract unscreened. V18 is screening progress only and does not change strict, near-pass, evolutionary, historical or geography evidence counts.'
text = replace_once(text, batch3, addition, 'ledger V18 section')

batch3row = '| Batch 3 | 100/100 TA decisions; V17 resolves every retained Batch-3 report at full text | Third systematic batch | Closed; advance to Batch 4 title/abstract screening |'
batch4row = batch3row + '\n| Batch 4 | 57/98 genuinely new TA targets adjudicated in V18; 46 retained / 11 excluded | Fourth systematic batch | Full-text adjudicate 46 high-information reports and screen remaining 41 TA records |'
text = replace_once(text, batch3row, batch4row, 'ledger Batch4 row')
p.write_text(text, encoding='utf-8')

# JBI readout
p = ROOT / 'docs' / 'SCH_JBI_GEOGRAPHY_PREVIEW_READOUT_V1.md'
text = p.read_text(encoding='utf-8')
for old, new, label in [
    ('title/abstract screened:               307', 'title/abstract screened:               364', 'JBI TA screened'),
    ('retained for full text:                202', 'retained for full text:                248', 'JBI retained'),
    ('title/abstract excluded:               105', 'title/abstract excluded:               116', 'JBI excluded'),
    ('unscreened:                            561', 'unscreened:                            504', 'JBI unscreened'),
    ('full-text undecided among retained:      0', 'full-text undecided among retained:     46', 'JBI FT backlog'),
    ('current retained full-text backlog:      0', 'current retained full-text backlog:     46', 'JBI current backlog'),
    ('full title/abstract screening:          NO (561 remaining)', 'full title/abstract screening:          NO (504 remaining)', 'JBI full screen'),
]:
    text = replace_once(text, old, new, label)

state = 'Batch 2 remains closed. V16 completes Batch-3 title/abstract screening and V17 closes all 44 newly retained Batch-3 reports at full text: 16 are included and 28 excluded. Strict remains 2, while near-pass and evolutionary lanes rise to 77 and 29; the historical-transition lane reaches four records without satisfying shared-cue → private-cue L4.'
state2 = state + '\n\nV18 begins Batch 4 without changing the evidence lanes: of 98 genuinely new title/abstract targets after two prior decisions, 57 high-information records are adjudicated, 46 are retained for full text and 11 excluded. The remaining 41 new Batch-4 records are still title/abstract unscreened.'
text = replace_once(text, state, state2, 'JBI V18 state')

next_old = 'Batch 3 is now closed at title/abstract and current full-text stages under V17. The next work object is **Batch-4 title/abstract screening**. Independence and outcome-scale coding continue in parallel; screening progress alone does not authorize pooling.'
next_new = 'Batch 3 remains closed. Under V18, Batch 4 has 57/98 genuinely new title/abstract targets adjudicated. The next work objects are **full-text adjudication of the 46 high-information reports retained by V18** and **title/abstract screening of the remaining 41 new Batch-4 records**. Independence and outcome-scale coding continue in parallel; screening progress alone does not authorize pooling.'
text = replace_once(text, next_old, next_new, 'JBI next priority')
p.write_text(text, encoding='utf-8')

# Dedicated V18 readout
(ROOT / 'docs' / 'SCH_PRISMA_V18_BATCH4_HIGH_INFORMATION_TA_READOUT.md').write_text('''# SCH PRISMA V18 — Batch-4 high-information title/abstract screening\n\n## Frozen Batch-4 accounting\n\n```text\nBatch-4 frozen records:                    100\nprior TA decisions:                          2  (SCHPRISMA-000329, SCHPRISMA-000339)\ngenuinely new TA targets:                   98\nhigh-information queue:                     57\nV18 RETAIN_FULLTEXT:                        46\nV18 EXCLUDE:                                11\nremaining new Batch-4 TA records:           41\n```\n\n## Machine-audited cumulative state\n\n```text\nfrozen denominator:                        868\ntitle/abstract screened:                   364\nretained for full text:                    248\ntitle/abstract excluded:                   116\nTA unscreened:                             504\n\nprimary studies included:                   89\nassessed full-text exclusions:             112\nreports not retrieved:                       1\ncurrent full-text undecided:                46\n\nSTRICT_LINKED_EXPERIMENT:                    2\nDIRECTIONAL_OR_NEAR_PASS:                   77\nEVOLUTIONARY_OUTCOME:                       29\nHISTORICAL_TRANSITION:                        4\n\npositive geographic records:               20\npositive receiver records:                  19\njoint geography + receiver records:         17\n```\n\nV18 is title/abstract screening progress only. The 46 retained reports are not promoted into evidence lanes, geography counters or historical claims until source-level full-text adjudication. The strict positive dual-audience same-`A` chain remains unrecovered and direct shared-cue → private-cue L4 remains unrecovered.\n\nThe next work objects are full-text adjudication of the 46 V18-retained reports and title/abstract screening of the remaining 41 genuinely new Batch-4 records.\n''', encoding='utf-8')

from __future__ import annotations

from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "manuscript" / "nph_viewpoint_figures"


def svg(width: int, height: int, body: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<style>
text {{ font-family: Arial, Helvetica, sans-serif; fill: #111; }}
.title {{ font-size: 34px; font-weight: 700; }}
.head {{ font-size: 23px; font-weight: 700; }}
.body {{ font-size: 19px; }}
.small {{ font-size: 16px; }}
.tiny {{ font-size: 14px; }}
.box {{ fill: #fff; stroke: #222; stroke-width: 2; }}
.soft {{ fill: #f4f4f4; stroke: #222; stroke-width: 2; }}
.dark {{ fill: #e5e5e5; stroke: #111; stroke-width: 2.5; }}
.dash {{ fill: none; stroke: #555; stroke-width: 2; stroke-dasharray: 9 7; }}
.line {{ fill: none; stroke: #222; stroke-width: 2.4; }}
.arrow {{ fill: none; stroke: #222; stroke-width: 2.4; marker-end: url(#arrow); }}
</style>
<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#222"/></marker></defs>
{body}
</svg>'''


def text(x: float, y: float, s: str, cls: str = "body", anchor: str = "start") -> str:
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(s)}</text>'


def box(x: float, y: float, w: float, h: float, title: str, lines: list[str], cls: str = "box") -> str:
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" class="{cls}"/>']
    out.append(text(x + 18, y + 32, title, "head"))
    yy = y + 64
    for line in lines:
        out.append(text(x + 18, yy, line, "body"))
        yy += 28
    return "".join(out)


def arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="arrow"/>'


def fig1() -> str:
    b = [text(600, 48, "Figure 1. Multifunctionality is not functional conflict", "title", "middle")]
    stages = [
        ("L0 — multifunctionality", ["one coordinate contributes", "to >1 biological function"]),
        ("L1 — local conflict", ["opposing causal effects", "on the same trait contrast"]),
        ("L2 — compromise geometry", ["zP* ≠ zG* plus supported", "interior combined optimum zC*"]),
        ("L3 — causal compromise", ["selective removal moves zC*", "and component gradients oppose"]),
        ("L4 — pure-function promotion", ["component optima stable across", "the alternate functional state"]),
    ]
    y = 105
    for i, (title, lines) in enumerate(stages):
        cls = "dark" if i in (1, 3) else "soft"
        b.append(box(120, y, 960, 112, title, lines, cls))
        if i < len(stages) - 1:
            b.append(arrow(600, y + 116, 600, y + 146))
        y += 150
    b.append(text(600, 865, "Each arrow is a promotion gate, not a synonym.", "head", "middle"))
    b.append(text(600, 900, "Aligned multifunctionality is an expected negative control, not a failure of the framework.", "body", "middle"))
    return svg(1200, 940, "".join(b))


def fig2() -> str:
    b = [text(650, 48, "Figure 2. What the crossed experiment identifies", "title", "middle")]
    x0, y0, w, h = 70, 115, 710, 620
    b.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="16" class="box"/>')
    b.append(text(x0 + 25, y0 + 38, "A. Context-specific reproductive surfaces", "head"))
    b.append('<line x1="130" y1="545" x2="720" y2="545" class="line"/>')
    b.append('<line x1="130" y1="545" x2="130" y2="185" class="line"/>')
    b.append(text(425, 582, "trait coordinate z", "body", "middle"))
    b.append(text(92, 350, "fitness", "body", "middle"))
    paths = [
        ('M 155 485 Q 300 190 445 485', 'W10(z): pollinator-present / antagonist-off'),
        ('M 300 485 Q 445 225 590 485', 'W11(z): combined state'),
        ('M 445 485 Q 590 205 710 485', 'W01(z): pollinator-off / antagonist-present'),
        ('M 205 500 Q 430 330 665 500', 'W00(z): both focal channels off'),
    ]
    for d, _ in paths:
        b.append(f'<path d="{d}" class="line"/>')
    b.append(text(285, 180, "zP*", "head", "middle"))
    b.append(text(445, 215, "zC*", "head", "middle"))
    b.append(text(595, 195, "zG*", "head", "middle"))
    yy = 620
    for _, lab in paths:
        b.append(text(95, yy, lab, "small"))
        yy += 25

    b.append(box(825, 115, 405, 220, "B. Direct claim", [
        "zP*, zG*, zC* are optima", "of declared ecological states.", "", "They are not automatically", "pure-function optima."
    ], "dark"))
    b.append(box(825, 370, 405, 365, "C. Promotion test", [
        "M_G0(z)=W10-W00", "M_G1(z)=W11-W01", "H_P0(z)=W01-W00", "H_P1(z)=W11-W10", "", "Promote only if component", "optima are context-stable", "within a frozen equivalence bound."
    ], "soft"))
    b.append(text(650, 805, "Consumer removal identifies causal contrasts; it does not erase every non-focal pathway by definition.", "head", "middle"))
    return svg(1300, 850, "".join(b))


def fig3() -> str:
    b = [text(650, 48, "Figure 3. Source-adjudicated reality pattern", "title", "middle")]
    b.append(text(650, 82, "16 independent biological clusters; counts describe recurrence in the screened universe, not natural prevalence.", "body", "middle"))
    categories = [
        ("Direct conflict signatures", 5, "opposing direction or combined compromise"),
        ("Context-weight shifts", 7, "functional weighting changes across environment/agents"),
        ("Aligned / no-conflict controls", 2, "multifunctional but no identified opposing optimum"),
        ("Conflict candidate", 1, "shared tracking; incomplete common-fitness attribution"),
        ("Sequential-filter boundary", 1, "selection at different life-history stages"),
    ]
    y = 130
    maxn = 7
    for name, n, note in categories:
        b.append(text(90, y + 28, name, "head"))
        xbar, barw = 480, 650 * n / maxn
        b.append(f'<rect x="{xbar}" y="{y}" width="{barw}" height="42" rx="8" class="dark"/>')
        b.append(text(xbar + barw + 18, y + 29, str(n), "head"))
        b.append(text(90, y + 58, note, "small"))
        y += 105
    b.append(box(90, 690, 1120, 150, "Quantitative gate remains fail-closed", [
        "Four strong same-coordinate designs are in the strict inventory, but no random-effects stratum currently",
        "has ≥3 independent clusters with a compatible estimand, orientation, valid uncertainty, and covariance handling.",
        "Positive-only admission cannot be reinterpreted as prevalence or as an independent recurrence test."
    ], "soft"))
    return svg(1300, 880, "".join(b))


def fig4() -> str:
    b = [text(650, 48, "Figure 4. From conflict identification to downstream questions", "title", "middle")]
    b.append(box(55, 115, 355, 310, "Conflict identification", [
        "same coordinate", "opposing causal geometry", "state-specific compromise", "component stability gate", "", "Output: justified conflict", "and, when possible, a", "common-scale conflict budget"
    ], "dark"))
    b.append(arrow(420, 270, 550, 270))
    b.append(text(485, 238, "export only", "small", "middle"))
    b.append(text(485, 259, "identified quantities", "small", "middle"))
    b.append(box(565, 115, 405, 310, "Value and evolutionary realization", [
        "recoverable benefit vs cost", "→ local accessibility", "→ invasion", "→ fixation", "→ long-run occupancy", "", "Requires new estimands and", "population-process assumptions"
    ], "soft"))
    b.append('<line x1="1002" y1="95" x2="1002" y2="445" class="dash"/>')
    b.append(box(1030, 115, 220, 310, "Mechanism allocation", [
        "after multiple trait axes", "", "trait interaction", "≠ mechanism", "", "orthogonal", "identification problem"
    ], "soft"))
    b.append(box(55, 510, 1195, 250, "The focal experiment closes the residual upstream causal gap", [
        "literature recurrence / specificity → compatibility audit → qualify focal context → reversible multi-level z",
        "→ selective functional interventions → W00(z), W10(z), W01(z), W11(z) → zP*, zG*, zC*",
        "→ predicted optimum shifts + opposing component gradients → optional context-stable function promotion"
    ], "box"))
    b.append(text(650, 820, "Multifunctionality is not promoted to conflict until the causal gate is passed.", "head", "middle"))
    return svg(1300, 860, "".join(b))


FIGURE_NAMES = [
    "FIG1_PROMOTION_LADDER.svg",
    "FIG2_CROSSED_IDENTIFICATION.svg",
    "FIG3_REALITY_PATTERN.svg",
    "FIG4_PROGRAM_HANDOFF.svg",
]


def build(out_dir: Path = OUT) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    svgs = [fig1(), fig2(), fig3(), fig4()]
    paths: list[Path] = []
    for name, content in zip(FIGURE_NAMES, svgs):
        path = out_dir / name
        path.write_text(content, encoding="utf-8")
        paths.append(path)
    return paths


if __name__ == "__main__":
    for p in build():
        print(p)

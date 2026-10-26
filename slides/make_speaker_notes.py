#!/usr/bin/env python3
"""Build speaker-notes.md and speaker-notes.pdf from the deck's <div class="notes">.

The deck is the single source of truth: edit the notes in index.html and re-run
this script. Nothing here is hand-maintained.

    python3 make_speaker_notes.py
"""
import html
import re
import pathlib
import subprocess

HERE = pathlib.Path(__file__).parent
DECK = HERE / "index.html"

INTRO = """# AF3625 Group 5 — speaker notes

Generated from `index.html` (the deck is the single source of truth).
**26 slides · about 16½ minutes of scripted speech.** With pointing at the diagrams,
pauses and the two handovers, the run lands at roughly 20–22 minutes — inside the
25-minute cap with room for questions.

| Role | Slides | Scripted time |
|---|---|---|
| Presenter A | 1–4 · cover, roadmap, the two concept primitives | ≈ 2:35 |
| Presenter B | 5–11 · **Question 5.1**, television market, country Z | ≈ 4:35 |
| Presenter C | 12–19 · **Question 5.2**, handbag market, country A | ≈ 4:50 |
| Presenter D | 20–26 · **Question 5.3** Egypt and **Question 5.4** the article | ≈ 4:25 |

That split keeps one presenter per question, which is easiest for the audience to follow.
If the group wants four exactly equal blocks instead, hand over at these points instead:
**A → 1–7** (intro, primer, and Q5.1 up to the import quantity) · **B → 8–13** (Q5.1
producer surplus to Q5.2 setup) · **C → 14–19** (Q5.2 parts a–f) · **D → 20–26**.
Every member must still know the whole answer set — the Q&A is marked on teamwork.

**Using these notes live:** press `S` in the browser for the presenter window (current
slide, next slide, this script, and a timer), or `N` for the notes drawer. Print this
document if you prefer paper — one block per slide, in order.

---
"""


def main() -> None:
    deck = DECK.read_text()

    slides = []
    for m in re.finditer(r'<section class="slide[^>]*data-title="([^"]+)"[^>]*>(.*?)(?=<section class="slide|</div>\s*<script)', deck, re.S):
        title, body = m.group(1), m.group(2)
        note = re.search(r'<div class="notes">(.*?)</div>', body, re.S)
        if not note:
            continue
        raw = note.group(1)
        secs = int(re.search(r"<b>(\d+) s", raw).group(1))
        who = re.search(r"·\s*(Presenter [A-D])", raw).group(1)
        paras = [html.unescape(re.sub(r"<[^>]+>", " ", p)).strip()
                 for p in re.findall(r"<p>(.*?)</p>", raw, re.S)]
        meta, script = paras[0], paras[1]
        handover = [p for p in paras[2:] if p.startswith("Handover:")]
        slides.append((len(slides) + 1, title, secs, who, script, handover))

    total = sum(s[2] for s in slides)
    md = [INTRO]

    for n, title, secs, who, script, handover in slides:
        md.append(f"## {n}. {title}\n")
        md.append(f"`{secs // 60}:{secs % 60:02d}` · **{who}**\n")
        md.append(script + "\n")
        for h in handover:
            md.append(f"> **{h}**\n")
        md.append("---\n")

    md.append(f"*Scripted speech: {total // 60} min {total % 60:02d} s across {len(slides)} slides.*\n")
    (HERE / "speaker-notes.md").write_text("\n".join(md))
    print(f"speaker-notes.md written — {len(slides)} slides, {total // 60}:{total % 60:02d}")

    # ── printable A4 portrait PDF from the same content ────────────────────
    body = []
    for n, title, secs, who, script, handover in slides:
        body.append(f'<section><h2><span class="n">{n}</span> {title}</h2>'
                    f'<p class="meta">{secs // 60}:{secs % 60:02d} · {who}</p>'
                    f'<p class="script">{script}</p>'
                    + "".join(f'<p class="hand">{h}</p>' for h in handover)
                    + "</section>")
    page = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>AF3625 Group 5 — speaker notes</title><style>
@page {{ size: A4 portrait; margin: 18mm 16mm; }}
body {{ font: 11.5pt/1.5 'Inter', system-ui, sans-serif; color: #0a2540; margin: 0; }}
h1 {{ font-size: 20pt; margin: 0 0 4pt; letter-spacing: -.02em; }}
.lead {{ font-size: 10.5pt; color: #3d4d68; margin: 0 0 14pt; }}
table {{ border-collapse: collapse; font-size: 10pt; margin: 0 0 8pt; }}
td, th {{ border-bottom: 1px solid #ccd6e4; padding: 3pt 10pt 3pt 0; text-align: left; }}
section {{ break-inside: avoid; border-top: 1.5pt solid #0a2540; padding: 7pt 0 10pt; }}
h2 {{ font-size: 13pt; margin: 0 0 2pt; }}
h2 .n {{ font-family: 'JetBrains Mono', monospace; color: #1d4ed8; }}
.meta {{ font-family: 'JetBrains Mono', monospace; font-size: 8.5pt; letter-spacing: .1em;
  text-transform: uppercase; color: #8b98ad; margin: 0 0 5pt; }}
.script {{ margin: 0; }}
.hand {{ margin: 6pt 0 0; border-left: 2.5pt solid #1d4ed8; padding-left: 7pt; font-size: 10.5pt; }}
</style></head><body>
<h1>AF3625 Group 5 — speaker notes</h1>
<p class="lead">Questions 5.1–5.4 · {len(slides)} slides · {total // 60} min {total % 60:02d} s of scripted
speech (≈ 20–22 minutes with the diagrams and pauses) · one block per slide, in deck order.</p>
<table>
<tr><th>Role</th><th>Slides</th><th>Time</th></tr>
<tr><td>Presenter A</td><td>1–4 · cover, roadmap, concept primitives</td><td>2:35</td></tr>
<tr><td>Presenter B</td><td>5–11 · Question 5.1 — television market, country Z</td><td>4:35</td></tr>
<tr><td>Presenter C</td><td>12–19 · Question 5.2 — handbag market, country A</td><td>4:50</td></tr>
<tr><td>Presenter D</td><td>20–26 · Question 5.3 Egypt + Question 5.4 article</td><td>4:25</td></tr>
</table>
{''.join(body)}
</body></html>"""
    (HERE / ".speaker-notes.html").write_text(page)
    subprocess.run(["google-chrome", "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={HERE / 'speaker-notes.pdf'}",
                    f"file://{HERE / '.speaker-notes.html'}"], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
    (HERE / ".speaker-notes.html").unlink()
    print("speaker-notes.pdf written")


if __name__ == "__main__":
    main()

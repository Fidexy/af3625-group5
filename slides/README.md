# Q5.1–5.4 presentation — `deck.pdf`

**Deliverable: `deck.pdf`** — 26 pages, 16:9 (1920 × 1080), embedded fonts, and every
diagram is **vector** (no raster images anywhere in the file).

`index.html` is the source. `figs/*.svg` are the diagrams on their own.

## The deck at a glance

| | |
|---|---|
| 1 | Cover |
| 2 | Roadmap |
| 3–4 | Concept primer: the world price · surplus and the two trade barriers |
| 5 | **Part 2 · Q5.1** — television market, country Z *(question as set)* |
| 6–11 | Reading the diagram · imports · producer surplus · the quota · **the S + quota trap** · quota rent |
| 12 | **Part 3 · Q5.2** — handbag market, country A *(question as set)* |
| 13–19 | Setup · autarky · free-trade imports · the $25 tariff · tariff revenue · consumer surplus · is the tariff beneficial? |
| 20 | **Part 4 · Q5.3** — generator market, Egypt *(question as set)* |
| 21–22 | Price, output, imports, revenue · gainers, losers and the deadweight loss |
| 23 | **Part 5 · Q5.4** — a real trade dispute *(question as set)* |
| 24 | The EU’s 2024 duties on Chinese EVs, mapped to Topic 5 |
| 25–26 | Conclusion · References and Q&A |

Each part opens with a light section page that **reproduces the question as set** — the
scenario, the equations and every sub-part (i)–(vi) / (a)–(f), verbatim — so the audience
can check each part off, and the tutor can see we are answering exactly what was asked.
There is no paraphrase of the question anywhere in the deck.

## Theme and style

A deck-local theme layer — *engineering blueprint* — derived from the skill’s
`engineering-whiteprint` theme: blueprint grid paper, square corners, hairlines, mono
(JetBrains Mono) for labels, numerals, equations and page furniture, Inter for prose.

Crucially it **re-anchors the theme tokens onto the colour code the assignment fixes for
the diagrams**, so the slides and the figures share one palette — no second green, no
second red:

| Colour | Meaning |
|---|---|
| navy `#0a2540` | ink, axes, domestic curves, world price |
| blue `#1d4ed8` | consumer surplus / loss to consumers — also the structural accent |
| green `#0e9f6e` | producer surplus / gain to producers |
| amber `#d97706` | government revenue / quota rent |
| red `#dc2626` (hatched) | deadweight loss |

Every figure sits in a bordered panel with a `FIG. n` tab and a one-line caption; tall
figures use a fixed height budget (`.figbox.cap`) so the SVG letterboxes instead of
pushing its caption into the footer. Page numbers are derived from slide order by a tiny
script, so re-ordering slides never leaves a stale “n / 26”.

### Legibility (this was designed for a projector, not a laptop)

The canvas is 1920 × 1080 px, so these are the numbers that matter:

| Element | Size on the canvas |
|---|---|
| Slide titles | 58 px |
| Body, bullets, calculation steps | 31 px |
| Table cells / equations | 29 px |
| Captions, secondary notes | 21–23 px |
| Figure labels (inside the SVGs) | 23–30 px rendered |

To keep type that size and still fit, the diagrams were re-drawn with **flatter price
axes** (a 1.5:1 or wider viewBox) and tight crops, so each figure fills its column
instead of leaving dead space — the SVG is displayed at roughly its natural size or
larger, which is what makes its labels match the body text. Slide bodies were trimmed at
the same time: fewer words, bigger type.

`scripts`-free check that is worth re-running after any edit: a small in-page script
measures, for every slide, the lowest painted element against the footer. The current
deck passes with **≥ 48 px of clearance on all 26 slides** and zero overflow.

> ⚠️ Do not name a slide class `divider` — `base.css` already defines
> `.divider{height:1px}` for horizontal rules, which silently collapses the slide. The
> section pages use `.secopen`.

## Presenting

```bash
xdg-open index.html        # ← →  navigate · F fullscreen · S presenter · N notes · O overview · T theme
```

The HTML is also the way to *rehearse*: nothing needs to be installed, and it works offline.

## Speaker notes

Every slide carries a spoken script in a hidden `.notes` block — press **`S`** for the
presenter window (current slide, next slide, script, timer) or **`N`** for the notes drawer.

| File | Use |
|---|---|
| `speaker-notes.pdf` | 8 pages A4 — print this if you prefer paper |
| `speaker-notes.md` | same content as text, for a laptop or phone |

**26 slides · 16 min 20 s of scripted speech** (≈ 20–22 minutes with the diagrams,
pauses and handovers). The notes are generated from the deck, so the deck stays the
single source of truth — never edit the two files by hand:

```bash
python3 make_speaker_notes.py     # rewrites speaker-notes.md + speaker-notes.pdf from index.html
```

Each block gives the slide, its time, the presenting role, the script, and a handover cue
where the presenter changes. Role split: **A** slides 1–4 (intro + concept primitives,
2:35) · **B** 5–11 (Question 5.1, 4:35) · **C** 12–19 (Question 5.2, 4:50) · **D** 20–26
(Questions 5.3 and 5.4 + conclusion, 4:25). One presenter per question — the notes file
also gives an alternative exactly-equal four-way split if the group prefers it.

**In class:** show `deck.pdf`, or open `index.html` in any browser. The PDF has no
dependencies at all — the HTML needs the skill’s `assets/` folder next to it.

## Rebuilding

```bash
# PDF (26 landscape pages; the @page rule in index.html sets the page size)
google-chrome --headless=new --disable-gpu --no-pdf-header-footer \
  --print-to-pdf=deck.pdf "file://$PWD/index.html"

# PNG of every slide
~/.pi/agent/skills/html-ppt/scripts/render.sh index.html all out/

# diagrams (rewrites figs/*.svg — do not hand-edit them)
python3 figs/generate_figures.py
```

## Answers used in the deck

| | Result |
|---|---|
| Q5.1 (ii) | imports = 120,000 − 20,000 = **100,000 TVs** |
| Q5.1 (iii) | PS = ½ × 20,000 × $25 = **$250,000** |
| Q5.1 (v) | S + quota must be **kinked**: domestic S below $75, a jump right by 20,000 at $75, then S shifted right by 20,000 |
| Q5.1 (vi) | quota rent = ($125 − $75) × 20,000 = **$1,000,000** (new price $125: Q<sub>d</sub> 80,000, Q<sub>s</sub> 60,000) |
| Q5.2 (a) | P* = **$700**, Q* = **38,600** |
| Q5.2 (b) | imports = **4,800** (Q<sub>d</sub> 38,800, Q<sub>s</sub> 34,000) |
| Q5.2 (c) | P = $625 → tariff = **$25** per handbag |
| Q5.2 (d) | tariff revenue = **$90,000** |
| Q5.2 (e) | CS = ½ × 38,750 × ($20,000 − $625) = **$375,390,625** |
| Q5.2 (f) | false: ΔCS −$969,375, ΔPS +$864,375, revenue +$90,000 → net **−$15,000** = DWL |
| Q5.3 (a) | price **$400**, Q<sub>s</sub> 5,000, Q<sub>d</sub> 6,000, imports **1,000**, revenue **$100,000** |
| Q5.3 (b) | ΔPS **+$450,000**, ΔCS **−$650,000**, DWL **$100,000** (net −$100,000) |
| Q5.4 | EU countervailing duties on Chinese BEVs, 29 Oct 2024 (Reuters) — slide 24 |

## Still to fill in

- Slide 1: the **member names** (and the slot, if the tutorial is not Tuesday).
- Rehearse to ≤ 22 minutes against the presenter timer.
- The individual written assignment (Q5.1–5.3, 600–1,000 words) is due one week after
  the presentation — the figures in `figs/` can be reused.

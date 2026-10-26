# Question 5 — AF3625 Group 5 working set

Everything needed to present **Q5.1–5.4** (group presentation) and write up **Q5.1–5.3**
(individual assignment), trimmed to the relevant pages. Originals in the parent folder
are untouched; page-level provenance is recorded below.

---

## Contents

| File | Pages | Why it is here |
|---|---|---|
| `00-questions/Group5_Questions_5.1-5.4.pdf` | 3 | The assignment itself. Trimmed from pp. 14–16 of the 23-page bank (Group 5 section only; Group 6 and other groups removed). |
| `00-questions/Q5.1_figure.png` | — | The TV-market diagram for Q5.1, extracted at its **native 975×762 px / 166 ppi** (lossless copy of the embedded JPEG). Not in the text layer — must be read visually. |
| `01-rubrics/AF3625_Presentation_Rubric.pdf` | 3 | Group presentation marks. |
| `01-rubrics/AF3625_Written Assignment_Rubric.pdf` | 2 | Individual assignment marks. |
| `02-subject-outline/AF3625 Subject Outline 2026-27 First semester.pdf` | 11 | Tutorial schedule (when Group 5 presents), assignment rules, **and the cover-page template on the last page**. |
| `03-lecture-slides/Topic 5 Lecture Slides.pdf` | 23 | **Core.** Free trade, tariff, quota, quota rent, winners/losers, DWL. |
| `03-lecture-slides/Topic 2 (consumer-producer-social surplus).pdf` | 33 | **Dependency.** CS/PS are *used* in Topic 5 but *defined* in Topic 2. Trimmed from pp. 1–33 (elasticity, pp. 34–46, removed). |
| `03-lecture-slides/Topic 1 (demand, supply & equilibrium).pdf` | 27 | Foundation for the D/S diagrams and for solving Q5.2(a). Trimmed from pp. 19–45 (scarcity/CBA intro, pp. 1–18, removed). |
| `04-self-study-notes/Unit 5 (with answers).pdf` | 37 | **Core.** Worked figures 5.4 (tariff) and 5.6 (quota), quota rent, DWL, plus answers to its own self-exercises. |
| `04-self-study-notes/Unit 2 (consumer-producer-social surplus + answers).pdf` | 21 | **Dependency.** §§2.2–2.3 (CS, PS, social surplus, price regulation) pp. 1–17, plus responses to Self Exercises 1–4, pp. 32–35. Elasticity sections removed. |

## Deadline facts (from the subject outline)

- **Presentation:** group, **25 min max**, slides pre-loaded on the classroom PC — do **not** email the file.
- **Group 5's slot:** Week 9 (Tue 27 – Fri 30 Oct 2026) or Week 10 Mon (2 Nov) — depends on your tutorial day.
- **Individual assignment:** Q5.1, 5.2, 5.3 only; **600–1,000 words** (answers only — cover page and diagrams excluded); font 12, 1.5/double spacing; word count stated on the cover page; cover page from the last page of the subject outline.
- **Submission:** Turnitin in your tutor's Blackboard site **and** email to the tutor, within 1 week of the presentation. −5 marks if handwritten; −1 mark/day late.
- Context: mid-term is **Sat 7 Nov 2026, 5–6 pm**, Topics 1–4 (20%).

## Marking weights

| Presentation (10%) | Written assignment (15%) |
|---|---|
| Accuracy & understanding 35% | Accuracy, understanding & reflection 50% |
| Elaboration & details 25% | Elaboration & details 17% |
| PowerPoint design 15% | Structure 17% |
| Language & presentation skills 15% | Correct English & economic expressions 16% |
| Teamwork 10% | |

## What was trimmed, and why

| Source | Kept | Dropped |
|---|---|---|
| Presentation questions (23 pp.) | pp. 14–16 (all of Q5.1–5.4) | all other groups |
| Topic 1 slides (45 pp.) | pp. 19–45 (price mechanism, demand, supply, equilibrium, shifts) | pp. 1–18 (scarcity, opportunity cost, CBA intro) |
| Topic 2 slides (46 pp.) | pp. 1–33 (CS, PS, social surplus, price ceiling/floor) | pp. 34–46 (elasticity of demand, tax burden) |
| Unit 2 (40 pp.) | pp. 1–17 + 32–35 (surpluses, price regulation, answers to SE 1–4) | elasticity §§2.4–2.5 (pp. 18–31) and their answers (pp. 36–40) |

## Deliberately NOT included (and where to find them)

- **Topic 5's prerequisites are already covered above.** Topics 3, 4, 6, 7, 8 and Units 3, 4, 6, 7 are not used anywhere in Q5.1–5.4 — they belong to other groups' questions, the mid-term (Topics 1–4) and the final (Topics 1–8).
- **Compound Interest Tables + Formula Sheet** — the folder itself says "for Topic 6-8". Not needed.
- **Unit 1** — its "economic surplus" is the cost-benefit concept (benefit − cost), *not* the CS/PS market triangles; for the area method Unit 2 is self-contained. Unit 1 also holds Unit 2's discrete PS example if you want it.
- **Elasticity sections of Topic 2 / Unit 2** — Q5.2(c) is plain quantity arithmetic ("decrease the import amount by 25%"), not an elasticity problem. The one adjacent item is Topic 2 slides pp. 41–43 (tax burden / tax revenue), which is about tax *incidence*, not the tariff revenue and DWL that Q5.2(d)/(f) and Q5.3 ask for.
- **Q5.4 needs an external source** — a news/magazine article from 2021 or later on international trade or globalisation. Not in this folder by design; it has to be found.

Originals (all still in place):

```
AF3625/
├── Tutorial Presentation Questions/26-27_Tutorial Presentation Questions.pdf
├── Assessment Rubrics (Presentation and Assignment)/*.pdf
├── Subject Outline/AF3625 Subject Outline 2026-27 First semester.pdf
├── Lecture Slides (Topic 1-8)/AF3625 Topic {1,2,5} Lecture Slides.pdf
└── Self-study Notes (Unit 1-7)/AF3625-Unit{1,2,5}(with answers).pdf
```

## Verification

- Full-file copies are byte-identical to their originals (`sha256sum` checked).
- All trimmed PDFs pass `qpdf --check`; the trimmed question set contains exactly one
  occurrence each of Q5.1–5.4 and no trace of the other groups.
- The Unit 5 copy reports the same benign linearization warnings as the original.

## Known trap for Q5.1(v)

Topic 5 states the rule explicitly: **"When domestic price ≥ world price, supply becomes
S_US + quota."** The "Domestic supply plus quota" curve drawn in the given figure is the
deliberately incorrect one you are asked to re-plot. Get that right before Q5.1(vi).

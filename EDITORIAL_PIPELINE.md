# Editorial pipeline

How a draft becomes a post here: layered review passes, each with one job, run in a fixed order,
each leaving evidence behind. The author reviews once at the end rather than refereeing every pass.

Audience: the author, and any agent session running an editing pass in this repo. Skills referenced
live in `.claude/skills/`.

---

## The one rule that matters: order

**Structure → facts → voice → rhythm → reach.**

Voice work is never first. Restructuring rewrites sentences, so any polish applied before the
structure settles is thrown away. This is not a style preference; it is the difference between one
voice pass and three.

The corollary: if a pass wants to reorder sections, stop, go back to layer 1, and come forward again.
Do not patch structure from inside a voice pass.

---

## Layer 0 — Calibration

Run once, refresh when the published corpus grows by a few posts. Everything downstream measures
against this, never against generic "good writing."

| Step | Skill | Output |
| --- | --- | --- |
| Learn the voice from published work | `blog-style` | voice profile from 5–10 posts in `_posts/` |
| Set tone targets | `blog-persona` | readability, sentence length, contraction frequency |
| Measure the corpus | — | the baseline table below |

### Measured baselines (as of 2026-09)

Taken from the published essay-genre posts, not the technical how-tos.

| Metric | Corpus range | Notes |
| --- | --- | --- |
| Body words | 2,032–2,766 | anything past ~2,800 needs a reason |
| Words per paragraph | 25–40 | the single most reliable tell |
| Em dashes | 0–6 per post | he reaches for `...` instead |
| Ellipses | 1–45 | personal essays run high, argued essays run low |
| External citations | 2–9 | density above this reads researched, not lived |
| Profanity | 0 historically | welcome where it lands; absence was habit, not preference |

**Use the range, not an abstraction.** A rhythm score of "8/10, inside the published range" was wrong
once because it counted short paragraphs instead of measuring average paragraph mass. Against the
corpus the same draft was a 5. Measure the thing the corpus measures.

### Ground-truth voice samples

`.docs/wip/lane-policing-manifesto_part-02_ORIGINAL.md` and `_part-04_ORIGINAL.md` are unedited.
They stay in `wip/` on purpose. Calibrate against those and the older `_posts/` entries, not against
recent AI-assisted posts.

---

## Layer 1 — Structural review

No skill. A reading pass that produces a ranked findings list and changes nothing.

Look for, in this order of cost:

1. **Does the opener defend a claim it hasn't made?** Dangling antecedents, warm-up sentences, and
   the real hook sitting three paragraphs down.
2. **Competing theses.** Two sentences each claiming to be the fundamental point. Pick one, subordinate
   the other explicitly.
3. **Overloaded sections.** One head carrying three arguments. The seams are usually already there.
4. **Buried best material.** The most personal or most concrete paragraph filed in the middle of the
   longest section.
5. **Endings that fire twice.** A real closing line followed by another section.
6. **Ungrounded images.** A metaphor whose setup lives in a different essay, or nowhere.
7. **Promises not kept.** "Three places" with only two delivered; a motif whose setup got cut in an
   earlier revision.

**Output: a plan file in `.docs/wip/`.** Ranked findings with the diagnosis, not just the complaint,
plus drafted rewrites for the top two or three. It must be resumable cold by a session with no
context. See `.docs/archive/magical-thinking-EDIT-PLAN.md` for the shape.

---

## Layer 2 — Apply structure

Work the plan in order. Largest structural move first, because it changes what the later ones touch.

Record what gets **rejected** and why, in the plan file. A later pass will otherwise re-propose an
idea the author already killed, which wastes a round and erodes trust.

---

## Layer 3 — Fact check

Skill: `blog-factcheck`

Run before voice work, because removing or softening an unsupported claim rewrites sentences.

- Every load-bearing statistic and named source gets its URL fetched and checked
- Uncited claims are flagged UNVERIFIED — that is a decision point, not an error
- Some claims are better **uncited and asserted from standing** than sourced. First-hand professional
  knowledge stated flat reads stronger than a footnote, and it improves citation texture. Prefer it
  where the author genuinely has the standing.

---

## Layer 4 — Voice

Skills: `humanizer`, then `stop-slop`

Feed the layer 0 profile in. Without it both skills default to generic de-slopping and will flatten
the author into clipped staccato, which is as wrong as leaving him formal.

Watch for:

- **Punctuation fingerprints that give away a revision.** Em dashes clustered in exactly the newly
  written paragraphs; curly apostrophes where the rest of the file is straight. Two hands visible in
  one file.
- **Participle clauses doing fake depth** — `...ing X, ensuring Y`. The most common remaining tell.
- **Register drift.** One section contracting freely, another switching to `It is` / `cannot` / `do not`.
- **Warm-up sentences.** "I should disclose something up front" announces instead of doing.

Contract **selectively**. Flat formality earns its place where the line is a verdict. Some sentences
are worse contracted, and quoted material must never be touched.

---

## Layer 5 — Rhythm

No skill. Pure measurement, then pure paragraph breaks. **Zero word changes.**

1. Print every paragraph's word count in order
2. Find the flat runs — three or more consecutive paragraphs all above ~120 words
3. Find isolation candidates — a short verdict sentence already sitting at the *end* of a heavy
   paragraph. The weight in front of it is what earns the break

A one-line paragraph works as a verdict after 200 words of build. After 20 words it just reads choppy.

**Dosage.** Target the corpus ratio. Isolating every punch destroys the contrast that makes the
technique work — the effect depends on the heavy blocks around it.

---

## Layer 6 — Reach (optional)

Skills: `made-to-stick`, `contagious`, `storybrand-messaging`

Only for posts meant to travel. Skip for personal essays that are their own reward.

`contagious` scores STEPPS out of 10. The two levers that usually matter most here:

- **Triggers.** What recurring daily moment will fire this post back into a reader's head? Frequency
  beats strength. A cue someone hits four times a day beats a powerful rare one.
- **Practical value.** Does the piece contain a portable test a reader can apply to something else?
  If the heuristic exists but appears once mid-essay, restate it in the closer. Tools get forwarded;
  essays get admired.

Title and `summary:` are the cheapest high-leverage changes. Summaries here make a claim and open a
gap — they do not describe the post. Check the published ones before writing a new one.

---

## Layer 7 — Adversarial pass (argument posts only)

No skill. The job is to attack the conclusion, not improve the prose.

For any post arguing a position the author holds, especially one where the author is the protagonist
of their own reasoning:

1. **Does the frame apply to the author now?** A piece explaining why other people believe things
   uncritically must audit the author's current position with the same specificity, or it is
   self-serving and readers feel it early.
2. **What would falsify the thesis?** If no possible evidence would count, the claim is unfalsifiable.
3. **Where is the steelman?** The person who did the work and reached the other conclusion. If the
   piece only argues against the weak version, it has not argued.
4. **Is the sequence honest?** Did the reasoning come before the conclusion, or after it as
   justification? The second is more common and almost always gets remembered as the first.
5. **Do the cited sources cut both ways?** Research about motivated reasoning generally applies to
   the author too. Citing it only against opponents misuses it.

**The trap:** do not write the "of course, I have my own biases" paragraph. Pre-exposing a weakened
criticism paired with a ready rebuttal is textbook attitude inoculation — the exact mechanism these
posts usually criticize. A concession must cost something specific or it should not be there. If no
real concession exists, narrow the thesis instead of faking humility.

---

## Layer 8 — Scorecard

Append to the plan file. Every score cites the measurement that produced it, so the table is
auditable rather than vibes.

Voice dimensions: AI vocabulary, em dash discipline, voice fingerprint, formatting tells, register
consistency, negative parallelism, rhythm, personality.

Editorial dimensions: opening hook, structural clarity, thesis consistency, argument integrity,
ending, evidence texture, emotional pulse.

Re-score after each pass and keep the history inline (`8.5 → 8.8 → 9.0`). A dimension that never
moves across three passes is a structural trade, not a defect — say so and stop trying to fix it.

**Track total length as a trend even though it is not a scored dimension.** Drafts grow in every
pass and nothing is ever cut unless someone is watching.

---

## Layer 9 — Author review

The author reads once, here, with a finished draft and a scorecard that says what moved and what
did not.

Worth their attention: the thesis, anything flagged as a deliberate trade, the title, and any
sentence a pass introduced rather than edited.

Not worth their attention: individual punctuation fixes, and anything already recorded as rejected.

---

## Layer 10 — Publish mechanics

Only after the author signs off.

- [ ] Front matter complete — see CLAUDE.md for the block
- [ ] `date:` is today or earlier. Jekyll **silently skips** future-dated posts
- [ ] `category:` has a matching file in `categories/`, or the link 404s
- [ ] `thumbnail:` file exists at the exact path in front matter, extension included
- [ ] Internal links resolve against real permalinks in `_posts/`
- [ ] `bundle exec jekyll build` succeeds
- [ ] In `build/`: page renders, `og:image` and `twitter:image` resolve, post appears in the home
      index, sitemap and feed
- [ ] Move the source draft to `.docs/archive/` and add a row to its README
- [ ] Bump `modified_date` on any post-publication edit

**This repo auto-deploys.** GitHub Pages is configured at the repo level against `main` with CNAME
`www.co3dex.com`, and GitHub's built-in `pages-build-deployment` run does the build. A push to `main`
goes live in about a minute.

---

## Standing rules

1. **Measure against the corpus, never against an abstraction.** Every claim about the author's voice
   should be checkable with a command.
2. **Record rejections.** The plan file is as much about what was killed as what was kept.
3. **Diagnose, do not just complain.** "This reads AI" is useless. "This is a tacked-on participle
   clause and it swaps to an abstract third person mid-passage" is actionable.
4. **Name the audience of the piece before editing it**, and say so. A memo for a team is not a blog
   post and should not be edited into one.
5. **Work material never enters `.docs/wip/`.** That directory is public. See CLAUDE.md.

# VOICE.md — how the owner writes

Two halves. **Measured**: `blog-style`'s `style_learn.py` over the twelve 2026 posts in `_posts/` (run once,
2026-09-13, locally, with `uv run --no-project --with textstat --with beautifulsoup4 python
.claude/skills/blog-style/scripts/style_learn.py _posts/2026-*.md --format markdown`). **Described**: Opus 5
reading the same twelve posts for what the numbers cannot see. The four 2022–2023 posts are left out; the voice
has moved since. Refreshed on request, not on a schedule.

The drafter writes toward the measured targets; the cut and the humanizer keep the described habits; the three
samples at the end are the voice sample the `humanizer` pass hands to its skill.

---

## Measured

<!-- VOICE_PROFILE_START -->
### Learned voice profile

Sample: 12 post(s).

### Style Baselines

- Sentence length: mean 17.92 words, median 12.5 words.
- Sentence burstiness: variance 441.6, standard deviation 21.01 words.
- Vocabulary richness: TTR 0.13 across 36115 words.
- Transition rate: 0.3% of sentences.
- Passive voice rate: 5.56% of sentences.
- AI trigger baseline: 0.42 words per 1,000.
- First-person rate: 23.37 mentions per 1,000 words.
- Heading question ratio: 0.032.

### Paragraph Distribution

- under_40: 709 paragraph(s), 68.37%
- 40_to_80: 263 paragraph(s), 25.36%
- 81_to_150: 57 paragraph(s), 5.5%
- 151_to_200: 8 paragraph(s), 0.77%
- over_200: 0 paragraph(s), 0.0%

### Tone Descriptors

- balanced cadence, varied rhythm, active voice, direct, personal, plainspoken

### Signature Phrases

- `psychological safety`: 37 occurrence(s)
- `real time`: 31 occurrence(s)
- `technical art`: 25 occurrence(s)
- `lane policing`: 20 occurrence(s)
- `tools engine`: 18 occurrence(s)
- `natural language`: 16 occurrence(s)
- `game development`: 15 occurrence(s)
- `print statements`: 15 occurrence(s)
- `log file`: 14 occurrence(s)
- `maya houdini`: 14 occurrence(s)
- `proper logging`: 13 occurrence(s)
- `root logger`: 13 occurrence(s)

### Warnings

- None
<!-- VOICE_PROFILE_END -->

---

## Described

### How the owner writes — what the numbers cannot see

**The ellipsis is a beat, not an omission.** It marks a breath, a pivot, or a swallowed clause, and it is spaced as a plain `...` with no surrounding spaces most of the time. `"Not solid things, not even particles... vibrations."` (`2026-04-08-string-theory-of-disappointment.md`). Also used to hold a list open before it lands: `"she notices every flaw, every missed beat, every small disappointment... in herself, in me, in everyone... and names it."` Preserve this. It is the single most identifying mark in the corpus.

**A long build, then a two-or-three-word landing.** Paragraphs frequently end on a fragment that does the judging. `"Wrong on both."` (`2026-07-17-lane-breaking-part-4.md`), `"He got cold feet. Didn't sign the check."` (`2026-04-17-desire-expectation-prison.md`), `"One-way street."` (`2026-07-17-lane-breaking-part-2.md`). The short sentence is almost never the first one in a paragraph.

**The one-line paragraph as a hinge.** A single sentence on its own line turns a section. `"That did not happen."` (`2026-07-17-lane-breaking-part-2.md`), `"My lane is the spaces between other lanes."` (`2026-07-17-lane-breaking-part-1.md`), `"It's faith wearing a lab coat."` (`2026-07-19-without-magical-thinking.md`). These are placed where a drafter would instead write a transition sentence.

**Judgement is stated flat and not walked back.** No "arguably", no "some might say". `"That is not about efficiency. That is about ego protection."` (`2026-07-17-lane-breaking-part-1.md`). `"That is not psychological safety. That is fear with better marketing."` (`2026-07-17-lane-breaking-part-3.md`). The naming happens in the same breath as the observation.

**The "not X, it's Y" contrast is the engine of the argument.** It appears everywhere and usually carries the thesis. `"I'm critical, not cynical"` (`2026-07-17-lane-breaking-part-4.md`); `"The kindness is not in the sugarcoating. It is in being willing to tell the truth while still having each other's backs."` (`2026-07-17-lane-breaking-part-3.md`); `"it isn't the engine, it's the armor"` (`2026-07-19-without-magical-thinking.md`). Keep it, but it should carry a real distinction, not decorate one.

**Technical detail lands inside personal writing with no apology and no bridge.** In a post about burnout, the craft arrives in full specificity: `"I overhauled the combat system from scratch, including a two-character combo where one player holds an enemy in a headlock while the other punches him in the gut"` (`2026-04-17-desire-expectation-prison.md`). The same move runs the other way: a distributed-systems post stops to describe a coworker's face watching a queue drain (`2026-07-10-swarm-doesnt-care.md`). No sentence explains why the reader is being shown this.

**Numbers arrive as receipts, tersely, with the method attached.** `"Turned a 6.7-hour sequential batch into 10 minutes with 50 workers running."` (`2026-07-10-swarm-doesnt-care.md`). Study figures get their claim stated first and the citation dropped after, `"randomized 1,802 cardiac bypass patients across six hospitals, found prayer had no effect on recovery, and the group told they were being prayed for did slightly worse"` (`2026-07-19-without-magical-thinking.md`). Numbers are never rounded up for effect and never used without the setup that makes them mean something.

**Credentials show up as scars, not as a bio line.** History enters mid-argument, attached to a specific failure: `"On Open 3D Engine, I was certain ACES was the right call... I couldn't have predicted the backlash"` (`2026-07-17-lane-breaking-part-4.md`), `"I have been guilty of doing this myself"` (`2026-07-17-lane-breaking-part-1.md`). Thirty years is mentioned, but almost always immediately before an admission of being wrong.

**"You" is the reader in the same chair, addressed directly and sometimes accused.** `"And if you catch yourself thinking 'is he talking about me?' It's not personal, and you're definitely not the only one. But yeah, that's a pretty good sign you're exactly the audience I'm writing to."` (`2026-07-17-lane-breaking-part-1.md`). Elsewhere "you" becomes a generalized second person for a shared experience: `"You probably know someone like her. Maybe you are her."` (`2026-04-08-string-theory-of-disappointment.md`).

**Asides in parentheses, dry and self-deprecating.** `"(Another day I could also tell you how this has made interviewing for new roles really difficult.)"` (`2026-07-17-lane-breaking-part-1.md`); `"something a little smarter than me remembering the right sequence at 6pm on a Friday"` (`2026-07-10-swarm-doesnt-care.md`). One per section at most, never explanatory.

**Openings drop the reader mid-position.** A claim, a scene, or an admission, never a preamble: `"I did all the terrible things."` (`2026-04-17-desire-expectation-prison.md`); `"I've spent 30 years building false realities for a living."` (`2026-07-19-without-magical-thinking.md`). The 2026 personal and opinion posts have no "in this post" and no roadmap paragraph.

**Closings hand the reader a line to carry, not a summary.** `"There is more of you than this one string."` (`2026-04-08-string-theory-of-disappointment.md`); `"I'm here to tell you to look at the walls."` (`2026-04-17-desire-expectation-prison.md`); `"the man at the front is just a man at a microphone."` (`2026-07-19-without-magical-thinking.md`). Short, concrete, and it reuses an image already established earlier in the post.

**Lists carry the taxonomy; prose carries the argument.** Bullets are reserved for enumerating symptoms, phrases people actually say, or numbered remedies, and each item is one clause: `"People stop telling you the truth about your ideas."` (`2026-07-17-lane-breaking-part-1.md`). Reasoning is never bulleted. The reverse is a tell.

**Section titles are often full sentences or fragments with attitude.** "When the Studio Goes Dark", "The part I didn't emphasize enough", "What I'm not going to pretend", "Some of them are actually trying to build God". They advance the piece rather than label it.

**Tics not to imitate.** The early technical posts open with a duplicated boilerplate "Welcome to the Co3deX" bio block and a "TL;DR (5-Minute Version)" with bold `**Problem:** / **Solution:** / **Result:**` labels; that scaffolding is dropped by the July posts and reads as template, not voice. Same for the dense bold-label bullet stacks in `2026-02-25-tool-logging-with-python.md`. Inconsistent dashes (a stray em dash in the earliest posts, non-breaking hyphens in "cross‑disciplinary") are artifacts, not style.

### What the owner does not do

- No hedging stack. Claims are made once, flatly, and defended afterward rather than pre-softened.
- No "in this post I will" roadmap, no closing recap of what was just argued.
- No motivational sign-off. Closings are stark or unresolved: `"This is not a happy-ending essay. The studio still closed."`
- No rule-of-three ornamental lists. Lists are four, five, or two items, sized by the content.
- No em dash chains. Pauses are ellipses, commas, or a full stop plus a fragment.
- No abstract exemplars. It is always a named thing: SpeedTree, ACES, HyperCard, seventy cowboy movies, `cmds.file(open=...)`.
- No praise for the reader, no "great question", no anticipated-objection theater.
- Rarely any passive construction where an actor exists; someone always did the thing.

### Three samples

**Candid personal, from `2026-04-17-desire-expectation-prison.md`:**

> I spent a year in Osaka setting up a global office. Building an MMO from scratch... real IP product development, the kind of work I had been pointing toward for years.
>
> The CEO told me he had raised fifteen million dollars. I told him to give me all of it... that moving from game operations into original IP development was expensive in ways I wasn't sure he fully understood, that the budget would compress faster than he expected, that underfunding it early was the most reliable way to kill it later. In reality I was trying to secure the 1.8 million I needed to properly start the project. I was trying to protect the thing from the gap between his stated confidence and his actual readiness.
>
> He got cold feet. Didn't sign the check.
>
> I canceled the project and came home.

**Technical explaining, from `2026-07-10-swarm-doesnt-care.md`:**

> Here's the thing I buried in Part 3 that I think is actually the whole point: BATS doesn't know or care what a worker is. A worker is just something that boots once, stays warm, and pulls jobs. I built Maya and Houdini workers first because that's what I needed. But the pattern doesn't know about Maya. It knows about "boot once, stay hot, poll for work."
>
> Here's the part most people don't expect: a Python worker that loads a model once and serves inference requests all day is architecturally identical to a Maya worker that loads a scene once and processes rock scans all day. Not similar. Identical. Same pull loop, same job queue, same priority system, same monitoring.

**Opinionated judgement, from `2026-07-17-lane-breaking-part-1.md`:**

> In practice, lane‑policing usually isn't stopping chaos. It kicks in when someone crosses an invisible status boundary.
>
> You don't hear it when an engineer comments on art. You don't hear it when design critiques narrative. Or when artists critique each other's work. You hear it when someone not in your vertical or inner-circle you trust has unexpected feedback. You hear it when someone from a "lower‑status" discipline (in that person's head) shines a light on risk, complexity, or tradeoffs in the "higher‑status" discipline. That is not about efficiency. That is about ego protection.
>
> Here's what those lane‑policing phrases actually buy you:
>
> - People stop telling you the truth about your ideas.
> - Problems get buried early and come back later when they are expensive.

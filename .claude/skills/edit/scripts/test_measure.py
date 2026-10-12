"""Tests for measure.py, the editorial pipeline's one measurement."""

from __future__ import annotations

from pathlib import Path

import measure as m

POST = """---
title: "A post"
category: life
---

# A heading that does not count

I've spent thirty years building false realities. That's the job, and I love it... most days.

> A block quote that does not count as prose.

```python
code = "does not count"
```

| a table | no |
| --- | --- |
| x | y |

- a list item, not prose
1. a numbered item, not prose

Here is a long paragraph with a link to [a source](https://example.com/a) and a footnote[^1] and a bare
URL https://example.com/b that together make three citations in this paragraph, which runs long enough to
have a few sentences in it, so that the measurement has something to measure and the words add up to more
than a handful, which matters for the paragraph-mass column that the corpus calls the most reliable tell.

Short one.

[^1]: ledger #3 - a breadcrumb, not prose
"""


# ----------------------------------------------------------------------------------------------------------------------
def test_body_text_keeps_prose_only() -> None:
    body = m.body_text(POST)
    assert "false realities" in body and "Here is a long paragraph" in body and "Short one." in body
    for gone in (
        "A heading",
        "block quote",
        "does not count",
        "a table",
        "list item",
        "numbered item",
        "breadcrumb",
        "title:",
    ):
        assert gone not in body, gone


# ----------------------------------------------------------------------------------------------------------------------
def test_metrics_counts() -> None:
    x = m.measure_text(POST)
    assert x.paragraphs == 3
    assert x.citations == 3  # one link, one footnote reference, one bare URL; the footnote definition is not prose
    assert x.ellipses == 1
    assert x.em_dashes == 0
    assert x.contractions == 2  # I've, That's
    assert x.body_words == sum(len(p.split()) for p in m.paragraphs(m.body_text(POST)))
    assert x.longest_paragraph > 60 and x.words_per_paragraph_median < x.longest_paragraph


# ----------------------------------------------------------------------------------------------------------------------
def test_words_fingerprint_ignores_paragraph_breaks_only() -> None:
    a = "One two three.\n\nFour five six.\n"
    b = "One two three. Four five six.\n"
    c = "One two three.\n\nFour five seven.\n"
    assert m.words_fingerprint(a) == m.words_fingerprint(b)
    assert m.words_fingerprint(a) != m.words_fingerprint(c)


# ----------------------------------------------------------------------------------------------------------------------
def test_rhythm_finds_flat_runs_and_isolation_candidates() -> None:
    heavy = " ".join(["word"] * 130) + ". Verdict here."
    text = "\n\n".join([heavy, heavy, heavy, "A short paragraph."])
    r = m.rhythm(text)
    assert r.counts[:3] == [132, 132, 132] and r.counts[3] == 3
    assert r.flat_runs == [(1, 3)]  # paragraphs 1-3, all over 120
    assert r.isolation_candidates == [1, 2, 3]  # each ends in a sub-25-word verdict sentence after 100+ words


# ----------------------------------------------------------------------------------------------------------------------
def test_baselines_ranges_exclusions_and_echo(tmp_path: Path) -> None:
    for slug, n in (("2026-01-01-essay-a", 30), ("2026-01-02-essay-b", 50), ("2026-01-03-howto", 400)):
        (tmp_path / f"{slug}.md").write_text(
            "---\ntitle: x\n---\n\n" + "\n\n".join(" ".join(["w"] * n) + "." for _ in range(3)) + "\n", encoding="utf-8"
        )
    report = m.baselines(
        sorted(tmp_path.glob("*.md")),
        exclude=["2026-01-03-howto"],
        command="measure.py baselines X --exclude 2026-01-03-howto",
    )
    assert report.startswith("<!-- measure.py baselines X --exclude 2026-01-03-howto -->")
    assert "2026-01-03-howto" in report and "excluded" in report  # listed as excluded, not silently dropped
    ranges = m.parse_ranges(report)
    assert ranges["body_words"][0] == 90 and ranges["body_words"][3] == 150  # the how-to's 1,200 is not in the range
    assert ranges["words_per_paragraph_mean"][0] == 30 and ranges["words_per_paragraph_mean"][3] == 50


# ----------------------------------------------------------------------------------------------------------------------
def test_draft_report_marks_out_of_range(tmp_path: Path) -> None:
    ranges = {
        "body_words": (2000, 2200, 2600, 2800),
        "words_per_paragraph_mean": (25, 28, 36, 40),
        "citations": (2, 3, 7, 9),
    }
    text = "---\nt: x\n---\n\n" + "\n\n".join(" ".join(["w"] * 70) + "." for _ in range(50)) + "\n"
    report = m.draft_report(text, ranges)
    assert "OUT" in report
    lines = {ln.split("|")[1].strip(): ln for ln in report.splitlines() if ln.startswith("| ") and "---" not in ln}
    assert "OUT" in lines["body_words"] and "OUT" in lines["words_per_paragraph_mean"]
    assert "OUT" in lines["citations"]  # zero citations is under the corpus floor too
    nl = chr(10)
    inside = m.draft_report(
        "---"
        + nl
        + "t: x"
        + nl
        + "---"
        + nl
        + nl
        + (nl + nl).join(" ".join(["w"] * 30) + " [^1]." for _ in range(80))
        + nl,
        ranges,
    )
    row = [ln for ln in inside.splitlines() if ln.startswith("| body_words")][0]
    assert "OUT" not in row  # 2,400 words at 30 a paragraph with 80 footnotes: inside min-max on length, so not OUT


# ----------------------------------------------------------------------------------------------------------------------
def test_scorecard_measures_register_drift_and_tells() -> None:
    text = (
        "---\nt: x\n---\n\n## One\n\nI've got it and it's fine, we're done here, that's that.\n\n"
        "## Two\n\nIt is not done. We do not know. It cannot be, leveraging the robust tapestry, ensuring success.\n"
    )
    s = m.scorecard(text)
    assert s.ai_vocabulary == 3  # leveraging, robust, tapestry
    assert s.participle_tells == 1  # ", ensuring success"
    assert s.sections == 2 and s.register_drift > 0.2  # contractions per sentence differ sharply between sections


# ----------------------------------------------------------------------------------------------------------------------
def test_main_subcommands_run(tmp_path: Path, capsys) -> None:
    f = tmp_path / "2026-01-01-a.md"
    f.write_text(POST, encoding="utf-8")
    assert m.main(["words", str(f)]) == 0
    assert m.main(["rhythm", str(f)]) == 0
    assert m.main(["scorecard", str(f)]) == 0
    out_md = tmp_path / "BASELINES.md"
    assert m.main(["baselines", str(f), "--output", str(out_md)]) == 0
    assert out_md.exists() and "<!-- " in out_md.read_text(encoding="utf-8")
    assert m.main(["draft", str(f), "--baselines", str(out_md)]) == 0
    assert "body_words" in capsys.readouterr().out

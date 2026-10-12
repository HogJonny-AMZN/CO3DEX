#!/usr/bin/env python3
"""The editorial pipeline's one measurement: a post's prose, in numbers, against the published corpus.

Usage::

    python measure.py baselines _posts/2026-*.md [--exclude SLUG ...] [--output BASELINES.md]
    python measure.py draft <file> --baselines BASELINES.md     # the same columns, with the corpus range and OUT
    python measure.py rhythm <file>                             # Layer 5: paragraph word counts, flat runs, isolation candidates
    python measure.py scorecard <file>                          # Layer 8's measured half
    python measure.py words <file>                              # body word count and a fingerprint that ignores paragraph breaks

Body means the prose after the front matter with code fences, tables, headings, block quotes, list items,
images, HTML, footnote definitions and comments removed. A citation is a Markdown link whose target starts with
``http``, a footnote reference ``[^n]`` in the body, or a bare URL, each counted once. Standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

__version__ = "1.0.0"

FRONT_MATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)
CODE_FENCE = re.compile(r"```.*?```", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
SKIP_LINE = re.compile(
    r"^\s*(?:#|>|\||[-*+]\s|\d+\.\s|!\[|<|\[\^[^\]]+\]:|(?:[-*_]\s*){3,}$)"
)  # the last: a thematic break
LINK_CITATION = re.compile(r"\]\(https?://[^)\s]+\)")
FOOTNOTE_REF = re.compile(r"\[\^[^\]]+\](?!:)")
BARE_URL = re.compile(r"(?<![(\]])https?://\S+")
CONTRACTION = re.compile(r"\b\w+'(?:s|re|ve|ll|d|m|t)\b", re.IGNORECASE)
SENTENCE_END = re.compile(r"[.!?](?:\s|$)")
PARTICIPLE_TELL = re.compile(
    r",\s+(?:ensuring|making|allowing|enabling|creating|leaving|turning|highlighting|demonstrating|showcasing|"
    r"underscoring|reflecting|fostering|paving)\b",
    re.IGNORECASE,
)
AI_VOCABULARY = (
    "delve",
    "tapestry",
    "leverage",
    "leveraging",
    "robust",
    "seamless",
    "seamlessly",
    "crucial",
    "landscape",
    "testament",
    "underscore",
    "underscores",
    "pivotal",
    "foster",
    "fostering",
    "navigate",
    "navigating",
    "realm",
    "embark",
    "elevate",
    "holistic",
    "synergy",
    "multifaceted",
    "nuanced",
    "intricate",
    "unlock",
    "harness",
    "game-changer",
    "groundbreaking",
    "transformative",
    "streamline",
    "paradigm",
    "resonate",
    "vibrant",
    "beacon",
)
AI_WORD = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in AI_VOCABULARY) + r")\b", re.IGNORECASE)
COLUMNS = (
    "body_words",
    "paragraphs",
    "words_per_paragraph_mean",
    "words_per_paragraph_median",
    "longest_paragraph",
    "em_dashes",
    "ellipses",
    "citations",
    "contractions_per_1k",
    "short_paragraph_ratio",
)
SHORT_PARAGRAPH = 25  # words; Layer 5 doses breaks against the corpus's share of these


# ----------------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Metrics:
    body_words: int
    paragraphs: int
    words_per_paragraph_mean: float
    words_per_paragraph_median: float
    longest_paragraph: int
    em_dashes: int
    ellipses: int
    citations: int
    contractions: int
    contractions_per_1k: float
    short_paragraph_ratio: float  # paragraphs under SHORT_PARAGRAPH words, as a share of all paragraphs


# ----------------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Rhythm:
    counts: list[int]
    flat_runs: list[tuple[int, int]]  # 1-based inclusive paragraph ranges, three or more in a row over 120 words
    isolation_candidates: list[int]  # 1-based paragraphs of 100+ words ending in a sentence under 25 words


# ----------------------------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Scorecard:
    ai_vocabulary: int
    em_dashes: int
    words_per_paragraph_mean: float
    participle_tells: int
    citations: int
    sections: int
    register_drift: float  # max minus min contractions-per-sentence across ## sections


# ----------------------------------------------------------------------------------------------------------------------
def body_text(markdown: str) -> str:
    """The prose only."""
    text = FRONT_MATTER.sub("", markdown)
    text = CODE_FENCE.sub("", text)
    text = HTML_COMMENT.sub("", text)
    kept = [line for line in text.splitlines() if not SKIP_LINE.match(line)]
    return "\n".join(kept)


# ----------------------------------------------------------------------------------------------------------------------
def paragraphs(body: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]


# ----------------------------------------------------------------------------------------------------------------------
def _words(text: str) -> list[str]:
    return text.split()


# ----------------------------------------------------------------------------------------------------------------------
def citations(body: str) -> int:
    return len(LINK_CITATION.findall(body)) + len(FOOTNOTE_REF.findall(body)) + len(BARE_URL.findall(body))


# ----------------------------------------------------------------------------------------------------------------------
def measure_text(markdown: str) -> Metrics:
    body = body_text(markdown)
    paras = paragraphs(body)
    counts = [len(_words(p)) for p in paras] or [0]
    words = sum(counts)
    contractions = len(CONTRACTION.findall(body))
    return Metrics(
        body_words=words,
        paragraphs=len(paras),
        words_per_paragraph_mean=round(words / max(1, len(paras)), 1),
        words_per_paragraph_median=float(statistics.median(counts)),
        longest_paragraph=max(counts),
        em_dashes=body.count("—"),
        ellipses=body.count("...") + body.count("…"),
        citations=citations(body),
        contractions=contractions,
        contractions_per_1k=round(1000 * contractions / max(1, words), 1),
        short_paragraph_ratio=round(sum(1 for c in counts if c < SHORT_PARAGRAPH) / max(1, len(paras)), 2)
        if paras
        else 0.0,
    )


# ----------------------------------------------------------------------------------------------------------------------
def words_fingerprint(markdown: str) -> str:
    """A hash of the body's word sequence; unchanged by paragraph breaks alone (Layer 5's zero-word-change check)."""
    return hashlib.sha256(" ".join(_words(body_text(markdown))).encode("utf-8")).hexdigest()[:16]


# ----------------------------------------------------------------------------------------------------------------------
def rhythm(markdown: str) -> Rhythm:
    paras = paragraphs(body_text(markdown))
    counts = [len(_words(p)) for p in paras]
    runs: list[tuple[int, int]] = []
    start = None
    for i, n in enumerate(counts + [0], start=1):
        if n > 120 and start is None:
            start = i
        elif n <= 120 and start is not None:
            if i - start >= 3:
                runs.append((start, i - 1))
            start = None
    candidates = []
    for i, p in enumerate(paras, start=1):
        if counts[i - 1] < 100:
            continue
        sentences = [s for s in SENTENCE_END.split(p) if s.strip()]
        if len(sentences) >= 2 and len(_words(sentences[-1])) < 25:
            candidates.append(i)
    return Rhythm(counts, runs, candidates)


# ----------------------------------------------------------------------------------------------------------------------
def scorecard(markdown: str) -> Scorecard:
    body = body_text(markdown)
    metrics = measure_text(markdown)
    # register drift: contractions per sentence, per ## section of the original (headings mark sections)
    sections = re.split(r"^##\s.*$", FRONT_MATTER.sub("", markdown), flags=re.MULTILINE)
    rates = []
    for section in sections:
        prose = body_text(section)
        n_sentences = len(SENTENCE_END.findall(prose))
        if n_sentences:
            rates.append(len(CONTRACTION.findall(prose)) / n_sentences)
    drift = round(max(rates) - min(rates), 2) if len(rates) > 1 else 0.0
    return Scorecard(
        ai_vocabulary=len(AI_WORD.findall(body)),
        em_dashes=metrics.em_dashes,
        words_per_paragraph_mean=metrics.words_per_paragraph_mean,
        participle_tells=len(PARTICIPLE_TELL.findall(body)),
        citations=metrics.citations,
        sections=len([r for r in rates]),
        register_drift=drift,
    )


# ----------------------------------------------------------------------------------------------------------------------
def baselines(paths: list[Path], exclude: list[str], command: str) -> str:
    """The corpus table as Markdown, opened by the command that made it, with the ranges as a JSON comment."""
    rows = []
    included: list[Metrics] = []
    for path in paths:
        slug = path.stem
        metrics = measure_text(path.read_text(encoding="utf-8"))
        excluded = slug in exclude
        if not excluded:
            included.append(metrics)
        rows.append((slug, metrics, excluded))
    ranges = {col: _range([getattr(x, col) for x in included]) for col in COLUMNS} if included else {}
    out = [
        f"<!-- {command} -->",
        "",
        "# Baselines",
        "",
        f"Measured by `measure.py` {__version__} over {len(included)} post(s); "
        f"{len(rows) - len(included)} excluded as technical, listed below. Regenerate with the command in the first line.",
        "",
        "| Post | " + " | ".join(COLUMNS) + " | status |",
        "| --- |" + " ---: |" * len(COLUMNS) + " --- |",
    ]
    for slug, x, excluded in rows:
        out.append(
            f"| {slug} | "
            + " | ".join(str(getattr(x, c)) for c in COLUMNS)
            + f" | {'excluded' if excluded else 'in corpus'} |"
        )
    out += [
        "",
        "## Corpus range",
        "",
        "Min and max are the hard edge (OUT beyond them); the p25–p75 band is the target (edge outside it).",
        "",
        "| Metric | Min | p25 | p75 | Max |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    out += [f"| {col} | {lo} | {p25} | {p75} | {hi} |" for col, (lo, p25, p75, hi) in ranges.items()]
    out += ["", f"<!-- ranges: {json.dumps(ranges)} -->", ""]
    return "\n".join(out)


# ----------------------------------------------------------------------------------------------------------------------
def _range(values: list[float]) -> tuple[float, float, float, float]:
    """(min, p25, p75, max); the quartiles by linear interpolation, so three or more posts give a band."""
    ordered = sorted(values)
    if len(ordered) < 3:
        return ordered[0], ordered[0], ordered[-1], ordered[-1]
    q1, _, q3 = statistics.quantiles(ordered, n=4, method="inclusive")
    return ordered[0], round(q1, 1), round(q3, 1), ordered[-1]


# ----------------------------------------------------------------------------------------------------------------------
def parse_ranges(baselines_md: str) -> dict[str, tuple[float, float, float, float]]:
    m = re.search(r"<!-- ranges: (\{.*?\}) -->", baselines_md, re.DOTALL)
    if not m:
        raise ValueError("no ranges comment in the baselines file")
    return {k: tuple(v) for k, v in json.loads(m.group(1)).items()}


# ----------------------------------------------------------------------------------------------------------------------
def draft_report(markdown: str, ranges: dict[str, tuple[float, float, float, float]]) -> str:
    x = measure_text(markdown)
    out = ["| Metric | Draft | Corpus min–max | Target p25–p75 | |", "| --- | ---: | --- | --- | --- |"]
    for col in COLUMNS:
        value = getattr(x, col)
        if col in ranges:
            lo, p25, p75, hi = ranges[col]
            flag = "OUT" if not lo <= value <= hi else ("edge" if not p25 <= value <= p75 else "")
            out.append(f"| {col} | {value} | {lo}–{hi} | {p25}–{p75} | {flag} |")
        else:
            out.append(f"| {col} | {value} | | | |")
    return "\n".join(out)


# ----------------------------------------------------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("baselines")
    b.add_argument("posts", nargs="+", type=Path)
    b.add_argument("--exclude", nargs="*", default=[], metavar="SLUG")
    b.add_argument("--output", type=Path)
    d = sub.add_parser("draft")
    d.add_argument("file", type=Path)
    d.add_argument("--baselines", type=Path, required=True)
    for name in ("rhythm", "scorecard", "words"):
        sub.add_parser(name).add_argument("file", type=Path)
    args = parser.parse_args(argv)

    if args.cmd == "baselines":
        shown = " ".join(
            ["measure.py baselines", *(str(p).replace("\\", "/") for p in args.posts)]
            + (["--exclude", *args.exclude] if args.exclude else [])
        )
        report = baselines(sorted(args.posts), args.exclude, shown)
        if args.output:
            args.output.write_text(report, encoding="utf-8")
            print(f"{args.output}\t{len(report.splitlines())} lines")
        else:
            sys.stdout.write(report)
        return 0
    text = args.file.read_text(encoding="utf-8")
    if args.cmd == "draft":
        sys.stdout.write(draft_report(text, parse_ranges(args.baselines.read_text(encoding="utf-8"))) + "\n")
    elif args.cmd == "rhythm":
        r = rhythm(text)
        for i, n in enumerate(r.counts, start=1):
            print(f"{i:3d}  {n:4d}  {'#' * (n // 10)}")
        print(f"flat runs (3+ over 120): {r.flat_runs or 'none'}")
        print(f"isolation candidates (100+ words ending in a sub-25-word sentence): {r.isolation_candidates or 'none'}")
    elif args.cmd == "scorecard":
        for k, v in asdict(scorecard(text)).items():
            print(f"{k}\t{v}")
    elif args.cmd == "words":
        x = measure_text(text)
        print(f"body_words\t{x.body_words}\nparagraphs\t{x.paragraphs}\nfingerprint\t{words_fingerprint(text)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

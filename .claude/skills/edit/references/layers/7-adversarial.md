# Layer 7 · Adversarial — Opus 5 (argument posts only)

Attack the conclusion, not the prose. Runs when the post argues a position the author holds, especially one
where the author is the protagonist of their own reasoning ("I did this differently and you should too" is
one). The coordinator runs it with `--argument`, or when the Layer 1 reviewer says the post argues.

## Inputs

- The draft.
- The plan file.

## The five questions

1. **Does the frame apply to the author now?** A piece explaining why other people believe things uncritically
   must audit the author's current position with the same specificity, or readers feel it early.
2. **What would falsify the thesis?** If no evidence would count, the claim is unfalsifiable.
3. **Where is the steelman?** The person who did the work and reached the other conclusion. Arguing against
   the weak version is not arguing.
4. **Is the sequence honest?** Did the reasoning come before the conclusion, or after it as justification?
5. **Do the cited sources cut both ways?** Research about motivated reasoning applies to the author too.

## Output

- Appended to the plan file; **the draft is not edited by this layer**. Edits it recommends go through Layer 2
  (structure) or Layer 9 (the author).

```text
## Layer 7 — Adversarial (round r)

| Question | Finding | Where (quote) | Recommendation: narrow the thesis / add the steelman / cut the concession / leave |
| --- | --- | --- | --- |
```

## The trap

Do not recommend the "of course, I have my own biases" paragraph. Pre-exposing a weakened criticism with a ready
rebuttal is attitude inoculation, the mechanism these posts usually criticise. A concession must cost something
specific or it should not be there. If no real concession exists, recommend narrowing the thesis instead of
faking humility.

Reply with the count of findings and which questions they fall under, nothing else.

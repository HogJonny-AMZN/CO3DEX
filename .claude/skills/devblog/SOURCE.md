# Source

**Original to this repository**, written 2026-09-13 for the devblog design kept in the SpriteJammer repository
(`docs/design/devblog.md`, locked by the owner the same day):

- `SKILL.md` — the coordinator
- `references/CRAFT.md`, `references/AUDIENCE.md` — written by hand
- `references/VOICE.md` — measured half from `blog-style`'s `style_learn.py` over the twelve 2026 posts; described
  half by Opus 5 reading the same posts; assembled by hand
- `references/passes/1-research.md` … `8-score.md` — one brief per pass
- `scripts/session_text.py` and `scripts/scan_public.py`, with their tests — standard library only

**Vendored skills the passes invoke**, each pinned in its own folder's `SOURCE.md` with its licence:

| Skill | Pass | Upstream |
| --- | --- | --- |
| `made-to-stick`, `storybrand-messaging`, `contagious` | 2 | wondelai/skills, MIT |
| `blog-factcheck` | 6 | AgriciDaniel/claude-blog, MIT |
| `humanizer` | 7 | blader/humanizer, MIT |
| `stop-slop` | 8 | hardikpandya/stop-slop, MIT |
| `blog-style` | building `VOICE.md`, locally only | AgriciDaniel/claude-blog, MIT |
| `blog-persona` | not used by the passes; installed for its tone dimensions | AgriciDaniel/claude-blog, MIT |

Pass 4 (fresh reader) is written from the idea of Anthropic's `doc-coauthoring` skill, and pass 5 (cut) from
Strunk's public-domain rules; neither skill is vendored (licence unconfirmed in both cases).

## Tests

```bash
uv run --no-project --with pytest pytest .claude/skills/devblog/scripts/
```

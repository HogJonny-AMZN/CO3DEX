# SpriteJammer timeline

One dated line per milestone, each with its source, extended by every devblog run. Sources are stable identifiers into the SpriteJammer repository: a journal file and heading, a benchmark file, an ADR, a commit hash, or a session id and time.

- 2026-09-06 17:08 — First prompt: a 2.5D HDR metroidvania engine over wgpu/Python/PySide6 — session 872aa807
- 2026-09-06 17:27 — Pivot to a horde-arena survivors-like ("the hundred man march" × Smash TV); `docs/` established as managed context — session 872aa807
- 2026-09-06 (session 1) — Twelve ADRs drafted; the causal chain (10k agents → GPU Swarm → no swappable core) written down as the central bet — journal/2026-09-06-project-kickoff.md
- 2026-09-06 — `docs/handoffs/CURRENT.md` established after two VS Code reload session losses — journal/2026-09-06-impostors-and-handoffs.md
- 2026-09-06 (session 2) — External adversarial architecture review commissioned and absorbed; ADR-012 found factually wrong; `Contested by:` header convention introduced — journal/2026-09-06-external-review-response.md
- 2026-09-06 (session 3) — S0 measures the horde tick at 19.6 ms uniform / 1.97 ms with Behavior LOD + Numba, refuting three independent estimates — benchmarks/2026-09-06-s0-cpu-horde-baseline.md
- 2026-09-06 — ADR-018 (CPU-resident swarm) supersedes ADR-003; ADR-008 no longer conditional — ADR-README.md
- 2026-09-06 — Definition of Done and the autonomy protocol recorded; journal changed to continuous per-session cadence — journal/2026-09-06-session-03.md
- 2026-09-06 — S7 impostor bake measures 25 MB, and a fill-rate metric is caught rewarding a distorted asset — benchmarks/2026-09-06-s7-impostor-bake.md
- 2026-09-06 — CI stood up; first run fails on both platforms on a gitignored-locally link — journal/2026-09-06-session-04.md
- 2026-09-07 — M1–M6 built as thin vertical slices; M1 window paces at 120 fps, M4 draws 20,000–100,000 agents, M6 lands the horde (80,000 at 71 fps) — benchmarks/2026-09-06-m1-window-and-pacing.md, 2026-09-07-m6-the-horde.md
- 2026-09-07 — "This is a research project ... if it ever becomes fun we will talk otherwise"; M7 withdrawn as a game-design gate — session 872aa807, 2026-09-08 01:08
- 2026-09-07 — S3, the deferred renderer's first increment, measures 500 lights at 2.07 ms and finds `hog_color`'s AgX oracle clips all HDR — benchmarks/2026-09-07-s3-deferred-hdr.md
- 2026-09-08 — Camera decided by measurement rather than preference: ADR-022, the 18° "long lens," closes gate G1 — journal/2026-09-06-session-04.md
- 2026-09-08 — ADR-023 retires `Plate`/`Layer Transition`, reassigns `Layer` to LargeWorlds' meaning, and establishes the one-`Deck` walkable-surface model — ADR-README.md
- 2026-09-08 (session 5) — The platform tile model (G4) derived from the owner's SC2 domain knowledge, corrected many times, settling on 25 tiles / 6 seams — journal/2026-09-08-session-05.md
- 2026-09-08–09 — Crowd tuning: jitter chased through six wrong metrics before landing on separation-force overshoot; the "breathing" ring diagnosed as a feedback loop — journal/2026-09-08-session-05.md
- 2026-09-09 (session 7) — S13 measures animation at horde scale: rigid-part draws are 4.3× over budget, the same articulation via skinning is 1.46×; bone budget ~26 at 20,000 agents — benchmarks/2026-09-09-s13-animation-at-horde-scale.md
- 2026-09-09/10 — The animation research session's worktree is removed while the session runs inside it; the session is lost and later recovered from its transcript — journal/2026-09-10-session-09.md
- 2026-09-10 (session 8) — P1 (the profiler) built; corrects "the sim is the entire frame" to 75–79% swarm / 20–24% render — benchmarks/2026-09-10-p1-profile-capture.md
- 2026-09-10 — P2 tunes the near tier to ≤10,000 agents; capping headcount alone triples the tick before the Mid tier is added — benchmarks/2026-09-10-p2-near-tier-and-crowd.md
- 2026-09-10 — The game gets a working title, "Oh My Horde!"; content conventions (Source/Content/Data tiers) designed — CURRENT.md § "Session 09"
- 2026-09-10/11 — CI on `main` found to have run no tests for three days; fixed and `main` protected by a ruleset requiring PRs — failure-modes.md entry 16
- 2026-09-11 — Work moves to a pull-request workflow at the owner's request; two-way-door decisions move into each PR's own Decisions table — journal/2026-09-10-session-08.md
- 2026-09-12 — The Ybot character is cooked into Content (AN12/AN13); AN14 measures the integrated animated horde at 20.93 ms p50, 4.26 ms over budget, traced to non-crowd baseline drift — benchmarks/2026-09-12-an14-animated-horde.md
- 2026-09-12 — No-AI-attribution rule adopted: work goes out under the owner's identity, no Co-Authored-By trailers or "Generated with" footers — journal/2026-09-10-session-08.md
- 2026-09-13 (session 13) — S16 command-bus spike: MEASURED PASS across direct call, MCP, and gRPC transports — benchmarks/2026-09-13-s16-command-bus.md
- 2026-09-13 — AN16 locomotion lands; a frozen-tier control found unable to distinguish its own two candidate causes, and the finding is withdrawn on review — benchmarks/2026-09-13-an16-locomotion.md
- 2026-09-13 — The devblog is requested, designed, and locked in conversation; this ledger is its first research pass — journal/2026-09-10-session-08.md

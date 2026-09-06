# A World Worth Learning

*What a world model, a neural renderer, or an "AI engine" has to have before what it makes deserves to be called a game. There is a concrete build proposal in here, under "What you would actually build." Everything before it is why that shape and not another. The long version is in the Interactive Imagination Thesis.*

*Thirty years in AAA, most of it spent in the seams between art, tools, and engine, which is exactly where generated content either integrates or falls apart. That's the bias I'm bringing.*

**If you take one line out of this: whatever you lock is what your game will be known for.**

---

## 1. A world that's different every time is disposable

The pitch for world models is infinite variety. I think infinite variety is the anti-goal, and I want to squash it early.

In a racing game, the track is the skill. You learn the corners, the braking points, which shortcut actually pays and which one only looks like it does. That intuition is the mastery, and it only accrues because the track doesn't change. Generate a new world every session and you've deleted the thing players were getting good at.

Split the genre, though, because they aren't the same bet. Gran Turismo and Forza Motorsport run on real cars and real tracks, and the mastery is learning the combination of the two: this car on this circuit, nothing transferable. Festival racing is looser on purpose. Forza Horizon and MotorStorm are about having fun with cars you already love in an environment that isn't strictly prescribing how.

Notice that both of them borrow. Nobody had to author the appeal of a 911 or the Nürburgring; that meaning arrived pre-loaded. Same trick Pokémon Go pulled with your neighborhood. And even the loose one still runs on a place you come to know. Forza Horizon players learn the map, the shortcuts, where the terrain bites. Different kind of mastery, same requirement underneath it: the world has to stay put long enough to be learned.

Novelty is cheap. Familiarity is what people come back for.

### Persistence is the brand

So a world needs a persistent, durable personality: vibe, style, art direction, the shape of the place. That isn't decoration sitting on top of the game. As a creator it's the thing I'm actually building, because it's the brand and it's the IP. It's the only thing every player holds in common, so it's the only thing anyone can recognize, argue about, share, or get good at.

A beloved experience needs accumulated progress. Both kinds: what the player has earned, and what the player has learned.

The best illustration I know is the mind game in *Ender's Game*, the school's evaluation program that reshapes itself around whichever kid is playing it. It adapted to him, generated new challenges, pulled imagery straight out of his actual life. But it persisted. He killed the giant and the corpse was still there, rotting, the next time he showed up. Familiar and durable and adaptive and hostile, all at once. He kept going back.

Genie holds world state for minutes. The mind game held it for a childhood, and its hook was everything it remembered about him.

## 2. Constraint is the thing

Almost everything we think we know about making great games is a theory about constraint. Interesting choices need something to push against. Chess, Go, Tetris: tiny rulesets, enormous depth.

So if we're moving into a medium where any constraint can be removed on demand, does what we know still hold?

It holds harder, not less.

> Great games are structured constraints and clear intent, tuned by feel, and finished by the player.

Two of those four are authorable. Two aren't. And if any constraint can be removed on demand, then choosing which ones to keep stops being a limitation you work around and becomes the entire job.

Which is what premise one already was, stated generally. A persistent world is a constraint I'm choosing to keep, on purpose, because the thing players get good at is the thing that stays put.

## 3. The baseline

Right now the loop is:

```text
Prompt -> marvel -> walk around -> leave
```

It has to become:

```text
Instant premise -> immediate agency -> meaningful challenge ->
surprising or expressive outcome -> share/remix/retry
```

That's the bar. A short-form experience can run a very small version of every step, but it can't skip one. How small the kernel can get:

- One movement language.
- One or two decisions worth making, expressive or tactical.
- A readable objective.
- A bounded session.
- A visible outcome.
- A reason to retry, send, remix, or compare. Any one of those will do.

And a second bar sits on top of the first:

> AI earns its place when it creates an interaction that is newly possible, not merely a more abundant version of existing content.

Clear the first bar and you've made a game. Clear the second and you've made one worth generating.

---

## Where world models actually are

World models feel interactive. They don't yet provide durable state, explicit rules, readable challenge, authored possibility space, or reliable multi-agent dynamics.

Coherence buys you an environment that holds still while somebody moves through it. It doesn't buy reachability, fairness, scoring, anti-cheat, frame pacing, persistence between sessions, or any reason to come back tomorrow.

That gap isn't fidelity, and it won't close because the renderer got better. Every item on both lists is a property of a system, not a property of an image.

### Accumulation, and where it has to live

Durability is the floor, not the goal. A save file is durable. A save file that changes what the game does next is accumulating.

That puts a problem in front of the short-form bet. Short form is where the technology actually works right now, and short form is disposable by design. Ninety seconds, share it, gone. If accumulation is what hooks people, the hook can't live inside the session. It has to live in the player's record across sessions: their runs, their friends' ghosts, what the system already knows they've beaten.

I'm not certain that's enough. It might be a leaderboard with extra steps. It's the only place left to put it, though, so it's where I'd look first.

### Distinctiveness

A model trained on shipped games hands back the average of shipped games, so it is very good at competent and structurally bad at distinctive. Games don't win on competent.

And visual quality was never photoreal anyway. Fall Guys has enormous visual quality: distinct, memorable, a flavor you could pick out of a lineup at a glance. Photoreal is simultaneously where generation is strongest and where the output is most interchangeable.

What stays hard regardless of pipeline:

- Whether the look is distinct enough that anybody recognizes it.
- Whether it holds together across a session and between players.
- Rigging and animation, the moment a player is controlling a character, because that's the control path and it has to sync to input and collision.
- AI is not the arbiter of whether output meets the project's aesthetic standard. That judgment belongs to whoever holds the creative brief.

One boundary, stated plainly: performance, controls, and collision are real reasons for the engine to remain the source of truth, and none of them are visual quality. Different argument.

### The contract

A game has to know all of this, inspectably and reproducibly.

- What exists.
- What changed.
- Who owns it, and who's allowed to affect it.
- What an object affords.
- Which rules apply.
- What's been saved.
- What every networked player agrees actually happened. That's the hard one.
- Whether an action is legal, reachable, fair, and performant.

A neural representation can render a gorgeous rock face. The game system still has to know whether it's climbable, destructible, blocking line of sight, feeding navigation, replicated to other players, and preserved in a save.

Explicit state isn't technical debt to pay down. It's load-bearing.

### Feel is a latency budget

For twitch experiences the critical loop stays local-first:

```text
Controller input -> local simulation tick -> gameplay/physics state -> frame
```

"Tuned by feel" isn't a figure of speech. It's that path, measured in milliseconds, and nothing generated in a datacenter gets to sit inside it.

Fighters, action games, high-skill racers, precision platformers, shooters, VR, anything responsiveness-sensitive gets real value out of predictable local execution. And it isn't only controller latency; it's frame pacing, input sampling, animation timing, collision, camera behavior, deterministic rules, rendering, display latency, and multiplayer trust.

---

## What you'd actually build

Block out a world. Real geometry, by hand. Tag it semantically, and let AI do most of that labor, because annotating a city block is exactly the tedious pass agentic editor tooling is already good at. Then place context into the world: what a place is, what it means, what the model needs to understand to stay coherent, with layers for vibe and art direction alongside the functional ones.

Then decide what's locked.

The road layout is locked. Same city, same intersections, same racing line, every time. Storefronts, billboards, the art direction that makes it read as one coherent place: locked. But the gas station on that corner is open, and it can be something else next week.

Those locks aren't only technical guarantees. They're the brand. They're the only thing every player holds in common, so they're the only thing anybody can recognize, meme, or miss when it's gone. **Whatever you lock is what your game will be known for.**

That's the whole architecture in one line: generation varies the context, the game system holds the contract.

The reference to beat isn't hypothetical. Forza Horizon 6 shipped in May 2026 with dynamic conditions, seasonal variation, rival ghosts, and an EventLab creation suite where players build custom events together in the open world and publish them by share code. No generative AI anywhere in that list.

So Forza Horizon varies conditions on a track a designer built. Generate the track itself and you still have to prove it's raceable and fair before anyone drives it. That's the hard part, that's the guarantee, and it's the only thing on offer here that Forza Horizon doesn't already do.

The emotional payload doesn't come from the generator either. The player walks in carrying it. Generation just has to aim.

## Selection is the new bottleneck

Long-form games require authorship over pacing, progression, systemic coherence, and emotional intent. AI can make more possibilities than any human can evaluate, which makes taste and selection more scarce, not less.

When generation is cheap, the bottleneck moves to selection. Choosing which constraints to keep and choosing which of ten plausible outputs belongs are the same job at opposite ends of the pipeline.

Nobody has good tooling for the second one. I don't either, and building tools is what I do for a living.

## What success looks like

If this works, here's what I think it actually looks like. Not a model that replaces the creator, but four kinds of memory the system holds on the creator's behalf.

1. **Project memory** — world canon, technical constraints, mechanics, asset lineage, decisions, and state.
2. **Taste memory** — what the creator rejects, what the project means by "generic," the visual grammar, pacing preferences, and intended emotional effect.
3. **Production memory** — project files, branches, builds, task dependencies, budgets, known defects, test results, and safe change boundaries.
4. **Player-model memory** — what players learn, misunderstand, exploit, abandon, return to, love, and share.

The fourth one is the answer to the disposability problem. If the session is short and throwaway, accumulation has to live somewhere other than the terrain: in the record of what a player has learned and earned across every visit.

None of that is AI having passion. It's a creator with better tools having more capacity to realize a specific intention.

---

## What it costs

Runtime generation shifts cost from a fixed production expense to a variable per-session one, and the industry has no pricing model for that. Two precedents: Stadia never built the library or the player trust to justify its infrastructure cost, and Crackdown 3's cloud physics shipped as a reduced version of the E3 2015 demo. In both cases the compute wasn't the hard part, but it was sitting in the denominator.

And abundance isn't the win. Content abundance creates a discovery, curation, moderation, IP, and quality problem. More isn't the same as better, and past a certain point more is actively worse, because nobody can find anything. A platform only matters if players want the new interaction, not because the technology is impressive.

## The test

Holding a world model coherent for five minutes is a research milestone. Making five minutes worth shipping is a product.

The distance between those two is the whole conversation.

## What I'm asking for

**Player/design** — which candidate experience contains a real repeatable loop, rather than an AI novelty demo?

**Engineering** — which architectural claims here are sound, premature, or missing? Especially around state, latency, validation, and runtime authority.

**Business/data** — who's the initial customer, what's the measurable value, and what evidence would falsify this fastest and cheapest?

**Art direction** — what's the actual vibe? Not photoreal, not "high quality," but a specific style and tone somebody could pick out of a lineup. That's brand development, it's a real workstream with real people on it, and it has to start ahead of the tech instead of getting retrofitted onto a demo.

**Locks and IP** — what gets locked and what gets generated? That call is an engineering decision and a brand decision at the same time, and I don't think I should be making it alone.

**Legal and clearance** — what's the tooling that keeps generated content inside boundaries somebody has actually cleared? Car manufacturers control whether you can depict their vehicle at all, and plenty won't license it damaged or burning. That's why GTA builds its own marques that rhyme with the cars you love instead of licensing the real ones. Landmarks are the same problem. So are likenesses. Game development already has a rigorous, well-tested process for all of this, and a generative system that can produce "a sports car" or "a famous building" on demand has no idea what it just made. The moment you distribute this as a product you hit that wall, definitively.

**Experiment** — what's the smallest prototype that could tell a new interactive medium apart from an attractive generated environment?

One concrete starting point: pick a constrained player fantasy, something like a Crazy Taxi × MotorStorm driving event, and define:

- The fixed conventional gameplay kernel.
- The AI-generated or AI-assisted layer.
- The player value you can't get out of ordinary authored content.
- The durable hook: what accumulates across sessions, and where it lives if the session itself is disposable.
- The success metrics.
- The technical and product assumptions most worth falsifying.

---

Whatever we lock is what this gets known for. That's the decision I care most about getting right, and it's the one I'd rather not make by myself.

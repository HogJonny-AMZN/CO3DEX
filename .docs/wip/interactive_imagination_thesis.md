# The Interactive Imagination Thesis
## From Prompt Worlds to Playable Worlds

**Status:** Working draft — August 2027  
**Audience:** Game-development engineering, game design, engineering/data-science  
**What this is:** A thought-train, not a pitch. First stabs at working out whether there's anything real here, written mostly to find out what I actually think. Where I'm guessing, I've said so. If a piece of it is useful, take the piece and leave the rest.  
**Vantage:** Dated slightly ahead on purpose. Writing from just past the present forces the argument to commit to what will have settled, rather than hedging everything in the present tense. Read the dates as claims, not decoration.

---

## Executive thesis

**The engine does not die. It becomes a compiler for intent.**

That's the thesis. The rest of this memo is about what that compiler has to guarantee, and what it should never be allowed near.

Two bars. Clear neither and it's a demo, not a product:

1. **Creator leverage:** It lets a creator or team make a better, more specific, more polished game than they otherwise could (not just quantity quickly, but quality).
2. **New player affordance:** It lets a player do something impossible, unaffordable, or too specific to them and the people they play with to have been authored in advance.

Bar one is settled, and I'd rather not spend this memo relitigating it. The capability is deployed, the tooling is first-party, and the productivity evidence is messier than the enthusiasm but points somewhere clear enough: generation got cheap, verification didn't, and the time comes back at the contract. What none of that evidence measures is whether the output is any *good*, which for us is the whole game. Numbers and citations are in the FAQ.

One thing to carry forward, though. Watch the perception gap, because that's the mechanism by which a room full of capable people talks itself into something working before it does.

Bar two is the actual bet. I spend most of this memo trying to break it. The claim: a new medium exists here, experiences players can enter, shape, share, and remix that couldn't have been economically authored in advance. The analogy isn't "AI makes a bigger open world." It's closer to *Pokémon Go*, where a known fantasy became newly real because a new interaction medium changed what participation felt like.

What this thesis is *not*: a claim that AI replaces game design, local hardware, deterministic simulation, or human authorship. In some of the most valuable genres, fighters and racers and precision platformers and competitive shooters, the conventional local-first runtime matters more, not less.

For twitch games I'm not sure this premise transfers at all. That's probably its own exploration doc.

The central question stays fixed throughout:

> What does AI make valuable that is not already better served by a conventional game and conventional development pipeline?

---

## The thing I'm actually trying to work out

Almost everything we think we know about making great games is a theory about constraint. Interesting choices need something to push against. Chess, Go, Tetris: tiny rulesets, enormous depth.

So if we're moving into a medium where *any* constraint can be removed on demand, does what we know still hold?

I think it holds harder, not less.

> Great games are structured constraints and clear intent, tuned by feel, and finished by the player.

Two of those four are authorable. Two aren't. That split is the same line this memo keeps drawing. The design theory behind it, and where I think it's incomplete, is in the Adversarial FAQ.

---

## The north stars

Start with what’s real. Build to what’s bet.

### 1. Now (2027): AI-augmented game production

The 2025–2026 experimental phase is the floor. Unreal Engine 5.x ships a first-party MCP plugin — an MCP server inside the editor process. Claude Code, Cursor, or any MCP-compatible agent spawns actors, configures lighting, creates material instances, inspects Slate widgets, and runs automation tests on your behalf. Epic put it in the engine. The debate about whether agentic tooling belongs in a production pipeline is over.

The caveats that shipped with it are still this memo’s thesis in compressed form: local connections only, no auth layer, APIs subject to change. The capability arrived before the contract did. That gap is the work.

The production quality contract:

- Art-directable. Not a one-shot output you either take or throw away.
- Preserves the project's style, lore, and design grammar.
- Editable in engine-native representations, in the tools people already have open.
- Performant, streamable, collision-aware, nav-aware, actually compatible with gameplay.
- Plays nice with animation, rigging, LODs, materials, lighting, platform constraints, version control. All of it, not most of it.
- Survives iteration. Change it twice and it shouldn't quietly break semantic or technical intent.
- Validates, profiles, packages, ships.

The question was never “can AI generate an attractive scene?” It is:

> Can a creator direct an AI-assisted production apparatus to make a valid, performant, art-directed playable world that is consistent with the game they are actually building?

### 2. Near-term (2027–2029): playable, shareable interactive objects

World-model demonstrations showed what was possible — prompt a small coherent environment and immediately walk, jump, fly, drive, or inhabit it. The reference point is DeepMind’s Genie 3, announced August 2025 and available to Google AI Ultra subscribers as “Project Genie” in early 2026. Navigable worlds in real time, world state held for minutes rather than seconds.

It ran at 720p and 24fps, and “minutes” was the memory horizon. Hold those two apart, though, because they aren't the same kind of number. Fidelity is a gap that closes on its own as models and hardware improve, and that is already true. The memory horizon is a different problem: where it sits decides what you're allowed to build within that constraint. Remarkable as generation either way, and nowhere near the contract a game runtime has to honor.

They feel interactive. They don’t yet provide durable state, explicit rules, readable challenge, authored possibility space, or reliable multi-agent dynamics.

But I don't want to oversell the memory horizon as a problem, because for this particular product class it isn't one. Short form runs from about a minute at the low end out to three or five. If a world model can hold a large world coherently for three to five minutes, it has *met* the session length rather than fallen short of it. The horizon and the target are the same number. That's the actual reason to look at short form first, and it isn't modesty.

The catch is that a coherent three minute world still isn't a shippable game world. Coherence buys you an environment that holds still while somebody moves through it. It doesn't buy reachability, fairness, scoring, anti-cheat, frame pacing, persistence between sessions, or any reason to come back tomorrow. Every one of those sits on the conventional layer's list, and not one of them gets easier because the generated part got good.

Holding a world model coherent for five minutes is a research milestone. Making five minutes worth shipping is a product. The distance between those two is most of this memo.

The near-term product that works is constrained, socially legible, and playable:

- A 60 to 120 second generated obstacle descent.
- A personalized arcade delivery crisis.
- A rooftop traversal route that ends in a collaborative mural.
- A promptable party challenge with a fixed movement grammar.
- A tiny level someone can remix, make harder, theme, and fire off to a friend.

The loop must be more than:

```text
Prompt → marvel → walk around → leave
```

It needs to become:

```text
Instant premise → immediate agency → meaningful challenge →
surprising or expressive outcome → share/remix/retry
```

AI earns its place when it creates an interaction that is newly possible, not merely a more abundant version of existing content.

Which is where I have to admit a problem with my own list. Every object up there is disposable by design. Ninety seconds, share it, gone. But if accumulation is what actually hooks people, and the mind game argument later in this memo says it is, then short-form disposable objects are the *least* likely thing to hook anybody, and they're the first thing I'm proposing we build.

Maybe the accumulation doesn't have to live in the place. Maybe it lives in the player's record across places: their runs, their friends' ghosts, what the system already knows they've beaten. That would put player-model memory in charge of the durability instead of terrain. I'm not sure that's enough, and I'd rather leave it sitting here unresolved than paper over it.

### 3. Long-term (2030–2034): creator-scale, long-form games

The long-term outcome is not "one prompt makes *Red Dead Redemption 3*."

It is that a small, intensely opinionated team can make a 10–30 hour game with a level of audiovisual richness, systemic density, and production polish that historically required a much larger organization — while retaining a sharper and more personal creative voice than a risk-managed blockbuster.

That’s the harder promise to keep. Long-form games aren’t just a content problem — they require coherent authorship over time:

- Emotional and aesthetic continuity.
- Mechanical learning and mastery.
- Pacing. Pressure, recovery, surprise, comfort, in an order that means something.
- World rules the player can trust.
- Progression that changes the player's relationship to the game, not just their numbers.
- Systemic boundaries that create meaning instead of noise.
- And then the unglamorous half: testing, support, localization, performance, accessibility, maintenance.

AI can increase the number of viable possibilities. It does not automatically select the one that belongs in hour fourteen because of what the player experienced in hour two.

The case for AI in production isn’t that it has more passion. It’s that a creator can direct a much more capable apparatus while keeping a specific point of view intact.

I'll flag that this is the least evidenced claim in the memo. Nobody has done it. I picked the 10 to 30 hour figure because it sounds reasonable, not because I have anything behind it. And the whole horizon depends on a chain of things that each have to work and mostly haven't yet. I believe it. I can't show it to you.

---

## Why a new medium matters

### The Pokémon Go lesson

*Pokémon Go* didn't win on content density. A known fantasy became newly real through a medium shift — place, movement, social coincidence.

Look at what was actually non-enumerable in there: the place and the people. Niantic didn't author your neighborhood and couldn't have; there were as many maps as there were players, and that was most of the product. It didn't author the stranger you kept running into at the same gym either. The world supplied both of those, not a design doc.

That's bar two, all of it. A designer can enumerate weather, routes, difficulty, cosmetics, co-op modes. A designer can't enumerate *where you are*, *who you play with*, or *what's true this week*. Place, people, moment. Everything else in this memo is downstream of one of those three.

The third one is thinnest and the easiest to fake badly. Games already reach for it with seasons, live events, and battle passes, which is exactly the tell: an authored moment has to be planned months before the moment, and the moment doesn't wait. Whether that gap actually needs a generative system or just better ops, I genuinely don't know. I'd rather someone argue me out of it now than after we've indexed on it.

Our bet is the same shape, harder. Niantic borrowed places and people that already existed. We'd have to generate the first and earn the second.

I want to be careful with the word "real" here, because it's the wrong axis and I almost wrote it that way. Hyrule isn't real. Rapture isn't real. Nearly every place players love is synthetic and crafted by hand, so "can generated compete with real" is a bad question. The real world was never Pokémon Go's quality. It was its shortcut. Your neighborhood showed up pre-loaded with meaning, memory, and social texture that Niantic never had to author, and that's a delivery mechanism, not the thing being delivered.

The thing being delivered is whether a place hooks you, and whether it still matters on the fifth visit. That's a question about accumulation, not fidelity.

The best illustration I know is the mind game in *Ender's Game*. It adapted to him, generated new challenges, pulled imagery straight out of his actual life. But the part people skip is that it *persisted*. He killed the giant and the corpse was still there, rotting, the next time he showed up. The playground past the End of the World stayed where he left it. That's why it worked as a psychological evaluation instrument, and it's why he kept going back. It was familiar and durable and adaptive and hostile, all at once.

Genie holds world state for minutes. The mind game held it for a childhood, and then used that context. That gap isn't fidelity. It's memory, which puts accumulation right back on the contract.

That's three separate approaches to the same wall. The world model's coherence horizon is minutes. Short form is minutes, which is exactly why it's the right first target. And the mind game's hook was everything it remembered about him. Session length and durability are two different problems, and only the first one is anywhere close to solved. Which means whatever actually hooks a player is not going to live inside the session.

The lesson is:

> A smaller production can become more affecting than a larger conventional game if it creates a form of participation that was previously unavailable.

The question for AI-native experiences is the same: not "can it generate more content?" but "does it enable something conventional games cannot economically deliver?"

### The difference between the two examples

Worth sitting with: *Pokémon Go* was never pitched as a new medium. People decided it was one afterward, because it permeated. *Dreams* was pitched as a new medium and never permeated at all.

That distinction matters more here than it looks, because Dreams is much closer to this thesis than Pokémon Go is. Squint at the Interactive Imagination Thesis and you get Dreams with an LLM bolted on and the entry bar lowered. I think that's genuinely what some people expect to fall out of this exercise, and I'd rather name it than leave it under the table. If lowering the creation floor is the whole idea, then we've described a product that already shipped, got acclaimed, and closed.

So the weight lands on permeation, not capability. Everybody in this space is racing on capability and assuming speed is the constraint. It isn't. Iteration takes as long as it takes, and ideas take considerably longer than that to spread and change what people expect. We don't need a network effect on day one. We need a seed that's fun enough and viral enough that the idea catches and travels on its own. That's the part nobody is budgeting for, and it's the part that decides which of those two examples we end up resembling.

### Familiar fantasy plus new affordance

Examples:

| Reference point | Familiar fantasy | Core verb | Potential new affordance |
|---|---|---|---|
| Pokémon Go | Catch Pokémon in the world | Explore and collect | Physical place, movement, real-world social discovery |
| Arcade delivery game | Drive recklessly and deliver under pressure | Pick up, route, deliver | A city block nobody built, delivered as a valid route |
| Off-road festival racing | Survive spectacular chaotic races | Choose line, race, recover | A course no designer placed, still guaranteed fair |
| Graffiti traversal | Earn the right to leave a mark | Traverse, paint, escape | A wall that didn't exist until someone asked for it |
| LittleBigPlanet/Dreams-like creation | Turn an idea into a thing others can play | Make, remix, share | Intent becomes a validated playable draft, without the skill cliff |

Every entry in that last column is a place or artifact nobody authored. That's the through-line. If you can restate a row's affordance as "more variation on something a designer built," it belongs in a conventional game, not in this memo.


---

## The primary running example

*The driving event concept — Crazy Taxi × MotorStorm — comes from Dan's pitch. Used here as a concrete test case, not claimed as original.*

The premise is not “generate an open city and let a player drive around.” That recreates the prompt-world trap: an impressive environment with no durable reason to stay.

A better premise is:

> Drop the player into an instantly readable, high-energy driving event. Give them a clear objective, a short but expressive route choice, risk/reward shortcuts, spectacular recoveries and failures, a score or outcome worth sharing, and a reason to retry or challenge a friend.

The AI-enabled layer might create variation in:

- Event framing and destination.
- Weather, terrain, traffic, hazards, crowd spectacle, route composition, visual identity.
- Daily and weekly challenge conditions.
- Social challenge seeds, replay contexts.
- Contextual dressing and cinematic presentation. Incidental dialogue too, though that one is consent-gated under SAG-AFTRA 2025 and needs costing before anybody designs around it.

The conventional game layer still owns:

- Vehicle handling.
- Collision and physics truth.
- Camera and input feel, which is most of what people mean when they say a racer feels good.
- Route reachability.
- Score, timing, win/loss.
- Multiplayer sync.
- Anti-cheat and replay integrity.
- Performance and predictable frame pacing.

Generation varies the context. The game system holds the contract.

Take route composition and route reachability, one on each side of that line. Generation proposes the route; the conventional layer validates it before the player ever sees it.

### The obvious objection

Forza Horizon 6 shipped in May 2026. Dynamic conditions, seasonal variation, rival ghosts, festival spectacle, and an EventLab creation suite whose headline addition is Horizon CoLab: friends building custom events together in the open world, then publishing them by share code. No generative AI anywhere in that list.

That objection is correct, and it's the standard. Anything on the AI-generated list above that Forza Horizon already delivers isn't a reason to build. The only version of this worth prototyping is the one where the *thing being varied* is something a designer couldn't have enumerated in advance. If we can't name that thing in one sentence, we should kill the example and go find a better one.

Horizon CoLab varies authored parameters inside authored places. **The thing we'd be varying is the place itself.**

That's the sentence. Unpacked: the player gets a valid, performant, replayable event inside a generated context (location, terrain, environmental identity, crowd scenario) that no designer ever placed in the world. Forza Horizon varies conditions on a track a designer built. Generate the track itself and you still have to prove it's raceable and fair before anyone drives it.

If the generated context can't hold together as a playable environment, the example is dead and we find another one.

---

## The simplest version I can actually describe

Everything above is architecture talk. Here's the smallest concrete thing I can imagine that does the job, and I think it's buildable with what we have now.

Block out a world. Real geometry, by hand, the way anyone would.

Tag it semantically, and let AI do most of that labor, because annotating a city block is exactly the tedious pass bar one is already good at.

Then place context *into* the world. Not just labels. The description of what a place is, what it means, what the latent space around it needs to understand to stay coherent. Layers for vibe and visual direction alongside the functional ones.

Then decide what's locked.

The road layout is locked. Same city, same intersections, same racing line, every time. Storefronts, billboards, the art direction that makes it read as one coherent place: locked. But the gas station on that corner? Unlocked. It can be something else next week.

So far that's a creator tool, the workflow half this memo has been circling. But it's also the spine you'd need for player context injection, which I didn't see until I'd written it down.

George lives in Florida. It's hurricane season, and his mother just posted "be careful" on his feed. Anne's been working through a zombie apocalypse novel on her Kindle. They sit down to play together, and the city is overrun while they race through high wind and driving rain.

Same city. Same roads. Same handling model, same collision, same guarantee that the route is completable and the race is fair. Different world.

And here's why that lands harder than anything a designer could have scripted for them: they were already pre-wired for it. George has been half-thinking about that storm for a week. Anne's been living in that novel for three nights. Neither of them expected the game to know.

The Pokémon Go trick, showing up a second time. The system doesn't manufacture the emotional payload. The player walks in carrying it. Generation just has to aim.

### What this fixes

The lock granularity is the iteration question again, applied to space instead of artifacts. Regeneratable, constraint-annotated, promoted: the gas station, the storefront style, the road layout. Same three states, except now they're a level-design decision rather than an abstract tooling problem, which means somebody can actually author them.

Locked geometry is also what makes the conventional layer's promises keepable. Route reachability stops being a validation pass fighting a generator and becomes a property of the part nobody is allowed to regenerate. The AI works in the slots, and the slots got picked by someone who knew where the racing line went.

And it's durable and adaptive at the same time, which is the mind game. The terrain persists, so the place stays familiar and stays yours. The contents move, so it stays alive. Neither half hooks anyone on its own. Pokémon Go had this exact shape and never had to build it, because the streets came pre-locked.

### The part I don't have an answer for

Read the George and Anne example again and notice where the context came from. His mother's post. Her Kindle.

I don't think we get to do that, and I'd rather say so here than have it come up later. Reaching into somebody's social feed and reading list to season a racing game is a privacy story with an obvious headline attached, and it lands on a player base this memo has already documented as 63% hostile to generative AI and 3% positive among teenagers. Building the creepiest possible version first would be a remarkable own goal.

The defensible version uses what a player hands over on purpose, or what the platform already legitimately knows. Weather in Florida is a public API. Hurricane season is a calendar. A friend list is a friend list. And "pick tonight's vibe" is a menu, which is unglamorous and works.

I don't know where the line sits. That's a real question for this group, and it should get answered before anyone builds the demo, not after.

---

## What makes a prompt world a game?

### The minimum gameplay kernel

```text
Premise → verbs → constraints → meaningful choice →
consequence → completion/failure → replay, expression, or social response
```

For a short-form experience, the kernel may be very small:

- One movement language.
- One or two decisions worth making, expressive or tactical.
- A readable objective.
- A bounded session.
- A visible outcome.
- A reason to retry, send, remix, or compare. Any one of those will do.

### Example: graffiti traversal

“Prompt an alley, run around, paint it, share it” is a compelling creator fantasy. By itself it risks becoming a virtual painting app: novel, expressive, and technically interesting, but not necessarily a game.

The game emerges when the player must earn the canvas:

```text
See a desirable surface → read a route → traverse under pressure →
complete a constrained creative challenge → escape/reveal/score → share
```

The world generator can produce mood, architecture, prompts, props, and visual opportunity. The game system must guarantee reachability, rhythm, fair risk, readable movement, and a meaningful end state.

---

## The hybrid engine thesis

Here's the architecture I'd actually bet on, and it's boring on purpose: hybrid.

```text
Human direction, authored constraints, and creative tools
              ↓
AI planning, generation, orchestration, and iteration
              ↓
Semantic game and world representation
(entities, rules, affordances, goals, relationships, history)
              ↓
Authoritative runtime
(simulation, physics, ECS/state, saves, networking, replay)
              ↓
Hybrid presentation
(authored assets, procedural systems, generated assets,
 neural animation/rendering where appropriate)
              ↓
Human playtesting and automated evaluation
```

### Latent representations are not world truth

This is the section I expect to argue about most, so I'll be blunt. A latent world representation can be excellent at predicting, reconstructing, generating, or transforming what a place looks like. That doesn't make it a durable game world.

A game has to know all of this, inspectably and reproducibly.

- What exists.
- What changed.
- Who owns it, and who's allowed to affect it.
- What an object affords.
- Which rules apply.
- What's been saved.
- What every networked player agrees actually happened. That's the hard one.
- Whether an action is legal, reachable, fair, and performant.

A neural representation can render a gorgeous rock face. The game system still has to know whether it's climbable, destructible, paintable, blocking line of sight, feeding navigation, replicated to other players, and preserved in a save.

The counterargument is that better world models will eventually track state reliably. For single-player experiences with short sessions, maybe. Multiplayer trust, deterministic replay, and save systems are a different problem — they require every player and every server to agree on what occurred, and that agreement can't be probabilistic. Explicit state isn't technical debt to pay down; it's load-bearing.

### AI-native should not mean engine-free

An AI-native engine is an increasingly capable **intent compiler and verification environment**, not a neural replacement for all conventional engine subsystems.

That's the full production cycle. This is the authoring loop specifically:

```text
Creative intent
   ↓
AI-assisted generation and modification
   ↓
Inspectable engine-native artifacts
   ↓
Validation, profiling, build, and runtime execution
```

The output you want isn't an opaque generated video. It's a scene, mesh, material, collision proxy, animation graph, behavior tree, quest state, component definition, test case, performance budget, and build artifact that a human can open up and revise.

"Inspect and revise" means very different things across that list, though. A mesh or material you just open in tools you already know. A behavior tree is readable, but what it does at runtime isn't fully predictable from looking at its structure. A test case and a build artifact are process outputs, not creative ones. The closer a generated artifact gets to being an executable system with emergent behavior, the harder you have to constrain the generation and the more explicit the validation has to be.

### The iteration question

Say a creator gets a generated behavior tree and wants to tweak one branch. What happens? Edit it directly and you break the generation chain, because the next pass overwrites your change. Go back to the source constraints and regenerate and you probably keep the intent, but you lose the good accidents sitting next to it. Neither answer is always right.

A workable model has three states: regeneratable (untouched), constraint-annotated (the annotation survives the next generation pass), and promoted (manually locked, out of the generation chain). Which state each artifact is in has to be explicit, not assumed. That's the tooling problem, and it isn't small.

It's also not only an artifact problem, and I think that's the useful part. Those same three states are exactly what "lock the road layout, leave the gas station open" means further down in this memo. The world-space version is the easier one to get right, because a level designer already thinks in terms of what's fixed and what's dressing — the vocabulary exists, and so does the intuition. Start there. The behavior tree case is the same question with worse ergonomics and no floor plan to reason against.

---

## Hardware and runtime reality

I don't buy the cloud-only future, and I'd rather argue it in numbers than vibes. The future is heterogeneous.

### Local hardware remains essential

For twitch experiences, the critical loop must remain local-first:

```text
Controller input → local simulation tick → gameplay/physics state → frame
```

Fighters, action games, high-skill racers, precision platformers, shooters, VR, anything responsiveness-sensitive gets real value out of predictable local execution. And it isn't only controller latency; it's frame pacing, input sampling, animation timing, collision, camera behavior, deterministic rules, rendering, display latency, and multiplayer trust.

Cloud compute still earns its keep on everything without a deadline attached.

- Training models.
- Generating heavy assets or world variants.
- Large-context project agents.
- Build and test farms, same as always.
- Population-scale simulation and analytics.
- Expensive asynchronous planning, or prepping content nobody needs this frame.

Local silicon owns everything that does have one.

- High-frame-rate local rendering.
- Low-latency play.
- Bounded inference, animation, reconstruction, enhancement.
- Offline use, and the thing nobody wants to say out loud: actually owning what you bought.
- Privacy and cost control.

Cloud-rendered interactive frames aren't the model. More plausible:

> Cloud systems prepare, coordinate, and expand possibility; local hardware delivers immediate, trusted play.

---

## What must remain true

These aren't footnotes. Treat them as constraints.

### Creative discipline

- Long-form games require authorship over pacing, progression, systemic coherence, and emotional intent.
- AI can make more possibilities than any human can evaluate; taste and selection become more scarce, not less.

When generation is cheap, the bottleneck moves to selection. Which of ten plausible behavior trees belongs in hour fourteen? Which of a hundred generated environments has the right rhythm? Which AI-proposed mechanic makes the game better rather than louder? None of that answers itself. You need editorial tooling, quality screening, and a record of what the project has already rejected. The "What success looks like" section calls this taste memory. It's also probably where most of the actual design work ends up.

### Visual quality discipline

Start with what visual quality isn't: photoreal. Gen-AI can do photoreal, and photoreal was never the bar. Fall Guys has enormous visual quality. So does Tearaway. Distinct, memorable, a flavor you could pick out of a lineup at a glance. That's the bar.

Which makes this another instance of the constraint argument. A look is a set of decisions about what you're deliberately *not* doing. And a model trained on shipped games hands back the average of shipped games, which is by construction the least distinct thing on offer. Photoreal is simultaneously where generation is strongest and where the output is most interchangeable.

Here's where I need to correct my own list. If a game leans mostly on generation, including neural rendering, a chunk of the traditional production contract stops applying and I shouldn't defend it out of habit:

- LOD budgets are a rasterization concept. No mesh, nothing to LOD.
- PBR materials and light rigs are an authoring representation for a renderer that isn't in the loop anymore. Both can be semantically structured and injected as context instead.

But the *constraint class* doesn't vanish, it changes shape. Something still budgets the frame; it's resolution, model size, and sampling density rather than triangles. And consistency becomes the new hard problem, because holding a look stable across frames, across a session, and across every player's generated variant is precisely what these systems are worst at. Light rigs were one solution to a problem that still exists.

What stays hard regardless of pipeline:

- Whether the look is distinct enough that anybody recognizes it.
- Whether it holds together across a session and between players.
- Rigging and animation, the moment a player is controlling a character, because that's the control path and it has to sync to input and collision.
- AI is not the arbiter of whether output meets the project's aesthetic standard. That judgment belongs to whoever holds the creative brief.

One boundary worth stating plainly: performance, controls, and collision are real reasons for the engine to remain the source of truth, and none of them are visual quality. Different argument, different section.

### Runtime discipline

- Twitch games require local responsiveness, predictable frame pacing, and authoritative simulation.
- A fighting game’s fixed rules are part of its value; unconstrained generative mechanics undermine competitive trust.

### Product discipline

- Content abundance creates a discovery, curation, moderation, IP, and quality problem.
- A platform only matters if players want the new interaction—not because the technology is impressive.
- The two bars already carry different regulatory weight, and the storefronts have said so. Valve rewrote Steam's AI disclosure rules in January 2026 to exempt AI dev tools explicitly, on the stated grounds that efficiency gains are not what the policy is about. Player-facing generated content still requires disclosure, and games that generate content *at runtime* require a specific checkbox. Bar one is now a private production decision. Bar two is a public label on the store page. That asymmetry should inform which bet we take first and what we promise about it.

### Economic discipline

**Supply side.**

- Runtime generative compute shifts cost from a fixed production expense to a variable per-session expense. The games industry has no established pricing model for that shift. Everyone reading this already knows it. It stays on the list because it is the thing that keeps getting stepped over on the way to the demo.
- Stadia couldn't build the content library or player trust to justify its infrastructure cost. Crackdown 3's cloud physics shipped as a reduced version of what was demoed at E3 2015 — the gap reflected both technical limits and economic ones. The compute was not the hard part in either case, but it was in the denominator.
- AI generation at the authoring layer has the same cost exposure at a smaller scale. Inference costs for high-quality content are real and don't fit neatly into fixed production budgets.

**Demand side, and it's worse than the cost side for a reason most people get wrong.**

The usual worry is that players won't pay a premium for generated content. The data doesn't really back that as the main risk. Circana's December 2025 PlayerPulse found roughly a quarter of US players saying generative AI makes them less likely to buy, with most of the rest neutral or unsure. A Steam-user survey put negative reaction at 31%, but only 8% said they'd refuse to buy under any circumstance, and around 60% stay neutral as long as the finished product is good.

The damage shows up in behavior instead of stated preference. Game Oracle looked at thousands of Steam releases and found that titles disclosing AI content pull roughly **53% fewer user reviews** than comparable games. Fewer reviews means less social proof, weaker algorithmic surfacing, a smaller discovery footprint. That analysis is correlational, and disclosed titles probably skew lower-budget, so treat it as a strong flag rather than a proven cause. But it points somewhere specific. The risk isn't that players refuse to pay. It's that they never see the thing.

Sentiment gives the flag teeth. Quantic Foundry, December 2025: player attitudes 63% negative overall, rising to 77–83% against AI-generated quests and dialogue. The age curve is the part that should worry us most, because 3% of players aged 13–17 and 7% of 18–24 hold positive attitudes, against 22% of players over 45. The short-form, social, remixable object this memo is proposing points straight at the least receptive audience on that curve.

A CHI 2026 study closes the obvious escape hatch. The negative bias showed up *without* disclosure or priming at all, with player experience tracking what they believed about where content came from more than where it actually came from. You can't quietly engineer around this. And under Steam's runtime-generation rule you wouldn't be allowed to try anyway.

*Still missing and worth someone's afternoon: an actual inference-cost-per-session figure against realistic ARPU. Every number above is demand-side.*

These lead to a working principle:

> AI belongs where it expands meaningful possibility without compromising the contract that makes the experience worth trusting.

This means AI can be foundational in creator tools, development workflows, bounded social modes, adaptive training, content variation, and new forms of playable expression. It should not automatically be inserted into a ranked fighting game’s canonical combat rules or a high-skill driving game’s critical control path.

---

## The path to the north star

This is a hypothesis, not a promise. I'd rather be corrected on it now than in two years.

| Horizon | Likely capability | Role in the thesis | Confidence |
|---|---|---|---|
| 2027 (now) | AI-augmented conventional development is the baseline: agents modify Unreal projects, generate drafts, operate tools, assist code/content/QA. UE 5.x ships first-party MCP. Capability deployed; production contract is the remaining work. | The practical substrate exists, first-party. The debate is execution, not viability. | Established |
| 2027–2029 | More reliable, art-directable, performant, editable generated content within pipelines; stronger project-aware agents; first bounded playable short-form experiences that hold a repeatable loop | Production quality and creative leverage become the meaningful change | Plausible and strategically important |
| 2030–2034 | Integrated intent-driven systems that create and modify semantic scenes, logic, assets, tests, and variants; smaller teams make richer long-form work | The bridge from creator tooling to creator-scale authored games | Conditional on reliability, cost, rights, evaluation, and adoption |

The five-year milestone is not “AI independently ships a great game.” It is closer to:

> AI-assisted content, characters, worlds, and implementation become trustworthy enough that a creator can repeatedly turn directed taste into engine-quality playable work at a scale previously unavailable to them.

---

## What success looks like

If this works, here's what I think it actually looks like. Not a model that replaces the creator.

Think of it as four kinds of memory the system maintains on the creator's behalf:

1. **Project memory** — world canon, technical constraints, mechanics, asset lineage, decisions, and state.
2. **Taste memory** — what the creator rejects, what the project means by “generic,” the visual grammar, pacing preferences, and intended emotional effect.
3. **Production memory** — project files, branches, builds, task dependencies, budgets, known defects, test results, and safe change boundaries.
4. **Player-model memory** — what players learn, misunderstand, exploit, abandon, return to, love, and share.

None of that is AI having passion. It's a creator with better tools having more capacity to realize a specific intention.

---

## Initial discussion ask

This memo does not ask for agreement on a final game concept, a final model architecture, or a precise decade-long roadmap.

First, my own falsifier, so I am not outsourcing the hardest part:

> If by mid-2029 the best AI-assisted content in this pipeline still costs more engineer-hours to make production-valid than it saved in authoring hours, the contract never closed — bar one stays a wash in practice, and bar two never gets funded. That is the number I would track. Not fidelity. Not prompt-to-scene time. **Net hours to shippable.**

Then it asks the group to help answer four questions:

1. **Player/design:** Which candidate experience contains a real repeatable loop, rather than merely an AI novelty demo?
2. **Engineering:** Which architectural claims are sound, premature, or missing—especially around state, latency, validation, and runtime authority?
3. **Business/data:** Who is the initial customer, what is the measurable value, and what would falsify the thesis faster or more cheaply than the net-hours-to-shippable test above?
4. **Experiment:** What is the smallest prototype that could distinguish a new interactive medium from an attractive generated environment?

One concrete starting point: identify a constrained player fantasy — something like the Crazy Taxi × MotorStorm driving event — and define:

- The fixed conventional gameplay kernel.
- The AI-generated or AI-assisted layer.
- The player value that cannot be achieved through ordinary authored content alone.
- The durable hook: what accumulates across sessions, and where it lives if the session itself is disposable.
- The success metrics.
- The technical and product assumptions most worth falsifying.

---

# Adversarial FAQ

*Not all of this is adversarial. It's where the details, numbers, and citations live so the front half can stay short.*

## Bar one: what does the productivity evidence actually say?

Bar one is no longer in question. But be careful what "works" means here, because the evidence is messier than the enthusiasm. METR's 2025 randomized trial found experienced developers 19% *slower* with AI on mature codebases they knew cold ... and those same developers came out believing they'd been 20% faster. Telemetry across roughly ten thousand developers found the opposite sign on throughput and the same sign on cost: more tasks done, far more PRs merged, review time up 91%, bugs up 9%. DORA's 2025 report landed in the same place. Adoption raises throughput and instability together.

Those results aren't in conflict. They're one phenomenon. Generation got cheap. Verification didn't. The time comes back at the contract.

None of those studies measured quality. Completion time, PRs merged, throughput, defect counts. Every metric in that literature is a rate or a defect rate, and not one of them tells you whether the output is any *good*. Bar one, as I've written it, claims quality and not just velocity. The productivity fight is more obvious because both sides are measuring what's easy to measure.

None of that is academic for us, it's the whole crux. A model trained on shipped games gives you back the average of shipped games, which makes it very good at competent and structurally bad at distinctive. Games don't win on competent, they win when they are beloved. The fully generated titles out there right now are remix clones at casual quality, and that's exactly what regression to a training mean looks like when you point it at a medium. AI-*assisted* production is a different animal, because there the quality still belongs to whoever is directing it. Which is the entire point. Taste, selection, gating, and validation aren't friction to optimize away; they're the only place quality enters the pipeline, and no benchmark in the productivity literature is going to tell you whether you have them.

So bar one stands, with the flattery removed. The capability is deployed. The tooling is first-party. What's open is whether what comes out the far end is reliably shippable and a memorable game. And watch the perception gap, because that's the mechanism by which a room full of capable people talks itself into something working before it does.

---

## Is this just Unreal plus Claude?

Right now, largely yes, and that's not a criticism. The work is making that combination reliable, project-aware, and production-grade.

"AI-native" doesn't mean engines are invalid. It describes what happens when AI-assisted intent, generation, tooling, validation, and runtime representations become deeply integrated.

## Why would a player want prompted worlds instead of curated games?

They won't, unless the prompted experience hands them something curated games can't: immediate personal relevance, meaningful expression, social remix, a specific fantasy made playable, a shared situation nobody else got.

## Does "constraints and intent" survive a medium where any constraint can be removed?

The theory is well supported. Sid Meier's "a series of interesting choices" only works under constraint; remove it and the choices stop being interesting. Salen and Zimmerman's *Rules of Play* argues that meaningful play emerges *from* rule systems rather than despite them. The MDA framework says the designer authors mechanics while the player experiences aesthetics, which is the same claim in different clothes: you specify constraint, you don't specify experience.

So yes, it survives. But the formulation needs two more terms before it's honest.

It has no player in it. Constraints and intent describe the authored artifact, and a game only exists while somebody is playing it. Chess isn't great because of its rules. It's great because of fifteen hundred years of people playing it at each other, and no ruleset predicts that.

It has no feel in it either. Why does Mario feel good? Not because of a rule. Acceleration curves, coyote time, animation timing, which frame the input registers on. That's craft at the millisecond and it's mostly unspecifiable in advance. Costikyan would add uncertainty as a third gap: constraint builds the possibility space, but it's uncertainty inside that space that makes you lean forward.

Here's why those gaps help rather than hurt. Structured constraints and clear intent are the authorable, specifiable, structural parts, and those are exactly what generation can be pointed at. Feel, uncertainty, and whatever the players end up making of it are exactly what this memo keeps saying has to stay human and conventional.

So the theory isn't wrong and isn't quite complete, and its incompleteness falls along precisely the line the rest of this argument draws. If any constraint can be removed on demand, then choosing which ones to keep stops being a limitation you work around and becomes the entire job.

## Why not simply make more procedural content?

Both procedural and generative systems fail when they substitute quantity for authored meaning. The goal is not infinity. It is directed possibility under constraints.

## Why does a fighting game resist an AI-native core?

AI can help with training partners, replay analysis, test cases, coaching, casual modes, cosmetics, and community events. It should not freely invent canonical runtime combat behavior in ranked play.

## Could a generative fighting-game mode still be valuable?

Yes, if clearly separated from the canonical competitive contract. A social party mode, generated challenge gauntlet, adaptive training drill, or constrained custom-rule experience may be desirable precisely because it is variable.

```text
Canonical competitive mode:
  authored, deterministic, local-first, fixed rules

Generative social/training/creator mode:
  expressive, bounded, variable, explicitly non-canonical
```

## Why does local hardware remain important?

AI doesn't reduce the case for local hardware. It can increase it: creator workflows, neural enhancement, local inference, high-end rendering, and high-frame-rate interactive games all benefit from capable GPUs and NPUs.

## Does neural rendering replace assets and scenes?

Not by itself. A game runtime requires semantic objects and authorable structures. A neural representation may augment or replace portions of visual rendering, but gameplay still needs collision, navigation, interaction affordances, replication, performance budgeting, and persistence.

Neural and generative representations where they're visually valuable; conventional representations where rules, tooling, and runtime truth matter.

## What makes a short-form experience worth playing?

A clear premise, immediate agency, one satisfying skill or expressive choice, a bounded challenge, a visible outcome, and a reason to retry or share.

## What makes LittleBigPlanet and Dreams relevant?

They're the closest thing to my near-term bet that anyone has actually shipped, which is why I want to be honest about how it went.

Dreams proved that creation, remix, play, and social sharing can be a game's core identity. It was acclaimed. It had a first-party studio, Sony's backing, and no real competitor. Media Molecule ended live support on September 1, 2023, after concluding they couldn't define a sustainable path for continuing full development. The servers stayed up. The business didn't.

So it isn't just the skill cliff and the discovery problem, though both were real. The best version of this idea, built by the best team available, with patient platform money behind it, didn't find a sustainable business.

My honest read is that the creation floor was the binding constraint, and AI is a credible attack on exactly that constraint. Turning an intention into a playable draft is the thing Dreams could never quite do for people, and that's the strongest reason to think this time could go differently.

But anyone citing Dreams as encouragement without citing September 2023 is selling something.

## What does “AI makes something better for the creator” mean?

It doesn't mean the AI has more passion than the creator.

It means the creator can test more directions, manifest more of their specific taste, spend less time on commodity production work, and sustain a richer authored vision with fewer people and less capital.

I'm not going to pretend that last clause is neutral. "Fewer people" is a cost, and the people who pay it are in this building. I don't have the answer. I do think a memo that skips past it isn't worth reading.

The best outcome is not generic abundance. It is **more of the creator’s intent arriving intact in the final playable work**.

## When does this create an RDR2-scale game?

This is the wrong unit of measurement if it means reproducing every dimension of a major studio’s historical production footprint.

The more useful question is when a smaller team can make a game that is equally memorable or more personally affecting for a particular audience because AI changes what the team can realize.

AAA-quality moments, environments, characters, and vertical slices will likely arrive much earlier than coherent 50-hour systemic worlds with blockbuster-level density, stability, and long-term support.

## What remains uniquely human?

A human need not manually produce every object to remain the author.

Human work stays central in a pile of places.

- Choosing what matters.
- Establishing a world's aesthetic constitution.
- Picking between things that are all plausible.
- Designing rules and boundaries.
- Reading an audience and a cultural moment.
- Deciding what gets held back, fixed, or made by hand anyway.
- Owning the work's emotional and ethical effect. Somebody has to.

As possibility becomes cheap, selection and judgment become more valuable.

## What could make this fail?

- Generated content remains technically fragile, legally unclear, or expensive — and the compute economics of runtime generation have no established consumer pricing model. Stadia and Crackdown 3's cloud physics are failures of unit economics, not engineering ambition. Generative AI at session scale repeats that question at a different but not obviously more favorable price point.
- Models produce visual plausibility without semantic/gameplay reliability.
- Discovery collapses under content abundance.
- Platforms optimize shallow engagement instead of meaningful play.
- Creators and performers lose control, provenance, compensation, or trust. This one is neither hypothetical nor unpriced. The 2025 SAG-AFTRA agreement exists because the industry got it wrong first.
- The alleged new-medium interaction is not actually wanted by players.
- Teams confuse a prototype’s novelty with a durable game loop.

## What is the disciplined next move?

Choose one constrained hypothesis and build the smallest prototype that can falsify it.

For example:

> A short-form arcade driving experience where a conventional, responsive driving kernel is surrounded by AI-assisted event/world variation. The player must receive a unique but valid route challenge, create a memorable run, and have a strong reason to replay or share it.

Don't measure whether the system makes a beautiful city. Measure whether the player gets a repeatable, meaningful loop they couldn't get from ordinary authored content.

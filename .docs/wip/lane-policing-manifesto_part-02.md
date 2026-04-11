# Lane-Breaking: When One Lens Dominates

In Part 1 (link), I promised to pull the camera back and cover the bigger forces: fake safety vs real safety, engineering bias, stewardship, invention, all of it. One part. Neat and tidy.

That did not happen.

The more I wrote, the more the pieces refused to fit in one container. So this is now a four‑part series. I'd rather be honest about that than cram it and deliver something half-baked. In this part I'm looking at the structural forces behind lane‑policing: how specialists and multipassionates see work differently, where engineering bias comes from, and why the pattern doesn't stay inside any one discipline. The environment question... fake safety, stewardship, what kind of leadership actually works... that's Part 3.

The thing that connects all of it: whose discomfort gets treated as signal, and whose gets filed away as noise.

## Specialists, multipassionates, and how they see work

Every studio I've worked in has been built around specialists: people who go deep in a narrow domain and build rare, hard‑won expertise there. Clearly defined roles, more internal authority inside that slice, mandate to optimize for depth and precision. That focus is genuinely valuable when you're pushing a discipline to its limits... rendering, low‑level engine work, network code, animation, UX... but the same focus can make knock‑on effects in other parts of the system invisible.

I've known a lot of multipassionates and multipotentialites too. Broad, overlapping interests. Learn new domains quickly. Drawn to intersections where ideas from multiple fields collide. The [research on generalists and multipotentialites](https://www.ted.com/talks/emilie_wapnick_why_some_of_us_don_t_have_one_true_calling) consistently surfaces the same traits: idea synthesis, rapid learning, adaptability, and an ability to switch between very different modes of thinking. In complex, unpredictable environments (modern games and tools are exactly that), [broader pattern‑recognition tends to matter more than ultra‑narrow depth](https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/making-collaboration-across-functions-a-reality).

I've lived this. I can see both sides because I've been on both sides, and the tension is real. Specialists push a single pillar to world‑class levels. Multipassionates spot the weird failure modes between pillars. The problem isn't the mix. It's when the org only knows how to reward one type, and the other starts to look like a problem to be managed.

## Engineering bias: when one lens dominates

"Engineering bias" is a specific pattern I want to name carefully. Not "engineers are bad." Not "code doesn't matter." I mean technical perspectives get treated as inherently more objective and authoritative than design, art, production, or player perspectives, even on questions where those other perspectives have better information.

You see it in rooms where the default authority lives with engineering, by habit, not because the problem demands it. An engineer's intuition about UX beats a designer's research. Someone just knows better than the user study data. A clever tools architecture beats an artist's lived reality of iteration pain. A performance concern gets treated as "hard physics," while a content‑throughput concern is filed under "nice to have, if we have time." A rendering engineer says normalizing vectors in a shader is expensive, but the artist's eye clearly sees what is wrong. And looks bad.

I've lived this one directly. Years ago, we were building a demo for GDC and I wrote some shaders for paper rendering (with translucency), IBL, vertex shader animation and such, a whole visual world built around a large number of lights. The rendering engineer kept optimizing the shaders. The visual results kept taking a hit. One pass, the normals weren't normalized — you could see it immediately. At another point the translucency that had looked genuinely beautiful went flat and weird. We argued about it, more then once. Close to the GDC deadline I stopped expending energy on arguing and let him submit what he insisted was correct. Then in the packaged build, I quietly changed three key shaders back to what actually looked good. Never told anybody. All the praise for that demo was about how great it looked. He either didn't notice, didn't care, or let the feedback speak for itself. I still don't know which.

Under the hood, it's not one bias. It's a stack: confirmation bias, but for technical data. Status‑quo bias, but for the current engine and pipeline. Pro‑innovation bias, but for new tech over messy human workflows. Identity and status bias, where "the engineer in the room" is coded as more rational by default.

Stack those up, and if something sounds like an engineering problem, engineering's story is automatically more "real" than anyone else's.

For polymaths and multi‑passionate people, this is brutal. Our whole value is seeing how a decision in one lane is going to quietly detonate three lanes away. We see how a tool choice will kneecap content production six months out, how a "clean" technical abstraction will land as friction for players, how a performance budget will shape art direction and schedule. To even say those things out loud, we have to cross into engineering's domain.

Engineering bias plus lane‑policing makes that basically illegal.

Critique flowing out of engineering into art, design, production? Totally normal. "Just being realistic." Critique flowing back in from those same disciplines? Suddenly it's overreaching. "You don't understand how hard this is." "Let the engineers worry about that." One-way street.

That's the collision point with [psychological safety](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Group_Performance/Edmondson%20Psychological%20safety.pdf) \[[Edmondson, 1999](https://journals.sagepub.com/doi/10.2307/2666999)\].

If engineers have implicit veto power, everyone else learns fast that challenging technical direction, scope, or tool choices is not safe. Especially if your title doesn't say "engineer." You start self‑censoring anything that smells technical, even when the risk you're seeing is fundamentally about players, creators, visuals, or production reality.

Good teams don't eliminate engineering bias entirely. There are moments when you need someone to say "physics still applies" or "we cannot ship this if it falls over under load." The difference is whether that identity gets to override evidence from other disciplines.

What I want: engineers bring hard constraints and see classes of risk nobody else sees. Designers, artists, writers, and producers bring different constraints and different classes of risk that are just as real. And polymaths are expected, not just allowed, to connect all of that and say, "If we keep going like this, here's where the system breaks." That's not overreach. That's the job.

Engineering bias says: technical discomfort matters more than everyone else's reality.

Psychological safety says: discomfort is data, no matter whose lane it comes from.

When those two are in the same room, you find out fast whether a studio truly wants cross-functional collaboration, or whether "T-shaped" was just something they wrote on a slide.

## It's not just engineering

I'm picking on engineering bias because it's common and easy for me to see (I have lived it.) But any discipline can start believing its lens is the only real one.

I've also seen it in design and other departments. Things like "all levels must start in design," as if fun can only be born in Figma, a spec doc, or a gray‑box layout. Some of the best levels I've worked on started in art: someone gets inspired, there's concept art, someone blocks out a visual space in 3D, drops in a few props or landmarks, and suddenly you've got something walkable and vaguely playable. Rough. Not "designed" yet. But it sparks something. Design looks at that messy aesthetic inspiration, sees the potential, and builds on it: tightens the loops, tunes flow and pacing, turns a cool sketch into a layout people remember. It's not about who left the starting line. It's about who helps the thing cross the finish.

I've seen it in QA. At Rockstar, some of the sharpest creative ideas and calls came out of QA feedback. They were the ones living with the game more than eight hours a day, seeing edge cases nobody else saw, feeling where the fun dropped off or where players would push systems in ways design hadn't anticipated. That team was intentionally diverse... a poetry laureate, a business‑school grad, sports nuts, music heads, conspiracy weirdos... and that mix mattered. They weren't just bug‑finders; they were an always‑on reality check for how the game actually felt and played in the wild.

Production sees what doesn't show up in Jira tickets: patterns in schedule, scope, human bandwidth, the quiet warning signs that a team is running on fumes. Community and support see how decisions actually land, long after the feature is "done" and everyone has moved on. Marketing sometimes spots a fantasy or angle the core team is too close to see. I've had a marketing conversation reframe a whole product direction in twenty minutes. None of that happens if those voices get lane‑policed out of the room before the train hits the wall.

The moment any silo starts believing only their discipline gets to define reality, you're back to lane‑policing in a different jersey. [Psychological safety](https://pmc.ncbi.nlm.nih.gov/articles/PMC9819141/) means discomfort is treated as data no matter where it comes from. The teams that win let the best signals through, not just the ones from the "right" lane.

So that's the structural layer: specialists and multipassionates see work differently, engineering bias tilts the playing field, and the same pattern shows up anywhere a discipline decides its lens sees and knows best. Knowing that doesn't fix anything on its own. The harder question is what the environment has to look like for cross-disciplinary signal to actually survive contact with the org.

That's where Part 3 goes. There's a version of "psychological safety" that is just theater... slide decks, internal campaigns, public praise that everyone knows doesn't match the private conversation. There's a version of feedback culture that mistakes coddling for care, and ships weak work wrapped in a glossy layer of "amazing effort." And then there's the real thing, which is a lot less comfortable and a lot more useful. Part 3 also gets into something I think about a lot: the difference between stewarding something beloved and inventing something new. Those two kinds of work don't just feel different... they require fundamentally different cultures to succeed. One rewards execution and ego control. The other punishes ego and depends on an environment where people can question even the things the director believes most strongly. Getting that wrong is expensive.

\----
Part 3: (link)

---

## Resources and further reading

Links embedded in this post point to free, open-access sources wherever possible. The HBR articles below are behind a subscription paywall — I'm listing them here because they're worth reading if you have access, or can find them through a library.

**Free:**

- Emilie Wapnick — [Why some of us don't have one true calling](https://www.ted.com/talks/emilie_wapnick_why_some_of_us_don_t_have_one_true_calling) (TED talk, ~12 min)
- Amy Edmondson — [Psychological Safety and Learning Behavior in Work Teams](https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Group_Performance/Edmondson%20Psychological%20safety.pdf) (MIT-hosted PDF, 1999 original paper)
- Edmondson 1999 — [journal record](https://journals.sagepub.com/doi/10.2307/2666999) (Sage, abstract free)
- McKinsey — [Making collaboration across functions a reality](https://www.mckinsey.com/capabilities/people-and-organizational-performance/our-insights/making-collaboration-across-functions-a-reality)
- PMC — [Psychological Safety and Management Team Effectiveness](https://pmc.ncbi.nlm.nih.gov/articles/PMC9819141/) (open-access, peer-reviewed)

**Further reading (HBR — subscription required):**

- [Why Cross-Functional Collaboration Stalls, and How to Fix It](https://hbr.org/2024/06/why-cross-functional-collaboration-stalls-and-how-to-fix-it) (2024)
- [What Is Psychological Safety?](https://hbr.org/2023/02/what-is-psychological-safety) (2023)
- [Research: To Excel, Diverse Teams Need Psychological Safety](https://hbr.org/2022/03/research-to-excel-diverse-teams-need-psychological-safety) (2022)
- [75% of Cross-Functional Teams Are Dysfunctional](https://hbr.org/2015/06/75-of-cross-functional-teams-are-dysfunctional) (2015)

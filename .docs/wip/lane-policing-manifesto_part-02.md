# Lane-Breaking: When One Lens Dominates

In Part 1 (link), I promised to pull the camera back and cover the bigger forces: fake safety vs real safety, engineering bias, stewardship, invention, all of it. One part. Neat and tidy.

That did not happen.

The more I wrote, the more the pieces refused to fit in one container. So this is now a four‑part series. I'd rather be honest about that than cram it and deliver something half-baked. In this part — Part 2 — I'm looking at the structural forces behind lane‑policing: how specialists and multipassionates see work differently, where engineering bias actually comes from, and why this pattern doesn't stay inside any one discipline. The environment question — fake safety, stewardship, what kind of leadership actually works — that's Part 3.

## Specialists, multipassionates, and how they see work

Most studios are still architected around specialists: people who go deep in a narrow domain and build rare, hard‑won expertise there. In organizations, specialists tend to have clearly defined roles, more internal power inside that slice, and a mandate to optimize for depth, precision, and efficiency within their lane. That focus is incredibly valuable when you are pushing the limits of a discipline: rendering, low‑level engine work, network code, animation, UX; but the same focus can make it harder to see knock‑on effects in other parts of the system.

Multipassionates and multipotentialites sit at the other end of the spectrum. They tend to have broad, overlapping interests, learn new domains quickly, and are drawn to work at the intersections where ideas from multiple fields collide. Research on [generalists and “multipotentialites”](https://www.youtube.com/watch?v=7WuwNRycEQA) consistently highlights traits like idea synthesis (combining concepts from different disciplines), rapid learning, adaptability, and an ability to switch between very different modes of thinking as situations change. In complex, unpredictable environments; exactly the kind of environments modern games and tools live in.  [Organizations often get more value](https://iiardjournals.org/get/IJSSMR/VOL.%2011%20NO.%2010%202025/Cross-Functional%20Team%20Collaboration%20272-284.pdf) when leaders have this broader pattern‑recognition rather than ultra‑narrow expertise.

Neither profile is “better” in the abstract; they see different parts of the same landscape. Specialists excel at pushing a single pillar to world‑class levels, but may miss cross‑team dependencies or human factors outside their remit. Multipassionates are wired to scan across pillars, spot weird failure modes between them, and prototype new combinations, but they can look threatening or “unfocused” inside systems that only know how to reward single‑lane depth. When those two ways of seeing are allowed to coexist with psychological safety, you get small, sharp teams that can both build deep technology and steer around the walls everyone else hits too late.

## Engineering bias: when one lens dominates

Let’s talk about “engineering bias.” I don’t mean “engineers are bad” or “code doesn’t matter.” I mean a specific pattern: technical perspectives get treated as inherently more objective and authoritative than design, art, production, or player perspectives, even on questions where those other perspectives have better information.

You see it in rooms where the default authority lives with engineering, by habit, not because the problem truly demands it. An engineer’s intuition about UX beats a designer’s research. Someone knows better than the user-study data. A clever tools architecture beats an artist’s lived reality of iteration pain. A performance concern gets treated as “hard physics,” while a content‑throughput concern is filed under “nice to have, if we have time.” A rendering engineer says normalizing vectors in a shader is expensive, but the artist's eye clearly sees what is wrong (and looks bad.)

Under the hood, it’s not one bias. It’s a stack. Confirmation bias, but for technical data. Status‑quo bias, but for the current engine and pipeline. Pro‑innovation bias, but for new tech over messy human workflows. Identity and status bias, where “the engineer in the room” is coded as more rational by default.

The result is simple: if something sounds like an engineering problem, engineering’s story is automatically more “real” than anyone else’s.

For polymaths and multi‑passionate people, this is brutal. Our whole value is that we can see how a decision in one lane is going to quietly detonate three lanes away. We see how a tool choice will kneecap content production six months from now, how a “clean” technical abstraction will land as friction for players, how a performance budget decision will shape art direction and schedule. Fixing bad shading visuals without requiring permission. To even say those things out loud, we have to cross into engineering’s domain.

Engineering bias plus lane‑policing makes that basically illegal.

Critique flowing out of engineering into art, design, production? Totally normal. “Just being realistic.” Critique flowing into engineering from those same disciplines? Suddenly it’s overreaching. “You don’t understand how hard this is.” “Let the engineers worry about that.” The direction of acceptable criticism becomes a one‑way street.

That’s where this collides directly with [psychological safety](https://amycedmondson.com/psychological-safety/) \[[alt](https://journals.sagepub.com/doi/10.2307/2666999)\].

If engineers have implicit veto power, everyone else learns very fast that challenging technical direction, scope, or tool choices is not safe. Especially if your title doesn’t say “engineer,” or if your value comes from living at the intersections. You start self‑censoring anything that smells technical, even when the risk you’re seeing is fundamentally about players, creators, visuals or production reality.

Healthy teams don’t get rid of engineering bias entirely. There are moments when you really do need someone to say, “Physics still applies,” or “We cannot ship this if it falls over under load.” What they don’t do is let that identity override evidence from other disciplines.

The version I want looks more like this:

- Engineers bring hard constraints and see classes of risk nobody else sees.  
- Designers, artists, writers, and producers bring different constraints and see different classes of risk that are just as real.  
- Polymaths and cross‑disciplinary folks are allowed – expected – to connect all of those and say, “If we keep going like this, here’s where the system breaks.”

Engineering bias says: technical discomfort matters more than everyone else’s reality.

Psychological safety says: discomfort is data, no matter whose lane it comes from.

When those two collide, you find out very quickly whether a studio truly wants cross‑functional collaboration, or whether “T‑shaped” was just something they wrote on a slide.

## It’s not just engineering

I’m picking on “engineering bias” because it’s common and easy to see, but this pattern isn’t unique to engineers. Any discipline can start believing its lens is the most “real” and everyone else’s input is ornamental.

I’ve seen it in design. You’ll hear rules like “all levels must start in design,” as if fun can only be born in Figma, a spec doc, or a gray‑box layout. In reality, some of the best levels I’ve worked on started in art: someone gets inspired, there is concept art, someone blocks out a visual space in 3D, drops in a few props or landmarks, and suddenly you’ve got something walkable and vaguely playable. It’s rough. It’s not “designed” yet. But it sparks something. Design looks at that messy aesthetic inspiration, sees the potential, and builds on it—tightens the loops, tunes flow and pacing, turns a cool sketch into a layout and encounters people naturally remember. It’s not about who left the starting line. It’s about who helps the thing cross the finish.

I’ve seen it in QA. At Rockstar, some of the sharpest creative ideas and calls came out of QA feedback. They were the ones living with the game more than eight hours a day, seeing edge cases nobody else saw, feeling where the fun dropped off or where players would push systems in ways design hadn’t anticipated. That team was intentionally diverse in background—a poetry laureate, a business‑school grad, sports nuts, music heads, conspiracy weirdos—and that mix mattered. They weren’t just bug‑finders; they were an always‑on reality check for how the game actually felt and played in the wild.

You can extend this everywhere. Production sees patterns in schedule, scope, and human bandwidth that don’t show up in Jira tickets. Community and support see how decisions land in the wild long after a feature is “done.” Marketing sometimes spots a fantasy or angle the core team is too close to see. Any of those perspectives can be the one that saves you from a blind spot—if it’s allowed in the room before the train hits the wall.

The point isn’t that every idea is great or that hierarchy is useless. It’s that the moment any silo starts believing only their discipline gets to define reality, you’re back to lane‑policing in a different jersey. Psychological safety means discomfort is treated as data no matter where it comes from: art, design, QA, community, production, or engineering. The teams that win are the ones that let the best signals through, not just the ones that come from the “right” lane.

Knowing what goes wrong is one thing. The harder question is: what does the environment have to look like for that signal to actually get through? That’s what Part 3 is about — fake safety vs. real safety, what kind of work demands what kind of leadership, and what it actually means to steward a culture instead of just claiming to.

\----
Part 3: (link)

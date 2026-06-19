# Lane-Breaking: Safety, Bias and Stewardship

In Part 1 (link), I told the up‑close version of this: being a polymath in a world that says it loves “T‑shaped people” and then punishes you the moment you cross an invisible lane line. We talked about how lane‑policing kills psychological safety and trains people who can see across systems to shut up and do their narrow tickets. In this part, I want to pull the camera back and look at the bigger forces that make that worse or better: fake safety vs real safety, departmental bias, and why stewardship and invention need different kinds of leadership.

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

## When "safety" turns into theater

There is another flavor of this that shows up in big‑tech and big‑brand environments.

On paper, the story is all about being a “world‑class workplace,” hitting diversity goals, and building an inclusive culture. The slide decks look great. There are hiring targets, internal campaigns, lots of messaging. And to be clear: [fixing representation matters](https://scholarworks.boisestate.edu/cgi/viewcontent.cgi?article=1106&context=pubadmin_facpubs), and diversity and inclusion are a feature, not a bug. Some of the strongest people I’ve worked with only got in because someone finally took goals like these seriously. That part is real. The problem isn’t diversity or representation; it’s when we stop insisting on [merit and standards](https://scholarworks.boisestate.edu/cgi/viewcontent.cgi?article=1106&context=pubadmin_facpubs) as well, quietly waive the bar for optics, and then let “diversity” take the blame when those shortcuts blow up.

I’ve seen it happen. A highly specialized role with a well‑understood bar—portfolio review, design calibration, technical calibration, peer assessment—suddenly gets an exception because a candidate ticks an important box for a leader or hiring manager. A portfolio doesn’t matter this time. The design review will slow down hiring. We can skip the technical screening. The justification is framed as progress: “we need more people like this.” When it doesn’t work out, the post‑mortem isn’t “we broke our own process,” it’s a quiet eye‑roll about “hiring for diversity” from that same leader. No accountability for the decision; everyone else loses in multiple ways. For underrepresented folks who did clear the bar, this is poison: it makes them wonder whether every side‑eye is about their work or about someone else’s shortcut. The individual is set up to fail, the team’s trust in the bar and interview process erodes, and people who genuinely do clear the bar start wondering who’s silently questioning their legitimacy and purpose.

That’s the failure mode I’m talking about. Not “merit versus diversity” as a fake binary, but leadership using identity to justify inconsistent standards, then letting existing personnel take on the tarnish and marginalized groups carry the reputational damage instead of owning the call.

The problem is the shellac.

Your artifacts and assessments are required, and you expect to take hits and roll with punches. In big tech sometimes it feels like you’re in the octagon. Your own docs are expected to be brutally combed over, commented on, and objectively reviewed for accuracy and value. But with certain peers, you’re expected to walk on eggshells, deliver meaningful feedback indirectly, behind closed doors and through middle‑people. That is not safety, and it’s definitely not psychological safety. It’s coddling dressed up as care.

Teams or individuals can ship obviously weak work and, in a more public forum, it gets coated in a glossy layer of praise: “So proud of this team,” “Incredible effort,” “Amazing outcome,” “Great work.” The real conversation happens in private: here is what broke, here is who isn’t delivering, here is where the bar actually is. This isn’t about any one person’s merit; it’s about how organizational incentives decide which truths get spoken out loud and which get buried.

I grew up and cut my teeth in cultures where excellence was the North Star. The lane was “best game we can make,” full stop. We could say hard things out loud. People bristled, arguments happened, but the assumption was that we were adults and the work mattered. Thick skin was part of the job, not because cruelty was the goal, but because honesty was.

In the softer, brand‑driven version, a different pattern appears:

- Public story: everything is great, everyone is killing it, the employer brand stays pristine.  
- Private story: a small circle tells the truth quietly, where it feels “safe” to admit something sucks.

That is not psychological safety. That is fear with better marketing.

[Real psychological safety](https://psychsafety.com/about-psychological-safety/) is permission for [candor](https://www.library.hbs.edu/working-knowledge/four-steps-to-build-the-psychological-safety-that-high-performing-teams-need-today). It is the ability to say the uncomfortable thing in the room where it matters, push for the highest standards, and not be punished for it. What you see instead is a kind of organizational “[ruinous empathy](https://www.radicalcandor.com/blog/criticism-ruinous-empathy)”: leaders are so afraid of bruising anyone or scratching the brand that they stop giving clear, direct feedback.

You cannot optimize for a flawless public culture story and quietly de‑optimize for truth, merit, and excellence without paying for it. The price is [trust](https://claudiageratz.com/blog/why-psychological-safety-matters).

People are not stupid. They know when output is weak. When messaging is flimsy. They know when someone is struggling. When the official story is “everything is amazing” and the unofficial story is “we’re in trouble, but don’t say it out loud,” you train everyone to play along. 

You create a culture where:

- Saying the hard thing in public is risky.  
- Saying nothing and nodding along is safe.

Call it what you want, but it is not inclusive and it is not safe. It is just another form of lane‑policing: “Your job is to support the narrative, not to say what you actually see.”

The places that feel harsh on the surface—where someone will look you in the eye and say “this isn’t good enough yet”—are often the ones that are truly safe. The kindness is not in the sugarcoating. It is in being willing to tell the truth while still having each other’s backs. Delivering objective feedback and criticism is a skill; how it’s delivered matters. But perfect is the enemy of good: people need psychological safety to use their voice and offer real feedback before you can help them hone it. That, too, is a form of stewardship.

## Stewardship vs invention

There is also a big difference between stewarding something beloved and inventing something new.

Some of the best work I have seen in this industry has been faithful remakes and remasters of classic games. The praise is almost always about stewardship: preserve what made the original special, modernize visuals, controls, and feel.

That is a specific kind of problem:

- The core creative identity already exists: tone, mechanics, pacing, story, fantasy.  
- The audience contract is known: fans will tell you what is sacred and what is negotiable.  
- The question is not "what is this game?" but "how do we honor this game now?"

It is still hard, but the ambiguity is narrower. If you corral ego and align on what is sacred versus what is fair game, the target is clear. You are aiming for "this feels like I remember it, but better," not "this is some brand-new thing nobody has a mental model for yet."

New IP is a different universe.

There is no proven fantasy. No fan contract. No existing shape to protect. Every pillar – mechanics, world, story, camera, systems – is subject to change, and most of your strongest early beliefs will be wrong in at least one important way. The risk profile is not "don't screw up this beloved thing." It is "can we even find something that deserves to be beloved?"

In a remake, a top‑down "*we already know what this is, just execute*" culture can survive, sometimes even thrive, because the original game quietly does a lot of the heavy lifting. In a new IP, that same culture is a trap:

- If dissent is unwelcome, you cling to bad assumptions too long.  
- If lanes are rigid, nobody challenges the core fantasy or scope until it is baked into the schedule.  
- If leadership treats the game as a fixed vision instead of a hypothesis, you only discover you were wrong when it is very expensive.

This is where psychological safety and critical thinking go from "nice ideas" to survival traits. In a risky new IP, you need people from every discipline asking, "What if this pillar is wrong?", "What if this workflow will not scale?", "What if players do not want this?" And you need leadership that can hear that without treating it as a personal attack.

Remakes reward ego control and craftsmanship. New IP punishes ego and rewards environments where it is safe to question even the things the director believes most strongly.

## Stewards of culture and safety

If you’re a lead, director, or manager, you’re not just shipping features. You’re the steward of the culture around them. You decide how much voice people really have, whose discomfort counts as data, and whether psychological safety is real or just a phrase in a deck.

Most people don’t need to win every argument. They need to feel heard, respected, and taken into account. [Good leaders listen and ask questions](https://online.hbs.edu/blog/post/psychological-safety-in-the-workplace). When people feel like their perspective was genuinely considered, they can disagree and still commit. When they don’t—when their input disappears into a void, or gets swatted away with lane‑policing—they get brittle, skeptical, and eventually disengaged.

Good leadership doesn’t mean crowdsourcing every decision. Leaders still make the call. The difference is in how they get there: do they actively pull in voices from across art, design, engineering, QA, production, community? Do they ask real questions before they decide? Do they make the reasoning visible so people understand the tradeoffs, even when they don’t love the outcome?  Do they listen to the signals—especially when those signals show up as discomfort?

In my experience, if you do that, most people will absolutely toe the line. They’ll help you make it happen. The decision is made, the ambiguity is gone, the direction is clear—and because they had a voice on the way there, they’ll put their shoulder into the result instead of quietly sandbagging it.

This is what stewardship looks like at the cultural level. It’s not about being perfect, or never hurting anyone’s feelings. It’s about building a team where telling the truth is safer than staying quiet, where merit and standards are applied consistently, and where people can say “I disagree, but I’m in” without feeling like they just volunteered for exile. If there’s a “this is the way” for modern studios, I think it starts there.  

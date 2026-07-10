---
layout: post
title: "The Swarm Doesn't Care What's Inside the Worker"
summary: "Everyone's arguing about whether AI replaces the game pipeline. I already built the piece of infrastructure that makes that the wrong question. Here's where BATS goes next."
author: hogjonny
date: "2026-07-10 00:00:00 -0600"
modified_date: "2026-07-10 00:00:00 -0600"
category: python
thumbnail: /assets/img/posts/the-swarm-doesnt-care.png
keywords: python,ai,mcp,orchestration,agents,dcc,pipeline,game-development,distributed-systems,bats
permalink: /blog/swarm-doesnt-care/
usemathjax: false
---

# Welcome to the Co3deX

Hello and welcome to the CO3DEX, a blog of my Journeys in Real-time 3D Graphics and Technical Art. My name is Jonny Galloway. I am a polymath technical art leader who bridges art, tools, engine, AI and product. I work as a Principal Technical Artist and tools/engine specialist with 30+ years in AAA game development, working across content, design, production, and technology.

## The Swarm Doesn't Care What's Inside the Worker

Every week there's a new hot take about AI replacing the 3D pipeline. Generate the mesh, skip the artist, ship the game. I've stopped arguing with those takes directly, because arguing about whether AI *should* replace the pipeline skips a question that actually matters more: replace it with what, running on what?

If you're a Technical Artist or a TD, you've probably had this exact argument in a Slack thread more times than you can count this year, and you're probably about as tired of it as I am.

Here's what I actually think is right, and I'll spend the rest of this post backing it up instead of just asserting it: AI doesn't need its own pipeline. It needs to be another worker in a swarm that already knows how to handle work it doesn't fully understand.

I've been sitting on that for a few months now, mostly because I was too busy building it to write about it. This isn't a hot take, either. It's the next entry in a series where I've been documenting actual infrastructure as I build it, not predicting what it might do someday. By the end of this you'll have the actual pattern behind it, not just my opinion on whether it's a good idea.

### Where this started

Guess which of these four posts secretly made the AI-worker idea possible. I'll tell you at the end, but it's probably not the one you'd pick.

[Part 1](/blog/tool-logging-with-python/) was about logging. Boring, foundational, the kind of thing nobody wants to write about but every production tool eventually needs. [Part 2](/blog/threading-antipatterns-qt-async/) was about ripping threading code out of a tool that never needed it in the first place... turns out you can't parallelize a sequential pipeline no matter how many threads you throw at it.

[Part 3](/blog/distributed-orchestration-bats/) is where it got interesting. I stopped thinking about tools and started thinking about infrastructure. Instead of a script that launches Maya, does one thing, and dies, I built a swarm: workers that boot once, stay warm, and pull jobs from a queue for as long as there's work. Turned a 6.7-hour sequential batch into 10 minutes with 50 workers running. That's not a script anymore. That's a job substrate.

[Part 4](/blog/natural-language-infrastructure-mcp/) put a conversational layer on top of it. Twenty MCP tools, so I can tell Claude "submit 10 Maya jobs for these hero swords" instead of opening VS Code and writing boilerplate gRPC calls every time an artist needs a batch of assets. The infrastructure didn't get smarter. It got a language interface.

Here's the answer: none of them, on purpose. Four parts, and at no point did I set out to build "an AI pipeline." I set out to fix specific, boring problems: I couldn't see what a tool was doing, threading was adding complexity for zero benefit, sequential batches were slow, and submitting work required me personally sitting at a keyboard. Each fix was in service of the last one.

None of it happened because a room signed off on a plan, either. Scoping something down to a single asset at a time is a reasonable starting point. Wanting to explore every angle before committing resources is a reasonable instinct too. But taken far enough, both turn into reasons nothing moves. Consensus is data, it tells you what a room currently believes, and sometimes that's genuinely useful. But consensus-seeking dressed up as diligence is just a slower way to say no. So I built this on my own time, with my own resources, pointed at a problem I could see clearly, and let the results make the argument faster than a room still negotiating scope ever would have. Ask forgiveness, not permission, isn't a slogan for me. It's what happens when you'd rather ship something real than wait for consensus that may not arrive.

### The part I didn't emphasize enough

Here's the thing I buried in Part 3 that I think is actually the whole point: BATS doesn't know or care what a worker is. A worker is just something that boots once, stays warm, and pulls jobs. I built Maya and Houdini workers first because that's what I needed. But the pattern doesn't know about Maya. It knows about "boot once, stay hot, poll for work."

Here's the part most people don't expect: a Python worker that loads a model once and serves inference requests all day is architecturally identical to a Maya worker that loads a scene once and processes rock scans all day. Not similar. Identical. Same pull loop, same job queue, same priority system, same monitoring. Don't take my word for it, here's the Maya worker loop from Part 3:

```python
# Worker loop
while True:
    job = stub.RequestJob(DCCClientInfo(
        worker_id=self.worker_id,
        dcc_type="maya",
        capabilities=["modeling", "rendering"]
    ))

    if job.job_id:
        result = self.execute_job(job)
        stub.UpdateStatus(JobStatusUpdate(job_id=job.job_id, status=result.status, progress=100))
    else:
        time.sleep(5)
```

And here's the AI worker I already sketched out in that same post, a worker that loads a diffusion model once on boot and then answers generation requests without ever paying the load cost again:

```python
# AI worker stays hot with model loaded
@register_python_worker
def stable_diffusion_worker():
    model = load_stable_diffusion_model()  # Load once on boot (5-10s)

    while True:
        job = request_job(dcc_type="python", capability="stable_diffusion")
        if job:
            prompt = job.parameters["prompt"]
            image = model.generate(prompt)  # Inference on warm model (<1s)
            save_image(image, job.output_files[0])
            report_complete(job)
```

Go ahead, diff them. Poll, check for work, execute, report, loop, that's the entire contract. Swap the model loader for `cmds.file(open=...)` and you'd have to squint to tell which one is the AI worker. The swarm doesn't know the difference and doesn't need to.

I wasn't the only one who found that surprising. I showed a coworker the pool monitor mid-run once, watched their face when the worker count climbed and jobs started draining out of the queue two and three at a time instead of one. What got them wasn't the concept. It was watching the total time actually fall while it happened.

That's not a hypothetical bolt-on. It's the same swarm I already have running, pointed at a different kind of work.

### So what's actually next

I keep seeing the industry conversation frame this as a binary: either AI replaces the pipeline, or it doesn't touch it. I don't think that's the real fork, and I don't think it's a close call. The real fork is whether AI shows up as a one-off script somebody wires up badly, or as another bounded job type inside infrastructure that already knows how to schedule, validate, retry, and monitor work.

I already have the second option sitting on my machine. That's not a hot take, it's just what happens when you build the boring infrastructure first and let the AI conversation catch up to it.

The next thing I want to try is adding an AI worker type alongside Maya and Houdini... something that does first-pass mesh or material generation and drops its output straight into the same queue that already routes work through retopo, UV, bake, and engine validation. Not a separate AI pipeline bolted on the side. The exact same swarm, one more worker type, output that still has to clear the same gates as everything else before it ships.

And because MCP is already in place from Part 4, the natural extension after that is agentic: instead of me typing "submit 10 Maya jobs," an agent looks at a request like "block out 5 hero sword variants and get them through retopo" and composes the multi-step job sequence itself, calling the tools that already exist. I'm not describing a new architecture there. I'm describing the same 20 tools, called by something a little smarter than me remembering the right sequence at 6pm on a Friday.

### What I'm not going to pretend

I'm not going to pretend a warm-loaded model worker makes hero-asset generation autonomous, or that an agent composing job graphs means nobody reviews the output. The validation layer that already exists for Maya and Houdini jobs doesn't get a pass just because the job came from a model instead of a script. If anything it matters more, because the failure mode for a bad AI-generated mesh isn't "obviously wrong," it's "plausible enough that someone doesn't catch it until three stages later."

There's a bigger reason the pipeline stays in charge than any single failure mode, though. Trust. Maya, Houdini, the engine, the bake tools, the validation scripts, all of it has decades of shipped games behind it. That trust wasn't given, it was earned one shipped title at a time. AI doesn't have that yet, and a good demo doesn't buy it any. A generated mesh that gets a "whoa" out of a room is a dopamine hit, not a production credential. It says nothing about whether that mesh survives a bake, hits a texel density budget, or holds up in an engine that has to run at 60fps on a shipping SKU. The pipeline earned its authority the slow way. AI gets to participate once it starts earning the same way, one validated job at a time, not because a demo made someone's jaw drop in a conference room.

Every Technical Artist reading this already knows what I mean. We've all opened a generated mesh and found UV shells that look fine in a thumbnail and fall apart the second they hit a bake, or topology that's nowhere near engine performance budgets once it actually has to run in a level instead of sit in a viewport. That's not a one-off bug, it's just one example of a whole category of failure points that AI output hits reliably, and it's exactly why those stages stay owned by human eyes or the existing validation mechanisms that already catch them for every other asset in the pipeline. The job type changes. Who signs off on UVs and runtime budgets doesn't.

The swarm not caring what's inside the worker cuts both ways. It means AI work gets to ride the same infrastructure Maya and Houdini already trust. It also means AI work doesn't get to skip the parts of that infrastructure that exist specifically to catch garbage before it ships.

### Where this is going

I don't have a Part 5 written yet. What I have is a working substrate, four posts of receipts showing I've actually built and used the thing, and a fairly clear idea of what I want to try next. That's usually the point where I stop talking and start building, so consider this the "here's what I'm thinking" post before the "here's what happened" one.

If you've been following the series, you already know I don't reach for AI because it's the trend. I reach for it when the boring infrastructure work underneath it already justifies the bet. This time, I already did the boring part.

So here's where I actually stand, not as a prediction but as a position: the studios arguing about whether AI replaces the pipeline are asking the wrong question, and the ones who figure that out early are the ones who'll spend the next few years shipping instead of debating.

---

*This post follows a series on building maintainable game development tools:*

- *[Part 1: Tool Logging with Python](/blog/tool-logging-with-python/)*
- *[Part 2: Don't Thread What You Can't Parallelize](/blog/threading-antipatterns-qt-async/)*
- *[Part 3: When Parallelization IS the Answer](/blog/distributed-orchestration-bats/)*
- *[Part 4: Natural Language Infrastructure with MCP](/blog/natural-language-infrastructure-mcp/)*
- *This post: thinking out loud about what comes next*

*If you're staring down the same decision, whether to bolt AI onto your pipeline as a side project or build it into infrastructure you already trust, I'd genuinely like to compare notes. Reach out on [Twitter](https://twitter.com/hogjonny) or [LinkedIn](https://www.linkedin.com/in/hogjonny), or drop a comment below.*

---

```python
import logging as _logging
_MODULENAME = 'co3dex.posts.the_swarm_doesnt_care'
_LOGGER = _logging.getLogger(_MODULENAME)
_LOGGER.info(f'Initializing: {_MODULENAME} ... a worker is a worker is a worker')
```

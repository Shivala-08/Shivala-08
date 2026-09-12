# GitHub Profile — Hire-Me Upgrade Manual

## Project

**Owner:** Pallav Dholariya  
**GitHub:** `Shivala-08`  
**Profile repository:** `Shivala-08/Shivala-08`  
**Goal:** Turn the GitHub profile from a visually impressive student profile into a recruiter-readable engineering portfolio that communicates:

> **AI/ML Engineer · Systems Builder**

### Core personal positioning

> **Curious enough to learn anything.  
> Disciplined enough to ship.**

The profile should feel ambitious, technical, honest, and evidence-driven — not like a collection of badges or AI-generated marketing copy.

---

# 0. Non-Negotiable Rules

These rules apply to every change.

- Do not add more visual widgets unless they provide real information.
- Do not invent metrics.
- Do not exaggerate project maturity.
- Do not claim production-readiness unless the architecture supports that claim.
- Every performance number must have a measurement method.
- Every technology listed must be defensible in an interview.
- Prefer real engineering evidence over adjectives.
- Prefer fewer strong projects over many mediocre ones.
- Keep the animated terminal banner.
- Keep the profile visually distinctive, but reduce visual noise below the banner.
- Do not create fake stars, followers, activity, testimonials, or usage numbers.
- If a feature is unfinished, either finish it or remove it from the public README.
- If an idea does not improve recruiter comprehension, skip it.

---

# 1. Target Profile Structure

The final README should follow this order:

```text
1. Animated terminal banner
2. One-line identity + personal statement
3. Internship CTA + resume/contact links
4. Currently Building
5. Measured Results
6. Flagship Projects
   - Deploy Forge
   - Synapse
   - The Skynet
7. Other Strong Builds
   - Omnitrix OS
   - CineVault
8. Engineering Principles
9. Tech Stack
10. GitHub Activity
11. Contribution Snake
12. Contact / Closing CTA
```

The profile should answer these questions in order:

```text
WHO ARE YOU?
        ↓
WHAT DO YOU BUILD?
        ↓
WHY SHOULD I BELIEVE YOU?
        ↓
WHAT HAVE YOU BUILT?
        ↓
HOW DO YOU THINK?
        ↓
WHAT TECHNOLOGIES DO YOU USE?
        ↓
HOW CAN I CONTACT YOU?
```

---

# 2. Phase 1 — Fix the Hero Section

## Current problem

The banner is already visually strong.

Do NOT spend time redesigning it.

The problem is what comes immediately after it.

The profile currently repeats the identity with:

- AI/ML Engineer
- Full-Stack Developer
- activity information
- multiple visual widgets

This delays the actual recruiter message.

## Required change

Replace the text immediately below the banner with:

```md
<h2 align="center">AI/ML Engineer · Systems Builder</h2>

<p align="center">
  Curious enough to learn anything.<br>
  Disciplined enough to ship.
</p>
```

Then add:

```md
<p align="center">
  🟢 <strong>OPEN TO SOFTWARE / AI/ML INTERNSHIPS</strong>
</p>

<p align="center">
  <a href="YOUR_RESUME_URL">Resume</a> ·
  <a href="YOUR_LINKEDIN_URL">LinkedIn</a> ·
  <a href="mailto:pallavdholariya@gmail.com">Email</a> ·
  <a href="YOUR_PORTFOLIO_URL">Portfolio</a>
</p>
```

### Important

Do not write:

> Passionate developer

Do not write:

> Future software engineer

Do not write:

> Aspiring AI engineer

Do not write:

> I am a highly motivated...

The projects are supposed to prove those things.

---

# 3. Phase 2 — Remove Broken / Redundant Components

## 3.1 Remove "Last activity"

Delete:

```text
Last activity: No recent activity
```

Reason:

A broken activity widget can contradict the rest of the profile and create a false impression of inactivity.

If the automation is not reliable, remove it instead of debugging it for visual reasons.

---

## 3.2 Remove the empty WakaTime block

If the WakaTime section is not actually populated:

```md
<!--START_SECTION:waka-->
<!--END_SECTION:waka-->
```

remove the entire section.

Only add WakaTime after it reliably displays useful information.

---

## 3.3 Remove the 3D contribution graph

Remove the large 3D contribution visualization.

Keep:

- GitHub Stats
- Streak Stats
- Contribution Snake

The 3D graph is visually interesting but adds little hiring signal.

The README should prioritize:

```text
Projects > Evidence > Engineering > Activity > Decoration
```

---

# 4. Phase 3 — Rewrite "Engineering Profile"

Replace the existing oversized profile section with:

```md
## ⚡ Engineering Profile

I like going one layer deeper.

I build AI systems, developer infrastructure, and interactive products — then
measure the parts that matter instead of assuming the abstraction is good enough.

| Area | What I actually build |
|---|---|
| 🤖 AI / ML | Retrieval systems, LLM workflows, evaluation pipelines |
| ⚙️ Systems | Build pipelines, deployment infrastructure, automation |
| 🌐 Web | Full-stack applications and interactive interfaces |
| 🎮 Graphics | WebGL rendering, GPU-driven interaction, performance work |
```

The key sentence is:

> **I like going one layer deeper.**

This becomes a recurring theme across the profile.

---

# 5. Phase 4 — Add "Currently Building"

Keep this section short.

```md
## 🔨 Currently Building

| Project | Focus |
|---|---|
| 🧠 Synapse | Retrieval, routing, and AI experimentation |
| 🚀 Deploy Forge | Git-backed deployment infrastructure |
| 🌐 The Skynet | Custom WebGL + AI portfolio system |

> Building → measuring → breaking → fixing → shipping.
```

Do not list 10 projects here.

Maximum: 3.

---

# 6. Phase 5 — Replace "Engineering Receipts" With "Measured Results"

Rename:

```text
Engineering Receipts
```

to:

```text
Measured Results
```

Use:

```md
## 📊 Measured Results

| Project | Measurement | Result |
|---|---|---:|
| The Skynet | Client-side 3D bundle | **883 KB → 24.9 KB** |
| Deploy Forge | Local production build | **~15s** |
| Synapse | Retrieval latency | **207 ms** |
```

### CRITICAL

Only include the Synapse accuracy number if you provide methodology.

Do NOT show:

```text
62.5% accuracy
```

without explaining:

- dataset
- number of queries
- metric definition
- baseline
- retrieval configuration

If there is no baseline, move the accuracy number into Synapse's evaluation section.

---

# 7. Phase 6 — Make Metrics Scientifically Defensible

Every metric in the profile must answer:

```text
WHAT?
HOW?
UNDER WHAT CONDITIONS?
COMPARED TO WHAT?
```

For example, do not write:

```text
207ms latency
```

Write:

```text
207ms retrieval latency
p50 · 40-query benchmark · LLM disabled
```

Only use this exact wording if it matches the actual measurement.

For Deploy Forge:

```text
~15s production build
```

is acceptable only if the README explains that it was measured locally.

If you later benchmark it properly, upgrade the metric to:

```text
~15s build
p50 · N runs · environment: ______
```

---

# 8. Phase 7 — Rebuild the Flagship Projects Section

Create three primary projects.

Order:

```text
1. Deploy Forge
2. Synapse
3. The Skynet
```

These represent three engineering dimensions:

```text
Deploy Forge → Infrastructure
Synapse      → AI / ML
The Skynet   → Performance / Graphics
```

---

# 9. Deploy Forge — Rewrite the Positioning

## Do NOT call it

```text
Production deployment platform
```

unless you can defend production-grade isolation, rollback, concurrency,
security, observability, and failure handling.

Use:

```text
LIVE · PERSONAL PROJECT
```

or:

```text
DEPLOYED · ACTIVE
```

## Recommended profile copy

```md
### 🚀 Deploy Forge — Git-Backed Deployment Infrastructure

A deployment system that turns:

GitHub Repository
→ Build
→ Artifact Rewrite
→ Git Commit
→ Vercel Deployment

into a single workflow.

**Why I built it**

I got tired of manually repeating:

clone → install → build → copy → commit → push → deploy.

So I built the pipeline instead.

**Engineering**

- GitHub `repository_dispatch`
- GitHub Actions build runners
- Framework auto-detection
- Build artifact handling
- Absolute-path rewriting for sub-path hosting
- Dynamic Next.js routing
- Deployment status callbacks
- AES-256-GCM environment-variable encryption
- Prisma-backed deployment state

**Measured**

~15s local production build.

**Known limitations**

- Git-backed artifacts introduce propagation latency.
- Arbitrary builds require stronger process isolation.
- Rollback support is not implemented yet.
- Concurrent deployments need stronger isolation.
```

---

# 10. Deploy Forge — Fix the Incorrect Technical Claim

Do NOT describe framework detection as:

```text
Pydantic parser
```

The project is TypeScript/Next.js and its framework detector is implemented around
repository/package configuration.

Use:

```text
Automated framework detection — scans repository configuration to select
appropriate build profiles for supported frameworks.
```

If you want the exact supported list, document it in the project README.

---

# 11. Deploy Forge — Add Architecture Documentation

Create:

```text
docs/
├── architecture.md
├── deployment-flow.md
├── security.md
├── failure-modes.md
└── benchmarks.md
```

## `docs/architecture.md`

Explain:

```text
User
 ↓
DeployForge API
 ↓
Deployment Record
 ↓
GitHub repository_dispatch
 ↓
GitHub Actions
 ↓
Clone Target Repository
 ↓
Install Dependencies
 ↓
Build
 ↓
Rewrite Paths
 ↓
Commit Artifacts
 ↓
Vercel
 ↓
Live Site
```

Then explain why GitHub Actions is used instead of building inside the
serverless application.

---

# 12. Deploy Forge — Add Failure Modes

Create:

```md
# Failure Modes

## Build failure

Target repository fails during installation or build.

Expected behavior:
- deployment becomes FAILED
- logs remain accessible
- no READY state is emitted

## Vercel failure

Artifact generation succeeds but hosting fails.

Expected behavior:
- deployment state does not silently become READY

## Path rewrite failure

Absolute asset paths remain rooted at `/`.

Expected behavior:
- deployment validation should detect missing assets before READY

## Concurrent deployment

Two builds target the same site.

Document:
- current behavior
- race condition risk
- planned locking/versioning solution
```

This is extremely valuable for interviews.

---

# 13. Deploy Forge — Add Security Documentation

Create:

```md
# Security Model

## Current trust boundary

The system executes build commands from external repositories through
GitHub Actions.

This means build execution must be treated as untrusted code execution.

## Current protections

- Secrets are not stored directly in generated site files.
- Environment values are encrypted.
- Deployment credentials are stored through GitHub/Vercel secret mechanisms.

## Current limitations

- Arbitrary builds can consume runner resources.
- Build scripts can execute arbitrary commands inside the runner.
- Stronger isolation is required for multi-user hostile workloads.

## Future architecture

Untrusted build
      ↓
Ephemeral isolated worker
      ↓
Immutable artifact
      ↓
Artifact store
      ↓
Deployment
```

Do not claim that the current architecture is multi-tenant secure if it is not.

Honest limitations increase credibility.

---

# 14. Deploy Forge — Add Tests

Prioritize tests around actual engineering risk.

Recommended:

```text
tests/
├── framework-detection.test.ts
├── path-rewriting.test.ts
├── deployment-state.test.ts
└── routing.test.ts
```

Highest priority:

### Path rewriting

Test:

```text
href="/style.css"
```

becomes:

```text
href="/sites/<siteId>/style.css"
```

and:

```text
src="/app.js"
```

becomes:

```text
src="/sites/<siteId>/app.js"
```

Also test:

- nested paths
- query strings
- already-prefixed paths
- SPA fallback
- URLs that should NOT be rewritten

---

# 15. Deploy Forge — Add CI

Create:

```text
.github/workflows/ci.yml
```

Minimum pipeline:

```text
push / pull_request
        ↓
npm ci
        ↓
lint
        ↓
typecheck
        ↓
test
        ↓
build
```

If a command does not exist in `package.json`, add it only when appropriate.

Do not create fake CI commands just to produce a green badge.

---

# 16. The Skynet — Reposition It

Change:

```text
The Skynet — Interactive OS
```

to:

```text
The Skynet — Custom WebGL Portfolio OS
```

Lead with the performance story.

Recommended profile block:

```md
### 🌐 The Skynet — Custom WebGL Portfolio OS

A browser-based AI lab / portfolio system where I replaced a heavy 3D rendering
stack with a focused WebGL renderer.

**The problem**

The original 3D implementation shipped a large client-side bundle.

**The experiment**

Instead of optimizing around the abstraction, I replaced the rendering layer.

**Result**

883 KB → 24.9 KB

**What I learned**

- WebGL rendering pipeline fundamentals
- GPU buffers and shaders
- Camera and interaction systems
- Picking / hit testing
- Performance profiling
- Lazy loading
- Reduced-motion handling

[Source] [Live Demo] [Architecture]
```

---

# 17. The Skynet — Add a Rendering Architecture Diagram

Create:

```text
docs/rendering.md
```

Explain:

```text
Input
 ↓
Interaction / Camera
 ↓
Scene State
 ↓
Geometry
 ↓
GPU Buffers
 ↓
Shaders
 ↓
WebGL Draw Calls
 ↓
Framebuffer
```

Explain what the old implementation did and what the new renderer does.

The goal is to prove:

> You did not simply copy a WebGL tutorial.

---

# 18. The Skynet — Add Performance Methodology

Create:

```text
docs/performance.md
```

Include:

```md
## Benchmark Environment

Browser:
CPU:
GPU:
OS:
Viewport:

## Before

Bundle:
First load:
FPS:
GPU usage:

## After

Bundle:
First load:
FPS:
GPU usage:

## Method

Explain exactly how every number was measured.
```

Never publish numbers you cannot reproduce.

---

# 19. Synapse — Make This Your AI Proof

Synapse should answer:

> "Can Pallav actually reason about AI systems?"

Do not make the README a list of AI buzzwords.

Instead show:

```text
Problem
 ↓
Architecture
 ↓
Baseline
 ↓
Experiment
 ↓
Evaluation
 ↓
Failure cases
 ↓
Next experiment
```

---

# 20. Synapse — Add an Evaluation Section

Create:

```text
docs/evaluation.md
```

Recommended table:

```md
| Configuration | Recall@K | MRR | Latency |
|---|---:|---:|---:|
| Dense retrieval | XX | XX | XX ms |
| + Reranker | XX | XX | XX ms |
| + Graph | XX | XX | XX ms |
| Full pipeline | XX | XX | XX ms |
```

Only populate values after running the benchmark.

Do not fabricate results.

---

# 21. Synapse — Add Failure Cases

This is more impressive than only showing successful examples.

Add:

```md
## Failure Cases

### Query type A
Expected:
Actual:
Why it failed:
Potential fix:

### Query type B
Expected:
Actual:
Why it failed:
Potential fix:
```

AI engineers are expected to understand failure modes, not just demos.

---

# 22. Add "Engineering Principles"

Replace motivational wording with:

```md
## 🧠 Engineering Principles

01 — Constraints before architecture  
Understand the actual limitation before selecting a solution.

02 — Smallest useful system first  
Build the smallest system that can prove the idea.

03 — Measure before optimizing  
No performance claim without a measurement.

04 — Optimize the bottleneck  
Don't rewrite the world because one component is slow.

05 — Ship → observe → iterate  
A deployed system teaches more than an unfinished abstraction.
```

---

# 23. Replace "Other Builds" With Curated Projects

Use:

```md
## 🧪 Other Builds

### 🛰️ Omnitrix OS
Immersive browser OS experiment focused on interaction, animation, WebGL,
and audio.

### 🎬 CineVault
Full-stack movie discovery application exploring API integration, discovery
UX, and scalable frontend patterns.
```

Keep these short.

The flagship projects get the deep writeups.

---

# 24. Pinned Repository Strategy

Pin these five:

```text
1. deploy-forge
2. The-skynet
3. Synapse
4. ben-10-os
5. CineVault
```

Remove lower-signal repositories from the pinned section.

Do not delete them.

The goal is curation, not pretending they don't exist.

---

# 25. Repository Cleanup

Review every public repository.

Classify each as:

```text
A — Flagship
B — Strong supporting project
C — Learning / experiment
D — Abandoned / irrelevant
```

Then:

```text
A → Public + polished
B → Public + clean README
C → Public if useful, otherwise archive
D → Archive
```

Target:

> 6–10 obvious high-quality repositories.

You currently have many more public repositories, so the profile needs curation.

---

# 26. Standard README Template For Every Serious Project

Use this structure:

```md
# Project Name

> One-sentence description.

[Demo] [Source] [Architecture]

## Why I Built It

The problem that triggered the project.

## What It Does

Short explanation.

## Architecture

Diagram.

## Engineering Decisions

### Decision 1
Why:
Tradeoff:

### Decision 2
Why:
Tradeoff:

## Performance / Evaluation

Reproducible measurements.

## Failure Cases

What doesn't work yet.

## Testing

What is covered.

## Security

Threat model / limitations.

## Roadmap

Only real future work.

## Tech Stack

Only technologies actually used.
```

---

# 27. Add CI Badges Only When CI Is Real

For flagship repositories, target:

```text
CI
Build
Tests
Lint
Typecheck
```

Do not add badges merely for decoration.

A recruiter should be able to click a badge and see an actual workflow.

---

# 28. Add Demo GIFs

For:

```text
Deploy Forge
The Skynet
Omnitrix OS
```

record approximately:

```text
15–30 seconds
```

Show the important behavior immediately.

## Deploy Forge GIF

Show:

```text
Connect repository
 ↓
Launch deployment
 ↓
Build status
 ↓
Logs
 ↓
Live result
```

## The Skynet GIF

Show:

```text
Portfolio boot
 ↓
3D interaction
 ↓
AI lab
 ↓
Terminal
 ↓
Neural navigation
```

## Omnitrix OS GIF

Show:

```text
Boot
 ↓
Dial interaction
 ↓
Transformation / UI
 ↓
System navigation
```

Do not make cinematic GIFs that hide the actual functionality.

---

# 29. Improve the Contact CTA

At the bottom:

```md
## 🤝 Let's Build Something

If you're working on:

- AI systems
- developer infrastructure
- performance-heavy web applications
- interesting engineering problems

I'd love to hear about it.

**Pallav Dholariya**

[LinkedIn] · [Email] · [Portfolio]
```

For internship targeting:

```md
> 🟢 Open to Software Engineering and AI/ML Internship opportunities.
```

---

# 30. Final GitHub Activity Section

Use:

```md
## 📈 Activity

<p align="center">
  <!-- GitHub stats -->
</p>

<p align="center">
  <!-- Streak -->
</p>

<p align="center">
  <!-- Contribution snake -->
</p>
```

Do not add:

- multiple contribution graphs
- 3D graph
- empty WakaTime
- broken activity widgets

---

# 31. Contribution Snake

Keep the existing snake system.

Requirements:

```text
.github/workflows/snake.yml
```

It should:

- run on schedule
- support manual workflow dispatch
- run on pushes to main
- have appropriate write permissions
- generate dark/light assets
- publish the generated assets
- display them with a theme-aware picture element

Only display the generated snake after the workflow has successfully generated
the output.

Do not debug the snake endlessly if it is already functioning.

---

# 32. Social Badges

Keep badges minimal.

Recommended:

```text
LinkedIn
Email
Portfolio
GitHub
```

Do not create 10 social badges.

Use your actual brand links.

Skip a GitHub badge if the profile already clearly identifies the account.

---

# 33. Remove These Types of Content

Delete or rewrite:

```text
"Passionate about..."
"Dreaming of..."
"Future..."
"Hardworking..."
"Fast learner..."
"Jack of all trades master of none"
```

Your chosen personal line is:

> **Curious enough to learn anything. Disciplined enough to ship.**

Use that instead.

---

# 34. Avoid "AI Buzzword Density"

Before publishing any README, count how many times you use:

```text
AI
LLM
Agent
RAG
Intelligent
Scalable
Production
High-performance
Enterprise
Next-generation
```

If a paragraph contains several of these but does not contain:

```text
code
architecture
measurement
tradeoff
experiment
failure
```

rewrite it.

---

# 35. Recruiter Scan Test

After finishing the README, open it in an incognito browser.

Give yourself 10 seconds.

You should be able to answer:

```text
Who is Pallav?
        ↓
AI/ML Engineer · Systems Builder

What is he looking for?
        ↓
Software / AI/ML Internship

What is he building?
        ↓
Synapse · Deploy Forge · The Skynet

Is there evidence?
        ↓
Benchmarks + architecture + tests

Can I contact him?
        ↓
Resume · LinkedIn · Email
```

If any answer requires scrolling too far, move it upward.

---

# 36. Engineer Scan Test

Give the README to a technical person.

Ask them:

```text
1. What is Deploy Forge actually doing?
2. Why does it use GitHub Actions?
3. What is the biggest architectural weakness?
4. What did Pallav actually optimize in The Skynet?
5. How was the 24.9 KB number measured?
6. What is Synapse evaluating?
7. What would you improve in each system?
```

If they can answer these from the READMEs, the profile has succeeded.

---

# 37. Final Visual Hierarchy

The finished page should visually feel like:

```text
╔══════════════════════════════════════════════╗
║                ANIMATED BANNER               ║
╚══════════════════════════════════════════════╝

          AI/ML Engineer · Systems Builder

       Curious enough to learn anything.
          Disciplined enough to ship.

          🟢 OPEN TO INTERNSHIPS

       Resume · LinkedIn · Email · Portfolio


## 🔨 Currently Building

Synapse        Deploy Forge        The Skynet


## 📊 Measured Results

883KB → 24.9KB       ~15s       207ms
The Skynet           DeployForge Synapse


## 🚀 Flagship Projects

Deploy Forge
Architecture · Security · Benchmarks · Demo

Synapse
Retrieval · Evaluation · Failure Cases

The Skynet
WebGL · Performance · Rendering


## 🧠 Engineering Principles

Constraints → Build → Measure → Optimize → Ship


## 🧪 Other Builds

Omnitrix OS · CineVault


## 🛠 Tech Stack

...


## 📈 Activity

Stats · Streak · Snake


## 🤝 Let's Build Something

LinkedIn · Email · Portfolio
```

---

# 38. Implementation Order

DO NOT change everything at once.

Follow this exact order.

## Phase A — Profile cleanup

- [ ] Remove Last Activity
- [ ] Remove empty WakaTime
- [ ] Remove 3D contribution graph
- [ ] Change headline to `AI/ML Engineer · Systems Builder`
- [ ] Add internship CTA
- [ ] Add Resume link
- [ ] Add LinkedIn
- [ ] Add Email
- [ ] Keep animated banner

STOP AND REVIEW.

---

## Phase B — Profile storytelling

- [ ] Rewrite Engineering Profile
- [ ] Add Currently Building
- [ ] Rename Engineering Receipts → Measured Results
- [ ] Validate every metric
- [ ] Add Engineering Principles
- [ ] Reduce Other Projects

STOP AND REVIEW.

---

## Phase C — Deploy Forge

- [ ] Correct technical description
- [ ] Change production wording
- [ ] Add architecture document
- [ ] Add security model
- [ ] Add failure modes
- [ ] Add benchmark methodology
- [ ] Add tests
- [ ] Add CI
- [ ] Record demo GIF
- [ ] Improve README

STOP AND REVIEW.

---

## Phase D — The Skynet

- [ ] Reposition around custom WebGL
- [ ] Document old architecture
- [ ] Document new renderer
- [ ] Add performance methodology
- [ ] Add benchmark reproducibility
- [ ] Add tests where practical
- [ ] Add CI
- [ ] Record demo GIF
- [ ] Improve README

STOP AND REVIEW.

---

## Phase E — Synapse

- [ ] Explain actual problem
- [ ] Document architecture
- [ ] Define baseline
- [ ] Build evaluation dataset
- [ ] Run retrieval benchmark
- [ ] Measure latency
- [ ] Add ablation table
- [ ] Document failure cases
- [ ] Add CI
- [ ] Improve README

STOP AND REVIEW.

---

## Phase F — Repository curation

- [ ] Reorder pinned repositories
- [ ] Archive irrelevant repositories
- [ ] Update descriptions
- [ ] Add consistent README structure
- [ ] Add licenses where appropriate
- [ ] Add CI to serious repositories
- [ ] Add meaningful recent commits
- [ ] Make sure demos actually work

---

## Phase G — Final profile assembly

- [ ] Assemble final README
- [ ] Test dark mode
- [ ] Test light mode
- [ ] Test mobile width
- [ ] Test every link
- [ ] Test every image
- [ ] Test snake
- [ ] Test stats
- [ ] Test badges
- [ ] Check resume link
- [ ] Check email
- [ ] Check LinkedIn
- [ ] Check portfolio
- [ ] Remove placeholders
- [ ] Remove broken widgets

---

# 39. Final Quality Gate

Do not consider the profile finished until every flagship repository can answer:

```text
WHY?
WHAT?
HOW?
WHY THIS ARCHITECTURE?
WHAT BROKE?
HOW WAS IT MEASURED?
WHAT ARE THE LIMITATIONS?
WHAT WOULD YOU BUILD NEXT?
```

The profile itself must answer:

```text
WHO?
WHAT?
PROOF?
CONTACT?
```

---

# 40. Final Positioning

The final profile should NOT communicate:

> "I know a lot of technologies."

It should communicate:

> **"I encounter technical constraints, investigate them, build systems around them, measure the result, and ship."**

That is the hiring signal.

The visual design gets the recruiter to stop scrolling.

The projects get them to click.

The benchmarks get them to believe you.

The architecture docs get engineers interested.

The limitations prove you're honest.

The resume/contact CTA makes the next step obvious.

---

# Definition of Done

The profile is DONE when:

- [ ] Banner looks excellent without further unnecessary tweaking.
- [ ] First screen clearly says `AI/ML Engineer · Systems Builder`.
- [ ] Internship availability is immediately visible.
- [ ] Resume is one click away.
- [ ] No broken activity widgets exist.
- [ ] No empty WakaTime section exists.
- [ ] No redundant 3D contribution graph exists.
- [ ] Deploy Forge is presented as infrastructure, not just a pretty dashboard.
- [ ] The Skynet is presented as a performance/WebGL engineering project.
- [ ] Synapse contains real evaluation methodology.
- [ ] At least two flagship projects have tests.
- [ ] At least two flagship projects have CI.
- [ ] Metrics are reproducible or explicitly labeled as local experiments.
- [ ] Known limitations are documented.
- [ ] Every flagship README contains architecture.
- [ ] Every flagship project has a working demo or clearly states why it cannot.
- [ ] Pinned repositories tell one coherent story.
- [ ] The profile can be understood in under 30 seconds.
- [ ] A technical reviewer can spend 10+ minutes going deeper.

---

# The Core Principle

## Don't make the GitHub profile louder.

## Make it harder to doubt.

The goal is not to make a recruiter think:

> "Wow, this is a cool GitHub profile."

The goal is to make them think:

> **"This student already investigates problems like an engineer. I want to interview him."**

# GitHub Profile — Serious Hiring Audit Implementation Manual

> **READ THIS ENTIRE MANUAL BEFORE CHANGING ANYTHING.**
>
> This is not a suggestion list. Treat it as the **implementation specification** for rebuilding the GitHub profile of **Pallav Dholariya (`Shivala-08`)**.
>
> **Follow these instructions seriously. Do not improvise major design, architecture, wording, project selection, metrics, or claims.**
>
> The objective is not to make the profile louder.
>
> The objective is to make it **harder for a technical recruiter or engineering hiring manager to doubt the candidate.**
>
> **Do not add random widgets. Do not invent metrics. Do not fabricate activity. Do not exaggerate project maturity. Do not replace real engineering evidence with marketing copy.**
>
> If an instruction conflicts with the actual repository state, **inspect the repository first and adapt only the implementation detail — never the underlying hiring strategy.**
>
> If something cannot be verified, mark it as `TODO` or remove the claim. **Never guess.**

---

# 1. Candidate Profile

## Identity

**Name:** Pallav Dholariya

**GitHub:** `Shivala-08`

**Education:** B.Tech CSE (AI & ML) — Newton School of Technology × ADYPU

**Location:** Pune, India

## Positioning

### Primary headline

```text
AI/ML Engineer · Systems Builder
```

### Personal line

```text
Curious enough to learn anything.
Disciplined enough to ship.
```

### Current status

```text
Building...
Learning...
Shipping...
```

### Hiring goal

The profile is optimized for:

- Software Engineering internships
- AI/ML internships
- Strong engineering internships
- Recruiter discovery
- Technical hiring-manager review
- Personal brand development

---

# 2. THE CORE STRATEGY

The profile currently has enough visual personality.

It does **not** need more decoration.

The problem is that the strongest engineering evidence is buried beneath visual/activity content.

The new hierarchy must therefore be:

```text
VISUAL HOOK
    ↓
WHO PALLAV IS
    ↓
WHAT PALLAV IS LOOKING FOR
    ↓
WHAT PALLAV IS BUILDING
    ↓
MEASURED ENGINEERING EVIDENCE
    ↓
FLAGSHIP PROJECTS
    ↓
ENGINEERING THINKING
    ↓
TECH STACK
    ↓
GITHUB ACTIVITY / VISUALIZATION
    ↓
OTHER BUILDS
    ↓
CONTACT
```

The profile should communicate:

> **I encounter technical constraints, investigate them, build systems around them, measure the result, document the tradeoffs, and ship.**

It should NOT communicate:

> "Look how many technologies I know."

---

# 3. NON-NEGOTIABLE RULES

These rules apply to the entire implementation.

## Rule 1 — No fabricated evidence

Never invent:

- stars
- followers
- commits
- benchmark numbers
- latency
- accuracy
- deployment times
- FPS
- user counts
- production claims
- testimonials
- adoption
- performance improvements

If a number has not been measured:

```text
TODO — benchmark required
```

or remove it.

---

## Rule 2 — No fake seniority

Do not write:

```text
Senior Engineer
Expert
Production-grade
Enterprise-ready
Highly scalable
Industry-leading
World-class
```

unless the repository genuinely supports the claim.

The goal is to make Pallav look **technically capable**, not artificially senior.

---

## Rule 3 — Projects are the proof

Visual elements get attention.

Projects earn credibility.

Therefore:

```text
Projects > Metrics > Architecture > Engineering Decisions > Activity > Decoration
```

---

## Rule 4 — Keep the 3D contribution graph

**Do NOT remove the 3D contribution graph.**

The recent audit specifically changed this recommendation.

The 3D graph fits Pallav's visual identity.

It should be treated as:

> **visual GitHub activity / personal branding**

—not as engineering evidence.

It belongs **after the important project content**.

---

## Rule 5 — Remove the broken activity widget

The profile currently exposes a:

```text
Last activity: No recent activity
```

state.

This is harmful.

**Remove it completely.**

Do not attempt to make a decorative replacement unless the replacement is reliable and useful.

---

## Rule 6 — No empty WakaTime section

If WakaTime is not populated with meaningful real data:

**Remove it.**

Do not leave:

```html
<!--START_SECTION:waka-->
<!--END_SECTION:waka-->
```

in the README.

Only add it after the integration is actually working.

---

## Rule 7 — Do not blindly redesign the banner

The animated terminal banner is already a strong differentiator.

Keep it.

Only modify it if there is a concrete bug or readability problem.

---

## Rule 8 — Do not add another widget just because it looks cool

Before adding any visual component, ask:

```text
Does this help a recruiter understand Pallav?
Does this provide engineering evidence?
Does this reinforce the personal brand?
```

If all three answers are no:

**Do not add it.**

---

## Rule 9 — Be honest about limitations

A strong engineer understands limitations.

For every serious project, document:

```text
What works
What doesn't
Why
What tradeoff was accepted
What should be improved next
```

---

## Rule 10 — Preserve source of truth

Never edit generated SVGs manually if a generator exists.

Keep:

- generator scripts
- source data
- `.npy` files
- workflow files
- source images
- source assets

The generated SVG is an output.

---

# 4. TARGET README STRUCTURE

The final profile README should follow this exact conceptual order:

```text
1. Animated terminal banner

2. AI/ML Engineer · Systems Builder

3. Curious enough to learn anything.
   Disciplined enough to ship.

4. Internship CTA

5. Currently Building

6. Measured Results

7. Featured / Flagship Projects
   Deploy Forge
   The Skynet
   Synapse

8. Other Builds
   Omnitrix OS
   CineVault

9. Engineering Principles

10. Tech Stack

11. GitHub Activity
    Stats
    Streak
    3D contribution graph
    Snake

12. Contact / Let's Build Something
```

Do not move activity widgets above the flagship projects.

---

# 5. PHASE 1 — FIX THE FIRST SCREEN

## Goal

A recruiter must understand the candidate in approximately **5–10 seconds**.

Immediately below the animated banner, add:

```md
<h2 align="center">AI/ML Engineer · Systems Builder</h2>

<p align="center">
  Curious enough to learn anything.<br>
  Disciplined enough to ship.
</p>
```

Then:

```md
<p align="center">
  🟢 <strong>OPEN TO SOFTWARE ENGINEERING / AI/ML INTERNSHIPS</strong>
</p>
```

Then:

```md
<p align="center">
  <a href="YOUR_RESUME_URL">Resume</a> ·
  <a href="YOUR_LINKEDIN_URL">LinkedIn</a> ·
  <a href="mailto:pallavdholariya@gmail.com">Email</a> ·
  <a href="YOUR_PORTFOLIO_URL">Portfolio</a>
</p>
```

### IMPORTANT

Do not write a giant introductory paragraph.

The first screen must be:

```text
Who I am
What I build
What I want
How to contact me
```

---

# 6. PHASE 2 — CURRENTLY BUILDING

Add:

```md
## 🔨 Currently Building

| Project | Focus |
|---|---|
| 🧠 Synapse | AI / retrieval / experimentation |
| 🚀 Deploy Forge | Git-backed deployment infrastructure |
| 🌐 The Skynet | Custom WebGL + performance engineering |

> Building → measuring → breaking → fixing → shipping.
```

Only include projects that are genuinely active.

If a project is not currently active, replace it.

Maximum:

**3 projects.**

---

# 7. PHASE 3 — MEASURED RESULTS

Add:

```md
## 📊 Measured Results

| Project | Measurement | Result |
|---|---|---:|
| The Skynet | 3D renderer bundle | **883 KB → 24.9 KB** |
| Deploy Forge | Local production build | **~15s** |
| Synapse | Retrieval benchmark | **TODO — benchmark required** |
```

### IMPORTANT

The Synapse number must NOT be invented.

If a verified benchmark exists, use:

```text
metric
dataset
number of queries
baseline
measurement environment
```

If it doesn't exist:

```text
TODO — benchmark required
```

Do not publish unsupported AI accuracy numbers.

---

# 8. PHASE 4 — FLAGSHIP PROJECTS

These are the three projects that should carry the hiring narrative.

## Priority order

```text
1. Deploy Forge
2. The Skynet
3. Synapse
```

They represent:

```text
Deploy Forge → Infrastructure
The Skynet   → Performance / Graphics
Synapse      → AI / ML
```

This combination is the core technical story.

---

# 9. DEPLOY FORGE — POSITIONING

## Project title

```text
🚀 Deploy Forge — Git-Backed Deployment Infrastructure
```

Do NOT describe it primarily as:

```text
premium deployment platform
```

Do NOT claim:

```text
production-ready deployment platform
```

unless the architecture actually supports that claim.

Use:

```text
Git-backed deployment infrastructure
```

or:

```text
Personal deployment infrastructure experiment
```

depending on the actual maturity.

---

# 10. DEPLOY FORGE — RECOMMENDED README STORY

Use this conceptual structure:

```md
## Why I built it

I got tired of repeating:

clone → install → build → copy → commit → push → deploy.

So I built the pipeline instead.
```

Then:

```md
## What it does

GitHub Repository
        ↓
Build
        ↓
Artifact processing
        ↓
Git commit
        ↓
Vercel deployment
```

Then explain the architecture.

---

# 11. DEPLOY FORGE — HIGHLIGHT THE REAL ENGINEERING PROBLEM

One of the strongest parts of the project is sub-path hosting.

The system needs deployed sites to work under something like:

```text
/sites/{siteId}
```

while many generated applications assume:

```text
/
```

For example:

```html
<script src="/app.js">
```

can break under:

```text
/sites/abc/app.js
```

This should be explicitly documented.

The README should explain:

```text
Problem
↓
Why normal root-relative assets break
↓
Path rewriting strategy
↓
Tradeoffs
↓
Failure cases
```

This is much stronger than calling the project "premium."

---

# 12. DEPLOY FORGE — ARCHITECTURE DOCUMENT

Create:

```text
docs/architecture.md
```

Document:

```text
User
 ↓
DeployForge API
 ↓
Deployment record
 ↓
GitHub repository_dispatch
 ↓
GitHub Actions
 ↓
Clone target repository
 ↓
Install dependencies
 ↓
Build
 ↓
Rewrite paths
 ↓
Commit artifact
 ↓
Vercel
 ↓
Live deployment
```

For every major component explain:

```text
Why is it here?
What does it do?
What are its limitations?
```

---

# 13. DEPLOY FORGE — SECURITY DOCUMENT

Create:

```text
docs/security.md
```

Explain the trust boundary.

Important point:

**Build commands from repositories are untrusted code execution.**

Document:

- secret handling
- environment variable encryption
- GitHub token handling
- Vercel credentials
- build execution
- runner trust
- potential abuse
- current limitations
- future isolation strategy

Do not claim complete multi-tenant security unless it exists.

---

# 14. DEPLOY FORGE — FAILURE MODES

Create:

```text
docs/failure-modes.md
```

At minimum:

### Build failure

What happens?

### GitHub Actions failure

What happens?

### Artifact rewrite failure

What happens?

### Vercel failure

What happens?

### Concurrent deployment

What happens if two deployments target the same project?

### Invalid repository

What happens?

The goal is to demonstrate that Pallav thinks about:

> **what happens when the happy path stops working.**

---

# 15. DEPLOY FORGE — BENCHMARK

Create:

```text
docs/benchmarks.md
```

Separate:

```text
Build time
GitHub Actions time
Artifact processing
Git commit/push
Vercel propagation
Total deployment time
```

Do not use:

```text
~15s
```

as though it represents the entire deployment.

If `~15s` is only the local production build, label it:

```text
Local production build: ~15s
```

Eventually benchmark:

```text
Click Deploy
        ↓
Live URL

Total: XXs
```

---

# 16. DEPLOY FORGE — TESTING

Prioritize tests around actual risks.

Recommended:

```text
framework-detection.test.ts
path-rewriting.test.ts
deployment-state.test.ts
routing.test.ts
```

Especially test path rewriting.

Test:

```text
href="/style.css"
src="/app.js"
```

and verify correct sub-path behavior.

Also test:

- nested paths
- query strings
- already-prefixed paths
- external URLs
- assets that should not be rewritten

---

# 17. DEPLOY FORGE — CI

Create:

```text
.github/workflows/ci.yml
```

Pipeline:

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

Only use commands that actually exist.

Do not create fake CI simply to generate a badge.

---

# 18. THE SKYNET — POSITIONING

Use:

```text
🌐 The Skynet — Custom WebGL Portfolio OS
```

The story should be:

```text
Existing 3D abstraction
        ↓
Measured bundle cost
        ↓
Identify bottleneck
        ↓
Replace rendering layer
        ↓
Custom WebGL renderer
        ↓
Benchmark
        ↓
Debug matrix / picking issues
        ↓
Ship
```

This is a very strong engineering story.

---

# 19. THE SKYNET — CORE RESULT

Highlight:

```text
883 KB → 24.9 KB
```

But explain exactly what those numbers represent.

Use a benchmark methodology.

Create:

```text
docs/performance.md
```

Include:

```md
## Environment

Browser:
OS:
CPU:
GPU:
Viewport:

## Before

Bundle:
FPS:
LCP:
TBT:

## After

Bundle:
FPS:
LCP:
TBT:

## Measurement Method

Exactly how each value was collected.
```

Do not invent missing values.

---

# 20. THE SKYNET — RENDERING ARCHITECTURE

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
Scene state
 ↓
Geometry
 ↓
GPU buffers
 ↓
Shaders
 ↓
WebGL draw calls
 ↓
Framebuffer
```

Document:

- buffers
- shaders
- transforms
- camera
- picking
- interaction
- matrix math
- performance considerations

The goal is to demonstrate:

> **This wasn't just a copied WebGL tutorial.**

---

# 21. THE SKYNET — FAILURE CASES

Document actual bugs encountered.

For example:

```text
Matrix layout issue
↓
Incorrect inversion
↓
Picking failed
↓
Investigated column-major representation
↓
Corrected transform handling
```

Only include this if it accurately reflects the repository history.

Failure documentation is valuable.

---

# 22. SYNAPSE — AI PROOF

Synapse must become the repository that answers:

> **Can Pallav actually reason about AI systems?**

Do not make it a buzzword showcase.

Structure:

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

# 23. SYNAPSE — EVALUATION

Create:

```text
docs/evaluation.md
```

Recommended:

```md
| Configuration | Recall@K | MRR | p50 Latency |
|---|---:|---:|---:|
| Baseline | TODO | TODO | TODO |
| Retriever | TODO | TODO | TODO |
| + Reranker | TODO | TODO | TODO |
| Full pipeline | TODO | TODO | TODO |
```

Do not publish fake numbers.

Run the benchmark first.

Document:

- dataset
- number of queries
- ground truth
- metric definitions
- baseline
- hardware/environment
- model configuration

---

# 24. SYNAPSE — FAILURE CASES

Add:

```md
## Failure Cases

### Query Type A

Expected:
Actual:
Why:
Potential fix:

### Query Type B

Expected:
Actual:
Why:
Potential fix:
```

This section is important.

A mediocre result with excellent analysis is more convincing than an impressive result with no methodology.

---

# 25. OMNITRIX OS — SUPPORTING FLAGSHIP

Do NOT remove Omnitrix OS.

Use it as evidence of:

- interaction design
- WebGL
- animation
- audio
- browser APIs
- PWA
- frontend engineering

Position it as:

```text
Interactive systems / frontend / graphics project
```

not as your primary AI project.

The portfolio story becomes:

```text
Deploy Forge → Infrastructure
The Skynet → Performance / Graphics
Synapse → AI / ML
Omnitrix OS → Interactive frontend
```

---

# 26. OTHER BUILDS

Keep:

```text
CineVault
```

as supporting project.

Recommended descriptions:

```md
### 🎬 CineVault

Full-stack movie discovery application exploring API integration,
discovery UX, and scalable frontend patterns.
```

Keep these concise.

---

# 27. ENGINEERING PRINCIPLES

Add:

```md
## 🧠 Engineering Principles

**01 — Constraints before architecture**

Understand the actual limitation before choosing the solution.

**02 — Smallest useful system first**

Build enough to prove the idea before expanding the abstraction.

**03 — Measure before optimizing**

No performance claim without a measurement.

**04 — Optimize the bottleneck**

Don't rewrite the world because one component is slow.

**05 — Ship → observe → iterate**

A deployed system teaches more than an unfinished abstraction.
```

This section should be short.

---

# 28. TECH STACK

Do not turn this into a wall of icons.

Organize it:

```text
## 🛠 Tech Stack

### Languages
Python · JavaScript · SQL · Bash

### Frontend
React · Next.js · Tailwind · HTML · CSS · Framer Motion · Lenis

### Backend
FastAPI

### Data
PostgreSQL · Supabase

### Infrastructure
Docker · GitHub Actions · Vercel · Cloudflare · Linux · ngrok

### Tools
VS Code · Git · Claude Code · Antigravity IDE
```

Only retain technologies that are actually represented in your work or that you can discuss technically.

---

# 29. GITHUB ACTIVITY — KEEP IT

This is where the visualizations go.

Use:

```text
## 📈 GitHub Activity
```

Then:

```text
GitHub Stats
Streak
3D contribution graph
Contribution snake
```

### Important

The activity section must come **after** flagship projects.

The 3D graph is visual branding.

The project architecture is engineering evidence.

Do not reverse them.

---

# 30. CONTRIBUTION SNAKE

Keep the existing contribution snake.

Ensure:

```text
.github/workflows/snake.yml
```

supports:

- scheduled execution
- `workflow_dispatch`
- push to main
- appropriate permissions
- light output
- dark output

Use theme-aware `<picture>` rendering.

Only display generated assets once the workflow has successfully generated them.

---

# 31. SOCIAL BADGES

Keep badges minimal.

Use:

- LinkedIn
- Email
- Portfolio

Do not create a wall of badges.

GitHub is already obvious from the profile itself.

---

# 32. PINNED REPOSITORIES

Change the pinned repositories to:

```text
1. Deploy Forge
2. The Skynet
3. Synapse
4. Omnitrix OS
5. CineVault
```

The six slots should tell a coherent story.

Do not pin a weaker project simply because it has more commits.

---

# 33. REPOSITORY CURATION

Categorize public repositories:

```text
A — Flagship
B — Strong supporting
C — Experiment
D — Abandoned / irrelevant
```

Then:

```text
A → Public + polished
B → Public + clean README
C → Public if useful
D → Archive
```

Do not delete historical work unnecessarily.

Archive instead.

---

# 34. STANDARD README FOR SERIOUS PROJECTS

Use:

```md
# Project Name

> One-sentence description.

[Demo] [Source] [Architecture]

## Why I Built It

## What It Does

## Architecture

## Engineering Decisions

### Decision 1

Why:
Tradeoff:

### Decision 2

Why:
Tradeoff:

## Performance / Evaluation

## Failure Cases

## Testing

## Security

## Limitations

## Roadmap

## Tech Stack
```

Every serious project should answer:

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

---

# 35. CI STANDARD

For serious projects:

```text
Pull Request
    ↓
Install
    ↓
Lint
    ↓
Typecheck
    ↓
Tests
    ↓
Build
```

Add CI badges only when the workflow is real.

---

# 36. LICENSES

Check every serious public project.

Add an appropriate license where appropriate.

Do not blindly add MIT to every repository without considering whether you actually want the code licensed that way.

---

# 37. DEMO GIFS

Record short demos for:

```text
Deploy Forge
The Skynet
Omnitrix OS
```

Target:

```text
15–30 seconds
```

## Deploy Forge

Show:

```text
Repository
 ↓
Deploy
 ↓
Build
 ↓
Logs
 ↓
Live result
```

## The Skynet

Show:

```text
Boot
 ↓
WebGL interaction
 ↓
AI/terminal experience
 ↓
Navigation
```

## Omnitrix OS

Show:

```text
Boot
 ↓
Dial interaction
 ↓
Transformation
 ↓
System navigation
```

Do not make cinematic footage that hides functionality.

---

# 38. REMOVE THESE TYPES OF CONTENT

Remove or rewrite:

```text
Passionate about...
Future...
Dreaming of...
Hardworking...
Fast learner...
Jack of all trades, master of none
```

The chosen personal statement is:

> **Curious enough to learn anything. Disciplined enough to ship.**

Use it consistently.

---

# 39. AI BUZZWORD FILTER

Before publishing, search the profile for:

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

If a paragraph contains several buzzwords but no:

```text
architecture
experiment
measurement
tradeoff
failure
code
```

rewrite it.

---

# 40. RECRUITER 10-SECOND TEST

Open the GitHub profile in a fresh/incognito browser.

Without reading deeply, answer:

```text
Who is Pallav?

AI/ML Engineer · Systems Builder


What is he looking for?

Software / AI/ML internships


What is he building?

Deploy Forge · The Skynet · Synapse


Is there evidence?

Benchmarks + architecture + code


How do I contact him?

Resume · LinkedIn · Email
```

If any answer requires excessive scrolling:

**Move the information upward.**

---

# 41. TECHNICAL INTERVIEWER TEST

Ask a technical reviewer:

```text
1. What does Deploy Forge actually do?
2. Why does Deploy Forge use GitHub Actions?
3. What is the biggest architectural weakness?
4. What did Pallav actually optimize in The Skynet?
5. How was the 883 KB → 24.9 KB measurement obtained?
6. What is Synapse evaluating?
7. What are the major failure modes?
8. What would you improve next?
```

If the READMEs allow the reviewer to answer these questions:

**Good.**

If not:

**Improve documentation before adding visual content.**

---

# 42. DO NOT OVERSELL THE CANDIDATE

The goal is not:

```text
"Make Pallav look senior."
```

The goal is:

```text
"Make Pallav look unusually capable for his experience level."
```

That is a much more believable and compelling signal.

---

# 43. FINAL VISUAL HIERARCHY

The finished profile should roughly feel like:

```text
╔══════════════════════════════════════╗
║          ANIMATED TERMINAL           ║
╚══════════════════════════════════════╝

        AI/ML Engineer · Systems Builder

     Curious enough to learn anything.
        Disciplined enough to ship.

       🟢 OPEN TO INTERNSHIPS

       Resume · LinkedIn · Email


## 🔨 Currently Building

Synapse       Deploy Forge       The Skynet


## 📊 Measured Results

883KB → 24.9KB     ~15s     [Synapse benchmark]


## 🚀 Flagship Projects

Deploy Forge
Architecture · Security · Benchmarks · Demo

The Skynet
WebGL · Performance · Rendering

Synapse
Retrieval · Evaluation · Failure Cases


## 🧠 Engineering Principles

Constraints → Build → Measure → Optimize → Ship


## 🧪 Other Builds

Omnitrix OS · CineVault


## 🛠 Tech Stack


## 📈 GitHub Activity

Stats
Streak
3D graph
Snake


## 🤝 Let's Build Something

LinkedIn · Email · Portfolio
```

---

# 44. FINAL CTA

Add:

```md
## 🤝 Let's Build Something

I'm looking for opportunities to work on real engineering problems across
software systems, AI/ML, developer infrastructure, and performance-focused
applications.

If you're building something interesting, I'd love to hear about it.

**Pallav Dholariya**

[LinkedIn] · [Email] · [Portfolio]

> 🟢 Open to Software Engineering and AI/ML Internship opportunities.
```

---

# 45. IMPLEMENTATION ORDER

**DO NOT IMPLEMENT EVERYTHING AT ONCE.**

Follow these phases exactly.

---

## PHASE A — FIRST SCREEN

- [ ] Keep animated banner
- [ ] Remove Last Activity widget
- [ ] Remove empty WakaTime
- [ ] Add `AI/ML Engineer · Systems Builder`
- [ ] Add personal statement
- [ ] Add internship CTA
- [ ] Add Resume
- [ ] Add LinkedIn
- [ ] Add Email
- [ ] Add Portfolio

### STOP.

Review the first screen before continuing.

---

## PHASE B — INFORMATION ARCHITECTURE

- [ ] Add Currently Building
- [ ] Add Measured Results
- [ ] Move flagship projects above activity widgets
- [ ] Keep 3D contribution graph
- [ ] Move stats/activity below projects
- [ ] Add Engineering Principles
- [ ] Keep Other Builds concise

### STOP.

Review the complete README flow.

---

## PHASE C — DEPLOY FORGE

- [ ] Rewrite positioning
- [ ] Explain actual architecture
- [ ] Highlight sub-path deployment problem
- [ ] Add architecture diagram
- [ ] Add security model
- [ ] Add failure modes
- [ ] Add benchmarks
- [ ] Add meaningful tests
- [ ] Add CI
- [ ] Record demo GIF
- [ ] Improve README

### STOP.

Test Deploy Forge independently.

---

## PHASE D — THE SKYNET

- [ ] Explain original architecture
- [ ] Explain custom renderer
- [ ] Document 883 KB → 24.9 KB
- [ ] Add measurement methodology
- [ ] Add rendering architecture
- [ ] Document actual bugs/failure cases
- [ ] Add tests where useful
- [ ] Add CI
- [ ] Record demo GIF
- [ ] Improve README

### STOP.

Test The Skynet independently.

---

## PHASE E — SYNAPSE

- [ ] Explain actual problem
- [ ] Document architecture
- [ ] Establish baseline
- [ ] Build evaluation dataset
- [ ] Run retrieval benchmark
- [ ] Measure latency
- [ ] Add ablation table
- [ ] Document failure cases
- [ ] Add CI
- [ ] Improve README

### STOP.

Do not publish unsupported AI metrics.

---

## PHASE F — REPOSITORY CURATION

- [ ] Reorder pinned repositories
- [ ] Archive irrelevant projects
- [ ] Update descriptions
- [ ] Standardize flagship READMEs
- [ ] Check licenses
- [ ] Add CI where appropriate
- [ ] Check demos
- [ ] Remove dead links
- [ ] Remove placeholders

---

## PHASE G — FINAL QA

Test:

- [ ] Dark mode
- [ ] Light mode
- [ ] Mobile
- [ ] Desktop
- [ ] Banner
- [ ] Stats
- [ ] Streak
- [ ] 3D graph
- [ ] Snake
- [ ] All project links
- [ ] Resume
- [ ] LinkedIn
- [ ] Email
- [ ] Portfolio
- [ ] Demo links
- [ ] Images
- [ ] GIFs

---

# 46. DEFINITION OF DONE

Do not call the profile complete until:

- [ ] The first screen identifies Pallav in under 5 seconds.
- [ ] Internship availability is obvious.
- [ ] Resume is one click away.
- [ ] No "Last activity: No recent activity" appears.
- [ ] No empty WakaTime block appears.
- [ ] The 3D contribution graph remains.
- [ ] Activity widgets appear after engineering content.
- [ ] Deploy Forge is clearly explained as infrastructure.
- [ ] The Skynet is clearly explained as a performance/WebGL project.
- [ ] Synapse has real evaluation methodology.
- [ ] Metrics are reproducible or explicitly labeled.
- [ ] At least the flagship projects have meaningful tests.
- [ ] Flagship projects have CI where appropriate.
- [ ] Architecture is documented.
- [ ] Failure modes are documented.
- [ ] Limitations are documented.
- [ ] Pinned repositories tell a coherent story.
- [ ] No fake claims exist.
- [ ] No placeholder links exist.
- [ ] No dead widgets exist.
- [ ] No unnecessary visual clutter remains.

---

# 47. THE FINAL HIRING SIGNAL

The profile should make the recruiter think:

> **"This is a second-year student who is already investigating engineering problems beyond tutorial-level projects."**

Then:

> **"He built his own deployment infrastructure."**

Then:

> **"He replaced a major graphics abstraction with a custom WebGL renderer and measured the result."**

Then:

> **"He's experimenting seriously with AI systems."**

Then:

> **"He documents tradeoffs and limitations instead of pretending everything is production-ready."**

Finally:

> **"I want to interview him."**

---

# 48. FINAL PRINCIPLE

## DO NOT MAKE THE GITHUB PROFILE LOUDER.

## MAKE IT HARDER TO DOUBT.

The banner gets attention.

The positioning creates clarity.

The projects create interest.

The architecture creates credibility.

The benchmarks create evidence.

The failure cases demonstrate engineering maturity.

The limitations demonstrate honesty.

The activity visualizations reinforce the personal brand.

The contact CTA creates the next step.

That is the entire strategy.

**Follow this manual seriously.**
**Do not skip the engineering work and compensate with visuals.**
**Do not fabricate evidence to make the profile look stronger.**
**Do not add features outside this specification unless they materially improve recruiter comprehension or engineering credibility.**

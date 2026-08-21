<!-- ===== THEME-AWARE HERO BANNER ===== -->
<!-- GitHub automatically shows dark.svg in dark mode and light.svg in light mode -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Shivala-08/Shivala-08/main/dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Shivala-08/Shivala-08/main/light.svg">
  <img alt="Pallav Dholariya" src="https://raw.githubusercontent.com/Shivala-08/Shivala-08/main/light.svg">
</picture>
## Identity

<h2 align="center">AI/ML Engineer · Systems Builder</h2>

<p align="center">
  Curious enough to learn anything.<br>
  Disciplined enough to ship.
</p>

<p align="center">
  🟢 <strong>OPEN TO SOFTWARE ENGINEERING / AI/ML INTERNSHIPS</strong>
</p>

<p align="center">
  <a href="mailto:pallavdholariya@gmail.com?subject=Resume Request">Resume</a> ·
  <a href="https://www.linkedin.com/in/pallavdholariya/">LinkedIn</a> ·
  <a href="mailto:pallavdholariya@gmail.com">Email</a> ·
  <a href="https://pallav-os.vercel.app">Portfolio</a>
</p>

<br>

---

## 🔨 Currently Building

| Project | Focus |
|---|---|
| 🧠 Synapse | AI / retrieval / experimentation |
| 🚀 Deploy Forge | Git-backed deployment infrastructure |
| 🌐 The Skynet | Custom WebGL + performance engineering |

> Building → measuring → breaking → fixing → shipping.

<br>

---

## 📊 Measured Results

| Project | Measurement | Result |
|---|---|---:|
| The Skynet | 3D renderer bundle | **883 KB → 24.9 KB** |
| Deploy Forge | Local production build | **~15s** |
| Synapse | Retrieval benchmark | **62.5% Accuracy** |

* Synapse evaluation: 62.5% retrieval accuracy, 0.875 Recall@5, 0.667 MRR, and 207 ms query latency on a 40-question ground-truth dataset (LLM-disabled, local SentenceTransformer sandbox).

<br>

---

## 🚀 Featured: Deploy Forge — Git-Backed Deployment Infrastructure

### Why I Built It
I got tired of repeating the manual compile loop: `clone` → `install` → `build` → `copy` → `commit` → `push` → `deploy` for static site prototypes. Traditional serverless applications (like Next.js deployed on Vercel) have read-only filesystems and runtimes that cannot compile arbitrary code. I built Deploy Forge to move this process out of the application request lifecycle.

### Pipeline Flow
```text
GitHub Repository
       │
       ▼
[Deploy Forge API] ──(repository_dispatch)──► [GitHub Actions Runner]
                                                       │
                                                       ▼
                                            [Isolated Build Zone]
                                            - Clone external repo
                                            - npm install && npm build
                                                       │
                                                       ▼
                                            [Path Rewriter Script]
                                            - sed absolute URLs
                                                       │
                                                       ▼
                                            [Git Commit & Push Back]
                                                       │
                                                       ▼
                                            [Vercel Auto-Redeploy]
                                                       │
                                                       ▼
                                                   Live URL
```

### Engineering Challenges & Path Rewriting
When static sites are built, assets like scripts and styles default to absolute references:
```html
<script src="/main.js">
```
When served on a platforms sub-path (`/sites/{id}/`), these references break. Deployed sites must run under sub-path directories without manual configuration.

The pipeline handles this by executing a recursive regex rewording pass on the built HTML and CSS assets inside the runner before pushing back:
```bash
find "public/sites/${SITE_ID}" -name "*.html" -exec \
  sed -i "s|href=\"/|href=\"${BASE_PATH}/|g; s|src=\"/|src=\"${BASE_PATH}/|g" {} \;
```

### Tradeoffs
Using Git commits back to the main repository provides version history and simple persistence for free. However, Vercel must redeploy the DeployForge platform for every new commit, introducing a `30–60s` deployment propagation delay.

* **Status:** `🟢 PRODUCTION`
* [View Source](https://github.com/Shivala-08/deploy-forge) · [Live Demo](https://deploy-forge-4klc.vercel.app)
* [Architecture Docs](https://github.com/Shivala-08/deploy-forge/blob/main/docs/architecture.md) · [Security Model](https://github.com/Shivala-08/deploy-forge/blob/main/docs/security.md) · [Failure Modes](https://github.com/Shivala-08/deploy-forge/blob/main/docs/failure-modes.md) · [Benchmarks](https://github.com/Shivala-08/deploy-forge/blob/main/docs/benchmarks.md)

<br>

---

## 🌐 The Skynet — Custom WebGL Portfolio OS

An interactive browser-based operating system designed to display my technical work while keeping bundle payloads minimal.

### From Library User → Systems Builder
The site's main hero section featured a 3D point network representing a neural graph. Originally loaded via `three.js` and `React Three Fiber`, it introduced an `883 KB` JavaScript chunk and caused blocking rendering frames on mobile.

I deleted the framework dependencies and wrote a dedicated GPU renderer (`mini-renderer.ts`, ~500 lines) that executes WebGL draw calls directly, dropping 3D bundle cost from **883 KB to 24.9 KB** (a **97% reduction**).

### Rendering Flow
```text
Mouse Drag / Scroll Input
          │
          ▼
 [Interaction Layer] ──(raycast hit-test)──► [Matrix Math (mini-math.ts)]
                                                      │
                                                      ▼
                                            [WebGL MiniRenderer]
                                            - Perspective camera
                                            - Shaded mesh instancing
                                            - Per-vertex point cloud
                                                      │
                                                      ▼
                                                 Framebuffer
```

### Engineering Details & Transform Bug
* **Shader Gradients:** Avoided multi-material overhead by baking the color-grade function directly into the point/line fragment shaders.
* **Transform Bugs:** During development, camera raycast picking failed. Debugging revealed an incorrect column-major matrix transposition inversion in the math loop. I resolved it by correcting the row-column indices in `Mat4.invert`.

* **Status:** `🟢 PRODUCTION`
* [View Source](https://github.com/Shivala-08/The-skynet) · [Live Demo](https://pallav-os.vercel.app)
* [Performance Docs](https://github.com/Shivala-08/The-skynet/blob/main/docs/performance.md) · [Rendering Docs](https://github.com/Shivala-08/The-skynet/blob/main/docs/RENDERING.md)

<br>

---

## 🧠 Synapse — Knowledge Intelligence Engine

A personal R&D project exploring **hybrid retrieval, knowledge-graph-augmented RAG, and adaptive complexity model routing**.

### System Architecture
```text
           User Query
                │
                ▼
        [Semantic Cache] ── Cache Hit ──► Immediate Response (196ms)
                │ Cache Miss
                ▼
     [Complexity Classifier]
                │
                ├─────► Fast Path ────► Llama 3.1 8B (Low Latency)
                │
                └─► Deep Reasoning ───► Nemotron 3 Ultra 550B (High Budget)
                        ▲
                        │ Context Injection
                ┌───────┴───────┐
                │  Hybrid Search│ (Vector Store + NetworkX Graph)
                └───────────────┘
```

### Retrieval Evaluation
To measure retrieval quality without LLM bias, Synapse contains a deterministic ablation harness. Running across a 40-question ground-truth set showed that adding a cross-encoder re-ranker was the single largest accuracy contributor (+11 points) but introduced a **200ms** latency penalty.

### Failure Modes
* **Multi-Hop Synthesis:** Chunks are retrieved based on independent semantic similarity. Questions requiring cross-document synthesis (e.g. comparing two different circulars) frequently fail semantic match criteria when evaluated with the LLM disabled.

* **Status:** `🟡 ACTIVE DEVELOPMENT`
* [View Source](https://github.com/Shivala-08/synapse)
* [Evaluation Docs](https://github.com/Shivala-08/synapse/blob/main/docs/evaluation.md)

<br>

---

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

<br>

---

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

<br>

---

## 📈 GitHub Activity

<div align="center">

<!-- Streak — full width -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=Shivala-08&hide_border=true&background=0A101F&stroke=22D3EE&ring=A78BFA&fire=10B981&currStreakLabel=22D3EE&sideLabels=94A3B8&currStreakNum=F8FAFC&sideNums=F8FAFC&dates=64748B&titleColor=22D3EE&card_width=1180" />
  <img width="100%" src="https://streak-stats.demolab.com/?user=Shivala-08&hide_border=true&background=FFFFFF&stroke=0891B2&ring=7C3AED&fire=059669&currStreakLabel=0891B2&sideLabels=475569&currStreakNum=0F172A&sideNums=0F172A&dates=94A3B8&titleColor=0891B2&card_width=1180" alt="Streak" />
</picture>

<br>

<!-- Stats — center width -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats-eight-theta.vercel.app/api?username=Shivala-08&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&hide_border=true&title_color=22D3EE&icon_color=A78BFA&text_color=94A3B8&bg_color=0A101F&card_width=500" />
  <img width="60%" src="https://github-readme-stats-eight-theta.vercel.app/api?username=Shivala-08&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&hide_border=true&title_color=0891B2&icon_color=7C3AED&text_color=0F172A&bg_color=FFFFFF&card_width=500" alt="GitHub Stats" />
</picture>

<br>

<!-- ===== 3D CONTRIBUTION GRAPH ===== -->
![3D contribution graph](./profile-3d-contrib/profile-night-rainbow.svg)

<br>

<!-- ===== CONTRIBUTION SNAKE ===== -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Shivala-08/Shivala-08/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Shivala-08/Shivala-08/output/github-snake.svg" />
  <img alt="Snake eating my contributions" src="https://raw.githubusercontent.com/Shivala-08/Shivala-08/output/github-snake.svg" />
</picture>

</div>

<br>

---

## 🧪 Other Builds

<div align="center">
  <img width="100%" src="https://raw.githubusercontent.com/Shivala-08/Shivala-08/projects/projects.svg" alt="Featured Projects Grid" />
</div>

<div align="center">

| Project | Role | Status | Links |
| --- | --- | --- | --- |
| `Deploy Forge` | Solo | 🟢 Live | [Repo](https://github.com/Shivala-08/deploy-forge) · [🔗 Live Demo](https://deploy-forge-4klc.vercel.app) |
| `Synapse AI Engine` | Solo | 🟡 In Dev | [Repo](https://github.com/Shivala-08/synapse) |
| `The Skynet` | Solo | 🟢 Live | [Repo](https://github.com/Shivala-08/The-skynet) · [🔗 Live Demo](https://pallav-os.vercel.app) |
| `Omnitrix OS` | Solo | 🟢 Live | [Repo](https://github.com/Shivala-08/ben-10-os) · [🔗 Live Demo](https://ben-10-os.vercel.app) |

</div>

<br>

### 🟢 Omnitrix OS
* **Problem:** Build a highly interactive, responsive 3D dashboard representation of the Omnitrix interface.
* **Build:** Utilized Next.js, Three.js, and GSAP timeline choreography with custom Web Audio synthesis.
* **Result:** Achieved steady `116fps` render speed on mobile and desktop devices.
* [Repo](https://github.com/Shivala-08/ben-10-os) · [Demo](https://ben-10-os.vercel.app)

### 🎬 CineVault
Full-stack movie discovery application exploring API integration, discovery UX, and scalable frontend patterns.
* [Repo](https://github.com/Shivala-08/cinevault) · [Demo](https://cinevault-eight-red.vercel.app)

<br>

---

## Lab Notes

Things I'm currently trying to understand:
* **RAG Chunking Strategy:** How retrieval quality changes with dynamic semantic boundary chunking vs. fixed-token limits.
* **RAG Evaluation:** Finding repeatable, automated retrieval metrics (Recall/MRR) to measure pipeline shifts without relying on "it feels good."
* **GPU Context Underneath Frameworks:** Understanding how vertex/index buffers and shaders bind to OpenGL/WebGL contexts without rendering abstractions.
* **Process Isolation:** How self-hosted build engines can safely isolate user-submitted scripts during compilation phases.

<br>

---

## 🤝 Let's Build Something

I'm looking for opportunities to work on real engineering problems across software systems, AI/ML, developer infrastructure, and performance-focused applications.

If you're building something interesting, I'd love to hear about it.

**Pallav Dholariya**

<div align="center">

[**💼 LINKEDIN**](https://www.linkedin.com/in/pallavdholariya/) &nbsp;•&nbsp; [**✉️ EMAIL ME**](mailto:pallavdholariya@gmail.com)

</div>

> 🟢 Open to Software Engineering and AI/ML Internship opportunities.

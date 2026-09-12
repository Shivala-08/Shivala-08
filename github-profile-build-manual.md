# GitHub Profile Build Manual — Agent Instructions

**Scope.** This is a build spec for an AI coding agent (e.g. Claude Code) to build an animated
terminal-style GitHub profile for `Shivala-08/Shivala-08`, in the same technical style as the
`arifhaxn/arifhaxn` reference build (banner + stats + snake + projects grid), extended with the extra
sections requested below. All infrastructure is assumed **already live**:

- ✅ Profile repo `Shivala-08/Shivala-08` exists, public, on `main`
- ✅ github-readme-stats is forked and self-hosted on Vercel with `PAT_1` set
- ✅ Repo Settings → Actions → Workflow permissions = Read and write
- ✅ `.github/workflows/snake.yml` triggers (cron / dispatch / push) are enabled

Do **not** re-do repo creation, token generation, Vercel deploy, or Actions permission toggling. This
manual only covers the *content* the agent needs to generate and commit.

---

## 0. Reference values (this profile — use these exactly, don't re-ask)

### Personal Details

```
Name:            Pallav Dholariya
GitHub Username: Shivala-08        → repo Shivala-08/Shivala-08, branch main
Role:            AI/ML Engineer • Full-Stack Developer
Bio:             Curious enough to learn anything. Disciplined enough to ship.
Location:        Pune, Maharashtra, India
Education:       B.Tech in Computer Science & Engineering (AI & ML)
                 Newton School of Technology × ADYPU
```

### Current Status

- 🔭 Building…
- 📚 Learning…
- 🚀 Shipping…

### Tech Stack

**Languages**
- Python
- JavaScript
- SQL
- Bash

**Frontend**
- React
- Next.js
- Tailwind CSS
- HTML5
- CSS3
- Framer Motion
- Lenis

**Backend**
- FastAPI

**Databases**
- PostgreSQL
- Supabase

**DevOps & Infrastructure**
- Docker
- GitHub Actions
- Vercel
- Cloudflare
- Linux
- ngrok

**Tools**
- VS Code
- Git
- Claude Code
- Antigravity IDE

### Featured Projects

- Omnitrix OS
- CineVault
- Deploy Forge

(no taglines/tags/stars given — pull real data for these three repos from the GitHub API,
same rule as Phase 5 below; don't invent descriptions)

### Social Links

```
GitHub:      https://github.com/Shivala-08
LinkedIn:    https://www.linkedin.com/in/pallavdholariya
Email:       pallavdholariya@gmail.com
Portfolio:   Coming Soon (no live URL — see badge note in Phase 4)
Instagram / Facebook: not provided — omit those badges entirely, don't fabricate handles
```

### Design Preferences

**Theme:** Cyberpunk (Option C)

**Personality target:** Professional, Premium, Futuristic, Cyberpunk, Terminal Hacker. No exact hex
codes were given for this theme, so propose (don't silently assume) a palette and confirm before
building the banner — this is the single highest-leverage check-in of the whole project. A defensible
starting point that keeps the "premium," not "novelty," reading:

```
Background:     #0A0014 (near-black, cold violet undertone)
Primary neon:   #F72585 (magenta) — for the pulsing LIVE badge, key accents, headline highlights
Secondary neon: #00F5FF (cyan) — UI chrome: borders, dotted leaders, panel labels
Accent:         #9D4EDD (electric purple) — pill/tag fills, secondary highlights
Portrait dot hue: pick ONE of magenta or cyan for dot density (not both — see palette rule below)
```

**Palette rule (unchanged from the reference build):** the portrait dot hue must differ from the UI
chrome hue, or the face blends into its own frame. With a magenta/cyan pair, put the portrait in
whichever of the two is *not* used for the panel borders and text.

**Cyberpunk vs the reference build's "no glitch" rule:** the original banner spec explicitly bans grid
lines, scanlines, glitch bars, and CRT flicker *inside the dithered portrait* — that rule still holds,
because those effects break the dither at rendering size. "Terminal Hacker" cyberpunk texture (subtle
scanline overlay, a soft neon glow/blur on the chrome, a blinking cursor) can still be applied to the
**UI chrome** — panel borders, the title bar, the `LIVE` badge, section headers — just not to the
portrait dot layer itself. Flag this distinction to the user rather than either dropping the cyberpunk
texture entirely or breaking the portrait to chase it.

### README Sections (order)

1. About Me
2. Animated Banner
3. Tech Stack
4. Visitor Counter
5. GitHub Stats
6. GitHub Streak
7. Top Languages
8. Contribution Snake
9. Activity Graph
10. Featured Projects
11. Coding Quote
12. Random Dev Joke
13. Contact

### Primary Goal

Build a GitHub profile that:
- Impresses recruiters
- Helps land internships
- Builds a strong personal brand
- Demonstrates AI engineering expertise
- Looks polished and senior-engineer level

---

Work through the phases below **in order**, checking in with the user after each phase. Show one
variation and let them react — don't generate five options at once.

---

## Phase 1 — Banner (`dark.svg` / `light.svg`)

This is the only phase that genuinely needs AI/code execution (Python + Pillow/NumPy/SciPy). The
rest is templating. Budget most of the session here; expect real back-and-forth on contrast and crop.

**Canvas:** one terminal window, 1180×610, titled `profile.sh --live`. Left ~38% = portrait panel
labelled `VISUAL.MAP`. Right = `SYSTEM.INFO` readout with dotted leaders, a pulsing `LIVE` badge
(recolour from red to the primary neon — red reads as an error state, not cyberpunk), and a coloured
pill with the handle.

### 1a. Portrait generation (Python)

1. Crop head + shoulders — not a tight face crop (over-zoomed reads aggressive). Needs the user's
   photo: flat/uniform background, even face lighting, 1000px+ short edge — request it if not yet
   supplied.
2. Resample to a 300×340 grid, then 1-bit Floyd–Steinberg dither in serpentine order.
3. Contrast: `autocontrast(cutoff=1)` + `UnsharpMask(radius=3, percent=140)` only — cap at 1.3×.
   (2.4× was tried and rejected on the reference build: harsh, skull-like.)
4. Render dots as `<path>` runs with `shape-rendering="crispEdges"`. Never font glyphs — they mush
   below ~2px.
5. **Dark mode:** segment the background out — threshold on colour distance, binary closing, fill
   holes, keep the largest connected component — so dots draw only the lit subject. Hard-clear
   error-diffusion bleed at the mask edge, or dark mode reads as a photo negative.
6. **Light mode:** keep the background; dots draw the dark parts of the photo.
7. Single hue only — all tone comes from dot density, not colour variation (see theme note above for
   which neon to use).
8. No grid lines, scanlines, glitch bars, or CRT flicker inside the portrait layer itself.

### 1b. Intro animation (~3.2s, plays once)

- ~60 interleaved random groups fade in over ~2s.
- Each group must be scattered across the *whole* portrait so dots appear everywhere at once and
  thicken together. **Do not** wipe. **Do not** group by spatial region — that reveals patch-by-patch.
- Verify with an evenness metric: ~0.05 = good, ~0.7 = patchy (re-shuffle grouping if so).
- Requires a duplicate portrait layer (~180KB). Merging to one layer breaks the intro.

### 1c. Loop animation (~14.2s, repeating)

Two independent layers:

- **Portrait layer** — full density (~17k dots), grouped into ~94 drift bands. Each band translates
  ~42% toward the first logo's centroid while fading, then returns.
- **Traveller layer** — ~900 dots that morph between three logo targets, matched by optimal transport
  so each dot takes the shortest path. Opacity keyframes `0;0;0;1;1;...;0` so travellers are hidden
  during the portrait phase (otherwise their thicker dots crowd the fine dither). **Ask the user which
  three logos/marks to morph between** — none were specified (candidates given the stack: React,
  FastAPI, and a generic `</>` or terminal-cursor glyph would fit, but confirm rather than assume).

Timing: portrait holds 3.0s, each logo holds 2.0s, transitions are 1.3s. Use **explicit uneven
`keyTimes`** — evenly-spaced keyframes force every phase to the same length, which is wrong here.

**The grid trap:** drift is a linear function of position, so quantizing it into groups mathematically
recreates a square grid, and the dissolve looks blocky. Add per-dot noise (sigma ~4) before grouping.
Verify with a straight-boundary metric: ~0.01 = organic, ~0.17 = you built a grid.

**Core tradeoff to respect:** portrait quality needs ~17,000 dots; living per-dot motion needs ~1,000.
These don't work in a single layer — the two-layer design (dense static + sparse traveller) is the
resolution, not a compromise to optimize away.

### 1d. Info panel (tech-stack rows — restructured for this profile's six categories)

The reference build used five `Core.*` categories; this profile has **six**, so widen the panel or drop
to a slightly smaller row height (still ≥ readable at 13–14px) rather than cramming or truncating.

- Row font-size 14, header 13, `LIVE` 12, pill 14, spacing 23px (tighten toward ~20px if six rows +
  the header block doesn't fit 610px height cleanly — check before committing).
- Lock every row with `textLength` + `lengthAdjust="spacingAndGlyphs"` so values stay right-aligned
  regardless of viewer font.
- Dotted leaders computed from label/value string length — never hand-edit the SVG.
- Rows:
  - `Subject, Role, Origin, Education, Status`
  - `Stack.Languages, Stack.Frontend, Stack.Backend, Stack.Databases, Stack.DevOps, Stack.Tools`
  - `Grid.GitHub, Grid.LinkedIn, Grid.Mail, Grid.Portfolio`
- Long lists (e.g. Frontend has 7 items, DevOps has 6) will overflow a single dotted-leader row at
  14px — either wrap to two lines with reduced leading, or comma-truncate with a `+N more` suffix
  and put the full list only in the actual README Tech Stack section (Phase 1g below), not squeezed
  into the banner. Don't shrink font below ~11px to force a fit — that breaks legibility, which is the
  thing this panel exists for.
- Bio line (`Curious enough to learn anything. Disciplined enough to ship.`) doesn't fit the
  label/value row format — place it as a one-line subtitle under the terminal title bar, not as a
  `SYSTEM.INFO` row.

### 1e. Verification (do this, don't eyeball it)

- `cairosvg` only renders the first SMIL frame and mishandles additive transforms and `textLength` —
  use it only for correlation-vs-approved-render checks, band distributions, and ink coverage, then
  have the user confirm visually in an actual browser.
- Known cosmetic issue: at GitHub's ~900px README width the dot lattice can show faint vertical
  moiré banding. It disappears on zoom — the fix is a coarser portrait (fewer, larger dots), and it's
  rarely worth chasing further.
- Expect the final banner file size to land ~900KB–1MB. Warn the user before changes likely to grow
  it further (per-dot jitter alone pushed the reference build to 2.8MB).
- Keep the generator script and any `.npy` intermediate data as the source of truth — not the SVG
  output — so edits are re-runs, not hand-patches.

### 1f. Upload

Commit `dark.svg` and `light.svg` to the root of `Shivala-08/Shivala-08` (repo already exists).

### 1g. Full Tech Stack README section (separate from the banner panel)

Since "Tech Stack" is its own requested README section, give it a proper block below the banner —
grouped headers matching the six categories above, each as a row of tag badges (shields.io static
badges or simple bold-label + comma list, themed to the palette). This is where the *complete* lists
live; the banner panel can stay abbreviated per 1d.

---

## Phase 2 — Stats, streak, and top-languages cards (no deploy work — instance already live)

Using the existing self-hosted instance URL, generate this block (join into one line; wrapped here for
readability):

```html
<div align="center">
<img width="100%" src="https://streak-stats.demolab.com/?user=Shivala-08&hide_border=true&background=0A0014&stroke=00F5FF&ring=F72585&fire=9D4EDD&currStreakLabel=00F5FF&sideLabels=94A3B8&currStreakNum=F8FAFC&sideNums=F8FAFC&dates=64748B&titleColor=00F5FF&card_width=1180" alt="streak" />
<br/>
<img width="49%" src="https://YOUR-INSTANCE.vercel.app/api?username=Shivala-08&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&hide_border=true&title_color=00F5FF&icon_color=F72585&text_color=94A3B8&bg_color=0A0014&card_width=500" alt="stats" />
<img width="49%" src="https://YOUR-INSTANCE.vercel.app/api/top-langs/?username=Shivala-08&layout=compact&langs_count=8&hide_border=true&title_color=00F5FF&text_color=94A3B8&bg_color=0A0014&card_width=500" alt="top langs" />
</div>
```

Substitute `YOUR-INSTANCE` with the real Vercel URL. Keep `hide_rank=true` — the letter grade is
stars/follower-weighted and misleading for newer accounts; it measures repo popularity, not skill.

---

## Phase 3 — Contribution snake (workflow file only — Actions permissions already set)

Commit `.github/workflows/snake.yml`:

```yaml
name: Generate Snake Animation

on:
  schedule:
    - cron: "0 */12 * * *"
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  generate:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - name: Generate snake SVGs
        uses: Platane/snk/svg-only@v3
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/github-snake.svg?palette=githublight&color_snake=9D4EDD&color_dots=#ebedf0,#f0abfc,#e879f9,#c026d3,#9D4EDD
            dist/github-snake-dark.svg?palette=githubdark&color_snake=F72585&color_dots=#2d1b3a,#5b2a6e,#9D4EDD,#F72585,#00F5FF
      - name: Push to output branch
        uses: crazy-max/ghaction-github-pages@v3.1.0
        with:
          target_branch: output
          build_dir: dist
          commit_message: "Update snake animation [skip ci]"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Colour rule:** the first colour in `color_dots` is the empty cell. For the dark snake it must be a
visible slate/purple like `#2d1b3a` — against GitHub's dark background (`#0d1117`) a near-black empty
cell disappears and the grid reads as broken.

Commit to `main`, confirm the Actions tab run goes green (~1 min) and creates the `output` branch,
**then** add the display block:

```html
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Shivala-08/Shivala-08/output/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Shivala-08/Shivala-08/output/github-snake.svg" />
  <img alt="Contribution snake" src="https://raw.githubusercontent.com/Shivala-08/Shivala-08/output/github-snake.svg" />
</picture>
</div>
```

Adding this before the Action runs green will show a broken image (the `output` branch won't exist yet).

---

## Phase 4 — Social badges (Contact section)

Only three real links were given — don't add Instagram/Facebook badges, they weren't provided:

```html
<div align="center">
<a href="https://github.com/Shivala-08">
  <img src="https://img.shields.io/badge/GitHub-0A0014?style=for-the-badge&logo=github&logoColor=00F5FF" alt="GitHub" />
</a>
&nbsp;&nbsp;
<a href="https://www.linkedin.com/in/pallavdholariya">
  <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>
&nbsp;&nbsp;
<a href="mailto:pallavdholariya@gmail.com">
  <img src="https://img.shields.io/badge/Email-0A0014?style=for-the-badge&logo=gmail&logoColor=F72585&labelColor=0A0014" alt="Email" />
</a>
</div>
```

**LinkedIn bug:** shields.io only renders the LinkedIn glyph on brand blue `#0A66C2`. Any custom
colour silently drops the logo, leaving just text. Either accept brand blue (used above), or embed the
glyph as a base64 data-URI to keep it themed.

**Portfolio is "Coming Soon"** — don't render a dead-link badge. Either omit it until there's a real URL,
or render a visually distinct, non-clickable "Portfolio — coming soon" chip so it doesn't read as a
broken link.

Skip a GitHub badge in the *reference* build's convention (circular on your own profile) — but here
it's explicitly listed as a social link the user wants shown, so include it; that's a deliberate deviation
from the reference, not an oversight.

---

## Phase 5 — Featured Projects grid

Same visual pattern as the reference build's `PROJECTS.LIST` panel: terminal-style header
(`PROJECTS.LIST` / `./projects.sh --all`), 2-column card grid, dark panel background, each card with
an icon tile, bold project name, one-line tagline, tech tag pills, a star-count + updated-time footer,
and a language-percentage donut.

**Repos to feature:** Omnitrix OS, CineVault, Deploy Forge.

**No taglines, tags, star counts, or language breakdowns were provided for these three** — pull them
live from the GitHub API (repo description, topics, primary/secondary language %, stargazer count,
`pushed_at`) rather than inventing plausible-sounding copy. If a repo has no description or topics set
on GitHub, flag that back to the user instead of fabricating one — a placeholder tagline undermines
the "impresses recruiters" goal more than a brief pause to ask does.

---

## Phase 6 — Visitor counter

Simple embedded badge, no self-hosting needed:

```html
<img src="https://komarev.com/ghpvc/?username=Shivala-08&label=Profile%20Views&color=F72585&style=for-the-badge" alt="Profile views" />
```

Place it near the top of the README (directly under the banner is the conventional spot) so it's the
first thing after the animated header, not buried near the footer.

---

## Phase 7 — Activity graph

Uses `ashutosh00710/github-readme-activity-graph`, no fork/deploy required (public instance is fine
here — it isn't the same rate-limited service as github-readme-stats):

```html
<img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=Shivala-08&theme=react-dark&hide_border=true&bg_color=0A0014&color=00F5FF&line=F72585&point=9D4EDD" alt="activity graph" />
```

If this specific public instance is unreliable, self-hosting it follows the identical fork-and-deploy
pattern as Phase 2 (skip, since deploy work is out of scope here) — flag to the user only if the public
instance is actually rate-limiting, don't pre-emptively self-host.

---

## Phase 8 — Coding quote

A rotating dev-quote badge, e.g.:

```html
<img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=radical" alt="coding quote" />
```

Theme this to the closest available preset (or the service's custom-colour params, if it supports them)
rather than forcing a mismatched default theme into an otherwise fully-themed cyberpunk README.

---

## Phase 9 — Random dev joke

Similar pattern to Phase 8 — a joke-API badge (e.g. a `readme-jokes` GitHub Action or a static badge
service). Two implementation options, flag the tradeoff to the user rather than picking silently:

- **Static badge/image service** — zero setup, but the joke only refreshes on the service's own
  schedule/cache, not "one per profile view."
- **Scheduled GitHub Action** (like the snake workflow) that fetches a joke and rewrites a README
  section on a cron — more control, but it's another workflow to maintain and another thing that can
  go stale silently if the Action stops running (same "pauses after ~60 days of inactivity" risk as the
  snake).

---

## Phase 10 — About Me section

A short prose block above or just below the banner, built from the given bio and status lines — not
invented. Suggested shape (adapt formatting to the cyberpunk theme, keep the words as given):

```
> Curious enough to learn anything. Disciplined enough to ship.

- 🔭 Building…
- 📚 Learning…
- 🚀 Shipping…
```

Don't pad this with generic filler ("passionate developer," "love solving problems") that wasn't
supplied — the given bio is already tight and on-brand; keep it that way.

---

## Final assembly

Assemble in the order the user specified for README Sections:

1. About Me (Phase 10)
2. Animated Banner (Phase 1)
3. Tech Stack (Phase 1g)
4. Visitor Counter (Phase 6)
5. GitHub Stats (Phase 2)
6. GitHub Streak (Phase 2)
7. Top Languages (Phase 2)
8. Contribution Snake (Phase 3)
9. Activity Graph (Phase 7)
10. Featured Projects (Phase 5)
11. Coding Quote (Phase 8)
12. Random Dev Joke (Phase 9)
13. Contact (Phase 4)

## Working rules for the agent

- Verify by measurement (correlation, evenness/boundary metrics, ink coverage), not by eye — then
  ask the user to confirm in an actual browser.
- If the user says something "didn't change": check the raw file first
  (`raw.githubusercontent.com/.../file.svg?v=999`, view-source, search the hex colour) before
  assuming a bug — it's almost always CDN cache or the wrong theme (dark assets only render in dark
  mode).
- Flag file-size growth honestly before committing to an approach that will bloat the SVG.
- Confirm the cyberpunk palette (Section 0) and the three logo-morph targets (Phase 1c) before
  building the banner — both were left open by the brief and are expensive to redo after the fact.
- Pull all project/repo data live from the GitHub API (Phase 5) rather than inventing taglines, tags, or
  stats — this profile's stated goal is to impress recruiters, and fabricated-looking data undermines
  that more than an honest "still needs a description" flag does.
- If an idea won't work or costs more than it's worth, say so instead of building it.
- If the user rejects something twice, stop and ask rather than trying a third variation.
- Two failure modes to actively guard against, carried over from the reference build: grouping the
  intro fade by spatial region (patchy reveal), and quantized linear drift without per-dot noise (grid
  trap).

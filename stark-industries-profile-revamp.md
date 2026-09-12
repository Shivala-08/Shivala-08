# STARK INDUSTRIES — GITHUB PROFILE REVAMP PROTOCOL
### Subject: Shivala-08 (Pallav Dholariya) · Filed under: "It's not vanity if it's engineered."

---

Alright. I pulled the schematics. You already built something — Game of Life art seeded from
your own commit history, that's not a template, that's *taste* — but a workshop full of good
parts isn't a suit yet. Nothing here is on fire. Everything here is inconsistent. Four different
colour languages fighting for the same screen. That's the actual problem, and it's the only one
worth fixing first. Let's suit this thing up properly.

This document is for whichever coding agent picks up the tools next. Read it like a build log,
not a suggestion box. Every phase below assumes the boring infrastructure — repo, Vercel,
Actions permissions — is already live and wired. **Don't touch deploy plumbing. Touch design.**

---

## PHASE 0 — DIAGNOSTIC SCAN (what's actually on the suit right now)

I had JARVIS run a scan. Here's the manifest, panel by panel, exactly as observed live at
`github.com/Shivala-08`:

| Panel | What's there | Colour language it's using |
|---|---|---|
| Banner (`VISUAL.MAP` + `SYSTEM.INFO`) | Dithered portrait, dotted-leader spec sheet, pulsing `LIVE` badge | Cyan/purple, dark navy background |
| Identity | Headline "AI/ML Engineer · Systems Builder", bio, green "open to internships" dot, Resume/LinkedIn/Email/Portfolio links | Neutral white/grey on black |
| GitHub Activity — stat row | 1,151 total contributions · 3 current streak (fire icon) · 11 longest streak | Cyan ring, orange flame |
| GitHub Activity — stats card | Stars 0 · Commits 2.3k · PRs 16 · Issues 0 · Contributed-to 4 | Cyan header, purple icons |
| GitHub Activity — radar chart | Commit / Issue / PullReq / Review / Repo pentagon | **Gold/amber** — doesn't match anything else on the page |
| GitHub Activity — 3D isometric graph | Extruded contribution blocks + language donut (TypeScript/HTML/CSS) | **Blue-to-magenta gradient** — a *third* palette |
| Game of Life panel | `./life.sh --seed=contributions --generations=20`, evolving pixel-art from two cellular-automaton runs | **Teal** — a *fourth* palette |
| Other Builds grid | 4 project cards (`deploy-forge`, `synapse`, `The-skynet`, `ben-10-os`), each with LIVE/WIP status chip, tags, demo link, star count, updated-time | Purple icon tiles, green/orange status chips |
| Contact footer | Resume · LinkedIn · Email · Portfolio (portfolio is live now — `pallav-os.vercel.app`, no longer "coming soon") | Plain text links |

**Verdict, and I mean this as an engineer, not a critic:** every individual panel is well-made.
None of them are talking to each other. That's Mark I syndrome — a pile of great parts bolted
onto the same chassis in whatever colour the library defaulted to. The fix isn't "add more
panels." The fix is **one palette, applied everywhere**, plus filling the three gaps that were on
the original spec and never got built.

**Also flagging, don't skip this:** the earlier project shortlist (Omnitrix OS, CineVault,
Deploy Forge, Udhaar Ledger) doesn't match what's actually live (`deploy-forge`, `synapse`,
`The-skynet`, `ben-10-os`). CineVault and Udhaar Ledger aren't on the grid; Synapse AI Engine
and The Skynet are, and weren't on the original list. **Confirm the final four with the user
before rebuilding the grid** — don't silently drop or silently keep projects based on a guess.

**Gaps versus the original wishlist — never got built, still worth building:**
- Visitor counter — absent.
- Coding quote — absent.
- Random dev joke — absent.
- Dark/light theme swap on the banner — needs verifying; confirm it's a real `<picture>` element
  with both `dark.svg` and `light.svg` sources, not a single static image pretending to be
  theme-aware.

---

## PHASE 1 — THE ARC REACTOR (unified palette — do this before touching anything else)

Every retrofit starts with a power source. Here's the one palette every panel below pulls from.
No more gold radar charts next to purple stat cards next to teal life-art. One suit, one glow.

```
Background (deep space):     #05060A
Arc reactor cyan (primary):  #00E5FF   — chrome, borders, primary data lines, the LIVE badge
Repulsor gold (accent):      #FFC857   — highlights, hover states, "look here" moments
Mark-VII red (alert/status): #E23636   — used ONLY for status chips that mean "hot" (LIVE, WIP-active)
Titanium grey (secondary):   #8892A6   — secondary labels, muted text, timestamps
Success green (unchanged):   #2ED573   — keep the existing "open to internships" green, it's already correct and doesn't need to fight the new palette
```

Rule: **one accent per visual weight class.** Cyan carries structure (borders, leaders, chrome).
Gold carries emphasis (the one number, tag, or line you want the eye to land on per panel). Red
is reserved for state, not decoration — if everything glows red, nothing means "hot" anymore.
Apply this to every panel in the diagnostic table. That alone will make the profile look like one
build instead of four different tutorials stitched together.

---

## PHASE 2 — THE SUIT-UP SEQUENCE (banner: `dark.svg` / `light.svg`)

Keep the existing structure — dithered portrait in `VISUAL.MAP`, dotted-leader spec sheet in
`SYSTEM.INFO` — it's good bones. Retrofit, don't rebuild from scratch:

1. **Recolour the portrait dot layer** to arc-reactor cyan `#00E5FF` (dark mode) — replace
   whatever mixed cyan/purple is currently rendering. Single hue only, per the original dither
   spec: no colour variation, all tone from dot density.
2. **Recolour the `LIVE` badge** from its current pulse colour to repulsor gold `#FFC857`, pulsing
   at the same rate. Gold reads as "power source," not "error," which red does — save red for
   actual status chips elsewhere (Phase 5).
3. **Verify the theme swap is real.** Confirm the README embeds an actual `<picture>` element:
   ```html
   <picture>
     <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Shivala-08/Shivala-08/main/dark.svg">
     <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Shivala-08/Shivala-08/main/light.svg">
     <img alt="Pallav Dholariya" src="https://raw.githubusercontent.com/Shivala-08/Shivala-08/main/light.svg">
   </picture>
   ```
   If it's currently a bare `<img>` pointing at one file, that's a real bug, not a style choice —
   fix it before doing anything else in this phase. Test both themes after.
4. **Tech-stack rows** — the current `ToolChain`/`Core.*` rows already reflect the live stack
   (Python, JavaScript, TypeScript, SQL · React, Next.js, Tailwind CSS · FastAPI, Node.js ·
   PostgreSQL, Supabase · Docker, GitHub Actions, Vercel, Linux). Keep this list as the source of
   truth — it's more current than any earlier draft of this manual. Don't regress it.
5. Leave the animation choreography (intro fade, drift/traveller loop) as-is if it's already
   running well — this phase is a *palette and correctness* pass, not a rebuild. Only touch
   timing/motion if the user specifically flags it as sluggish or broken.

---

## PHASE 3 — THE HUD (Identity section)

This section is already doing its job — clean headline, honest bio in the user's own words, a
real "open to internships" signal, working contact links. Don't rewrite the copy; a fabricated
Stark-flavoured bio would undercut the "impresses recruiters" goal harder than a plain one ever
could. Two structural fixes only:

1. Recolour the section divider rule and any accent underline to arc-reactor cyan, matching
   Phase 1.
2. Add a GitHub badge/link alongside Resume · LinkedIn · Email · Portfolio if one isn't already
   there — it was requested as a Contact-section link in the original brief and the footer only
   shows it as a profile-level link, not inline here.

---

## PHASE 4 — THE TELEMETRY DECK (GitHub Activity: streak, stats, radar, 3D graph)

This is where the palette chaos is worst — three sub-panels, three different accent colours.
Recolour, don't rebuild the charts themselves:

- **Streak/stat row** — already cyan-forward, keep it, just confirm the flame icon on the
  current-streak ring uses gold `#FFC857` instead of orange, so it reads as "this system" and
  not "borrowed from a different template."
- **Stats card** ("My GitHub Statistics") — recolour header text and icons to cyan + gold per
  Phase 1's weight-class rule (structure = cyan, the one metric worth emphasizing = gold).
- **Radar chart** — currently gold-only against a dark background with no other accent; bring
  the axis labels and grid lines to titanium grey `#8892A6` so the gold fill actually pops instead
  of fighting flat gold-on-gold, and so it stops looking like a leftover from a different
  dashboard.
- **3D isometric activity graph + language donut** — currently blue-to-magenta gradient cubes
  and a TypeScript/HTML/CSS donut in unrelated colours. Recolour the cube gradient to a cyan→gold
  ramp (cyan at low-activity, gold at peak-activity days) so it visually says "this is the same
  system as the banner," and retint the donut segments to sit within the palette (cyan, gold,
  titanium grey) rather than arbitrary per-language defaults.

---

## PHASE 5 — THE GAME OF LIFE PANEL (keep this, it's the best idea on the page)

Don't touch the concept. A cellular automaton seeded from real commit history is exactly the
kind of "demonstrates AI/engineering thinking" flourish that separates a memorable profile from
a template one. Only change:

- Recolour the live cells from teal to arc-reactor cyan, dead/background cells to the deep-space
  background colour, so it reads as part of the same system rather than a fourth palette.
- Keep the `$ ./life.sh --seed=contributions --generations=20` command-echo styling exactly as
  is — that terminal-authenticity detail is doing real work and shouldn't be "improved" into
  something generic.

---

## PHASE 6 — OTHER BUILDS (project grid)

Structure is good — status chips (LIVE/WIP), tags, demo links, star count, updated-time are all
the right ingredients. Retrofit:

1. **Confirm the final four projects with the user** before touching content (see Phase 0 flag).
   Don't silently reconcile the old wishlist against the live grid.
2. Recolour: icon tiles to a single consistent tint (cyan or gold, pick one, don't mix per-card),
   status chips stay semantically coded — green/`#2ED573` for LIVE, gold `#FFC857` for WIP (not
   orange — keep it inside the palette), tags as thin cyan-outlined pills instead of solid purple.
3. Pull all copy (taglines, tags, star counts, update times) live from the GitHub API per repo —
   the existing taglines ("6 manual deploy steps → 1 dashboard click," "Dropped 3D chunk weight
   from 883KB to 24.9KB") are strong, specific, and clearly already written by a human who
   understands the projects — preserve that voice for any new cards, don't flatten it into generic
   repo-description boilerplate.

---

## PHASE 7 — THE MISSING SYSTEMS (build these; they were speced and never shipped)

### 7a. Visitor counter
```html
<img src="https://komarev.com/ghpvc/?username=Shivala-08&label=Profile%20Views&color=00E5FF&style=for-the-badge" alt="Profile views" />
```
Place directly under the banner — first thing after the header, not buried in the footer.

### 7b. Coding quote
```html
<img src="https://quotes-github-readme.vercel.app/api?type=horizontal&theme=dark&color=05060A&titleColor=00E5FF&textColor=8892A6" alt="coding quote" />
```
Confirm the service's custom-colour params actually take the palette above; if it only offers
fixed presets, pick the closest dark/cyan preset rather than forcing a mismatched default into an
otherwise fully-themed page.

### 7c. Random dev joke
Same two-option tradeoff as before — flag it, don't pick silently:
- **Static badge service** — zero maintenance, refreshes on the service's own cache cycle.
- **Scheduled GitHub Action** (same pattern as the snake workflow) that rewrites a README block
  on a cron — more control, more surface area to go stale silently if the Action stops running.

Given this profile already runs a Game-of-Life generation script and a snake workflow, one more
scheduled Action isn't a stretch operationally — but it's still the user's call, not a default.

---

## FINAL ASSEMBLY ORDER

1. Banner (Phase 2)
2. Identity (Phase 3)
3. Visitor counter (Phase 7a)
4. Tech Stack (already in the banner panel per Phase 2.4 — no separate section needed unless the
   user wants the full uncompressed lists spelled out below the banner too; ask rather than
   duplicate)
5. GitHub Activity: streak / stats / radar / 3D graph (Phase 4)
6. Contribution snake (unchanged — recolour to match Phase 1 if not already cyan/gold)
7. Game of Life panel (Phase 5)
8. Coding quote (Phase 7b)
9. Random dev joke (Phase 7c)
10. Other Builds grid (Phase 6)
11. Contact footer (Phase 3.2)

---

## WORKING RULES FOR THE AGENT

- **This is a retrofit, not a rebuild.** Every panel in the diagnostic table already works.
  Recolour and fill gaps; don't regenerate charts, art, or copy that's already good just because
  it'd be satisfying to rewrite from scratch.
- **One palette, everywhere, no exceptions.** If a new panel or badge doesn't have a
  colour-customization option that fits Phase 1, say so before shipping a mismatched default —
  a profile with five accent colours reads as five tutorials, not one build.
- **Don't fabricate voice.** The bio, the project taglines, the "open to internships" line are
  the user's own words and observations. Preserve them. This manual's Stark framing is for the
  *build log*, not licence to rewrite the user's actual README copy into billionaire-engineer
  cosplay.
- **Confirm the project shortlist before touching Phase 6.** Old spec and live reality disagree;
  don't silently resolve that either direction.
- **Verify the `<picture>` dark/light swap is real** before calling Phase 2 done — this is the
  one item flagged as a possible existing bug, not just a style pass.
- If something doesn't work or costs more than it's worth: say so. A billionaire genius still
  runs the numbers before greenlighting a build.

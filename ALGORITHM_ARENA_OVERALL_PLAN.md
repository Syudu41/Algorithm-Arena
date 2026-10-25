# Algorithm Arena — Overall Product & AI-Assisted Development Plan

**Version:** 3.0 | **Date:** October 25, 2026  
**Single source of truth for the whole project.** For the exact current instructions to a coding agent, use `ALGORITHM_ARENA_CURRENT_TASK.md`. These replace older README/Codex briefs. Keep old briefs for historical context only.

## 1. Why the project exists

**Product:** Algorithm Arena — a visually rigorous sorting-algorithm learning website whose explanatory and user-input animations are rendered by genuine Manim. The interaction is educational; the application **does not itself need AI**.

**Lecture:** MIS 7623 AI Assisted Application Development guest lecture, Thursday **October 29, 2026 at 5:30 PM**, assumed 60 minutes with a shorter 30-minute option. Midterm same day ~2:40–4:00 PM. Complete demo, slides, evidence, and backups by **Monday October 26** so Tuesday/Wednesday remain for exam study.

**Teaching message:** AI coding agents can accelerate implementation, but human engineers still own requirements, visual/product judgment, tests, security, debugging, release and communication. Illustrate with actual work, not staged or invented claims.

**Visual-first slides:** 3Blue1Brown-influenced explanatory diagrams, very little on-slide text. Opening is our own line, e.g. “What if we could see how an algorithm thinks?” Attribute any real direct quotations only after verifying the exact source. Include a **single one-slide end-to-end AI-assisted software development workflow**. Capture screenshots/clips and agent prompts as evidence for slides.

## 2. Scope matrix and decisions

| Capability | Scope | Status/notes |
|---|---|---|
| About page | **Now** | Purpose and development story |
| Sorting page | **Now** | Bubble Sort entry |
| Bubble Sort detail | **Now** | Human-reviewed algorithm explainer and custom input |
| Pre-rendered Manim explanation | **Now** | Must pass 3Blue1Brown-referenced visual contract |
| Custom-input Manim animation | **Now**, local backend | One actual new/cached Manim output per normalized input |
| Computer Modern Roman typography | **Now** | Verified font/TeX, no default fallback |
| Explicit pace and player controls | **Now** | MP4 duration ≠ render wall time; speed selectable |
| GitHub Pages site | **Now** | Static public pages/video; test deployed URLs if possible |
| Public custom rendering | **Later** | Needs separate hosted HTTPS backend and risk controls |
| Race workflow | **After Explore** | Two algorithms on same input, Manim rendered, synced player/UI |
| Additional algorithms | **After Explore** | Insertion Sort next, perhaps Merge Sort thereafter |
| Break & Fix | **Lecture workflow** | Reproduce a real bug or explicitly labeled educational fault, verify correction |
| Challenge | **Removed** | Do not build |
| Standalone showcase page | **Removed** | Manim is integrated throughout Learn/Explore/Race |
| AI explanations / chatbot | **Excluded** | Agent assists development, not a runtime feature |
| User accounts, DB, generic code execution | **Excluded** | Over-scoped and risky |

## 3. Unchangeable product requirements

1. **Genuine Manim-produced visuals** for both explanatory samples and user-specific outputs. Browser animation is fine only for UI transitions/player controls, not a replacement.
2. **3Blue1Brown-referenced explanatory animation quality is a release requirement**, not an optional moodboard. Meaningful shape transforms, physical swaps, accurate compare/swap focus, continuous object identity, consistent dark canvas/palette, readable CMR, uncluttered scenes, obvious completed state, rational pacing. Reject generic colored-bar gifs or unrelated effects. Original designs; no copied channel branding/media.
3. **Same visual language across all workflows** (Explore now, Race later); reuse Manim scene abstractions and consistent trace events.
4. **Font:** CMU Serif/Computer Modern Roman through verified font renderer or LaTeX (test actual installed fonts and outputs). Check labels and numbers at 720p.
5. **Timing baseline:** instructional MP4 35–60s; typical custom five-item MP4 12–30s; compare 0.20–0.40s, swap 0.35–0.60s, holds ~0.1–1.5s as appropriate; target 720p/30 fps. Measure actual MP4 durations, wall render times, and file sizes separately. No guarantee of instantaneous on-demand renders.
6. **Honest hosting:** GitHub Pages serves static site/assets; Python renderer is separate. Without deployed HTTPS API, public site is explanatory only, local demo can render custom input. Never advertise unsupported functionality.
7. **Non-destructive iteration:** inspect current code, preserve working renderer and tests, establish backup/branch, run regression tests after each change. Do not choose frameworks/extensions solely for novelty.

### Which Manim edition?

**Important technical distinction:** The original 3Blue1Brown engine is **3b1b/manim (ManimGL)**. **Manim Community Edition (ManimCE)** is a separate fork and is not his exact engine. Existing project code reportedly has working Manim renders but its edition/version have **not been inspected here**. Do not silently promise exact 3Blue1Brown engine parity. First inventory the installed edition and check the actual visual output. Prioritize preserving functional existing code. If the user requires strict *engine* identity, migration to ManimGL becomes a separate measured decision requiring a proof-of-concept and approval. If the requirement means *visual/explanatory standard*, ManimCE may satisfy it provided all scenes pass the visual contract. Agent reports this clearly before a migration.

## 4. User journeys

### Explore / Learn (immediate)
1. Open `/sorting/bubble-sort` from site navigation.
2. Read brief adjacent-comparison/swap explanation; click **Explain**.
3. Play immediately available original Manim teaching video, with playback controls.
4. Enter a bounded comma-separated array (2–10 signed integers, -99..99); click **Animate my array**.
5. Show actual render status rather than freeze UI. Video begins with exact input, displays meaningful comparisons/swaps, ends sorted, metrics shown consistently; handle invalid input and backend-down state.

### Race (next workflow; **not to implement yet**)
1. Select two available algorithms; choose one common array.
2. Produce two genuine Manim outputs under the shared visual grammar.
3. Show side-by-side playback; synced start/seek/speed where technically supported, graceful partial readiness.
4. Compare comparisons and writes/swaps using precisely defined metrics, not Manim render time or video length as algorithm-performance benchmarks.
5. Same input validation, security controls, render caching, and video rendering abstraction; do not duplicate the sorting logic in the scenes.

### Break & Fix (lecture narrative, not mandatory tab)
Show the site/algorithm working; introduce or reproduce a genuine edge case; demonstrate agent-assisted test/diagnosis; show reviewed fix, passing tests and a security boundary. If no authentic defect arose, explicitly label a seeded educational faulty version as such. Keep baseline and fixed versions reproducible.

## 5. Architecture and hosting

```text
GitHub Pages frontend (existing stack, or Vite/React/TS)
  ├─ About
  ├─ Sorting
  └─ Bubble Sort
       ├─ Static genuine Manim teaching MP4 (always available)
       └─ Custom values → validated render API (local for lecture)
                                  ├─ pure Python sorting/trace engine
                                  ├─ bounded trusted Manim scene worker
                                  ├─ cache, timeout, job states
                                  └─ served browser-playable MP4
```

Site must be responsive and keyboard-accessible; use safe video paths, no secrets in browser, no eval/exec/dynamic arbitrary scenes, and no unbounded rendering. GitHub Pages cannot host the Python service; a separate HTTPS deployment is optional and requires additional risk mitigation. Capture an API-unavailable state that still preserves the static explanation.

## 6. AI-assisted SDLC — required one-slide diagram

**User problem / scope → Requirements and acceptance criteria → Architecture and threat model → Agent-assisted implementation → Automated unit/integration/UI tests → Debug / review / improve → Security review → Build / deploy / verify → Monitor / maintain**.

Place **human review throughout**, and show feedback loops from test/security back to requirements/design/code. Avoid framing it as a perfect one-way sequence. Label actual roles the coding agent fulfilled (planner, coder, test writer, code reviewer) only where evidence exists. Use actual prompts, code diffs, test outputs and screenshots as speaker evidence.

## 7. Release gates and evidence

| Gate | Must be demonstrably true |
|---|---|
| Visual | Tutorial and 2 custom MP4s reviewed for CMR, animations, coherence, correctness, timing; visual contract PASS |
| Correctness | Bubble output matches Python sorted, replayable trace, counted compares/swaps, edge cases covered |
| Security | Validated bounded input, no code execution, safe subprocess/path, resource caps; review evidence |
| Site | Three public page types, accessible controls, working real Manim teaching MP4, production base path |
| Local interaction | Custom array triggers genuine Manim render and plays clip; proper status/errors/backend-down |
| Time | Actual playback duration, cold/warm render wall time, outputs/fps reported |
| Deployment | Static frontend tested on GitHub Pages or clearly pending with reproducible deployment instructions |
| Developer narrative | Save agent prompts, a reviewed diff, reproducible defect/fix (if available), actual test screenshots/logs |

**Do not claim these passed until the coding agent actually runs/checks them.** A polished page without a working custom Manim pipeline is partial completion; a working video with generic bars is a visual-contract failure.

## 8. Timeline and priorities

**Tonight, October 25:** repository audit, confirm renderer edition, initial visual proof, document safe plan; begin Bubble Sort visual component and static pages.

**Monday, October 26:** finish full Explore flow; verify static site + local render; tests and security; capture footage, evidence and visual-first slides, rehearse. Avoid spending the entire day on speculative ManimGL migration or public backend hosting.

**Tuesday–Wednesday, October 27–28:** reserve for midterm study; only essential emergency checks.

**Thursday, October 29:** midterm ~2:40–4:00 PM; lecture 5:30 PM. Run a short smoke test from prepared environment; use backup footage for any live renderer failure.

**Priority when blocked:** genuine Manim visual proof → correct Bubble Sort/local render → site with tutorial → UI polish/automation → public frontend; public custom-render hosting, extra algorithms, Race after release gate.

## 9. Lecture structure — 60 / 30 minutes

| Segment | 60 min | 30 min |
|---|---:|---:|
| Visual hook and why visual explanation | 6 | 3 |
| Complete AI-assisted development workflow | 10 | 5 |
| Requirements, architecture and agent use | 10 | 5 |
| Live Bubble Sort demo and edge case | 12 | 7 |
| Testing, debugging and security evidence | 15 | 7 |
| Lessons, tradeoffs, Q&A | 7 | 3 |

Slides should be mostly imagery, traces, diagrams and screenshots, not walls of text. Since lecture duration is assumed rather than confirmed, this 60-minute plan is provisional. Showcase what was actually accomplished; don't imply deployed runtime features beyond the real environment.

## 10. Agent execution protocol

1. Read **both** documents in this order: overall plan then current task.
2. Audit first, make a non-destructive checkpoint; run baseline.
3. Report conflicts, especially engine distinction and GitHub Pages/backend boundary.
4. Implement smallest testable increment; after each phase report real tests, render metadata, visual review results, remaining gaps.
5. Never regenerate the whole repo without a documented need. Never mark a requirement passed because code *looks* correct.
6. Keep `docs/implementation_evidence.md` or similar as a living log for PowerPoint prep, noting actual agent assistance and human decisions.

## Sources checked

- [Original ManimGL used by 3Blue1Brown](https://github.com/3b1b/manim)
- [Grant Sanderson on his Manim usage and Community Edition](https://www.3blue1brown.com/about/)
- [ManimCE / ManimGL version differences](https://docs.manim.community/en/stable/faq/installation.html)
- [Manim text and font verification](https://docs.manim.community/en/stable/guides/using_text.html)
- [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)

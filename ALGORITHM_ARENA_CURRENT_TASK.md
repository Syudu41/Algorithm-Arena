# Algorithm Arena — Current Task for Any Coding Agent

**Version:** 3.0 | **Date:** 2026-10-25 | **Due:** Monday, 2026-10-26 | **Scope:** Workflow 1 — Explore, Bubble Sort only  
**Relationship:** This file contains the *immediate execution instructions*. Read `ALGORITHM_ARENA_OVERALL_PLAN.md` for product rules, non-goals, and release milestones. These two files supersede all previous Codex briefs and READMEs.  
**Important:** This is an instruction to **audit and extend existing work**, not to erase it. Do not use the agent to build a completely different product.

## 0. Objective and hard acceptance rule

Deliver a functional GitHub Pages-compatible **About → Sorting → Bubble Sort** site with (1) a genuine Manim-produced, polished, pre-generated Bubble Sort explanation and (2) a custom-array form that triggers actual input-specific Manim rendering through a separate Python service for the **local demo**. Preserve previously completed sorting/rendering code if sound.

**Non-negotiable aesthetic:** Both sample/explainer videos and custom-input videos must use the **same coherent 3Blue1Brown-referenced visual grammar**. A generic animated bar-chart is **not** acceptable. Use original scene composition and art; do not reproduce 3Blue1Brown logos, narration, video frames, or licensed media as if they were ours. Reference their *explanatory animation language* (visual reasoning, meaningful transformations), not unverified claims of pixel-identical replication. See Visual Contract below. If there is a technical conflict or a compelling need to depart from this standard, stop and report it explicitly rather than silently falling back.

**Manim edition caveat:** Grant Sanderson's current channel uses the **original 3b1b/manim (ManimGL)**; the Community Edition is a separate fork. Existing code may already use ManimCE. First identify which renderer the repo uses. **Do not perform a destructive CE → GL migration without a small prototype, compatibility report, and confirmation**. ManimCE is acceptable only if the resulting footage passes the exact visual contract and the edition choice is documented; if user intended *the same engine* as 3Blue1Brown, flag this unresolved edition choice for explicit approval. Do not falsely claim ManimCE is the exact version he uses.

## 1. First action: repository inspection — no writing yet

1. Inventory repo structure, branch, `git status`, Python/Manim edition and version, existing videos/scenes, source modules, frontend/backend, tests, deployment configuration, fonts and graphics dependencies.
2. Run existing tests and **one existing render**, recording literal commands, exit codes, render wall time, MP4 duration, frame size, fps, and errors.
3. Preserve working sources and media. Create a branch or safe Git checkpoint; don't delete, rename, or overwrite files with other work in progress.
4. Produce a short **gap table** (`exists / partial / missing / blocked`) against the requirements below, and list the smallest safe change set.
5. If anything already works, wire it in before rewriting it. Refactor only to resolve demonstrated needs.

## 2. Required website pages (no scope drift)

Use existing frontend stack; if none, Vite + React + TypeScript is appropriate. Static output must work on GitHub Pages including its `/repo-name/` base path; test links and nested route reloads (hash routing is acceptable).

- `/about`: what Algorithm Arena is, why visual explanations, the AI-assisted development story (without invented accomplishments), link to Sorting.
- `/sorting`: clear introduction and **Bubble Sort** card/link. No false live controls for incomplete algorithms.
- `/sorting/bubble-sort`: simple explanation (adjacent comparisons, conditional swaps, repeated passes, completion), accurate complexity, explanation video, custom comma-separated input, submit button, status/messages, result player, sorting summary.
- Header/navigation: Algorithm Arena, Sorting, About; suitable mobile/keyboard treatment; player with play/pause/replay/scrub/speed. Use user click to initiate video playback rather than unmuted autoplay assumptions.

## 3. Visual contract — strict, for ALL Manim videos

**Reference principle:** The motion must *teach the reasoning*. The algorithm's current decision is always intelligible from what moves/highlights; numerical values are attached to their objects throughout. We are referencing original 3Blue1Brown explanatory aesthetic, not asking for a frame-copy of one video.

### Visual composition
- 16:9 canvas, dark navy/near-black background, limited luminous/contrasting palette, uncluttered geometric array tiles/number tokens, meaningful spacing, camera stable unless motion is pedagogically necessary.
- **Computer Modern Roman (CMR)** everywhere inside Manim visuals: titles, values, comparisons, annotations. Preferred exact family: `CMU Serif` / `Computer Modern Roman` as verified installed; LaTeX `Tex`/`MathTex` with Computer Modern is another verified path. No silently substituted default sans fonts. Perform and log font check (Pango for ManimCE Text, font system for ManimGL, TeX availability). Numeric labels should be legible at projector scale.
- Visual states: current adjacent pair glows/highlights; explain comparison with a brief text/math cue; when condition true, values **exchange physical positions with visible arcs or deliberate motion**; when false, visibly continue without a swap; at the end of a pass, sorted suffix becomes visually distinct. Use outlines/icons/text in addition to color.
- Swap positions rather than replacing entire scene or jump cutting. Use animation transformations, matching continuity and easing; no random celebratory particles, uncontrolled flashes, giant UI chrome, unrelated bar race effects, or cuts that obscure causality.
- Explanation and custom clips share the **same color semantics, typography, positions, swap motion, label placement, and transition logic**. Create reusable Manim components and a trace-to-scene adapter. Only instructional narration/callouts differ.
- Animation shouldn't assert anything that contradicts the actual algorithm trace. Samples must not be static video pretending to be an input-specific render.

### Timing contract (distinguish three different times)
- **Playback duration (MP4):** tutorial target **35–60 seconds**; custom 5-item typical target **12–30 seconds**, dependent on number of comparisons/swaps. These are design ranges, not performance promises. Record actual durations via `ffprobe` or equivalent.
- **Per event initial pacing:** comparison focus **0.20–0.40 s**, swap animation **0.35–0.60 s**, very short intentional rests **0.10–0.25 s**, beginning/ending holds **~0.5–1.5 s**. Tune by watching the render; for repeated comparisons, compress carefully without skipping algorithm semantics.
- **Render wall time (request → playable MP4):** benchmark on demo computer for sample 5-item and worst-case 10-item arrays; record cold/warm measurements and media file size. **No promise of instantaneous generation**. Use loading states while rendering, job timeout (configurable), and cache keyed by normalized array and renderer version.
- **Player speed:** 0.5× / 1× / 1.5× / 2× if supported. Altering player speed **does not shorten render latency**. Keep default 1×, and don't auto-play without user input.
- Baseline output aim: **1280×720, 30 fps**, H.264 MP4, browser playable. Confirm true encoder/container/resolution rather than relying on flag name alone.

### Mandatory quality gate
Create **a written 3Blue1Brown-style review** for the tutorial and **two distinctly different custom arrays**, using actual frame captures or reviewer observations. Check: CMR verified, explanatory pair highlights, continuous swaps, visible sorted suffix, visual consistency, legibility, timing, array fidelity, and correctness. If it looks like a stock web bar visualizer, FAIL and revise. No generic-MP4-is-good-enough criterion.

## 4. Explore functional contract

**Learn:** Explanation MP4 is packaged with static frontend and always playable, even when Python service is not running. Explanatory prose is fixed human-reviewed copy, no LLM API.

**Try your input:** Accept comma-delimited integer arrays of **length 2–10**, elements **-99 to +99** inclusive, negatives/duplicates/zeros permitted, default `5,2,4,1,3`. Reject decimals, empty tokens, strings, long arrays, `NaN`, infinity, code, arithmetic expressions. Validate on both frontend and backend. Show exact submitted array, sorted ascending output, and accurate comparison/swap counts.

Click **Animate my array** → nonblocking state (validating → queued/rendering → ready OR failed/timed out/unavailable) → play new genuine Manim MP4 for those exact values. Make repeat/cancel/replace requests safe from stale video race conditions. Repeated identical requests may use exact-cache hit with a cache label. The local app must stay responsive while rendering. Provide useful but honest failures, never fabricated percentage progress.

**Algorithm:** one deterministic Python Bubble Sort producing immutable/serializable trace events for `compare`, `swap`, `pass_complete`, `complete`; render consumes trace; tests reconstruct end state from trace and confirm counts. Clarify whether best case is O(n) only if early exit is implemented; otherwise O(n²).

## 5. GitHub Pages and Python renderer boundary

GitHub Pages **cannot execute Python or on-demand Manim**. Frontend + tutorial MP4 are public static assets. On-demand custom-array Manim uses a **separate local Python HTTP service** for the lecture. Public remote rendering requires an independent HTTPS-hosted service and safeguards, and is explicitly out of scope for this immediate task. Public frontend must not claim that remote custom rendering works unless it has been verified; do not hardcode `localhost` in public builds.

Existing API routes should be retained if functional. If none exist, recommended:
- `POST /api/renders` JSON `{"algorithm":"bubble", "values":[5,2,4,1,3]}` → job ID/status;
- `GET /api/renders/{id}` → `queued | rendering | ready | failed | timed_out`, plus video URL and metadata when ready;
- GET rendered MP4 from a strictly scoped output route.

Do not pass user strings to shell or Python source/LaTeX. Bind numeric inputs as data through validated JSON / input file. Spawn a **fixed, trusted Manim scene** via argument-vector subprocess, `shell=False`, fixed working directory, bounded input, queue size, concurrent render cap and timeout. For publicly accessible render worker in future, require isolation, rate limits, HTTPS/CORS and resource quotas. Prevent path traversal and stale media overwrite.

## 6. Implementation order for this task

**Phase A — Audit:** repo gap report, existing test/render baseline, safe checkpoint.

**Phase B — Visual proof:** Before major UI work, use **existing Manim engine** to render (a) a 35–60 s tutorial scene and (b) custom `[5,2,4,1,3]` and `[8,3,7,2,6]`, matching the strict visual contract. Verify fonts, smooth swaps, durations, and source-to-output fidelity. Fix reusable scene once, not individually hardcoded videos.

**Phase C — Site:** About, Sorting, Bubble Sort, navigation, beautiful but minimal UI, embedded tutorial MP4, proper GitHub Pages base paths and asset loading.

**Phase D — Custom input:** Connect local rendering service, state management, playable MP4 output, exact array/metrics validation; ensure page still works if service is missing.

**Phase E — Verification and delivery:** tests, visual quality audit, security guardrails, local E2E, static production build, Pages path check, demo instructions, fallback clips and evidence. Publish GitHub Pages only if access/configuration is available; otherwise provide exact deployment instructions, do not claim it is live.

**Stop conditions:** No massive framework rewrite; do not switch to browser-only animation; no fabricated video results; don't migrate between ManimCE/ManimGL without a working pilot and impact analysis; don't spend the whole timeline on font install or rendering optimizations without reporting blockers.

## 7. Tests and evidence the agent MUST return

- Unit tests against Python `sorted()` including duplicates, all-equal, reversed, already sorted, negatives, -99/99, invalid inputs.
- Trace unit tests proving comparisons/swaps refer to valid indices and replay reproduces sorted result and metrics.
- Render integration: MP4 exists, is decodable, metadata FPS/resolution/duration, visually verify the *actual* labels and swap scene for two input arrays. Preserve evidence stills and measured cold/warm time.
- Browser smoke: navigation, mobile, keyboard/video player, tutorial offline/API-down, invalid inputs, custom successful render, failed/timeout state, GitHub Pages asset URLs.
- Security inspection: no `eval`/`exec` of input, no user-provided scene source, subprocess argument safety, server validation, queue/time limits, path handling, no credentials baked in.
- Provide precise change log and evidence in `docs/implementation_evidence.md` (or equivalent) noting **observed vs not yet verified**, exact commands, paths, screenshots/stills (if available), true issues and fixes, and all remaining limitations. Preserve an example Codex/agent dialogue or prompt and its reviewed diff for lecture documentation.

## 8. Required response from coding agent after every phase

1. **What existed**, 2. **what changed**, 3. **what passed with exact commands**, 4. **Manim edition and verified CMR font**, 5. **actual MP4 playback length / render wall time**, 6. **visual contract PASS/FAIL**, 7. **known blockers**, 8. **next incremental action**. Never call an incomplete implementation complete.

### Authoritative references
- Original 3Blue1Brown ManimGL: https://github.com/3b1b/manim
- 3Blue1Brown author description: https://www.3blue1brown.com/about/
- Community Manim version distinctions: https://docs.manim.community/en/stable/faq/installation.html
- ManimCE fonts: https://docs.manim.community/en/stable/guides/using_text.html
- GitHub Pages: https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site

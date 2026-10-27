# Explore implementation evidence — 2026-10-25

Authority: read `ALGORITHM_ARENA_OVERALL_PLAN.md`, then
`ALGORITHM_ARENA_CURRENT_TASK.md`. Workflow 1 / Bubble Sort only. No Race work.
This is an agent's observed evidence, not a claim of human sign-off.

## Phase A — audit and preservation

Existing branch: `feature/explore-bubble`; HEAD `ac1b3c3`. The initial working
tree contained staged renderer/tests/fonts/media and unstaged edits to
`.gitignore` and `renderer/arena/render.py`. No staged work was reset, committed,
or overwritten. There was no frontend, HTTP API, deployment configuration, or
implementation evidence log. README already described some features not yet
implemented. No applicable AGENTS.md was found.

Checkpoint (outside Git, preserving source and media):

- `/tmp/algorithm-arena-pre-explore.tar.gz`
- `/tmp/algorithm-arena-initial-staged.patch`
- `/tmp/algorithm-arena-initial-unstaged.patch`

Inventory commands: `git status --short --branch`, `git log -3 --oneline`,
`rg --files`, `find .. -name AGENTS.md -print`, `git remote -v`, source/test reads,
`.venv-manim/bin/python -m pip show manim manimgl pytest fastapi uvicorn`.
Manim **Community Edition 0.19.1**, Python 3.11; no ManimGL, FastAPI or Uvicorn.
FFmpeg/ffprobe/fontconfig tools reside in `.venv-manim/bin`, outside initial PATH.
TeX is available through `~/.TinyTeX/bin/x86_64-linux`.

Initial invocation `.venv-manim/bin/python -m pytest renderer/tests -q`:
109 passed, 1 skipped, 1 failed (35.06s). The render test skipped without ffprobe.
I mistakenly launched a second suite concurrently; Manim's shared text directory
creation raced. This was a verification mistake, not an application defect.
With `PATH="$PWD/.venv-manim/bin:$PATH"` and a single suite:
**111 passed**, exit 0, 34.34s, including real rendering and every-frame decode.
Subsequent tests were run without another suite sharing the text directory.

Baseline MP4s (all H.264, yuv420p, 1280×720, 30/1 fps):

| Existing clip | Playback | Bytes |
|---|---:|---:|
| media/bubble-tutorial.mp4 | 37.566667s | 2,326,737 |
| media/c52413.mp4 | 19.466667s | 966,187 |
| media/c83726.mp4 | 19.466667s | 980,219 |

Gap table at audit:

| Requirement | Audit status | Smallest change |
|---|---|---|
| Python sorting, immutable replay trace, validation | exists | preserve |
| Genuine tutorial/custom scenes, shared stage | exists | review actual output |
| CMU/TeX font path | partial | verify Pango and font files |
| Visual/timing evidence | partial | fresh renders, probes, frame reviews |
| About → Sorting → Bubble Sort | missing | static hash-routed pages |
| Local async render API/cache/status | missing | wrap fixed existing worker |
| Pages release | missing | deploy static output only |
| Browser/security evidence | missing | integration and browser checks |

## Phase B — visual proof and narrow repairs

`PATH="$PWD/.venv-manim/bin:$PATH" .venv-manim/bin/python scripts/verify_renders.py`
first failed after rendering: `OSError: [Errno 18] Invalid cross-device link`.
The existing worker used `Path.replace()` from `/tmp` to repository output.
Fixed by `shutil.copyfile(produced, destination_part)` then atomic destination
rename. No scene rewrite. The rerun rendered all six videos successfully and
fully decoded them with `ffmpeg -v error -i VIDEO -f null -`, exit 0.

A real visual issue was observed in `review-tutorial.png`: simultaneous caption
dissolves overlaid sentences and held an obsolete decision cue. Changed only
caption transitions: fade out then fade in; clear stale cue except the first
swap's explanatory decision. Re-rendered tutorial, retaining the original MP4.
New release asset: `media/bubble-tutorial-v3.mp4`; public build packages that as
`media/bubble-tutorial.mp4`. A real video still supplies the public poster.

Font commands:

```
.venv-manim/bin/fc-scan --format '%{family}: %{style}\n' renderer/fonts/cmunrm.ttf renderer/fonts/cmunti.ttf renderer/fonts/cmunbx.ttf
```

Observed CMU Serif: Roman / Italic / Bold. A Python `register_font()` probe
confirmed `'CMU Serif' in manimpango.list_fonts()` is True. `ensure_tex()` checks
both latex and dvisvgm; genuine MathTex rendered successfully. Existing tests
reject glyphs missing from CMU and reject non-integers before TeX interpolation.
No sans-serif fallback was introduced. **CE is not Grant Sanderson's ManimGL**;
no engine migration was made.

Measurements: output of `ffprobe -v error -show_entries
stream=codec_name,width,height,r_frame_rate,pix_fmt:format=duration,size -of json VIDEO`.
Full data: [render-measurements.json](evidence/render-measurements.json).

| Render | Playback | Scene render | Process wall | Bytes |
|---|---:|---:|---:|---:|
| [5,2,4,1,3], first measured | 19.466667s | 17.53s | 18.82s | 966,187 |
| [8,3,7,2,6], first measured | 19.466667s | 17.07s | 18.18s | 980,219 |
| Tutorial before caption repair | 37.566667s | 42.74s | 43.90s | 2,326,737 |
| reversed 10, first measured | 52.400000s | 84.22s | 85.46s | 4,488,779 |
| reversed 10, repeat | 52.400000s | 63.43s | 64.74s | 4,488,779 |
| [5,2,4,1,3], repeat | 19.466667s | 18.46s | 19.61s | 966,187 |
| Revised tutorial | 37.566667s | 40.31s | not separately measured | 2,331,029 |

The first/repeated runs use the **existing TeX/text cache**, not a pristine OS or
font-cache cold start. Manim animation caching is disabled. All films were
H.264 / yuv420p / 1280×720 / 30 fps and decoded without error. MP4 duration is
never used as an algorithm performance benchmark. The five-item timings and
tutorial duration meet the brief; ten-item playback intentionally exceeds the
five-item target because all 45 comparisons and swaps are shown.

### Written 3Blue1Brown-referenced visual review

Agent-assessed PASS, with human visual sign-off still pending. Review used actual
frames (not a generic MP4 existence test), mid-swap samples, source-to-trace
inspection, and freshly rendered footage. The aesthetic is original; no channel
media, branding or narration was copied.

| Check | Tutorial (revised) | [5,2,4,1,3] | [8,3,7,2,6] |
|---|---|---|---|
| CMR/Computer Modern and legible 720p values | PASS | PASS | PASS |
| Pair focus and accurate swap/keep cue | PASS | PASS | PASS |
| Continuous tile identity/physical arc swap | PASS | PASS | PASS |
| Sorted suffix uses line, word and check badges | PASS | PASS | PASS |
| Dark, uncluttered stable 16:9 composition | PASS | PASS | PASS |
| Shared palette, type, stage, trace adapter | PASS | PASS | PASS |
| Exact input and sorted output | [4,1,6,2,5,3] → [1,2,3,4,5,6] | → [1,2,3,4,5] | → [2,3,6,7,8] |
| Counts match Python trace | 14 compares / 7 swaps | 10 / 7 | 10 / 7 |
| Target playback duration | 37.57s PASS | 19.47s PASS | 19.47s PASS |

Evidence: `review-custom-52413.png`, `review-custom-83726.png`,
`tutorial-revised-18s.png`, `tutorial-revised-36s.png`, `swap-midpoint.png`.
The initial `review-tutorial.png` records the genuine issue before correction.
The revised montage was recaptured through FFmpeg after the first capture
omitted some sampled frames; individual full-resolution captures above are
also retained. Full videos remain available locally
under `renderer/renders/verification/`. Source review confirms values and boxes
travel in the same VGroup and are exchanged using arcs, rather than replaced.
Secondary index/metric text is deliberately quieter than the values; projector
legibility in the actual lecture room remains untested.

## Phase C — static site

Added buildless HTML/CSS/ES modules (there was no frontend to preserve): About,
Sorting, Bubble Sort, hash navigation, bounded input, native MP4 controls plus
replay and 0.5×/1×/1.5×/2× speed controls. Default is 1×; playback requires a user
click. The tutorial remains independent of Python. CMU webfonts are bundled.
No runtime AI, Race, incomplete algorithm controls or unrelated pages.

`npm run build`, `npm test`, `node --check web/app.js`: exit 0. Node reported one
passing test-file suite; it contains valid boundary and invalid-token assertions.
Assets and route links are relative; hash navigation supports nested reloads
under `/Algorithm-Arena/`. Static config has `renderApi: null`, no localhost URL.
Backend-down text explains the actual public/local boundary.

## Phase D — local rendering

Added `arena.service` using the standard library, retaining the existing worker
CLI. POST/GET jobs plus strictly scoped MP4 route with HTTP byte ranges. One
worker, maximum four active/queued jobs, timeout (default 300s), fixed trusted
scene and argv subprocess, no shell/source execution. Validation accepts only
2–10 actual integers in -99..99, rejecting bool/float/string values. Cache keys
include normalized values, renderer version, source and font fingerprint.
Completed outputs are atomic and reused across restarts.

The UI uses AbortController plus a request generation number; replacement,
route changes and Stop waiting prevent an old result attaching to a new input.
Stop waiting cancels observation, not the server's already queued job; the UI
says so. No invented percentage progress or automatic result autoplay.

Requests are loopback-only and same-origin; POST host/origin checks reject DNS
rebinding/cross-site origins. Body is capped at 2048 bytes. Output identifiers
are fixed hex; path traversal is rejected. Failures expose a short useful error;
worker diagnostics remain local. This is not a hardened public render service.
Disk caches require periodic cleanup; the local demo does not yet enforce a
total disk quota or user authentication. No public render backend is deployed.

## Phase E — verification

Final regression command:

```
PATH="$PWD/.venv-manim/bin:$PATH" .venv-manim/bin/python -m pytest renderer/tests -q
```

With loopback permitted: **121 passed**, exit 0, 23.07s. One dependency warning:
Python audioop is deprecated for Python 3.13; current environment is Python 3.11.
A prior sandboxed run had 120 passed, 1 failed solely because socket creation was
not permitted. Re-run `renderer/tests/test_service.py -q` with local network
permission: **10 passed**, 1.02s. Security tests include server-side invalid input,
wrong algorithm/extra scene keys, queue capacity, pending deduplication, timeout
and semaphore release, cache normalization, origin rejection, traversal rejection,
and exact video byte ranges. Existing tests cover sorted(), 500 seeded random
arrays, edge cases, immutable traces, replay, counts and final suffixes.

`node scripts/browser-smoke.mjs` against the actual local service: exit 0.
The first attempt used JS `.click()` and failed Chrome's user-activation rule;
fixed the test to send real mouse input. No application autoplay workaround.

Browser checks (installed Google Chrome, dependency-free DevTools harness):
About → Sorting → detail; tutorial metadata, user playback, speed; invalid input
focus; genuine exact custom render, correct counts, decode, no result autoplay;
repeat cache label; mobile no horizontal overflow; keyboard reaches submit;
API-down retains tutorial; failed/timed_out UI using explicitly injected HTTP
responses; public static unavailable message; no runtime exceptions.
Saved `browser-results.json`, `browser-mobile.png`, `browser-explore.png`.

Remaining verification limitations: no physical projector, screen-reader session,
Safari/Firefox coverage, human copy sign-off, or clean-machine dependency install.
Cache has no disk quota; render latency varies with machine load and TeX cache.

### Final local API benchmarks

`.venv-manim/bin/python scripts/benchmark_api.py`, exit 0, against the actual
local service. Data: [api-benchmark.json](evidence/api-benchmark.json).

| Array | New input-cache miss, request → ready | Exact cache hit | Playback |
|---|---:|---:|---:|
| [8,3,7,2,6] | 23.4443s | 0.0023s | 19.467s |
| [10,9,8,7,6,5,4,3,2,1] | 81.1146s | 0.0026s | 52.400s |

These are cold/warm **application output-cache** measurements with existing TeX
cache, not cold installation measurements. A hit does not launch Manim. A miss
renders through the fixed genuine scene. Browser default-array render separately
reported 20.16s wall and 19.467s playback. No real-time generation guarantee.

### Deployment — verified

Public URL: https://syudu41.github.io/Algorithm-Arena/#/about

GitHub login `Syudu41` had repository admin/push permissions. Pages initially
returned 404 and remote had only `main`. Prepared `dist/` in the isolated
`/tmp/algorithm-arena-pages-release` Git checkout; committed only static assets
as `8558546424d836891b4cb8d62f96420971f24479` and pushed a new `gh-pages` branch.
The first HTTPS Git push lacked a credential helper; re-ran with the existing
`gh auth git-credential` helper, without printing/storing credentials.
Pushing `gh-pages` enabled Pages automatically; a subsequent create request
returned 409 already enabled. GET confirmed legacy branch source `gh-pages` `/`,
HTTPS enforced, latest build `1314611002` **built**, no error.

All **13 deployed assets** were fetched from the real repository base URL and
matched `dist/` byte-for-byte, including video, poster and fonts. See
[deployment-assets.json](evidence/deployment-assets.json).

```
ARENA_URL=https://syudu41.github.io/Algorithm-Arena ARENA_STATIC_ONLY=1 node scripts/browser-smoke.mjs
```

Exit 0: actual public navigation, tutorial metadata and user-click playback,
speed, honest unavailable custom-render state, nested hash-route reload, and no
runtime exceptions. Evidence: `public-browser-results.json`, `browser-public.png`.
Only static output was published; no renderer, secrets, API or source edits were
pushed. Current source branch/index remained intact. Added local checkpoint
branch `checkpoint/explore-audit-2026-10-25` at audited HEAD; the `/tmp` archive
and patches additionally preserve the original uncommitted working code/media.

### Agent assistance / review record

See [agent_session.md](agent_session.md) for the actual request and decisions.
[renderer-changes.diff](evidence/renderer-changes.diff) compares the renderer
against the pre-session archive, preserving prior unstaged edits accurately.
Self-review checked the fixed worker/path boundary, trace reuse, cache identity,
validation, job limits, and asynchronous UI ownership. No claim that a human has
already signed off on the new code, instructional copy, or visual quality.

Final local browser rerun passed 17 checks, including Stop waiting and input
replacement while a queued HTTP response was injected. These exercise UI request
ownership without pretending a real Manim job failed. Actual rendering success
and worker timeout behavior were independently tested. Final desktop/mobile
captures and browser-results.json were refreshed; no runtime exceptions.
`git diff --check`: exit 0. Source work remains uncommitted for review; the
original Git index was not restaged. Only static release assets were committed
and pushed in the isolated deployment checkout. No Race work was started.

## Source delivery follow-up

The user subsequently requested pushing the changes and supplied the guest
lecture presentation brief. Saved it verbatim as `docs/PRESENTATION_BRIEF.md`
and linked it from README. The lecture focuses on AI-assisted development,
testing, debugging and security, with Algorithm Arena as its concrete evidence.
Source delivery uses `feature/explore-bubble`; the deployed static build remains
on its separate `gh-pages` branch. No application code changed in this follow-up;
the previously recorded verification applies to the same implementation.

## About-page looping GIF — 2026-10-27

User requested a conspicuous, looping GIF reading "Algorithm Arena", inspired by
[Mitko Nikov's Manim Basics in 100 Seconds](https://www.youtube.com/watch?v=rIgOfmcd1iA).
Worked on the user's new, initially clean `feature/intro-gif` branch. Inspected
the reference's title metadata, thumbnail, and preview storyboard. Its circular
serif title and cyan arc informed an original Manim scene; no downloaded media
was included in the site.

Added `renderer/arena/intro.py` and `scripts/render_intro.py`. This is a dedicated
square title GIF, separate from the 16:9 sorting explanation/custom films. It
uses the existing CMU Serif typography and palette. The title remains visible
while an outer cyan arc rotates continuously through a seamless full revolution.
No changes to sorting, renderer API allowlist, or tutorial output.

Reproduce:

```
PATH="$PWD/.venv-manim/bin:$PATH" .venv-manim/bin/python scripts/render_intro.py
```

Actual output: `media/algorithm-arena-intro.gif`, 720×720, 150 frames, 25 fps,
6.00s, 398,419 bytes; GIF loop extension = 0 (infinite). Manim render 3.63s;
render plus GIF palette conversion/still generation 19.11s. Metadata saved in
`docs/evidence/intro-gif-metadata.json`. `algorithm-arena-intro-still.png` is the
pause/reduced-motion fallback. The title uses verified bundled CMU Serif Italic.
FFmpeg decoded the complete GIF with no errors.

The About hero now pairs the original opening copy with the large title GIF.
On mobile the animation appears first, inside the initial viewport. Added a
Pause/Play control and automatic still-image selection for reduced-motion
preferences. Static build copies both GIF and still with relative asset paths,
so the existing GitHub Pages repository base remains supported.

Checks: `npm run build`, `npm test`, `node --check web/app.js`, and
`git diff --check` exited 0. No changes to the sorting implementation required
another sorting-render benchmark. The frontend test runner reported one passing
test file, containing the existing valid/invalid input assertions.

Actual Chrome checks: initial desktop visibility; automatic GIF load; changing
screen pixels; continued animation beyond the first six-second loop; pause to
still; Play resumes GIF; reduced-motion automatically selects still; mobile
visibility/no overflow; navigating away and back restores GIF; no runtime
exceptions. All ten passed. Used screenshot comparisons because canvas drawImage
samples the GIF default frame and is not a valid playback probe.
Evidence: `intro-browser-results.json`, `intro-about-desktop.png`,
`intro-about-mobile.png`. A source-frame comparison also confirmed frames 0 and
25 differ in the arc region. The browser verification harness was temporary at
`/tmp/arena-intro-reference/browser-intro.mjs`; no new test framework installed.

Published the About update to the existing `gh-pages` branch in an isolated
checkout: `1490e7863d1d607a2afb3fa13c990059fbda06d0`. Pages build status is
`built`, with no error. Live GIF, fallback PNG, app.js, and style.css all returned
HTTP 200 and matched the tested files byte-for-byte; see `intro-deployment.json`.
Live page: https://syudu41.github.io/Algorithm-Arena/#/about .
The same ten Chrome checks also passed against the live GitHub Pages URL;
refreshed the recorded screenshots/results from that public run. Only the
About-page GIF/layout and build asset copying changed in the frontend.

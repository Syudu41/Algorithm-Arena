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

### About animation control follow-up — 2026-10-27

At the user's request, removed the Pause/Play button and its styles/listeners.
The GIF continues looping automatically. Reduced-motion preferences still select
the static image, including preference changes while About is open. The GIF
asset itself is unchanged. `node --check web/app.js`, `npm run build`, `npm test`,
and `git diff --check` passed; no animation re-render was necessary.

## Professional presentation cleanup — 2026-10-28

User requested returning to `main`, avoiding unnecessary branches, discussing a
dedicated Manim agent without implementing it, and polishing the website before
further feature work. Main was already selected and clean; fetched/pulled with
`--ff-only`. No agent was created, no branches added, and no new algorithms or
Manim scenes were implemented.

Audit found forced line breaks on mobile, inconsistent spacing/control sizing,
technical copy in primary product flows, a public custom-render submit action
that appeared available despite the static hosting boundary, and a skip link
that could replace the active hash route with `#main`.

Changes:
- Kept the existing dark palette, Computer Modern identity, original looping GIF,
  site routes, video assets, sorting engine and local service.
- Consolidated typography, spacing, active navigation, focus outlines, touch
  targets and footer navigation. Added an original SVG favicon. Reorganized the
  compressed stylesheet and page templates into readable sections.
- Removed forced hero line breaks; balanced headings and adjusted mobile GIF size
  while retaining its prominent, automatic display and reduced-motion fallback.
- Simplified About copy and the sorting card; retained the actual development
  story. Clarified the Bubble Sort title and added accurate complexity/stability
  facts. Detailed counting and trace-storage caveats remain available inline.
- Grouped the custom-input controls into a clear panel with explicit availability.
  Static/public mode labels the local-demo requirement and disables the render
  action before submission. Local mode keeps the working submission workflow.
- Added distinct, text-labeled working/error/ready states and form busy semantics;
  kept stale-request protection. Moved output encoding/render metadata into an
  expandable details section, with a visible new/cache-hit label.
- Fixed skip-link focus without changing the route, reset route cleanup ownership,
  respected reduced-motion when scrolling to a film, and added a useful missing
  page recovery link/title. No animation pause button was reintroduced.

Verification:
- `npm run build`, `npm test`, `node --check web/app.js`, `git diff --check`: exit 0.
  Frontend validator assertions passed (Node reports one passing test-file suite).
- Temporary Chrome harness `/tmp/arena-cleanup-layout.mjs`: **30 checks passed**.
  All three pages at 320/390/768/1440px had no horizontal overflow, one h1, and
  header navigation targets at least 44px high. Additional checks covered skip
  link route/focus, automatic GIF/no pause control, reduced motion, public mode
  availability before submit, missing route recovery, and runtime exceptions.
- Existing Chrome Explore regression via `/tmp/arena-cleanup-flow.mjs`:
  **17 checks passed**, including genuine custom Manim rendering, exact array and
  metrics, decodable film, no result autoplay, playback/speed, invalid input,
  cached repeat, mobile, keyboard, API unavailable, failure/timeout UI, and safe
  stop/replace. Failure and timeout UI responses were explicitly injected; the
  successful custom film was real. No browser runtime exceptions.
- Updated the retained smoke harness to scroll Explain into view before sending
  a real mouse click, so it works across viewport sizes and lesson heading heights.

Custom render observed in this run: [5,2,4,1,3], sorted [1,2,3,4,5], 10
comparisons, 7 swaps; 19.467s playback, 25.70s Manim scene render, 45.27s worker
wall time, 966,187 bytes, H.264 1280×720/30 fps. Existing TeX cache reused.
Tutorial remains 37.566667s and the About GIF remains a 6s infinite loop; neither
was regenerated. This is a presentation cleanup, not a renderer optimization.
The sorting Python suite was not rerun because no Python code changed; the real
browser/API render served as the relevant integration regression.

Evidence: `cleanup-layout-checks.json`, `cleanup-local-browser.json`, desktop/
mobile `cleanup-about-*`, `cleanup-sorting-*`, `cleanup-bubble-*`, and local
custom-result screenshots. Remaining limits: Chrome-only browser verification,
no physical projector/screen-reader session or fresh human review. Public custom
rendering remains outside scope, and the local cache still has no disk quota.

Published static cleanup as existing `gh-pages` commit
`eb527fe89847d49ab45fd4683813498e61792046`; GitHub reports `built`, no error.
The live index, JavaScript, stylesheet, favicon and public configuration returned
HTTP 200 and matched the tested build byte-for-byte (`cleanup-deployment.json`).
Seven additional Chrome checks passed on the actual public site: navigation,
video metadata/no autoplay, user-triggered playback, speed, honest public render
availability, nested hash-route reload, and no runtime exceptions. Evidence:
`cleanup-public-browser.json`, `cleanup-public-bubble.png`. No new source branch
or specialist agent was created; delivery is directly on `main` as requested.

## Public content cleanup — 2026-10-28

User requested cleaner textual content and removal of the Python/local-script
portion from sorting. Explained the distinction between playing saved films on
static hosting and generating new arrays. Chose the non-destructive default:
remove the local-only form and all setup/unavailability copy from public pages,
while retaining the existing local demo when a render API is configured. No
backend, sorting code, media, or Python scripts were deleted.

About now focuses on visual learning and playback controls, removing course,
agent-development and renderer-edition copy from the product pages. Shortened
sorting/lesson descriptions and labels, removed the one-lesson counter, and kept
algorithm counting/space explanations focused on the algorithm instead of the
application's trace storage. The development narrative remains in repository
documentation for the lecture.

Public Bubble Sort now ends with the playable tutorial, visual key and algorithm
explanation. The custom form/result section is rendered only when renderApi is
configured. Explanation playback is bound independently of that form. Static
Chrome testing caught the initially shared Explain/form setup; separated the
handlers and reran both modes successfully before deployment.

`npm run build`, `npm test`, `node --check web/app.js`, `git diff --check`: exit 0.
Updated the existing browser smoke assertions to check absence of local form/
setup copy in static mode. Seven static browser checks and seventeen local
Explore regression checks passed after correction. The local test uses the
existing cached genuine MP4; no Manim media was regenerated. Tutorial playback
remains 37.566667s; cached five-item output remains 19.467s. Source render timings
from the prior phase remain historical, not new render-time measurements.

Evidence: `copy-public-browser.json`, `copy-public-bubble.png`,
`copy-local-browser.json`, `copy-local-result.png`, `copy-local-result-mobile.png`.
No agent or new source branch was created. Source delivery remains on main.

Published as `gh-pages` commit `b9cf1df9f5e6433aa784c0703bec4c3b04125643`;
Pages reports built, no error. Live app.js/style.css match the tested build
byte-for-byte (`copy-deployment.json`). Eight public-site Chrome checks passed,
including learning-focused About copy, no local/Python setup/form content,
working Explain/playback speed, and nested reload. Updated public results and
screenshot were captured from the actual deployed URL.

## Typography feature — 2026-10-28

User requested CMR headings and Arial/Inter running text, with a separate commit
for each completed feature. Set body and UI text to Arial with Helvetica /
Liberation Sans fallbacks; explicitly retained bundled CMR for h1/h2/h3 and the
brand title. Manim/GIF text and media are unchanged.

`npm run build`, `npm test`, `node --check web/app.js`, `git diff --check`: exit 0.
Chrome's platform-font inspection confirmed CMU Serif on the heading and
Liberation Sans (Arial-compatible) on running text. All three pages fit at
320/390/768/1440px. Fourteen checks passed; see `typography-checks.json`.

## Reusable Manim agent feature — 2026-10-28

User selected both Codex and terminal invocation, a full animation-package role,
and an Insertion Sort card/detail lesson with local-only custom input. Added
native `.codex/agents/manim-agent.toml`, repository skill
`.agents/skills/manim-agent/SKILL.md`, and AGENTS.md routing/feature-commit rules.
The role inherits model/permissions and owns traces, scenes, media, tests and
visual evidence; website integration/publishing remain with the coordinator.

Added executable `bin/Manim-agent`, backed by `scripts/manim_agent.py`. It accepts
natural algorithm words, optional URL, values/mode/quality/pace/output options.
Normal execution sends a normalized JSON request through stdin to the installed
Codex CLI, using argv and workspace-write, without bypassing approvals. Dry run
is offline. README contains both invocation styles and parameter examples.

Validation: skill-creator quick_validate reported valid; native TOML parsed with
all required fields; **10 offline CLI tests passed** in 0.11s (parsing, invalid
values/paths/URLs, no-call dry run, argv/stdin dispatch and exit-code propagation).
Actual executable `--help` and an Insertion Sort URL/negative-array `--dry-run`
returned 0. Installed `codex exec --help` confirms the launch flags. No real
model request was made through the terminal launcher during these interface
tests; the following Insertion Sort feature will exercise the agent workflow
through the available delegation tool using the same role/skill instructions.
No Insertion Sort implementation is included in the agent-definition commit.

## Insertion Sort feature, generated by Manim agent — 2026-10-28

After separate typography and agent-interface commits, delegated the animation
package to the actual `manim_agent` subagent using the committed role/skill.
Worker authored the insertion trace, scene adapter, trusted scene registration,
proof/benchmark script, tests, media, frame reviews and package manifest. The
coordinator independently reviewed actual frames and implemented website/API
integration. Worker did not commit or deploy.

Added an Insertion Sort card **below Bubble Sort**, a separate static lesson at
`#/sorting/insertion-sort`, and local-only exact custom input. CMR headings and
Arial-compatible running text apply to the new page. Public builds still hide
all local form/setup UI. The new explanation is genuinely rendered by installed
ManimCE0.19.1 using verified shared CMR/TeX helpers and original shared tiles.
The key lifts, larger values shift right, the key fills a dashed gap, and a teal
ordered prefix grows. Only global completion uses green check badges.

Metrics are explicit: comparisons of existing values with key; one shift per
value moved right; one key placement per outer iteration (n−1), including a
return to the same position. [5,2,4,1,3] produces [1,2,3,4,5] with9 comparisons,
7 shifts,4 placements. The API accepts only fixed `bubble`/`insertion` algorithms,
uses the trusted `insertion_custom` scene, and includes algorithm in cache keys.
The browser verifies returned algorithm/input before presenting a result.
No arbitrary scene/code execution, new public API deployment, or Race workflow.

The specialist's first prototype visibly separated value labels from boxes due
to overlapping parent/child transforms. Parent review flagged the risk; actual
prototype frames confirmed it. Fixed by styling the box before moving the whole
key tile. Labeled prototype FAIL evidence is retained; only corrected release
media enters the public build. Parent/worker reviewed comparison, key lift,
mid-shift, no-shift case, prefix and completion frames from two custom arrays
and the tutorial. Agent-assessed visual contract PASS; human/projector sign-off
remains pending. Full analysis is in `docs/evidence/insertion/visual-review.md`.

| Actual render | Playback | Process wall | Bytes |
|---|---:|---:|---:|
| Tutorial | 41.166667s | 72.03s | 2,431,091 |
| Custom [5,2,4,1,3] | 20.900s | 24.67s | 1,164,093 |
| Custom [8,3,7,2,6] | 20.900s | 30.73s | 1,182,036 |
| Five-item repeated render | 20.900s | 33.02s | 1,164,093 |
| Reversed ten, first render | 60.800s | 132.60s | 5,318,166 |
| Reversed ten, repeated render | 60.800s | 114.34s | 5,318,166 |

All six MP4s fully decoded, H264/yuv420p1280×720/30fps. Existing TeX/text cache
was reused; these are not clean-machine cold-start measurements or cache-hit
latencies. No local browser renders ran during these six scene benchmarks.
Source/script/commands/event timelines and outputs are recorded in
`package.json`, `measurements.json`, and per-output JSON files under the
Insertion evidence directory. Tutorial/default-five timing targets passed;
ten-item playback is longer because all45 comparisons/shifts remain visible.

Verification:
- Specialist full suite (after all scene benchmarks):
  `PATH="$PWD/.venv-manim/bin:$PATH" .venv-manim/bin/python -m pytest renderer/tests -q`
  with loopback permission: **163 passed**,30.48s,exit0; one existing audioop
  deprecation warning. Includes genuine Bubble render/decode and both traces,
  service, security, and CLI tests. No simultaneous duplicate suites were run.
- Parent targeted API/CLI checks:22 passed,6.09s. Checks include independent
  same-array cache IDs per algorithm and fixed trusted Insertion worker routing.
- `npm run build`, `npm test`, `node --check web/app.js`,
  `node --check scripts/insertion-smoke.mjs`, `git diff --check`: exit0.
- Retained `scripts/insertion-smoke.mjs`: **23 static checks** and **27 local
  checks** passed: catalog order, real playback/no autoplay, actual platform
  fonts, 320/390/768/1440px layouts across all four pages, route reloads,
  invalid values, exact custom result9/7/4, no false swaps, and cache hit.
- The real local API film was20.90s,1,164,093bytes; scene33.08s/worker34.88s and
  measured request→ready35.312s. Renderer-source fingerprint matched the current
  browser job. The repeat used the exact algorithm-specific output cache.
- Existing Bubble browser regression:17 checks passed after integration,
  including a genuine custom render, counts10/7, playback/cache, invalid input,
  API unavailable, injected failed/timeout states, and stop/replace protection.
- An initial new browser harness navigated before the page was ready and timed
  out; corrected its startup wait before recording the passing checks.

No human/projector review, non-Chrome coverage, or public custom-render hosting
is claimed. Terminal Manim-agent launch remains validated offline/protocol-level;
this feature proves the reusable specialist via real Codex delegation. Evidence
screenshots distinguish static and local mode. Original Bubble media remains
unchanged. Source feature commit is intentionally separate from font/agent work.

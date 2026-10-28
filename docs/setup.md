# Explore local demo

The retained Manim Community Edition 0.19.1 renderer needs Python 3.11, Cairo/Pango,
FFmpeg/ffprobe and TeX (`latex`, `dvisvgm`). CMU fonts are bundled and registered by
the renderer; math uses Computer Modern through TeX. `ARENA_TEX_BIN` can point to
the TeX binary directory. The worker fails explicitly if TeX is absent.

On this machine the existing `.venv-manim` already contains the dependencies:

```sh
export PATH="$PWD/.venv-manim/bin:$PATH"
npm run build
PYTHONPATH=renderer .venv-manim/bin/python -m arena.service
```

Open http://127.0.0.1:8765/#/about → Sorting → Bubble Sort, Insertion Sort or Merge Sort. Click Explain, then
submit `5,2,4,1,3`. Wait for Ready and press Play. Repeat for an exact cache hit.
`--port 8766 --timeout 300` configures the local server. Keep this service local;
it is intentionally bound to loopback, uses same-origin POST requests, and is
not a public rendering deployment.

The static `dist/` build contains `renderApi: null`; the local server provides
its own same-origin configuration. Thus the public site never silently requests
localhost. Static hash links work under `/Algorithm-Arena/` and reload safely.
The build is plain HTML/CSS/ES modules with no framework dependencies.

## Checks

```sh
export PATH="$PWD/.venv-manim/bin:$PATH"
.venv-manim/bin/python -m pytest renderer/tests -q
npm test
npm run build
node scripts/browser-smoke.mjs
node scripts/insertion-smoke.mjs
node scripts/merge-smoke.mjs
.venv-manim/bin/python scripts/verify_renders.py
.venv-manim/bin/python scripts/render_insertion.py --benchmarks
```

The browser smoke script needs installed Google Chrome and local socket access;
it talks to the real service at port 8765. It also injects HTTP failures to check
UI errors; these are explicitly labeled in its results. Rendering verification
writes fresh MP4s and logs to ignored `artifacts/renders/bubble/` and never
replaces the retained baseline media. It reuses the TeX cache and is not a clean
machine installation benchmark.

## Media policy

The public repository tracks only the lesson tutorials and posters, plus
the About GIF and its still fallback. Logo and favicon SVGs live in `web/`.
Custom inputs render on demand through the local service; pre-rendered custom
examples are not website dependencies. Keep optional lecture backups, failed
prototypes, screenshots, logs and raw measurements in ignored `artifacts/`.
The local archive from cleanup is `artifacts/private-archive/`; it is not
required to build or run the application.

## GitHub Pages

Publish only `dist/` on the `gh-pages` branch, with Pages source `gh-pages` `/`.
Build with `node scripts/build.mjs`, copy `dist/.` into a separate checkout of
that branch, commit and push normally (never force push). Review the source changes before release. Pages
contains only static assets: public on-demand rendering is not implemented.

See [GitHub's Pages API documentation](https://docs.github.com/en/rest/pages/pages)
for the branch publishing configuration. Deployment status and actual URL checks
are recorded in [evidence](evidence.md).


## Insertion Sort

Insertion Sort appears immediately below Bubble Sort in the catalog and at
`#/sorting/insertion-sort`. Public pages play the bundled explanation without
local-only controls; the local server enables its custom-array form. For
[5,2,4,1,3], Insertion reports 9 comparisons, 7 shifts and 4 key placements. Bubble
reports 10 comparisons and 7 swaps. These operations are defined in each lesson;
a shift or key placement is not reported as a swap. The cache includes the
algorithm as well as normalized values and renderer fingerprint.

To check a static build/site with the retained Insertion browser harness:

```sh
ARENA_URL=https://syudu41.github.io/Algorithm-Arena ARENA_STATIC_ONLY=1 node scripts/insertion-smoke.mjs
node scripts/merge-smoke.mjs
```

The reusable `Manim-agent` developer command and its optional parameters are
explained in [agent](agent.md). This is a development helper, not an AI service in the site.

Fresh browser captures go to `artifacts/browser/{bubble,insertion}/`. Render
verification and benchmarks use `artifacts/renders/` and `artifacts/benchmarks/`.
These generated outputs are ignored. Release-generation scripts intentionally
update their tutorial/poster assets; custom proofs stay under `artifacts/`.
Review release changes before committing.

## Merge Sort

Merge Sort appears below Insertion Sort at `#/sorting/merge-sort`. The public
lesson includes a genuine Manim explanation; the local service enables exact
custom arrays. For [5,2,4,1,3], this stable top-down implementation reports
8 comparisons and 12 writes. A write means placement into a merged output run,
including remaining values when one input run empties; copy-back bookkeeping is
excluded. Equal front values are taken from the left run first.

```sh
ARENA_URL=https://syudu41.github.io/Algorithm-Arena ARENA_STATIC_ONLY=1 node scripts/merge-smoke.mjs
```

Custom proof videos, screenshots and full measurements stay in ignored
`artifacts/`. Only the required Merge tutorial and poster are tracked.

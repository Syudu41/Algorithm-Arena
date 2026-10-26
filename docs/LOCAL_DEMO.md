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

Open http://127.0.0.1:8765/#/about → Sorting → Bubble Sort. Click Explain, then
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
.venv-manim/bin/python scripts/verify_renders.py
```

The browser smoke script needs installed Google Chrome and local socket access;
it talks to the real service at port 8765. It also injects HTTP failures to check
UI errors; these are explicitly labeled in its results. Rendering verification
writes fresh MP4s and logs to ignored `renderer/renders/verification/` and never
replaces the retained baseline media. It reuses the TeX cache and is not a clean
machine installation benchmark.

## Backup and reproducible real defect

The original three MP4s remain in `media/`; `bubble-tutorial-v3.mp4` contains the
caption improvement and is packaged as the public explanation. `c52413.mp4` and
`c83726.mp4` are offline custom-example backups. Keep them for the lecture if the
live renderer fails. The public tutorial works independently of the Python API.

A real defect found during this session: `Path.replace()` tried to move a
finished `/tmp/arena-…/out.mp4` into the repository across filesystem boundaries,
raising `OSError: [Errno 18] Invalid cross-device link`. The correction copies
into a destination-side `.part.mp4` before atomic rename. The baseline test
had both temporary and output files in `/tmp`, so it missed the defect.
The initial source archive and staged/unstaged patches are preserved in `/tmp/`;
see the evidence log for exact paths. Do not present this as a seeded defect.

## GitHub Pages

Publish only `dist/` on the `gh-pages` branch, with Pages source `gh-pages` `/`.
Build with `node scripts/build.mjs`, copy `dist/.` into a separate checkout of
that branch, commit and push normally (never force push). The source working
tree has pre-existing staged work and should be reviewed separately. Pages
contains only static assets: public on-demand rendering is not implemented.

See [GitHub's Pages API documentation](https://docs.github.com/en/rest/pages/pages)
for the branch publishing configuration. Deployment status and actual URL checks
are recorded in `implementation_evidence.md`.

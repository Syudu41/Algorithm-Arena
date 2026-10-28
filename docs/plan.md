# Product plan

Algorithm Arena makes sorting decisions visible through genuine Manim animation.
It is also a case study for AI-assisted development: humans own requirements,
visual judgment, testing, security and release. The application has no runtime AI.
Current user instructions and root [AGENTS.md](../AGENTS.md) govern ongoing work.
The completed Bubble-only execution brief has been retired; its history remains
in Git. Lecture requirements live in [slides](slides.md).

## Current scope

Explore follows About → Sorting → Bubble Sort or Insertion Sort. Each lesson
plays a bundled explanatory video with user-operated playback controls. The local
demo additionally accepts exact custom arrays and renders them through Python.
The public GitHub Pages site hides local-only forms and never calls localhost.
Race, Challenge, chatbots, accounts, databases and public rendering are outside
the current work. Preserve existing algorithms when adding a new one.

## Visual contract

Use genuine Manim for algorithm explanations and custom outputs. The installed
engine is **Manim Community Edition 0.19.1**, distinct from 3b1b/ManimGL. The
3Blue1Brown inspiration concerns explanatory quality, not engine identity or
copied branding. No migration is needed for the working renderer.

- Use a consistent dark canvas, restrained luminous palette and verified CMR
  text inside scenes. Website headings may use CMR; body text and controls use
  Arial, Helvetica or Liberation Sans.
- Show the actual comparison, physical movement and object identity. Bubble
  swaps tiles and fixes a suffix; Insertion holds a key, shifts values and grows
  an ordered prefix that may still move.
- Explain keep decisions as well as changes. Avoid overlapping captions, stale
  highlights, invisible swaps and decorative motion unrelated to the algorithm.
- Release output is H.264 MP4, 1280×720 at 30 fps. Tutorials run 35–60 seconds;
  typical five-item custom videos run 12–30 seconds. Measure playback duration,
  process wall time and scene render time separately.
- Review decoded frames, including a motion midpoint and completed state, for
  correctness, CMR legibility, spacing, pacing and continuous object identity.
  Failed or unreviewed animation is not release-ready.

The original About GIF loops continuously. The header has an original animated
SVG logo with a static reduced-motion alternative and matching favicon.

## Architecture and safety

The static frontend is buildless HTML/CSS/ES modules. The local Python HTTP
service validates requests, computes immutable algorithm events and dispatches
fixed trusted Manim scenes in a bounded worker. Scenes consume traces rather than
implementing a second sorting algorithm. Cache keys include algorithm, values and
renderer fingerprint; ready media is published atomically.

Accept 2–10 comma-separated integers, each −99 through 99. Allow duplicates,
zero and negative values. Reject empty tokens, decimals, expressions and text on
both client and server. Keep data out of executable code, use safe subprocess
arguments, enforce trusted scene allowlists and retain loopback/same-origin
restrictions, timeouts and resource bounds. Do not expose the local service as
a public API without a separate hosting/security design.

Metrics describe actual operations: comparisons and swaps for Bubble;
comparisons, shifts and key placements for Insertion. Video duration and render
wall time are not algorithm-performance benchmarks.

## Delivery and review

Audit existing code before changing it. Work on main unless isolation is needed.
Finish, verify and commit each feature separately. Use the animation specialist
for animation packages; the coordinator reviews and integrates them.

Verify trace correctness for sorted/reversed, duplicates, all equal, negative and
boundary inputs. Preserve Bubble regression coverage after shared changes. Check
real media with ffprobe and full decode, and review tutorial plus two exact custom
inputs for a full animation package. Check browser playback using real user
activation, responsive layouts and keyboard navigation, public/local boundaries,
request errors and caching. Run socket-dependent checks in an environment that
permits sockets; distinguish harness failures from application defects.

Report commands and exit codes, actual test counts, playback durations, render
timings, visual findings and limitations. Distinguish output-cache misses, warm
TeX and exact-cache hits; never claim a clean-machine cold benchmark without one.
Store all generated QA output, custom examples and lecture archives in ignored
`artifacts/`. Track only website-required media; summarize verified results in
`docs/evidence.md` without committing raw captures or trials. Label injected
failures and do not invent human approval.

Publish only the static `dist/` build to `gh-pages`, using a separate checkout and
normal pushes. Check actual deployed routes/assets when publishing. Custom input
remains local until a separate backend deployment is authorized.

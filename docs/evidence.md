# Verification

Algorithm Arena uses Manim Community Edition 0.19.1 with CMR/TeX scene text.
Release videos are silent H.264, 1280×720 at 30 fps, with embedded captions.
Raw frames, trial renders, logs and lecture archives are local development
artifacts, excluded from this public repository.

## Recorded animation measurements

| Required website film | Playback | Scene render | Process wall |
|---|---:|---:|---:|
| Bubble tutorial | 37.566667s | See local measurements | See local measurements |
| Insertion tutorial | 41.166667s | 70.36s | 72.03s |
| About GIF | 6s loop | See local measurements | See local measurements |

These are actual previous render measurements, with warm TeX/text caches.
They are not clean-machine cold-start benchmarks. No release animation was
regenerated for media cleanup; its playback duration and render measurements
remain unchanged. Custom-array films are generated on demand by the local
service, independently of any pre-rendered examples.

## Recorded verification

The completed Explore regression suite passed 163 Python tests, including a
genuine Manim render/decode integration test. Static browser checks passed 23
Insertion checks and 7 Bubble checks with zero runtime exceptions. The prior
local browser runs passed 27 Insertion checks and 17 Bubble checks. These are
recorded runs, not claims of fresh execution on each documentation edit.

Run the commands in [setup](setup.md) to reproduce verification. Fresh outputs
go to ignored `artifacts/`; only website-required assets belong in `media/`.
The public static site does not expose the local custom-input form.

Human/projector review is pending. Render latency varies with load and input;
ten-item films can exceed the typical five-item playback range. There is no
public rendering service or Race implementation.

## Current brand mark

The header uses an original ten-ribbon SVG rosette with a 24-second continuous
rotation and a matching static favicon/reduced-motion alternative. No lettermark
or external font is used. Browser review passed five checks: actual moving
pixels, 320px header fit, static fallback selection, stationary reduced-motion
pixels and the 24-second infinite loop. Responsive lesson regression passed
23 checks across 320, 390, 768 and 1440px with zero runtime exceptions. Node
validation passed (one test), and the production build passed. Actual desktop,
mobile and enlarged-symbol captures were reviewed locally and remain ignored.
This native SVG change required no Manim render; lesson timings are unchanged.

GitHub Pages deployment `e20069e` completed successfully. Both served SVG files
matched the build byte-for-byte (1,493-byte symbol and 1,231-byte favicon). The
five symbol/motion/mobile checks also passed against the actual public website.

## Merge Sort animation package

The dedicated Manim specialist implemented a stable top-down trace with original
identity-carrying split, compare and merged-placement events. The coordinator
reviewed trace tests, source and actual decoded frames. The first midpoint review
found moving values crossing fading comparison text; the cue was moved below the
output tray and affected custom proofs were regenerated. Trial footage and raw
evidence remain ignored local artifacts, with only the tutorial/poster tracked.

Writes count placements into merged output runs, including drained remainders;
copy-back bookkeeping is excluded. Both five-item proofs use 8 comparisons and
12 writes. The six-item tutorial uses 10 comparisons and 16 writes. The ten-item
boundary/duplicate proof uses 25 comparisons and 34 writes.

| Proof | Playback | Scene render | Process wall | Bytes |
|---|---:|---:|---:|---:|
| custom-52413 | 18.233s | 33.60s | 34.81s | 1,283,293 |
| custom-83726 | 18.233s | 47.60s | 48.93s | 1,287,926 |
| tutorial | 48.100s | 82.89s | 84.04s | 2,896,782 |
| stress-ten | 41.233s | 101.56s | 102.80s | 3,542,594 |

All four outputs: H.264/yuv420p, 1280×720 at 30 fps, full FFmpeg decode exit 0.
Actual split, two-run comparison, write midpoint, remainder, stable equal choice
and completed-state frames were reviewed. Ten-wide rows and −99 labels fit.
TeX/text caches were warm; these are process renders, not clean-machine cold-start
or exact output-cache timings. Pure trace regression: **151 passed**, exit 0,
0.35s, including 500 seeded Merge arrays and existing Bubble/Insertion tests.
Local service unit/HTTP guards: **18 passed**, exit 0, 1.16s. The terminal agent
Merge tutorial dry run passed. All six existing release media files retain their
original hashes. Physical-projector and human visual review remain pending.

Full renderer/service/agent regression after animation review: **197 passed**,
exit 0, **37.58s**, including the existing genuine Bubble MP4 render/decode test.
One existing dependency warning (`audioop` deprecation under Python 3.11).

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

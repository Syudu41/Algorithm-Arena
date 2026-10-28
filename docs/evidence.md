# Verification evidence

This index records observed results from the completed Explore implementation.
It is agent review, not human sign-off. Current scope is in [plan](plan.md);
lecture debugging examples are in [story](story.md). Git history retains earlier
chronological logs and superseded captures.

## Animation packages

The installed engine is Manim Community Edition 0.19.1 with verified CMR/TeX.
Release films are H.264, 1280×720, 30 fps and silent with embedded captions.

| Film | Playback | Scene render | Process wall |
|---|---:|---:|---:|
| Insertion tutorial | 41.166667s | 70.36s | 72.03s |
| Insertion custom [5,2,4,1,3] | 20.900s | 23.58s | 24.67s |
| Insertion custom [8,3,7,2,6] | 20.900s | 29.54s | 30.73s |

The corrected Bubble tutorial plays for 37.566667s; Bubble custom examples play
for 19.466667s. See [Bubble measurements](evidence/render-measurements.json) and
[Insertion measurements](evidence/insertion/measurements.json) for measured
runs, including repeat and worst-case inputs. These reuse warm TeX/text caches;
process render times are not clean-machine cold starts or output-cache hits.

[Insertion visual review](evidence/insertion/visual-review.md) documents exact
metrics, reviewed frames, a real failed prototype and its correction. The
[Bubble source diff](evidence/renderer-changes.diff) preserves the authentic
cross-filesystem output and caption fixes. All release films were fully decoded;
actual motion/decision/final frames were reviewed, not just posters.

## Recorded regression and release results

- Full Python renderer/service/agent suite: **163 passed**, exit 0, 30.48s.
  One existing `audioop` deprecation warning under Python 3.11.
- [Insertion static browser checks](evidence/insertion/web-static-checks.json):
  **23 passed**; [local checks](evidence/insertion/web-local-checks.json):
  **27 passed**. Covers catalog order, playback, actual fonts, responsive layouts,
  public/local boundary, validation, metrics and cache behavior.
- [Bubble browser regression](evidence/insertion/bubble-regression.json):
  **17 passed**.
- [Local Insertion request](evidence/insertion/web-local-job.json): real job
  metadata, 20.9s playback and 35.312s request-to-ready time.
- [Insertion release verification](evidence/insertion/deployment-verification.json):
  deployed routes and asset checks.
- [Logo browser checks](evidence/logo-browser-checks.json): **13 passed**;
  [deployed verification](evidence/logo-deployment.json) confirms the SVG assets,
  eight-second header loop, static reduced-motion alternative and intact About GIF.
- [About GIF metadata](evidence/intro-gif-metadata.json): six-second, 720×720,
  continuously looping original title animation.

These are recorded prior runs, not claims that every command was rerun during
documentation cleanup. Setup commands are in [setup](setup.md). Fresh QA captures
belong in ignored `artifacts/`; add only reviewed, useful release proof here.

## Limitations

Public hosting is static: custom rendering remains local. Films have no audio.
Human/projector review is pending. Render latency varies with load and input;
ten-item Insertion films can exceed the five-item duration range. There is no
Race implementation or public rendering service.

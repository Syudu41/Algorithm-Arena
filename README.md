# Algorithm Arena

**What if we could see how an algorithm thinks?**

Algorithm Arena is a sorting-algorithm learning site. Its explanatory and custom-input animations are rendered by real **Manim**, in a clean visual style inspired by 3Blue1Brown. It was built as the live demo for the MIS 7623 guest lecture on *AI-assisted application development*.

> [!NOTE]
> The app itself contains **no AI**. A coding agent helped build it; humans own the requirements, visual judgment, tests, security and release.

## Scope

- **Now — Explore:** About → Sorting → Bubble Sort and Insertion Sort lessons, pre-rendered Manim explanations, and local-demo forms that render exact custom arrays. The public static site hides local-only controls.
- **Later:** Race (two algorithms on the same input) and additional algorithms; neither is part of this update.
- **Excluded:** chatbots and AI explanations, user accounts, databases, arbitrary code execution, Challenge mode.

## Architecture

```text
GitHub Pages (static)            Local Python service (lecture demo)
  About · Sorting · lessons      →  validate input → algorithm trace
  bundled explainer MP4              → fixed trusted Manim scene → cached MP4
```

> [!IMPORTANT]
> GitHub Pages **cannot run Python or Manim**. The public site is explanation-only. Custom rendering works only while the local render service is running.

## Visual contract (summary)

- Dark canvas, a small luminous palette, and **Computer Modern** typography inside Manim; CMR website headings with Arial-compatible running text
- Decisions are highlighted and values move physically: Bubble swaps and fixes a suffix; Insertion holds a key, shifts values, and grows an ordered prefix
- The explainer and custom videos share one scene grammar, driven by the same trace events
- Output is 1280×720 at 30 fps H.264. The explainer runs 35–60 s; a typical 5-item custom render runs 12–30 s

> [!WARNING]
> The renderer is **Manim Community Edition**, not 3b1b/ManimGL, Grant Sanderson's own engine. The aim is his *visual standard*, not engine parity.

## Input rules

- 2–10 comma-separated integers, each from −99 to 99 (default `5,2,4,1,3`)
- Duplicates, zeros and negatives are allowed. Decimals, expressions, text and empty tokens are rejected on both the client and the server.

## Docs

- [`ALGORITHM_ARENA_OVERALL_PLAN.md`](ALGORITHM_ARENA_OVERALL_PLAN.md): product rules, scope and release gates
- [`ALGORITHM_ARENA_CURRENT_TASK.md`](ALGORITHM_ARENA_CURRENT_TASK.md): current execution brief
- [`docs/implementation_evidence.md`](docs/implementation_evidence.md): living log of tests, renders and decisions

## Run Explore locally

```sh
export PATH="$PWD/.venv-manim/bin:$PATH"
npm run build
PYTHONPATH=renderer .venv-manim/bin/python -m arena.service
```

Open http://127.0.0.1:8765/#/about. See [local demo instructions](docs/LOCAL_DEMO.md)
for dependencies, tests, backups and deployment details. The verified public
static site is https://syudu41.github.io/Algorithm-Arena/; custom input renders
through the local service only.

## Lecture purpose

Algorithm Arena is the case study for a lecture about AI-assisted software
engineering: building, testing, debugging, security, and human judgment.
The [presentation brief](docs/PRESENTATION_BRIEF.md) preserves the project’s
motivation and the requirements for the planned slides.

## Manim agent

Use the dedicated development agent for algorithm animation work. It owns the
trace, scenes, correctness tests, tutorial/custom MP4s, review frames and measured
render evidence. The coordinating agent reviews the package and integrates it
into the website. This does not add runtime AI to the application.

In Codex, ask:

```text
Manim-agent insertion sort algo
Manim-agent insertion sort algo https://algs4.cs.princeton.edu/21elementary/
Manim-agent bubble sort --values 5,2,4,1,3 --mode custom --pace slow
```

The native agent definition is [manim-agent.toml](.codex/agents/manim-agent.toml);
the reusable workflow is [SKILL.md](.agents/skills/manim-agent/SKILL.md).
Root `AGENTS.md` routes natural-language requests to the specialist. A newly
added skill/agent may require a fresh Codex session for native discovery; it can
also be loaded explicitly by its file path. The current coordinator can delegate
using the same checked-in instructions without waiting for native discovery.

The terminal entry point uses an installed, authenticated **Codex CLI**:

```sh
export PATH="$PWD/bin:$PATH"
Manim-agent insertion sort algo
Manim-agent insertion sort algo https://algs4.cs.princeton.edu/21elementary/ --values=-3,0,2,2 --mode both
Manim-agent insertion sort --quality preview --mode tutorial --dry-run
```

Or run `./bin/Manim-agent` directly. `--dry-run` prints the normalized request and
launch protocol without contacting an AI service. Normal execution passes the
request through stdin to `codex exec` in the workspace-write sandbox, with the
existing Codex account/model settings; it does not bypass permissions. If Codex
is missing, the command reports that prerequisite instead of pretending to run.

Options: `--reference URL`; `--values` (2–10 integers, -99..99); `--mode`
`both|tutorial|custom`; `--quality` `release|preview`; `--pace` `normal|slow|fast`;
`--output-dir` (inside this repo). Quote multiword algorithm names if desired.
A positional reference URL is also accepted. Release defaults are 720p/30 fps,
CMR scene text, the shared palette, a 35–60s tutorial and exact custom-input films.
Preview footage is labeled and is not automatically published. The agent must
report actual playback durations, render timings, frame reviews and limitations.

Complete each feature, verify it, then make a separate concise commit. Delegated
workers return changes to the coordinator for review/commit; direct terminal
runs commit their completed animation package. Website publishing is separate.

Agent/skill mechanisms follow the official documentation for
[custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents),
[skills](https://learn.chatgpt.com/docs/build-skills), and
[noninteractive Codex](https://learn.chatgpt.com/docs/non-interactive-mode).

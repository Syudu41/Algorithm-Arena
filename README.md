# Algorithm Arena

**What if we could see how an algorithm thinks?**

Algorithm Arena is a sorting-algorithm learning site. Its explanatory and custom-input animations are rendered by real **Manim**, in a clean visual style inspired by 3Blue1Brown. It was built as the live demo for the MIS 7623 guest lecture on *AI-assisted application development*.

> [!NOTE]
> The app itself contains **no AI**. A coding agent helped build it; humans own the requirements, visual judgment, tests, security and release.

## Scope

- **Now — Explore (Bubble Sort):** About → Sorting → Bubble Sort pages, a pre-rendered Manim explainer video, and a custom-array form that renders a new Manim video for your exact values.
- **Next:** Race (two algorithms on the same input), Insertion Sort, maybe Merge Sort.
- **Excluded:** chatbots and AI explanations, user accounts, databases, arbitrary code execution, Challenge mode.

## Architecture

```text
GitHub Pages (static)            Local Python service (lecture demo)
  About · Sorting · Bubble Sort  →  validate input → Bubble Sort trace
  bundled explainer MP4              → fixed trusted Manim scene → cached MP4
```

> [!IMPORTANT]
> GitHub Pages **cannot run Python or Manim**. The public site is explanation-only. Custom rendering works only while the local render service is running.

## Visual contract (summary)

- Dark canvas, a small luminous palette, and **Computer Modern** typography throughout
- The pair being compared is highlighted, swaps are physical arcing moves, and the sorted part of the array is marked as each pass finishes
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

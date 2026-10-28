# Algorithm Arena

**What if we could see how an algorithm thinks?**

A sorting-algorithm learning site with genuine Manim explanations, built as a
case study for a lecture on AI-assisted software development. The application
contains no runtime AI.

[Open the website](https://syudu41.github.io/Algorithm-Arena/).
Explore Bubble Sort, Insertion Sort and Merge Sort, with CMR headings and Arial-compatible
body text. The public static site plays bundled explanations; exact custom-array
rendering is available through the local Python service.

## Local demo

The existing environment uses Manim Community Edition 0.19.1 and Python 3.11.
See [setup](docs/setup.md) for dependencies, verification and publishing.

```sh
export PATH="$PWD/.venv-manim/bin:$PATH"
npm run build
PYTHONPATH=renderer .venv-manim/bin/python -m arena.service
```

Open http://127.0.0.1:8765/#/about.

## Manim agent

In Codex, request `Manim-agent insertion sort algo [optional reference URL]`.
The specialist owns the trace, scenes, tests, videos and measured render evidence;
the coordinator reviews the package and handles website integration.
The terminal entry point uses your installed, authenticated Codex CLI:

```sh
./bin/Manim-agent insertion sort algo --quality preview --mode tutorial --dry-run
```

See [agent](docs/agent.md) for parameters and both invocation styles.

## Repository guide

| Location | Contents |
|---|---|
| `web/` | Static HTML, CSS, JavaScript, logo and favicon |
| `renderer/` | Algorithm traces, Manim scenes, local service and tests |
| `media/` | Release videos, posters and the About GIF |
| `scripts/` | Build, browser checks, render verification and agent CLI |
| [plan](docs/plan.md) | Product scope and visual contract |
| [setup](docs/setup.md) | Local demo, checks and deployment |
| [agent](docs/agent.md) | Animation specialist usage |
| [evidence](docs/evidence.md) | Reviewed verification and render measurements |
| [slides](docs/slides.md) | Guest lecture presentation brief |

`README.md`, `AGENTS.md` and agent `SKILL.md` retain their conventional names for
tool discovery. Generated builds, caches and fresh QA captures are ignored;
raw render evidence and lecture archives stay local under `artifacts/`. Only
media used by the website is tracked.

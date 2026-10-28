# Manim agent


Use the dedicated development agent for algorithm animation work. It owns the
trace, scenes, correctness tests, tutorial/custom MP4s, review frames and measured
render evidence. The coordinating agent reviews the package and integrates it
into the website. This does not add runtime AI to the application.

In Codex, ask:

```text
Manim-agent insertion sort algo
Manim-agent merge sort algo
Manim-agent insertion sort algo https://algs4.cs.princeton.edu/21elementary/
Manim-agent bubble sort --values 5,2,4,1,3 --mode custom --pace slow
```

The native agent definition is [manim-agent.toml](../.codex/agents/manim-agent.toml);
the reusable workflow is [SKILL.md](../.agents/skills/manim-agent/SKILL.md).
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


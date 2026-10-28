# Algorithm Arena working conventions

- Work on main unless isolation is genuinely needed or the user requests a branch.
- Complete and verify one feature, then commit it before beginning the next.
  Use a concise, descriptive subject such as `Use Arial body text and CMR headings`.
  Keep unrelated changes out of the feature commit. Delegated workers return work
  for coordinator review; the coordinator owns the final feature commit.
- Website headings/titles may use bundled CMR. Running text and controls use
  Arial/Helvetica/Liberation Sans. Manim scene text remains verified CMR.
- `Manim-agent <algorithm> [reference]` and algorithm-animation requests use
  .agents/skills/manim-agent/SKILL.md and .codex/agents/manim-agent.toml.
  Delegate the rendering package to that specialist when delegation is available.
  A worker already acting as the specialist performs it directly, without
  recursively delegating. The coordinator handles website integration/release.
- Preserve existing algorithms and the static/public versus local-render boundary.
  New user instructions supersede older scope notes in the planning documents.

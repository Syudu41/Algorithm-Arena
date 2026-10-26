"""Fixed, trusted Manim scenes. User input reaches them only as validated
integers via `configure()`; nothing user-supplied is ever executed."""
from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, FadeTransform, Scene, VGroup, Write

from .bubble import Compare, PassComplete, Swap, bubble_trace
from .validation import validate_values
from .visual import DONE, INK, MUTED, ArrayStage, Pace, cmr, math

_VALUES: list[int] = [5, 2, 4, 1, 3]
TUTORIAL_VALUES = [4, 1, 6, 2, 5, 3]


def configure(values: list[int]) -> None:
    global _VALUES
    _VALUES = validate_values(values)


class BubbleCustom(Scene):
    def construct(self):
        trace = bubble_trace(_VALUES)
        stage = ArrayStage(self, list(trace.initial))
        stage.build()
        stage.play_trace(trace.events)


class BubbleTutorial(Scene):
    """Same stage and trace as custom renders, plus narration captions."""

    def construct(self):
        trace = bubble_trace(TUTORIAL_VALUES)
        n = len(TUTORIAL_VALUES)
        slow = Pace(compare=0.40, verdict=0.30, swap=0.60, keep=0.25, pass_end=0.6)
        stage = ArrayStage(self, list(trace.initial), pace=slow)
        caption = {"mob": None}

        def say(text: str, hold: float = 1.0, clear_decision: bool = True):
            new = cmr(text, 30, INK, "ti").move_to(UP * 2.55)
            old = caption["mob"]
            # Sequential text changes remain readable at every frame. A dissolve
            # superimposed two sentences and held the previous decision cue.
            outgoing = stage._set_cue(None, 0.2) if clear_decision else []
            if old:
                outgoing.append(FadeOut(old))
            if outgoing:
                self.play(*outgoing, run_time=0.2)
            self.play(FadeIn(new, shift=DOWN * 0.1), run_time=0.25 if old else 0.45)
            caption["mob"] = new
            self.wait(hold)

        # Opening: the whole idea in one line, before any motion.
        stage.build()
        say("Compare neighbours.  Swap them if they are out of order.", 1.4)

        seen = set()

        def before(k: int, ev):
            if isinstance(ev, Compare) and "first" not in seen:
                seen.add("first")
                say("One neighbouring pair at a time.", 0.5)
            elif isinstance(ev, Swap) and "swap" not in seen:
                seen.add("swap")
                say("Bigger on the left?  They trade places.", 0.2, clear_decision=False)
            elif isinstance(ev, Compare) and not ev.swap and "keep" not in seen:
                seen.add("keep")
                say("Already in order?  Leave them and move on.", 0.2)
            elif isinstance(ev, PassComplete) and ev.number == 1:
                say(f"The largest value, {max(TUTORIAL_VALUES)}, has bubbled to the end.", 0.2)
            elif isinstance(ev, Compare) and stage.pass_no == 1 and stage.sorted_from < n \
                    and "repeat" not in seen:
                seen.add("repeat")
                stage.pace = Pace()  # first pass taught slowly; later passes at normal pace
                say("Repeat on the unsorted part; each pass fixes one more.", 0.3)
            elif isinstance(ev, PassComplete) and ev.early_exit:
                say("A pass with no swaps means everything is in order.", 0.2)

        stage.play_trace(trace.events, before=before)

        # Closing: cost, stated as counts first, then growth rate.
        self.play(FadeOut(caption["mob"]), run_time=0.3)
        rows = VGroup(
            math(r"\textit{worst case}", r"\quad\frac{n(n-1)}{2}\ \text{comparisons}",
                 r"\;\Rightarrow\;", r"O(n^2)", size=42),
            math(r"\textit{already sorted}", r"\quad n-1\ \text{comparisons, then stop}",
                 r"\;\Rightarrow\;", r"O(n)", size=42),
        ).arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to(DOWN * 2.05)
        for r in rows:
            r[0].set_color(MUTED)
            r[3].set_color(DONE)
        self.play(FadeOut(stage.metrics), FadeOut(stage.rule), run_time=0.4)
        self.play(Write(rows[0]), run_time=1.2)
        self.wait(0.8)
        self.play(Write(rows[1]), run_time=1.2)
        self.wait(2.5)

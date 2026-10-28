"""Fixed trusted Insertion Sort scenes; custom integers are passed as data."""
from manim import DOWN, RIGHT, UP, FadeIn, FadeOut, Scene, VGroup, Write

from .insertion import Compare, PassComplete, SelectKey, Shift, insertion_trace
from .insertion_visual import InsertionPace, InsertionStage
from .validation import validate_values
from .visual import DONE, INK, MUTED, cmr, math

_VALUES=[5,2,4,1,3]
TUTORIAL_VALUES=[4,1,6,2,5,3]


def configure(values):
    global _VALUES
    _VALUES=validate_values(values)


class InsertionCustom(Scene):
    def construct(self):
        trace=insertion_trace(_VALUES)
        self.stage=InsertionStage(self,list(trace.initial))
        self.stage.build()
        self.stage.play_trace(trace.events)


class InsertionTutorial(Scene):
    def construct(self):
        trace=insertion_trace(TUTORIAL_VALUES)
        self.stage=stage=InsertionStage(self,list(trace.initial),pace=InsertionPace(
            compare=.4,verdict=.25,shift=.6,lift=.5,place=.55,prefix=.5))
        caption=None

        def say(text,hold=1.1,clear=True):
            nonlocal caption
            outgoing=stage.cue_anims(None) if clear else []
            if caption is not None:outgoing.append(FadeOut(caption))
            if outgoing:self.play(*outgoing,run_time=.2)
            caption=cmr(text,29,INK,'ti').move_to(UP*2.65)
            self.play(FadeIn(caption),run_time=.25)
            self.wait(hold)

        stage.build()
        say('Grow an ordered prefix, one value at a time.',1.4)
        seen=set()

        def before(index,ev):
            if isinstance(ev,SelectKey) and 'key' not in seen:
                seen.add('key');say('Hold the next value aside: this is the key.',1.0)
            elif isinstance(ev,Shift) and 'shift' not in seen:
                seen.add('shift');say('Larger than the key? Move one place to the right.',.8,clear=False)
            elif isinstance(ev,Compare) and not ev.shift and 'keep' not in seen:
                seen.add('keep');say('Smaller or equal? Stop shifting and place the key.',.8)
            elif isinstance(ev,PassComplete) and 'prefix' not in seen:
                seen.add('prefix');say('This prefix is ordered, but future keys can still move it.',1.0)
            elif isinstance(ev,SelectKey) and ev.index==3:
                say('Repeat: lift a key, make a gap, then insert.',.8)

        stage.play_trace(trace.events,before=before)
        self.play(FadeOut(caption),FadeOut(stage.metrics),run_time=.3)
        rows=VGroup(
            math(r'\textit{worst case}',r'\quad\frac{n(n-1)}{2}\ \text{comparisons and shifts}',r'\;\Rightarrow\;',r'O(n^2)',size=34),
            math(r'\textit{already ordered}',r'\quad n-1\ \text{comparisons, no shifts}',r'\;\Rightarrow\;',r'O(n)',size=34),
        ).arrange(DOWN,buff=.35).move_to(DOWN*1.9)
        for row in rows:row[0].set_color(MUTED);row[3].set_color(DONE)
        self.play(Write(rows[0]),run_time=1.0);self.wait(.7)
        self.play(Write(rows[1]),run_time=1.0);self.wait(2.5)

"""Fixed trusted Merge Sort scenes; user values remain validated data."""
from manim import DOWN, UP, FadeIn, FadeOut, Scene, VGroup, Write as Draw
from .merge import Compare, MergeComplete, MergeStart, Split, Write, merge_trace
from .merge_visual import MergePace, MergeStage
from .validation import validate_values
from .visual import DONE, INK, MUTED, cmr, math

_VALUES=[5,2,4,1,3]
TUTORIAL_VALUES=[4,1,6,2,5,3]


def configure(values):
    global _VALUES
    _VALUES=validate_values(values)


class MergeCustom(Scene):
    def construct(self):
        trace=merge_trace(_VALUES)
        self.stage=MergeStage(self,list(trace.initial))
        self.stage.build();self.stage.play_trace(trace.events)


class MergeTutorial(Scene):
    def construct(self):
        trace=merge_trace(TUTORIAL_VALUES)
        self.stage=stage=MergeStage(self,list(trace.initial),MergePace(
            split=.65,begin=.75,compare=.55,write=.65,finish=.65,hold=1.3))
        caption=None

        def say(text,hold=1.15):
            nonlocal caption
            if caption is not None:self.play(FadeOut(caption),run_time=.18)
            caption=cmr(text,28,INK,'ti').move_to(UP*2.6)
            self.play(FadeIn(caption),run_time=.22);self.wait(hold)

        stage.build();say('Divide the problem. Merge the answers.',1.3)
        seen=set()
        def before(index,ev):
            if isinstance(ev,Split) and 'split' not in seen:
                seen.add('split');say('Split in half, until each run holds one value.')
            elif isinstance(ev,MergeStart) and 'start' not in seen:
                seen.add('start');say('A single value is already ordered. Now merge.',1.1)
            elif isinstance(ev,Compare) and 'compare' not in seen:
                seen.add('compare');say('Compare the front value of each ordered run.',1.1)
            elif isinstance(ev,Write) and not ev.remainder and 'write' not in seen:
                seen.add('write');say('Take the smaller value into the next output slot.',1.1)
            elif isinstance(ev,Write) and ev.remainder and 'rest' not in seen:
                seen.add('rest');say('One run empty? The remaining values follow in order.',1.1)
            elif isinstance(ev,MergeStart) and ev.lo==0 and ev.hi==len(TUTORIAL_VALUES):
                say('Two ordered halves. One final merge.',1.3)
            elif isinstance(ev,MergeComplete) and ev.lo==0 and ev.hi==len(TUTORIAL_VALUES):
                say('Every placement is a write, not a swap.',1.1)
        stage.play_trace(trace.events,before=before)
        self.play(FadeOut(caption),run_time=.2)
        summary=VGroup(
            math(r'\textit{time}',r'\quad O(n\log n)',size=35),
            math(r'\textit{extra space}',r'\quad O(n)',size=35),
            cmr('Equal values: choose left first to preserve their order.',26,MUTED,'ti'),
        ).arrange(DOWN,buff=.25).move_to(DOWN*1.85)
        summary[0][1].set_color(DONE);summary[1][1].set_color(DONE)
        self.play(Draw(summary),run_time=1.1);self.wait(2.1)

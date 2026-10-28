"""Insertion Sort trace adapter using Algorithm Arena's shared Manim grammar."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from manim import (DOWN, LEFT, ORIGIN, RIGHT, UL, UP, UR, AnimationGroup,
                   DashedVMobject, FadeIn, FadeOut, FadeTransform, Line,
                   RoundedRectangle, VGroup, Write, rate_functions)

from .insertion import Compare, Complete, Event, InsertKey, PassComplete, SelectKey, Shift
from .visual import (BG, DONE, DONE_FILL, FOCUS, INK, KEEP, MUTED, SWAP, TILE,
                     Tile, cmr, done_badge, focus_window, label_size, math, num, tex_int)


@dataclass(frozen=True)
class InsertionPace:
    compare: float = .32
    verdict: float = .18
    shift: float = .50
    lift: float = .45
    place: float = .50
    prefix: float = .35
    hold: float = 1.2

    @classmethod
    def for_size(cls, n):
        return cls() if n<=6 else cls(compare=.24, verdict=.14, shift=.38,
                                     lift=.35, place=.38, prefix=.28, hold=1.0)


class InsertionStage:
    def __init__(self, scene, values, pace=None):
        self.scene=scene
        self.n=len(values)
        self.pace=pace or InsertionPace.for_size(self.n)
        self.side=1.0 if self.n<=8 else 1.1
        step=self.side+(.28 if self.n<=8 else .15)
        self.slots=[ORIGIN+RIGHT*(step*(k-(self.n-1)/2))+UP*.15 for k in range(self.n)]
        size=label_size(values,self.side)
        self.tiles=[Tile(v,self.side,size).move_to(p) for v,p in zip(values,self.slots)]
        self.comparisons=self.shifts=self.placements=0
        self.key=None
        self.key_label=None
        self.gap=None
        self.window=None
        self.cue=None
        self.prefix=VGroup()
        self.pass_label=VGroup()
        self.ordered_until=0
        self.history=[]  # exact scene times for reproducible motion review captures

    def _prefix(self, end):
        a=self.slots[0]+LEFT*self.side/2+DOWN*(self.side/2+.56)
        b=self.slots[end]+RIGHT*self.side/2+DOWN*(self.side/2+.56)
        rule=Line(a,b,color=KEEP,stroke_width=3)
        ticks=VGroup(*(Line(p,p+UP*.12,color=KEEP,stroke_width=3) for p in (a,b)))
        label=cmr('ordered prefix',24,KEEP,'ti').next_to(rule,DOWN,buff=.10)
        return VGroup(rule,ticks,label)

    def _metric_value(self,k):
        value=[self.comparisons,self.shifts,self.placements][k]
        return cmr(str(value),28).next_to(self.metric_labels[k],RIGHT,buff=.15)

    def _bump(self,k):
        new=self._metric_value(k)
        old,self.metric_values[k]=self.metric_values[k],new
        return FadeTransform(old,new)

    @property
    def metrics(self):
        return VGroup(*self.metric_labels,*self.metric_values)

    def cue_anims(self,new=None):
        old=self.cue;self.cue=new
        if old is not None and new is not None:return [FadeTransform(old,new)]
        if old is not None:return [FadeOut(old)]
        if new is not None:return [FadeIn(new)]
        return []

    def build(self):
        s=self.scene;s.camera.background_color=BG
        title=cmr('Insertion Sort',40).to_corner(UL,buff=.55)
        indices=VGroup(*(cmr(str(i),22,MUTED).move_to(p+DOWN*(self.side/2+.3)) for i,p in enumerate(self.slots)))
        self.metric_labels=[cmr(t,24,MUTED,'ti').move_to(RIGHT*x+DOWN*2.65)
                            for t,x in [('comparisons',-4.0),('shifts',-.55),('placements',2.7)]]
        self.metric_values=[self._metric_value(k) for k in range(3)]
        self.prefix=self._prefix(0)
        s.play(Write(title),run_time=.8)
        s.play(AnimationGroup(*(FadeIn(t,shift=UP*.25) for t in self.tiles),lag_ratio=.08),FadeIn(indices),run_time=1.0)
        s.play(FadeIn(self.metrics),FadeIn(self.prefix),run_time=.4)
        s.wait(.6)

    def select_key(self,ev):
        s=self.scene;p=self.pace
        self.key=self.tiles[ev.index];self.tiles[ev.index]=None
        newpass=cmr(f'key {ev.index}',28,MUTED,'ti').to_corner(UR,buff=.55)
        self.gap=DashedVMobject(RoundedRectangle(corner_radius=.15,width=self.side,height=self.side,
                           stroke_color=MUTED,stroke_width=2),num_dashes=24).move_to(self.slots[ev.index])
        self.key_label=cmr('key',24,FOCUS,'ti').move_to(self.slots[ev.index]+UP*(1.2+self.side/2+.25))
        self.key.box.set_stroke(FOCUS,width=4)
        anims=[self.key.animate.shift(UP*1.2),
               FadeIn(self.key_label),FadeIn(self.gap),*self.cue_anims(None)]
        if len(self.prefix):anims.append(FadeOut(self.prefix))
        self.prefix=VGroup()
        anims.append(FadeTransform(self.pass_label,newpass) if len(self.pass_label) else FadeIn(newpass))
        self.pass_label=newpass
        if self.window is not None:
            anims.append(FadeOut(self.window));self.window=None
        s.play(*anims,run_time=p.lift)
        s.wait(.15)

    def compare(self,ev):
        s=self.scene;p=self.pace
        left=self.tiles[ev.left_index]
        if self.window is None:
            self.window=focus_window(self.side+.24,self.side+.24).move_to(self.slots[ev.left_index])
            focus=FadeIn(self.window)
        else:focus=self.window.animate.move_to(self.slots[ev.left_index])
        self.comparisons+=1
        s.play(focus,left.box.animate.set_stroke(FOCUS,width=4),
               self.key.box.animate.set_stroke(FOCUS,width=4),self._bump(0),
               *self.cue_anims(None),run_time=p.compare)
        rel='>' if ev.left>ev.key else ('=' if ev.left==ev.key else '<')
        verdict=r'\textit{shift right}' if ev.shift else r'\textit{place key}'
        cue=math(f'{tex_int(ev.left)} {rel} {tex_int(ev.key)}',r'\;\Rightarrow\;',verdict,size=38).move_to(DOWN*1.85)
        cue[1:].set_color(SWAP if ev.shift else KEEP)
        s.play(*self.cue_anims(cue),left.box.animate.set_stroke(SWAP if ev.shift else FOCUS),run_time=p.verdict)
        if not ev.shift:s.wait(.15)

    def shift(self,ev):
        s=self.scene;p=self.pace;tile=self.tiles[ev.source]
        # Clear the pre-move comparison while values physically change places.
        # The held key travels above the moving prefix, never replacing a label.
        s.play(tile.animate.move_to(self.slots[ev.target]),
               self.key.animate.move_to(self.slots[ev.source]+UP*1.2),
               self.key_label.animate.move_to(self.slots[ev.source]+UP*(1.2+self.side/2+.25)),
               self.gap.animate.move_to(self.slots[ev.source]),
               *self.cue_anims(None),run_time=p.shift,rate_func=rate_functions.smooth)
        self.tiles[ev.target],self.tiles[ev.source]=tile,None
        self.shifts+=1
        s.play(tile.box.animate.set_stroke(TILE,width=3),self._bump(1),run_time=.12)

    def insert(self,ev):
        s=self.scene;p=self.pace
        cue=cmr(f'place {num(ev.value)} in the gap',30,KEEP,'ti').move_to(DOWN*1.85)
        anims=[*self.cue_anims(cue),self.key.animate.move_to(self.slots[ev.index]),
               FadeOut(self.gap),FadeOut(self.key_label)]
        if self.window is not None:
            anims.append(FadeOut(self.window));self.window=None
        # A no-shift comparison may have left its neighbour highlighted.
        for t in self.tiles:
            if t is not None:anims.append(t.box.animate.set_stroke(TILE,width=3))
        s.play(*anims,run_time=p.place,rate_func=rate_functions.smooth)
        self.key.box.set_stroke(TILE,width=3)
        self.tiles[ev.index]=self.key
        self.key=None;self.key_label=None;self.gap=None
        self.placements+=1
        s.play(self._bump(2),run_time=.12)

    def pass_complete(self,ev):
        self.ordered_until=ev.sorted_until
        self.prefix=self._prefix(ev.sorted_until)
        self.scene.play(FadeIn(self.prefix),*self.cue_anims(None),run_time=self.pace.prefix)
        self.scene.wait(.1)

    def complete(self,ev):
        s=self.scene;p=self.pace
        anims=[*self.cue_anims(None),FadeOut(self.prefix),FadeOut(self.pass_label)]
        for tile in self.tiles:
            badge=done_badge(self.side).move_to(tile.box.get_corner(UR)+(LEFT+DOWN)*self.side*.04)
            tile.add(badge)
            anims.extend([tile.box.animate.set_stroke(DONE,width=3).set_fill(DONE_FILL,1),FadeIn(badge,scale=.6)])
        result=cmr('every key is in order',34,DONE,'ti').move_to(UP*1.5)
        s.play(*anims,FadeIn(result),run_time=.6)
        self.cue=result;self.prefix=VGroup();self.pass_label=VGroup()
        s.wait(p.hold)

    def play_trace(self,events,before:Callable|None=None):
        handlers={SelectKey:self.select_key,Compare:self.compare,Shift:self.shift,
                  InsertKey:self.insert,PassComplete:self.pass_complete,Complete:self.complete}
        for index,ev in enumerate(events):
            if before:before(index,ev)
            start=float(self.scene.time)
            handlers[type(ev)](ev)
            self.history.append({'event':type(ev).__name__,'start':round(start,3),
                                 'end':round(float(self.scene.time),3)})

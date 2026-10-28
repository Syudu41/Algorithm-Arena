"""Merge trace adapter: recursive descent and two-run, identity-preserving merging."""
from __future__ import annotations
from dataclasses import dataclass
from manim import (DOWN, LEFT, RIGHT, UL, UP, UR, AnimationGroup, DashedVMobject,
                   FadeIn, FadeOut, FadeTransform, Line, RoundedRectangle, VGroup,
                   Write as Draw, rate_functions)
from .merge import Compare, Complete, Event, MergeComplete, MergeStart, Split, Write
from .visual import (BG, DONE, DONE_FILL, FOCUS, INK, KEEP, MUTED, SWAP, TILE, Tile,
                     cmr, done_badge, focus_window, label_size, math, num, tex_int)


@dataclass(frozen=True)
class MergePace:
    split: float = .4
    begin: float = .5
    compare: float = .34
    write: float = .4
    finish: float = .45
    hold: float = 1.1


class MergeStage:
    def __init__(self, scene, values, pace=None):
        self.scene=scene;self.n=len(values);self.pace=pace or MergePace()
        self.side=.90 if self.n<=6 else .82
        self.step=self.side+.24
        self.positions=[RIGHT*self.step*(i-(self.n-1)/2)+UP*1.15 for i in range(self.n)]
        size=label_size(values,self.side)
        self.tiles={i:Tile(v,self.side,size).move_to(p)
                    for i,(v,p) in enumerate(zip(values,self.positions))}
        self.order=list(range(self.n))
        self.parents={};self.branches={}
        self.comparisons=self.writes=0
        self.cue=None;self.phase=None;self.merge_labels=VGroup();self.windows=VGroup()
        self.guides=VGroup();self.current=None;self.history=[]

    def cue_anims(self,new=None):
        old=self.cue;self.cue=new
        if old is not None and new is not None:return [FadeTransform(old,new)]
        if old is not None:return [FadeOut(old)]
        if new is not None:return [FadeIn(new)]
        return []

    def _phase(self,text):
        new=cmr(text,27,MUTED,'ti').to_corner(UR,buff=.55)
        old=self.phase;self.phase=new
        return FadeTransform(old,new) if old is not None else FadeIn(new)

    def _metric(self,k):
        return cmr(str([self.comparisons,self.writes][k]),28).next_to(self.metric_labels[k],RIGHT,buff=.18)

    def _bump(self,k):
        old=self.metric_values[k];self.metric_values[k]=new=self._metric(k)
        return FadeTransform(old,new)

    @property
    def metrics(self):return VGroup(*self.metric_labels,*self.metric_values)

    def build(self):
        s=self.scene;s.camera.background_color=BG
        title=cmr('Merge Sort',40).to_corner(UL,buff=.55)
        self.metric_labels=[cmr(t,25,MUTED,'ti').move_to(RIGHT*x+DOWN*3.15)
                            for t,x in [('comparisons',-2.4),('writes',1.65)]]
        self.metric_values=[self._metric(0),self._metric(1)]
        definition=cmr('writes = values placed into merged runs',22,MUTED,'ti').move_to(DOWN*3.65)
        s.play(Draw(title),run_time=.8)
        s.play(AnimationGroup(*(FadeIn(t,shift=UP*.2) for t in self.tiles.values()),lag_ratio=.08),run_time=1)
        s.play(FadeIn(self.metrics),FadeIn(definition),run_time=.4)
        s.wait(.6)

    def split(self,ev):
        s=self.scene
        self.parents[(ev.lo,ev.hi)]=[p.copy() for p in self.positions[ev.lo:ev.hi]]
        origin=sum(self.positions[ev.lo:ev.hi])/(ev.hi-ev.lo)
        for i in range(ev.lo,ev.hi):
            self.positions[i]=self.positions[i]+DOWN*.68+(LEFT if i<ev.mid else RIGHT)*.19
        left=sum(self.positions[ev.lo:ev.mid])/(ev.mid-ev.lo)
        right=sum(self.positions[ev.mid:ev.hi])/(ev.hi-ev.mid)
        branches=VGroup(*(Line(origin+UP*.10,p+UP*self.side*.52,color=MUTED,
                               stroke_width=1.5,stroke_opacity=.65) for p in [left,right]))
        branches.set_z_index(-1);self.branches[(ev.lo,ev.hi)]=branches
        cue=cmr('split into smaller problems',29,KEEP,'ti').move_to(DOWN*2.4)
        s.play(*(self.tiles[self.order[i]].animate.move_to(self.positions[i]) for i in range(ev.lo,ev.hi)),
               FadeIn(branches),self._phase('divide'),*self.cue_anims(cue),run_time=self.pace.split)

    def begin_merge(self,ev):
        s=self.scene;self.current=ev
        ids=ev.left_ids+ev.right_ids;m=len(ids)
        self.source_positions={identity:RIGHT*((k-(m-1)/2)*self.step+(-.29 if k<len(ev.left_ids) else .29))+UP*.85
                               for k,identity in enumerate(ids)}
        self.output_positions=[RIGHT*((k-(m-1)/2)*self.step)+DOWN*1.05 for k in range(m)]
        leftcenter=sum(self.source_positions[i] for i in ev.left_ids)/len(ev.left_ids)
        rightcenter=sum(self.source_positions[i] for i in ev.right_ids)/len(ev.right_ids)
        self.merge_labels=VGroup(cmr('left run',25,KEEP,'ti').move_to(leftcenter+UP*.83),
                                 cmr('right run',25,KEEP,'ti').move_to(rightcenter+UP*.83),
                                 cmr('merged run',25,KEEP,'ti').move_to(DOWN*1.9))
        self.guides=VGroup(*(DashedVMobject(RoundedRectangle(corner_radius=.12,width=self.side,
                              height=self.side,stroke_color=MUTED,stroke_width=1.4),num_dashes=20).move_to(p)
                              for p in self.output_positions))
        self.remaining={'left':list(ev.left_ids),'right':list(ev.right_ids)}
        inactive=[i for i in self.order if i not in ids]
        s.play(*(FadeOut(self.tiles[i]) for i in inactive),
               *(FadeOut(b) for b in self.branches.values()),
               *(self.tiles[i].animate.move_to(self.source_positions[i]) for i in ids),
               FadeIn(self.merge_labels),FadeIn(self.guides),self._phase('merge'),
               *self.cue_anims(None),run_time=self.pace.begin)
        self.hidden=inactive

    def compare(self,ev):
        s=self.scene
        heads=[self.tiles[i] for i in (ev.left_id,ev.right_id)]
        windows=VGroup(*(focus_window(self.side+.16,self.side+.16).move_to(t) for t in heads))
        self.comparisons+=1
        relation='<' if ev.left<ev.right else ('=' if ev.left==ev.right else '>')
        verdict=r'\textit{left first}' if ev.take_left else r'\textit{take right}'
        cue=math(f'{tex_int(ev.left)} {relation} {tex_int(ev.right)}',r'\;\Rightarrow\;',verdict,size=33).move_to(DOWN*2.4)
        cue[1:].set_color(FOCUS)
        anims=[self._bump(0),*self.cue_anims(cue),FadeIn(windows)]
        if len(self.windows):anims.append(FadeOut(self.windows))
        for tile in heads:anims.append(tile.box.animate.set_stroke(FOCUS,width=4))
        self.windows=windows
        s.play(*anims,run_time=self.pace.compare)
        # The verdict remains visible before the chosen value starts moving.
        s.wait(.08)

    def write(self,ev):
        s=self.scene;tile=self.tiles[ev.identity]
        tile.box.set_stroke(SWAP,width=4)
        self.writes+=1
        anims=[tile.animate.move_to(self.output_positions[ev.target-self.current.lo]),self._bump(1)]
        if len(self.windows):anims.append(FadeOut(self.windows));self.windows=VGroup()
        if ev.remainder:
            cue=cmr('one run is empty: copy the rest',29,KEEP,'ti').move_to(DOWN*2.4)
            anims+=self.cue_anims(cue)
        else:anims+=self.cue_anims(None)
        s.play(*anims,run_time=self.pace.write,rate_func=rate_functions.smooth)
        tile.box.set_stroke(TILE,width=3)
        self.guides[ev.target-self.current.lo].set_opacity(0)
        # Unchosen heads return to the resting style; values move as whole tiles.
        for identity in self.remaining['left']+self.remaining['right']:
            self.tiles[identity].box.set_stroke(TILE,width=3)
        self.remaining['left' if ev.from_left else 'right'].pop(0)

    def finish_merge(self,ev):
        s=self.scene
        parent=self.parents[(ev.lo,ev.hi)]
        del self.branches[(ev.lo,ev.hi)]
        self.order[ev.lo:ev.hi]=ev.identities
        self.positions[ev.lo:ev.hi]=parent
        cue=cmr('one ordered run',29,KEEP,'ti').move_to(DOWN*2.4)
        s.play(*(self.tiles[identity].animate.move_to(p) for identity,p in zip(ev.identities,parent)),
               *(FadeIn(self.tiles[i]) for i in self.hidden),
               *(FadeIn(b) for b in self.branches.values()),
               FadeOut(self.merge_labels),FadeOut(self.guides),*self.cue_anims(cue),run_time=self.pace.finish)
        self.merge_labels=VGroup();self.guides=VGroup();self.current=None

    def complete(self,ev):
        s=self.scene
        anims=[*self.cue_anims(None),self._phase('complete')]
        for identity in self.order:
            tile=self.tiles[identity]
            badge=done_badge(self.side).move_to(tile.box.get_corner(UR)+(LEFT+DOWN)*self.side*.04)
            tile.add(badge)
            anims += [tile.box.animate.set_stroke(DONE,width=3).set_fill(DONE_FILL,1),FadeIn(badge,scale=.6)]
        result=cmr('small ordered runs become one sorted array',31,DONE,'ti').move_to(DOWN*.5)
        s.play(*anims,FadeIn(result),run_time=.6)
        self.cue=result;s.wait(self.pace.hold)

    def play_trace(self,events,before=None):
        handlers={Split:self.split,MergeStart:self.begin_merge,Compare:self.compare,
                  Write:self.write,MergeComplete:self.finish_merge,Complete:self.complete}
        for index,ev in enumerate(events):
            if before:before(index,ev)
            start=float(self.scene.time)
            handlers[type(ev)](ev)
            self.history.append({'event':type(ev).__name__,'start':round(start,3),
                                 'end':round(float(self.scene.time),3)})

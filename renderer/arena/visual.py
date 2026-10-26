"""Shared Manim visual grammar for every Algorithm Arena video.

`ArrayStage` turns trace events from `arena.bubble` into animation. The
tutorial and custom-input scenes both use it, so colour semantics, type,
positions and swap motion are identical; only the narration differs.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Callable, Optional

from manim import (
    DOWN, LEFT, ORIGIN, PI, RIGHT, UL, UP, UR,
    AnimationGroup, Circle, Create, FadeIn, FadeOut, FadeTransform, Line, MathTex, RoundedRectangle,
    Scene, Text, VGroup, VMobject, Write, rate_functions,
)

from .bubble import Compare, Complete, Event, PassComplete, Swap

FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"
FONT = "CMU Serif"

# Palette: one luminous accent per meaning, on a near-black navy canvas.
BG = "#0B0F1A"
INK = "#ECEFF4"          # values, titles
MUTED = "#6B7894"        # index labels, secondary text
TILE = "#58C4DD"         # resting element outline
TILE_FILL = "#14243A"
FOCUS = "#FFD25E"        # the pair being compared
SWAP = "#FC6255"         # condition true: they trade places
KEEP = "#9CDCEB"         # condition false: leave them
DONE = "#83C167"         # final position
DONE_FILL = "#16301F"


@lru_cache(maxsize=None)
def _cmap(path: str) -> frozenset[int]:
    from fontTools.ttLib import TTFont
    return frozenset(TTFont(path).getBestCmap())


def cmr(text: str, size: float = 36, color: str = INK, weight: str = "rm") -> Text:
    """Text in Computer Modern; refuses characters the font cannot draw, so
    Pango can never silently substitute a sans-serif fallback glyph."""
    path = str(FONT_DIR / f"cmun{weight}.ttf")
    missing = {c for c in text if not c.isspace() and ord(c) not in _cmap(path)}
    if missing:
        raise ValueError(f"CMU Serif lacks glyphs {sorted(missing)!r} in {text!r}")
    style = "ITALIC" if weight in ("ti", "bi") else "NORMAL"
    w = "BOLD" if weight in ("bx", "bi") else "NORMAL"
    return Text(text, font=FONT, font_size=size, color=color, slant=style, weight=w)


def math(*parts: str, size: float = 40, color: str = INK) -> MathTex:
    """Real TeX math in Computer Modern. Callers pass only trusted literals
    and validated ints formatted by `tex_int`; never raw user text."""
    return MathTex(*parts, font_size=size, color=color)


def tex_int(v: int) -> str:
    if type(v) is not int:
        raise TypeError("only validated ints may reach TeX")
    return str(v)


def num(v: int) -> str:
    # typographic minus, not a hyphen
    return f"−{-v}" if v < 0 else str(v)


@dataclass(frozen=True)
class Pace:
    """Seconds per beat. Defaults sit inside the timing contract."""
    compare: float = 0.32     # window glides onto the pair, outlines light up
    verdict: float = 0.22     # relation cue appears
    swap: float = 0.50        # physical arc exchange
    keep: float = 0.18        # brief rest when no swap is needed
    pass_end: float = 0.45    # tile settles into the sorted suffix
    hold: float = 1.2         # start / end holds

    @staticmethod
    def for_size(n: int) -> "Pace":
        # Longer arrays have quadratically more events: compress toward the
        # low end of each contract range but never skip an event.
        if n <= 6:
            return Pace()
        if n <= 8:
            return Pace(compare=0.26, verdict=0.18, swap=0.42, keep=0.13, pass_end=0.38)
        return Pace(compare=0.22, verdict=0.14, swap=0.36, keep=0.10, pass_end=0.32, hold=1.0)


def check_mark(size: float = 0.22, color: str = DONE) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=4)
    m.set_points_as_corners([[-0.5, 0.0, 0], [-0.15, -0.38, 0], [0.55, 0.45, 0]])
    return m.scale(size)


def focus_window(width: float, height: float) -> VGroup:
    """Comparison window: a crisp outline over soft halo strokes (the glow)."""
    layers = [RoundedRectangle(corner_radius=0.2, width=width, height=height,
                               stroke_color=FOCUS, stroke_width=w, stroke_opacity=o)
              for w, o in ((16, 0.08), (9, 0.16), (4, 1.0))]
    return VGroup(*layers)


class Tile(VGroup):
    """A value glued to its square: they always move together."""

    def __init__(self, value: int, side: float, label_size: float):
        self.value = value
        self.box = RoundedRectangle(
            corner_radius=side * 0.14, width=side, height=side,
            stroke_color=TILE, stroke_width=3, fill_color=TILE_FILL, fill_opacity=1,
        )
        self.label = cmr(num(value), size=label_size)
        super().__init__(self.box, self.label)


def label_size(values: list[int], side: float) -> float:
    """One type size for every tile in a video, fitted to the widest value."""
    nominal = side * 44
    widest = max(cmr(num(v), size=nominal).width for v in set(values))
    return nominal * min(1.0, side * 0.80 / widest)


def done_badge(side: float) -> VGroup:
    """Check-mark badge straddling the tile's top-right corner, clear of the value."""
    r = side * 0.17
    disk = Circle(radius=r, stroke_color=DONE, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    return VGroup(disk, check_mark(r * 1.1).move_to(disk))


class ArrayStage:
    def __init__(self, scene: Scene, values: list[int], pace: Optional[Pace] = None,
                 title: str = "Bubble Sort", y: float = 0.15):
        self.scene = scene
        self.n = len(values)
        self.pace = pace or Pace.for_size(self.n)
        self.title_text = title
        self.side = 1.0 if self.n <= 8 else 1.1
        gap = 0.28 if self.n <= 8 else 0.15
        step = self.side + gap
        x0 = -step * (self.n - 1) / 2
        self.slots = [ORIGIN + RIGHT * (x0 + k * step) + UP * y for k in range(self.n)]
        size = label_size(values, self.side)
        self.tiles = [Tile(v, self.side, size).move_to(p) for v, p in zip(values, self.slots)]
        self.window: Optional[RoundedRectangle] = None
        self.cue: Optional[VGroup] = None
        self.sorted_from = self.n
        self.comparisons = self.swaps = 0
        self.pass_no = 0

    # ---------- layout helpers ----------
    def _pair_center(self, i: int):
        return (self.slots[i] + self.slots[i + 1]) / 2

    def _metric_labels(self) -> VGroup:
        # Laid out once with two-digit placeholders so labels never shift.
        row = VGroup(cmr("comparisons", 26, MUTED, "ti"), cmr("00", 28),
                     cmr("swaps", 26, MUTED, "ti"), cmr("00", 28))
        row[1].next_to(row[0], RIGHT, buff=0.18)
        row[2].next_to(row[1], RIGHT, buff=0.6)
        row[3].next_to(row[2], RIGHT, buff=0.18)
        row.move_to(DOWN * 2.55)
        return VGroup(row[0], row[2])

    def _metric_value(self, k: int) -> Text:
        v = self.comparisons if k == 0 else self.swaps
        return cmr(str(v), 28).next_to(self.metric_labels[k], RIGHT, buff=0.18)

    def _bump(self, k: int):
        """Animation that updates comparison (k=0) or swap (k=1) count."""
        new = self._metric_value(k)
        old, self.metric_values[k] = self.metric_values[k], new
        return FadeTransform(old, new)

    def _pass_label(self) -> Text:
        return cmr(f"pass {self.pass_no}" if self.pass_no else "", 28, MUTED, "ti") \
            .to_corner(UR, buff=0.55) if self.pass_no else VGroup().to_corner(UR)

    def _sorted_rule(self) -> VGroup:
        if self.sorted_from >= self.n:
            return VGroup()
        a = self.slots[self.sorted_from] + LEFT * self.side / 2
        b = self.slots[-1] + RIGHT * self.side / 2
        off = DOWN * (self.side / 2 + 0.62)
        rule = Line(a + off, b + off, color=DONE, stroke_width=3)
        ticks = VGroup(*(Line(p + off, p + off + UP * 0.12, color=DONE, stroke_width=3)
                         for p in (a, b)))
        tag = cmr("sorted", 24, DONE, "ti").next_to(rule, DOWN, buff=0.12)
        return VGroup(rule, ticks, tag)

    @property
    def metrics(self) -> VGroup:
        return VGroup(self.metric_labels, *self.metric_values)

    # ---------- setup ----------
    def build(self, intro: Optional[Text] = None):
        s = self.scene
        s.camera.background_color = BG
        self.title = cmr(self.title_text, 40).to_corner(UL, buff=0.55)
        self.index_labels = VGroup(*(
            cmr(str(k), 22, MUTED).move_to(p + DOWN * (self.side / 2 + 0.3))
            for k, p in enumerate(self.slots)
        ))
        self.metric_labels = self._metric_labels()
        self.metric_values = [self._metric_value(0), self._metric_value(1)]
        self.pass_mob = self._pass_label()
        self.rule = self._sorted_rule()
        s.play(Write(self.title), run_time=0.8)
        s.play(
            AnimationGroup(*(FadeIn(t, shift=UP * 0.25) for t in self.tiles), lag_ratio=0.08),
            FadeIn(self.index_labels), run_time=1.0,
        )
        s.play(FadeIn(self.metrics), run_time=0.4)
        s.wait(self.pace.hold * 0.5)

    # ---------- event handlers ----------
    def _set_cue(self, cue: Optional[VGroup], run_time: float):
        anims = []
        if self.cue is not None and cue is not None:
            anims.append(FadeTransform(self.cue, cue))
        elif self.cue is not None:
            anims.append(FadeOut(self.cue))
        elif cue is not None:
            anims.append(FadeIn(cue, shift=DOWN * 0.1))
        self.cue = cue
        return anims

    def compare(self, ev: Compare):
        s, p = self.scene, self.pace
        a, b = self.tiles[ev.i], self.tiles[ev.j]
        w = self.side * 2 + (self.slots[1][0] - self.slots[0][0] - self.side) + 0.26
        if self.window is None:
            self.window = focus_window(w, self.side + 0.26).move_to(self._pair_center(ev.i))
            enter = FadeIn(self.window, scale=1.06)
        else:
            enter = self.window.animate.move_to(self._pair_center(ev.i))
        self.comparisons += 1
        s.play(
            enter,
            a.box.animate.set_stroke(FOCUS, width=4),
            b.box.animate.set_stroke(FOCUS, width=4),
            *self._set_cue(None, p.compare),
            self._bump(0),
            run_time=p.compare, rate_func=rate_functions.smooth,
        )
        rel = ">" if ev.left > ev.right else ("=" if ev.left == ev.right else "<")
        verdict = r"\textit{swap}" if ev.swap else r"\textit{keep}"
        cue = math(f"{tex_int(ev.left)} {rel} {tex_int(ev.right)}", r"\;\Rightarrow\;", verdict,
                   size=40)
        cue[1:].set_color(SWAP if ev.swap else KEEP)
        cue.move_to(self._pair_center(ev.i) + UP * (self.side / 2 + 0.75))
        s.play(*self._set_cue(cue, p.verdict),
               *(t.box.animate.set_stroke(SWAP if ev.swap else FOCUS) for t in (a, b)),
               run_time=p.verdict)
        if not ev.swap:
            s.wait(p.keep)
            self._rest(a, b, run_time=0.12)

    def _rest(self, *tiles: Tile, run_time: float):
        self.scene.play(*(t.box.animate.set_stroke(TILE, width=3) for t in tiles),
                        run_time=run_time)

    def swap(self, ev: Swap):
        s, p = self.scene, self.pace
        a, b = self.tiles[ev.i], self.tiles[ev.j]
        a.set_z_index(2)
        b.set_z_index(1)
        # Same arc sign: the left tile travels over the top, the right one under.
        s.play(
            a.animate(path_arc=-PI * 0.85).move_to(self.slots[ev.j]),
            b.animate(path_arc=-PI * 0.85).move_to(self.slots[ev.i]),
            run_time=p.swap, rate_func=rate_functions.smooth,
        )
        self.tiles[ev.i], self.tiles[ev.j] = b, a
        self.swaps += 1
        s.play(
            self._bump(1),
            *(t.box.animate.set_stroke(TILE, width=3) for t in (a, b)),
            run_time=0.14,
        )
        a.set_z_index(0)
        b.set_z_index(0)

    def _finalize(self, tiles: list[Tile]):
        anims = []
        for t in tiles:
            badge = done_badge(self.side).move_to(
                t.box.get_corner(UR) + (LEFT + DOWN) * self.side * 0.04)
            t.add(badge)
            anims += [t.box.animate.set_stroke(DONE, width=3).set_fill(DONE_FILL, 1),
                      FadeIn(badge, scale=0.6)]
        return anims

    def pass_complete(self, ev: PassComplete, note: Optional[str] = None):
        s, p = self.scene, self.pace
        newly = self.tiles[ev.sorted_from:self.sorted_from]
        self.sorted_from = ev.sorted_from
        new_rule = self._sorted_rule()
        cue = None
        if ev.early_exit:
            cue = math(r"\textit{no swaps this pass}", r"\;\Rightarrow\;",
                       r"\textit{already sorted}", size=38, color=DONE).move_to(UP * (self.slots[0][1] + self.side / 2 + 0.75))
        anims = [*self._finalize(newly), *self._set_cue(cue, p.pass_end)]
        anims.append(FadeTransform(self.rule, new_rule) if len(self.rule) else FadeIn(new_rule))
        if self.window is not None:
            anims.append(FadeOut(self.window))
            self.window = None
        s.play(*anims, run_time=p.pass_end)
        self.rule = new_rule
        if ev.early_exit:
            s.wait(p.hold * 0.6)

    def start_pass(self, number: int):
        self.pass_no = number
        new = self._pass_label()
        self.scene.play(FadeTransform(self.pass_mob, new) if len(self.pass_mob) else FadeIn(new),
                        run_time=0.25)
        self.pass_mob = new

    def complete(self, ev: Complete):
        s, p = self.scene, self.pace
        passes_label_present = len(self.pass_mob)
        anims = [*self._set_cue(None, 0.3)]
        if passes_label_present:
            anims.append(FadeOut(self.pass_mob))
            self.pass_mob = VGroup()
        if anims:
            s.play(*anims, run_time=0.3)
        passes = self.pass_no
        result = cmr(f"sorted in {passes} pass{'es' if passes != 1 else ''}", 34, DONE, "ti").move_to(
            UP * (self.slots[0][1] + self.side / 2 + 0.85))
        s.play(
            AnimationGroup(*(t.animate.shift(UP * 0.12) for t in self.tiles), lag_ratio=0.06),
            FadeIn(result, shift=DOWN * 0.1), run_time=0.6,
        )
        s.play(AnimationGroup(*(t.animate.shift(DOWN * 0.12) for t in self.tiles),
                              lag_ratio=0.06), run_time=0.4)
        self.cue = result
        s.wait(p.hold)

    # ---------- driver ----------
    def play_trace(self, events: tuple[Event, ...],
                   before: Optional[Callable[[int, Event], None]] = None):
        """Animate every event in order. `before(k, ev)` lets the tutorial
        insert narration without altering what the trace says."""
        expect_pass = 1
        for k, ev in enumerate(events):
            if before:
                before(k, ev)
            if isinstance(ev, Compare):
                if self.pass_no != expect_pass:
                    self.start_pass(expect_pass)
                self.compare(ev)
            elif isinstance(ev, Swap):
                self.swap(ev)
            elif isinstance(ev, PassComplete):
                self.pass_complete(ev)
                expect_pass = ev.number + 1
            elif isinstance(ev, Complete):
                self.complete(ev)

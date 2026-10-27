"""Original, seamless About-page title animation (not an API scene).

Inspiration: the circular title treatment in Mitko Nikov's
https://www.youtube.com/watch?v=rIgOfmcd1iA . No reference media is reused.
"""
from manim import Arc, Circle, Rotate, Scene, TAU, DOWN, VGroup, linear

from .visual import BG, INK, SWAP, TILE, cmr


class AlgorithmArenaIntro(Scene):
    def construct(self):
        self.camera.background_color = BG
        radius = 2.65
        disk = Circle(radius=radius, stroke_color=SWAP, stroke_width=2.8,
                      fill_color='#24151E', fill_opacity=0.58)
        # Concentric rings echo the reference's title, using our existing palette.
        rim = Circle(radius=radius + 0.28, stroke_color=TILE,
                     stroke_width=1, stroke_opacity=0.13)
        arc = Arc(radius=radius + 0.28, start_angle=0.35, angle=TAU * 0.72,
                  stroke_color=TILE, stroke_width=10)
        halo = Arc(radius=radius + 0.28, start_angle=0.35, angle=TAU * 0.72,
                   stroke_color=TILE, stroke_width=22, stroke_opacity=0.07)
        orbit = VGroup(halo, arc)
        first = cmr('Algorithm', size=66, color=INK, weight='ti')
        second = cmr('Arena', size=66, color=INK, weight='ti')
        title = VGroup(first, second).arrange(DOWN, buff=0.12)
        title.scale_to_fit_width(4.5)
        title.move_to(disk)
        self.add(disk, rim, orbit, title)
        # Only the arc rotates. Title remains readable, even at the loop boundary.
        # 150 distinct frames at 25 fps; last → first is one ordinary rotation step.
        self.play(Rotate(orbit, angle=-TAU, about_point=disk.get_center()),
                  run_time=6, rate_func=linear)

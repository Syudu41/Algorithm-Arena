"""Render worker: `python -m arena.render <job.json> <out.mp4>`.

Run by the service as an argv subprocess (shell=False). The job file holds
only {"scene": "<allow-listed name>", "values": [ints]}; both are validated
here again so the worker is safe even if invoked directly.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

RENDERER_VERSION = "arena-v3-insertion"
ROOT = Path(__file__).resolve().parent.parent
TEX_CACHE = ROOT / ".cache" / "tex"


def ensure_tex() -> str:
    """TeX is mandatory for the math cues; fail loudly, never fall back."""
    extra = os.environ.get("ARENA_TEX_BIN", str(Path.home() / ".TinyTeX/bin/x86_64-linux"))
    if Path(extra).is_dir():
        os.environ["PATH"] = extra + os.pathsep + os.environ.get("PATH", "")
    for tool in ("latex", "dvisvgm"):
        if not shutil.which(tool):
            raise RuntimeError(f"{tool} not found: install TeX (see docs) or set ARENA_TEX_BIN")
    return shutil.which("latex")


SCENES = {"custom": "BubbleCustom", "tutorial": "BubbleTutorial",
          "insertion_custom": "InsertionCustom", "insertion_tutorial": "InsertionTutorial"}


def render(scene_key: str, values: list[int] | None, out: Path) -> dict:
    from manim import tempconfig, register_font

    from . import scenes, insertion_scenes
    from .visual import FONT_DIR

    ensure_tex()
    TEX_CACHE.mkdir(parents=True, exist_ok=True)
    (TEX_CACHE.parent / "text").mkdir(exist_ok=True)
    if scene_key not in SCENES:
        raise ValueError(f"unknown scene {scene_key!r}")
    if scene_key == "custom":
        scenes.configure(values)
    module = insertion_scenes if scene_key.startswith("insertion_") else scenes
    if scene_key == "insertion_custom":
        insertion_scenes.configure(values)
    cls = getattr(module, SCENES[scene_key])
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="arena-") as media:
        opts = {
            "pixel_width": 1280, "pixel_height": 720, "frame_rate": 30,
            "media_dir": media, "tex_dir": str(TEX_CACHE),
            "text_dir": str(TEX_CACHE.parent / "text"), "output_file": "out",
            "disable_caching": True,
            "verbosity": "WARNING", "progress_bar": "none", "format": "mp4",
        }
        t0 = time.perf_counter()
        with register_font(str(FONT_DIR / "cmunrm.ttf")), \
                register_font(str(FONT_DIR / "cmunti.ttf")), \
                register_font(str(FONT_DIR / "cmunbx.ttf")), tempconfig(opts):
            scene = cls()
            scene.render()
            timeline = getattr(getattr(scene, "stage", None), "history", None)
            produced = Path(scene.renderer.file_writer.movie_file_path)
        elapsed = time.perf_counter() - t0
        tmp = out.with_suffix(".part.mp4")
        # The temporary render directory may be on a different filesystem.
        # Copy into the destination filesystem before the atomic publish.
        shutil.copyfile(produced, tmp)
        tmp.replace(out)  # atomic: a reader never sees a half-written file
    return {"scene": scene_key, "values": values, "render_seconds": round(elapsed, 2),
            "renderer_version": RENDERER_VERSION, "path": str(out),
            **({"timeline": timeline} if timeline is not None else {})}


def main(argv: list[str]) -> int:
    job_path, out_path = Path(argv[1]), Path(argv[2])
    job = json.loads(job_path.read_text())
    meta = render(job.get("scene", "custom"), job.get("values"), out_path)
    print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

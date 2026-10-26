"""Visual-guard and render integration tests.

The render test produces a real MP4 through the same worker the service uses
and checks it with ffprobe. It takes ~20 s; skip with `-m "not render"`.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from arena.visual import FONT_DIR, Pace, cmr, label_size, num, tex_int

ROOT = Path(__file__).resolve().parent.parent


def test_cmr_refuses_glyphs_missing_from_cmu():
    # These are absent from CMU Serif; Pango would silently fall back to sans.
    for bad in ("≤", "⇒", "✓"):
        with pytest.raises(ValueError, match="lacks glyphs"):
            cmr(f"2 {bad} 4")


def test_cmr_accepts_everything_the_scenes_print():
    for text in ("Bubble Sort", "comparisons", "swaps", "pass 9", "sorted in 9 passes",
                 "−99", "Compare neighbours.  Swap them if they are out of order."):
        cmr(text)


def test_vendored_fonts_present():
    for f in ("cmunrm", "cmunti", "cmunbx"):
        assert (FONT_DIR / f"{f}.ttf").is_file()


def test_negative_numbers_use_typographic_minus():
    assert num(-7) == "−7" and num(7) == "7"


def test_tex_only_receives_ints():
    assert tex_int(-99) == "-99"
    for bad in ("1}", 1.5, True, "\\input{x}"):
        with pytest.raises(TypeError):
            tex_int(bad)


def test_widest_label_fits_inside_tile():
    for side in (1.0, 1.1):
        size = label_size([-99, 99, -64], side)
        assert cmr(num(-99), size=size).width <= side * 0.8 + 1e-6


@pytest.mark.parametrize("n", range(2, 11))
def test_pacing_within_contract(n):
    p = Pace.for_size(n)
    assert 0.20 <= p.compare <= 0.40
    assert 0.35 <= p.swap <= 0.60
    assert 0.10 <= p.keep <= 0.25
    assert 0.5 <= p.hold <= 1.5


def _probe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_name,width,height,r_frame_rate,pix_fmt:format=duration",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True).stdout
    return json.loads(out)


@pytest.mark.render
@pytest.mark.skipif(shutil.which("ffprobe") is None, reason="ffprobe not on PATH")
def test_custom_render_produces_valid_mp4(tmp_path):
    job = tmp_path / "job.json"
    job.write_text(json.dumps({"scene": "custom", "values": [5, 2, 4, 1, 3]}))
    out = tmp_path / "out.mp4"
    proc = subprocess.run([sys.executable, "-m", "arena.render", str(job), str(out)],
                          cwd=ROOT, capture_output=True, text=True, timeout=300)
    assert proc.returncode == 0, proc.stderr[-2000:]
    meta = json.loads(proc.stdout.strip().splitlines()[-1])
    assert meta["values"] == [5, 2, 4, 1, 3]
    info = _probe(out)
    v = info["streams"][0]
    assert (v["codec_name"], v["width"], v["height"], v["r_frame_rate"], v["pix_fmt"]) == \
        ("h264", 1280, 720, "30/1", "yuv420p")
    assert 12 <= float(info["format"]["duration"]) <= 30
    # every frame decodes
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(out), "-f", "null", "-"],
                   check=True, timeout=120)


def test_worker_rejects_invalid_values(tmp_path):
    job = tmp_path / "job.json"
    job.write_text(json.dumps({"scene": "custom", "values": [1, 100]}))
    proc = subprocess.run([sys.executable, "-m", "arena.render", str(job),
                           str(tmp_path / "x.mp4")], cwd=ROOT, capture_output=True, text=True)
    assert proc.returncode != 0 and "InputError" in proc.stderr
    assert not (tmp_path / "x.mp4").exists()


def test_worker_rejects_unknown_scene(tmp_path):
    job = tmp_path / "job.json"
    job.write_text(json.dumps({"scene": "../../etc", "values": [1, 2]}))
    proc = subprocess.run([sys.executable, "-m", "arena.render", str(job),
                           str(tmp_path / "x.mp4")], cwd=ROOT, capture_output=True, text=True)
    assert proc.returncode != 0 and "unknown scene" in proc.stderr

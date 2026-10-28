"""Reproduce the About-page GIF with the existing genuine Manim installation.

PATH="$PWD/.venv-manim/bin:$PATH" .venv-manim/bin/python scripts/render_intro.py
"""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'renderer'))
from manim import register_font, tempconfig
from arena.intro import AlgorithmArenaIntro
from arena.visual import FONT_DIR


def main():
    media = ROOT / 'media'
    media.mkdir(exist_ok=True)
    output = media / 'algorithm-arena-intro.gif'
    poster = media / 'algorithm-arena-intro-still.png'
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='arena-intro-') as temporary:
        options = {'pixel_width': 720, 'pixel_height': 720,
                   'frame_width': 8, 'frame_height': 8, 'frame_rate': 25,
                   'media_dir': temporary, 'output_file': 'intro',
                   'disable_caching': True, 'verbosity': 'WARNING',
                   'progress_bar': 'none', 'format': 'mp4'}
        with register_font(str(FONT_DIR / 'cmunrm.ttf')), \
                register_font(str(FONT_DIR / 'cmunti.ttf')), tempconfig(options):
            scene = AlgorithmArenaIntro()
            scene.render()
            video = Path(scene.renderer.file_writer.movie_file_path)
        render_seconds = time.perf_counter() - started
        # Palette generation retains antialiased CMR edges without enormous GIFs.
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video),
                        '-filter_complex',
                        '[0:v]split[a][b];[a]palettegen=stats_mode=full[p];[b][p]paletteuse=dither=sierra2_4a',
                        '-loop', '0', str(output)], check=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(video),
                        '-frames:v', '1', str(poster)], check=True)
    from PIL import Image
    with Image.open(output) as gif:
        durations = []
        for frame in range(gif.n_frames):
            gif.seek(frame)
            durations.append(gif.info['duration'])
        metadata = {'engine': 'Manim Community Edition', 'scene': 'AlgorithmArenaIntro',
                    'text': 'Algorithm Arena', 'size': gif.size, 'frames': gif.n_frames,
                    'loop': gif.info.get('loop'), 'duration_seconds': sum(durations)/1000,
                    'fps': 1000/durations[0], 'render_seconds': round(render_seconds,2),
                    'total_seconds': round(time.perf_counter()-started,2),
                    'bytes': output.stat().st_size, 'file': str(output.relative_to(ROOT))}
    evidence = ROOT / 'artifacts/renders/intro'
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / 'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps(metadata,indent=2))


if __name__ == '__main__':
    main()

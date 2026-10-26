"""Run genuine scenes without overwriting retained release media."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'renderer/renders/verification'
OUT.mkdir(parents=True, exist_ok=True)
env = {**os.environ, 'PYTHONPATH': str(ROOT / 'renderer')}
measurements = []
for name, scene, values in [
    ('custom-52413', 'custom', [5,2,4,1,3]),
    ('custom-83726', 'custom', [8,3,7,2,6]),
    ('tutorial', 'tutorial', None),
    ('worst10', 'custom', list(range(10,0,-1))),
    ('worst10-warm', 'custom', list(range(10,0,-1))),
    ('custom-52413-warm', 'custom', [5,2,4,1,3]),
]:
    job, video = OUT / f'{name}.json', OUT / f'{name}.mp4'
    job.write_text(json.dumps({'scene':scene, 'values':values}))
    started = time.perf_counter()
    p = subprocess.run([sys.executable, '-m', 'arena.render', str(job), str(video)],
                       cwd=ROOT / 'renderer', env=env, capture_output=True, text=True, timeout=300)
    (OUT / f'{name}.log').write_text(p.stdout + p.stderr)
    if p.returncode:
        raise RuntimeError(p.stderr[-3000:])
    meta = json.loads(p.stdout.strip().splitlines()[-1])
    meta['wall_seconds'] = round(time.perf_counter()-started, 2)
    info = subprocess.run(['ffprobe','-v','error','-show_entries',
                          'stream=codec_name,width,height,r_frame_rate,pix_fmt:format=duration,size',
                          '-of','json',str(video)], check=True, capture_output=True, text=True)
    meta['probe'] = json.loads(info.stdout)
    subprocess.run(['ffmpeg','-v','error','-i',str(video),'-f','null','-'],check=True)
    meta['name'] = name
    measurements.append(meta)
    (OUT / 'measurements.json').write_text(json.dumps(measurements, indent=2))
    print(json.dumps(meta), flush=True)

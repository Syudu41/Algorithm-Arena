"""Render real Merge Sort proofs; only tutorial/poster are public release assets.

PATH="$PWD/.venv-manim/bin:$PATH" .venv-manim/bin/python scripts/render_merge.py
Add --stress for a ten-item boundary/duplicate render. All custom media and raw
proof stay in ignored artifacts/renders/merge/; no public evidence archive.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/renders/merge'
WORK=OUT/'work'


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'stream=codec_name,width,height,r_frame_rate,pix_fmt:format=duration,size',
        '-of','json',str(path)],text=True))


def still(video,path,when):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(when),'-i',str(video),
                    '-frames:v','1',str(path)],check=True)


def run(name,scene,values,path):
    job=WORK/f'{name}.json';job.write_text(json.dumps({'scene':scene,'values':values}))
    started=time.perf_counter()
    process=subprocess.run([sys.executable,'-m','arena.render',str(job),str(path)],cwd=ROOT,
        env={**os.environ,'PYTHONPATH':str(ROOT/'renderer')},capture_output=True,text=True,timeout=300)
    (WORK/f'{name}.log').write_text(process.stdout+process.stderr)
    if process.returncode:raise RuntimeError(process.stderr[-3000:])
    metadata=json.loads(process.stdout.strip().splitlines()[-1])
    metadata.update(name=name,wall_seconds=round(time.perf_counter()-started,2),probe=probe(path))
    subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
    metadata['decode']='PASS'
    stream=metadata['probe']['streams'][0]
    assert (stream['codec_name'],stream['width'],stream['height'],stream['r_frame_rate'],stream['pix_fmt'])==('h264',1280,720,'30/1','yuv420p')
    (OUT/f'{name}-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({k:v for k,v in metadata.items() if k!='timeline'}),flush=True)
    return metadata


def capture(metadata,path,values,tutorial=False):
    from arena.merge import Compare,Complete,MergeComplete,MergeStart,Split,Write,merge_trace
    trace=merge_trace(values);timeline=metadata['timeline'];name=metadata['name']
    duration=float(metadata['probe']['format']['duration'])
    frames={'initial':2.6,'final':duration-.3}
    for label,kind in [('split',Split),('runs',MergeStart),('compare',Compare),('mid-write',Write),('merged',MergeComplete)]:
        k=next(i for i,e in enumerate(trace.events) if isinstance(e,kind))
        beat=timeline[k]
        frames[label]=(beat['start']+beat['end'])/2 if label=='mid-write' else beat['end']-.03
    k=next(i for i,e in enumerate(trace.events) if isinstance(e,Write) and e.remainder)
    frames['remainder']=timeline[k]['end']-.03
    # Final six/ten-wide merge verifies the widest two-run and output layouts.
    k=next(i for i,e in enumerate(trace.events) if isinstance(e,MergeStart) and e.lo==0 and e.hi==len(values))
    frames['full-runs']=timeline[k]['end']-.03
    first_compare=next(i for i in range(k+1,len(trace.events)) if isinstance(trace.events[i],Compare))
    frames['full-compare']=timeline[first_compare]['end']-.03
    deepest=max((i for i,e in enumerate(trace.events) if isinstance(e,Split)),key=lambda i:trace.events[i].depth)
    frames['deepest-split']=timeline[deepest]['end']-.03
    equal=next((i for i,e in enumerate(trace.events) if isinstance(e,Compare) and e.left==e.right),None)
    if equal is not None:frames['equal-left-first']=timeline[equal]['end']-.03
    for label,when in frames.items():still(path,OUT/f'{name}-{label}.png',when)
    if tutorial:still(path,ROOT/'media/merge-poster.png',frames['full-compare'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stress',action='store_true')
    args=parser.parse_args()
    WORK.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(ROOT/'renderer'))
    cases=[('custom-52413','merge_custom',[5,2,4,1,3],OUT/'custom-52413.mp4'),
           ('custom-83726','merge_custom',[8,3,7,2,6],OUT/'custom-83726.mp4'),
           ('tutorial','merge_tutorial',[4,1,6,2,5,3],ROOT/'media/merge-tutorial.mp4')]
    if args.stress:
        cases.append(('stress-ten','merge_custom',[-99,99,0,-99,5,5,-1,99,0,2],OUT/'stress-ten.mp4'))
    rows=[]
    for name,scene,values,path in cases:
        metadata=run(name,scene,values,path)
        duration=float(metadata['probe']['format']['duration'])
        if scene=='merge_tutorial':assert 45<=duration<=60,('tutorial duration',duration)
        elif len(values)==5:assert 12<=duration<=30,('custom duration',duration)
        capture(metadata,path,values,tutorial=scene=='merge_tutorial')
        rows.append(metadata)
        (OUT/'measurements.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()

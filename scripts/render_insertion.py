"""Render/probe real Insertion Sort proofs without touching Bubble assets.

PATH="$PWD/.venv-manim/bin:$PATH" .venv-manim/bin/python scripts/render_insertion.py
Add --benchmarks for repeated five-item and first/repeated worst-ten renders.
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
WORK=ROOT/'renderer/renders/insertion'
EVIDENCE=ROOT/'docs/evidence/insertion'


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'stream=codec_name,width,height,r_frame_rate,pix_fmt:format=duration,size',
        '-of','json',str(path)],text=True))


def still(video,path,when):
    subprocess.run(['ffmpeg','-v','error','-y','-ss',str(when),'-i',str(video),
                    '-frames:v','1',str(path)],check=True)


def run(name,scene,values,out):
    job=WORK/f'{name}.json';job.write_text(json.dumps({'scene':scene,'values':values}))
    started=time.perf_counter()
    process=subprocess.run([sys.executable,'-m','arena.render',str(job),str(out)],
        cwd=ROOT/'renderer',env={**os.environ,'PYTHONPATH':str(ROOT/'renderer')},
        capture_output=True,text=True,timeout=300)
    (WORK/f'{name}.log').write_text(process.stdout+process.stderr)
    if process.returncode:raise RuntimeError(process.stderr[-3000:])
    metadata=json.loads(process.stdout.strip().splitlines()[-1])
    metadata['wall_seconds']=round(time.perf_counter()-started,2)
    metadata['probe']=probe(out)
    metadata['name']=name
    metadata['values']=values
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    metadata['decode']='PASS'
    (EVIDENCE/f'{name}-metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print(json.dumps({k:v for k,v in metadata.items() if k!='timeline'}),flush=True)
    return metadata


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmarks',action='store_true')
    args=parser.parse_args()
    WORK.mkdir(parents=True,exist_ok=True);EVIDENCE.mkdir(parents=True,exist_ok=True)
    rows=[]
    cases=[('custom-52413','insertion_custom',[5,2,4,1,3],ROOT/'media/insertion-custom-52413.mp4'),
           ('custom-83726','insertion_custom',[8,3,7,2,6],ROOT/'media/insertion-custom-83726.mp4'),
           ('tutorial','insertion_tutorial',[4,1,6,2,5,3],ROOT/'media/insertion-tutorial.mp4')]
    sys.path.insert(0,str(ROOT/'renderer'))
    from arena.insertion import Compare,PassComplete,SelectKey,Shift,insertion_trace
    for name,scene,values,out in cases:
        metadata=run(name,scene,values,out);rows.append(metadata)
        trace=insertion_trace(values)
        duration=float(metadata['probe']['format']['duration'])
        if scene=='insertion_custom' and not 12<=duration<=30:raise RuntimeError('custom timing contract failed')
        if scene=='insertion_tutorial' and not 35<=duration<=60:raise RuntimeError('tutorial timing contract failed')
        timeline=metadata['timeline']
        selections={'lift':SelectKey,'shift':Shift,'prefix':PassComplete}
        frames={'initial':2.6,'final':duration-.4}
        for label,kind in selections.items():
            k=next(i for i,e in enumerate(trace.events) if isinstance(e,kind))
            beat=timeline[k]
            frames[label]=(beat['start']+beat['end'])/2 if label!='prefix' else beat['end']-.03
        for label,condition in [('compare',True),('keep',False)]:
            k=next(i for i,e in enumerate(trace.events) if isinstance(e,Compare) and e.shift==condition)
            beat=timeline[k];frames[label]=beat['end']-.03
        for label,when in frames.items():still(out,EVIDENCE/f'{name}-{label}.png',when)
        if scene=='insertion_tutorial':
            still(out,ROOT/'media/insertion-poster.png',frames['compare'])
        (EVIDENCE/'measurements.json').write_text(json.dumps(rows,indent=2)+'\n')
    if args.benchmarks:
        for name,values in [('custom-52413-warm',[5,2,4,1,3]),
                            ('worst10',list(range(10,0,-1))),('worst10-warm',list(range(10,0,-1)))]:
            rows.append(run(name,'insertion_custom',values,WORK/f'{name}.mp4'))
            (EVIDENCE/'measurements.json').write_text(json.dumps(rows,indent=2)+'\n')


if __name__=='__main__':main()

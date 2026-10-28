"""Measure actual local API cache misses/hits separately from MP4 duration."""
import json
import time
from urllib.request import Request, urlopen
from pathlib import Path

base='http://127.0.0.1:8765'
output=Path(__file__).resolve().parents[1]/'artifacts/benchmarks/api.json'
output.parent.mkdir(parents=True,exist_ok=True)
rows=[]
for values in ([8,3,7,2,6],list(range(10,0,-1))):
 for repeat in range(2):
  started=time.perf_counter()
  request=Request(base+'/api/renders',data=json.dumps({'algorithm':'bubble','values':values}).encode(),headers={'Content-Type':'application/json'})
  with urlopen(request,timeout=10) as response: job=json.load(response)
  initial_cached=job['cached']
  while job['status'] in ('queued','rendering'):
   time.sleep(.25)
   with urlopen(base+'/api/renders/'+job['id'],timeout=10) as response: job=json.load(response)
  if job['status']!='ready': raise RuntimeError(job)
  rows.append({'values':values,'repeat':repeat,'cache_hit':initial_cached,
               'request_to_ready_seconds':round(time.perf_counter()-started,4),'metadata':job})
  output.write_text(json.dumps(rows,indent=2))
  print(json.dumps(rows[-1]),flush=True)

import json
from pathlib import Path
import subprocess
import sys
import threading
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer

import pytest

from arena.service import BusyError, RenderJobs, make_handler
from arena.validation import InputError


def wait_for(jobs, ident):
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        result = jobs.get(ident)
        if result['status'] not in ('queued', 'rendering'):
            return result
        time.sleep(.02)
    pytest.fail('job did not finish')


@pytest.mark.parametrize('payload', [None, {}, {'algorithm':'race','values':[1,2]},
    {'algorithm':'bubble','values':[True,2]}, {'algorithm':'bubble','values':[1,100]},
    {'algorithm':'bubble','values':[1,2],'scene':'untrusted'}])
def test_validation_before_spawn(tmp_path, payload):
    jobs = RenderJobs(tmp_path)
    with pytest.raises(InputError):
        jobs.submit(payload)
    assert not jobs.jobs


def test_bounded_queue_and_exact_pending_cache(tmp_path, monkeypatch):
    jobs = RenderJobs(tmp_path, capacity=1)
    monkeypatch.setattr(jobs, '_command', lambda *_: [sys.executable,'-c','import time; time.sleep(.3); raise SystemExit(1)'])
    a = jobs.submit({'algorithm':'bubble','values':[2,1]})
    assert jobs.submit({'algorithm':'bubble','values':[2,1]})['id'] == a['id']
    with pytest.raises(BusyError):
        jobs.submit({'algorithm':'bubble','values':[3,1]})
    assert wait_for(jobs,a['id'])['status'] == 'failed'
    assert jobs.slots.acquire(blocking=False)


def test_timeout_is_terminal_and_releases_capacity(tmp_path, monkeypatch):
    jobs = RenderJobs(tmp_path, timeout=.05, capacity=1)
    monkeypatch.setattr(jobs, '_command', lambda *_: [sys.executable,'-c','import time; time.sleep(10)'])
    result = jobs.submit({'algorithm':'bubble','values':[2,1]})
    assert wait_for(jobs,result['id'])['status'] == 'timed_out'
    assert jobs.slots.acquire(blocking=False)


def test_persistent_cache_and_normalization(tmp_path):
    from arena.service import FINGERPRINT
    jobs = RenderJobs(tmp_path)
    import hashlib
    values = [2,1]
    ident = hashlib.sha256(json.dumps([FINGERPRINT, values]).encode()).hexdigest()[:32]
    (tmp_path / f'{ident}.json').write_text(json.dumps({'id':ident,'status':'ready',
        'initial':values,'fingerprint':FINGERPRINT}))
    (tmp_path / f'{ident}.mp4').write_bytes(b'fixture')
    assert jobs.submit({'algorithm':'bubble','values':values})['cached'] is True
    assert jobs.get('../../etc/passwd') is None


def test_http_bounds_origin_paths_and_video_ranges(tmp_path):
    static = tmp_path / 'dist'
    static.mkdir()
    (static / 'index.html').write_text('Explore')
    jobs = RenderJobs(tmp_path / 'jobs')
    server = ThreadingHTTPServer(('127.0.0.1',0),make_handler(jobs,static))
    thread = threading.Thread(target=server.serve_forever,daemon=True)
    thread.start()
    base = f'http://127.0.0.1:{server.server_port}'
    try:
        assert urlopen(base+'/').read() == b'Explore'
        assert b'renderApi: ""' in urlopen(base+'/config.js').read()
        for path in ['/../service.py','/%2e%2e/service.py','/api/videos/../../etc/passwd','/api/renders/nope','/api/unknown']:
            with pytest.raises(HTTPError) as exc:
                urlopen(base+path)
            assert exc.value.code == 404
        req = Request(base+'/api/renders',data=b'{"algorithm":"bubble","values":[1,100]}',headers={'Content-Type':'application/json'})
        with pytest.raises(HTTPError) as exc:
            urlopen(req)
        assert exc.value.code == 400
        req.add_header('Origin','https://untrusted.example')
        with pytest.raises(HTTPError) as exc:
            urlopen(req)
        assert exc.value.code == 403
        ident='a'*32
        jobs.jobs[ident]={'id':ident,'status':'ready'}
        (jobs.output/f'{ident}.mp4').write_bytes(b'0123456789')
        response=urlopen(Request(base+f'/api/videos/{ident}.mp4',headers={'Range':'bytes=2-5'}))
        assert response.status == 206 and response.read() == b'2345'
        assert response.headers['Content-Range'] == 'bytes 2-5/10'
    finally:
        server.shutdown()
        server.server_close()
        thread.join()

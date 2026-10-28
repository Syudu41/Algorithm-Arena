"""Loopback-only Explore server: static site + bounded, trusted Manim jobs.

Run from repository root: PYTHONPATH=renderer .venv-manim/bin/python -m arena.service
"""
from __future__ import annotations

import argparse
from collections import OrderedDict
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import threading
import time
from urllib.parse import unquote, urlsplit

from .bubble import bubble_trace
from .render import RENDERER_VERSION
from .validation import InputError, validate_values

ROOT = Path(__file__).resolve().parents[2]
KEY = re.compile(r'[a-f0-9]{32}')
SCENE_KEYS = {'bubble': 'custom', 'insertion': 'insertion_custom'}
# Cache changes with trusted sources/fonts as well as explicit renderer version.
FINGERPRINT = hashlib.sha256(RENDERER_VERSION.encode() + b''.join(
    p.read_bytes() for p in sorted((ROOT / 'renderer/arena').glob('*.py'))
) + b''.join(p.read_bytes() for p in sorted((ROOT / 'renderer/fonts').glob('*.ttf')))).hexdigest()


class BusyError(Exception):
    pass


class RenderJobs:
    def __init__(self, output: Path, timeout: float = 300, capacity: int = 4):
        self.output = output.resolve()
        self.output.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        self.capacity = capacity
        self.jobs: OrderedDict[str, dict] = OrderedDict()
        self.lock = threading.Lock()
        self.slots = threading.BoundedSemaphore(capacity)
        self.worker = threading.Lock()  # exactly one Manim process

    def submit(self, payload):
        if not isinstance(payload, dict) or set(payload) != {'algorithm', 'values'} or payload['algorithm'] not in ('bubble', 'insertion'):
            raise InputError('send algorithm "bubble" or "insertion" and values only')
        values = validate_values(payload['values'])
        algorithm = payload['algorithm']
        if algorithm == 'bubble':
            trace = bubble_trace(values)
            operations = {'swaps': trace.swaps}
        else:
            from .insertion import insertion_trace
            trace = insertion_trace(values)
            operations = {'shifts': trace.shifts, 'placements': trace.placements}
        ident = hashlib.sha256(json.dumps([FINGERPRINT, algorithm, values]).encode()).hexdigest()[:32]
        with self.lock:
            existing = self.jobs.get(ident)
            if existing and existing['status'] in ('queued', 'rendering'):
                return dict(existing)
            meta_path, video = self.output / f'{ident}.json', self.output / f'{ident}.mp4'
            if meta_path.is_file() and video.is_file():
                try:
                    result = json.loads(meta_path.read_text())
                    if result['initial'] == values and result['fingerprint'] == FINGERPRINT and result['algorithm'] == algorithm:
                        result['cached'] = True
                        return result
                except (ValueError, KeyError):
                    pass
            if not self.slots.acquire(blocking=False):
                raise BusyError('Render queue is full. Try again after a job finishes.')
            result = {'id': ident, 'status': 'queued', 'initial': values,
                      'final': list(trace.final), 'comparisons': trace.comparisons,
                      'algorithm': algorithm, **operations, 'cached': False, 'fingerprint': FINGERPRINT}
            # Bounded in-memory history; persistent completed videos remain cached.
            if len(self.jobs) >= 100:
                for old in list(self.jobs):
                    if self.jobs[old]['status'] not in ('queued', 'rendering'):
                        del self.jobs[old]
                        break
            self.jobs[ident] = result
            threading.Thread(target=self._run, args=(ident,), daemon=True).start()
            return dict(result)

    def get(self, ident):
        if not KEY.fullmatch(ident):
            return None
        with self.lock:
            if ident in self.jobs:
                return dict(self.jobs[ident])
        path = self.output / f'{ident}.json'
        if path.is_file():
            return json.loads(path.read_text())
        return None

    def _update(self, ident, **data):
        with self.lock:
            self.jobs[ident].update(data)

    def _command(self, job, video):
        return [sys.executable, '-m', 'arena.render', str(job), str(video)]

    def _run(self, ident):
        try:
            with self.worker:
                self._update(ident, status='rendering')
                job = self.output / f'{ident}.input.json'
                video = self.output / f'{ident}.mp4'
                request = self.get(ident)
                job.write_text(json.dumps({'scene': SCENE_KEYS[request['algorithm']], 'values': request['initial']}))
                started = time.perf_counter()
                with subprocess.Popen(self._command(job, video), cwd=ROOT / 'renderer',
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      text=True, start_new_session=True) as process:
                    try:
                        stdout, stderr = process.communicate(timeout=self.timeout)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.communicate()
                        self._update(ident, status='timed_out', error='Render exceeded the configured time limit. Try a shorter array.')
                        return
                    if process.returncode:
                        (self.output / f'{ident}.log').write_text(stderr[-8000:])
                        raise RuntimeError('Manim could not render this array. See the local server log.')
                meta = json.loads(stdout.strip().splitlines()[-1])
                import av
                with av.open(str(video)) as media:
                    stream = media.streams.video[0]
                    info = {'duration_seconds': round(media.duration / 1_000_000, 3),
                            'width': stream.width, 'height': stream.height,
                            'fps': float(stream.average_rate), 'codec': stream.codec_context.name}
                self._update(ident, status='ready', video_url=f'/api/videos/{ident}.mp4',
                             render_seconds=meta['render_seconds'],
                             wall_seconds=round(time.perf_counter()-started, 2),
                             bytes=video.stat().st_size, **info)
                target = self.output / f'{ident}.json'
                temporary = target.with_suffix('.tmp')
                temporary.write_text(json.dumps(self.get(ident)))
                temporary.replace(target)
        except Exception as exc:
            self._update(ident, status='failed', error=str(exc))
        finally:
            self.slots.release()


def make_handler(jobs, static_dir):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(static_dir), **kwargs)

        def end_headers(self):
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Cross-Origin-Resource-Policy', 'same-origin')
            super().end_headers()

        def json_response(self, status, data):
            body = json.dumps(data).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            # Block cross-site requests and DNS rebinding. This is a local demo server.
            host = self.headers.get('Host', '')
            allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
            origin = self.headers.get('Origin')
            if host not in allowed or (origin and origin != f'http://{host}'):
                return self.json_response(403, {'error': 'Use the local same-origin demo page.'})
            if self.path != '/api/renders':
                return self.json_response(404, {'error': 'Unknown route'})
            try:
                if self.headers.get('Content-Type', '').split(';')[0] != 'application/json':
                    raise InputError('Content-Type must be application/json')
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 2048:
                    raise InputError('Request body must be 1–2048 bytes')
                self.connection.settimeout(5)
                result = jobs.submit(json.loads(self.rfile.read(size)))
                self.json_response(200 if result['status'] == 'ready' else 202, result)
            except (InputError, ValueError, UnicodeError) as exc:
                self.json_response(400, {'error': str(exc)})
            except BusyError as exc:
                self.json_response(429, {'error': str(exc)})

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == '/config.js':
                body = b'window.ARENA_CONFIG = {renderApi: ""};'
                self.send_response(200)
                self.send_header('Content-Type', 'text/javascript')
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(body)
                return
            if path.startswith('/api/renders/'):
                result = jobs.get(path.removeprefix('/api/renders/'))
                return self.json_response(200 if result else 404, result or {'error': 'Job not found'})
            if path.startswith('/api/videos/'):
                name = path.removeprefix('/api/videos/')
                ident = name.removesuffix('.mp4')
                result = jobs.get(ident)
                if not name.endswith('.mp4') or not result or result['status'] != 'ready':
                    return self.json_response(404, {'error': 'Video not ready'})
                return self.video(jobs.output / name)
            # No API fallthrough or directory listings / source exposure.
            candidate = (static_dir / unquote(path).lstrip('/')).resolve()
            if not candidate.is_relative_to(static_dir.resolve()) or not candidate.is_file() and path != '/':
                return self.send_error(404)
            if path == '/':
                self.path = '/index.html'
            return super().do_GET()

        def video(self, path):
            size = path.stat().st_size
            start, end = 0, size-1
            range_header = self.headers.get('Range')
            if range_header:
                match = re.fullmatch(r'bytes=(\d*)-(\d*)', range_header)
                if not match or not any(match.groups()):
                    return self.send_error(416)
                a, b = match.groups()
                if a:
                    start, end = int(a), min(int(b), size-1) if b else size-1
                else:
                    start = max(0, size-int(b))
                if start > end or start >= size:
                    return self.send_error(416)
            self.send_response(206 if range_header else 200)
            self.send_header('Content-Type', 'video/mp4')
            self.send_header('Accept-Ranges', 'bytes')
            self.send_header('Content-Length', str(end-start+1))
            if range_header:
                self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
            self.end_headers()
            with path.open('rb') as file:
                file.seek(start)
                remaining = end-start+1
                while remaining:
                    chunk = file.read(min(65536, remaining))
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    remaining -= len(chunk)

        def do_HEAD(self):
            # Only static files; API videos use GET with byte ranges.
            if self.path.startswith('/api/'):
                return self.send_error(405)
            candidate = (static_dir / unquote(urlsplit(self.path).path).lstrip('/')).resolve()
            if not candidate.is_relative_to(static_dir.resolve()) or not candidate.is_file():
                return self.send_error(404)
            super().do_HEAD()
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--timeout', type=float, default=300)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('timeout must be positive')
    static = ROOT / 'dist'
    if not (static / 'index.html').is_file():
        parser.error('Build the site first: node scripts/build.mjs')
    jobs = RenderJobs(ROOT / 'renderer/renders/jobs', timeout=args.timeout)
    server = ThreadingHTTPServer(('127.0.0.1', args.port), make_handler(jobs, static))
    print(f'Explore local demo: http://127.0.0.1:{args.port}/#/about', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()

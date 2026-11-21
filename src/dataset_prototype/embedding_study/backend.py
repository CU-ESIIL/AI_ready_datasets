"""Process-isolated access to two pinned Fire VASE capabilities; no fallback."""
import json
import os
from pathlib import Path
import select
import subprocess
from time import perf_counter_ns
from .contracts import PIN, UPSTREAM_SHA256


class UpstreamBackend:
    """Caller chooses a trusted installation; runtime models never choose paths/code."""
    def __init__(self, upstream, python):
        self.upstream = Path(upstream).resolve()
        head = subprocess.check_output(['git','-C',str(self.upstream),'rev-parse','HEAD'], text=True).strip()
        if head != PIN:
            raise ValueError('Fire VASE checkout differs from pinned commit')
        self.checkout_status = subprocess.check_output(['git','-C',str(self.upstream),'status','--porcelain'], text=True)
        self.compute_ns = self.ipc_bytes = self.calls = 0
        self.peak_rss_bytes = 0
        env = {'PATH':os.environ.get('PATH','/usr/bin:/bin'), 'LANG':'en_US.UTF-8',
            'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1',
            'GIT_NO_LAZY_FETCH':'1','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'}
        started = perf_counter_ns()
        self.process = subprocess.Popen([str(Path(python).absolute()), str(Path(__file__).with_name('worker.py')), str(self.upstream)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env, bufsize=1)
        try:
            hello = self._read()
            if hello.get('commit') != PIN or hello.get('sha256') != UPSTREAM_SHA256 or hello.get('ready') is not True:
                raise ValueError('upstream handshake failed')
            self.versions = hello['versions']
            self.startup_ns = perf_counter_ns()-started
        except BaseException:
            self.close()
            raise

    def _read(self):
        if not select.select([self.process.stdout], [], [], 30)[0]:
            raise TimeoutError('upstream worker timed out; no mock fallback')
        line = self.process.stdout.readline(1_000_001)
        if not line:
            # Worker stderr has no forwarded credentials; preserve a bounded failure.
            error = self.process.stderr.read(4000) if self.process.poll() is not None else ''
            raise RuntimeError('upstream worker failed: '+error)
        if len(line) > 1_000_000:
            raise ValueError('worker response exceeds bound')
        self.ipc_bytes += len(line.encode())
        return json.loads(line)

    def call(self, operation, values):
        if operation not in {'features','fit_pca','pulses'}:
            raise ValueError('unknown upstream capability')
        line = json.dumps({'operation':operation,'input':values}, allow_nan=False, separators=(',',':'))+'\n'
        if len(line) > 1_000_000:
            raise ValueError('request too large')
        self.process.stdin.write(line); self.process.stdin.flush()
        self.ipc_bytes += len(line.encode()); self.calls += 1
        result = self._read()
        self.compute_ns += result.get('compute_ns',0)
        self.peak_rss_bytes = max(self.peak_rss_bytes,result.get('worker_peak_rss_bytes',0))
        if result.get('ok') is not True:
            raise ValueError(f"upstream {result.get('error_type')}: {result.get('error')}")
        return result['result']

    def close(self):
        p = self.process
        if p.stdin:
            p.stdin.close()
        try:
            p.wait(timeout=3)
        except subprocess.TimeoutExpired:
            p.kill(); p.wait()
        for stream in (p.stdout,p.stderr):
            if stream:
                stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

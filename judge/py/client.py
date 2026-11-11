"""Synchronous client for the judge's Python zygote."""

import json
import os
import signal
import subprocess
import sys
import threading
from pathlib import Path

CAP_MS = 30_000
STDOUT_BYTES = 16 << 10
MAX_CODE_BYTES = 64 << 10
ADDRESS_SPACE_MB = 704
WALL_SECONDS = 120
SANDBOX_UID_START = 61_001
ZYGOTE = Path(__file__).with_name("zygote.py")


class ZygoteClient:
    def __init__(self, uid: int) -> None:
        self.uid = uid
        self.process: subprocess.Popen | None = None

    def __enter__(self):
        self._start()
        return self

    def _start(self) -> None:
        self._stop()
        env = {**os.environ, "JUDGE_SANDBOX_UID": str(self.uid)}
        self.process = subprocess.Popen(
            [sys.executable, str(ZYGOTE)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=env
        )
        try:
            if self.process.stdin is None or self.process.stdout is None:
                raise RuntimeError("zygote pipes are unavailable")
            if not json.loads(self.process.stdout.readline()).get("ready"):
                raise RuntimeError("zygote did not become ready")
        except json.JSONDecodeError, RuntimeError:
            self._stop()
            raise RuntimeError("zygote did not become ready") from None

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._stop()

    def _stop(self) -> None:
        if self.process is None:
            return
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        if self.process.stdin:
            self.process.stdin.close()
        if self.process.stdout:
            self.process.stdout.close()
        self.process = None

    def _validate_code(self, code: str) -> None:
        if len(code.encode()) > MAX_CODE_BYTES:
            raise ValueError(f"solution exceeds {MAX_CODE_BYTES} bytes")

    def run(self, job: dict) -> list[dict]:
        if self.process is None or self.process.poll() is not None:
            self._start()
        process = self.process
        assert process is not None
        if process.stdin is None or process.stdout is None:
            raise RuntimeError("zygote pipes are unavailable")
        self._validate_code(job["code"])
        process.stdin.write(json.dumps(job).encode() + b"\n")
        process.stdin.flush()
        events = []
        timer = None
        try:
            while line := process.stdout.readline():
                event = json.loads(line)
                events.append(event)
                if "pid" in event:
                    timer = threading.Timer(WALL_SECONDS, os.kill, (event["pid"], signal.SIGKILL))
                    timer.start()
                if "done" in event or "fatal" in event:
                    return events
        finally:
            if timer:
                timer.cancel()
        raise RuntimeError("zygote exited")

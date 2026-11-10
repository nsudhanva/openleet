"""Runs every reference solution of every work item through the zygote (the judge's own
sandbox, so the same conversion and limits as a real submission) and records what each one
printed for each test. openleet.judging.assemble decides what to keep.

Usage (inside the judge image, as root, without network):
    python vote.py WORK_DIR RESULTS_DIR [JOBS]
"""

import json
import os
import signal
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ZYGOTE = Path(__file__).with_name("zygote.py")
LIMITS = {"cpu_s": 30, "as_mb": 3072, "out_bytes": 512 << 20, "stdout_bytes": 0}
WALL_SECONDS = 120

# References may print integers longer than CPython's default 4300-digit limit; vote.py and
# stress.py both parse those events.
sys.set_int_max_str_digits(0)


class Zygote:
    """One zygote process, driven synchronously."""

    def __init__(self, uid: int) -> None:
        env = {**os.environ, "JUDGE_SANDBOX_UID": str(uid)}
        self.process = subprocess.Popen(
            [sys.executable, str(ZYGOTE)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=env
        )
        # Both are pipes, as requested above.
        assert self.process.stdin and self.process.stdout
        self.stdin, self.stdout = self.process.stdin, self.process.stdout
        assert json.loads(self.stdout.readline())["ready"]

    def run(self, job: dict) -> list[dict]:
        self.stdin.write(json.dumps(job).encode() + b"\n")
        self.stdin.flush()
        events, timer = [], None
        try:
            while line := self.stdout.readline():
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


local = threading.local()
next_uid = iter(range(61_001, 62_000))
uid_lock = threading.Lock()


def zygote() -> Zygote:
    """This worker thread's zygote, with a sandbox user of its own."""
    if getattr(local, "uid", None) is None:
        with uid_lock:
            local.uid = next(next_uid)
    if getattr(local, "zygote", None) is None or local.zygote.process.poll() is not None:
        local.zygote = Zygote(local.uid)
    return local.zygote


def outcomes(events: list[dict], count: int) -> tuple[list, int, str | None]:
    """Per-test results (None where the run never got), total CPU ms, and a run-level error."""
    results: list = [None] * count
    cpu, error = 0, None
    for event in events:
        if "ev" in event:
            ev = event["ev"]
            if "i" in ev:
                results[ev["i"]] = (
                    {"out": ev["out"]} if "out" in ev else {"error": ev.get("error", "MLE")}
                )
            else:
                error = ev.get("compile") or ev.get("sandbox")
        elif "done" in event:
            cpu = event["done"]["cpu_ms"]
            if event["done"]["signal"]:
                error = error or f"killed by signal {event['done']['signal']}"
        elif "fatal" in event:
            error = event["fatal"]
    return results, cpu, error


def ballots(spec: dict, codes: dict[str, str], tests: list[dict], limits: dict) -> dict:
    """What each named reference printed for every test, its CPU ms, and any run-level error."""
    voters = {}
    for name, code in codes.items():
        job = {"spec": spec, "code": code, "tests": tests, "limits": limits, "keep_going": True}
        try:
            results, cpu, error = outcomes(zygote().run(job), len(tests))
        except (RuntimeError, OSError, ValueError) as failure:
            results, cpu, error = [None] * len(tests), 0, repr(failure)
        voters[name] = {"results": results, "cpuMs": cpu, "error": error}
    return voters


def vote(item: dict, results_dir: Path) -> None:
    tests = [{"input": e["input"]} for e in item["examples"]]
    tests += [{"input": i} for i in item["inputs"]]
    voters = ballots(item["spec"], item["voters"], tests, LIMITS)
    (results_dir / f"{item['slug']}.json").write_text(
        json.dumps({"slug": item["slug"], "voters": voters})
    )


def main() -> None:
    work, results = Path(sys.argv[1]), Path(sys.argv[2])
    jobs = int(sys.argv[3]) if len(sys.argv) > 3 else os.cpu_count() or 1
    results.mkdir(parents=True, exist_ok=True)
    items = [json.loads(p.read_text()) for p in sorted(work.glob("*.json"))]
    todo = [i for i in items if i["supported"] and not (results / f"{i['slug']}.json").exists()]
    print(f"Voting on {len(todo)} problems with {jobs} workers", flush=True)
    done = 0
    with ThreadPoolExecutor(jobs) as pool:
        for _ in pool.map(lambda item: vote(item, results), todo):
            done += 1
            if done % 50 == 0:
                print(f"  {done}/{len(todo)}", flush=True)


if __name__ == "__main__":
    main()

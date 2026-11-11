"""Runs every reference solution of every work item through the zygote (the judge's own
sandbox, so the same conversion and limits as a real submission) and records what each one
printed for each test. openleet.judging.assemble decides what to keep.

Usage (inside the judge image, as root, without network):
    python vote.py WORK_DIR RESULTS_DIR [JOBS]
"""

import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from client import ADDRESS_SPACE_MB, CAP_MS, SANDBOX_UID_START, ZygoteClient

LIMITS = {
    "cpu_s": CAP_MS // 1000,
    "as_mb": ADDRESS_SPACE_MB,
    "out_bytes": 512 << 20,
    "stdout_bytes": 0,
}

# References may print integers longer than CPython's default 4300-digit limit; vote.py and
# stress.py both parse those events.
sys.set_int_max_str_digits(0)


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


def ballots(
    spec: dict,
    codes: dict[str, str],
    tests: list[dict],
    limits: dict,
    client: ZygoteClient,
) -> dict:
    """What each named reference printed for every test, its CPU ms, and any run-level error."""
    voters = {}
    for name, code in codes.items():
        job = {"spec": spec, "code": code, "tests": tests, "limits": limits, "keep_going": True}
        try:
            results, cpu, error = outcomes(client.run(job), len(tests))
        except (RuntimeError, OSError, ValueError) as failure:
            results, cpu, error = [None] * len(tests), 0, repr(failure)
        voters[name] = {"results": results, "cpuMs": cpu, "error": error}
    return voters


def vote(item: dict, results_dir: Path, client: ZygoteClient) -> None:
    tests = [{"input": e["input"]} for e in item["examples"]]
    tests += [{"input": i} for i in item["inputs"]]
    voters = ballots(item["spec"], item["voters"], tests, LIMITS, client)
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
    workers = min(max(1, jobs), len(todo))
    chunks = [(i, todo[i::workers]) for i in range(workers)]
    done = 0
    lock = threading.Lock()

    def run_chunk(chunk: tuple[int, list[dict]]) -> None:
        nonlocal done
        worker, items = chunk
        with ZygoteClient(SANDBOX_UID_START + worker) as client:
            for item in items:
                vote(item, results, client)
                with lock:
                    done += 1
                    if done % 50 == 0:
                        print(f"  {done}/{len(todo)}", flush=True)

    if chunks:
        with ThreadPoolExecutor(workers) as pool:
            list(pool.map(run_chunk, chunks))


if __name__ == "__main__":
    main()

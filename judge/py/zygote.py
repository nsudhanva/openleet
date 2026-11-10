"""The judge's Python zygote: imports LeetCode's environment once, then forks one sandboxed
child per job. Input conversion (and stress-test generation) happens here, before the fork, so
the child's CPU time is the solution's own; the child inherits the ready objects for free.

Protocol (one JSON object per line):
  in   {"spec": {...}, "code": "...", "keep_going": bool,
        "tests": [{"input": {...}} | {"gen": slug, "seed": n, "sha": hex}],
        "limits": {"cpu_s": n, "as_mb": n, "out_bytes": n, "stdout_bytes": n}}
  out  {"pid": n}                                   child started (the daemon watches its CPU)
       {"cpu_ms": n, "ev": <child event>}           child events, with the child's CPU so far
       {"done": {"code": n|null, "signal": n|null, "cpu_ms": n, "maxrss_kb": n}}
       {"ole": true}                                child wrote more than out_bytes
       {"fatal": "..."}                             the job itself is bad (never the solution)
Child events: {"i": n, "out": json, "stdout": s} | {"i": n, "error": s, "stdout": s}
              | {"i": n, "mle": true} | {"compile": s} | {"sandbox": s} (judge fault)
"""

import contextlib
import gc
import hashlib
import importlib.util
import io
import json
import linecache
import os
import resource
import signal
import sys
import threading
import traceback
from collections import OrderedDict
from pathlib import Path
from random import Random
from types import ModuleType

sys.path.insert(0, str(Path(__file__).parent))

import harness
import prelude

# An id no other process on the host uses, so RLIMIT_NPROC counts only this sandbox. Zygotes
# that run side by side (the test builder) each need their own.
SANDBOX_ID = int(os.environ.get("JUDGE_SANDBOX_UID", "61000"))
GEN_DIR = Path(os.environ.get("JUDGE_GEN_DIR", Path(__file__).parent / "gen"))
sys.path.append(str(GEN_DIR))  # generators import _shapes
SOLUTION_FILE = "solution.py"
STACK_BYTES = 256 * 1024 * 1024
RECURSION_LIMIT = 1_000_000
TICKS = os.sysconf("SC_CLK_TCK")

# Generated stress inputs of the problem judged last, prepared once and reused while the same
# problem is submitted again. Only one problem's are kept: they are big (10^5-node structures)
# and count against the judge's memory limit. Children mutate their own copy-on-write pages.
generated: OrderedDict[tuple[str, int], object] = OrderedDict()
generators: dict[str, ModuleType] = {}


def emit(obj: dict) -> None:
    sys.stdout.buffer.write(json.dumps(obj, separators=(",", ":")).encode() + b"\n")
    sys.stdout.buffer.flush()


def generator(slug: str) -> ModuleType:
    """gen/<slug>.py, loaded once: `generate(rng)` makes an input, `SEEDS` says how many."""
    if slug not in generators:
        spec = importlib.util.spec_from_file_location(f"gen_{slug}", GEN_DIR / f"{slug}.py")
        if spec is None or spec.loader is None:
            raise FileNotFoundError(f"No generator for {slug}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        generators[slug] = module
    return generators[slug]


def input_sha(data: object) -> str:
    """The fingerprint stored with a generated test, so a changed generator is caught."""
    return hashlib.sha256(harness.dumps(data).encode()).hexdigest()


def generated_input(spec: dict, test: dict):
    key = (test["gen"], test["seed"])
    if key in generated:
        generated.move_to_end(key)
        return generated[key]
    data = generator(test["gen"]).generate(Random(test["seed"]))
    if test.get("sha") and input_sha(data) != test["sha"]:
        raise ValueError(f"Generator {key} no longer makes the stored input")
    prepared = harness.prepare(spec, data)
    for other in [k for k in generated if k[0] != key[0]]:
        del generated[other]
    generated[key] = prepared
    return prepared


def prepare_all(spec: dict, tests: list[dict]) -> list:
    return [
        generated_input(spec, t) if "gen" in t else harness.prepare(spec, t["input"]) for t in tests
    ]


class CappedWriter(io.TextIOBase):
    """stdout for the solution: keeps the first `cap` characters, drops the rest."""

    def __init__(self, cap: int):
        self.cap, self.parts, self.size = cap, [], 0

    def write(self, text: str) -> int:
        if self.size < self.cap:
            piece = text[: self.cap - self.size]
            self.parts.append(piece)
            self.size += len(piece)
        return len(text)

    def take(self) -> str:
        text = "".join(self.parts)
        self.parts, self.size = [], 0
        return text


def user_traceback(error: BaseException) -> str:
    """The error as LeetCode shows it: the exception, then the solution's lines it went through."""
    frames = [f for f in traceback.extract_tb(error.__traceback__) if f.filename == SOLUTION_FILE]
    lines = [f"{type(error).__name__}: {error}".rstrip(": ")]
    lines += [f"    {f.line}\nLine {f.lineno} in {f.name} ({SOLUTION_FILE})" for f in frames]
    return "\n".join(lines)


def sandbox(limits: dict, keep_fd: int) -> None:
    """Runs in the child before any user code: no files, no privileges, bounded resources."""
    # Own process group, so the daemon can kill everything this job started at once.
    os.setpgid(0, 0)
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGPIPE):
        signal.signal(sig, signal.SIG_DFL)
    null = os.open(os.devnull, os.O_RDWR)
    for fd in (0, 1, 2):
        os.dup2(null, fd)
    os.closerange(3, keep_fd)
    os.closerange(keep_fd + 1, 1 << 16)
    # When the judge's memory runs out, the kernel kills this child first, never the zygote
    # or the daemon. Raising one's own score needs no privilege, but after setuid
    # /proc/self belongs to root, so it is done here.
    with contextlib.suppress(OSError):
        Path("/proc/self/oom_score_adj").write_text("1000")
    if os.getuid() == 0:
        os.setgroups([])
        os.setgid(SANDBOX_ID)
        os.setuid(SANDBOX_ID)
    cpu = int(limits["cpu_s"])
    as_bytes = int(limits["as_mb"]) * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu + 1))
    resource.setrlimit(resource.RLIMIT_AS, (as_bytes, as_bytes))
    resource.setrlimit(resource.RLIMIT_FSIZE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    sys.setrecursionlimit(RECURSION_LIMIT)
    # LeetCode's Python has no int<->str digit limit (CPython's default is 4300 digits).
    sys.set_int_max_str_digits(0)
    threading.stack_size(STACK_BYTES)


def child(job: dict, prepared: list, out_fd: int) -> None:
    sandbox(job["limits"], out_fd)
    stream = os.fdopen(out_fd, "wb", buffering=1 << 16)

    def send(event: dict) -> None:
        stream.write(harness.dumps(event).encode())
        stream.write(b"\n")
        stream.flush()

    stdout = CappedWriter(int(job["limits"].get("stdout_bytes", 1 << 14)))
    spec = job["spec"]
    # Test builders run every test even after a failure; the judge stops at the first one.
    keep_going = bool(job.get("keep_going"))

    def body() -> None:
        try:
            code = compile(job["code"], SOLUTION_FILE, "exec")
        except (SyntaxError, ValueError) as error:
            send({"compile": "".join(traceback.format_exception_only(error)).strip()})
            return
        # Tracebacks quote the solution's own lines.
        linecache.cache[SOLUTION_FILE] = (
            len(job["code"]),
            None,
            job["code"].splitlines(keepends=True),
            SOLUTION_FILE,
        )
        namespace = prelude.namespace()
        sys.stdout = stdout
        try:
            exec(code, namespace)
        except BaseException as error:
            send({"compile": user_traceback(error)})
            return
        for i, test in enumerate(prepared):
            try:
                out = harness.run(namespace, spec, test)
            except MemoryError:
                send({"i": i, "mle": True})
                return
            except BaseException as error:
                send({"i": i, "error": user_traceback(error), "stdout": stdout.take()})
                if keep_going:
                    continue
                return
            try:
                send({"i": i, "out": out, "stdout": stdout.take()})
            except (TypeError, ValueError) as error:
                send({"i": i, "error": f"Cannot print the result: {error}", "stdout": ""})
                return

    # This process plus the one worker thread; no further processes or threads after that.
    resource.setrlimit(resource.RLIMIT_NPROC, (2, 2))
    worker = threading.Thread(target=body)
    worker.start()
    worker.join()
    stream.close()


def cpu_ms(pid: int) -> int:
    try:
        fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        return (int(fields[11]) + int(fields[12])) * 1000 // TICKS
    except OSError, IndexError, ValueError:
        return -1


def handle(job: dict) -> None:
    try:
        prepared = prepare_all(job["spec"], job["tests"])
    except Exception as error:
        emit({"fatal": f"{type(error).__name__}: {error}"})
        return
    read_fd, write_fd = os.pipe()
    # Every object that exists now goes to the permanent generation: the child's collector
    # never walks the inputs or the cache, so it never copies their pages (that copy cost
    # ~0.7 s of the solution's CPU time with a 160 MB cache).
    gc.freeze()
    pid = os.fork()
    if pid == 0:
        os.close(read_fd)
        try:
            child(job, prepared, write_fd)
        except BaseException as error:
            os.write(write_fd, json.dumps({"sandbox": repr(error)}).encode() + b"\n")
        finally:
            os._exit(0)
    os.close(write_fd)
    del prepared
    emit({"pid": pid})
    limit = int(job["limits"].get("out_bytes", 64 << 20))
    total = 0
    with os.fdopen(read_fd, "rb") as events:
        for line in events:
            # An event longer than the pipe's atomic write size is cut short when the child is
            # killed while writing it (a time limit, or the stop after a wrong answer).
            if not line.endswith(b"\n"):
                break
            total += len(line)
            if total > limit:
                os.kill(pid, signal.SIGKILL)
                emit({"ole": True})
                break
            sys.stdout.buffer.write(b'{"cpu_ms":%d,"ev":%s}\n' % (cpu_ms(pid), line.rstrip(b"\n")))
            sys.stdout.buffer.flush()
    _, status, usage = os.wait4(pid, 0)
    gc.unfreeze()
    emit(
        {
            "done": {
                "code": os.waitstatus_to_exitcode(status) if os.WIFEXITED(status) else None,
                "signal": os.WTERMSIG(status) if os.WIFSIGNALED(status) else None,
                "cpu_ms": round((usage.ru_utime + usage.ru_stime) * 1000),
                "maxrss_kb": usage.ru_maxrss,
            }
        }
    )


def main() -> None:
    # Test inputs and generated tests may hold huge integers, as on LeetCode.
    sys.set_int_max_str_digits(0)
    gc.collect()
    # Objects that exist now are never collected, so children do not copy their pages.
    gc.freeze()
    emit({"ready": True})
    for line in sys.stdin.buffer:
        if line.strip():
            handle(json.loads(line))
        gc.collect()


if __name__ == "__main__":
    main()

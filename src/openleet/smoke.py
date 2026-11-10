"""`uv run openleet smoke`: an end-to-end test of the judge through a running server's HTTP API.

It submits each sampled problem's reference solution and broken variants of it (wrong answers,
crashes, syntax errors, slow code), then abuses the sandbox and the API (fork bombs, file and
network probes, killing processes, bad requests, parallel submissions) and checks every verdict.
Only HTTP is used, so the same command checks a local server and production:

    uv run openleet smoke --base-url https://openleet.sudhanva.me --seed 7

Reference solutions come from data/judge/specs.json (`--specs`), which should match the server's
release. Safe for production: requests are sequential (except the concurrency check), progress
and notes are never touched, and every draft it changes is put back. Submissions it makes stay
in each problem's history, and an accepted one marks the problem solved.
"""

import json
import random
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, TextIO

from openleet.judging import SPECS_PATH

DEFAULT_URL = "http://localhost:8080"
# The judge may queue a submission behind others, then run it twice (a slowed machine), each
# time for up to 120 s of CPU on a throttled machine (proto MAX_RUN_CPU_MS).
TIMEOUT_S = 600
BUSY_RETRIES = 20
BUSY_WAIT_S = 3.0
# The judge's per-test stdout cap (judge/src/run.rs STDOUT_BYTES, counted in characters).
STDOUT_CAP = 16 << 10
MAX_CODE_BYTES = 64 << 10
MARK = -987654321
# The largest time limit, and the one without a measured limit, in reference ms
# (server/src/judge.rs, limits::MAX_MS and limits::DEFAULT_MS).
MAX_LIMIT_MS = 30_000
DEFAULT_LIMIT_MS = 2000
UNICODE = "héllo ✓ 日本語 🚀"
CONCURRENT = 8
# Category order for the sample: rare kinds first, so a small sample still covers them.
CATEGORIES = (
    "adapter:cycle",
    "adapter:node_value",
    "adapter:nary",
    "adapter:next_pointer",
    "adapter:random_list",
    "adapter:intersection",
    "adapter:delete_node",
    "adapter:graph",
    "design",
    "linked-list",
    "tree",
    "float",
    "checker:unordered",
    "checker:unordered_nested",
    "stress",
    "function",
)


# ----------------------------------------------------------------------------- HTTP


@dataclass
class Reply:
    status: int
    body: Any
    seconds: float

    @property
    def error(self) -> str:
        return self.body.get("error", "") if isinstance(self.body, dict) else str(self.body)

    @property
    def busy(self) -> bool:
        return self.status == 503 and "busy" in self.error.lower()


class Api:
    def __init__(self, base: str):
        self.base = base.rstrip("/")

    def raw(self, method: str, path: str, data: bytes | None = None) -> Reply:
        request = urllib.request.Request(
            self.base + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json", "User-Agent": "openleet-smoke"},
        )
        started = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT_S) as response:
                status, text = response.status, response.read()
        except urllib.error.HTTPError as error:
            status, text = error.code, error.read()
        try:
            body = json.loads(text) if text else None
        except ValueError:
            body = text.decode(errors="replace")
        return Reply(status, body, time.monotonic() - started)

    def call(self, method: str, path: str, body: Any = None, retry_busy: bool = True) -> Reply:
        data = None if body is None else json.dumps(body).encode()
        for _ in range(BUSY_RETRIES):
            reply = self.raw(method, path, data)
            if not (retry_busy and reply.busy):
                return reply
            time.sleep(BUSY_WAIT_S)
        return reply

    def submit(self, slug: str, code: str, retry_busy: bool = True) -> Reply:
        return self.call("POST", "/api/submit", {"slug": slug, "code": code}, retry_busy)

    def run(self, slug: str, code: str, custom: str | None = None) -> Reply:
        body: dict[str, Any] = {"slug": slug, "code": code}
        if custom is not None:
            body["input"] = custom
        return self.call("POST", "/api/run", body)

    def code_info(self, slug: str) -> dict:
        reply = self.call("GET", f"/api/code/{slug}")
        if reply.status != 200:
            raise RuntimeError(f"GET /api/code/{slug}: {reply.status} {reply.error}")
        return reply.body


# ----------------------------------------------------------------------------- variants

# Appended to a solution: wraps its entry points so the tests the harness runs from `start` on
# misbehave in the chosen way. Only calls that come straight from the harness count (a
# recursive solution calling itself is left alone), so test i is the i-th harness call (the
# i-th constructor call for design problems).
WRAPPER = '''

import os as _smoke_os
import signal as _smoke_signal
import sys as _smoke_sys

_SMOKE_MARK = {mark}
_SMOKE = {{"mode": {mode!r}, "start": {start}, "flood": {flood!r}, "n": -1, "once": False}}
# Modes that act on the first test only.
_SMOKE_ONCE = ("probe", "recurse")


def _smoke_bad(value, rtype):
    t = (rtype or "").replace(" ", "")
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1 + abs(value)
    if isinstance(value, float):
        return value * 1.5 + 1.0
    if isinstance(value, str):
        return value + "#"
    if isinstance(value, (list, tuple)):
        return [*value, value[0] if value else None]
    if isinstance(value, (set, frozenset)):
        return set(value) | {{_SMOKE_MARK}}
    if isinstance(value, dict):
        return {{**value, "#": 0}}
    if isinstance(value, ListNode) or (value is None and "ListNode" in t):
        return ListNode(_SMOKE_MARK, value)
    if isinstance(value, TreeNode) or (value is None and "TreeNode" in t):
        return TreeNode(_SMOKE_MARK, value)
    if isinstance(value, Node) or (value is None and "Node" in t):
        node = Node(_SMOKE_MARK, left=value, next=value)
        node.children = [value] if value is not None else []
        node.neighbors = [node]
        return node
    return _SMOKE_MARK


def _smoke_spoil(arg):
    """In-place problems: the answer is the first argument afterwards. An empty tree or list
    cannot be spoiled, so the next test is spoiled instead."""
    if isinstance(arg, list):
        arg.append(arg[0] if arg else 0)
    elif arg is not None and hasattr(arg, "val"):
        arg.val = _SMOKE_MARK
    else:
        _SMOKE["start"] += 1


def _smoke_before(args):
    mode = _SMOKE["mode"]
    if mode == "crash":
        raise ZeroDivisionError("smoke: deliberate crash")
    if mode == "slow":
        # Passes the first two tests, then runs forever: a time limit with tests passed,
        # whatever the problem's limit is.
        _SMOKE["calls"] = _SMOKE.get("calls", 0) + 1
        if _SMOKE["calls"] > 2:
            while True:
                pass
    elif mode == "spin":
        while True:
            pass
    elif mode == "alloc":
        _SMOKE["hold"] = bytearray(8 << 30)
    elif mode == "grow":
        chunks = []
        while True:
            # Big steps: the memory limit comes long before the time limit, even on a slow VM.
            chunks.append(b"x" * (64 << 20))
    elif mode == "fork":
        while True:
            _smoke_os.fork()
    elif mode == "write":
        with open("/tmp/openleet-smoke", "w") as f:
            f.write("x" * 4096)
    elif mode == "pipe":
        for fd in _smoke_os.listdir("/proc/self/fd"):
            if int(fd) > 2:
                try:
                    _smoke_os.write(int(fd), b"garbage\\n")
                except OSError:
                    pass
    elif mode == "sys_exit":
        _smoke_sys.exit(0)
    elif mode == "os_exit":
        _smoke_os._exit(0)
    elif mode == "kill_self":
        _smoke_os.kill(_smoke_os.getpid(), _smoke_signal.SIGKILL)
    elif mode == "kill_parent":
        _smoke_os.kill(_smoke_os.getppid(), _smoke_signal.SIGKILL)
    elif mode == "kill_all":
        _smoke_os.kill(-1, _smoke_signal.SIGKILL)
    elif mode == "recurse":
        def down(n):
            return 0 if n == 0 else 1 + down(n - 1)
        assert down(10**5) == 10**5
    elif mode == "unicode":
        print({unicode!r})
    elif mode == "probe":
        _smoke_probe()


def _smoke_probe():
    def attempt(label, action):
        try:
            print(label, "OK", action())
        except BaseException as error:
            print(label, "ERR", type(error).__name__)

    def read(path):
        with open(path, "rb") as f:
            data = f.read(1 << 20)
        return f"{{len(data)}}B" + (" SECRET" if b"DEPLOY_SECRET" in data else "")

    state = "/var/lib/openleet"
    attempt("listdir:" + state, lambda: len(_smoke_os.listdir(state)))
    for path in (state + "/openleet.duckdb", "/etc/openleet.env", "/etc/passwd", "/etc/shadow",
                 "/proc/1/environ"):
        attempt("read:" + path, lambda: read(path))
    secrets = [k for k in _smoke_os.environ if "SECRET" in k or "TOKEN" in k or "PASSWORD" in k]
    print("environ", "SECRET" if secrets else "clean", ",".join(secrets))
    import socket
    for host, port in (("1.1.1.1", 53), ("127.0.0.1", 80), ("127.0.0.1", 8080)):
        attempt(f"net:{{host}}:{{port}}", lambda: socket.create_connection((host, port), 3).close())
    attempt("dns:example.com", lambda: socket.getaddrinfo("example.com", 80)[0][4][0])


def _smoke_outer():
    return _smoke_sys._getframe(2).f_code.co_filename != "solution.py"


def _smoke_wrap(cls, name, rtype, design):
    original = cls.__dict__.get(name) or getattr(cls, name)
    if isinstance(original, (staticmethod, classmethod)):
        return

    def wrapped(self, *args, **kwargs):
        outer = _smoke_outer()
        if outer and (name == "__init__" or not design):
            _SMOKE["n"] += 1
        active = outer and _SMOKE["n"] >= _SMOKE["start"]
        mode = _SMOKE["mode"]
        if active and mode not in ("wrong", "none") and not (name == "__init__" and design):
            if mode not in _SMOKE_ONCE or not _SMOKE["once"]:
                _SMOKE["once"] = True
                _smoke_before(args)
        if outer and _SMOKE["flood"]:
            for _ in range(2000):
                print("x" * 63)
        result = original(self, *args, **kwargs)
        wrong = _SMOKE["mode"] == "wrong" and _SMOKE["n"] == _SMOKE["start"]
        if outer and wrong and name != "__init__":
            if rtype == "None" and not design:
                _smoke_spoil(args[0] if args else None)
            else:
                result = _smoke_bad(result, rtype)
        return result

    setattr(cls, name, wrapped)


def _smoke_install(cls_name, entries, design):
    cls = globals()[cls_name]
    for name, rtype in entries.items():
        _smoke_wrap(cls, name, rtype, design)


_smoke_install({cls!r}, {entries!r}, {design!r})
'''


def variant(entry: dict, mode: str, start: int = 0, flood: bool = False) -> str:
    """The reference with misbehaving entry points (see WRAPPER)."""
    spec = entry["spec"]
    design = spec["kind"] == "design"
    if design:
        entries = {"__init__": None} | {
            name: info.get("returns")
            for name, info in spec.get("methods", {}).items()
            if name != "__init__"
        }
    else:
        entries = {spec["method"]: spec["returns"].replace(" ", "")}
    code = entry["reference"].rstrip() + WRAPPER.format(
        mark=MARK,
        mode=mode,
        start=start,
        flood=flood,
        unicode=UNICODE,
        cls=spec["cls"],
        entries=entries,
        design=design,
    )
    compile(code, "solution.py", "exec")  # a broken variant is this tool's bug, not the judge's
    return code


# ----------------------------------------------------------------------------- sampling


def categories(entry: dict) -> list[str]:
    spec = entry["spec"]
    text = json.dumps(spec)
    found = []
    if spec["kind"] == "design":
        found.append("design")
    if spec.get("adapter"):
        found.append(f"adapter:{spec['adapter']}")
    elif "ListNode" in text:
        found.append("linked-list")
    elif "TreeNode" in text:
        found.append("tree")
    if entry.get("floats"):
        found.append("float")
    if entry.get("checker", "exact") != "exact":
        found.append(f"checker:{entry['checker']}")
    if entry.get("tests", {}).get("stress"):
        found.append("stress")
    return found or ["function"]


def judged(specs: dict) -> dict[str, dict]:
    """Problems with a reference solution, which their limit admits (src/openleet/judging/
    limits.py) unless the limit had to stop at its cap."""
    return {
        slug: entry
        for slug, entry in specs.items()
        if entry.get("supported")
        and entry.get("reference")
        and entry.get("spec")
        and limit_ms(entry) < MAX_LIMIT_MS
    }


def sample(specs: dict[str, dict], size: int, rng: random.Random) -> list[str]:
    """`size` problems, round-robin over CATEGORIES so every kind is covered."""
    pools: dict[str, list[str]] = {c: [] for c in CATEGORIES}
    for slug in sorted(specs):
        for category in categories(specs[slug]):
            pools.setdefault(category, []).append(slug)
    for pool in pools.values():
        rng.shuffle(pool)
    chosen: list[str] = []
    while len(chosen) < min(size, len(specs)):
        progressed = False
        for pool in pools.values():
            while pool and pool[-1] in chosen:
                pool.pop()
            if pool and len(chosen) < size:
                chosen.append(pool.pop())
                progressed = True
        if not progressed:
            break
    return chosen


def limit_ms(entry: dict) -> int:
    """The problem's time limit in reference ms, as the server reads it."""
    return min(entry.get("limitMs") or DEFAULT_LIMIT_MS, MAX_LIMIT_MS)


def reference_ms(entry: dict) -> int:
    """CPU time of the problem's fastest trusted reference solution, in reference ms."""
    return min((entry.get("cpuMs") or {"": 0}).values())


def abuse_problem(specs: dict[str, dict]) -> str:
    """A plain, fast function problem with two or more inputs, for the sandbox checks."""
    candidates = [
        (limit_ms(e), slug)
        for slug, e in specs.items()
        if e["spec"]["kind"] == "function"
        and not e["spec"].get("adapter")
        and e.get("checker", "exact") == "exact"
        and not e.get("floats")
        and len(e["spec"]["params"]) >= 2
        and e["tests"].get("hidden", 0) >= 5
        and categories(e) == ["function"]
    ]
    return min(candidates)[1]


def slow_problems(specs: dict[str, dict], rng: random.Random, count: int) -> list[str]:
    """Stress problems with big list or string inputs and a limit of 8 s or less, so the slow
    variant's time limit comes quickly."""
    sized = [
        slug
        for slug, e in sorted(specs.items())
        if e["tests"].get("stress")
        and e["spec"]["kind"] == "function"
        and any(p["type"].startswith(("List", "str")) for p in e["spec"]["params"])
        and reference_ms(e) >= 100
        and limit_ms(e) <= 8000
    ]
    return rng.sample(sized, min(count, len(sized)))


# ----------------------------------------------------------------------------- checks


@dataclass
class Row:
    scenario: str
    problem: str
    expected: str
    got: str = ""
    cpu_ms: int | None = None
    ok: bool = False
    note: str = ""


@dataclass
class Smoke:
    api: Api
    specs: dict[str, dict]
    rng: random.Random
    show: Callable[[Row], None]
    rows: list[Row] = field(default_factory=list)
    infos: dict[str, dict] = field(default_factory=dict)
    # The Docker judge for local development has a network; production's has none.
    allow_network: bool = False

    def record(self, row: Row) -> Row:
        self.rows.append(row)
        self.show(row)
        return row

    def check(self, scenario: str, problem: str, expected: str, test: Callable[[], Row]) -> Row:
        try:
            row = test()
        except Exception as error:
            row = Row(scenario, problem, expected, got="exception", note=f"{error!r}"[:200])
        row.scenario, row.problem, row.expected = scenario, problem, expected
        return self.record(row)

    def info(self, slug: str) -> dict:
        if slug not in self.infos:
            self.infos[slug] = self.api.code_info(slug)
        return self.infos[slug]

    def total(self, slug: str) -> int:
        counts = self.specs[slug]["tests"]
        return counts.get("example", 0) + counts.get("hidden", 0) + counts.get("stress", 0)

    # --- one submission, judged against the expected verdict

    def verdict(
        self,
        slug: str,
        code: str,
        want: Iterable[str],
        extra: Callable[[dict], str | None] = lambda _: None,
    ) -> Row:
        """Submits `code`; ok when the verdict is in `want` and `extra` finds no problem."""
        want = tuple(want)
        reply = self.api.submit(slug, code)
        if reply.status != 200:
            return Row("", slug, "", got=f"HTTP {reply.status}", note=reply.error[:200])
        body = reply.body
        got = f"{body['verdict']} {body['passed']}/{body['total']}"
        problem = None if body["verdict"] in want else f"verdict {body['verdict']}"
        problem = problem or extra(body)
        note = problem or ""
        if problem and body.get("error"):
            note += f" | {body['error'].splitlines()[0][:120]}"
        return Row("", slug, "", got=got, cpu_ms=body.get("cpuMs"), ok=not problem, note=note)

    def problem_checks(self, slug: str) -> None:
        entry = self.specs[slug]
        total = self.total(slug)
        start = self.rng.randrange(1, total) if total > 1 else 0
        reference = entry["reference"]

        counts = entry["tests"]
        kinds = ["example"] * counts.get("example", 0) + ["hidden"] * counts.get("hidden", 0)
        kinds += ["stress"] * counts.get("stress", 0)

        def failed_at(body: dict) -> str | None:
            """Every test before `start` passed, and test `start` is the one shown."""
            if body["total"] != total:
                return f"total {body['total']} != {total} in specs.json"
            # An in-place answer that is an empty tree cannot be spoiled; a later test is.
            in_place = entry["spec"].get("returns", "").replace(" ", "") == "None"
            if body["passed"] != start and not (in_place and start < body["passed"] < total):
                return f"passed {body['passed']}, expected {start}"
            failing = body.get("failing")
            if not failing:
                return "no failing test shown"
            at = body["passed"]
            if failing["kind"] != kinds[at]:
                return f"failing test is {failing['kind']}, test #{at} is {kinds[at]}"
            return None

        def accepted(body: dict) -> str | None:
            if body["passed"] != body["total"] or body["total"] != total:
                return f"passed {body['passed']}/{body['total']}, specs.json says {total}"
            return None

        def traceback(body: dict) -> str | None:
            error = body.get("error") or ""
            if "solution.py" not in error or "ZeroDivisionError" not in error:
                return "traceback lacks solution.py / ZeroDivisionError"
            return failed_at(body)

        self.check(
            "reference",
            slug,
            "accepted",
            lambda: self.verdict(slug, reference, ["accepted"], accepted),
        )
        self.check(
            f"wrong on #{start} only",
            slug,
            f"wrong_answer {start}/{total}",
            lambda: self.verdict(slug, variant(entry, "wrong", start), ["wrong_answer"], failed_at),
        )
        self.check(
            f"crash at #{start}",
            slug,
            f"runtime_error {start}/{total}",
            lambda: self.verdict(
                slug, variant(entry, "crash", start), ["runtime_error"], traceback
            ),
        )

        def no_tests(body: dict) -> str | None:
            if body["passed"] != 0:
                return f"passed {body['passed']}"
            return None if "SyntaxError" in (body.get("error") or "") else "no SyntaxError shown"

        self.check(
            "syntax error",
            slug,
            "compile_error",
            lambda: self.verdict(
                slug, reference + "\n\ndef broken(:\n    pass\n", ["compile_error"], no_tests
            ),
        )
        self.check("run examples", slug, "accepted, every case ok", lambda: self.run_examples(slug))
        self.check(
            "run custom", slug, "accepted, expected from reference", lambda: self.run_custom(slug)
        )

    def run_examples(self, slug: str) -> Row:
        reply = self.api.run(slug, self.specs[slug]["reference"])
        if reply.status != 200:
            return Row("", slug, "", got=f"HTTP {reply.status}", note=reply.error[:200])
        body = reply.body
        cases = body["cases"]
        examples = self.info(slug)["judge"]["examples"]
        good = sum(1 for c in cases if c["ok"] is True)
        problem = None
        if body["verdict"] != "accepted":
            problem = f"verdict {body['verdict']}"
        elif len(cases) != examples or good != examples:
            problem = f"{good}/{len(cases)} cases ok, {examples} examples"
        got = f"{body['verdict']} {good}/{len(cases)}"
        return Row("", slug, "", got=got, cpu_ms=body["cpuMs"], ok=not problem, note=problem or "")

    def custom_input(self, slug: str, count: int = 2) -> str:
        """The shortest examples, in the Testcase box's format (one JSON value per line)."""
        shown = sorted(self.info(slug)["examples"], key=lambda e: len(e["input"]))[:count]
        lines = []
        for example in shown:
            for line in example["input"].splitlines():
                name, sep, value = line.partition(" = ")
                lines.append(value if sep and name.isidentifier() else line)
        return "\n".join(lines)

    def run_custom(self, slug: str) -> Row:
        custom = self.custom_input(slug)
        reply = self.api.run(slug, self.specs[slug]["reference"], custom)
        if reply.status != 200:
            return Row("", slug, "", got=f"HTTP {reply.status}", note=reply.error[:200])
        body = reply.body
        cases = body["cases"]
        filled = sum(1 for c in cases if c["expected"] is not None)
        good = sum(1 for c in cases if c["ok"] is True)
        problem = None
        if body["verdict"] != "accepted":
            problem = f"verdict {body['verdict']}"
        elif not cases or filled != len(cases) or good != len(cases):
            problem = f"{filled} expected filled, {good} ok of {len(cases)}"
        got = f"{body['verdict']} {good}/{len(cases)}"
        return Row("", slug, "", got=got, cpu_ms=body["cpuMs"], ok=not problem, note=problem or "")

    def slow_check(self, slug: str) -> None:
        def some_passed(body: dict) -> str | None:
            return None if body["passed"] > 0 else "no test passed before the limit"

        self.check(
            "slow (spins after 2 tests)",
            slug,
            "time_limit_exceeded, passed>0",
            lambda: self.verdict(
                slug, variant(self.specs[slug], "slow"), ["time_limit_exceeded"], some_passed
            ),
        )

    # --- the sandbox and the API

    def alive(self, slug: str, after: str) -> None:
        self.check(
            f"judge alive after {after}",
            slug,
            "accepted",
            lambda: self.verdict(slug, self.specs[slug]["reference"], ["accepted"]),
        )

    def run_stdout(self, slug: str, code: str, check: Callable[[dict], str | None]) -> Row:
        reply = self.api.run(slug, code)
        if reply.status != 200:
            return Row("", slug, "", got=f"HTTP {reply.status}", note=reply.error[:200])
        body = reply.body
        problem = check(body)
        got = f"{body['verdict']} {len(body['cases'])} cases"
        return Row("", slug, "", got=got, cpu_ms=body["cpuMs"], ok=not problem, note=problem or "")

    def abuse_checks(self, slug: str) -> None:
        entry = self.specs[slug]
        reference = entry["reference"]

        def submitted(mode: str, want: list[str], extra=lambda _: None) -> Callable[[], Row]:
            return lambda: self.verdict(slug, variant(entry, mode), want, extra)

        def error_has(*words: str) -> Callable[[dict], str | None]:
            def extra(body: dict) -> str | None:
                error = body.get("error") or ""
                missing = [w for w in words if w not in error]
                return f"error lacks {missing}" if missing else None

            return extra

        check = self.check
        check(
            "while True: pass",
            slug,
            "time_limit_exceeded",
            submitted("spin", ["time_limit_exceeded"]),
        )
        check(
            "8 GB bytearray",
            slug,
            "memory_limit_exceeded",
            submitted("alloc", ["memory_limit_exceeded"]),
        )
        check(
            "grow until killed",
            slug,
            "memory_limit_exceeded",
            submitted("grow", ["memory_limit_exceeded"]),
        )
        # The child can find its event pipe in /proc/self/fd and write anything to it.
        check(
            "garbage on the judge's pipe",
            slug,
            "runtime_error",
            submitted("pipe", ["runtime_error"], error_has("pipe")),
        )
        self.alive(slug, "memory, pipe")
        # The child may not fork: RLIMIT_NPROC is 2 (the process and its one worker thread).
        check(
            "fork bomb",
            slug,
            "runtime_error (fork refused)",
            submitted("fork", ["runtime_error"], error_has("BlockingIOError")),
        )
        self.alive(slug, "fork bomb")
        # RLIMIT_FSIZE is 0: no file can be written (Python ignores SIGXFSZ, so it is an error).
        check(
            "write a file",
            slug,
            "runtime_error (EFBIG)",
            submitted("write", ["runtime_error"], error_has("File too large")),
        )
        check(
            "sys.exit(0)",
            slug,
            "runtime_error (SystemExit)",
            submitted("sys_exit", ["runtime_error"], error_has("SystemExit")),
        )
        check(
            "os._exit(0)",
            slug,
            "runtime_error",
            submitted("os_exit", ["runtime_error"]),
        )
        # A SIGKILL the judge did not send reads as the kernel's OOM killer (judge/src/run.rs).
        check(
            "SIGKILL own pid",
            slug,
            "memory_limit_exceeded (unasked SIGKILL)",
            submitted("kill_self", ["memory_limit_exceeded"]),
        )
        # The zygote runs as root, the child as the sandbox user: EPERM.
        check(
            "SIGKILL parent (zygote)",
            slug,
            "runtime_error (PermissionError)",
            submitted("kill_parent", ["runtime_error"], error_has("PermissionError")),
        )
        self.alive(slug, "kill parent")
        check(
            "kill(-1, SIGKILL)",
            slug,
            "accepted (nothing else to kill)",
            submitted("kill_all", ["accepted"]),
        )
        self.alive(slug, "kill -1")
        check("recursion depth 1e5", slug, "accepted", submitted("recurse", ["accepted"]))

        def probe(body: dict) -> str | None:
            stdout = "".join(c["stdout"] for c in body["cases"])
            lines: dict[str, str] = {}
            for line in stdout.splitlines():
                label, _, rest = line.partition(" ")
                lines.setdefault(label, rest)
            leaks = [
                label
                for label in (
                    "listdir:/var/lib/openleet",
                    "read:/var/lib/openleet/openleet.duckdb",
                    "read:/etc/openleet.env",
                    "read:/etc/shadow",
                )
                if not lines.get(label, "").startswith("ERR")
            ]
            leaks += [label for label, rest in lines.items() if "SECRET" in rest]
            if lines.get("environ", "").startswith("SECRET"):
                leaks.append("environ")
            if not lines:
                return f"no probe output (verdict {body['verdict']})"
            if leaks:
                return "readable: " + ", ".join(dict.fromkeys(leaks))
            return None

        def network(body: dict) -> str | None:
            stdout = "".join(c["stdout"] for c in body["cases"])
            open_ = [
                line.split(" ")[0]
                for line in stdout.splitlines()
                if line.startswith(("net:", "dns:")) and " OK" in line
            ]
            if not any(line.startswith("net:") for line in stdout.splitlines()):
                return f"no probe output (verdict {body['verdict']})"
            if open_ and not self.allow_network:
                return f"reachable: {', '.join(open_)}"
            return None

        check(
            "read state dir, env, secrets",
            slug,
            "no app data readable",
            lambda: self.run_stdout(slug, variant(entry, "probe"), probe),
        )
        check(
            "network (socket, DNS)",
            slug,
            "not checked (--allow-network)" if self.allow_network else "every connection fails",
            lambda: self.run_stdout(slug, variant(entry, "probe"), network),
        )

        def flood(body: dict) -> str | None:
            sizes = [len(c["stdout"]) for c in body["cases"]]
            if body["verdict"] != "accepted":
                return f"verdict {body['verdict']}"
            return (
                None if sizes and all(s == STDOUT_CAP for s in sizes) else f"stdout sizes {sizes}"
            )

        check(
            "print flood (Run)",
            slug,
            f"accepted, stdout cut to {STDOUT_CAP}",
            lambda: self.run_stdout(slug, variant(entry, "none", flood=True), flood),
        )

        def flood_failing(body: dict) -> str | None:
            size = len((body.get("failing") or {}).get("stdout") or "")
            return None if size == STDOUT_CAP else f"failing stdout {size} chars"

        flooded_wrong = variant(entry, "wrong", 1, flood=True)
        check(
            "print flood + wrong (Submit)",
            slug,
            f"wrong_answer, stdout cut to {STDOUT_CAP}",
            lambda: self.verdict(slug, flooded_wrong, ["wrong_answer"], flood_failing),
        )

        def unicode(body: dict) -> str | None:
            if body["verdict"] != "accepted":
                return f"verdict {body['verdict']}"
            outs = {c["stdout"] for c in body["cases"]}
            return None if outs == {UNICODE + "\n"} else f"stdout {sorted(outs)!r:.120}"

        check(
            "unicode code and stdout",
            slug,
            "accepted, stdout intact",
            lambda: self.run_stdout(slug, variant(entry, "unicode"), unicode),
        )

        def status(
            want: int, method: str, path: str, data: bytes | str | None
        ) -> Callable[[], Row]:
            def test() -> Row:
                payload = data.encode() if isinstance(data, str) else data
                reply = self.api.raw(method, path, payload)
                ok = reply.status == want
                return Row("", "", "", got=f"HTTP {reply.status}", ok=ok, note=reply.error[:120])

            return test

        big = reference + "\n" + "#" * (MAX_CODE_BYTES + 1024) + "\n"
        check(
            "code over 64 KB",
            slug,
            "HTTP 400",
            status(400, "POST", "/api/submit", json.dumps({"slug": slug, "code": big})),
        )
        check(
            "malformed JSON body",
            slug,
            "HTTP 400",
            status(400, "POST", "/api/submit", '{"slug": "' + slug + '", "code": '),
        )
        unknown = "no-such-problem-openleet-smoke"
        check(
            "unknown slug (submit)",
            unknown,
            "HTTP 404",
            status(404, "POST", "/api/submit", json.dumps({"slug": unknown, "code": reference})),
        )
        check(
            "unknown slug (code)",
            unknown,
            "HTTP 404",
            status(404, "GET", f"/api/code/{unknown}", None),
        )
        lines = len(entry["spec"]["params"])
        check(
            "custom input, wrong line count",
            slug,
            "HTTP 400",
            status(
                400,
                "POST",
                "/api/run",
                json.dumps(
                    {"slug": slug, "code": reference, "input": "\n".join(["1"] * (lines + 1))}
                ),
            ),
        )
        self.concurrency(slug)
        self.alive(slug, "concurrency")

    def concurrency(self, slug: str) -> None:
        reference = self.specs[slug]["reference"]

        def one(_: int) -> Reply:
            return self.api.submit(slug, reference, retry_busy=False)

        def test() -> Row:
            started = time.monotonic()
            with ThreadPoolExecutor(CONCURRENT) as pool:
                replies = list(pool.map(one, range(CONCURRENT)))
            seconds = time.monotonic() - started
            accepted = sum(
                1 for r in replies if r.status == 200 and r.body["verdict"] == "accepted"
            )
            busy = sum(1 for r in replies if r.busy)
            odd = [
                f"{r.status} {r.body.get('verdict') if r.status == 200 else r.error}"
                for r in replies
                if not (r.busy or (r.status == 200 and r.body["verdict"] == "accepted"))
            ]
            problem = None
            if odd:
                problem = f"unexpected: {odd}"
            elif accepted == 0:
                problem = "nothing accepted"
            got = f"{accepted} accepted, {busy} busy in {seconds:.1f}s"
            return Row("", slug, "", got=got, ok=not problem, note=problem or "")

        self.check(f"{CONCURRENT} parallel submits", slug, "accepted or 503 busy, no hang", test)

    def draft_round_trip(self, slug: str) -> None:
        def test() -> Row:
            mine = f"# openleet smoke draft {UNICODE}\n"
            steps = []

            def state() -> tuple:
                info = self.api.code_info(slug)
                return info["draft"], info["previous"]

            put = self.api.call("PUT", "/api/drafts", {"slug": slug, "code": mine})
            steps.append(("save", put.status == 204 and state()[0] == mine))
            reset = self.api.call("POST", "/api/drafts/reset", {"slug": slug, "code": mine})
            steps.append(("reset", reset.status == 200 and state() == (None, mine)))
            back = self.api.call("POST", "/api/drafts/restore", {"slug": slug, "code": ""})
            steps.append(("restore", back.status == 200 and state() == (mine, None)))
            again = self.api.call("POST", "/api/drafts/restore", {"slug": slug, "code": mine})
            steps.append(("nothing to restore", again.status == 400))
            failed = [name for name, good in steps if not good]
            got = "round trip ok" if not failed else "failed: " + ", ".join(failed)
            return Row("", slug, "", got=got, ok=not failed)

        self.check("drafts save/reset/restore", slug, "round trip", test)

    def health(self, when: str) -> None:
        def test() -> Row:
            version = self.api.call("GET", "/api/version")
            companies = self.api.call("GET", "/api/companies")
            good = (
                version.status == 200
                and isinstance(version.body, dict)
                and bool(version.body.get("revision"))
                and companies.status == 200
                and bool(companies.body)
            )
            revision = version.body.get("revision") if isinstance(version.body, dict) else None
            got = f"version {version.status} ({revision}), companies {companies.status}"
            return Row("", "", "", got=got, ok=good)

        self.check(f"health {when}", "-", "200, 200", test)

    # --- drafts are put back exactly as they were

    def snapshot(self, slugs: Iterable[str]) -> dict[str, tuple]:
        saved = {}
        for slug in slugs:
            info = self.info(slug)
            saved[slug] = (info["draft"], info["previous"], info["solved"])
        return saved

    def restore(self, saved: dict[str, tuple]) -> list[str]:
        """Puts every draft back; returns the slugs it could not restore."""
        broken = []
        for slug, (code, previous, _) in saved.items():
            info = self.api.code_info(slug)
            if (info["draft"], info["previous"]) == (code, previous):
                continue
            # Reset makes `previous` the given text; Restore with '' then clears `previous`.
            call = self.api.call
            call("POST", "/api/drafts/reset", {"slug": slug, "code": previous or code or "#"})
            if previous is None:
                call("POST", "/api/drafts/restore", {"slug": slug, "code": ""})
            call("PUT", "/api/drafts", {"slug": slug, "code": code or ""})
            info = self.api.code_info(slug)
            if (info["draft"], info["previous"]) != (code, previous):
                broken.append(slug)
        return broken


# ----------------------------------------------------------------------------- output

COLUMNS = (("scenario", 32), ("problem", 34), ("expected", 34), ("got", 30), ("cpu ms", 7))


def cell(text: object, width: int) -> str:
    text = "" if text is None else str(text)
    return text if len(text) <= width else text[: width - 1] + "…"


def header() -> str:
    names = " ".join(f"{name:<{width}}" for name, width in COLUMNS)
    return f"{names} result\n" + "-" * (sum(w + 1 for _, w in COLUMNS) + 6)


def line(row: Row) -> str:
    values = (row.scenario, row.problem, row.expected, row.got, row.cpu_ms)
    cells = " ".join(
        f"{cell(v, w):>{w}}" if name == "cpu ms" else f"{cell(v, w):<{w}}"
        for (name, w), v in zip(COLUMNS, values, strict=True)
    )
    text = f"{cells} {'pass' if row.ok else 'FAIL'}"
    return text + (f"\n    {row.note}" if row.note and not row.ok else "")


def smoke(
    base_url: str = DEFAULT_URL,
    size: int = 30,
    seed: int | None = None,
    as_json: bool = False,
    specs_path: Path = SPECS_PATH,
    slow: int = 2,
    allow_network: bool = False,
) -> int:
    """Runs every check; returns the process exit code (1 when anything failed)."""
    seed = random.randrange(1 << 31) if seed is None else seed
    out = sys.stderr if as_json else sys.stdout
    specs = judged(json.loads(Path(specs_path).read_text()))
    rng = random.Random(seed)
    chosen = sample(specs, size, rng)
    abuse = abuse_problem(specs)
    api = Api(base_url)

    def show(row: Row) -> None:
        print(line(row), file=out, flush=True)

    run = Smoke(api, specs, rng, show, allow_network=allow_network)
    print(f"openleet smoke: {base_url}, {len(chosen)} problems, seed {seed}", file=out)
    print(header(), file=out, flush=True)
    run.health("at start")
    if not run.rows[-1].ok:
        return finish(run, seed, base_url, as_json, [], [], out)
    used = [*dict.fromkeys([*chosen, abuse])]
    saved = run.snapshot(used)
    broken: list[str] = []
    try:
        for slug in chosen:
            run.problem_checks(slug)
        for slug in slow_problems(specs, rng, slow):
            run.slow_check(slug)
        run.abuse_checks(abuse)
        run.draft_round_trip(abuse)
    finally:
        broken = run.restore(saved)
        run.health("at end")
    solved = [slug for slug, (_, _, was) in saved.items() if not was]
    return finish(run, seed, base_url, as_json, broken, solved, out)


def finish(
    run: Smoke,
    seed: int,
    url: str,
    as_json: bool,
    broken: list[str],
    solved: list[str],
    out: TextIO,
) -> int:
    failed = [r for r in run.rows if not r.ok]
    passed = len(run.rows) - len(failed)
    if as_json:
        print(
            json.dumps(
                {
                    "baseUrl": url,
                    "seed": seed,
                    "passed": passed,
                    "failed": len(failed) + len(broken),
                    "rows": [asdict(r) for r in run.rows],
                    "draftsNotRestored": broken,
                    "markedSolved": solved,
                },
                indent=1,
            )
        )
    print(
        f"\n{passed}/{len(run.rows)} passed"
        f"{', drafts not restored: ' + ', '.join(broken) if broken else ''}"
        f" (seed {seed}; rerun with --seed {seed})",
        file=out,
    )
    if solved:
        print(f"Accepted submissions may have marked these solved: {', '.join(solved)}", file=out)
    return 1 if failed or broken else 0

"""Exclusive Time of Functions: n functions and "id:start|end:timestamp" logs."""


def check(n: int, logs: list[str]) -> None:
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert 2 <= len(logs) <= 500, "2 <= logs.length <= 500"
    starts, ends = set(), set()
    stack: list[int] = []
    for log in logs:
        parts = log.split(":")
        assert len(parts) == 3 and parts[1] in ("start", "end"), "log is id:start|end:timestamp"
        assert parts[0].isdigit() and parts[2].isdigit(), (
            "id and timestamp are non-negative integers"
        )
        fid, kind, ts = int(parts[0]), parts[1], int(parts[2])
        assert 0 <= fid < n, "0 <= function_id < n"
        assert 0 <= ts <= 10**9, "0 <= timestamp <= 10^9"
        seen = starts if kind == "start" else ends
        assert ts not in seen, f"no two {kind} events will happen at the same timestamp"
        seen.add(ts)
        if kind == "start":
            stack.append(fid)
        else:
            assert stack and stack[-1] == fid, "each function has an end log for each start log"
            stack.pop()
    assert not stack, "each function has an end log for each start log"

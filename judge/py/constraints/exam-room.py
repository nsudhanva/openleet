"""Exam Room: an ExamRoom(n) design with seat and leave calls."""

import bisect
import itertools


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == "ExamRoom" and len(args[0]) == 1, "the constructor is ExamRoom(n)"
    n = args[0][0]
    assert isinstance(n, int) and 1 <= n <= 10**9, "1 <= n <= 10^9"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls will be made to seat and leave"
    taken: list[int] = []
    for op, a in zip(ops[1:], args[1:], strict=False):
        if op == "seat":
            assert len(a) == 0, "seat() takes no arguments"
            if not taken:
                best = 0
            else:
                best, dist = 0, taken[0]
                if n - 1 - taken[-1] > dist:
                    best, dist = n - 1, n - 1 - taken[-1]
                for x, y in itertools.pairwise(taken):
                    d = (y - x) // 2
                    if d > dist or (d == dist and x + d < best):
                        best, dist = x + d, d
                assert dist > 0, "a seat is free when seat() is called"
            bisect.insort(taken, best)
        else:
            assert op == "leave" and len(a) == 1, "calls are seat() and leave(p)"
            i = bisect.bisect_left(taken, a[0])
            assert i < len(taken) and taken[i] == a[0], "there is a student sitting at seat p"
            taken.pop(i)

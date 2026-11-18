"""Online Election: a design class built from persons and times, then q(t) calls."""

from itertools import pairwise


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args have the same non-zero length"
    assert ops[0] == "TopVotedCandidate" and all(o == "q" for o in ops[1:]), (
        "a constructor call followed by q calls"
    )
    assert len(args[0]) == 2, "constructor takes persons and times"
    persons, times = args[0]
    n = len(persons)
    assert 1 <= n <= 5000, "1 <= persons.length <= 5000"
    assert len(times) == n, "times.length == persons.length"
    assert all(0 <= p < n for p in persons), "0 <= persons[i] < persons.length"
    assert all(0 <= t <= 10**9 for t in times), "0 <= times[i] <= 10^9"
    assert all(a < b for a, b in pairwise(times)), "times is sorted in strictly increasing order"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls will be made to q"
    for a in args[1:]:
        assert len(a) == 1, "q takes one argument"
        assert times[0] <= a[0] <= 10**9, "times[0] <= t <= 10^9"

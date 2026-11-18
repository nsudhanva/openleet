"""Sequentially Ordinal Rank Tracker: SORTracker() with add(name, score) and get() calls."""

import string


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args have the same non-zero length"
    assert ops[0] == "SORTracker" and args[0] == [], "SORTracker() comes first"
    assert all(o in ("add", "get") for o in ops[1:]), "only add/get follow"
    assert len(ops) - 1 <= 4 * 10**4, "at most 4 * 10^4 calls in total to add and get"
    names: set[str] = set()
    adds = gets = 0
    for o, a in zip(ops[1:], args[1:], strict=True):
        if o == "add":
            assert len(a) == 2, "add takes name and score"
            name, score = a
            assert isinstance(name, str) and 1 <= len(name) <= 10, "1 <= name.length <= 10"
            assert set(name) <= set(string.ascii_lowercase), (
                "name consists of lowercase English letters"
            )
            assert name not in names, "name is unique among all locations"
            names.add(name)
            assert isinstance(score, int) and 1 <= score <= 10**5, "1 <= score <= 10^5"
            adds += 1
        else:
            assert a == [], "get takes no arguments"
            gets += 1
            assert gets <= adds, "calls to get never exceed calls to add"

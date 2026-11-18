"""Prefix and Suffix Search: WordFilter(words) followed by f(pref, suff) calls."""


def _word(s: str, lo: int, hi: int, what: str) -> None:
    assert isinstance(s, str), f"{what} is a string"
    assert lo <= len(s) <= hi, f"{lo} <= {what}.length <= {hi}"
    assert all("a" <= c <= "z" for c in s), f"{what} consists of lowercase English letters only"


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args have the same length"
    assert ops[0] == "WordFilter", "the first call is the constructor"
    assert len(args[0]) == 1 and isinstance(args[0][0], list), "WordFilter takes words"
    words = args[0][0]
    assert 1 <= len(words) <= 10**4, "1 <= words.length <= 10^4"
    for w in words:
        _word(w, 1, 7, "words[i]")
    calls = ops[1:]
    assert all(op == "f" for op in calls), "every later call is f"
    assert len(calls) <= 10**4, "at most 10^4 calls to f"
    for a in args[1:]:
        assert len(a) == 2, "f takes pref and suff"
        _word(a[0], 1, 7, "pref")
        _word(a[1], 1, 7, "suff")

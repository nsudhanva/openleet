"""Implement Trie (Prefix Tree): calls on a Trie with insert, search and startsWith."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops and ops[0] == "Trie", "constructor first"
    assert args[0] == [], "Trie() takes no arguments"
    assert len(ops) - 1 <= 3 * 10**4, "At most 3 * 10^4 calls in total"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("insert", "search", "startsWith"), (
            "only insert, search, startsWith are called"
        )
        assert len(a) == 1, f"{op} takes one argument"
        w = a[0]
        assert 1 <= len(w) <= 2000, "1 <= word.length, prefix.length <= 2000"
        assert set(w) <= LOWER, "word and prefix consist only of lowercase English letters"

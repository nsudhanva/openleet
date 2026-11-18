"""Stream of Characters: constructor with words, then letter queries."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert ops[0] == "StreamChecker", "first op is the constructor"
    assert all(o == "query" for o in ops[1:]), "every later op is query"
    assert len(args[0]) == 1, "constructor takes words"
    words = args[0][0]
    assert 1 <= len(words) <= 2000, "1 <= words.length <= 2000"
    for w in words:
        assert isinstance(w, str) and 1 <= len(w) <= 200, "1 <= words[i].length <= 200"
        assert all("a" <= c <= "z" for c in w), "words[i] consists of lowercase English letters"
    assert len(ops) - 1 <= 4 * 10**4, "at most 4 * 10^4 calls to query"
    for a in args[1:]:
        assert len(a) == 1, "query takes one letter"
        c = a[0]
        assert isinstance(c, str) and len(c) == 1 and "a" <= c <= "z", (
            "letter is a lowercase English letter"
        )

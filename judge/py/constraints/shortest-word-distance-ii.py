"""Shortest Word Distance II: a WordDistance object queried with pairs of words."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "WordDistance" and len(args[0]) == 1, "constructor takes wordsDict"
    words = args[0][0]
    assert 1 <= len(words) <= 3 * 10**4, "1 <= wordsDict.length <= 3 * 10^4"
    for w in words:
        assert isinstance(w, str) and 1 <= len(w) <= 10, "1 <= wordsDict[i].length <= 10"
        assert w.isascii() and w.isalpha() and w.islower(), (
            "wordsDict[i] is lowercase English letters"
        )
    present = set(words)
    assert len(ops) - 1 <= 5000, "at most 5000 calls to shortest"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op == "shortest" and len(a) == 2, "only shortest(word1, word2) is called"
        assert a[0] in present and a[1] in present, "word1 and word2 are in wordsDict"
        assert a[0] != a[1], "word1 != word2"

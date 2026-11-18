"""Words Within Two Edits of Dictionary: two lists of equal-length lowercase words."""


def check(queries: list[str], dictionary: list[str]) -> None:
    assert 1 <= len(queries) <= 100, "1 <= queries.length <= 100"
    assert 1 <= len(dictionary) <= 100, "1 <= dictionary.length <= 100"
    n = len(queries[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(w) == n for w in queries), "n == queries[i].length"
    assert all(len(w) == n for w in dictionary), "n == dictionary[j].length"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in queries), (
        "queries[i] is composed of lowercase English letters"
    )
    assert all(w.isascii() and w.isalpha() and w.islower() for w in dictionary), (
        "dictionary[j] is composed of lowercase English letters"
    )

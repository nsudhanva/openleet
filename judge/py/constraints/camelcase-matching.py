"""Camelcase Matching: query words and a pattern of English letters."""


def check(queries: list[str], pattern: str) -> None:
    assert isinstance(pattern, str), "pattern is a string"
    assert 1 <= len(pattern) <= 100, "1 <= pattern.length <= 100"
    assert 1 <= len(queries) <= 100, "1 <= queries.length <= 100"
    assert all(isinstance(q, str) for q in queries), "queries[i] are strings"
    assert all(1 <= len(q) <= 100 for q in queries), "1 <= queries[i].length <= 100"
    letters = pattern + "".join(queries)
    assert letters.isascii() and letters.isalpha(), (
        "queries[i] and pattern consist of English letters"
    )

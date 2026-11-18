"""Minimum Number of People to Teach: n languages, each user's known languages and the
friendship pairs."""


def check(n: int, languages: list[list[int]], friendships: list[list[int]]) -> None:
    assert isinstance(n, int) and 2 <= n <= 500, "2 <= n <= 500"
    m = len(languages)
    assert 1 <= m <= 500, "1 <= m <= 500"
    for langs in languages:
        assert isinstance(langs, list) and 1 <= len(langs) <= n, "1 <= languages[i].length <= n"
        assert all(isinstance(v, int) and 1 <= v <= n for v in langs), "1 <= languages[i][j] <= n"
        assert len(set(langs)) == len(langs), "languages[i] contains only unique values"
    assert 1 <= len(friendships) <= 500, "1 <= friendships.length <= 500"
    assert all(len(f) == 2 for f in friendships), "friendships[i].length == 2"
    assert all(1 <= u < v <= m for u, v in friendships), "1 <= ui < vi <= languages.length"
    assert len({(u, v) for u, v in friendships}) == len(friendships), (
        "all tuples (ui, vi) are unique"
    )

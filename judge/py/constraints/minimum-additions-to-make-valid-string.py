"""Minimum Additions to Make Valid String: a short string over a, b, c."""


def check(word: str) -> None:
    assert 1 <= len(word) <= 50, "1 <= word.length <= 50"
    assert all(c in "abc" for c in word), 'word consists of letters "a", "b" and "c" only'

"""Jewels and Stones: two strings of English letters, jewels all distinct."""


def check(jewels: str, stones: str) -> None:
    assert isinstance(jewels, str) and isinstance(stones, str), "jewels and stones are strings"
    assert 1 <= len(jewels) <= 50, "1 <= jewels.length <= 50"
    assert 1 <= len(stones) <= 50, "1 <= stones.length <= 50"
    letters = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    assert set(jewels + stones) <= letters, "jewels and stones consist of only English letters"
    assert len(set(jewels)) == len(jewels), "all the characters of jewels are unique"

"""Check Whether Two Strings are Almost Equivalent: two lowercase strings of equal length."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(word1: str, word2: str) -> None:
    assert len(word1) == len(word2), "n == word1.length == word2.length"
    assert 1 <= len(word1) <= 100, "1 <= n <= 100"
    assert set(word1) <= LOWER and set(word2) <= LOWER, (
        "word1 and word2 consist only of lowercase English letters"
    )

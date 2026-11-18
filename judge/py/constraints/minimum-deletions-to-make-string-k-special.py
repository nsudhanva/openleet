"""Minimum Deletions to Make String K-Special: a lowercase word and k."""


def check(word: str, k: int) -> None:
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 10**5, "1 <= word.length <= 10^5"
    assert 0 <= k <= 10**5, "0 <= k <= 10^5"
    assert all("a" <= c <= "z" for c in word), "word consists only of lowercase English letters"

"""Count Caesar Cipher Pairs: equal-length lowercase words with n * m <= 10^5."""


def check(words: list[str]) -> None:
    n = len(words)
    assert 1 <= n <= 10**5, "1 <= n == words.length <= 10^5"
    m = len(words[0])
    assert 1 <= m <= 10**5, "1 <= m == words[i].length <= 10^5"
    assert all(len(w) == m for w in words), "m == words[i].length"
    assert 1 <= n * m <= 10**5, "1 <= n * m <= 10^5"
    assert all(c.islower() and c.isascii() and len(c) == 1 for w in words for c in w), (
        "words[i] consists only of lowercase English letters"
    )

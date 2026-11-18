"""Edit Distance: two lowercase words."""


def check(word1: str, word2: str) -> None:
    assert isinstance(word1, str) and isinstance(word2, str), "strings"
    assert 0 <= len(word1) <= 500, "0 <= word1.length <= 500"
    assert 0 <= len(word2) <= 500, "0 <= word2.length <= 500"
    assert all("a" <= c <= "z" for c in word1 + word2), "lowercase English letters"

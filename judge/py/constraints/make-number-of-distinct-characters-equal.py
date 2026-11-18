"""Make Number of Distinct Characters Equal: two lowercase words."""


def check(word1: str, word2: str) -> None:
    assert 1 <= len(word1) <= 10**5, "1 <= word1.length <= 10^5"
    assert 1 <= len(word2) <= 10**5, "1 <= word2.length <= 10^5"
    for w in (word1, word2):
        assert all("a" <= c <= "z" for c in w), "lowercase English letters only"

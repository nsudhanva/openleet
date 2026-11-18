"""Find the Lexicographically Smallest Valid Sequence: two lowercase words, word2 shorter."""


def check(word1: str, word2: str) -> None:
    assert isinstance(word1, str) and isinstance(word2, str), "word1 and word2 are strings"
    assert 1 <= len(word2) < len(word1) <= 3 * 10**5, "1 <= word2.length < word1.length <= 3 * 10^5"
    assert all("a" <= c <= "z" for c in word1 + word2), (
        "word1 and word2 consist only of lowercase English letters"
    )

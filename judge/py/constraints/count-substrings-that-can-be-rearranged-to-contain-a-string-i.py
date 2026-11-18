"""Count Substrings That Can Be Rearranged to Contain a String I: two lowercase strings."""


def check(word1: str, word2: str) -> None:
    assert 1 <= len(word1) <= 10**5, "1 <= word1.length <= 10^5"
    assert 1 <= len(word2) <= 10**4, "1 <= word2.length <= 10^4"
    assert word1.isascii() and word1.islower() and word1.isalpha(), (
        "word1 is lowercase English letters"
    )
    assert word2.isascii() and word2.islower() and word2.isalpha(), (
        "word2 is lowercase English letters"
    )

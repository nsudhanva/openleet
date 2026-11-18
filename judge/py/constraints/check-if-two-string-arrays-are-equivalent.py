"""Check If Two String Arrays are Equivalent: two lists of lowercase strings."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(word1: list[str], word2: list[str]) -> None:
    assert 1 <= len(word1) <= 10**3 and 1 <= len(word2) <= 10**3, (
        "1 <= word1.length, word2.length <= 10^3"
    )
    for words in (word1, word2):
        assert all(1 <= len(w) <= 10**3 for w in words), "1 <= word[i].length <= 10^3"
        assert 1 <= sum(len(w) for w in words) <= 10**3, "1 <= sum(word[i].length) <= 10^3"
        assert all(set(w) <= LOWER for w in words), "word[i] consist of lowercase letters"

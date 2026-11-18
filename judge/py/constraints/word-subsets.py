"""Word Subsets: two lists of lowercase words, the first with distinct entries."""


def check(words1: list[str], words2: list[str]) -> None:
    assert 1 <= len(words1) <= 10**4, "1 <= words1.length <= 10^4"
    assert 1 <= len(words2) <= 10**4, "1 <= words2.length <= 10^4"
    assert all(1 <= len(w) <= 10 for w in words1), "1 <= words1[i].length <= 10"
    assert all(1 <= len(w) <= 10 for w in words2), "1 <= words2[i].length <= 10"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words1), (
        "words1[i] consists only of lowercase English letters"
    )
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words2), (
        "words2[i] consists only of lowercase English letters"
    )
    assert len(set(words1)) == len(words1), "all the strings of words1 are unique"

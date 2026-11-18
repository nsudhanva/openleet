"""Shortest Word Distance: a list of words and two distinct words from it."""


def check(wordsDict: list[str], word1: str, word2: str) -> None:
    assert 2 <= len(wordsDict) <= 3 * 10**4, "2 <= wordsDict.length <= 3 * 10^4"
    for w in wordsDict:
        assert isinstance(w, str) and 1 <= len(w) <= 10, "1 <= wordsDict[i].length <= 10"
        assert w.isascii() and w.isalpha() and w.islower(), (
            "wordsDict[i] is lowercase English letters"
        )
    assert word1 in wordsDict and word2 in wordsDict, "word1 and word2 are in wordsDict"
    assert word1 != word2, "word1 != word2"

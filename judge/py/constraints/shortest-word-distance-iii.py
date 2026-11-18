"""Shortest Word Distance III: a list of words and two words from it."""


def check(wordsDict: list[str], word1: str, word2: str) -> None:
    assert 1 <= len(wordsDict) <= 10**5, "1 <= wordsDict.length <= 10^5"
    for w in wordsDict:
        assert isinstance(w, str) and 1 <= len(w) <= 10, "1 <= wordsDict[i].length <= 10"
        assert w.isascii() and w.isalpha() and w.islower(), (
            "wordsDict[i] is lowercase English letters"
        )
    assert word1 in wordsDict and word2 in wordsDict, "word1 and word2 are in wordsDict"

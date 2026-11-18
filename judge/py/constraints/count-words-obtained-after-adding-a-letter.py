"""Count Words Obtained After Adding a Letter: two word lists, each word with distinct letters."""

import string


def check(startWords: list[str], targetWords: list[str]) -> None:
    assert 1 <= len(startWords) <= 5 * 10**4, "1 <= startWords.length <= 5 * 10^4"
    assert 1 <= len(targetWords) <= 5 * 10**4, "1 <= targetWords.length <= 5 * 10^4"
    letters = set(string.ascii_lowercase)
    for w in startWords + targetWords:
        assert isinstance(w, str), "each word is a string"
        assert 1 <= len(w) <= 26, "1 <= word.length <= 26"
        assert set(w) <= letters, "lowercase English letters only"
        assert len(set(w)) == len(w), "no letter occurs more than once in a word"

"""Number of Strings That Appear as Substrings in Word: a list of patterns and a word."""


def check(patterns: list[str], word: str) -> None:
    assert isinstance(patterns, list), "patterns is a list"
    assert 1 <= len(patterns) <= 100, "1 <= patterns.length <= 100"
    assert all(isinstance(p, str) for p in patterns), "patterns[i] is a string"
    assert all(1 <= len(p) <= 100 for p in patterns), "1 <= patterns[i].length <= 100"
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 100, "1 <= word.length <= 100"
    letters = set("abcdefghijklmnopqrstuvwxyz")
    assert all(set(p) <= letters for p in patterns), "patterns[i] is lowercase English letters"
    assert set(word) <= letters, "word is lowercase English letters"

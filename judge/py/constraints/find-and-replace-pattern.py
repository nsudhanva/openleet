"""Find and Replace Pattern: a list of words and a pattern of the same length."""


def _lower(t: str) -> bool:
    return isinstance(t, str) and t.isascii() and t.islower() and t.isalpha()


def check(words: list[str], pattern: str) -> None:
    assert _lower(pattern), "pattern is lowercase English letters"
    assert 1 <= len(pattern) <= 20, "1 <= pattern.length <= 20"
    assert 1 <= len(words) <= 50, "1 <= words.length <= 50"
    assert all(_lower(w) for w in words), "words[i] is lowercase English letters"
    assert all(len(w) == len(pattern) for w in words), "words[i].length == pattern.length"

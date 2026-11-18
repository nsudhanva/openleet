"""Number of Ways to Form a Target String Given a Dictionary: equal-length words and a target."""


def check(words: list[str], target: str) -> None:
    assert isinstance(words, list), "words is a list"
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    assert all(isinstance(w, str) for w in words), "words[i] is a string"
    assert 1 <= len(words[0]) <= 1000, "1 <= words[i].length <= 1000"
    assert all(len(w) == len(words[0]) for w in words), "all strings in words have the same length"
    assert isinstance(target, str), "target is a string"
    assert 1 <= len(target) <= 1000, "1 <= target.length <= 1000"
    letters = set("abcdefghijklmnopqrstuvwxyz")
    assert all(set(w) <= letters for w in words), "words[i] is lowercase English letters"
    assert set(target) <= letters, "target is lowercase English letters"

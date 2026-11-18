"""Extra Characters in a String: a lowercase string and a dictionary of distinct words."""


def check(s: str, dictionary: list[str]) -> None:
    assert isinstance(s, str) and isinstance(dictionary, list), "s is a string, dictionary a list"
    assert 1 <= len(s) <= 50, "1 <= s.length <= 50"
    assert 1 <= len(dictionary) <= 50, "1 <= dictionary.length <= 50"
    assert all(1 <= len(w) <= 50 for w in dictionary), "1 <= dictionary[i].length <= 50"
    assert all(w.isascii() and w.islower() and w.isalpha() for w in [s, *dictionary]), (
        "dictionary[i] and s consist of only lowercase English letters"
    )
    assert len(set(dictionary)) == len(dictionary), "dictionary contains distinct words"

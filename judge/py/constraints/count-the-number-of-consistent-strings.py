"""Count the Number of Consistent Strings: allowed characters and an array of words."""


def check(allowed: str, words: list[str]) -> None:
    assert 1 <= len(words) <= 10**4, "1 <= words.length <= 10^4"
    assert 1 <= len(allowed) <= 26, "1 <= allowed.length <= 26"
    assert all(1 <= len(w) <= 10 for w in words), "1 <= words[i].length <= 10"
    assert len(set(allowed)) == len(allowed), "the characters in allowed are distinct"
    assert allowed.isascii() and allowed.islower() and allowed.isalpha(), (
        "allowed is lowercase English letters"
    )
    assert all(w.isascii() and w.islower() and w.isalpha() for w in words), (
        "words[i] is lowercase English letters"
    )

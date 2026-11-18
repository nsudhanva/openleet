"""Alien Dictionary: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(isinstance(w, str) for w in words), "words[i] is a string"
    assert all(1 <= len(w) <= 100 for w in words), "1 <= words[i].length <= 100"
    assert all(all("a" <= c <= "z" for c in w) for w in words), (
        "words[i] consists of only lowercase English letters"
    )

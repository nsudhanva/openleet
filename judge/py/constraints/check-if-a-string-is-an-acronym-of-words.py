"""Check if a String Is an Acronym of Words: lowercase words and a lowercase string."""


def check(words: list[str], s: str) -> None:
    assert isinstance(words, list) and isinstance(s, str), "words is a list, s a string"
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(isinstance(w, str) and 1 <= len(w) <= 10 for w in words), (
        "1 <= words[i].length <= 10"
    )
    assert 1 <= len(s) <= 100, "1 <= s.length <= 100"
    assert all("a" <= c <= "z" for w in words for c in w), "words[i] is lowercase English letters"
    assert all("a" <= c <= "z" for c in s), "s is lowercase English letters"

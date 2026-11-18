"""Maximum Palindromes After Operations: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    for w in words:
        assert 1 <= len(w) <= 100, "1 <= words[i].length <= 100"
        assert all("a" <= c <= "z" for c in w), "words[i] is lowercase letters"

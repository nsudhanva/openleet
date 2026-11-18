"""Maximum Product of Word Lengths: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 2 <= len(words) <= 1000, "2 <= words.length <= 1000"
    for w in words:
        assert 1 <= len(w) <= 1000, "1 <= words[i].length <= 1000"
        assert all("a" <= c <= "z" for c in w), "words[i] is lowercase letters"

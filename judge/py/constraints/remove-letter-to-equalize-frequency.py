"""Remove Letter To Equalize Frequency: a lowercase word."""


def check(word: str) -> None:
    assert isinstance(word, str), "word is a string"
    assert 2 <= len(word) <= 100, "2 <= word.length <= 100"
    assert all("a" <= c <= "z" for c in word), "word consists of lowercase English letters only"

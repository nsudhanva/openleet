"""String Compression III: a lowercase word."""


def check(word: str) -> None:
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 2 * 10**5, "1 <= word.length <= 2 * 10^5"
    assert all("a" <= c <= "z" for c in word), "word consists only of lowercase English letters"

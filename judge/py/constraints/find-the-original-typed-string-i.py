"""Find the Original Typed String I: a lowercase word."""


def check(word: str) -> None:
    assert 1 <= len(word) <= 100, "1 <= word.length <= 100"
    assert all("a" <= c <= "z" for c in word), "word consists only of lowercase English letters"

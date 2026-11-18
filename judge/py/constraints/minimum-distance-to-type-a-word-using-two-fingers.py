"""Minimum Distance to Type a Word Using Two Fingers: a word of uppercase letters."""


def check(word: str) -> None:
    assert 2 <= len(word) <= 300, "2 <= word.length <= 300"
    assert all(len(c) == 1 and "A" <= c <= "Z" for c in word), (
        "word consists of uppercase English letters"
    )

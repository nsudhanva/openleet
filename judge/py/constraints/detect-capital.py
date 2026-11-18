"""Detect Capital: a word of English letters."""


def check(word: str) -> None:
    assert isinstance(word, str) and 1 <= len(word) <= 100, "1 <= word.length <= 100"
    assert word.isascii() and word.isalpha(), (
        "word consists of lowercase and uppercase English letters"
    )

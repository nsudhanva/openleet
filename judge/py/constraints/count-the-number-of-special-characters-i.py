"""Count the Number of Special Characters I: a word of English letters."""


def check(word: str) -> None:
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 50, "1 <= word.length <= 50"
    assert word.isascii() and word.isalpha(), (
        "word consists of only lowercase and uppercase English letters"
    )

"""Count the Number of Special Characters II: a word of English letters."""


def check(word: str) -> None:
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 2 * 10**5, "1 <= word.length <= 2 * 10^5"
    assert word.isascii() and word.isalpha(), (
        "word consists of only lowercase and uppercase English letters"
    )

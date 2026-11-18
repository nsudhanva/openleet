"""Number of Wonderful Substrings: a word over the letters a to j."""


def check(word: str) -> None:
    assert isinstance(word, str), "word is a string"
    assert 1 <= len(word) <= 10**5, "1 <= word.length <= 10^5"
    assert set(word) <= set("abcdefghij"), (
        "word consists of lowercase English letters from 'a' to 'j'"
    )

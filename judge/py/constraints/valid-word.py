"""Valid Word: a string of letters, digits, '@', '#' and '$'."""

import string


def check(word: str) -> None:
    assert 1 <= len(word) <= 20, "1 <= word.length <= 20"
    allowed = set(string.ascii_letters + string.digits + "@#$")
    assert all(c in allowed for c in word), (
        "word consists of English letters, digits, '@', '#', and '$'"
    )

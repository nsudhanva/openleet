"""Sort Vowels in a String: a string of English letters."""

import string


def check(s: str) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in string.ascii_letters for c in s), "s consists only of English letters"

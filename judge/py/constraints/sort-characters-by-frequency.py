"""Sort Characters By Frequency: a string of letters and digits."""

import string


def check(s: str) -> None:
    assert 1 <= len(s) <= 5 * 10**5, "1 <= s.length <= 5 * 10^5"
    allowed = set(string.ascii_letters + string.digits)
    assert all(c in allowed for c in s), "s consists of English letters and digits"

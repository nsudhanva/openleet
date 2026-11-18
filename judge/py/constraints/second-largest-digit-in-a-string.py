"""Second Largest Digit in a String: a string of lowercase letters and digits."""

import string


def check(s: str) -> None:
    assert isinstance(s, str) and 1 <= len(s) <= 500, "1 <= s.length <= 500"
    assert set(s) <= set(string.ascii_lowercase + string.digits), (
        "s consists of only lowercase English letters and digits"
    )

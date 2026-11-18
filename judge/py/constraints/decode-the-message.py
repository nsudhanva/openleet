"""Decode the Message: a substitution key containing every letter and a message."""

import string


def check(key: str, message: str) -> None:
    allowed = set(string.ascii_lowercase + " ")
    assert 26 <= len(key) <= 2000, "26 <= key.length <= 2000"
    assert set(key) <= allowed, "key consists of lowercase English letters and ' '"
    assert set(string.ascii_lowercase) <= set(key), (
        "key contains every letter of the alphabet at least once"
    )
    assert 1 <= len(message) <= 2000, "1 <= message.length <= 2000"
    assert set(message) <= allowed, "message consists of lowercase English letters and ' '"

"""Validate IP Address: a string of letters, digits, '.' and ':'."""

import string


def check(queryIP: str) -> None:
    allowed = set(string.ascii_letters + string.digits + ".:")
    assert all(c in allowed for c in queryIP), (
        "queryIP consists only of English letters, digits and the characters '.' and ':'"
    )

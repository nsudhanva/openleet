"""Custom Sort String: an order of unique lowercase letters and a lowercase string s."""

import string


def check(order: str, s: str) -> None:
    letters = set(string.ascii_lowercase)
    assert 1 <= len(order) <= 26, "1 <= order.length <= 26"
    assert 1 <= len(s) <= 200, "1 <= s.length <= 200"
    assert set(order) <= letters and set(s) <= letters, (
        "order and s consist of lowercase English letters"
    )
    assert len(set(order)) == len(order), "all the characters of order are unique"

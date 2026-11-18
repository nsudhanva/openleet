"""Decoded String at Index: an encoded string of letters and digits 2-9, and a position."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 2 <= len(s) <= 100, "2 <= s.length <= 100"
    assert all(("a" <= c <= "z") or ("2" <= c <= "9") for c in s), (
        "s consists of lowercase English letters and digits 2 through 9"
    )
    assert "a" <= s[0] <= "z", "s starts with a letter"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
    size = 0
    for c in s:
        size = size * int(c) if c.isdigit() else size + 1
    assert k <= size, "k is at most the length of the decoded string"
    assert size < 2**63, "the decoded string has less than 2^63 letters"

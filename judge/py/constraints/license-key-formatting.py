"""License Key Formatting: a string of letters, digits and dashes, and a group size."""


def check(s: str, k: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c == "-" or (c.isascii() and c.isalnum()) for c in s), (
        "s consists of English letters, digits, and dashes '-'"
    )
    assert 1 <= k <= 10**4, "1 <= k <= 10^4"

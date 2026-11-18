"""Letter Case Permutation: a string of ASCII letters and digits."""


def check(s: str) -> None:
    assert 1 <= len(s) <= 12, "1 <= s.length <= 12"
    assert all(c.isascii() and c.isalnum() for c in s), (
        "s consists of lowercase letters, uppercase letters, and digits"
    )

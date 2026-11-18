"""Number of Beautiful Partitions: a digit string, a part count and a minimum part length."""


def check(s: str, k: int, minLength: int) -> None:
    assert 1 <= len(s) <= 1000, "s.length <= 1000"
    assert 1 <= k <= len(s), "1 <= k <= s.length"
    assert 1 <= minLength <= len(s), "1 <= minLength <= s.length"
    assert all(c in "123456789" for c in s), "s consists of the digits '1' to '9'"

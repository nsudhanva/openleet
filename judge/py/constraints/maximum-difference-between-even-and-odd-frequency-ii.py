"""Maximum Difference Between Even and Odd Frequency II: a digit string and k."""


def check(s: str, k: int) -> None:
    assert 3 <= len(s) <= 3 * 10**4, "3 <= s.length <= 3 * 10^4"
    assert all(c in "01234" for c in s), "s consists only of digits '0' to '4'"
    assert 1 <= k <= len(s), "1 <= k <= s.length"

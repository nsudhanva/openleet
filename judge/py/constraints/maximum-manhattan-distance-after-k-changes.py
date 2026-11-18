"""Maximum Manhattan Distance After K Changes: a string of N/S/E/W moves and k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert 0 <= k <= len(s), "0 <= k <= s.length"
    assert all(c in "NSEW" for c in s), "s consists of only 'N', 'S', 'E', and 'W'"

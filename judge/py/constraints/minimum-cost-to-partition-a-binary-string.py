"""Minimum Cost to Partition a Binary String: a binary string and two costs."""


def check(s: str, encCost: int, flatCost: int) -> None:
    assert isinstance(s, str), "s is a string"
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all(c in "01" for c in s), "s consists only of '0' and '1'"
    assert 1 <= encCost <= 10**5, "1 <= encCost <= 10^5"
    assert 1 <= flatCost <= 10**5, "1 <= flatCost <= 10^5"

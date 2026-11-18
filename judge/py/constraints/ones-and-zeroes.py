"""Ones and Zeroes: binary strings and the budgets of zeroes m and ones n."""


def check(strs: list[str], m: int, n: int) -> None:
    assert 1 <= len(strs) <= 600, "1 <= strs.length <= 600"
    assert all(1 <= len(s) <= 100 for s in strs), "1 <= strs[i].length <= 100"
    assert all(set(s) <= {"0", "1"} for s in strs), "strs[i] consists only of digits '0' and '1'"
    assert 1 <= m <= 100, "1 <= m <= 100"
    assert 1 <= n <= 100, "1 <= n <= 100"

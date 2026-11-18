"""Range Addition II: an m x n matrix and [a, b] operations."""


def check(m: int, n: int, ops: list[list[int]]) -> None:
    assert 1 <= m <= 4 * 10**4 and 1 <= n <= 4 * 10**4, "1 <= m, n <= 4 * 10^4"
    assert 0 <= len(ops) <= 10**4, "0 <= ops.length <= 10^4"
    assert all(len(o) == 2 for o in ops), "ops[i].length == 2"
    assert all(1 <= a <= m for a, _ in ops), "1 <= ai <= m"
    assert all(1 <= b <= n for _, b in ops), "1 <= bi <= n"

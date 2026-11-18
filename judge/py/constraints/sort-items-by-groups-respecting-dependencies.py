"""Sort Items by Groups Respecting Dependencies: n items, m groups, before-lists."""


def check(n: int, m: int, group: list[int], beforeItems: list[list[int]]) -> None:
    assert 1 <= m <= n <= 3 * 10**4, "1 <= m <= n <= 3 * 10^4"
    assert len(group) == len(beforeItems) == n, "group.length == beforeItems.length == n"
    assert all(-1 <= g <= m - 1 for g in group), "-1 <= group[i] <= m - 1"
    for i, b in enumerate(beforeItems):
        assert 0 <= len(b) <= n - 1, "0 <= beforeItems[i].length <= n - 1"
        assert all(0 <= x <= n - 1 for x in b), "0 <= beforeItems[i][j] <= n - 1"
        assert all(x != i for x in b), "i != beforeItems[i][j]"
        assert len(set(b)) == len(b), "beforeItems[i] does not contain duplicates"

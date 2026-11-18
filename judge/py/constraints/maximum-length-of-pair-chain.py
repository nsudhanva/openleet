"""Maximum Length of Pair Chain: pairs [left, right] with left < right."""


def check(pairs: list[list[int]]) -> None:
    assert 1 <= len(pairs) <= 1000, "1 <= n <= 1000"
    assert all(len(p) == 2 for p in pairs), "pairs[i].length == 2"
    assert all(-1000 <= a < b <= 1000 for a, b in pairs), "-1000 <= left_i < right_i <= 1000"

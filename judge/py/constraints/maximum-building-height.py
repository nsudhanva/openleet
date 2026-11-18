"""Maximum Building Height: n buildings and [id, maxHeight] restrictions."""


def check(n: int, restrictions: list[list[int]]) -> None:
    assert 2 <= n <= 10**9, "2 <= n <= 10^9"
    assert 0 <= len(restrictions) <= min(n - 1, 10**5), (
        "0 <= restrictions.length <= min(n - 1, 10^5)"
    )
    assert all(len(r) == 2 for r in restrictions), "restrictions[i].length == 2"
    assert all(2 <= i <= n for i, _ in restrictions), "2 <= id_i <= n"
    assert len({i for i, _ in restrictions}) == len(restrictions), "id_i is unique"
    assert all(0 <= h <= 10**9 for _, h in restrictions), "0 <= maxHeight_i <= 10^9"

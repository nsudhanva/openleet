"""Count Unguarded Cells in the Grid: an m x n grid with guard and wall positions."""


def check(m: int, n: int, guards: list[list[int]], walls: list[list[int]]) -> None:
    assert isinstance(guards, list) and isinstance(walls, list), "guards and walls are lists"
    assert 1 <= m <= 10**5 and 1 <= n <= 10**5, "1 <= m, n <= 10^5"
    assert 2 <= m * n <= 10**5, "2 <= m * n <= 10^5"
    assert 1 <= len(guards) <= 5 * 10**4, "1 <= guards.length <= 5 * 10^4"
    assert 1 <= len(walls) <= 5 * 10**4, "1 <= walls.length <= 5 * 10^4"
    assert 2 <= len(guards) + len(walls) <= m * n, "2 <= guards.length + walls.length <= m * n"
    assert all(isinstance(p, list) and len(p) == 2 for p in guards + walls), (
        "guards[i].length == walls[j].length == 2"
    )
    assert all(0 <= r < m for r, _ in guards + walls), "0 <= row < m"
    assert all(0 <= c < n for _, c in guards + walls), "0 <= col < n"
    cells = {(r, c) for r, c in guards + walls}
    assert len(cells) == len(guards) + len(walls), "all positions in guards and walls are unique"

"""Find the Number of Winning Players: n players and [player, color] ball picks."""


def check(n: int, pick: list[list[int]]) -> None:
    assert 2 <= n <= 10, "2 <= n <= 10"
    assert 1 <= len(pick) <= 100, "1 <= pick.length <= 100"
    assert all(len(p) == 2 for p in pick), "pick[i].length == 2"
    assert all(0 <= p[0] <= n - 1 for p in pick), "0 <= xi <= n - 1"
    assert all(0 <= p[1] <= 10 for p in pick), "0 <= yi <= 10"

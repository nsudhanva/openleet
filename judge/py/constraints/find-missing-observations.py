"""Find Missing Observations: m known dice rolls, a mean and n missing rolls."""


def check(rolls: list[int], mean: int, n: int) -> None:
    assert 1 <= len(rolls) <= 10**5, "1 <= m <= 10^5"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= mean <= 6, "1 <= mean <= 6"
    assert all(1 <= v <= 6 for v in rolls), "1 <= rolls[i] <= 6"

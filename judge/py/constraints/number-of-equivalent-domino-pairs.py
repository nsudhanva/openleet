"""Number of Equivalent Domino Pairs: a list of [a, b] dominoes."""


def check(dominoes: list[list[int]]) -> None:
    assert 1 <= len(dominoes) <= 4 * 10**4, "1 <= dominoes.length <= 4 * 10^4"
    assert all(len(d) == 2 for d in dominoes), "dominoes[i].length == 2"
    assert all(1 <= v <= 9 for d in dominoes for v in d), "1 <= dominoes[i][j] <= 9"

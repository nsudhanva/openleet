"""Push Dominoes: a string of L, R and . dominoes."""


def check(dominoes: str) -> None:
    assert isinstance(dominoes, str), "dominoes is a string"
    assert 1 <= len(dominoes) <= 10**5, "1 <= n <= 10^5"
    assert all(c in "LR." for c in dominoes), "dominoes[i] is either 'L', 'R', or '.'"

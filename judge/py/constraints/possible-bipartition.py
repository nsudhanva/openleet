"""Possible Bipartition: n people and unique dislike pairs [a, b] with a < b."""


def check(n: int, dislikes: list[list[int]]) -> None:
    assert 1 <= n <= 2000, "1 <= n <= 2000"
    assert 0 <= len(dislikes) <= 10**4, "0 <= dislikes.length <= 10^4"
    assert all(len(d) == 2 for d in dislikes), "dislikes[i].length == 2"
    assert all(1 <= a < b <= n for a, b in dislikes), "1 <= ai < bi <= n"
    assert len({(a, b) for a, b in dislikes}) == len(dislikes), (
        "all the pairs of dislikes are unique"
    )

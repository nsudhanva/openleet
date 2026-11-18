"""Find the Town Judge: n people and unique [a, b] trust pairs."""


def check(n: int, trust: list[list[int]]) -> None:
    assert 1 <= n <= 1000, "1 <= n <= 1000"
    assert 0 <= len(trust) <= 10**4, "0 <= trust.length <= 10^4"
    assert all(len(t) == 2 for t in trust), "trust[i].length == 2"
    assert all(1 <= v <= n for t in trust for v in t), "1 <= ai, bi <= n"
    assert all(t[0] != t[1] for t in trust), "ai != bi"
    assert len({tuple(t) for t in trust}) == len(trust), "all the pairs of trust are unique"

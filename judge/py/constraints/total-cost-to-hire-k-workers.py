"""Total Cost to Hire K Workers: worker costs, k hires and a candidates window."""


def check(costs: list[int], k: int, candidates: int) -> None:
    n = len(costs)
    assert 1 <= n <= 10**5, "1 <= costs.length <= 10^5"
    assert all(1 <= c <= 10**5 for c in costs), "1 <= costs[i] <= 10^5"
    assert 1 <= k <= n, "1 <= k <= costs.length"
    assert 1 <= candidates <= n, "1 <= candidates <= costs.length"
